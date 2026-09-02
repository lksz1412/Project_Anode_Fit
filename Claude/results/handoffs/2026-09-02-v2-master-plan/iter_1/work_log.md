# work_log — v2.0.0 마스터 플랜 초안 저작 (작업 sub · iter_1)

> 작업 sub(Fable 5.1) · 2026-09-02. 유닛 = master + 작업 sub(본 세션) + 검수 sub, 직렬. 산출 = 같은 폴더 `plan_draft.md` + 본 파일. 기존 파일 생성·수정·삭제 0 · `Codex/` 무접근 · git 명령 미실행.

---

## 1. 수행

1. brief(`Claude/results/handoffs/2026-09-02-v2-master-plan/brief.md`) 전문 정독(1–219).
2. 계획서 양식 정본 2본 전문 정독 — `skill_LKS_original_plan-execution/SKILL.md`(1–239)·`references/record-formats.md`(1–42).
3. brief §3-A 14본·§3-B 7본 전문 정독(아래 Read Coverage). §3-C 구조 확인: 마스터 tex 3본 전문·`INDEX_v25.md` 전문·`V1024_EXECUTION_LEDGER.md`(반환 15행 = 파일 전체로 보임)·`Claude/plans/*.md`·`Claude/**/HANDOVER*.md` Glob.
4. load-bearing 전제 **읽기 전용 실측**(PowerShell 2회, 파일 생성 = 산출 폴더 `iter_1` 뿐): 파일 존재(xelatex·JCP PDF·jcp_extract·dossier·도구 3본·코드·독립 부록·프리앰블·PDF 3종·sintef_data·test_skew_regsol.py·`docs/v2.0.0` 부재) · v1.0.25.1 빌드 세트 tex 60/9214줄 · 자산 카운트 전건 · `\boxed` 파일별 분포 · v1.0.25 vs v1.0.25.1 hash diff · 코드 줄수 · plans/HANDOVER/Fable/ledger 건수·줄수.
5. `plan_draft.md` 저작(11-section 순서·이름 보존 · 작업 챕터 1 = Step 단위 · 챕터 2·3 = Phase/Step 범위·게이트·중단·다음 조건 · 챕터 4~6 = Phase 목록·게이트·"3.7 확정 후 세부화" · DR-1~9 각 내용·근거·기본값·선택지 · Correction History 1행). 저작 후 자체검수 1회 — F-10 게이트(T-6·Step 7·Step 21)가 원천 규약(`HANDOVER_v24.md`:83)보다 거칠어 3곳 정정.
6. 본 work_log 작성.

## 2. 근거·판단 (4-tier)

**확정(원천 path+line)**
- 자산 카운트(brief §4.2)는 빌드 세트 60 tex(마스터 3 + `_sections` 56 + `appendix_phase_separation`)에 한정한 수치이며, 본 sub 재계수가 전건 일치했다: display 230(= `equation(*)` 228 + `align(*)` 1 + `gather/multline` 1) · boxed 64 · label 429 · bibitem 95 · cite 265/distinct 93 · section 49 · subsection 115 · figure 28 · table+longtable 20 · warnbox 14·keybox 18·bgbox 10·verifybox 15·srcbox 16·derivbox 1. `\[…\]` 38개는 230 에 포함되지 않는다(brief 미기재 — 초안에 병기). `docs/v1.0.25.1/` 를 재귀로 세면 `results/` 하위 경쟁 초안 tex 가 섞여 90 tex·boxed 116 등으로 부풀므로 빌드 세트 정의가 중요하다(초안 Phase 2.1 게이트에 반영).
- v1.0.25 vs v1.0.25.1: `_sections` 3파일(`ch1_sec05_width`·`ch1_sec06_eqpeak`·`ch3v22_sec02b_sifr`) DIFF + 마스터 tex 3본 DIFF · `appendix_phase_separation.tex` SAME · `Anode_Fit_v1.0.24.py` SAME(hash). brief §2 해석과 일치. touch-up 4건 ↔ 파일 매핑(F1·F3 → sifr / M-w → sec05_width / L-bg → sec06_eqpeak)은 `V1025_1_TOUCHUP_NOTE.md`:30–35.
- 코드 1917줄(`HANDOVER_v25.md`:134 "1917" 과 일치).
- git HEAD `4069cb3`·untracked 21 = 세션 시작 하네스 스냅샷(본 sub 는 git 명령 미실행).
- 사용자 verbatim 으로 초안에 쓴 것: brief §2 발화 6기준·추가 발화(Fable 5.1) · "v19=구문 최고·v23=논리 최고"(`VERSION_COMPARISON_v19_v23_v24.md`:3) · 헌법 3종 verbatim(`CLOSING_v1.0.15.md`:9) · DG-1/DG-2 verbatim(`plans/2026-07-26-…-plan.md`:16–17·`HANDOVER_v25.md`:46–47) · A7 사용자 지시 verbatim(:13·18·19) · F-01~F-11 사용자 지적(`USER_FEEDBACK_v1024_READING.md`). 그 밖의 "선호·권고" 는 master(brief) 또는 작업 sub 출처로 명시했다.

**원천 ≠ 요약(원천이 정본 — 초안은 원천/실측 값)**
- brief §3-A A1 `CLAUDE.md` 줄수 "90" → 실물 89행(마지막 행 89). 나머지 §3-A·§3-B 20본은 brief 줄수와 일치.
- brief §3-C "plans/ 전체 목록(90 파일·9567줄)" → 실측 `Claude/plans/*.md` = INDEX 제외 91 파일·9503줄(INDEX 65 포함 92·9568). INDEX 포함 줄수가 9567 과 ±1 이라 집계 기준 차이로 추정. 초안 §2.8 에 실측 병기.
- brief §3-C "HANDOVER*.md 28본(1612줄, old/ 제외)" → 실측 28 = old/ 3본 **포함**, old/ 제외 = 25본, 1612줄 = old/ 제외 실측과 일치. 초안 §2.8 에 병기. 또 `HANDOVER_v24.md` 가 네 폴더(v1.0.24·v1.0.24.1·v1.0.25·v1.0.25.1)에 사본으로 존재해 고유본 수는 더 적다(1.1 에서 hash 판정).
- brief §3-C 에 없는 실물: `Claude/docs/**/PLAN_*.md` 15본(v1.0.20/plans 9·v1.0.22/plans 6) + `docs/v1.0.20/plans/2026-07-16-v1020-master-plan.md`. 페이즈별 세부 계획서 실물이라 초안 1.1 Step 1 (ii) 인벤토리와 DR-7 정독 범위에 포함시켰다.
- `Claude/results/**/*LEDGER*.md` 30본(results 2·process 26·research 2). `docs/vN/results/` 안의 ledger(V1022·V1023·V1024_REFLECT·V1025_CHANGE 등 — `INDEX_v25.md`·`docs/INDEX.md` 에 언급)는 본 실측 밖 → 1.1 에서 추가 실측하도록 명시.

**추정(초안에 "추정" 표기)**
- brief 의 plans/HANDOVER 집계 차이의 원인(INDEX·old/ 포함 여부).
- 3.3 페이지 추정은 3.3 에서 산출(초안은 "추정" 열만 예약).

**미검증**
- xelatex 실행 가능·PATH · Python 패키지·SymPy 설치 · 버전 브랜치가 main 조상 · PDF 페이지 수 102/30/22(파일 존재만 확인) · 코드 release 문자열 1.0.25(코드 미정독) · 게이트 GREEN(미재실행) · `tools_check_structure.py` 가 v2.0.0 새 파일명에서 동작하는지.

**판단(작업 sub 출처)**
- Phase 2.2 청크를 `\boxed` 파일별 분포(27/10+7/16/4)로 배정한 것 — 게이트 "64/64" 를 셀 수 있게 하려는 배정이며 실제 행 범위는 세부 계획서에서 확정.
- 등록부 1.2 의 행 집합을 30 버전으로 고정한 것 — brief §4.3 계보 목록을 그대로 열거해 "누락 0" 을 계수 가능하게 함(Ch2/코드 트랙은 열에 병기).
- Non-goals 에 "기존 코드 읽기·게이트 실행(수치 대조)은 허용" 을 덧붙인 것 — brief §5 6.1 의 "코드 재현" 렌즈와 §6 "코드 동기 X" 의 경계를 명시하기 위함(DQ-9).
- DR-6 기본값을 세분한 것(DQ-6).

## 3. Read Coverage (파일 · 행 범위 — 전건)

| # | 파일 | 행 범위 | 방식 |
|---|---|---|---|
| 0 | `Claude/results/handoffs/2026-09-02-v2-master-plan/brief.md` | 1–219(전문) | Read |
| S1 | `C:\Users\lksz1\.claude\skills\skill_LKS_original_plan-execution\SKILL.md` | 1–239(전문) | Read |
| S2 | `…\skill_LKS_original_plan-execution\references\record-formats.md` | 1–42(전문) | Read |
| A1 | `CLAUDE.md` | 1–89(전문; brief 표기 90) | Read |
| A2 | `Claude/docs/INDEX.md` | 1–197(전문) | Read |
| A3 | `Claude/plans/INDEX.md` | 1–65(전문) | Read |
| A4 | `Claude/docs/v1.0.25.1/results/V1025_1_TOUCHUP_NOTE.md` | 1–62(전문) | Read |
| A5 | `Claude/docs/v1.0.25.1/results/HANDOVER_v25.md` | 1–171(전문) | Read |
| A6 | `Claude/docs/v1.0.25.1/results/HANDOVER_v24.md` | 1–89(전문) | Read |
| A7 | `Claude/results/comp_v26_data/HANDOVER_regsol_investigation.md` | 1–56(전문) | Read |
| A8 | `Claude/plans/2026-07-26-v1025-surgical-skew-consistency-plan.md` | 1–241(전문) | Read |
| A9 | `Claude/docs/Fable_점검/FABLE_AUDIT_01_history_v3-v1011.md` | 1–73(전문) | Read |
| A10 | `Claude/docs/v1.0.15/CLOSING_v1.0.15.md` | 1–106(전문) | Read |
| A11 | `Claude/results/comp_v24/USER_FEEDBACK_v1024_READING.md` | 1–207(전문) | Read |
| A12 | `Claude/results/comp_v24/VERSION_COMPARISON_v19_v23_v24.md` | 1–80(전문; 80행 = `</content>` 잔재 태그) | Read |
| A13 | `Claude/docs/v1.0.25.1/_sections/ch1_sec00_intro.tex` | 1–95(전문) | Read |
| A14 | `Claude/docs/v1.0.25.1/_sections/ch1_appE_selfconsistent.tex` | 1–218(전문) | Read |
| B1 | `Claude/docs/v1.0.18.2/ROADMAP_future_physics.md` | 1–50(전문) | Read |
| B2 | `Claude/results/comp_v24/IMPROVEMENT_DIRECTIONS.md` | 1–87(전문) | Read |
| B3 | `Claude/results/comp_v24/LIT_ADVANCE_SYNTHESIS.md` | 1–130(전문) | Read |
| B4 | `Claude/docs/v1.0.22/results/comp_v23/SURV_SYNTHESIS.md` | 1–45(전문) | Read |
| B5 | `Claude/docs/v1.0.22/results/comp_SM2/SM2_SURVEY.md` | 1–136(전문) | Read |
| B6 | `Claude/plans/2026-07-18-v1023-ratio-and-advanced-methods-plan.md` | 1–226(전문) | Read |
| B7 | `Claude/plans/2026-07-18-anodefit-MASTER-plan.md` | 1–129(전문) | Read |
| C1 | `Claude/docs/v1.0.25.1/ch1_graphite_v1.0.24.tex` | 1–62(전문) | Read |
| C2 | `Claude/docs/v1.0.25.1/ch2_lco_v1.0.24.tex` | 1–34(전문) | Read |
| C3 | `Claude/docs/v1.0.25.1/ch3_si_v1.0.24.tex` | 1–34(전문) | Read |
| C4 | `Claude/docs/v1.0.25.1/results/INDEX_v25.md` | 1–139(전문) | Read |
| C5 | `Claude/results/V1024_EXECUTION_LEDGER.md` | 1–15(limit 40 요청에 15행 반환 — 파일 전체로 보임·미확정) | Read(부분) |
| G1 | `Claude/plans/*.md` | 목록(92 = 91 + INDEX) | Glob |
| G2 | `Claude/**/HANDOVER*.md` | 목록(28) | Glob |
| X1 | PowerShell 읽기 전용 실측 ①(존재 검사·재귀 카운트·diff·plans/HANDOVER/Fable/ledger/CLOSING 목록) | — | 실행(출력 보관 = 본 로그 §2 요약) |
| X2 | PowerShell 읽기 전용 실측 ②(빌드 세트 60 tex 카운트·boxed 분포·코드 줄수·plans/PLAN_*/HANDOVER 재계수·hash) | — | 실행 |

**안 읽은 것(미검독 — 초안 §2.8 에 명시)**: plans 91 중 A8·B6·B7 외 88본 · docs/**/PLAN_* 16본 · HANDOVER 25 중 A5·A6·A7 외 22본 · Fable 감사 8 중 A9 외 7본 · `_sections` 56 중 A13·A14 외 54본 · 코드 전문 · PDF 3종 · comp_v24 나머지 · comp_v26_data 나머지 · v1.0.25.1/results 나머지 · ledger 30 중 C5 외 · dossier · jcp_extract · JCP PDF · `_archive/`·`old/`.

## 4. 산출 파일

- `D:\Projects\Project_Anode_Fit\Claude\results\handoffs\2026-09-02-v2-master-plan\iter_1\plan_draft.md` — 11-section 마스터 플랜 초안 v1.
- `D:\Projects\Project_Anode_Fit\Claude\results\handoffs\2026-09-02-v2-master-plan\iter_1\work_log.md` — 본 파일.
- 그 밖의 파일 생성·수정·삭제 = 0(폴더 `iter_1` 생성만).

## 5. Decision Queue (골격 이견 · brief 오류 · 추가 후보 — master 승격 판단)

| ID | 종류 | 내용 | 근거 | 초안 처리 |
|---|---|---|---|---|
| DQ-1 | brief 오류(경미) | §3-C 건수: plans "90 파일·9567줄" → 실측 91(INDEX 제외)/92·9503/9568 · HANDOVER "28본(1612줄, old/ 제외)" → 28 은 old/ 포함, old/ 제외 25·1612줄 | X1·X2 실측 | §2.8 에 실측 병기 · 1.1 Step 1 에서 정본화 |
| DQ-2 | 추가 후보 | `docs/**/PLAN_*.md` 15 + `docs/v1.0.20/plans/2026-07-16-v1020-master-plan.md` 를 이력 인벤토리·DR-7 정독 범위에 포함 | X2 실측(brief §3-C 미기재) | 1.1 Step 1 (ii)·DR-7 비용에 포함 |
| DQ-3 | 정의 기록 | "display 수식 환경 230" = equation/align/gather/multline 집계(228+1+1) · `\[…\]` 38 별도 | X2 | §2.2 표에 병기 |
| DQ-4 | 추가 후보(파일명) | 등록부·레지스터·블루프린트·인벤토리·서지 원장 파일명 제안: `V2_HISTORY_INVENTORY.md` · `V2_REG1_VERSION_CHANGES.md` · `V2_REG2_BINDING_DECISIONS.md` · `V2_REG3_LOST_DIRECTIONS.md` · `V2_GAP_REGISTER.md(+.json)` · `V2_THEORY_BLUEPRINT.md(+.json)` · `docs/v2.0.0/results/V2_REFERENCE_LEDGER.md` — `Claude/results/V1024_*` 접두 관행 승계 | brief §7 미규정 | §Implementation Changes 에 "제안" 표기 |
| DQ-5 | 추가 후보(파일명) | Result topic 토큰 제안: HISTORY / GAP / BLUEPRINT / BIB / CLOSING (`PHASE_<id>_V2_<topic>_RESULT.md`) | brief §7 `<topic>` 미지정 | Phase 절에 사용 |
| DQ-6 | 기본값 세분(이견) | DR-6 기본값을 brief "읽기 전용 허용" 일괄에서 "(i) 문헌 검색·(ii) Crossref 허용 · (iii) 공개데이터 재다운로드는 2.6 진입 시 재확인" 으로 세분 — 다운로드는 파일 생성·출처 기록·스크립트 실행과 결합돼 별도 확인이 안전하다는 sub 판단. brief 기본값 유지도 가능 | A7 §⑤(GITT 다운로드 = 스크립트 실행과 결합) | DR-6 에 sub 제안으로 표기 |
| DQ-7 | 범위 확인 | 2.6 에서 `results/comp_v26_data/test_skew_regsol.py` 를 **실행**할지 — brief 는 "정식화" 만 요구. 실행 시 결정 입력이 풍부해지나 코드 실행·데이터 다운로드가 따른다 | brief §5 2.6 · A7 | "실행 여부 = DR-6·DQ" 로 유보 |
| DQ-8 | 새 의존성 예고 | T-12(SymPy 재유도)에 SymPy 필요 — 설치 여부 미검증. 부재 시 새 의존성 = 정지 조건 | Assumptions 7 | 사전 확인 권고(GO 전 1g 대조 항목) |
| DQ-9 | 경계 확인 | 6.1 "코드 재현" 렌즈 vs Non-goal(코드 수정 X) — 초안은 "기존 코드로 회수 가능한 식의 수치 대조, 코드 수정 없이" 로 한정 | brief §5 6.1·§6 | Non-goals·6.1 에 명시 |
| DQ-10 | 보강(이견 아님) | 3축 대응을 5축(작업 챕터 / 문건 Chapter / ver.N / CLAUDE.md P1 원구상 Chapter 1~5 / 3.3 후보 신구조)으로 확장 | P3 #7 · `CLAUDE.md`:14–17 | Phase Range 상단 표 |
| DQ-11 | 범위 밖 기록 | `plans/INDEX.md` 스테일 표기(v1.0.23~v1.0.25 구간) 전면 재정렬은 brief 범위 밖 — I-2 는 "행 추가만" | A3:5–8 | 별도 작업으로 DQ |
| DQ-12 | 미검증 예고 | `tools_check_structure.py`·`tools_tex_strict_check.py` 가 v2.0.0 새 폴더·파일명에서 인자만으로 동작하는지 미검증 — 안 되면 도구 사본을 `docs/v2.0.0/results/` 에 두고 인자 갱신(원본 무수정) | Assumptions 6 | 4.0 게이트에 "도구 동작 확인" 포함 |
| DQ-13 | 원천 결함 기록 | `VERSION_COMPARISON_v19_v23_v24.md` 80행에 `</content>` 잔재 — 원천 무수정 원칙상 손대지 않음 | A12:80 | 기록만 |
| DQ-14 | 인벤토리 규칙 | `HANDOVER_v24.md` 사본 4곳(v1.0.24·v1.0.24.1·v1.0.25·v1.0.25.1) — hash 로 고유본 판정 후 고유본만 정독 | G2 | 1.1 Step 1 (iii) |
| DQ-15 | 범위 확인 | 2.2 판정 대상 = boxed 64 만(brief). 비박스 display 166 은 스크리닝(Step 16)으로 한정 — 전수 판정 확장 여부는 비용이 커 master 판단 | brief §5 2.2 | Step 16 스크리닝 |
| DQ-16 | 자체검수 정정 기록 | F-10 게이트(T-6·1.3 Step 7·2.5 Step 21)를 FB3 집행 규약(`HANDOVER_v24.md`:83 — 요동/양성 → 영문 body 0 · 음함수/섭동/준위 → 국문 + 첫 병기 · 유일근 → "유일한 근")대로 정정함. 초안 v1 저장 후 Edit 3건 | A6:83 | 반영 완료 |
| DQ-17 | 확인 요청 | Non-goals 의 "회사 데이터 의존 정량 X" 항목 — brief §6 문구 그대로이나 초안은 Task #38 세부(stage-2L 0.30 mV/℃·Ω 점값·LCO 전자항 T-의존·α↔$L_V$)를 `HANDOVER_v25.md`:122 에서 보강 인용. 골격 변경 아님 | A5:122 | 보강 인용 |

## 6. 미해결

- brief §3-C 건수 불일치(DQ-1)의 집계 기준 — master 확인.
- `docs/vN/results/` 안의 ledger·MERGE_READINESS·CHANGE_LEDGER 건수·줄수 — 미실측(1.1 에서).
- SymPy 설치 여부·xelatex PATH — 미검증(GO 전 1g 대조).
- DR-1~DR-9 — 사용자 결정 대기. DG-A/B/C — 3.7 에서 정지.
- 검수 sub 감사 → master 삼각검증·통합 → `Claude/plans/2026-09-02-v2-master-plan.md` 저장(master 소관).
