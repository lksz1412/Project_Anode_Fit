# critic — v2.0.0 마스터 플랜 초안 v3 완결성 비평 ("무엇이 빠졌는가")

> 작성 = 「v2.0.0 수식 연구 진보 마스터 플랜」 워크플로의 완결성 비평 에이전트 [critic](Fable 5.1), 2026-09-03. 대상 = `wf/plan_draft_v3.md`(860행 전문). 대조 원천 = `brief.md`(§2 사용자 verbatim·§5 골격·§8 DR)·`wf/fix_change_log.md`·감사 3본(`wf/audit_spec.md`·`audit_format.md`·`audit_logic.md`)·`audit_checklist.md`·판독 R1~R7(전문)·`skill_LKS_original_plan-execution/SKILL.md`(11-section 정본). 산출 = 본 파일 1건. 기존 파일 생성·수정·삭제 0 · `Codex/` 무접근 · git 명령 미실행.
> 규약 = 4-tier(**확정** / **근거 미발견** / **추정** / **미검증**), 확정에는 path+line. "사용자 결정·지적" 은 brief §2 verbatim 과 원천이 사용자 결정으로 기록한 항목에만 쓰고, 그 밖의 판정은 전부 본 critic 의 판단이다. 행 번호 `:n` 은 별도 표기가 없으면 `wf/plan_draft_v3.md` 의 Read 표시 행이다.
> 본 critic 은 원천 실물(tex·md·PDF) 을 열지 않았고, 판독 산출이 옮긴 path:line 의 정오는 판정하지 않았다(Assumptions 19 와 같은 한계). 다만 Assumptions 의 1g 검증 가능성을 확정으로 바꾸기 위해 읽기 전용 실측 5건(Glob 4·PowerShell 1)을 수행했다(§7).

---

## 0. 판정 요약

초안 v3 는 사용자 기준 1)~6) 전건에 Phase·게이트·검수 렌즈로 이어지는 구현 경로를 갖고, 판독 R1~R7 의 Decision Queue 97건과 key finding 은 한 건도 통째로 누락되지 않았으며, cumulative step 1–50 은 리셋·중복·건너뜀 없이 단조이고, 11-section 이름·순서는 정본(`SKILL.md:69`)과 일치한다. 감사 55건은 fixer 가 전건 반영했고 부분 반영 4건의 사유는 세 건이 타당하나, **LOGIC-02 의 "실제 충돌 0" 주장은 틀렸다** — Test Plan 의 `T-1`·`T-2`(빌드·구조 검사)와 R6 후보 `T-1`·`T-2`(entropy production·선형 flux–force)가 같은 문서 안에서 두 의미로 공존한다(HIGH 1건). 그 밖에 4.x 게이트의 boxed 회수 수치가 현행 장 소속 기준이라 (b) 구조와 어긋나는 점(MED), 판독 path:line 정확성 전제에 GO 전 대조 절차가 없는 점(MED), F-01 재판정이 어느 Step 에도 없는데 게이트 1.3 이 "미검증 0" 을 선언하는 점(MED), 유실 자산 원문 4건의 실물 존재가 Assumptions 에 없는 점(MED — 본 critic 실측으로 존재 확정) 이 남는다. CRIT 는 없고 골격·Step·section 은 무결하므로, 아래 §9 목록을 master 통합 시 반영하는 조건으로 **master 통합 진입 가능**으로 판정한다.

| 판정 항목 | 결과 | 근거 절 |
|---|---|---|
| 기준 1)~6) 구현 경로 | 전건 있음(빠진 기준 없음 — 하위 항목 2건 LOW) | §1 |
| 판독 R1~R7 미반영 | 통째 누락 0 · 개별 Step 미지정 5건(LOW·MED 1) | §2 |
| fixer 기각·부분 반영 타당성 | rejected 0 · 부분 4건 중 3 타당·1 불충분(LOGIC-02) | §3 |
| cumulative step 단조성 | 단조 · 리셋 0 · 중복 0 · 건너뜀 0 | §4 |
| 11-section 순서 | 보존(부록 3절은 11-section 밖으로 표제 명시) | §5 |
| Decisions Required 완비 | DR-1~23 전건 4요소 보유 · orphan 포인터 1(S0–S5) | §6 |
| Assumptions 1g 검증 가능성 | 22항 중 18 검증 가능 · 3 이연(19·20·21) · 누락 1(유실 원문 실물) | §7 |

---

## 1. 사용자 기준 1)~6) ↔ 구현 경로 대조

brief §2 verbatim(brief:36–41)의 여섯 기준을 초안의 진단·설계·저작·검수·Test Plan 에서 추적했다. "있음" 은 Phase 와 확인 가능 게이트가 모두 실재함을 뜻한다.

| 기준 | 진단 | 설계 | 저작 게이트 | 검수·Test Plan | 판정 · 근거 |
|---|---|---|---|---|---|
| 1) 비약·누락·생략 없는 유도(80~90%) | 2.2 Step 16–20 boxed 64 4단 척도·비박스 15 라벨·GAP-ID(:362–374) | 3.4 Step 44 (a)~(d) 사슬 계획(:466) | 4.x "(a)~(d) 사슬 100%"(:498)·T-8(:559) | 6.1 follow 변형(산문 가림) + proxy 명기(:520)·T-12 SymPy 64/64(:563)·DR-22 하한(:744–748) | **있음** — proxy 한계를 Summary :18 에 정직 표기 |
| 2) 대학원 교재 수준 형식 | 2.5 Step 27 체크표(:400) | 3.3 구조안(:459) | 4.0 `\newtheorem` 신설(:497)·T-20 절별 O/X(:571) | 6.2 T-20 전건(:521) | **있음** — 단 T-20 에 "연습문제" 지위(포함/제외)가 없음(§9 #10, LOW) |
| 3) 리뷰 논문급 레퍼런스 | 2.4 Step 24–26 95/95·원장 체인·밀도(:390–392) | 3.5 Step 47–48 규약 10조항·문헌 맵(:474–475) | 4.1 "신규 서지 V1 등재"(:498) | 5.1~5.2 DOI 전수·한 문헌 한 키·저자 전원·무인용 절 0(:512–513)·T-9·T-16(:560·:567) | **있음** |
| 4) 타전공 석박사 청중 | 2.5 Step 29 가독성 7항목(:402) | — | 4.0 두문자어 표·용어 결정표(:497)·T-21(:572) | 6.1 usable 입력 = T-21(:520) | **있음** |
| 5) 최대 일반식 → 레퍼런스 확실한 가정으로 간소화 | 2.3 Step 21–23 간소화 65×6열·계보도·부재 단(:380–384) | 3.2 Step 38–41 사다리 3축·매핑 64/64(:448–453)·3.4 T-19 계획판(:470) | 4.1~4.9 T-19 절별(:498–506) | 6.2 T-19 전건(:521) | **있음** |
| 6) 사용자 계획 스킬·지침 준수(마스터플랜–세부계획서–작업이력서)·효율보다 완성도 | Interfaces 유닛 직렬·역할 경계·5항목 고지(:531–533) | 기록 3계층·재독 강제·정지 조건·git 페어(:534–537) | 4.x 절 단위 루프·통째 배치 금지(:493) | DR-7 (i) 기본값(:653–657)·DR-23(:750–754)·T-10·T-11·T-14 | **있음** — 세부 계획서 3단 구분이 헤더 :4 에 고정됨(스킬 1e `SKILL.md:86` 와 합치) |

기준 6 의 하위 요구 "마스터플랜 - 세부계획서 - 작업이력서" 는 OUT-DETAIL(:276)·OUT-STEP(:285)·OUT-RESULT(:286)·OUT-LEDGER(:287) 로 산출물 대장에 박혀 있고, 매 Phase Result 편입(fixer FORMAT-01 처리)으로 스킬 2b(`SKILL.md:165`)·헌법 §0 "Result 생략 금지" 와도 합치한다. 빠진 기준은 없다.

---

## 2. 판독 R1~R7 key finding · Decision Queue 대조 — 미반영 목록

각 판독 파일의 Decision Queue 전건과 본문 key finding(요지·유실 표·후보 등급·규약 초안)을 초안의 Phase·Step·DR·부록 A 처리표와 대조했다. 부록 A (B) 표(:790–802)는 판독 DQ 97건의 처리처를 전건 명시하고 있고, 본 critic 이 각 처리처를 초안 본문에서 실물로 확인한 결과 **처리처가 비어 있는 DQ 는 0건**이다. 아래는 key finding 가운데 "1.4 등록부 시드로 흡수된다" 는 일반 규정에만 기대고 개별 Step·게이트 지정이 없는 항목이다(주장의 출처는 판독 파일 path:line).

| # | 출처 | key finding | 초안 반영 상태 | 판정 |
|---|---|---|---|---|
| K-1 | R3 A-4 F-01 행(`R3_binding_decisions_and_lost_directions.md:85`) "절은 유지됨 … 축약·강등 여부 미검증 → 작업 챕터 2.5 에서 (a)(b) load-bearing / (c)(d) 배경의 분리 재판정" · R3 A-6 D21-2(`:126`) "F-01 재판정과 연동" | 1.3 Step 8 은 "미검증 2건 해소 = F-04·F-08"(:331)만 다루고, 게이트 1.3 은 "미검증 0(F-04·F-08·D21/D22 상세 해소)"(:334)을 선언 · 2.5 Step 27~29(:400–402)에 F-01 항목 없음 | **미반영(MED)** — 게이트 1.3 의 "미검증 0" 이 F-01 을 빠뜨린 채 성립 |
| K-2 | R3 B-1(`:186`) "LCO 장 산문 비율 별도 계측 권고(2.2)" | 2.2 Step 19(:371)·2.5 Step 27(:400)에 산문 비율 계측 없음 | 미반영(LOW) — 형식 요소 O/X 로 대체 가능하나 정량 지표는 아님 |
| K-3 | R2 P-7(`R2_version_register_v1020_to_v1026.md:233`) "양 버전 샘플 이미지 QA(연속·매끄러움·미분가능성) → 6.1 실행 기반 검증 렌즈" | 6.1(:520)의 실행 기반 검증 렌즈 = SymPy·수치 극한·코드 수치 대조 — 렌더 이미지 QA 항목 없음 · 1.1 Step 1 (xiv) 는 untracked 이미지의 지위만(:303) | 미반영(LOW) |
| K-4 | R3 A-9(`:170`) 북극성·M 통찰("M = 브로드닝으로 낮아진 피크가 dV/dQ 에서 커진 것처럼 보인 상황을 억지로 맞춘 인자")을 "v2.0.0 이론 진보의 동기 층으로 승계" | 3.1 축 목록(:426–432)·4.0(:497) 어디에도 M 통찰·dQ/dV↔dV/dQ 높이 관계(캠페인 A-1) 언급 없음 | 미반영(LOW) — 서론·4.0 동기 층 1문단 후보 |
| K-5 | R1 L-14(`R1_version_register_v3_to_v1019.md:146`) staging 'w'+'n' 중복 키 → "문건 서술(폭 폴백 지위)은 2.5 register 감사 대상" · L-15(`:147`) tab:notation N3 재배열 · L-18(`:150`) N6a/N6b 서브라벨·W2-2 orphan 라벨 | 1.4 Step 10 "R1 §5 전건" 시드(:340)로만 흡수 · 2.5·2.1 개별 항목 없음 | 미반영(LOW) — 낮은 우선순위이나 2.1 라벨 검사(orphan 라벨)·2.5 폭 폴백 서술은 한 줄로 배정 가능 |

R1 DQ-1~10·R2 DQ-1~12·R3 DQ-1~16·R4a DQ-1~10·R4b DQ-1~10·R5 DQ-1~12·R6 DQ-1~12·R7 DQ-1~15 는 부록 A (B) 표의 처리처(DR 승격 / Step 흡수)가 본문에서 전건 실재함을 확인했다(확정 — 예: R2 DQ-5 → 2.6 Step 30 (a) :410, R7 DQ-13 → 3.5 Step 48 :475, R6 DQ-12 → 2.6 Step 31 (v) :411, R5 DQ-9 → 3.1 승계 표 :434 "#2 α opt-in(단 함수형이 원 제안 양측 폭과 다름 — R5 DQ-9)"). 판독 등급(R5 §4 A 6·B 10·C 11 / R6 §7 A 7·B 10·C 7)은 3.1 Step 34(:437)에 A 13·B 20 명단으로 전건 전사됐고, R5 §2 23단·R6 §5 6 rung 은 2.3 Step 23(:382)·3.2 Step 38–39(:448–449)에, R7 §5 10조항은 3.5 Step 47(:474)에, R4b G01~G42 는 2.2 Step 19(:371) 표적과 GAP-ID 별칭 열(:368)에 들어 있다.

---

## 3. 감사 55건 처리 검증 — fixer 부분 반영 4건의 타당성과 잔존 결함

`fix_change_log.md:12–14` 는 반영 51·부분 4·rejected 0 이다. rejected 가 0 이므로 "기각 사유" 는 부분 반영 4건의 이견 사유로 읽는다. 아울러 감사 원문(3본)을 직접 읽어 초안 v3 에 실제 반영됐는지 표본 대조했다.

| ID | fixer 이견 사유(`fix_change_log.md`) | 본 critic 판정 | 근거 |
|---|---|---|---|
| SPEC-04 | 감사 "Claude 10·Codex 11" 을 스냅샷 재계수 8·13 으로 정정(`:29`) | **타당(확정)** | 세션 git status 스냅샷: Claude 측 = png 5 + `process/C3_graph_check/`·`C3_pdf_render/` + `regsol_test/` = 8 · `Codex/work/` 하위 13 폴더 = 13 · 합 21 |
| LOGIC-02 | 판독 ID 전건 접두 대신 산출물 ID `OUT-` 재명명 + 이름공간 규약 + 충돌 지점만 `R2:` 접두 — "실제 충돌(같은 문서 안 두 의미) 0"(`:62·:98`) | **불충분(HIGH)** — 충돌 1쌍 잔존 | Test Plan `T-1` LaTeX 빌드·`T-2` 구조 검사(:552–553) vs R6 후보 `T-1` entropy production·`T-2` 선형 flux–force(Summary :31 "T-1 entropy production 일반 상태식", 3.1 :429·:434, 3.2 Step 39 :449 "T-2 warnbox 필수", 4.1 :498 내용 열 "T-1 …·T-2 …" 와 같은 행 게이트 열 "T-19/T-20/T-21", Step 40 :450 "Q-1·Q-2"). 이름공간 표 :221 은 `K/E/T/R/S/H/Q-x = R6 후보` 로만 선언하고 Test Plan `T-n` 을 등재하지 않아, 독자가 3.2 Step 39 의 "T-2 warnbox 필수" 를 구조 검사 T-2 로 오독할 수 있다. LOGIC-02 가 지목한 유형("같은 문서 안 두 의미")이 그대로 남았다 |
| LOGIC-10 | v1 참조를 삭제하지 않고 헤더에서 `iter_1/plan_draft.md` 로 정의(`:70·:99`) | **타당** — Correction History v1 행(:607)이 v1 이름을 요구하므로 삭제 불가 · master 저장 시 분리 판단은 DQ-I13 에 있음 | 헤더 :3 정의 · §2.0 원천 코드표 :39–68 재수록으로 brief 코드 orphan 은 해소됨 |
| FORMAT-01 | Result 를 Step 추가 없이 각 Phase 마지막 Step 의 다음 조건에 편입, 1.5/2.7/3.7 은 챕터 통합 Result(`:39·:100`) | **타당(조건부)** — 스킬 2b 는 Result 를 Step 으로 강제하지 않음(`SKILL.md:165` "매 Phase 종료 시 …") · brief §5 골격 확장이므로 DQ-I14 master 확인이 붙어 있음 | 1.1~3.6 각 "다음 조건" 에 `PHASE_<id>_V2_<topic>_RESULT.md`+`.json` 실재(:309·:325·:334·:344·:360·:374·:384·:394·:404·:413·:442·:453·:462·:470·:477·:483) · T-14 "Result 쌍 = 종료 Phase 수"(:565) · Ledger 행 5(:348) 정합 |

표본 대조 결과 감사 권고가 실제로 들어간 것을 확인한 항목: FORMAT-03 중단 조건(2.3~3.6 전건 :384·:394·:404·:413·:418·:462·:470·:477·:483) · FORMAT-07 열 수 이름 열거(1.4 6열 :344 · 3.1 8열 :437 · 3.3 10항목 :462) · FORMAT-13 Assumptions 22(:601) · FORMAT-14 T-1/T-2 PowerShell 형(:552–553) · FORMAT-20 commit 페어(:537) · FORMAT-22 D21 ≥5(:334) · LOGIC-05 23단(:382) · LOGIC-06 57/57(:462) · LOGIC-11 [MODEL-1] 시점(:137·:703) · LOGIC-15 8항·D1~D4·≈0.96(:153·:332·:411) · LOGIC-18 Step 14 마스터 3본+지원 4본(:357) · LOGIC-20 FB0~FB7·H-1·청크 창·렌즈셋 6종(:331·:437·:374·:348) · SPEC-08 proxy(:18·:520) · SPEC-12 diff hunk 4건(:418) · SPEC-13 F-02/F-03 grep(:404·:497·:557) · FORMAT-18 3/3·4/4·64/64(:499·:500·:506) · FORMAT-21 Assumptions 19 상충 목록(:598). 55건 가운데 반영 흔적을 찾지 못한 항목은 없다(확정).

---

## 4. cumulative step 단조성

Phase Range 표(:225–246)와 각 Phase 본문의 Step 번호를 전건 대조했다.

| 챕터 | Phase → Steps(표) | 본문 Step 실재 | 판정 |
|---|---|---|---|
| 1 | 1.1 1–2 · 1.2 3–7 · 1.3 8–9 · 1.4 10–12 · 1.5 13 | Step 1·2(:303–306) · 3·4·5·6·7(:319–323) · 8·9(:331–332) · 10·11·12(:340–342) · 13(:348) | 1–13 연속 |
| 2 | 2.1 14–15 · 2.2 16–20 · 2.3 21–23 · 2.4 24–26 · 2.5 27–29 · 2.6 30–31 · 2.7 32 | 14·15(:357–358) · 16~20(:368–372) · 21~23(:380–382) · 24~26(:390–392) · 27~29(:400–402) · 30·31(:410–411) · 32(:417) | 14–32 연속 |
| 3 | 3.1 33–37 · 3.2 38–41 · 3.3 42–43 · 3.4 44–46 · 3.5 47–48 · 3.6 49 · 3.7 50 | 33~37(:436–440) · 38~41(:448–451) · 42·43(:459–460) · 44~46(:466–468) · 47·48(:474–475) · 49(:481) · 50(:487) | 33–50 연속 |
| 4~6 | "51–"(:244) · "(4 에 이어 연속)"(:245) · "(5 에 이어 연속)"(:246) — 3.7 확정 후 세부 계획서에서 부여(:158) | — | 리셋 없음 선언 |

리셋·중복·건너뜀 0(확정). §2.7(:158)의 "챕터 1 Steps 1–13 · 챕터 2 14–32 · 챕터 3 33–50" 과 Correction History v2 행(:608)·Phase Range 주석(:248 "13 / 19 / 18")·부록 A (B) 표의 Step 참조(예: 1.2 Step 6, 2.2 Step 20, 3.4 Step 45, 3.5 Step 48)가 전부 위 표와 일치한다. 사소한 불일치 1건: 1.2 Step 3 "행 1~21"·Step 4 "행 22~31"(:319–320)의 행 분할이 실제 필수 행 배분(R1 구간 22 = RB·Fable v2·v3~v10 8·v1.0.10·v1.0.11·Fable 이력감사·v1.0.12~v1.0.19 9 / R2 구간 9 = v1.0.20~v1.0.26)과 1 어긋난다 — 게이트 36/36 에는 무영향(§9 #7, LOW).

---

## 5. 11-section 순서

`## ` 헤딩 실측: Summary(:12) → Current Ground Truth(:35) → Phase Range(:210) → Non-goals(:252) → Implementation Changes(:269) → Phase 1.1~6.3(:297~:516) → Implementation Interfaces(:526) → Test Plan(:546) → Assumptions(:576) → Correction History(:605) → Decisions Required(:613). 정본 `SKILL.md:69` 의 순서·이름과 일치하며 개명 없음(확정). 그 뒤 `## 부록(11-section 밖 · handoff 전용 — master 가 … 분리한다)`(:760) 아래 `### 부록 A/B/C` 가 있다 — 12번째 `##` 헤딩이 파일에 존재하지만 표제 자체가 분리 지시를 담고 있고 DQ-I13·FORMAT-12 처리로 기록돼 있어 순서 위반으로 보지 않는다. 비코드 프로파일(Implementation Changes = 산출물 대장·Implementation Interfaces = 운용·Test Plan = 실제 게이트)은 brief §9 규격대로다. Phase 4.0~4.9·5.1~5.3·6.1~6.3 을 묶음 헤딩으로 둔 것은 brief §9 "챕터 4~6 은 Phase 목록·게이트·'3.7 확정 후 세부화' 명시" 와 스킬 1e(`SKILL.md:86` "진행 중인 Phase 만 최신 유지")에 합치한다.

---

## 6. Decisions Required 완비 대조

DR-1~DR-23 각각에 내용·근거·기본값·한 줄 응답 선택지 4요소가 있는지 확인했다(:617–754). 23건 전건 4요소 보유(확정). brief §8 의 DR-1~DR-9 는 전건 승계되고 판독 반영으로 갱신됐다(DR-1 v1.0.26 상태 정정 :619 · DR-6 R7 기실행 :648 · DR-7 세 선택지 :654 · DR-8 dossier vs PDF :660). DR-10~23 은 판독·감사가 드러낸 결정이며 각각 원천 path:line 근거를 갖는다.

남은 결함 두 가지는 모두 경미하다. 첫째, Non-goals 의 S0–S5 bullet(:263)이 "DR-16 인접" 이라 가리키나 DR-16 본문(:708–712)에는 S0–S5 언급이 없다 — FABLE §5-8 명시 결정 5건 가운데 Eyring(DR-16)·§1.18(DR-17)·KWW(DR-15)·자기완결(DR-22·Assumptions 20)은 DR 가 있고 S0–S5 본문 편입만 1.4 Step 12 명시 결정 대기 표 → DG-B(:342) 로만 간다. 결정 자체가 3.7 에서 닫히므로 blocking 은 아니나 포인터는 orphan 이다(§9 #6, LOW). 둘째, DR-6 의 기본값 문면에 있는 하위 결정 "R7 Crossref 조회 결과 승계 vs 본 arc 재조회"(:648·:650)가 응답 선택지(:651)에 노출되지 않아 사용자가 `전부 허용` 을 택하면 승계가 암묵 승인된다(§9 #13, LOW).

---

## 7. Assumptions(1g 실물 대조 대상)의 검증 가능성

스킬 1g(`SKILL.md:100`)는 실행 직전 Current Ground Truth·Assumptions 의 load-bearing 전제를 Glob/Read 로 대조하라고 한다. Assumptions 1–22(:580–601)를 "GO 전에 명령 하나로 참/거짓을 가릴 수 있는가" 로 판정했다.

| 항목 | 검증 수단 | 판정 | 본 critic 실측(읽기 전용) |
|---|---|---|---|
| 1 xelatex 경로·실행 | Test-Path + `& xelatex --version` | 가능(명령 미기재) | `Test-Path` **True**(확정) |
| 2 동결 base·카운트 | T-4 스크립트 | 가능 | — |
| 3 diff 3파일 | diff/hash | 가능 | — |
| 4 `docs/v2.0.0/` 부재 | Glob | 가능 | 부재 **확정**(Glob 0건) |
| 5 JCP PDF·extract·dossier 존재 / refs 6·7 미소장 | Test-Path / Glob(`*121102*`·`*164123*`) | 가능(미소장 쪽 명령 미기재) | — |
| 6 도구 3본 | Test-Path | 가능 | — |
| 7 Python·패키지·SymPy | `python -c "import …"` | 가능(명령 미기재) | Python **3.12.10** · sympy **1.14.0** · numpy/scipy/matplotlib/pandas import **OK**(확정) — "SymPy 미검증" 은 "설치 확인" 으로 갱신 가능 |
| 8 git HEAD·tracked 0·조상 | `git rev-parse`·`git merge-base --is-ancestor`(master 전용) | 가능 | — |
| 9 전원 Fable 5.1 | 세션 모델 ID | 운용 전제 | — |
| 10 부록 E ② 유보·dossier 행 | Read | 가능 | — |
| 11 이력 규모 ≈12,400줄 | Get-ChildItem 합산 | 가능 — 단 열거 합(9503+1612+885+106+401 = 12,507)이 12,400 을 넘음(§9 #8) | — |
| 12 brief §3-C 건수 차이 | 카운트 | 가능 | — |
| 13 SM2-A/B/C 집행 | grep 자산 태그 | 가능 | — |
| 14 sintef_data·comp_v26 CSV | Test-Path | 가능 | — |
| 15 PDF 102/30/22p | pdfinfo/PyPDF | 가능(명령 미기재·"미열람") | — |
| 16 Codex 무접근 | 규약 | — | — |
| 17 v1.0.26 실물 | Test-Path | 가능 | — |
| 18 Crossref 접근 | Invoke-RestMethod | 가능(DR-6 종속) | — |
| 19 판독 path:line 정확 | **GO 전 절차 없음** — "1.1~1.2·2.1~2.5 에서 실물 재대조"(:598) | **이연(MED)** — §2.2~§2.6 의 게이트 기준 좌표 전부가 이 전제 위 | — |
| 20 긴장 해소 | 사용자 확인(DR-22) | 결정 사항 | — |
| 21 [C-92] 등 서브 판단 | 1.3 Step 9 | 이연(근거 미발견 표기 정직) | — |
| 22 신규 예정 파일 부재 | Glob | 가능 | `plans/2026-09-02-v2-master-plan.md`·`results/PHASE_1-6_V2_EXECUTION_LEDGER.md`·`results/V2_*.md`·`results/PHASE_*_V2_*`·`docs/v2.0.0/**` **전건 부재 확정**(Glob 0건) · `Claude/results/Step *` **0건**(이전 arc 와 파일명 충돌 없음 — `results/process/V1014_STEP11_APPLY.md` 류는 다른 명명이라 무관) |

누락된 load-bearing 전제 1건: **유실 자산 원문 4건의 실물 존재**. 1.4 Step 11 (i)(:341)와 DR-15/16/17(:703·:709·:717)은 Fable v2 tex·Opus v5/v6 §1.15·v3/v4/v5 §1.10·Opus v4 §1.18 정독을 전제하면서 "실물 경로 1.1 확정·미정독이면 원문 미정독 표기" 로 열어 두었고 Assumptions 에는 항목이 없다. 본 critic Glob 실측: `Claude/old/_archive/graphite_ica_ch1_Fable_v2.tex`·`graphite_ica_ch1_Fable_v3.tex`·`graphite_ica_ch1_Opus_v4.tex`·`graphite_ica_ch1_Opus_v5.tex`·`graphite_ica_ch1_Opus_v6.tex` 5본 **존재 확정**. R1 L-19(`R1…:151`) 의 "INDEX `_archive/` 목록에 Fable v1/v2 명시 없음" 은 INDEX 표기의 문제이지 실물 부재가 아니다. Assumptions 에 경로를 넣고 Step 11 (i) 의 유보 문구를 갱신할 수 있다(§9 #5, MED — 실물은 있으므로 STOP 사유는 아님).

---

## 8. 그 밖의 발견(골격·게이트 정합)

**8.1 4.x boxed 회수 게이트의 기준 좌표(MED).** 4.6 흑연 적용 게이트 "boxed 회수 27/27"(:503)·4.7 "16/16"(:504)·4.8 "4/4"(:505)·4.4 "10/10"(:501)·4.2 "독립 부록 3/3"(:499)·4.3 "부록 E 4/4"(:500)는 §2.2 의 **현행 장 소속 분포**(27+10+4+3+16+4)를 그대로 Phase 게이트로 옮긴 것이다. 그러나 4.x 표 자체가 "기본 골격 = 3.3 (b) 기준"(:493)이고, (b) 에서는 Ch1 곡선 사슬 27 가운데 Part 0 boxed(sec02a 5·sec02b 4 — `R4a…:21–22`)와 §3 eq:Uj·§4 eq:dUhys·§5 eq:tst-box·eq:xieq·§6 eq:eqpeak·§8·§9 lag/tail 의 일반 유도가 4.1~4.5 로 이동한다 — 4.2 내용 열이 "중심(eq:Uj …)·폭·정칙용액…"(:499)을 스스로 적고 있다. 곧 4.6 이 27 을 회수할 수 없고 4.2·4.3·4.5 게이트에는 그 몫의 건수가 없다. 4.3 에만 "위치 = DG-A; 4.9 승계 시 4.9 계수" 이관 규칙(:500)이 있고 4.6↔4.1~4.5 사이에는 없다. 4.9 의 합 64/64(:506)와 6.2(:521)는 유지되므로 무유실 원칙은 지켜지지만, Phase 별 게이트는 3.2 Step 41 매핑표(:451) 산출 뒤 "매핑표 기준 회수 건수(Phase 별 합 = 64)" 로 재부여해야 확인 가능하다. 권고 = 4.x 게이트 열의 고정 수치를 "Step 41 매핑표 기준·현행 분포는 참고" 로 바꾸고, 4.6 게이트에 "Part 0·§3~§9 일반 유도 boxed 는 4.1~4.5 에서 계수" 이관 규칙을 4.3 과 같은 문면으로 추가.

**8.2 D-계열 이름공간(LOW).** CLOSING D1~D6(:126)·v1.0.23 D1~D4(:332)·anodefit D1~D7(:140·:320)·FB 리비전 계획 D1(:320 "계획 D1 in-place")이 한 문서에 공존하나 이름공간 표(:221)는 `D1~D6 = 사용자 결정 이력(R3 A-1)` 만 등재한다. 각 출현이 문맥 접두를 달고 있어 실충돌은 낮다 — 표에 한 줄 보강.

**8.3 중단 조건 균일성(LOW).** 1.5(:348–349)·3.7(:487)에는 "중단 조건" 줄이 없다(다른 17 Phase 는 있음). brief §9 요구 범위는 챕터 2·3 이므로 위반은 아니나, 1.5 는 Step 단위 세부 Phase(1e)라 균일성 권고.

**8.4 반영 확인(누락 아님 — 기록).** brief §4~§8 의 항목은 초안에 전건 있다: §4.1~4.6 수치·구조 맵·미검독 표시(§2.1~§2.9), §5 작업 챕터 1~6·Phase ID·게이트 축, §6 Non-goals 7항(:256–265), §7 운용 7항(:530–542), §8 DR-1~9. P3 #7 3축은 5축 표(:214–221)로 확장됐고, P4 8항은 §2.8·§2.9·Step 1·Step 2·§2.7·각 Phase 중단 조건·Test Plan·Implementation Changes 로 확인된다.

---

## 9. missing 목록(심각도 순)

| # | 심각도 | 항목 | 위치(초안 v3) | 근거 tier |
|---|---|---|---|---|
| 1 | **HIGH** | ID 충돌 잔존: Test Plan `T-1`·`T-2` vs R6 후보 `T-1`·`T-2` — 같은 문서 두 의미. 이름공간 표에 Test Plan ID 미등재. fixer "실제 충돌 0" 주장(`fix_change_log.md:62·:98`) 반증 | Summary :31 · Phase Range :221 · 3.1 :429·:434 · 3.2 Step 39 :449 · 4.1 :498 · Test Plan :552–553 | 확정 |
| 2 | MED | 4.x Phase 별 boxed 회수 수치가 현행 장 소속(27/10/4/3/16/4) 기준 — (b) 구조에서 4.6 "27/27" 성립 불가·4.2/4.5 몫 미계수 · Step 41 매핑표 기준 재부여 규칙 없음(4.3 만 이관 규칙 보유) | 4.x 표 :497–506 · §2.2 :96 · 6.2 :521 | 확정(문면) |
| 3 | MED | Assumptions 19(판독 path:line 정확성)에 GO 전 1g 대조 절차 없음 — 전건을 1.1~2.5 로 이연. §2.2~§2.6 게이트 기준 좌표 전부가 이 전제 위 | Assumptions :598 · §2.9 :206 | 확정(문면) |
| 4 | MED | R3 A-4 F-01(§1.1.4 (a)(b) load-bearing / (c)(d) 배경 분리 재판정)이 어느 Step 에도 없음 — 게이트 1.3 "미검증 0(F-04·F-08·D21/D22)" 이 F-01 을 빠뜨린 채 선언 · R3 A-6 D21-2 연동도 동일 | 1.3 Step 8 :331 · 게이트 1.3 :334 · 2.5 :400–402 | 확정 — `R3…:85·:126` |
| 5 | MED | 유실 자산 원문 4건(Fable v2·Opus v5/v6·v3/v4/v5·Opus v4)의 실물 존재가 Assumptions 에 없음 — Step 11 (i) 는 "경로 1.1 확정·미정독 시 표기" 로 유보. 본 critic Glob: `Claude/old/_archive/graphite_ica_ch1_{Fable_v2,Fable_v3,Opus_v4,Opus_v5,Opus_v6}.tex` 5본 존재 | 1.4 Step 11 (i) :341 · DR-15/16/17 :703·:709·:717 · Assumptions :580–601 | 확정(실측) |
| 6 | LOW | Non-goals S0–S5 bullet 의 "DR-16 인접" 포인터 orphan(DR-16 에 S0–S5 없음) — FABLE §5-8 5건 중 S0–S5 본문 편입만 DR 부재 | :263 · :708–712 · :342 | 확정 |
| 7 | LOW | 1.2 Step 3 "행 1~21"/Step 4 "행 22~31" 분할이 실제 배분(22/9)과 1 어긋남 — 게이트 36/36 무영향 | :319–320 · :315 | 확정 |
| 8 | LOW | Assumptions 11 "측정분 ≈12,400줄" — 열거 합 12,507(PLAN_* 16·ledger 30 미포함) | :590 | 확정(산술) |
| 9 | LOW | Assumptions 1·5·7·15 에 1g 대조 명령 미기재(검증은 가능). SymPy 는 실측 설치 확인(1.14.0) — "미검증" 갱신 가능 | :580·:584·:586·:594 · T-12 :563 | 확정(실측) |
| 10 | LOW | T-20 교재 형식 요소에 "연습문제" 지위(포함/N/A) 미결 — R4a §5.1 연습 0 확정인데 기준 2 조작적 정의에서 빠짐 | T-20 :571 · 2.5 Step 27 :400 | 확정 — `R4a…:239` |
| 11 | LOW | 판독 key finding 개별 Step 미지정 4건: LCO 산문 비율 계측(R3 B-1)·샘플 이미지 QA → 6.1(R2 P-7)·M 통찰 동기 층(R3 A-9)·L-14/L-15/L-18(R1) — 1.4 시드 흡수로만 간접 반영 | 2.2 :371 · 2.5 :400 · 6.1 :520 · 4.0 :497 | 확정 — §2 표 |
| 12 | LOW | Phase 1.5·3.7 에 "중단 조건" 줄 없음(17 Phase 는 있음) | :348–349 · :487 | 확정 |
| 13 | LOW | DR-6 응답 선택지에 "R7 Crossref 결과 승계 vs 재조회" 하위 결정 미노출 | :648–651 | 확정 |
| 14 | LOW | D-계열 이름공간 4종(CLOSING·v1.0.23·anodefit·FB 계획) 공존 — 표에는 CLOSING 만 | :221 · :126 · :140 · :320 · :332 | 확정 |

"없음" 판정의 근거: 사용자 기준 1)~6) 구현 경로 누락 = 없음(§1 표 전건 "있음") · 판독 DQ 97건 처리처 공백 = 없음(§2) · 감사 55건 미반영 = 없음(§3 표본 대조) · step 리셋·중복·건너뜀 = 없음(§4) · 11-section 개명·순서 위반 = 없음(§5) · DR 4요소 결손 = 없음(§6).

---

## 10. Decision Queue (critic — 결정은 master·사용자)

- **DQ-C1 [master 통합 시 수정 권고]** #1 T-1/T-2 충돌 — 두 해법: (a) R6 후보 인용 전건에 `R6:` 접두(Summary·3.1·3.2·4.1·4.4 약 10곳), (b) Test Plan ID 를 `TP-n` 으로 재명명(Summary 행 1~5·Phase Range 4.x·6.x·4.x 표·6.2·Test Plan·부록 다수 — 치환 범위가 큼). 본 critic 제안 = (a) + 이름공간 표에 "Test Plan `T-1~T-21` = 게이트 ID" 행 추가. 근거 = LOGIC-02 원 권고(`audit_logic.md:21` "출처 접두 강제").
- **DQ-C2 [골격 이견 아님·게이트 문면]** #2 4.x boxed 회수 수치를 Step 41 매핑표 기준으로 재부여 — brief §5 4.x 골격("각 Phase = 절 단위 루프 + 빌드 게이트 + 본문 코드 토큰 0 + Result")은 불변이며 게이트 수치의 기준 좌표만 바꾼다.
- **DQ-C3 [1g 절차 후보]** #3 Assumptions 19 에 GO 전 표본 대조(각 R 당 path:line 2건, 합 16건 Read)를 넣을지 — 전건 재대조는 1.1~2.5 소관이라 표본만. master 판단.
- **DQ-C4 [사실 갱신]** #5·#9 본 critic 실측(원문 tex 5본 존재·xelatex True·Python 3.12.10·sympy 1.14.0·패키지 OK·신규 예정 파일 전건 부재·`Step *` 0건)을 master 가 Assumptions 표의 검증 상태 열에 옮길지 — 실측 시점 2026-09-03, 방법 = Glob·PowerShell 읽기 전용.
- **DQ-C5 [DR 신설 여부]** #6 S0–S5 본문 편입을 DR-24 로 독립시킬지, DR-16 부기로 갈지 — FABLE §5-8 5건의 대칭성 관점에서는 DR-24 가 자연스러우나 결정은 3.7 DG-B 에서 닫히므로 어느 쪽이든 blocking 은 아니다.
- **DQ-C6 [기준 2 조작적 정의]** #10 연습문제 지위 — T-20 에 "N/A(제외)" 로 못박을지, DR 로 올릴지. 사용자 verbatim(brief:37)은 "교재 수준의 상세한 설명" 이라 연습문제를 요구하지 않는다는 읽기가 가능하나 이는 본 critic 의 추정이다.

---

## 11. Read Coverage (파일·행 범위 전건 — head→tail)

| # | 파일 | 행 범위 | 방식 |
|---|---|---|---|
| 1 | `Claude/results/handoffs/2026-09-02-v2-master-plan/brief.md` | 1–219(전문) | Read |
| 2 | `…/wf/plan_draft_v3.md`(대상) | 1–108 · 109–216 · 217–324 · 325–432 · 433–540 · 541–648 · 649–756 · 757–860(전문, 8분할 합쳐 전 영역) | Read |
| 3 | `…/wf/fix_change_log.md` | 1–133(전문) | Read |
| 4 | `…/wf/audit_spec.md` | 1–162(전문) | Read |
| 5 | `…/wf/audit_format.md` | 1–84(전문) | Read |
| 6 | `…/wf/audit_logic.md` | 1–90(전문) | Read |
| 7 | `…/audit_checklist.md`(루트) | 1–48(전문) | Read |
| 8 | `…/wf/R1_version_register_v3_to_v1019.md` | 1–91 · 92–206(전문) | Read |
| 9 | `…/wf/R2_version_register_v1020_to_v1026.md` | 1–75 · 76–150 · 151–300(전문) | Read |
| 10 | `…/wf/R3_binding_decisions_and_lost_directions.md` | 1–200 · 201–398(전문) | Read |
| 11 | `…/wf/R4a_diagnosis_scope_ch1_partT.md` | 1–180 · 181–363(전문) | Read |
| 12 | `…/wf/R4b_diagnosis_scope_ch2_ch3_appendix.md` | 1–220 · 221–431(전문) | Read |
| 13 | `…/wf/R5_theory_candidates_thermo_statmech.md` | 1–110 · 111–215 · 216–426(전문) | Read |
| 14 | `…/wf/R6_theory_candidates_kinetics_hys_heat.md` | 1–210 · 211–415(전문) | Read |
| 15 | `…/wf/R7_reference_master_map.md` | 1–180 · 181–360 · 361–534(전문) | Read |
| 16 | `C:\Users\lksz1\.claude\skills\skill_LKS_original_plan-execution\SKILL.md` | 1–239(전문) | Read |
| 17 | handoff 폴더 목록 | 20건 | Glob |
| 18 | `Claude/results/Step *` · `Claude/results/**/*STEP*` | 존재 확인(0건 / process 3건) | Glob |
| 19 | `Claude/old/**/*{Fable_v2,Fable_v3,Opus_v4,Opus_v5,Opus_v6}*.tex` | 존재 확인(5건) | Glob |
| 20 | 신규 예정 파일 5패턴(`plans/2026-09-02-v2-master-plan.md`·`PHASE_1-6_V2_EXECUTION_LEDGER.md`·`V2_*.md`·`PHASE_*_V2_*`·`docs/v2.0.0/**`) | 존재 확인(0건) | Glob |
| 21 | xelatex Test-Path · `python -c "import sympy/numpy/scipy/matplotlib/pandas"` | 실행 1회(읽기 전용) | PowerShell |
| 22 | 세션 시작 git status 스냅샷(시스템 제공) | untracked 21 열거 | 열람 |

안 읽은 것(미검독 — 추정 금지): `wf/plan_draft_v2.md`·`iter_1/plan_draft.md`·`iter_1/work_log.md`(fixer 변경 이력은 `fix_change_log.md` 와 v3 본문으로만 판정) · `wf/R7_reference_master_map.json` · `references/record-formats.md` · 원천 실물 전부(`CLAUDE.md` 는 시스템 주입본으로만 · `_sections/*.tex`·`docs/**`·`plans/**`·PDF·코드 — 존재 확인 Glob 외 내용 미열람) · `Codex/`(금지). 산출 = 본 파일 1건. 기존 파일 생성·수정·삭제 0 · git 명령 미실행 · Codex 무접근 · 팝업 도구 미사용.
