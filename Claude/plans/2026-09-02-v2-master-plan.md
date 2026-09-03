# v1.0.27 Plan — 수식 연구 진보 마스터 플랜 (열역학·동역학 관점의 일반화 재구축) · v5(사용자 결정 DR-1~23 반영 재baseline)

> **v5 · 사용자 결정(2026-09-03, DR-1~23 + 신규 요구) 반영 재baseline · master(Fable 5.1) — 목표 버전 라벨 = v1.0.27(DR-2; 파일명의 "v2" 는 두 번째 마스터 arc 라는 뜻이며 버전 번호가 아니다) · v4 = master 통합(2026-09-03) · 저장 위치 `Claude/plans/2026-09-02-v2-master-plan.md`(11-section 본문). 판독 R1~R7·감사 3본·수정 로그·비평·부록 A~C 는 `Claude/results/handoffs/2026-09-02-v2-master-plan/wf/`. v3 = 워크플로 수정 에이전트 [fixer](Fable 5.1) · 2026-09-03 — v2(통합 저작 에이전트 [integrator], 2026-09-03)에 검수 sub 감사 발견 55건(SPEC-01~13 · FORMAT-01~22 · LOGIC-01~20)을 반영한 판. 반영 내역 = 같은 폴더 `fix_change_log.md`.** v2 는 직전 초안 v1(`iter_1/plan_draft.md`, 작업 sub — 본 문서에서 "v1 초안"·"v1 sub 실측"·"v1 work_log DQ-n" 은 전부 이 파일과 `iter_1/work_log.md` 를 가리킨다)을 시드로 하고, 판독 산출 8본(`wf/R1`~`R7`)을 반영해 보강·정정한 **초안**이다. 최종 통합·저장·commit = master(본 파일 v4). 사용자 GO 전까지 실행은 없다(기획 단계).
> **성격** = 마스터 플랜(top-level). 실행은 사용자 GO 뒤의 일이며 본 문서는 계획만 담는다. 페이즈별 세부 계획서(1e)의 3단 구분 = **작업 챕터 1** 은 본 문서의 Phase 1.1~1.5 절이 곧 세부 계획서(Step 단위까지 세부화 — 진행 예정 Phase) · **작업 챕터 2·3** 은 본 문서에 Phase·Step 범위·게이트·중단·다음 조건을 적고, 각 Phase 착수 시 그 절을 시드로 **별도 세부 계획서** `Claude/plans/2026-MM-DD-v1027-phase-<id>-plan.md` 를 작성한다 · **챕터 4~7** 은 Phase 목록·게이트와 "3.7 Result 후 세부화" 표시까지만 적고 3.7 Result 뒤 별도 세부 계획서를 쓴다(챕터 7 코드 동기는 챕터 6 종료 후). "매 Step 착수 시 세부 계획서 재독" 의 대상은 챕터 1 = 본 문서의 해당 Phase 절, 챕터 2 이후 = 그 별도 세부 계획서다. 매 Phase(1.1~7.3 전건) 종료 시 `PHASE_<id>_V1027_<topic>_RESULT.md`+`.json` 을 남기고(스킬 2b·헌법 §0), 챕터 말 Phase(1.5·2.7·3.7·4.9·5.3·6.3·7.3)는 챕터 통합 Result 를 겸한다.
> **양식** = 11-section(Summary / Current Ground Truth / Phase Range / Non-goals / Implementation Changes / Phase N — \<name\> / Implementation Interfaces / Test Plan / Assumptions / Correction History / Decisions Required) · cumulative step(Phase 를 넘어도 리셋 없음) · 챕터→Phase→step · Phase ID `<작업챕터>.<n>` · 게이트 = 명령/증거/범위 정량 · 비코드 프로파일(Implementation Changes = 산출물 변경 대장 · Implementation Interfaces = 운용 · Test Plan = 실제 게이트).
> **원천** = `brief.md`(master 명세·사용자 verbatim §2) + v1 초안·work_log(DQ 17건) + R1(등록부 v3→v1.0.19)·R2(등록부 v1.0.20→v1.0.26)·R3(구속력 있는 결정·유실 등록부)·R4a(Ch1 진단 스코핑)·R4b(Ch2·Ch3·부록 진단 스코핑)·R5(열역학·통계역학 후보)·R6(동역학·히스·열 후보)·R7(레퍼런스 마스터 맵). 전건 head→tail 정독(말미 부록 C 「Read Coverage」). 요약과 원천이 어긋난 곳은 원천을 따르고 그 사실을 「Correction History」·부록 A 「Decision Queue」에 적었다. v3 반영 근거 = 검수 sub 감사 3본(`wf/audit_spec.md`·`audit_format.md`·`audit_logic.md`) — 본 fixer 는 이 3본을 직접 열지 않고 master 가 전달한 발견 목록(55건 전문)으로 반영했다.
> **attribution 규약** = "사용자 결정·지적·verbatim" 은 brief §2 발화와 원천이 사용자 결정으로 기록한 항목(원천이 큰따옴표 또는 「전문」으로 표시한 것)에만 쓴다. 원천이 "요지" 로 표시한 발화는 "요지" 로 남긴다(R1 DQ-10·R2 DQ-7). 판독 에이전트의 판정은 "R5 판정"·"R4a 판정" 처럼 출처를 붙이고, 본 통합 에이전트의 판단은 "[integrator 판단]" 으로 표시한다.
> **모델 배정** = 전원 **Fable 5.1**(brief:45 사용자 verbatim "이 작업은 모델 배정을 예외적으로 모두 페이블 5.1로 진행한다.") — 헌법 배분표의 사용자 명시 예외. **Codex 측** = 무접근(읽기 포함).

---

## Summary

**과제 한 줄.** Claude 측 전 작업 이력(구트랙 RB → Fable v2/v3 → … → v1.0.26 A/B, 계획서·인계·감사·클로징·ledger)을 파악한 뒤, 현행 v1.0.25 두 버전(`Claude/docs/v1.0.25/` base + `Claude/docs/v1.0.25.1/` 현행 최신)을 검토하고, **물리적·화학적, 특히 열역학적·동역학적 관점에서 이 수식 연구를 진보시키는 새 버전(라벨 v1.0.27 — 사용자 확정 DR-2, 순차 번호 유지)** 을 저작한다. 사용자 지시(brief:33 verbatim)는 "통합하든 수정하든 전혀 다른 새로운 이론을 끌고와서 엮든 뭐가 됐든간에 … 이 수식 연구의 진보를 이뤄야한다" 이며, 그 진보의 품질 기준은 사용자가 지정한 여섯이다.

| # | 사용자 기준(brief:36–41 verbatim — 큰따옴표 안은 발화 그대로) | 본 계획에서의 지위(게이트 ID) | 판독이 드러낸 현행 대비 거리(출처) |
|---|---|---|---|
| 1 | "수식만으로도 80~90% 이상의 내용을 이해할 수 있을정도로 비약, 누락, 생략 없는 거의 유도에 가까운 수식 전개" | 진단 축(2.2) · 저작 게이트(챕터 4 (a)~(d) 사슬 = T-8) · 검수 렌즈(6.1 follow·적대검산 + **산문을 가린 수식·박스·라벨만의 follow 변형**) — **(a)~(d) 사슬 완결은 "80~90% 이해" 의 proxy 이지 직접 측정이 아니다**(실독자 reading-test 미수행 — R1 §2 V5 행) | boxed 64 = 사슬 완결 36·부분 18·없음 1·N/A 2·비유도 7 → 유도 대상 55(R4a §2·R4b §3 판정) + 비박스 결과식 15 라벨(R4a N1~N8 8 + R4b 7 라벨 = 6 항목; 판정 행 단위 = 라벨)이 "풀면·수치 확인" 으로 대체되거나 미박스 |
| 2 | "포맷은 대학원 수준의 열역학, 통계역학, 동역학 교재 수준의 상세한 설명" | 진단 축(2.5 Step 27) · 저작 게이트(교재 형식 요소 = **T-20**, 4.1~4.9 절별) · 마감 게이트(6.2 T-20 전건) | 정의·정리·증명 환경 0 · 예제 2(+부록 1) · 연습 0 · (a)~(d) 표지가 없는 절 7(R4a §5.1·§2.2, R4b §7.5) |
| 3 | "리뷰 논문급의 빈틈 없는 레퍼런스 작업 및 내용" | 진단 축(2.4) · 설계(3.5) · 완결(챕터 5) | bibitem 95(distinct 93)·DOI 84·Crossref 전건 해소, 그러나 무인용 본문 절 4(§3·§6·§8·§9)·이론 원전 층(Marcus·Kramers·Onsager·Kubo·Ising·Redlich–Kister·Safran 등) 본문 출현 0·원장 체인 V1023 = V1022 사본(R7 §1·§3) |
| 4 | "청중은 전공은 다를지언정 석박사급 인력인 상황." | 진단 축(2.5 Step 29 가독성 7항목) · 저작 게이트(**T-21** 절별 7항목 O/X, 4.1~4.9) · 검수 렌즈(6.1 usable 의 입력 표 = T-21) | 두문자어 미전개 11종·기호표 누락 h_η·regular solution 역어 이원화·전방 참조 밀도(R4b §4 G32·G03·G26, R4a §5.1) |
| 5 | "최대한 일반화된 식을 유도하고 거기서 우리가 필요한 방향으로 수식을 간소화할 수 있는 레퍼런스가 확실한 가정" | 진단 축(2.3) · 설계 핵심(3.2 "일반→특수" 사다리) · 구조 결정(3.3) · 저작 게이트(**T-19 사다리 대조표** — 3.4 계획판 · 4.1~4.9 절별 · 6.2 전건; R5 TH-9.1 을 문건 측 실물로 지정) | 간소화 지점 65(Ch1 35 + Ch2·3·부록 30) 중 레퍼런스 부재 17+·일반형이 식으로 제시된 지점 9·일반형이 박스인 지점 1(R4a §3, R4b §5); 사다리 위쪽 절반(일반 격자기체 Hamiltonian·다중 부분격자·Redlich–Kister·일반 DOS·일반 엔트로피 수지·비평형 상태식)이 문건에 없음(R5 §2, R6 §0) |
| 6 | "작업 방식은 나의 계획 스킬, 지침을 따를 것. 마스터플랜 - 세부계획서 - 작업이력서 단계. 무슨일이 있어도 절대 나의 지침을 따를것. 작업 방법론으로는 니가 더 효율적일지 모르나 나는 효율이 아닌 결과물의 완성도 신뢰도를 중요시한다." | 방법론 전체(본 문서·세부 계획서·Step 이력·Result·Ledger·검수 하한) — 효율을 이유로 어떤 하한도 낮추지 않는다 | — |

**왜 새 버전인가.** 현행 v1.0.25.1 은 v1.0.22 가 고정한 활물질별 3챕터 골격(흑연 + Part 0 + Part T / LCO / Si·혼합 + 부록 E 자기일관)의 국소 수정판이다(R2 §2.3 "현행 문건 골격의 출발점"). 사용자 평은 **v1.0.19 = 구문 최고 · v1.0.23 = 논리 최고**(`results/comp_v24/VERSION_COMPARISON_v19_v23_v24.md`:3 verbatim)이고, v24 이후 변경은 사용자 피드백 집행(품질 하락 0, 의도된 voice 평탄화, 같은 문서 §0)이다. 판독 8본은 현행이 **결과식·닫힌형·검산을 거의 전부 자력 보유**하면서도(R6 §0) 세 종류의 구조적 공백을 갖는다고 수렴한다. (i) **배열 공백** — Eyring 근본식 척추(사용자 2026-06-11 지시, Fable v2 유일 구현, v7 절삭 이후 미계승 — `docs/Fable_점검/FABLE_AUDIT_01_history_v3-v1011.md`:47)의 내용은 §5 bgbox·N7 안에 흩어져 있고 조직 원리는 코드 spine N0→N9 다(R6 K-1). (ii) **사다리 상단 공백** — 비평형 열역학 일반 상태식(entropy production·affinity·flux–force)과 일반 격자기체 Hamiltonian·다중 부분격자 staging·Redlich–Kister 비정칙 초과 자유에너지·일반 포논 DOS·일반 엔트로피 수지가 문건에 없거나 언급 수준이다(R5 §2 굵은 단, R6 T-1). (iii) **두-상 생성 사슬 미폐합** — Ω>2RT 평형 dQ/dV 를 만드는 사슬(볼록 포락 → Maxwell 델타 + 단상 꼬리 → 폭 합성)이 본문 어디에도 식으로 닫혀 있지 않고 이론 조각은 Part 0·§4·독립 부록(본문 미연결·기호 배향 반대)에 흩어져 있으며, dQ/dV 커널은 v1.0.25 에서 삭제된 뒤 v1.0.26 A/B 조사가 "흑연 두-상은 참 / regsol 커널의 gallery 대체는 거짓 / skew-logistic-7 이 BIC 최선" 까지 왔으나 평형 데이터 재검과 사용자 결정이 남아 있다(R5 TH-2.1, R2 §2.10). 사용자 기준 5(일반식 → 간소화)와 기준 1(유도에 가까운 전개)은 국소 수정으로는 닿지 않는 요구이므로, 이력 통합 → 진단 → 이론 설계 → (사용자 결정) → 저작의 **새 arc** 를 연다.

**범위(일곱 작업 챕터).** 작업 챕터 1 이력 통합(등록부 3종) → 2 현행본 진단(GAP REGISTER — 대상 = v1.0.25·v1.0.25.1·v1.0.26A/B, DR-1) → 3 이론 진보 설계(THEORY BLUEPRINT — 3.7 은 비차단 보고점) → 4 저작 v1.0.27 → 5 서지 완결 → 6 검수·수렴·마감 → **7 코드 동기(doc-leads; 문건 확정 후, DR-4·DR-9)**. 구조(DG-A)와 라벨(DG-C)은 사용자가 확정했고(DR-3·DR-2·DR-12), 채택 이론(DG-B)은 사용자 위임(DR-11·15·16·17·18·23)에 따라 master 가 3.7 에서 확정·보고한다 — 사용자만 결정 가능한 항목이 **새로** 생길 때만 정지한다(DR-9 "챕터 전체를 쭉 이어진행"). 챕터 4~7 세부 계획서는 3.7 Result 뒤에 쓴다. 마스터 플랜은 헌법이며 Phase·Step 은 추가만 가능하고 삭제하지 않는다(DR-9). 판독 산출 R1~R7 은 챕터 1~3 각 Phase 의 **시드**다 — 시드가 있다고 해서 검수 하한을 낮추지 않는다(기준 6). 정독 범위는 사용자 확정 DR-7(핵심 문건 전문 + 세부 계획서·ledger·result 는 토픽 한정)을 따르고, 등록부·레지스터의 Read Coverage 는 본 arc 의 Read 만 계수한다(판독 커버리지는 참조 열). 시드는 작업 sub 판정이므로 각 Phase 에서 검수 sub 의 refute 와 master 삼각검증을 거쳐야 등록부·레지스터로 확정된다.

**핵심 정직 프레임.** (1) 코드와 이론은 별개다(DR-10) — 본문·부록 어디에도 코드·스크립트·파일명 언급 0(DR-14: 코드맵·코드 절·대응 지도는 문건 밖 코드 문건 OUT-CODEDOC 으로), 코드 동기는 문건 확정 후 작업 챕터 7(DR-4·DR-9). 이전 코드·산출물이 드러낸 문제(regsol 역전·near-delta 천장·α 축퇴·G-금지 등)는 유도의 **동기**로만 반영하고 언급하지 않는다. (2) 새 이론을 접목할 때는 선행 서베이가 확정한 **기각군**(Wiener–Hopf·WKB·다중척도·중심다양체·Langevin·Preisach 연산자 채택·Kubo 동적 χ 승격·Tikhonov/MaxEnt 역산·Bazant/Dreyer PDE 생성기·전이 6+ 증설·DFT 결합E→Ω 대입 등 — R5 §1.2 12건·R6 §6 20항)을 승계해 재조사하지 않는다. (3) 기존 자산(`\label` 429·`\boxed` 64·식 번호 체계·절 말미 `% 자산` 태그 체계)은 **무유실**로 승계한다 — v1.0.22 계보 감사 "미로그 축소·생략·왜곡 0" 기준(`docs/v1.0.22/results/HANDOVER_v1.0.22.md`:29). (4) regsol 미결(v1.0.26)은 결정이 아니라 **설계 입력**으로 흡수한다(2.6·3.1) — 단 사용자가 "이미지로 확인하고 나서 정할려니까"(`results/comp_v26_data/HANDOVER_regsol_investigation.md`:13 verbatim)로 열어 둔 결정은 DG-B 에서 명시적으로 닫는다(DR-10). (5) 근거 없는 수치·서지·결정은 만들지 않는다 — 추정은 "추정" 으로 표기한다.

**후보 이론의 골격(판독 등급, 결정 아님).** 열역학·통계역학 축 A 필수 6건 = TH-1.1 일반 격자기체 Hamiltonian 정점 · TH-2.1 정칙용액+Maxwell 두-상 dQ/dV 사슬 폐합 · TH-3.1 Redlich–Kister → α_j 승격 · TH-5.1 상분리 부록 본문 승격 · TH-9.1 일반→특수 대조표 · TH-9.2 기호 통합표(R5 §4 등급). 동역학·히스·열 축 A 7건 = K-1 Eyring/TST 척추 재배열 · R6:T-1 entropy production 일반 상태식 · S-1 부록 E 3층 승계 · S-2 refs 6/7 5항 완결 · S-5 순환 의존 dependency graph·4분류 표 · H-2 정칙용액→로지스틱 rung(커널 채택은 2.6 조건부) · Q-1 비가역 발열 분해(R6 §7 등급). B 강권 20건(R5 10 + R6 10)은 3.7 DG-B 결정 대상이다. 이 등급은 R5·R6 의 판정이며 본 계획은 그것을 **카탈로그 시드**로 승계할 뿐 채택을 확정하지 않는다.

---

## Current Ground Truth

> brief §4 의 master 실측 수치를 그대로 옮기고, v1 초안의 작업 sub 실측(`[sub 실측 ✓]`)과 판독 8본의 확정 사실(`[R# 확정]` + path:line)을 병기한다. brief·v1 과 판독이 어긋난 곳은 판독 원천을 따르고 정정 사실을 적었다. 안 읽은 것은 **미검독**으로 표시한다. 4-tier: 확정 / 근거 미발견 / 추정 / 미검증.

### 2.0 brief §3 원천 코드표와 약호 정의(본 문서가 A#·B#·note_A#·[C-92]·GS-n 으로 인용하는 것)

| 코드 | 파일(`D:\Projects\Project_Anode_Fit\` 기준) | 줄(brief 기재) |
|---|---|---|
| A1 | `CLAUDE.md` | 90(R3 실측 89) |
| A2 | `Claude/docs/INDEX.md` | 197 |
| A3 | `Claude/plans/INDEX.md` | 65 |
| A4 | `Claude/docs/v1.0.25.1/results/V1025_1_TOUCHUP_NOTE.md` | 62 |
| A5 | `Claude/docs/v1.0.25.1/results/HANDOVER_v25.md` | 171 |
| A6 | `Claude/docs/v1.0.25.1/results/HANDOVER_v24.md` | 89 |
| A7 | `Claude/results/comp_v26_data/HANDOVER_regsol_investigation.md` | 56 |
| A8 | `Claude/plans/2026-07-26-v1025-surgical-skew-consistency-plan.md` | 241 |
| A9 | `Claude/docs/Fable_점검/FABLE_AUDIT_01_history_v3-v1011.md` | 73 |
| A10 | `Claude/docs/v1.0.15/CLOSING_v1.0.15.md` | 106 |
| A11 | `Claude/results/comp_v24/USER_FEEDBACK_v1024_READING.md` | 207 |
| A12 | `Claude/results/comp_v24/VERSION_COMPARISON_v19_v23_v24.md` | 80 |
| A13 | `Claude/docs/v1.0.25.1/_sections/ch1_sec00_intro.tex` | 95 |
| A14 | `Claude/docs/v1.0.25.1/_sections/ch1_appE_selfconsistent.tex` | 218 |
| B1 | `Claude/docs/v1.0.18.2/ROADMAP_future_physics.md` | 50 |
| B2 | `Claude/results/comp_v24/IMPROVEMENT_DIRECTIONS.md` | 87 |
| B3 | `Claude/results/comp_v24/LIT_ADVANCE_SYNTHESIS.md` | 130 |
| B4 | `Claude/docs/v1.0.22/results/comp_v23/SURV_SYNTHESIS.md` | 45 |
| B5 | `Claude/docs/v1.0.22/results/comp_SM2/SM2_SURVEY.md` | 136 |
| B6 | `Claude/plans/2026-07-18-v1023-ratio-and-advanced-methods-plan.md` | 226 |
| B7 | `Claude/plans/2026-07-18-anodefit-MASTER-plan.md` | 129 |

- `note_A1`~`note_A5` = `Claude/docs/Fable_점검/FABLE_AUDIT_note_A1_v3-v5.md` · `…A2_v5-v7.md` · `…A3_v7-v9.md` · `…A4_v9-v1011.md` · `…A5_ch2-code.md`(R1 Read Coverage #4~#8).
- `[C-92]` = Part T §2.5 mixing 절 말미 자산 태그 번호가 붙은 warnbox(`_sections/ch2_sec05_mixing.tex`:230–238) — 히스 gap 소산·경로의존 정량을 "본 장 범위 밖" 으로 선언한 서브 저작 문구(R6 §3·DR-18).
- `GS-1`·`GS-2` = Ch3 의 정직 공백 라벨 — GS-1 소성 히스테리시스(`ch3v22_sec04_mech.tex`:89–99 "물리 가정 충돌 + 유도 미완결"), GS-2 유한율속 비가산(`ch3v22_sec03_blend.tex`:251–266 "물리 가정 충돌")(R4b G22·A25·A27).
- 판독 문건 내부 ID 의 출처 접두 규약은 Phase Range 이름공간 표 마지막 행.

### 2.1 git·환경

| 항목 | 값 | 근거·검증 상태 |
|---|---|---|
| 브랜치 `main` HEAD | `4069cb3`(2026-07-27, "feat(v1.0.26 A/B): regsol 재검증 — 물리 4전이 vs gallery 7전이 두 버전 산출") | 확정 — 세션 시작 git status 스냅샷·brief §4.1. 본 통합 에이전트는 git 명령을 실행하지 않았다(경계) |
| origin/main | main 과 동일(`4069cb3`) | **master 실측 ✓ 2026-09-02**(`git branch -vv`) — 이후 master 커밋 2건(`79b4c34`·`82b5b38`, handoff 산출 추가)은 push 전 |
| tracked 변경 / untracked | 0 / 21 = **Claude 측 8**(`Claude/docs/v1.0.17/figs/graph_suite_v1017.png`·`v1.0.17/sample_test_v1017.png`·`v1.0.18.1/figs/graph_suite_v1018_1.png`·`v1.0.18.1/sample_test_v1018_1.png`·`v1.0.18.2/figs/graph_suite_v1018_2.png`·`Claude/results/process/C3_graph_check/`·`C3_pdf_render/`·`Claude/results/regsol_test/`) + **Codex 측 13**(`Codex/work/*` 13 폴더 — 무접근·지위 판정 안 함) | 확정 — 세션 시작 git status 스냅샷(감사 SPEC-04 의 "Claude 10·Codex 11" 은 스냅샷 재계수로 8·13 정정 — [fixer 실측]). `regsol_test/` 는 v1.0.26 README 가 폐기 판정(`results/comp_v26_data/README.md`:28–31, R2 §2.10) · `C3_*`·`sample_test_*` 는 v1.0.23 R2:P-7 샘플 이미지 QA 관련 가능성(R2 DQ-11 추정) → 1.1 에서 Claude 측 8건 지위 확정 |
| 버전 브랜치 | `v1.0.25.1`·`v1.0.25-surgical`·`v1.0.24.1` 전부 main 의 조상 | **master 실측 ✓ 2026-09-02**(`git merge-base --is-ancestor` 전건 YES; 배경 = `V1025_1_TOUCHUP_NOTE.md`:10–12, R2 §2.9) |
| XeLaTeX | MiKTeX 25.12 `C:\Users\lksz1\AppData\Local\Programs\MiKTeX\miktex\bin\x64\xelatex.exe` | **[sub 실측 ✓ 존재]**. 2026-07-26 빌드 102/30/22p 실증 = `docs/v1.0.25.1/results/V1025_1_TOUCHUP_NOTE.md`:55. PATH·실행 가능 미검증 |
| Python | 3.12.10 + numpy/scipy/matplotlib/pandas + **SymPy 1.14.0** | **master 실측 ✓ 2026-09-03**(import 전건 OK) — T-12 새 의존성 정지 조건 해소 |
| 외부 접근(Crossref) | `api.crossref.org/works/{DOI}` 조회가 **2026-09-03 판독 단계에서 실제 수행됨**(현행 DOI 84건 + 후보 74건, 응답 JSON 은 세션 스크래치·R7 json 부본) | **[R7 확정]** R7:7 — 이 사실은 DR-6 의 "허용 여부" 결정 이전에 판독 에이전트가 읽기 전용 조회를 실행했다는 뜻이며, 본 계획의 2.4·3.5·5.1 은 그 결과를 승계 가능(재조회 필요 여부는 DR-6) |
| 구조 검사 도구 | `docs/v1.0.25.1/results/tools_check_structure.py`(`check` 만 — JSON 모드는 v1.0.24 R0 마스터 tex 덮어쓰기 사고, `HANDOVER_v24.md`:50) · `tools_tex_strict_check.py` · `tools_doc_code_audit.py` | **[sub 실측 ✓ 3본 존재]** · v1.0.27 새 파일명 동작 여부 미검증 |
| 사용자 논문 | `Claude/JCP_147(14)_144111_(2017) - Effects of external electric field.pdf` + `Claude/jcp_extract.txt` | **[sub 실측 ✓ 존재]**(내용 미검독) |
| refs 6·7 원문 | `lee2011jcp` S. Lee·C. Y. Son·J. Sung·S. Chong, JCP 134, 121102 (2011), DOI 10.1063/1.3565476 · `son2013jcp` C. Y. Son 외, JCP 138, 164123 (2013), DOI 10.1063/1.4802584 — 서지 Crossref 확정, **원문 미소장** | 확정 — `_sections/ch1v22_bib.tex`:46–47(R3 B-9·R7 §2.1 #41–42). 방법론 추출본 = `Claude/old/Archive_oldtrack/PHASE_DIAG_REFS67_DOSSIER.md`(50줄, R6·R7 전문 정독) — ★dossier 는 "임시 열람 후 삭제(2026-05-29)" 표기(:3)이나 brief §4.1 은 JCP147 PDF 현 소장을 실측 → 불일치 표면화(R6 DQ-6) |
| `Claude/docs/v1.0.27/` | 부재 | **[sub 실측 ✓ 부재]** — 저작 시 생성(DR-2) |
| v1.0.26 A/B 실물 | `docs/v1.0.26A-regsol/README.md`(199줄)·`docs/v1.0.26B-gallery/README.md`(193줄)·`results/comp_v26_data/README.md`(50줄)·`out_versions/build.log`(36줄)·조사 스크립트 6본 존재 | **[R2 확정 · master 실측 ✓ 2026-09-03: `docs/v1.0.26A-regsol/`·`docs/v1.0.26B-gallery/` 각 README.md·figures/·params/ 존재]** — brief §4.3 "실행 차단·미완" 은 **착수 시점 인계문서 기준의 stale 표현**(§2.3 정정) |

### 2.2 현행 문건 v1.0.25.1 (동결 base — 무수정)

- **구조**: 3 마스터 tex(`ch1_graphite_v1.0.24.tex`·`ch2_lco_v1.0.24.tex`·`ch3_si_v1.0.24.tex`, 파일명 유지 = DG-2 v1.0.25 한정 규약) + `_sections/` 56(`common_preamble_v1024.tex` 포함) + `appendix_phase_separation.tex`(독립 부록·자체 `\documentclass`·마스터 미편입, `results/INDEX_v25.md`:35) = **60 tex · 9214줄** **[sub 실측 ✓]**. PDF **102/30/22p**(파일 존재 ✓, 페이지 수는 A4:55 인용).
- **빌드 미포함 잔존 파일** **[R3·R4b 확정]**: `_sections/ch1_appD_si.tex`(91줄)는 세 마스터 어느 `\input` 목록에도 없는 orphan(`ch1_graphite_v1.0.24.tex`:25–60·`ch2_lco_v1.0.24.tex`:22–32·`ch3_si_v1.0.24.tex`:23–32; 내용은 v1.0.21 부록 D → Ch3 §3.1 승격 `ch3_si_v1.0.24.tex`:3). 자산 태그 [V21-Q7-01~05] 가 이 파일에만 남아 있다(R4b G27). brief §4.2 "_sections 56" 카운트에는 포함돼 있다.
- **자산 카운트**(brief §4.2 = master 실측 · **[sub 재계수 ✓ 전건 일치]** · 모집단 = **파일 집합 60 tex = 빌드 포함 58 + 빌드 미포함 2(orphan `ch1_appD_si.tex`·독립 `appendix_phase_separation.tex`)** — "빌드 세트" 가 아니다: 빌드 포함 58 만 세면 boxed 61(독립 부록 3 제외)·label 392(부록 30 + orphan 7 제외)가 되어 brief 수치와 정의상 어긋난다(R4b §1.3·§1.4; T-4 정의 문서)):

| 자산 | 값 | 정의·비고(카운트 게이트 정의 확정 필요 — R7 DQ-15) |
|---|---|---|
| display 수식 환경 | **230** | = `equation(*)` 228 + `align(*)` 1 + `gather/multline` 1(sub 실측). `\[ … \]` 38개는 별도. R4a(범위 29파일 disp 169, `\[` 포함)·R4b(84 + `\[` 7)의 절별 카운트는 **집계 기준이 달라** 합이 230/268 과 일치하지 않는다 → 2.1 에서 정의 하나로 재계수 |
| `\boxed` | **64** | 전 문건. 분포 = Ch1 곡선 사슬(sec01~10) 27 · Part T(ch2_sec00~08) 10 · 부록 E 4 · 독립 부록 3 · Ch2 LCO(sec11~17) 16 · Ch3 Si 4 → 27+10+4+3+16+4 = 64(v1 초안 §2.2 보충 표 = R4a §1 = R4b §1.4 정합). brief "본문 39" 는 v1.0.25 note 의 집계(범위 정의 상이, R4a DQ-7·R2 DQ-12) → 게이트 문구는 "64/64(전 문건)" 로 통일 |
| `\label` | **429** | boxed 인데 `\label` 부재 1건: `ch1_sec06_eqpeak.tex`:91 감수율 항등 bgbox(R4a #19) |
| `\bibitem` / distinct 키 | **95 / 93** | Ch1 44 + Ch2 15 + Ch3 36; 중복 키 = `swiderska2019`(Ch1+Ch2, 의도된 중복 D22)·`verbrugge2017`(Ch1+Ch3, 제목 오류 공유) **[R7 확정]** |
| `\cite` 호출 / distinct 키 | **265 / 93** | = 본문 `_sections` 53본 명령 262 + `ch1v22_bib.tex`:46–47 내부 상호참조 3; 키 단위로 펼치면 315; 93 키 전부 ≥1회 인용·미정의 키 0·미인용 bib 0 **[R7 확정]** |
| DOI | **84 / 95** | 없는 9 = 서적·장 8 + 내부 자료 1(`numverif2026`) — Crossref 84건 전건 해소, 실질 결함 6건 R-01~R-06(§2.6) **[R7 확정]** |
| section / subsection | **49 / 115** | |
| figure / table+longtable | **28 / 20** | |
| 박스 환경 | warnbox 14 · keybox 18 · bgbox 10 · verifybox 15 · srcbox 16 · derivbox 1 (+ signbox·codebox·procedurebox — R4a §1 합계 9종) | `ch1_preamble.tex`:31–36·`ch2_preamble.tex`:31–35 의 `\newtheorem*` 은 박스 이름용 — **정의·정리·보조정리·증명 환경은 정의돼 있지 않다**(R4a §1) |
| 자산 태그(`% 자산` 주석) | v1 sub 실측 `[A-xxx]` 159 · `[E-xxx]` 8 **vs** R3 grep 계열 `[C-nn]`·`[V21-Qn-nn]`·`[V22-SM2-X]`·`[V22-R5-nn]`·`[LCOΩ-n]`·`A-0nn` 138건·34파일(`% 자산` 주석 46건·31파일) | **원천 간 상충(미해소)** — 두 실측이 다른 패턴을 센 것으로 추정. 2.1 Step 14 에서 기계 추출로 계열 목록·건수를 확정(DQ-I3) |

- **조립**(마스터 tex 3본 `\input` 순서 — **[sub 실측 ✓]**): **Ch1 흑연** = §0 서론 · §1 N0N1 · §2a/§2b Part 0 · §3 중심 · §4 히스 · §5 폭 · §5b gr2L · §6 평형 peak · §7 broadening · §8 lag · §9 tail · §10 합산 → Part T(`ch1v22_partT_divider` + `ch2_sec00~10`) → §18 입력 → 부록 A 부호검산·B 코드맵·C/D(`ch2_appA_traps`·`ch2_appB_codemap`)·E 자기일관 → `ch1v22_bib`. **Ch2 LCO** = `ch2v22_sec00_intro`·`ch2v22_notation`·`ch1_sec11~17`(intro·center·hys·decomp·elec·peak·16b omega·MSMR)·`ch2v22_bib`. **Ch3 Si·혼합** = `ch3v22_sec00_intro`·`notation`·sec01 map·sec02 cases·sec02b sifr·sec03 blend·sec04 mech·`\appendix`·sec05 code·`ch3v22_bib`. 장간 `\externaldocument` xr(빌드 순서 ch1→ch2→ch3→ch1 재패스). **파일 접두 ↔ 소속 반전** = `ch2_sec*` 는 Ch1 Part T, `ch1_sec11~17` 은 Ch2, `ch2_app*` 는 Ch1 부록 C/D(`HANDOVER_v1.0.22.md`:45 경고, R2 §0·R4b §8.3).
- **§3.5 코드 명세절의 3중 불일치** **[R4b 확정]**: `ch3_si_v1.0.24.tex`:30–31 이 `\appendix` 를 `ch3v22_sec05_code` 앞에 두어 조립상 부록이나, 파일명 `sec05`·라벨 `sec:si-code`·본문 참조 "§3.5 코드" 6곳(`ch3v22_sec03_blend.tex`:88,109,132,260,272·`ch3v22_sec01_map.tex`:123)이 본문 절 표기 → P3 #8 게이트 문면(파일 단위 vs 조립 단위)이 모호(DR-14).
- **문건의 자기 규정**(`_sections/ch1_sec00_intro.tex`): spine N0~N9, 세 층 Part 0 → Part I → Part T, "세 인자(T·전위·C-rate)는 모두 하나의 속도식 k≃k₀exp[−ΔG_a/RT] 의 서로 다른 자리로 들어온다"(:37–40) 선언 — 그러나 조직 원리는 코드 spine(:42–88)(R6 §3).
- **부록 E**(`ch1_appE_selfconsistent.tex`, 218줄): 동결 0차(eq:sc-frozen :32–42) ← 1차 ratio(eq:sc-ratio :86–90) ← 참 비선형 Volterra(eq:sc-true :51–55·eq:sc-volterra-eq :62–65) 3층 · 타당성 ε=2χ_d(Ω/RT)Δξ_supp(eq:sc-valid :149–153) · 전달함수 H(ω)=1/(1+iωL_V)(:183–188) · refs 6/7 5항 sub-section `sec:sc-p35`(:113–135) — ② 위치 항 "페이지·문단 세부는 원문 대조로 확정" **미완**(:120–121) · 서두 warnbox 가 전하 보존 반전·배경 자기일관을 "적분핵 없는 대수 근" 으로 명시 배제(:19–27)(R6 §3·S-1·S-2).
- **코드** `Anode_Fit_v1.0.24.py` = **1917줄** **[sub 실측 ✓]**(release 1.0.25). doc-leads 정합·게이트 GREEN·골든 bit-exact = A4 인용(미재실행). **본 계획에서 코드는 Non-goal.** G-금지 게이트 수 = `INDEX_v25.md`:23 "8/8·G-금지 미구현" vs `V1025_1_TOUCHUP_NOTE.md`:19 "9/9(G-금지 포함)" **원천 간 모순**(R2 N11) → 2.1 실물 확인.
- **v1.0.25 vs v1.0.25.1 차이** **[sub 실측 ✓ hash · R4a §2.3 · R4b §2 diff 확정]**: `_sections` 3파일 DIFF — `ch3v22_sec02b_sifr.tex`(F1 :40–44 정직화 문장, F3 :144–145 inline 표식 — 2 hunk)·`ch1_sec05_width.tex`(M-w :303–304)·`ch1_sec06_eqpeak.tex`(L-bg :107–108) + 마스터 3본 표시 버전 · 독립 부록 SAME · 코드 SAME. 식·라벨·boxed 불변. ★F1 이 본문에 `\texttt{V1025\_DATA\_ADDENDUM.md}` 토큰을 새로 들여왔다(`ch3v22_sec02b_sifr.tex`:43, R4b G35).

### 2.3 계보 (확정 — A2·A9·A12 + R1·R2 정정)

5-28 구트랙 RB(전하보존 6장 → Ch1~5 통합 107p, `Claude/old/Archive_oldtrack` — ★동명이물 주의: `COMPARISON_CLAUDE_v4/v5/v5.2_*`·`REVIEW_LEDGER_v3/v4_*` 는 구트랙 기록이며 본 계보의 v3/v4/v5 와 번호만 같다, `note_A1`:36–39 — note_A# 의 실경로는 §2.0) → 6-07 Ch2~5 야간 초안(원구상 발열·반응속도론·통합 상태방정식·히스테리시스 4장, 사용자 verbatim `results/process/HANDOVER_2026-06-07_ch2-5-overnight.md`:8) → 6-10 TBR 50p → 6-11 Fable v2(★Eyring 근본식 척추 유일 완전 구현, `HANDOVER_2026-06-11_ch1-v2-blank-rewrite.md`:7,11) → 6-12 v3(수식 자기완결·97식) → Opus v4(§1.18 적층 준안정·athermal 훅 +158줄) / v5(수식-구동 장르 전환·§1.18 배제 → park) / v6(흐름도 재조립, 손실 0) → 6-29 v7(코드 플로우차트 N0→N9 척추로 **의도 절삭** 894줄·17p — 사용자 당대 「실제 표현에 필요한 수식만」 → 사후 「중간 도출을 완전히 날렸다」, `note_A2`:90–96,113) · v8(유도 4단 복원·G-derive) · v9(LCO 전자 엔트로피·산문 회귀 기원) · v10(broadening 복원·w 이중지위·w_eff 제거) → 7-01 v1.0.10(코드-문건 동기) → **v1.0.11(byte-identical 중단판 — brief 계보 누락, `note_A4`:11–16, R1 DQ-3)** → 7-02 Fable 이력 감사(`docs/Fable_점검/` 8본·885줄) → v1.0.12(N=10 경쟁·체리픽·LCO 수식화·S0–S5 는 FITTING_GUIDE 에만 복원) · v1.0.13(Part 0 신설·LCO Part II) · v1.0.14(Hill 유도·부록 A/B·spinodal 독립 부록 신설 "별도 문건" 결정·그림 경연) · v1.0.15(격자 퇴출 사용자 verbatim·점별 인과 기억 적분·★CLOSING 헌법 3종) · v1.0.16(n(T)) · v1.0.17(register·서지) · v1.0.18.1/.2(vib Einstein·로드맵 제안 2~5, 2-버전 관례 원형) → 7-08~13 v1.0.19(Fable 전면 재작성 Ch1 61p+Ch2 24p·Part II 7분할·doc-leads·자산 336/133 보존[자기 서술·실물 미검증]) → v1.0.20(서지 원장 V1 규칙·품질 정정·동결) · v1.0.21(대정준 전하보존 `eq:implicit`·TST bgbox·항법판[→폐기]·Si 부록) · v1.0.22(★활물질별 3챕터 재편 D22·계보 감사 ③=0건·CLT/CNT·SM2-A/B/C 집행) → 7-18 v1.0.23(★JCP147 Fredholm ratio 부록 E·전달함수·고등수학 서베이 — 사용자 평 "논리 최고") → 7-18 두 계획서(anodefit MASTER·완성도 검증 V0~V6 — 그 형태로 집행된 Result **근거 미발견**, R2 §2.5) → 7-19~22 v1.0.24(reflect @3/@5/LCO 토글 + 사후 SINTEF 단일 프로토콜 피팅·doc↔code 감사 — 회사 조건 매트릭스 검증은 없음, R2 DQ-4) · v1.0.24.1(피드백 리비전 FB0~FB7·F-01~F-11·`docs/v1.0.24.1/` 폴더 실체화·코드 sha256 f230f59b 불변) → 7-26 v1.0.25(국소 수정: @2 skew opt-in·인과 pad·SI opt-in·**regsol 커널 삭제 DG-1**·FWHM λ^{3/2}·데이터 정직화 — 빌드 미수행) · v1.0.25.1(독립 검증+touch-up 4건·XeLaTeX 102/30/22p·push — 현행 최신) → 7-27 **v1.0.26 A/B(regsol 재검증 — A regsol-4 vs B logistic-7 두 판 산출 완료 · 평형 데이터(GITT/p-OCV+hold) 재검 미실행 · regsol 되살리기 사용자 결정 미기록)**.

- **정정 1(brief §4.3)**: "v1.0.26 A/B(실행 차단·미완)" → 착수 인계문서 `HANDOVER_regsol_investigation.md` 는 `results/comp_v26_data/README.md`:23 이 "착수 시점 인계문서(실행 차단됐던 기록)" 로 규정한 stale 문서이며, 실물은 `out_versions/A_regsol/`·`B_gallery/`·`docs/v1.0.26A-regsol/`·`docs/v1.0.26B-gallery/` 산출 완료. 판정(A README:19) = "흑연이 두-상이다 = 참(Ω/RT 2.54/2.03/1.88/2.30 ≈ 2RT, Cordoba 2024 앵커 정합) / regsol 커널이 gallery 를 대체한다 = 거짓(ΔBIC +844.5·면적 결손 +12.05%)"; 전이 수 스윕에서 skew-logistic-7(BIC 991.5)이 최선(B README:18). 미완의 실질 = 평형 데이터 재검 미실행(README:24,46–48) + 사용자 결정 미기록(HANDOVER:13,54) **[R2 확정]**.
- **정정 2(brief §4.3)**: v1.0.11 삽입(위 굵은 글씨).
- **정정 3(brief §4.3 표현)**: v1.0.24 "공개데이터 검증 캠페인" 은 V-계획(회사 조건 매트릭스)이 집행된 것처럼 읽히나 실물은 reflect 캠페인 + 사후 SINTEF 피팅(R2 DQ-4).
- **Ch2 트랙**(R1 §3.1): Ch2 v3(5p) → v4(13p·w_eff narrowing 오류가 적대 2R 통과 — 설계 doc 순응 검수의 한계) → v5(파생 C 제거) → v1.0.10 동결 편입 → v1.0.19 재작성 → v1.0.22 Ch1 Part T 로 병합. **코드 트랙**(R1 §3.2): v11_final(617행 또는 706줄 — 원천 불일치, R1 DQ-2) → v1.0.10(742줄) → … → v1.0.25(1917줄). **부록(spinodal) 트랙**(R1 §3.3): v1.0.14 신설 → v1.0.17 단위 정정 → v1.0.18.1 → v1.0.19 승계·편입은 사용자 결정 대기 → v1.0.25.1 "독립 부록·무변경".
- **수치 불일치(1.2 에서 실물 확정, R1 DQ-2)**: v1.0.10 Ch1 34p(`docs/INDEX.md`:172) vs 35p(`FABLE_AUDIT_01`:13·`note_A4`:61) · v11_final 617행(`note_A5`:9) vs 706줄(`FABLE_AUDIT_01`:16·`note_A2`:76) · v3 2758 vs 2759 · v4 2912/2735/~2771.
- 사용자 평(A12:3 verbatim): "v19=구문 최고·v23=논리 최고". v24 이후 = 사용자 피드백 집행, 품질 하락 0, 의도된 voice 평탄화(A12 §0·§3).

### 2.4 현재 구속력 있는 결정·제약 (Non-goals·Assumptions·게이트로 승계 — R3 등록부 A 반영)

- **헌법 3종**(`docs/v1.0.15/CLOSING_v1.0.15.md`:9 사용자 verbatim "이 문건의 제일 중요한 두가지는 교과서 수준의 문건, 논문의 깊이의 전문성이고, 세번째가 수식 주도의 문건이다. 수식만 쭉 따라가도 제대로 된 물리, 화학적 논리를 대부분 이해할 수 있는 수준의 문건."): ① 교과서 register(:11–16; [D1] 자기 diff·버전 이력 서술 금지 · [D2] 방어 어투 금지 · 내부 라벨·고백조 누출 금지 · 연속성 — 단 2026-09-02 지시 "전혀 다른 새로운 이론을 끌고와서 엮든" 이 백지 재작성을 배제하지 않으므로 연속성 조항은 **조건부 승계**[R3 A-1 판단]) ② 논문 깊이(:18–21) ③ 수식-주도(:23–26; [D3] "대입하면 [박스]" 점프 0) + 완결 문장·orphan 0·한글 prose + 영어 원어(:29–30)·[D4~D6] 격자 잔재/대조 수식어/스위치 잔재 0(:31)·분량은 콘텐츠의 자연 결과(:32). 2026-09-02 기준 1~4 와 내용 일치 → v1.0.27 게이트 축으로 그대로 승계(R3 A-1).
- **CLOSING Part 2 프로세스 규율 2-1~2-6**(:38–60; 사용자 verbatim "내 지침이랑 과거 이력좀 제대로 확인좀해라"·"하다못해 1.0.14 본 문건을 제대로 파악했으면 이런짓을 했을까?"·"죽는 부분은 지워야지"·"그런식으로 땜질하지마 문건이 누더기가 되잖아"·"무슨 검사를 안하고 그대로 가져가려고 골든이라고 처리하려고하냐") — 존속·승계. **Part 4 w/T 사용자 결정**(:86–93): (1) 폭은 n 으로 fit · (2) 실측 T 투입 · (3) 4단 사다리 (i) 상수 n 집행/(ii)~(iv) 다온도 데이터 의존 park · (4) **n(T) 채택 시 가역열 config 항 동반 변경 ∂w/∂T=(R/F)(n+T·n′) — 이론 규칙으로 승계 필요**(R3 DQ-12) · (5) w 이중지위·use_w_eff 제거.
- **CLAUDE.md P1~P5**(`CLAUDE.md`:11–67) — 존속. 단 **스테일 조항 [R3 확정]**: P1 원구상 "Chapter 1~5"·P3 #6·P5 둘째·셋째 조항의 `ver.N` 은 현행 문건에 0건(grep); P3 #1 의 네 기호 `V_{n,app}`·`V_{n,drive}`·`V_{n,OCV}` 는 현행 0건이고 현행 체계는 두 전위 `V_app`·`V_n`(F-01 keybox, `USER_FEEDBACK_v1024_READING.md`:17). P3 #8 코드=부록 게이트(grep=0)는 **동결 base 에서 이미 위반**(토큰 정의에 따라 3~7건: `ch1_sec10_sum.tex`:145·`ch2_sec08_synthesis.tex`:56 `\code{use\_si\_constants()}` · `ch3v22_sec02b_sifr.tex`:43 `\texttt{V1025\_DATA\_ADDENDUM.md}` · `ch1_sec05b_gr2L.tex`:85,212 `regsol2` · `ch3v22_sec02b_sifr.tex`:53,175 `regsol_si` — R3 B-12·R4a §5.2·R4b §7.2). P3 #3 dependency graph/표는 부재(서술만 — `ch1_sec02b_part0.tex`:353–357·appE:19–27·`ch1_sec17_msmr.tex`:154–159), P3 #4 4분류는 Ch3 만 준수(GS-1 소성 히스·GS-2 유한율속 비가산 — 정의 §2.0). CLAUDE.md 자체 개정은 사용자 소관(DR-13).
- **사용자 피드백 F-01~F-11**(`results/comp_v24/USER_FEEDBACK_v1024_READING.md`; 집행 FB0~FB7 = `HANDOVER_v24.md`:77–89) — 규범 존속. 현행 집행 확인(R3 A-4 grep): F-02 `p_i`(`ch1_sec02a_part0.tex`:47,60,77) · F-03 자리당 소문자(:319–321) · F-05 제목 `(N#)` 0 · F-06 프리앰블(`common_preamble_v1024.tex`:9,23–25) · F-07 `\item[` 0 · F-09 cases 단축 · F-10 비주석 "요동" 0(단 독립 부록에 13회 — F-10 집행 범위 밖, R4b G26; "되먹임" 병기 없음 1건 R4a §5.4) · F-11 ③ §3.5 `\appendix` 뒤 이동. **미검증** = F-04 본문 산문 스윕·F-08 도입부 분량(grep 판정 불가). FB3 집행 규약(`HANDOVER_v24.md`:83): 요동/양성 → 영문(body 0) · 음함수/섭동/준위 → 국문 + 첫 병기 · 유일근 → "유일한 근" · 정준/대정준·분배함수 = 유지 확정(재-litigate 금지, `plans/2026-07-22-v1024-feedback-revision-plan.md`:34–39).
- **v1.0.24/25 결정**(R3 A-5): 존속 = D-A @2 opt-in·D-B gallery opt-in·D-C regsol/@1/@3/@4 커널 배제(해석적 기록 보존·Ω 전량 존치)·DG-1 "regsol 삭제"(사용자 verbatim, `HANDOVER_v25.md`:46 — **코드 결정**)·Ω 물리 전량 유효·gallery ≠ 상(XRD 상 수 불변)·@2 α = 현상학 형상 파라미터(tier C, 4-손잡이 축퇴)·$w_\mathrm{eff}$ 폭 읽기 금지(FWHM ∝ λ^{3/2})·$C_\mathrm{bg}$ 창-국소 상수·comp_v24 무수정/addendum 우선·원본 아카이브 불가침·Task #38 park. **v1.0.25 한정** = D-D 국소 수정 원칙·DG-2 파일명 유지(사용자 verbatim "파일명을 왜 바꿔? 버전명만 바꿔주면 되는거 아니냐?" :47). **폐기** = v1.0.25 모델 배분(Opus 5.0/4.8 요지 인용) → 2026-09-02 전원 Fable 5.1.
- **D21/D22 계열**(R3 A-6, grep 위치 확인·상세 미검증): D22 "활물질별 재편"(`docs/v1.0.21/HANDOVER_v1.0.21.md`:18) = 현행 구조의 근거 → brief 3.3 (b) Part I/II 재구조와 **직접 충돌** → DG-A 는 D22 supersede 를 명시하는 사용자 결정이어야 함(DR-12) · D22-8 병합 빌드 금지·3장 분리+xr(`plans/2026-07-18-v1023-…-plan.md`:72) → v1.0.27 단일 문서 vs 분리 빌드 결정 필요(DR-12) · D22 "사후 제거 조항"(통계역학 증축) 승계 · D21-1 항법판 → D22-1 폐기(식 의존성 지도 기능은 재구조 시 재필요 가능성, R2 §2.2 판단).
- **노테이션·용어·서지 규약**(R3 A-7): 확률 소문자 p·상태함수 대문자·자리당 소문자 f_int/s_int·Helmholtz F vs Faraday F 문맥 구분·용어 정책(억지 한글화 배제·정준/대정준 유지)·서지 = 원장 V1 키만·기억 서지 0·표준 정리 무인용 관용(`SM2_SURVEY.md`:5)·tier A/B/C 규약(`ch1_sec07_broadening.tex`:64 각주 전역 정의) — 존속·승계. **regular solution 역어 이원화** = "정규용액"(sec11 1·sec13 12·mech 2·appD 2·부록 7) vs "정칙용액"(sec16b 4·sifr 7·ch3 bib 1) [R4b G26 확정] → 결정 필요(DR-20).
- **미완·미결**(R2 §4): 해소 = N1 빌드·N2 push·N10 게이트 재확인. 미해소 = N4 흑연 두-상 4 vs 2(Dahn 1991 본문)·N6 CSV 8종 보존·N7 재현 스크립트·N8 sigr 프로토콜·N9 다중셀·N11 G-금지 원천 모순·N13/Task #38(Non-goal). v1.0.26 = R2:R-1 평형 데이터 재검 미실행·R2:R-2 흑연 0.104 V 피크 FWHM ≲1 mV 정체 미판정·R2:R-3 regsol 되살리기 사용자 결정 미기록·R2:R-4 skew-logistic-7 최선 발견 문건 미반영. park = R2:P-2 FR 보류 풀 M 158+L ~120·P-3 병합 이관 5항(착수 근거 미발견)·P-6 Fisher/Legendre–Fenchel·P-10 IMPROVEMENT #4·P-12 voice 복원 옵션 3·P-13 항법 3종 폐기.

### 2.5 방향성 유실·park·미착수 (작업 챕터 1.4 등록부의 시드 — R1 §5 L-01~L-23 · R2 §4 N/R/P · R3 B-1~B-12 통합 예정)

- **미계승 지속 [R3 B-1 확정]**: ★Eyring 근본식 척추(사용자 6-11; 현행 = §5 TST bgbox·§8 lag 국소 유도만, `ch1_sec05_width.tex`:13–14,88,112·`ch1_sec08_lag.tex`:100; FABLE "v12 척추 결정 필요" 이후 결정 기록 **근거 미발견**) · S0~S5·16-울타리(본문 0건, FITTING_GUIDE 에만 D3 선별 복원) · §1.18 적층 준안정·athermal 훅(0건, park 지속) · KWW/장벽분포(0건, **2026-06-30 radius 조사 [MODEL-1 선택] → v1.0.11 Non-goals** 로 scope-out(R1 L-04·R3 B-1) — R6 R-2·DQ-3 의 "v1.0.15 [MODEL-1 선택]" 은 시점 오기로 판정[fixer]·부록 A DQ-I17; 그 선택이 사용자인지 master 인지 **미검증**) · "필요한 식만 vs 자기완결" 긴장(2026-09-02 기준 1·2 가 자기완결 쪽으로 해소한 것으로 읽힘 — 사용자 확인 대상, R3 DQ-13).
- **원구상 Chapter 2~5 ↔ 현행 대응 [R3 B-2·R6 §2]**: 발열 = Part T(가역 발열만 — 비가역은 "유지" 한 줄·[C-92] warnbox(정의 §2.0)) · 반응속도론 = §5·§8·§9·부록 E 보유·분산(독립 동역학 장 없음) · **통합 상태방정식 = 대응 절 근거 미발견(미착수)** — 실질 씨앗 = `eq:sum`·`ch2_sec08_synthesis`:13–22·"한 자유에너지의 두 응답"(`ch2_sec07_revheat.tex`:74–94) · 히스테리시스 = §4·§13·§3.4·부록 재료별 분산. 결론(R6 §2 추정): 원구상 Chapter 2~5 의 **내용**은 현행에 대부분 있으나 계층 순서로 배열돼 있지 않다 — brief 3.3 (b)안은 원구상을 Part I 네 장으로 되살리는 것과 동치.
- **ROADMAP 제안 2~5 [R3 B-3·R5 §1.3]**: 제안 1 vib Einstein 집행 · 제안 2 Ω(ξ) 미착수(v1.0.25 는 대신 현상학 α_j 채택, "물리적 동기는 조성 의존 Ω(x) 류" 자인 `ch1_sec06_eqpeak.tex`:69–71) · 제안 3 Cahn–Hilliard→γ_j 미착수(CH 는 부록에만 :439) · 제안 4 BV+Nernst–Planck 미착수(`Nernst.Planck`·`Warburg` 0건) · 제안 5 PSD 의도적 scope-out 유지(`ch1_sec07_broadening.tex`:313).
- **IMPROVEMENT·LIT_ADVANCE·SURV·SM2 [R3 B-4~B-7]**: #4 정칙용액 자유에너지 = 실측 역전으로 코드 삭제·문건 "미채택" 보존 → 재개방 핵심(DG-1 코드 결정과 문건 이론 채택 분리 필요, R3 DQ-7) · LIT ★군 반영 여부 미검증(1.2 에서 확정) · SURV Tier1 집행(부록 E)·Tier2 Fisher 미집행·Preisach 연산자 채택 = D(명명 노트만, R3 DQ-15) · **SM2-A/B/C 세 건 모두 v1.0.22 집행 확정**(`ch1_sec06_eqpeak.tex`:74–119 [V22-SM2-A]·`ch1_sec02b_part0.tex`:387–409 [V22-SM2-B]·`ch2_sec07_revheat.tex`:74–95 [V22-SM2-C] — brief §4.5 "미확정" **정정**, R3 B-7·R5 §1.1) · SM2 축 B staging 미시화 "스코프 밖" 은 서브 판단(사용자 결정 기록 아님) → 재판정(R3 DQ-16·R5 DQ-8) · flow-1 사다리 대조표·flow-3 기호 충돌표 미집행 → 4.0/3.4 산출물 · anodefit 캠페인 B·E 미착수(Non-goal)·D1~D7 응답 근거 미발견·Campaign A 성패 미검증.
- **v1.0.20~v1.0.26 신규 발견 [R2 §4]**: 완성도 검증 V2~V5(GITT×T·율 ∝|I|·휴면 판정·L_V Arrhenius·M-제거 증명·식별성) 집행 근거 미발견 → 1.4 시드 추가 · 항법 3종 폐기(사용자 결정) · voice 복원 옵션 3 사용자 판단 미집행 · v1.0.22 다음 버전 후보 7건 후속 근거 미발견 · P4 Fisher D3 보류.
- **서지 측 유실 [R7 §1.2]**: 원장에만 있고 bib 에 없는 키 4(`safran1980`·`safran1987`·`williamswatts1970`·`kohlrausch1854` — KWW scope-out·Safran 범위 밖의 결과로 추정, 삭제 시점 기록 미발견) · bib 에 있으나 원장 미등재 키 6(`lee2017jcp`·`lee2011jcp`·`son2013jcp`·`schmitt2022`·`verbrugge2017`·`artrith2018`).

### 2.6 판독이 확정한 진단 정량 (작업 챕터 2 게이트의 기준 좌표 — 검수 sub 재검 전 "작업 sub 판정")

| 축 | 정량(출처) | 비고 |
|---|---|---|
| 기준 1 유도 완결 | Ch1 범위 boxed 41 = 있음 22·부분 16·없음 1(eq:qrev — Bernardi 원식 미기재 `ch2_sec07_revheat.tex`:18)·N/A 2(R4a §2) / Ch2·Ch3·부록 boxed 23 = 완결 14·부분 2(eq:lcoomega-kernel·eq:si-coupling)·비유도 7(R4b §3) → 전 문건 64 = 있음/완결 36·부분 18·없음 1·비유도/N-A 9 | 두 판정 척도(R4a 3단+N/A / R4b 완결·부분·비유도)가 다르므로 2.2 에서 통일(R4a DQ-1·R4b DQ-8). 비박스 결과식 대체 8 라벨(R4a N1~N8) + 박스 우선순위 역전 후보 6 항목 = 7 라벨(R4b §3 — eq:lco-SeV·eq:lco-U1V 가 한 항목) → **판정 행 단위 = 라벨, 합 15**(항목 단위 14) + 논리 결함 42건 G01~G42(R4b §4, 자인되지 않은 3건 = G11 순환·G18 층위 혼합·G04 등치 선언) |
| 기준 1 서식 | (a)~(d) 표지 0 인 절 7 = §7 broadening·Part T §2.1·2.2·2.3·2.5·2.7·부록 E(R4a §2.2) | 헌법 ③ 서식이 절의 약 1/3 미적용 |
| 기준 5 가정 사다리 | Ch1 간소화 지점 35(레퍼런스 × 17·유효범위 × 5·가정 미명시 2; 최우선 S10 ΔC_p=0 암묵·S16 n_j 다중도 기원 0·S23 z_cut=4.357·A_cap=4.0 선택값, R4a §3) / Ch2·3·부록 30(일반형 식 제시 9·일반형 박스 1 = 독립 부록 eq:app-fxi·사다리 역전 2 G01·G21·출발식 postulate 2 G08·G23, R4b §5) | 사다리 위쪽 절반 부재(R5 §2 굵은 단 L1·L2a·L2b·L2d·L2e·L3d·L3f·L6a·L6b·L6d·L7) |
| 기준 3 서지 | bibitem 95·distinct 93·cite 265(262+3)·키 단위 315·DOI 84·Crossref 전건 해소 · 실질 결함 R-01 `verbrugge2017` 제목 오류+`msmr_origin2017` 과 동일 DOI 10.1149/2.0341708jes 이중 키 · R-02 `schmitt2022` 첫저자 J.→C.·4인 생략 · R-03 `koebbing2024` 권·호 미반영(원장은 34(7) 해소) · R-04 `sethuraman_stresspot2010` 쪽 공란(A1253) · R-05 관사 · R-06 et al. 4건 · bib 헤더 카운트 스테일(39/14/14 vs 44/15/36) · V1023 원장 = V1022 md5 동일 사본 · 무인용 본문 절 4(§3·§6·§8·§9 — 줄수는 집계 기준별 병기: R7 주석 제외 115·125·142·240 / R4a 파일 줄수 121·131·148·253)·저밀도 3(§2b·§4·T4) · 이론 원전 키워드 본문 0회(Marcus·Kramers·Onsager·Nernst–Planck·Fokker–Planck·Preisach·KWW·Kubo·Ising·Redlich–Kister·Safran) · 필수 문헌 체크리스트 12주제 ~150행, 이론 층 X 48건 중 38건 DOI Crossref 확인 완료(R7 §1·§3·§4) | 1차 원전 공백 후보 = R4a §4.3 15주제·R4b §6.3 8계열·R5 §5 (N) 32건·R6 신규 서지(de Groot–Mazur·Prigogine·Onsager·de Donder·Kramers·KWW·Marcus/Chidsey·Warburg) — 상당수가 R7 §4 에서 DOI 확인됨 |
| 기준 2·4 형식 | 정의·정리·증명 환경 0·예제 2(+부록 수치예 1)·연습 0·keybox 없는 절 6·F-11 본문 토큰 3~7·F-04 버전 태그 본문 13줄(Ch1)+12곳(Ch3)·검수 ID "#7" 5회·고백조 6·tier 표기 21건·두문자어 미전개 11종·기호표 h_η 누락·U_oc 소스 이원화·SOC/SoC 혼용(R4a §5·R4b §4·§7) | tier 표기와 교재 register 의 양립·버전 번호 없는 지위 서술 규약 필요(DR-21) |
| 구조 | orphan 1(`ch1_appD_si`)·독립 미편입 1(`appendix_phase_separation`, v1.0.14 사용자 결정 "별도 문건" — 요지 표기)·같은 유도의 다중 수록 3계열(정칙용액 커널 3곳 `ch1_sec05b_gr2L.tex`:43/`ch1_sec16b_lcoomega.tex`:24–31/`ch3v22_sec02b_sifr.tex`:83–87 · Sommerfeld 2곳 · spinodal 3곳)·Part 0↔Part T 중복 유도 4쌍(eq:sm-logistic/eq:logistic 등, R4a §7)·Ch1 의존 식 라벨 distinct Ch2 27/Ch3 18(R4b §1.4)·부록↔본문 Ω 정의식 상이(`appendix_phase_separation.tex`:100–102 Ω≡zN_AΔw vs `ch1_sec02b_part0.tex`:24 Ω≡−(z/2)N_Au, R5 §6-6)·기호 충돌 국소 각주 8항(g 4종·q 3종·u_j 2종·γ 2종·F 2종·z 2종·ξ↔θ 배향·Ω 정의식 — R5 TH-9.2) | R4b §8.1 다중 수록 3계열 = 3.3 (b)안 지지의 스코프 내 실증(R4b 판단) |
| 두-상 커널 판정 상충 | v1.0.24 @3 채택(Si 0.9944) → v1.0.25 @3 역전(−0.53%p, 전이 승격 조건) → v1.0.26 HANDOVER "@3 +0.67%p 유일 실효(별개 ablation)" → v1.0.26 A/B regsol-4 대체 불가(ΔBIC +844.5)·흑연 Ω≈2RT 참·skew-logistic-7 최선(R2 DQ-5) | 조건(전이 수·프로토콜·소재·지표)이 전부 달라 2.6 에서 표로 분리 |

### 2.7 cumulative step 좌표

직전 arc(v1.0.25 계획)는 Step 1~31 로 종결·v1.0.26 조사는 ledger 없음(A7). 본 마스터 플랜은 **새 arc** 이므로 **Step 1 부터** 단조 누적한다(Phase 를 넘어도 리셋 없음). 판독 산출 R1~R7 은 arc 착수 전 사전 조사이므로 Step 번호를 갖지 않으며, 1.1 인벤토리에 "시드" 로 등재된다. Step 이력 파일 = `Claude/results/Step <N> — <제목>.md`(step 하나 = 파일 하나). 본 초안의 번호 = 챕터 1 Steps 1–13 · 챕터 2 Steps 14–32 · 챕터 3 Steps 33–50 · 챕터 4~7 은 51 부터 연속(3.7 Result 후 세부 계획서에서 부여).

### 2.8 구조 맵

```
D:\Projects\Project_Anode_Fit\
├─ CLAUDE.md                                   프로젝트 지침 P1~P5(89행; brief 표기 90)
├─ Claude\
│  ├─ docs\
│  │  ├─ INDEX.md                              문건 MOC(197줄)
│  │  ├─ v1.0.25.1\  ★현행 최신(동결 base·무수정) — ch1/ch2/ch3 *_v1.0.24.tex · appendix_phase_separation.tex(독립)
│  │  │   · _sections\(56, ch1_appD_si.tex = orphan) · Anode_Fit_v1.0.24.py(1917) · test_gates_*.py · results\(HANDOVER_v25·v24·TOUCHUP_NOTE·INDEX_v25·tools_*.py·MERGE_READINESS·CHANGE_LEDGER·DATA_ADDENDUM …) · PDF 3
│  │  ├─ v1.0.25\    base(무수정) · v1.0.24.1\ · v1.0.24\  동결 아카이브(불가침)
│  │  ├─ v1.0.26A-regsol\README.md(199) · v1.0.26B-gallery\README.md(193)   v1.0.26 결과 문서(tex 무변경)
│  │  ├─ v1.0.15\CLOSING_v1.0.15.md(106)     헌법 3종 · v1.0.18.2\ROADMAP_future_physics.md(50)
│  │  ├─ v1.0.20\results\V1020_REFERENCE_LEDGER.md(55) · v1.0.21\…V1021(38) · v1.0.22\…V1022(33) · v1.0.23\…V1023(33 = V1022 사본)
│  │  ├─ v1.0.20\plans\(PLAN_P0~P8 + v1020 master) · v1.0.22\plans\(PLAN_R1/R2/R3/R5/RA/FR) · v1.0.22\results\comp_v23\(SURV_SYNTHESIS·SURV1~4) · comp_SM2\SM2_SURVEY.md
│  │  ├─ Fable_점검\(8 md·885줄)               이력 전수감사(01·02·03·note A1~A5)
│  │  └─ v1.0.10~v1.0.24\ · _archive\          구버전(HANDOVER_* 각 폴더)
│  ├─ plans\  INDEX.md(65, 스테일) + 91 계획서(9503줄)
│  ├─ results\
│  │  ├─ V1024_EXECUTION_LEDGER.md · V1024_FEEDBACK_EXECUTION_LEDGER.md   12-col 실례
│  │  ├─ comp_v24\(USER_FEEDBACK·VERSION_COMPARISON·IMPROVEMENT_DIRECTIONS·LIT_ADVANCE_SYNTHESIS·sintef_data\ …)
│  │  ├─ comp_v26_data\(README·HANDOVER_regsol_investigation[stale]·regsol_kernel.py·test_skew_regsol_v2.py·test_gallery_vs_regsol.py·build_two_versions.py·make_version_docs.py·out_versions\build.log·out_skew\[폐기]·test_skew_regsol.py[폐기])
│  │  ├─ regsol_test\[untracked·폐기 판정] · process\(ledger 26·HANDOVER 4·C3_*[untracked]) · research\(ledger 2)
│  │  └─ handoffs\2026-09-02-v2-master-plan\{brief.md, audit_checklist.md(루트 — 검수 sub 지침), iter_1\{plan_draft.md, work_log.md}, wf\{R1_…R7_*.md, R7_reference_master_map.json, audit_spec.md·audit_format.md·audit_logic.md(v2 감사 3본), plan_draft_v2.md, plan_draft_v3.md ← 본 파일, fix_change_log.md}}
│  ├─ old\Archive_oldtrack\(PHASE_DIAG_REFS67_DOSSIER.md(50) · HANDOVER_RB_* 3 · COMPARISON_*/REVIEW_LEDGER_*[동명이물])
│  ├─ JCP_147(14)_144111_(2017) - Effects of external electric field.pdf · jcp_extract.txt
└─ Codex\   ★무접근(읽기 포함)
```

**신규 예정(저작 시 생성 — 생성 시점에 이 맵을 즉시 갱신)**: `Claude/plans/2026-09-02-v2-master-plan.md`(master 최종 저장) · `Claude/plans/2026-MM-DD-v1027-phase-<id>-plan.md`(별도 세부 계획서) · `Claude/results/Step <N> — <제목>.md` · `Claude/results/PHASE_<id>_V1027_<topic>_RESULT.md`(+`.json`) · `Claude/results/PHASE_1-7_V1027_EXECUTION_LEDGER.md` · 등록부·레지스터·블루프린트(§Implementation Changes) · `Claude/docs/v1.0.27/`(4.0) · `Claude/docs/v1.0.27/results/V1027_REFERENCE_LEDGER.md`(+`.json`) · `Claude/docs/v1.0.27/results/refcheck/`(Crossref 응답 보존, R7 규약 4(e)) · `Claude/docs/HANDOVER_v1.0.27.md`(6.3).

### 2.9 이력 인벤토리 실측·판독 커버리지·미검독

| 군 | 실측(v1 sub) | 판독 8본이 전문 정독한 것(중복 제거 전 합산 — 참조용; 본 arc 정독 범위는 DR-7 사용자 확정 = 핵심 전문 + 토픽 한정) | 미검독(정독 배정 Phase) |
|---|---|---|---|
| `Claude/plans/*.md` | **92 파일·9,567줄(master 실측 2026-09-03 = 날짜 계획서 89 + `INDEX.md` + `MASTER_ROADMAP_*` 2)** — v1 sub 91/9,503·brief 90/9,567 은 집계 기준 차이(1.1 에서 파일명 단위로 정본화) | 8본(A8·B6·B7·v1021·v1022·v1024 completeness·v1024 feedback + anodefit) | 83본 |
| `docs/**/PLAN_*.md` + `docs/v1.0.20/plans/2026-07-16-v1020-master-plan.md` | 15 + 1 | 0 | 16본 전부 |
| `HANDOVER*.md` | **25(old/ 제외)·1,612줄 / old/ 포함 28 — master 실측 ✓ 2026-09-03**(brief §3-C 의 "28본(old/ 제외)" 은 old/ 포함 건수를 잘못 붙인 것 — 정본 = 25/1,612, old/ 3본은 구트랙 별도 표시); `HANDOVER_v24.md` 사본 4곳 | R1 14본·R2 7본·R3 1본(중복 포함) → 고유본 약 20 | v1.0.10(HANDOVER_v1.0.10)·v1.0.12·구트랙 3 등 잔여 + hash 판정 |
| `docs/Fable_점검/*.md` | 8·885줄 | R1 6본(01·A1~A5) | 02·03 |
| `CLOSING_v1.0.15.md` | 1·106줄 | R1·R3 전문 | — |
| INDEX | `docs/INDEX.md` 197·`plans/INDEX.md` 65·`INDEX_v25.md` 139 | R1(docs·plans)·R2(INDEX_v25)·v1 sub 전문 | — |
| ledger | `Claude/results/**/*LEDGER*.md` 30(results 2·process 26·research 2) + `docs/vN/results/` 내 ledger(V1021·V1022·V1024_REFLECT·V1025_CHANGE 등, 미실측) | 서지 원장 4본(R7) | 나머지 전부 |
| 조사 문서군 | comp_v24·comp_v26_data·comp_v23(SURV1~4)·comp_SM2·ROADMAP·v1.0.26 README 3본·dossier | R2·R3·R5·R6·R7 가 전문 정독(SURV1~4·SM2·LIT·IMPROVEMENT·ROADMAP·README 3본·dossier·build.log) | comp_v24 나머지(FIT_CHECK·DATA_REGISTRY·ABLATION·GRAPHITE_STAGING_XRD·AUDIT·SOURCES·REFLECT_SEED_TABLE)·MULTI_DATASET_REVIEW·`docs/v1.0.25.1/results/` 나머지(MERGE_READINESS·CHANGE_LEDGER·DATA_ADDENDUM·DOC_EDIT_REPORT·T13_T14·CASCADE_TODO·CODE_GUIDE·FITTING_GUIDE)·V1020_STYLE_RUBRIC·V1013_TERMS_POLICY·V1014_TONE_AUDIT |
| 현행 문건 tex | 60 tex·9214줄 | R4a 29본(5558줄)·R4b 24본(3324줄)·R5·R6 보강 정독 → `_sections` 56 중 미정독 = `ch1v22_partT_divider`·`ch1_preamble`·`ch2_preamble`·`common_preamble_v1024`(grep 만) + 마스터 tex 3본(부분) | 위 지원 4본 + 마스터 3본 전문 — **배정 = 2.1 Step 14**(2.7 Read Coverage 에 계수); 나머지 53본 = 2.2 Step 17~19 |
| 코드·PDF·JCP | 코드 1917줄·PDF 3종·JCP PDF·jcp_extract | 0(존재 확인만) | 코드는 Non-goal(수치 대조 목적 읽기만) · JCP PDF·jcp_extract 는 S-2(refs ② 확정)에서 정독 |

**미검독 명시(추정 금지)**: 위 표 우측 열 전건 · `Codex/` 전체(금지). 본 통합 에이전트(v2)는 판독 산출 8본·v1 초안·work_log·brief·양식 정본 2본만 전문 정독했고, v3 fixer 는 그 위에 `audit_checklist.md`(루트)·plan_draft_v2 를 더해 정독했을 뿐 원천 실물(tex·md·PDF)은 직접 열지 않았다 — 본 문서의 path:line 은 전부 판독 산출이 기록한 근거의 전사이며, 1.1~1.2 에서 실물 재대조 대상이다.

---

## Phase Range

> ★ **이름공간 대응 주석(P3 #7).** 아래 "작업 챕터 1~6" 은 **본 계획의 작업 단위**다. 문건에는 "Chapter" 이름공간이 넷 더 있으므로(R6 DQ-11: brief 는 3축을 말하나 CLAUDE.md P1 원구상까지 세면 넷) 다섯 축을 한 표에 고정한다. 보고서·이력에서 둘 이상을 함께 쓸 때는 "작업 챕터 N / 문건 Chapter N / ver.N / 원구상 Chapter N / 후보 Part" 로 명시한다.

| 축 | 단위 | 값 | 출처 |
|---|---|---|---|
| 작업 챕터(본 계획) | 1~6 | 이력 통합 / 진단 / 이론 설계 / 저작 / 서지 / 검수·마감 | brief §5 |
| 문건 Chapter(현행 v1.0.25.1) | 1~3 | 흑연(+Part 0·Part T·부록 A~E) / LCO / Si·혼합 — 파일 접두는 반전(`ch2_sec*`=Ch1 Part T, `ch1_sec11~17`=Ch2) | 마스터 tex 3본·`HANDOVER_v1.0.22.md`:45 |
| 역사적 ver. | 1~5 | `graphite_ica_dynamic_ver5.tex` 적층 구조(현행 문건 `ver.N` 0건) | `CLAUDE.md`:14·R3 A-3 |
| 원구상 Chapter | 1~5 | 전하보존 / 발열 / 반응속도론 / 통합 상태방정식 / 히스테리시스 — 현행 대응 = §2.5 둘째 항목(R6 §2 표) | `CLAUDE.md`:15–17 |
| 확정 구조(DR-3·DR-11·DR-12·신규 요구) | Ch1 / Ch2 / Ch3 | **재료별 3장 유지 · 분리 빌드+xr(병합은 완성 후 옵션)**. **Ch1 흑연** = 열역학·동역학 이론 집중(Part I 흑연 사슬 + Part T 열특성·히스) + **후반부 부록 D = 통계역학 전체(교과서급 — 더 길고 상세, 비전공자·타전공 석박사 가독)** + 상분리 편입(DR-11 master 판단) · **Ch2 LCO·Ch3 Si·블렌드** = Ch1 에 없는 분기만(음극 흑연·Si 예측 강화 우선) · **코드 절·코드맵 = 문건 밖**(DR-14) | 사용자 2026-09-03 |
| 산출물 ID / 판독 ID / 자산 태그 | `OUT-*` / `R#:<ID>` / `[태그]` | **본 계획 산출물 = `OUT-` 접두**(OUT-PLAN·OUT-DETAIL·OUT-INV·OUT-REG1~3·OUT-GAP·OUT-BP·OUT-DOC·OUT-REFLEDGER·OUT-STEP·OUT-RESULT·OUT-LEDGER·OUT-HANDOFF·OUT-HANDOVER·OUT-INDEX1/2·OUT-CLAUDEMD — §Implementation Changes). **판독 문건 내부 ID** 는 접두 없이 쓰면 다음 출처를 뜻한다: `R-1~R-4`·`P-1~P-16`·`N1~N13` = R2 §4(v1.0.26 미결·park·v1.0.25 미완; 다른 ID 와 나란히 쓸 때는 `R2:` 접두) · `K/E/T/R/S/H/Q-x` = R6 후보 · `TH-x.y` = R5 후보 · `R-01~R-06` = R7 서지 결함 · `#n`·`N1~N8`·`S1~S35` = R4a · `G01~G42`·`A01~A30` = R4b · `L-01~L-23` = R1 §5 · `A-n`·`B-n` = R3 등록부 · `D-A~D-D`·`DG-1/2`·`D21-n`·`D22-n`·`D1~D6` = 사용자 결정 이력(R3 A-5·A-6·A-1). **자산 태그** = 절 말미 `% 자산` 주석의 다계열([C-nn]·[V21-Qn-nn]·[V22-SM2-X]·[V22-R5-nn]·[LCOΩ-n]·A-0nn — 2.1 Step 14 확정) | [fixer] — 감사 LOGIC-02(같은 문서 안의 ID 충돌 해소) |
| Test Plan 게이트 ID · D-계열 | `T-1`~`T-21` / `D#` | **Test Plan 의 게이트 ID = `T-1`(LaTeX 빌드)~`T-21`(가독성)**. R6 후보 `T-1`(entropy production)·`T-2`(선형 flux–force)와 이름이 겹치므로 R6 후보는 본문 전건 `R6:T-1`·`R6:T-2` 로 접두한다. D-계열 4종도 문맥 접두로 구분: `CLOSING D1~D6` / `v1.0.23 D1~D4` / `anodefit D1~D7` / `FB 계획 D1` | [master] — 비평 #1·#14 |

| Phase | 이름 | Steps(cumulative) | 게이트 요지(정량) | 정지·결정 | 시드 | 상태 |
|---|---|---:|---|---|---|---|
| **1.1** | 인벤토리·정독 배정 | 1–2 | 인벤토리 전건 path+줄수(Test-Path True 100%)·빌드 포함/orphan 열·brief §3-C 건수 차이 열거·untracked Claude 8 지위/Codex 13 무접근 표기·정독 배정표 = **핵심 문건 전문 + 세부 계획서·ledger·result 는 토픽 한정 정독(DR-7 사용자 확정)** + 정독 주체·범위 열 · Phase Result | (DR-7 확정) | 본 §2.8·§2.9 | 대기 |
| **1.2** | 버전별 변경점 등록부(RB→v1.0.26) | 3–7 | 필수 행 31/31(brief 30 + v1.0.11) + 병기 행 5(S2·S3·E1·E3·[계획 전용] — S1 RB·S4 Fable v2 는 필수 행과 동일 행) = 36/36(= R1 26 + R2 10) · 11열 빈 셀 0 · 수치 불일치 4건 실물 확정 · verbatim 등급 열 · Phase Result | — | R1·R2 | 대기 |
| **1.3** | 유효 결정·제약 등록부 | 8–9 | 헌법 3종·P3 8항·F-01~11·D/DG·D21/D22·용어·노테이션·서지 규약 전건 = path+line + verbatim/요지 등급 + 상태{존속/v1.0.25 한정/폐기/스테일} · 미검증 항목 0(F-04·F-08·D21/D22 본문) · Phase Result | 통제문서 모순 시 더 제한적 지시 채택 | R3 A | 대기 |
| **1.4** | 방향성 유실·park·미결 등록부 | 10–12 | 시드 3원(R1 §5 23·R2 §4 33·R3 B 12절) 통합 ID · **6열**(원 지시 시점·유실/park 시점·현행 처리 상태·재개방 후보 여부·근거 path·시드 출처) 빈 셀 0 · 실물 확인 항목(SM2·Fisher·LIT ★군·V2~V5·Campaign A) 판정 근거 첨부 · 유실 자산 원문 정독 목록 4건(정독/미정독 표시) · 명시 결정 대기 표 · Phase Result | — | R1 §5·R2 §4·R3 B | 대기 |
| **1.5** | Result — 챕터 1 | 13 | 챕터 통합 Result `PHASE_1_V1027_HISTORY_RESULT.md`+`.json`(1.1~1.4 Phase Result 4쌍 위) · Ledger 행 5 · Read Coverage 행 범위(정독 주체 열) · 문서 렌즈셋 6종 3-Pass | — | — | 대기 |
| **2.1** | 자산 지도 | 14–15 | 카운트 정의 고정(모집단 = 파일 집합 60 = 빌드 58 + 미포함 2) 후 재계수 = brief §4.2 전건 일치 · 마스터 3본 + 지원 4본 전문 정독(행 범위) · boxed 64 ID 표(라벨 부재 1 표시) · 빌드 포함/미포함 열 · 자산 태그 계열 확정 · G-금지 게이트 실물 수 · diff 3+3+hash · touch-up 4건 판정 · **v1.0.26A/B 자산 지도(DR-1 A+B)** · Phase Result | — | 본 §2.2 표·R4a §1·R4b §1·R2 §2.10 | 대기 |
| **2.2** | 유도 완결성 감사(기준 ①) | 16–20 | 판정 척도 4단 통일 · **작업 sub 전문 정독(53본, 청크 19) + 64 판정 행 재작성 → 검수 sub refute 1R 이상 → master 삼각검증** · 비박스 결과식 15 라벨 + display 166 스크리닝 · GAP-ID 통합(R4a #·N + R4b G01~G42) · 청크 ≤~500(최대 ~700)·렌즈 follow+적대검산 · Phase Result | — | R4a §2·R4b §3·§4 | 대기 |
| **2.3** | 일반성·가정 사다리 감사(기준 ⑤) | 21–23 | 간소화 지점 65(S1~S35 + A01~A30) 6열 빈 셀 0 · 계보도 잎 = boxed 64 전건 · R5 §2 23단·R6 §5 6 rung 과 대조 · Phase Result | — | R4a §3·R4b §5·R5 §2·R6 §5 | 대기 |
| **2.4** | 서지 감사(기준 ③) | 24–26 | 95/95 검증표(R-01~R-06 GAP) · 원장 체인 대조(미등재 6·원장 only 4·사본 문제) · 절별 밀도 49행·무인용 4절 · 1차 문헌 공백 스크리닝(체크리스트 ~150행 대조) · Phase Result | DR-6 | R7 §1~§4·R4a §4·R4b §6 | 대기 |
| **2.5** | 형식·register 감사(기준 ②④) | 27–29 | 형식 요소 체크표 49(+115)행 · F-04/F-10/F-11 + 헌법 ① 잔존 grep 수치(토큰 정의 확정 후) · 가독성 7항목(T-21 진단판)·교재 형식 요소 체크표(T-20 진단판)·두문자어·기호표·역어·F-02/F-03 노테이션 grep · Phase Result | DR-14·DR-20·DR-21 | R4a §5·R4b §7 | 대기 |
| **2.6** | v1.0.26 regsol 미결의 설계 입력화 | 30–31 | 네 판정 상충표(조건 분리) · LCO Ω 커널 지위 · 관측 폭 vs 평형 폭 층위 · 정식화 문서 (i)~(v) · 커널 단위 기본값 · N4 · 필요 데이터·실행 여부 · Phase Result | DR-1·DR-6·DR-10 | R2 §2.10·§4·R5 TH-2.1·R6 H-2 | 대기 |
| **2.7** | Result — GAP REGISTER | 32 | 챕터 통합 Result `PHASE_2_V1027_GAP_RESULT.md`+`.json`(2.1~2.6 Phase Result 위) · GAP 전건 4-tier · Read Coverage = 본 arc Read 로 v1.0.25.1 9214줄 전 영역 + v1.0.25 diff hunk 4건 | — | — | 대기 |
| **3.1** | 후보 이론 조사·평가 | 33–37 | 승계 표(집행 완료·기각·미집행) 전건 · R5+R6 통합 카탈로그(A 13·B 20·C 18·D 승계) 경계 정리 · 신규 검색(DR-6) 서지 DOI 확인 · 평가 열 8(등급·모델 차원·침습도·서지·선행 데이터·기준 1~5 기여·회수 조건·재검산 대상) 빈 셀 0 · 기각군 재조사 0 · Phase Result | DR-6·DR-15~18 | R5 §1·§3·§4·R6 §4·§6·§7·R7 §4 | 대기 |
| **3.2** | 통합 골격 설계("일반→특수" 사다리) | 38–41 | 열역학·동역학·열/히스 사다리 각 단 = 가정·레퍼런스·회수 조건 3열 빈 셀 0 · 정직 조건 4 명기 · boxed 64/64 회수 매핑 + 비박스 핵심식 15 · 회수 불가 0(또는 설계 GAP) · Phase Result | — | R5 §2·R6 §5 | 대기 |
| **3.3** | 문건 구조 설계(사용자 확정 구조의 내부 배열안) | 42–43 | Ch1 내부 배열(본문 = 거시 열역학·동역학 유도 / 후반 부록 D = 통계역학 교과서급 + 상분리 편입) · Ch2/Ch3 분기 목록(Ch1 에 없는 것만·Ch1 결과식 xr 대응 열) · 자산 이동 맵 **57/57** · 코드 절·코드맵 문건 밖 이전 맵 · 분리 빌드+xr 키 설계 · 본문/부록 분할 규칙 → 배열안 · Phase Result | — | R6 §2·R4b §8·R3 A-6·신규 요구 | 대기 |
| **3.4** | 수식 사슬 원형(derivation skeleton) | 44–46 | 목표 boxed 목록 · 사슬 계획 4열 + **목표 boxed 별 사다리 좌표(축·단 ID)·가정 ID·레퍼런스 V1 키 열(T-19 계획판)** · 신규/승계/회수 100% · 라벨 alias 정책 · dependency graph 1본 + 4분류 표(R6:S-5) · Phase Result | — | R4a §7·R4b §8·R6 S-5 | 대기 |
| **3.5** | 레퍼런스 마스터 원장 설계 | 47–48 | 원장 재개설 설계 + 규약 10조항 확정 + refcheck/ · 주제별 필수 문헌 맵(축×단) 빈 칸 0 · Phase Result | DR-6·DR-19 | R7 §4·§5 | 대기 |
| **3.6** | 설계 적대검토 | 49 | refute mandate·최약점 ≥1·빈 통과 금지 · **커버리지×렌즈 6종 완주 + 연속 2R 확정결함 0 수렴 + 10R 하한**(BLUEPRINT = 고가치 reference 등급 — DR-23 기본값) · SymPy 재검산 ≥3 · Phase Result | DR-23 | — | 대기 |
| **3.7** | Result — THEORY BLUEPRINT + 보고(비차단) | 50 | 챕터 통합 Result md+json(3.1~3.6 Phase Result 위) · Phase audit 3-Pass · R5·R6 DQ 24건 해소/이관표 · **DG-B 채택 이론 목록 = master 확정**(사용자 위임 DR-11·15~18·23) · DG-A/DG-C = 사용자 기확정 · 사용자에게 보고 후 무중단 진행(사용자만 결정 가능한 항목이 새로 생기면 그 항목만 정지) | 보고 | — | 대기 |
| **4.0~4.9** | 저작 v1.0.27(Ch1 이론 집중 → 부록 D 통계역학 → Ch2/Ch3 분기 → 3장 정합) | 51– | 절 단위 루프 · 분리 빌드 게이트(xelatex 3-pass err 0·undefined 0·STRUCTURE PASS) · **전 tex 코드 토큰 0**(DR-14) · **학술 용어 영어 원어·tier 표기 0**(DR-20·21) · Phase 별 Result · (a)~(d) 사슬 · T-19/T-20/T-21 절별 · boxed 회수 합 64/64(Step 41 매핑표 기준) | 3.7 Result 후 세부화 | R5·R6 배치 열·3.3 배열안 | 대기 |
| **5.1~5.3** | 서지 완결 | (4 에 이어 연속) | 원장 DOI 전수 검증·한 문헌 한 키·저자 전원 · **전문 리뷰 논문 서지 포맷(DR-19)** · 절별 밀도 하한 · Result | 3.7 Result 후 세부화 | R7 §5 | 대기 |
| **6.1~6.3** | 검수·수렴·마감 | (5 에 이어 연속) | 10R + 커버리지×렌즈 6종 완주 **둘 다**(follow 변형 = 수식·박스·라벨만 노출한 청크 ≥1회) · P3 8항(현행 기호 재해석)+헌법 3종+F 게이트+T-19/T-20/T-21 · 빌드 GREEN·PDF·HANDOVER·INDEX·commit·push | 3.7 Result 후 세부화 | — | 대기 |
| **7.1~7.3** | 코드 동기(doc-leads) — DR-4·DR-9 | (6 에 이어 연속) | 문건↔코드 대응 지도(문건 밖 OUT-CODEDOC) · 코드 개정(additive·기본 경로 bit-exact 폴백·게이트 GREEN) · 공개데이터 재현·문건이 서술한 극한·수치 결과 = 코드 출력 · Result | 챕터 6 종료 후 세부화 | v1.0.25 코드·v1.0.26 조사 코드·현행 코드맵 | 대기 |

> Phase/step 수·범위는 **최소 기준점**이며 검토 필요 시 확장·신규 Phase 추가가 가능하다(silent 누락 금지·명시 deferral + Decision Queue 등재). 챕터 1~3 이 v1 초안(1–10 / 11–24 / 25–40) 대비 13 / 19 / 18 로 늘어난 근거는 「Correction History」v2 행.

---

## Non-goals

> brief §6 그대로 + 판독이 확정한 경계.

- **챕터 1~6 동안 코드 수정 X** — 코드 동기는 작업 챕터 7(문건 확정 후, DR-4·DR-9). 그 전까지 기존 코드(`Anode_Fit_v1.0.24.py`·조사 코드 `regsol_kernel.py` 등)는 읽기·실행(수치 대조 목적)만. **문건 본문·부록 어디에도 코드·스크립트·파일명 언급 X**(DR-10·DR-14 — 코드맵·코드 절·부록 E 대응 지도는 문건 밖 코드 문건 OUT-CODEDOC 으로 이동). `CODE_GUIDE_v24`·`FITTING_GUIDE` 갱신(R2:P-14)은 챕터 7.
- `Claude/docs/v1.0.25/`·`v1.0.25.1/`·`v1.0.24*/`·`v1.0.26A-regsol/`·`v1.0.26B-gallery/` 수정 X(동결 base·비교 기준). 작업은 항상 `docs/v1.0.27/` **신규 사본** 위에서 하거나 새로 쓴다(DR-13 — 이전 버전 산출물은 기록용). 동결 base 의 결함(P3 #8 위반 3~7건·서지 R-01~R-06·라벨 없는 boxed 1·orphan)은 **base 에서 고치지 않고** GAP REGISTER 에 등재해 v1.0.27 저작에서만 반영한다.
- `Codex/` 접근 X(읽기 포함).
- 역문제·상태추론(anodefit 캠페인 E·Tikhonov/MaxEnt 역산 — SURV3 기각군)·전셀 합성(캠페인 B) X.
- 회사 데이터 의존 정량(Task #38: stage-2L 0.30 mV/℃·Ω 점값·LCO 전자항 T-의존·α↔$L_V$ 율속 분리·CLOSING Part 4 (ii)~(iv)) X — 필요 항목은 warnbox·tier 로 정직 표기. 다온도 의존 후보(TH-2.3 Ω(T)·TH-7.2 Debye 파라미터화·TH-1.4)는 일반식만 적고 파라미터화는 opt-in·tier C.
- 새 공개데이터 **상시 파이프라인** X — 단 필요한 논문·데이터는 그때그때 찾아 쓴다(DR-6 확정: 외부 논문·데이터 즉시 확보 허용; 조사·확보 = Haiku/Sonnet 서브). 기존 확보 데이터(`results/comp_v24/sintef_data/`·`comp_v26_data/` CSV) 재사용 허용.
- 기각군 재조사 X — R5 §1.2 12건·R6 §6 20항(Wiener–Hopf·WKB·다중척도·중심다양체·Langevin·Preisach 연산자/연속 밀도/FORC·동적 Kubo 승격·RG 장치·안장점 독립 절·LDT·볼록최적화 전역해·Bazant/Dreyer PDE 생성기·비대칭 커널 "문헌 근거" 주장·전이 6+ 증설·DFT 결합E→Ω 대입·블렌드 역학 결합·Si 소성 구성식 창작·경로의존 소산 정량·Jarzynski/Crooks·비등온 T(V) 되먹임). Preisach 는 명명·embed 노트 한정(C).
- **S0–S5 역방향 식별 사슬·16-울타리는 두 갈래로 나눈다.** (i) 피팅 알고리즘·코드 구현(Optuna 대체 절차 등) = DR-4 별도 코드 플랜 소관 → 본 계획 Non-goal. (ii) 식별 사슬의 **본문 서술 편입**(기준 5 사다리의 역방향·G-usable) = Non-goal 이 **아니라** 1.4 명시 결정 대기 항목 → 3.3/3.4 결정 후보 → DG-B(R1 DQ-7·R3 B-1 "재개방 검토"; R6 §6 마지막 행은 카탈로그 범위 선언이지 기각 판정이 아니다). DR-16 인접.
- 나노 PSD·Gibbs–Thomson 확장 X(마이크론 흑연 범위, `ch1_sec07_broadening.tex`:313) — Non-goal warnbox 유지(TH-5.4).
- **독자 참여형 섹션 X**(사용자 2026-09-03 "이 문건은 논리 전개가 주") — 예제(Example)·연습문제(Exercise)·풀어보기·독자에게 계산을 맡기는 어떤 장치도 두지 않는다. 교과서 형식은 정의·유도·중간식·요약·회수 표로만 구현하고, 저자가 수행한 극한·부호·크기 확인은 논리 전개의 문장("…이면 …로 환원된다")으로 적는다 — 박스 이름도 "검산"·"verify" 류의 독자 지시형 명칭을 쓰지 않는다. 현행 worked example 3곳(§10 흑연·§15 LCO·Part T 발열)과 verifybox 15개는 v1.0.27 에서 독자 참여 장치 없이 결과 서술로만 전환한다.
- **tier A/B/C 표기 X**(DR-21) — 신뢰·가정 상태는 서술로 적는다(매크로·각주 정의 제거). **학술 용어의 한글 억지 번역 X**(DR-20) — 문장 골조는 한글, 학술 용어는 영어 원어(regular solution·entropy production·affinity 등); 한국 학술용어는 존중, 일본식·중국식 번역어 배제, 애매하면 영어.
- 효율을 이유로 검수 하한을 낮추는 것 X(사용자 기준 6). 정독 범위는 **사용자 확정(DR-7)** = 핵심 문건 전문 + 그 밖(세부 계획서·ledger·result)은 토픽 한정 정독 — 축약이 아니라 범위 정의이며, 등록부 각 행의 근거 절은 반드시 원천에서 정독한다.

---

## Implementation Changes

> 비코드 프로파일: **산출물 변경 대장**. 파일명 중 brief §7 규정분은 규정대로, 등록부·레지스터·블루프린트 파일명은 v1 작업 sub 제안(`Claude/results/V1024_*` 접두 관행 승계, `iter_1/work_log.md` DQ-4)을 승계하며 master 가 확정한다. "시드" 열 = 판독 산출·v1 실측 중 그 산출물의 초안이 되는 것. **산출물 ID 는 `OUT-` 접두**로 통일한다 — v2 의 P-/R-/D-/S-/H-/C-/I- 접두가 판독 문건 ID(R2 §4 R-1~R-4·P-1~P-16, R6 S-1~S-5·H-1, R7 R-01~R-06)와 충돌했기 때문이다(Phase Range 이름공간 표 마지막 행).

| ID | 산출물 | 위치(제안 포함) | 생성/갱신 | 소유 Phase | 시드 | 게이트 |
|---|---|---|---|---|---|---|
| OUT-PLAN | 마스터 플랜(본 문서의 최종본) | `Claude/plans/2026-09-02-v2-master-plan.md` | 생성(master) | — | v1 초안·본 v2 | 11-section 순서·이름 보존 · `plans/INDEX.md` 행 갱신 |
| OUT-DETAIL | 페이즈별 세부 계획서 | 챕터 1 = 본 문서 Phase 1.1~1.5 절 / 챕터 2·3 = Phase 착수 시 `Claude/plans/2026-MM-DD-v1027-phase-<id>-plan.md`(본 문서 Phase 절이 시드) / 챕터 4~7 = 3.7 Result 후 별도 파일(챕터 7 은 챕터 6 종료 후) | 생성 | 각 Phase 착수 시 | R5·R6 배치 열 | Phase 착수 전 존재 · 매 Step 착수 시 재독 |
| OUT-INV | 이력 인벤토리 | `Claude/results/V1027_HISTORY_INVENTORY.md` | 생성 | 1.1 | 본 §2.8·§2.9(v1 초안 §2.8 실측 승계) | Test-Path 100% · 줄수 실측 · orphan 검사 · brief §3-C 차이 열거 · untracked 8/13 · 정독 배정표(정독 주체 열) |
| OUT-REG1 | 등록부 ① 버전별 변경점 | `Claude/results/V1027_REG1_VERSION_CHANGES.md` | 생성 | 1.2 | **R1 + R2**(초안·통합 필요) | 31+5 = 36행 · 11열 빈 셀 0 · 불일치 4건 확정 |
| OUT-REG2 | 등록부 ② 유효 결정·제약 | `Claude/results/V1027_REG2_BINDING_DECISIONS.md` | 생성 | 1.3 | **R3 등록부 A** | 전건 path+line+등급+상태 · 미검증 0 |
| OUT-REG3 | 등록부 ③ 방향성 유실·park·미결 | `Claude/results/V1027_REG3_LOST_DIRECTIONS.md` | 생성 | 1.4 | **R1 §5 + R2 §4 + R3 등록부 B** | 통합 ID · 6열 · 유실 자산 원문 정독 목록 · 명시 결정 대기 표 |
| OUT-GAP | GAP REGISTER | `Claude/results/V1027_GAP_REGISTER.md`(+`.json`) | 생성 | 2.1~2.7 | **R4a·R4b·R7 + 본 §2.2 표** | 4-tier · boxed 64 판정 · 간소화 65 · 서지 95 · GAP-ID 통합 |
| OUT-BP | THEORY BLUEPRINT | `Claude/results/V1027_THEORY_BLUEPRINT.md`(+`.json`) | 생성 | 3.1~3.7 | **R5·R6 카탈로그 + R7 §4·§5** | 카탈로그·사다리·구조안·skeleton·원장 설계·적대검토 · DG-A/B/C 안건서 |
| OUT-DOC | 새 문건 v1.0.27 | `Claude/docs/v1.0.27/`(DR-2) — 마스터 tex·`_sections/`·프리앰블·bib(원장 생성)·PDF | 생성 | 4.0~4.9 | 현행 60 tex 자산(신규 사본 위에서 저작, DR-13) + 블루프린트 + 3.3 배열안 | 분리 빌드 GREEN·STRUCTURE PASS·**전 tex 코드 토큰 0**(DR-14)·라벨 매핑 429/429 |
| OUT-REFLEDGER | 서지 마스터 원장 + 검증 로그 | `Claude/docs/v1.0.27/results/V1027_REFERENCE_LEDGER.md`(+`.json`) · `refcheck/` | 생성 | 3.5 설계 → 5.1~5.3 확장 | **R7 §2 표·json 부본·§5 규약** | DOI 검증 100% · 기억 서지 0 · 한 문헌 한 키 · bib 생성 |
| OUT-STEP | 스텝 이력 | `Claude/results/Step <N> — <제목>.md` | 생성(step 하나=파일 하나) | 전 Step | — | 5항목 |
| OUT-RESULT | Phase Result | `Claude/results/PHASE_<id>_V1027_<topic>_RESULT.md` + `.json` — id = 1.1~7.3 각 Phase(topic 은 세부 계획서에서 확정, 예: 1.1 INV·1.2 REG1·1.3 REG2·1.4 REG3·2.1 ASSET·2.2 DERIV·…) · 챕터 말 Phase 는 챕터 통합 Result 를 겸함(id = 1·2·3·4·5·6·7, topic = HISTORY / GAP / BLUEPRINT / AUTHOR / BIB / CLOSING / CODE) | 생성 | **매 Phase 종료(1.1~7.3 전건)** — 스킬 2b "매 Phase 종료 시 Result 12항목(md+json)·Result 없이 다음 Phase 진입 금지"·헌법 §0 Result 생략 금지 | — | 12항목 · Read Coverage 행 범위(정독 주체 열) |
| OUT-LEDGER | Ledger | `Claude/results/PHASE_1-7_V1027_EXECUTION_LEDGER.md` | 생성·갱신 | 각 Phase 종료 | — | 12-col |
| OUT-HANDOFF | 핸드오프 | `Claude/results/handoffs/<task>/` | 생성 | 서브 스폰 시 | 본 폴더 | brief + iter_N/wf |
| OUT-HANDOVER | 인계 | `Claude/docs/HANDOVER_v1.0.27.md` | 생성 | 6.3 | — | 5항목 + chain |
| OUT-INDEX1 | `Claude/docs/INDEX.md` | 갱신(행 추가 — 기존 행 무수정) | 갱신 | 6.3(및 v1.0.27 폴더 생성 시) | — | 본문이 진실·INDEX 갱신 |
| OUT-INDEX2 | `Claude/plans/INDEX.md` | 갱신(활성 행 추가; 스테일 정정은 별도 작업 — `iter_1/work_log.md` DQ-11) | 갱신 | OUT-PLAN 저장 시 | — | |
| OUT-CLAUDEMD | CLAUDE.md 개정안(문서만) | `Claude/results/V1027_CLAUDE_MD_REVISION_PROPOSAL.md` | 생성 | 6.3 | R3 A-3 스테일 조항 + P3 #8 "코드 = 부록 전용" → "코드 = 문건 밖"(DR-14) + 용어 정책(DR-20)·tier 폐지(DR-21) | 사용자 결정 전 CLAUDE.md 무수정(DR-13) |
| OUT-CODEDOC | 코드 대응 문건(**문건 밖**, DR-14) | `Claude/docs/v1.0.27/code/CODE_MAP_v1027.md` — 현행 `ch1_appB_codemap`·`ch2_appB_codemap`·`ch3v22_sec05_code`·부록 E 대응 지도의 이전지 + boxed↔함수 1:1 표 | 생성 | 4.0(이전)·7.1(갱신) | 현행 코드맵 4본 | 문건 tex 코드 토큰 0 · 대응 100% |
| OUT-CODE | 코드 v1.0.27(doc-leads 동기) + 게이트 | `Claude/docs/v1.0.27/code/Anode_Fit_v1.0.27.py` · `test_gates_v1027*.py` · `CODE_GUIDE`·`FITTING_GUIDE` 갱신 | 생성 | 7.2~7.3 | v1.0.25 코드 1917줄·v1.0.26 조사 코드 | 골든 bit-exact 폴백·게이트 GREEN·문건↔코드 1:1·`PHASE_7_V1027_CODE_RESULT` |
| — | **불변** | `docs/v1.0.24*/`·`v1.0.25/`·`v1.0.25.1/`·`v1.0.26A/B/` · 코드 · `Codex/` · `comp_v24/`·`comp_v26_data/` 원본(정정은 addendum) · 이전 Result/Ledger/HANDOVER(immutable) · 판독 산출 R1~R7(초안 보존 — 정정은 등록부·레지스터에서) | 무수정 | — | — | 결과 문건 보호(Addendum/Supersession/Correction) |

---

## Phase 1.1 — 인벤토리·정독 배정 (Steps 1–2)

**목적.** 작업 챕터 1(이력 통합)의 정독 대상 전건을 실물로 고정하고 정독 배정표를 만든다. **정독 범위(사용자 확정 DR-7, 2026-09-03 "토픽이 있는 곳만 제한적으로 한정하여 정독")** = ① **전문 정독**: 마스터플랜급 계획서(`*master*`·`*MASTER*`·`MASTER_ROADMAP*`)·인계 chain 전건(HANDOVER 25 + old/ 3)·Fable 감사 8·CLOSING·INDEX 3·서지 원장 4·v1.0.26 실물 3본·dossier·유실 원문 tex 5본의 해당 절 ② **토픽 한정 정독**: 페이즈 세부 계획서·ledger·result·조사 문서군은 구조 추출(Phase 표·게이트·결정·Correction History)로 등록부 행을 세운 뒤, 행의 근거가 되는 절만 원천에서 정독한다(행 범위 기록). 판독 R# 기정독은 참조 열에 표시한다. 검수 sub 는 등록부 확정 근거 행을 원천에서 전건 대조한다(cross-check). Read Coverage 표에는 **정독 주체·범위 열**(전문 / 토픽 한정 / 판독 R# 참조 / 검수 대조)을 둔다. 이 규칙은 축약이 아니라 사용자가 정한 범위 정의이며, 등록부 게이트(빈 셀 0·근거 path+line)는 그대로다.

**입력.** §2.9 실측·판독 커버리지 표 · `docs/INDEX.md` · `plans/INDEX.md`(스테일) · `docs/v1.0.25.1/results/INDEX_v25.md` · 세션 시작 git 스냅샷 · R1~R7 각 Read Coverage 절.

- **Step 1 — 인벤토리 파일 생성(OUT-INV)**: 다음 군을 **전건 path + 줄수 + 버전 귀속 + 문서 종류 + 판독 정독 여부(R# 표시)** 로 등재한다 — (i) `Claude/plans/*.md` 91 + `INDEX.md` (ii) `Claude/docs/**/PLAN_*.md` 15 + `docs/v1.0.20/plans/2026-07-16-v1020-master-plan.md` (iii) `HANDOVER*.md` 25(old/ 제외) + old/ 3(구트랙 별도 표시) — `HANDOVER_v24.md` ×4 폴더 등 동일 파일명 사본은 hash 로 중복 판정해 고유본만 정독 대상(v1 DQ-14) (iv) `docs/Fable_점검/*.md` 8 (v) `CLOSING_v1.0.15.md` (vi) `docs/INDEX.md`·`plans/INDEX.md`·각 `docs/vN/results/INDEX_v*.md` (vii) ledger = `Claude/results/**/*LEDGER*.md` 30 + `docs/vN/results/*LEDGER*.md`(V1021·V1022·V1023·V1024_REFLECT·V1025_CHANGE 등 실측) (viii) 각 버전 `MERGE_READINESS_*`·`CHANGE_LOG/LEDGER`·`PHASE_*_RESULT.md`·`AUDIT_LINEAGE`·`V1025_DATA_ADDENDUM`·`DOC_EDIT_REPORT`·`T13_T14`·`CASCADE_TODO`·`ARCHIVE_NOTE` (ix) 조사 문서군 = `results/comp_v24/*.md`·`comp_v26_data/*.md`·`docs/v1.0.22/results/comp_v23/*.md`·`comp_SM2/*.md`·`comp_FR/`·`docs/v1.0.18.2/ROADMAP_future_physics.md`·`docs/v1.0.20/results/`(FIGS_PICK·DIRECTION_*·TRIAGE_P7·V1020_STYLE_RUBRIC)·`V1013_TERMS_POLICY`·`V1014_TONE_AUDIT` (x) `old/Archive_oldtrack/PHASE_DIAG_REFS67_DOSSIER.md`·`jcp_extract.txt` (xi) **v1.0.26 실물 3본**(`docs/v1.0.26A-regsol/README.md`·`docs/v1.0.26B-gallery/README.md`·`results/comp_v26_data/README.md`) + `out_versions/build.log`(R2 DQ-2) (xii) **서지 원장 4본**(V1020~V1023, R7 §1.2) (xiii) **2026-07-19 reflect 계획서·`V1024_REFLECT_EXECUTION_LEDGER.md`**(R2 DQ-3) (xiv) git untracked 21건 = **Claude 측 8건**(`docs/v1.0.17~18.2` png 5·`results/process/C3_*` 2·`results/regsol_test/`)의 지위(유효/폐기 — `regsol_test/` 폐기 판정 R2 §2.10, `C3_*`·`sample_test_*` = R2:P-7 관련 추정 R2 DQ-11) + **Codex 측 13건**(`Codex/work/*`)은 지위 = "Codex 소관·무접근(판정 안 함)" 으로 고정 기재(열람 0 — 지위 판정을 위해 Codex 폴더를 여는 일이 없도록) (xv) 판독 산출 R1~R7 + R7 json + v1 초안·work_log(시드 등재) (xvi) 현행 60 tex — **마스터 3본 `\input` 대조로 빌드 포함/미포함 열**(orphan `ch1_appD_si.tex`·독립 `appendix_phase_separation.tex`, R4b DQ-3).
  - 명령(재현 가능): `Get-ChildItem -Recurse -Filter '*.md' | ForEach-Object { "$($_.FullName)`t$((Get-Content $_.FullName).Count)" }` 를 (i)~(xv) 각 경로에 적용; hash = `Get-FileHash -Algorithm SHA256`; orphan = 마스터 tex 의 `\input{…}` 목록과 `_sections/*.tex` 파일 목록 차집합.
  - 증거: OUT-INV 표 + 군별·전체 합계(파일 수·줄수) + 실측 명령 출력 첨부 + brief §3-C 건수·줄수(plans 90·9567 / HANDOVER 28·1612)와의 차이 파일 목록 + 판독 커버리지 대조(R# Read Coverage 절의 파일 집합 ⊆ OUT-INV).
- **Step 2 — 정독 배정표**: OUT-INV 전건을 **계보 순(§2.3)** 으로 정렬해 정독 순서·청크(≤~500줄 창, 최대 ~700; 800줄 미만 파일만 통째)·담당(작업 sub 직렬 — 유닛 1개)·Read Coverage 기록 양식(파일·행 범위·**정독 주체**)·**검수 대조 방식**(①군 = 전문 정독 + 검수 대조 / ②군 = 구조 추출 + 근거 절 정독 + 검수 대조; 판독 기정독은 참조 열 — DR-7 확정)을 확정한다. 정독 순서 규칙 = comp_v24 원본 → `V1025_DATA_ADDENDUM.md`(충돌 시 addendum 우선, `HANDOVER_v25.md`:150–152) · 구트랙 파일은 경로 병기(동명이물 경고). ①군 전문 / ②군 토픽 한정(DR-7 사용자 확정).
  - 게이트: 배정표 파일 집합 = OUT-INV 파일 집합(차집합 0) · 각 파일에 청크 경계(행) 명시 · 총 줄수 합계 = OUT-INV 합계 · 판독 기정독 참조 열 = R# Read Coverage 와 일치 · 정독 주체 열 빈 셀 0.

**게이트 1.1(정량).** OUT-INV Test-Path True 100% · 줄수 열 빈 셀 0 · **brief §3-C 건수·줄수(plans 90·9567 / HANDOVER 28·1612)와의 차이를 파일명·줄수로 열거하고 정본 확정**(§2.9 의 91/9503·25/1612 vs brief 90/9567·28/1612) · 배정표 차집합 0 · 빌드 포함/미포함 열 60/60 · untracked Claude 8건 지위 열 빈 셀 0 · Codex 13건 = 무접근 표기(열람 0). **중단 조건.** 인벤토리 군 실물 부재 발견 → 미검독·부재로 표기하고 진행(정지 아님). **다음 조건.** Step 1·2 이력 파일 + `PHASE_1.1_V1027_<topic>_RESULT.md`+`.json`(12항목) + Ledger 행 저장.

## Phase 1.2 — 버전별 변경점 등록부 RB→v1.0.26 (Steps 3–7)

**목적.** 계보의 각 버전이 **무엇을 바꿨고(구조/물리/식/코드/게이트/결정/페이지) 그 근거가 어디에 있는지** 한 표로 고정한다. 챕터 3.2 자산 회수 매핑과 3.3 구조 결정의 이력 근거다. **시드 = R1(구트랙 RB→v1.0.19, 26행·9열·§3 보조 등록부·§4 규범 성립 시점 14건·§5 유실 L-01~L-23) + R2(v1.0.20→v1.0.26, 10행·§2 상세·§3 연결선·§4 미완 N/R/P)** — 두 초안은 원천 대부분을 인계·감사·계획서로 읽었고 plans 잔여·ledger·docs/vN/results 결과물·Fable 감사 02/03 은 읽지 않았다.

**등록부 행(누락 0 의 기준 집합 = 필수 31 + 병기 5 = 36 = R1 §2 표 26행 + R2 §1 표 10행).** 필수 = brief §4.3 계보 30(RB · Fable v2 · v3 · v4 · v5 · v6 · v7 · v8 · v9 · v10 · v1.0.10 · v1.0.12 · v1.0.13 · v1.0.14 · v1.0.15 · v1.0.16 · v1.0.17 · v1.0.18.1 · v1.0.18.2 · v1.0.19 · v1.0.20 · v1.0.21 · v1.0.22 · v1.0.23 · v1.0.24 · v1.0.24.1 · v1.0.25 · v1.0.25.1 · v1.0.26 A/B + Fable 이력감사) + **v1.0.11**(R1 DQ-3). 병기 = 선행 행 S2 6-07 Ch2~5 야간 초안·S3 6-10 TBR + 결정 원천 E1 6-30 radius 조사·E3 v1.0.15 KICKOFF + [계획 전용] 2026-07-18 anodefit MASTER·완성도 검증(R1 §1·R2 §2.5). R1 의 S1(구트랙 RB)·S4(6-11 Fable v2 백지)는 필수 행 RB·Fable v2 와 **같은 행**이므로 별도 계상하지 않는다(v2 의 "병기 7·합 38" 은 이중 계산 — 감사 FORMAT-04·LOGIC-07). Ch2 트랙·코드 트랙·부록 트랙은 §3 보조 등록부로 분리 유지.

**열(11).** 버전 · 날짜(원천 기재; 추정은 표시) · 구조 · 물리·식(신설·삭제·라벨 증감) · 코드 · 게이트/빌드 · 페이지 · 결정(사용자 verbatim / 요지 — **등급 열 병기**) · 유실·park·미결 · 근거 path(+line) · 판독 출처(R1/R2/신규).

- **Step 3 — RB → v1.0.19 보강 정독**(범위 = 1.1 규칙: 인계·감사 전문 / plans·ledger·results 는 토픽 한정): R1 미정독 원천 정독 — `FABLE_AUDIT_02_ch1ch2_content.md`·`FABLE_AUDIT_03_code_fitness.md`, 해당 구간 plans(2026-05-29~07-08), docs/v1.0.10~v1.0.19 각 폴더의 HANDOVER(v1.0.10·v1.0.12 등 R1 미정독분)·PLAN_*·ledger·results, `results/process/` ledger 26·HANDOVER 4, `research/` ledger 2, `research/broadening_w_design.md`(L-21 ρ(U_j) 잔존 주의). R1 표 행별 4-tier 보충을 원천으로 재확인·보강 → 행 1~22.
- **Step 4 — v1.0.20 → v1.0.26 보강 정독**(범위 = 1.1 규칙): R2 미정독 원천 — `plans/2026-07-19-v1024-si-2L-codex-reflection-plan.md`·`V1024_REFLECT_EXECUTION_LEDGER.md`·`V1024_FEEDBACK_EXECUTION_LEDGER.md`·`PHASE_FB*_RESULT.md`·`MERGE_READINESS_v24/v25`·`V1025_CHANGE_LEDGER`·`V1025_DATA_ADDENDUM`·`V1025_DOC_EDIT_REPORT`·`V1025_T13_T14_REPORT`·`V1025_DOC_CASCADE_TODO`·`ARCHIVE_NOTE`·`MULTI_DATASET_REVIEW`·comp_v24 나머지(FIT_CHECK·DATA_REGISTRY·ABLATION_ANODE·GRAPHITE_STAGING_XRD·AUDIT_v1024_DOC_CODE·HIST_*·REFLECT_SEED_TABLE·SOURCES)·docs/v1.0.20~23 results(ledger·CHANGE_LOG·AUDIT_LINEAGE·comp_FR·PHASE_P*·FIGS_PICK·DIRECTION_*·TRIAGE_P7·V1020_STYLE_RUBRIC)·`V1013_TERMS_POLICY`·`V1014_TONE_AUDIT` → 행 23~31. 이 Step 에서 확정할 미검증 항목: 완성도 검증 V0~V6 의 집행 여부(R2 DQ-3) · Campaign A(M 제거 증명) 성패·anodefit D1~D7 응답(R3 DQ-9) · LIT_ADVANCE ★군의 v1.0.24.1/25 반영 여부(R3 DQ-8) · N11 G-금지 게이트 수(실물 `test_gates_v1025.py` 확인은 2.1 로 이관, 여기서는 문서 기록만) · v1.0.24.1 폴더 실체화 vs 계획 D1 "in-place"(R2 DQ-9).
- **Step 5 — 보조 등록부·동명이물·수치 확정**: Ch2 트랙(v3→v4→v5→v1.0.10)·코드 트랙(v11_final→v12→v1.0.10→…→v1.0.25)·부록(spinodal) 트랙(v1.0.14→v1.0.19→v1.0.25.1) 통합(R1 §3). 구트랙 `COMPARISON_*`·`REVIEW_LEDGER_*` 는 경로 병기 규칙으로 등록. **수치 불일치 4건 실물 확정**(R1 DQ-2): v1.0.10 Ch1 34p/35p → `docs/v1.0.10/` PDF 또는 aux LastPage · `Anode_Fit_v11_final.py` 617/706 → `(Get-Content).Count` · v3 2758/2759 · v4 2912/2735/~2771 → 실물 tex `wc -l`; 실물 부재 시 "양측 병기·미확정". 날짜 추정 행(v4·v5·Ch2 v5·v10, R1 DQ-8)은 master 가 `git log --follow` 로 대조(sub 는 git 금지) — 그 결과를 이 Step 이력에 기록.
- **Step 6 — verbatim 등급 확정**: 원천이 큰따옴표·「전문」·"생략 없이" 로 기록한 것만 verbatim, "요지" 표기는 요지(R1 DQ-10·R2 DQ-7). 확실한 verbatim 목록(R1 DQ-10) = 6-07(`HANDOVER_2026-06-07`:8)·6-30 7건·KICKOFF 4건·CLOSING 인용문·v1.0.13 GO 문장 + R2 원천 큰따옴표분(v1.0.20~26). v1.0.20 확장 분리 지시 이중 표기(`HANDOVER_v1.0.20.md`:17–18 vs `plans/2026-07-16-v1021-master-plan.md`:3, R2 DQ-6)는 병기하고 정본 선택은 master · `HANDOVER_v25.md`:37–49 지시 11건은 요지(지시 6 세 물리 질문 원문 = 사용자 제공 시 승격, R2 DQ-7).
- **Step 7 — OUT-REG1 통합 저장 + 사용자 평 반영**: R1+R2+Step 3~6 → OUT-REG1. "v19=구문 최고·v23=논리 최고"(A12:3 verbatim) 를 v1.0.19·v1.0.23 행 결정 열에 A12 line 인용으로 기재(R1 DQ-5 해소). 방향 전환 3지점(R2 §3: v1.0.23 역문제 후보 → v1.0.24 forward 반영 / V-계획 미집행 / @3 채택→삭제→재검증)을 §3 연결선으로 기록. 관통 규범 성립 시점 표(R1 §4 14건)를 OUT-REG2 연결용으로 부록화.

**게이트 1.2(정량).** 필수 행 31/31 + 병기 행 5/5 = 36/36 · 11열 빈 셀 0(근거 없는 셀은 "근거 미발견" 명기 = 빈 셀 아님) · 각 행 근거 path ≥1 · verbatim 등급 열 값 ∈ {verbatim / 요지 / 근거 미발견} · 수치 불일치 4건 확정 또는 "미확정·병기" · 사용자 평 행에 A12 line · R1·R2 DQ 22건(10+12) 각각 "해소/이관/미해소" 표기. **중단 조건.** 없음(부재 근거는 4-tier). **다음 조건.** Step 3~7 이력 파일 + OUT-REG1 저장 + `PHASE_1.2_V1027_<topic>_RESULT.md`+`.json` + Ledger 행.

## Phase 1.3 — 유효 결정·제약 등록부 (Steps 8–9)

**목적.** v1.0.27 저작이 **반드시 지켜야 할 것 / v1.0.25 한정이라 풀리는 것 / 폐기된 것 / 표기가 스테일한 것**을 출처 line 단위로 확정한다. 챕터 4 저작 게이트와 6.2 규범 게이트가 여기서 나온다. **시드 = R3 등록부 A(A-1 헌법·D1~D6 / A-2 프로세스 규율·Part 4 / A-3 P1~P5 현행 충족 상태 / A-4 F-01~F-11 grep 집행 확인 / A-5 v1.0.24/25 결정 / A-6 D21/D22 위치 확인 / A-7 노테이션·용어·서지 규약 / A-8 2026-09-02 지시 / A-9 anodefit)**. R3 는 `HANDOVER_v24.md`·v1.0.20~23 결정 이력 본문·appE 본문을 읽지 않았다.

- **Step 8 — 규범군 확정**: R3 A-1·A-2·A-4·A-7·A-8 을 원천 재대조로 확정하고, **미검증 2건 해소** = F-04 본문 산문 스윕·F-08 도입부 분량(grep 불가 항목 → `HANDOVER_v24.md`:77–89 FB3/FB6 집행 기록 + 현행 `ch1_sec11_lcointro.tex` 정독으로 판정) + **F-01 §1.1.4 필요성은 1.3 에서 "2.5 Step 27 이관" 으로 표기**(R3 A-4:85 — (a)(b) load-bearing / (c)(d) 배경 분리 재판정은 형식 감사 소관; D21-2 일반 top3 잔존과 연동 R3 A-6:126 — 비평 #4) + FB0~FB7 집행 기록 전건(R2 §2.7 확정 `HANDOVER_v24.md`:81–88 — brief §4.3·R3 A-4 의 "FB0~FB9" 표기는 이 Step 에서 원천 대조해 정정) + 지배 문서 4종(`CLOSING`·`V1020_STYLE_RUBRIC`·`V1013_TERMS_POLICY`·`V1014_TONE_AUDIT`) 정독 후 규범 행 추가 + `HANDOVER_v25.md` §③ 다음 세션 주의 11항. **상태 열 4값** = 존속 / v1.0.25 한정 / 폐기 / **스테일**(P1 원구상 Chapter·P3 #1 네 기호·P3 #6·P5 `ver.N` — 위반이 아니라 v1.0.22 재편 이전 표기, R3 A-3) — 스테일 조항은 "현행 기호·구조로 재해석해 승계" 하고 CLAUDE.md 개정안은 OUT-CLAUDEMD 로 분리(DR-13).
- **Step 9 — 결정군·규약군 확정**: R3 A-5·A-6·A-9 + D21/D22 본문 정독(`plans/2026-07-16-v1021-master-plan.md`·`2026-07-17-v1022-master-plan.md`·`docs/v1.0.21/results/V1021_*`·`docs/v1.0.22/results/*`) → D21-1~6·D22-1~8·D-1~D-7·D21-6′·v1.0.23 D1~D4(D3 만 사용자 확정, D1/D2/D4 는 기본값 집행 — R2 §2.4; v2 의 "D5" 는 R2 에 없음 — 근거 미발견)·D-A~D-D·DG-1/DG-2·v1.0.18 2-버전 결정·v1.0.14 spinodal "별도 문건"(요지)·v1.0.15 격자 퇴출(verbatim)·v1.0.26 "이미지 확인 후 결정" 예고(verbatim) 를 각 행 = 출처 path+line + verbatim/요지 + 상태 + v1.0.27 적용 방식(게이트 ID 예약). 추가 확정 항목: (a) **서브 저작 선언 vs 사용자 결정 분리** — Part T [C-92] "히스 소산·경로의존 정량 범위 밖"(`ch2_sec05_mixing.tex`:230–238)·"∂Ω/∂T 범위 밖"(:193–194)·SM2 축 B "스코프 밖"(`SM2_SURVEY.md`:41–42)·6-30 [MODEL-1 선택] → v1.0.11 Non-goals 의 KWW scope-out 은 사용자 결정 기록이 있는지 원천에서 확인해 "사용자 결정 / 서브 판단(개정 가능)" 으로 분류(R5 DQ-6·DQ-8, R6 DQ-2·DQ-3, R3 B-1) (b) CLOSING Part 4 (4) n(T)↔config 동반 규칙을 **이론 규칙**으로 등재(R3 DQ-12) (c) "필요한 식만(v7) vs 자기완결 교과서" 긴장 = 헌법 3종·2026-09-02 기준 1·2 로 해소된 것으로 기재하되 **사용자 확인 대상** 표시(R3 DQ-13; DR-22 연동) (d) dossier "임시 열람 후 삭제" 기록 vs JCP147 PDF 현 소장 불일치 표면화(R6 DQ-6; DR-8) (e) 데이터 프로토콜 규약(`gr.csv`=p-ocv·`si.csv`=p-ocvhold·comp_v24 원본 무수정·addendum 우선) (f) 자산 태그 계열(2.1 확정 전 "다계열" 로만 기재) (g) 서지 규약 = V1 키만·기억 서지 0·표준 정리 무인용 관용·tier 병기·서적 쪽수 인용 금지(`V1020_REFERENCE_LEDGER.md`:3,33·V1021:26,34·V1022:3, R7 §5 승계 근거).

**게이트 1.3(정량).** 전건 출처 line 존재 · 상태 열 4값 중 하나 · 등급 열(verbatim/요지) · 빈 셀 0 · 헌법 3종·P3 8항·F-01~11·D22-1~8·D21 = 각각 3·8·11·8·**≥5** 행 존재(D21 행 수의 출처 = `HANDOVER_v1.0.20.md`:32–44 의 D21-1~6 표(R2 §2.1) — R3 A-6 시드는 5행(D21-4 없음)이므로 Step 9 정독 후 확정) · 미검증 0(F-04·F-08·D21/D22 상세 해소; F-01 은 "2.5 Step 27 이관" 표기로 해소 계수) · "서브 판단(개정 가능)" 분류 항목 ≥4 각각 원천 근거. **중단 조건.** 두 통제문서 지시 모순 발견 → 더 제한적인 지시를 채택하고 DQ 등재(정지 아님; 사용자만 결정 가능한 blocking 이면 정지). **다음 조건.** OUT-REG2 저장 + `PHASE_1.3_V1027_<topic>_RESULT.md`+`.json` + Ledger 행.

## Phase 1.4 — 방향성 유실·park·미결 등록부 (Steps 10–12)

**목적.** 과거에 지시됐으나 계승되지 않은 방향, park 된 항목, 미착수 후보, 미결 사안을 **재개방 후보 여부**와 함께 고정한다. 챕터 3.1 후보 카탈로그의 시드이자 "재조사 0" 의 근거이며, 3.7 DG-B 안건의 예비 목록이다. **시드 3원 = R1 §5(L-01~L-23) · R2 §4(N1~N13·R-1~R-4·P-1~P-16) · R3 등록부 B(B-1~B-12)** — 세 시드는 ID 체계가 다르고 항목이 겹친다(R1 DQ-4: L-01 Eyring·L-03 적층·L-13 제안 2~5 가 양쪽에 걸침).

- **Step 10 — 시드 전건 등록·ID 통일**: 세 시드 + brief §4.5 + 본 §2.5 를 한 ID 체계(예: LD-nn, 원 ID 를 별칭 열로 보존)로 통합. 각 항목 = **원 지시 시점 · 유실/park 시점 · 현행 처리 상태(v1.0.25.1 grep·정독 근거) · 재개방 후보 여부{재개방/조건부/유지/승계 기각/DQ} · 근거 path · 시드 출처**. 항목 수 = 세 시드 합집합(중복 제거) — 게이트에서 합집합 수를 기록.
- **Step 11 — 실물 확인·정독 발견분**: (a) **SM2-A/B/C 집행 확정 반영** — v1 Assumptions 13·brief §4.5 "미확정" 을 확정 집행(`ch1_sec06_eqpeak.tex`:74–119·`ch1_sec02b_part0.tex`:387–409·`ch2_sec07_revheat.tex`:74–95 자산 태그, R3 B-7·R5 §1.1)으로 정정 → "재개방 후보 아님·승계"; SM2-E 흡수 여부는 2.2 확인 (b) SURV Tier2 Fisher 미집행(`Fisher` 0건)·Tier3 Legendre 명명 부분(`Fenchel` 0) 확정 (c) LIT ★군 반영 여부 = Step 4 결과 전사 (d) 완성도 검증 V2~V5(M-제거 증명·휴면 판정·L_V Arrhenius·식별성) 미집행 후보 추가(R2 DQ-3) (e) 원구상 Ch4 "통합 상태방정식·전기-열 coupling(implicit DAE)" 을 **별도 항목**으로 쪼개고 v1.0.20 이후(Part T·Bernardi·`eq:sum`·two-responses bgbox) 와 대조(R1 DQ-6) (f) 원장 only 4키(`safran1980`·`safran1987`·`williamswatts1970`·`kohlrausch1854`) 삭제 시점 기록 탐색(R7 DQ-5) (g) 항법 3종 폐기(R2:P-13, 사용자 결정)·voice 복원 옵션 3(R2:P-12, 사용자 판단 미집행)·FR 보류 풀 M158+L~120(R2:P-2)·병합 이관 5항(R2:P-3)·v1.0.22 다음 버전 후보 7건(R2:P-16) 등재 (h) 1.2·1.3 정독에서 새로 발견한 유실·park 추가 (i) **유실 자산 원문 정독 목록** — DR-15·DR-16·DR-17·DG-B 안건이 인계 요약이 아니라 원문에 서도록 네 실물을 해당 절 범위로 head→tail 정독하고 행 범위를 Read Coverage 에 기록한다: ① Fable v2 tex(Eyring 근본식 배열 17단위 — R1 S4; 실물 = `Claude/old/_archive/graphite_ica_ch1_Fable_v2.tex` — master 실측 ✓ 존재, Assumptions 23) ② Opus v5/v6 §1.15 S0~S5·16-울타리(`Claude/old/_archive/graphite_ica_ch1_Opus_v5.tex`·`…_Opus_v6.tex` — master 실측 ✓) ③ v3/v4/v5 §1.10 KWW/장벽분포(R1 L-04; `Claude/old/_archive/graphite_ica_ch1_Fable_v3.tex`·`…_Opus_v4.tex`·`…_Opus_v5.tex` — master 실측 ✓) ④ Opus v4 §1.18 적층 준안정·athermal 훅(R1 V4 행·DR-17). 미정독이면 해당 DR/DG-B 안건에 **"원문 미정독"** 을 명기한다. 이 목록은 brief §3-C 정독 범위 밖 확장이나 실물 5본 존재를 확인한 master 가 승인했다(DQ-I15 해소).
- **Step 12 — 명시 결정 대기 표 + 4축 대응**: FABLE §5-8 "Phase 4.1 명시 결정 항목" 5건(Eyring 척추 회복·§1.18/athermal 재개방·S0–S5 복원 범위·KWW 진단 prose·자기완결 vs 필요식만 조율 — 결정 기록 **근거 미발견**, R1 E2·R3 B-1) + regsol 되살리기(v1.0.26 사용자 예고) + 상분리 부록 편입(v1.0.14 "별도 문건" 결정 → 재개방은 사용자) + [C-92] 경계 + 원구상 Ch2~5 계층 회복 을 **DR-10~DR-18·DG-B 안건 예비 목록**으로 표화. 원구상 Chapter 1~5 ↔ 현행 3장 ↔ 후보 Part I/II ↔ 작업 챕터 4.x 4축 대응표(R6 §2)를 등록부 부록으로.

**게이트 1.4(정량).** 시드 합집합 전건 등재(합집합 수 명기·누락 0) · 6열(원 지시 시점·유실/park 시점·현행 처리 상태·재개방 후보 여부·근거 path·시드 출처) 빈 셀 0 · (a)~(i) 각 판정에 grep 수치 또는 path 첨부 · 유실 자산 원문 4건 정독/미정독 표시 · 명시 결정 대기 표 ≥9 항목 각각 원 지시 근거 · 4축 대응표 5행. **중단 조건.** 없음. **다음 조건.** OUT-REG3 저장 + `PHASE_1.4_V1027_<topic>_RESULT.md`+`.json` + Ledger 행.

## Phase 1.5 — Result: 챕터 1 (Step 13)

- **Step 13**: 챕터 통합 Result `Claude/results/PHASE_1_V1027_HISTORY_RESULT.md` + `.json`(1.1~1.4 의 Phase Result 4쌍 위에 챕터 종합; 12항목: Summary / Step Range 1–13 / Inputs / Files Created(OUT-INV·OUT-REG1~3) / Files Updated / **Read Coverage(파일·행 범위 전건 — 본 arc Read 만 계수, 판독 R# 커버리지는 참조 열)** / Execution Evidence / Validation·Gate·Confirmed / Non-Changes / Open Issues / Decision Queue / Next=Step 14) · Ledger `PHASE_1-7_V1027_EXECUTION_LEDGER.md` 행 1.1~1.5 · Phase audit(문서 렌즈셋 6종 = 사실 정합·출처/번호/카운트 일치·orphan 0·라벨·용어 잔존·follow-ability·usability — 헌법 "10차원×3-Pass" 의 문서 프로파일(스킬 3c), 3-Pass) · 검수 sub 청크 검수 ≥1R + 연속 2R 확정결함 0 수렴(등록부 3종 = A1·A2 통상 산출물 등급 — DR-23 에서 상향 가능).
- **게이트 1.5.** Result md+json 쌍 존재 · Read Coverage 합계 = 배정표 합계(차이 = 미검독 명시) · Ledger 행 5 · 검수 라운드 표. **중단 조건.** 없음(Result 미저장 = 챕터 2 진입 금지가 곧 게이트). **다음 조건.** Result 없이 챕터 2 진입 금지.

---

## Phase 2.1 — 자산 지도 (Steps 14–15)

**목적.** 진단의 기준 좌표계. 현행 두 버전의 자산을 기계 추출로 고정하고, 판독 4원(v1 작업 sub 실측·R4a·R4b·R7)이 서로 다른 정의로 센 수치를 **한 정의**로 통일한다.

- **Step 14 — 카운트 정의 고정 + 재계수**: 카운트 스크립트(§Test Plan T-4)를 v1.0.25.1 **파일 집합 60 tex(빌드 포함 58 + 미포함 2 — 열별 부분합 병기)** 에 재실행. **정의를 먼저 문서화**(R7 DQ-15·R4a DQ-7·R2 DQ-12): display = `equation/align/gather/multline(*)`(230) 과 `\[…\]`(38) 분리 · boxed = 전 문건 64(범위 분포 27/10/4/3/16/4) · cite = 명령 265(본문 262 + bib 내부 3)·키 단위 315 · bibitem 95·distinct 93 · 주석 줄 `%` 제외 여부 명시. → brief §4.2 표와 전건 일치 확인. `\boxed` 64 각각 = ID·파일·행·`\label`(부재 1건 `ch1_sec06_eqpeak.tex`:91 표시)·절·문건 Chapter·spine 노드(N0~N9/Part T/부록)·현행 지위(채택/해석적 기록/opt-in/비유도 박스). `\label` 429·`\bibitem` 95·distinct cite 93 목록 첨부(2.4·챕터 5·6 무유실 게이트 기준 파일). **빌드 포함/미포함 열**(orphan `ch1_appD_si`·독립 부록·`ch1v22_partT_divider` 등) · **자산 태그 계열 기계 추출**(v1 `[A-xxx]`159/`[E-xxx]`8 vs R3 다계열 138 상충 해소 — 패턴별 건수·파일) · **G-금지 게이트 실물 수**(`test_gates_v1025.py` 함수 수, N11) · 박스 환경 9종 카운트 + `\newtheorem*` 정의 목록(정리·정의·증명 환경 0 확정) · **마스터 tex 3본(`ch1_graphite_v1.0.24.tex`·`ch2_lco_v1.0.24.tex`·`ch3_si_v1.0.24.tex`) + 지원 4본(`ch1v22_partT_divider`·`ch1_preamble`·`ch2_preamble`·`common_preamble_v1024`) 전문 정독**(행 범위 기록 — §2.9 미정독 7본의 배정처이며 2.7 Read Coverage 에 계수; 판독은 grep·부분만 봤다). **orphan 라벨·서브라벨 검사**(W2-2 orphan 라벨·N6a/N6b 서브라벨 — R1 L-18·비평 #11).
- **Step 15 — 두 버전 diff·touch-up·명명 유산**: v1.0.25 vs v1.0.25.1 = `_sections` 3파일 + 마스터 3 + ARCHIVE_NOTE·PDF hash 대조 확정 · touch-up 4건 각각 행 범위·성격(산문 additive)·식/라벨 불변 판정(F1 `ch3v22_sec02b_sifr.tex`:40–44 / F3 :144–145 / M-w `ch1_sec05_width.tex`:303–304 / L-bg `ch1_sec06_eqpeak.tex`:107–108 — R4a §2.3·R4b §2 승계) · F1 이 들여온 `\texttt{…md}` 토큰 등재 · N5 `ARCHIVE_NOTE.md` 표제 확인 · **파일 접두·라벨·xr 키·자산 태그 승계표 시드**(R4b §8.3: `ch1_sec11~17`=Ch2·`ch2_sec*`=Part T·`ch2_app*`=부록 C/D·`ch1_appD` orphan·`sec:lco-code` 역사 명칭 G38·`ch1_appD` "D" vs 부록 D 명명 충돌 G28) · Ch1 의존 식 라벨 distinct Ch2 27/Ch3 18 표(R4b §1.4) 전사 · **v1.0.26A/B 자산 지도**(DR-1 = A+B 사용자 확정): `docs/v1.0.26A-regsol/`·`v1.0.26B-gallery/`(README·figures·params) + `results/comp_v26_data/`(스크립트 6본·out_versions·README) — 문건 tex 무변경 확인 후 판정·데이터 자산만 등재.

**게이트 2.1.** 카운트 표 = brief §4.2 전건 일치(정의 문서 첨부) · boxed 표 64행(지위 열 빈 셀 0) · 빌드 포함/미포함 60/60 · 자산 태그 계열 표(상충 해소 명시) · G-금지 실물 수 확정 · diff 파일 집합 = {3+3} + hash · 승계표 시드. **중단 조건.** 카운트 불일치 → 원인(정의·파일 집합) 규명 후 정본 확정(정지 아님). **다음 조건.** Step 14·15 이력 + 마스터 3본·지원 4본 정독 행 범위 + `PHASE_2.1_V1027_<topic>_RESULT.md`+`.json` + Ledger 행.

## Phase 2.2 — 유도 완결성 감사(기준 ①) (Steps 16–20)

**목적.** "수식만으로 80~90% 이해" 기준을 **boxed 64 각각의 (a)출발식 → (b)연산 → (c)중간식 ≥1 → (d)박스 사슬** 존재로 판정하고, 비약·누락·생략·논리 결함을 GAP-ID 로 등록한다. **시드 = R4a §2(Ch1 범위 41건 판정 + §2.1 비박스 8건 N1~N8 + §2.2 서식 표지 카운트) · R4b §3(23건 판정 + 박스 우선순위 역전 6) · §4(G01~G42)** — 전부 판독 작업 sub 의 판정이므로 이 Phase 는 **본 arc 작업 sub 의 전문 정독 + 판정 행 재작성 → 검수 sub refute → master 삼각검증** 의 3단으로 돈다(시드를 그대로 확정하지 않는다 — 검수 sub 만 돌리면 arc 안에서 전문 정독이 0 이 된다).

**청크(§2.6 정량 기준, 각 ≤~500줄 창·최대 ~700 — 실제 행 범위는 세부 계획서).** 총 9214줄 → 최소 19 청크(Step 17 = 7 · Step 18 = 5 · Step 19 = 7 — R4a §1·R4b §1.4 파일 줄수로 기계 산출; 나머지 332줄 = 마스터 3본 + 지원 4본은 2.1 Step 14 소관).

- **Step 16 — 판정 척도·GAP-ID 통일**: R4a 3단+N/A(있음/부분/없음) 와 R4b(완결/부분/비유도) 를 **4단 척도** = 완결 / 부분 / 없음 / 비유도(규약·도식·모델 가정·정정·옵션·진술 — 박스 해제 여부 열 동반, R4b DQ-8) 로 통일. **"없음" 하한**은 DR-22(기본값 = 엄격: (c) 중간식 0 이면 보강 대상 — R4a DQ-1 에 따르면 부분 16 중 12 가 추가로 떨어져 보강 대상 25→약 30). GAP-ID 이름공간 = `GAP-<기준>-<nnn>` 로 R4a #n·N1~N8·S1~S35, R4b G01~G42·A01~A30, R7 R-01~R-06 을 별칭 열로 흡수. Ch1 의존 대입형(R4b "닫힘 14 중 두 장만으로 따라올 수 있는 것 8")은 follow 열로 분리.
- **Step 17 — Ch1 곡선 사슬(sec00~sec10, 3,428줄 = R4a §1 파일 줄수 합 95+245+391+475+122+337+425+239+132+376+149+254+188, boxed 27 = N/A 1 포함)**: 작업 sub 가 청크 7(≤500) 전문 정독 후 R4a #1~#27 판정 행을 재작성 → 검수 sub 가 refute — 렌즈 = follow + 적대검산(부호·차원·극한). 특히 #10 eq:sm-nernst 중간식 0·#15 eq:xieq n_j 정의 삽입·#18 eq:skewpeak 연쇄율 생략·#19 라벨 부재·#24 eq:peakshape 한 줄 대수 부재·#26 eq:reversal 거울 유도 생략·#27 eq:sum 중간식 0·S7 접촉전위 "표준 처리"·S10 ΔC_p=0 암묵·S23 z_cut=4.357(수치 정합은 R4a 검산) 을 표적. master 삼각검증 후 확정.
- **Step 18 — Part T(ch2_sec00~10 1,487) + §18(93) + 부록 A/B/E(90+185+218) + Ch1 bib(57) = 2,130줄(R4a §1 합), boxed 14 = N/A 1 포함, 청크 5**: 작업 sub 전문 정독·판정 행 재작성 → 검수 sub 가 R4a #28~#41 refute — #30 eq:Sconfig(Part 0 위임)·#31 eq:Se-ch2(Sommerfeld 미유도)·#35 eq:hys_rev 선형화 서술·**#36 eq:qrev "없음"(Bernardi 원식 미기재)**·#37 eq:complete 한 줄 대수·#38 eq:sc-true 2χ_d 기원 미기재·#40 eq:sc-valid Δξ_supp≈L_V/(4w) 근거·#41 전달함수 1줄. 부록 E 는 P3 ⑤ 5항 존재 확인 + ②항 미완 GAP + dossier (e)-1~4 vs 부록 E ⑤(1)~(4) 대조(R6 S-2: (e)-2 stretched-tail 저온 열화가 부분 일치) 등재.
- **Step 19 — Ch2 LCO(본문 8절 1,455 + 서두·기호표·bib 47) + 부록 C/D(152) · Ch3(본문+기호표 1,026 + 서두·bib 56) + 독립 부록(497) + orphan(91) = 3,324줄(R4b §1.4), boxed 16 + 4 + 3, 청크 7**: 작업 sub 전문 정독·판정 행 재작성 → 검수 sub 가 R4b #1~#23·G01~G42 refute — 표적 = **자인되지 않은 논리 결함 3**(G11 sec16b R² 순환 논증 · G18 sifr 관측 폭 vs 평형 폭 층위 혼합[R4b 추정] · G04 sec13 Ω↔ECI 등치 선언) · 부분 2(G10 eq:lcoomega-kernel 중간식 · G23 eq:si-lcmu postulate — Λ_σ≈95–105 mV/GPa 어림은 R4b 산술[추정]) · 사다리 역전 2(G01 sec12 · G21 blend) · G05 F^×≈0 사후 정당화 · G06 n_j 일반형 단언 · G42 문건 내 재현 불가 예제. Ch1 결과식 xr 참조의 사슬 단절 지점(참조만 하고 유도를 건너뛰는 곳 — G02 artanh 위임 등) 별도 열. 독립 부록은 유일한 완전 "일반→특수" 사례(eq:app-fxi)·수치예 재계산 일치(R4b 검산)를 확정 기록. LCO 장 산문 비율(display 식 수 대 산문 줄수) 계측을 판정 행에 병기(R3 B-1 — 비평 #11).
- **Step 20 — 비박스 결과식·중복 유도·통합 GAP 표**: R4a N1~N8(eq:gr2l-fwhm·eq:skewapex·eq:widthbudget·eq:gibbsthomson·eq:Acut z_cut·eq:Svib_mode·Sommerfeld 적분·eq:dxidT) + R4b 박스 우선순위 역전 후보 6 항목 = 7 라벨(eq:lco-kirchhoff·eq:lco-SeV·eq:lco-U1V·eq:blend-dqdv·eq:si-vshift·eq:app-spinodal·eq:app-maxwell — R4b 는 eq:lco-SeV·eq:lco-U1V 를 한 항목으로 묶음) = **15 라벨(판정 행 단위 = 라벨; 항목 단위 14)** 을 판정 행으로 승격 · display 166(=230−64) 중 "결과식으로 쓰이나 박스 없는 식" 스크리닝(후보 등재 — 챕터 3.4 목표 boxed 승격 검토) · **Part 0↔Part T 중복 유도 4쌍**(eq:sm-logistic/eq:logistic·eq:mu/eq:Veq_BW·eq:sm-Smix/eq:Sconfig·eq:sm-thresh/eq:slope_BW, R4a DQ-2)·**다중 수록 3계열**(정칙용액 커널 3곳·Sommerfeld 2곳·spinodal 3곳, R4b §8.1)·**같은 곡률식 3절 독립 유도**(R5 §6-5) 등재 · 서식 표지 0 절 7 · 통합 GAP 표(기준 ① 몫).

**게이트 2.2.** boxed 64/64 판정 행(4단 척도·비유도 박스 해제 여부 열·follow 열) · 검수 sub refute 1R 이상 + master 삼각검증 기록 · 비약/누락/생략 목록 = GAP-ID·파일·행·성격{점프(D3)/중간식 부재/전제 미명시/차원·부호 검산 부재/참조 단절/출발식 postulate/논리 결함} · 비박스 15 판정 행(라벨 단위) · 작업 sub 정독 행 범위 = 본 Phase 배정 53본 전건(8,882줄) · 청크 창 ≤~500(최대 ~700) · 두 렌즈 각 1회 이상 · R4a·R4b 판정과의 차이(뒤집힌 행) 목록. **중단 조건.** 없음(발견은 GAP 이지 정지 아님). **다음 조건.** Step 16~20 이력 + `PHASE_2.2_V1027_<topic>_RESULT.md`+`.json` + Ledger 행.

## Phase 2.3 — 일반성·가정 사다리 감사(기준 ⑤) (Steps 21–23)

**목적.** 현행 문건이 **어디서 일반식을 특수식으로 간소화했는지**, 그 가정·유효범위·레퍼런스가 명시돼 있는지를 등록한다. 챕터 3.2 사다리 설계의 진단 입력. **시드 = R4a §3(S1~S35) · R4b §5(A01~A30) · R5 §2(사다리 23단 — 굵은 단 11 = 부재) · R6 §5(6 rung)**.

- **Step 21 — Ch1 간소화 지점 S1~S35 검수·보강**: 각 행 = 위치(파일·행·라벨)·간소화(일반→특수)·가정 문장 verbatim·유효범위 명시 여부·레퍼런스(V1 키)·tier·GAP. 검수 sub 는 R4a 집계(레퍼런스 × 17·유효범위 × 5·가정 미명시 2)를 refute 하고 누락 지점을 추가(예: 등온/점별 T(V)·C_bg 창-국소·전자항 토글·대정준↔정준 동등성·L_V 동결 — 직전 v1 초안 Step 17 의 후보 예).
- **Step 22 — Ch2·Ch3·부록 A01~A30 검수·보강**: "일반형 제시" 열(식 9·박스 1)·사다리 역전 2(G01·G21)·출발식 postulate 2(G08 logistic 게이트·G23 Larché–Cahn)·정직 분류 준수(A25·A27 4분류)·Ch1 이미 특수화된 식을 출발점으로 삼는 구조(기준 ⑤ 계보가 두 장 안에서 형성되지 않음, R4b §5 관찰) 확정.
- **Step 23 — "일반식 → 특수식" 계보도(65 노드)**: 등록부를 그래프/표로 재배열(뿌리 = 가장 일반적인 식, 잎 = 현행 boxed 64 + 비박스 핵심 14) + 각 간선에 가정 ID. **R5 §2 사다리 23단(L0·L1·L1′·L2a·L2b·L2c·L2d·L2e·L3a·L3b·L3c·L3d·L3e·L3f·L4·L5a·L5b·L5c·L6a·L6b·L6c·L6d·L7 — R5:79–103)·R6 §5 6 rung(L0~L5)** 과 대조해 현행 문건이 갖지 않은 단(굵은 단 11: L1·L2a·L2b·L2d·L2e·L3d·L3f·L6a·L6b·L6d·L7 + 동역학 L0·L1)을 "부재 단" 으로 명시. 레퍼런스 없는 간선·유효범위 없는 간선을 GAP 으로.

**게이트 2.3.** 등록부 65행 × 6열(위치/가정/유효범위/레퍼런스/tier/GAP) 빈 셀 0 · 계보도의 잎 = boxed 64 전건 포함(누락 0) · 부재 단 목록(R5·R6 대조 — 단 ID 집합 23 을 그대로 첨부) · 최우선 지점(S10·S16·S23·G04·G23) 판정 확정. **중단 조건.** 없음(발견은 GAP·정지 아님). **다음 조건.** Step 21~23 이력 + `PHASE_2.3_V1027_<topic>_RESULT.md`+`.json` + Ledger 행.

## Phase 2.4 — 서지 감사(기준 ③) (Steps 24–26)

**시드 = R7(95건 목록표 §2 + Crossref 84 대조 §1.3 + 원장 계보 §1.2 + 절별 밀도 §3[기계 스캔] + 체크리스트 §4[12주제 ~150행] + 규약 초안 §5 + json 부본) · R4a §4 · R4b §6.** 외부 접근은 DR-6 — 판독 단계에서 Crossref 조회가 이미 실행됐으므로(R7:7) 그 응답을 승계할지 재조회할지는 DR-6 응답에 따른다.

- **Step 24 — bibitem 95 검증표 확정**: R7 §2 표(키·서지·DOI·Crossref 판정·원장·인용 절) 승계 + 검수 sub 대조 → 각 항목 검증 방법(Crossref/원문/미검증)·결과·1차/2차 구분. **결함 R-01~R-06 GAP 등재**(`verbrugge2017` 제목 오류+`msmr_origin2017` 동일 DOI 이중 키 — 동결 base 무수정·v2 에서 키 1개로 통합 / `schmitt2022` C. Schmitt 4인 / `koebbing2024` 34(7) / `sethuraman_stresspot2010` A1253 / 관사 / et al. 4건) · bib 헤더 카운트 스테일 3건(G30) · `lee_sic2025` 권 공란 · `numverif2026` 내부 자료 참고문헌 등재의 처리(부록·각주 이관 후보, R4a DQ-4) · abstract tier 3건(occupation2019·chemmater2015·jpcc2021)·rsc2021 K-graphite 비교 인용.
- **Step 25 — 원장 체인 대조**: V1020(55줄)·V1021(38)·V1022(33)·V1023(33 = V1022 md5 사본) ↔ 현행 bib 93 키 전건 대조 — 미등재 6(`lee2017jcp`·`lee2011jcp`·`son2013jcp`·`schmitt2022`·`verbrugge2017`·`artrith2018`)·원장 only 4·부록 [A1]~[A5] 키화 후보(Cahn–Hilliard 1958 DOI 10.1063/1.1744102·Cahn 1961 10.1016/0001-6160(61)90182-1 Crossref 재확인 일치) · "V1 키만 인용" 규칙이 v1.0.23 부터 끊긴 사실 등재(R7 §1.2) · 3.5 원장 재개설 설계의 입력(DR-19).
- **Step 26 — 인용 밀도·1차 문헌 공백**: section 49 × cite 의 절별 밀도 표(R7 §3 기계 스캔을 **정독 기반**으로 재검증 — R7 은 본문 미정독) · 무인용 본문 절 4(§3·§6·§8·§9)·저밀도 3(§2b·§4·T4)·유도 절 교과서 인용 0(sec12·sec14·sec15 유도부·독립 부록) 확정 · 결과식 boxed 64 중 1차 문헌 인용 없는 식 목록 · **1차 문헌 공백 스크리닝**(R4a §4.3 15주제 · R4b §6.3 8계열 · R7 §4 체크리스트 X 48건[그중 38건 DOI 확인 완료] · R5 §5 (N) 32건 · R6 신규 서지 — 이론 원전 키워드 본문 0회 11종) → 체크리스트 자체 설계는 3.5, 여기서는 현행 95 대비 공백 표.

**게이트 2.4.** 95/95 행 · DOI 열 값 ∈ {검증 DOI / DOI 없음(서지 확인) / 미검증} · 결함 6 + 헤더 3 GAP 등재 · 원장 대조표(미등재 6·only 4·사본 1) · 절별 밀도 49행(정독 기반 표시) · 공백 목록(주제별·후보 DOI 확인 여부 열). **중단 조건.** 없음(DR-6 불허 시 "미검증" 표기·정지 아님). **다음 조건.** Step 24~26 이력 + `PHASE_2.4_V1027_<topic>_RESULT.md`+`.json` + Ledger 행.

## Phase 2.5 — 형식·register 감사(기준 ②④) (Steps 27–29)

**시드 = R4a §5(형식 요소·F-11 4건·F-04 13줄+어휘·F-10 0~1) · R4b §7(§3.5 3중 불일치·토큰 잔존·헌법 ① 잔존 G13/G33/G34/G38·용어·형식 요소 표).**

- **Step 27 — 교재 형식 요소 체크표**: 절별(49 section·115 subsection)로 정의·정리(명제)·유도 (a)~(d) 표지·예제·요약(keybox)·기호표·다리(도입/마무리)·검산 박스·원전 다리(srcbox)·정직 한계(warnbox) 존재 O/X. 확정 시드 = 정의·정리·증명 환경 0(`\newtheorem*` 은 박스용)·예제 2+부록 1·연습 0·keybox 없는 절 6·서식 표지 0 절 7·Ch2 "정의·요약" 층 얇음·Ch3 "유도·예제" 층 얇음·독립 부록이 가장 교재형(R4b §7.5). **F-01 §1.1.4 재판정** — (a)(b) 점별 닫힘 원칙·두 전위 keybox = load-bearing / (c)(d) 측정 원리 배경·원전 다리 = 배경 으로 분리 판정하고 v1.0.27 에서의 처리(유지/부록 강등/축약)를 GAP 으로 등재(R3 A-4:85·D21-2 연동 R3 A-6:126 — 비평 #4). 아울러 폭 폴백 지위 서술(R1 L-14)·`tab:notation` N3 재배열(R1 L-15)을 register 항목으로 등재(비평 #11).
- **Step 28 — F-04/F-10/F-11 + 헌법 ① 잔존 grep(토큰 정의 확정 후)**: **코드 토큰 정의 확정**(DR-14: `\code{`·`\texttt{`·`func_`·`solve_U_oc`·`_regsol`·`regsol2`·`regsol_si`·클래스명·파일명 `.md/.py` 포함 여부 · 판정 단위 = 조립상 부록 아닌 절) → 비부록 `_sections/*.tex` 카운트(현행 3~7 → 확정값) · §3.5 3중 불일치(파일명·라벨 `sec:si-code`·본문 참조 6곳) · `ch2_appA_traps.tex`:67–68 라벨명을 `\code{}` 로 감싼 용법 오류(경미) · F-10 = 요동/양성/유일근 카운트(본문 0·독립 부록 "요동" 13) + 음함수/섭동/준위 첫 출현 병기 + 정준/대정준 카운트만 + regular solution 역어 이원화·원어 병기 0 · F-04 = 버전 태그 본문(Ch1 13줄·Ch3 12곳)·프로세스 어휘(opt-in 8·round-trip 14·bit-exact 2·골든 1·G-SI 1·@2/@5 5)·검수 ID "#7" 5회·고백조 6("우리 진단"·"회사가 검산 가능")·tier 표기 21건(정직성 규약 — 교재 register 양립은 DR-21)·`ch1_sec05b_gr2L.tex`:1–12 헤더 주석 잔존 → 수치.
- **Step 29 — 타전공 석박사 가독성 판정(정성 → 항목 분해)**: 각 절 (i) 전제 개념 선행 도입 (ii) 기호 첫 등장 정의(`tab:notation`·`ch2v22_notation`·`tab:si-notation` 대조 — h_{η,j} 누락 G03·U_oc 소스 이원화·`\cat`/`\config` 매크로 혼용 G36) (iii) 두문자어 첫 출현 병기(미전개 11종 DFT·NMR·XRD·INS·SEI·XPS·CMC·SBR·FEC·AIC/BIC·η_ICE·pOCV/p-ocvhold·SOC/SoC/SoH 혼용 — Ch1 전개 여부 확인) (iv) 절 도입/마무리 다리 (v) 극한·코너·tier 표기 (vi) 전방 참조 밀도(R4a §5.1 추정 — sec01:31–35 등) (vii) 오독 유발 문장(G37 서두 σ_d "부호 반대")·시연 세트 명명 충돌(G16) — 7항목 O/X 표.

**게이트 2.5.** 체크표 49(+115)행(= T-20 진단판) · grep 수치 3종 + 헌법 ① 4종 첨부(토큰 정의 문서 동반) · **F-02/F-03 노테이션 grep(확률 P 대문자 0 — 압력 P 수동 제외 · 총량 F/S 대문자 vs 자리당 f_int/s_int 소문자)** · 가독성 7항목 표 빈 셀 0(= T-21 진단판) · 용어 결정 필요 항목 목록(DR-20). **중단 조건.** 없음. **다음 조건.** Step 27~29 이력 + `PHASE_2.5_V1027_<topic>_RESULT.md`+`.json` + Ledger 행.

## Phase 2.6 — v1.0.26 regsol 미결의 설계 입력화 (Steps 30–31)

**목적.** "두-상 커널 문제"를 **결정하지 않고** 판정 기준·필요 데이터·현 근거를 정식화해 챕터 3.1(후보 평가)·3.2(사다리)·3.7 DG-B 의 입력으로 넘긴다. **시드 = R2 §2.10·§4(R-1~R-4)·DQ-5 · R5 TH-2.1·DQ-2 · R6 H-2·DQ-4·DQ-12 · R4a §7(sec05b:85–92 regsol2 Ω_j/RT=[4.06,2.02,3.55,4.07]·경계값 2.02 민감·sec07:12–26 두-상 지목 근거 = 실측 plateau·appB:20–23 커널 삭제 기록) · R4b DQ-4·DQ-9.**

- **Step 30 — 판정 상충표·지위·층위**: (a) **네 판정 상충표**(R2 DQ-5) — v1.0.24 @3 채택(Si 0.9944, 블렌드 0.9848 / 전이 흑연4+Si3 / p-OCV 단일 프로토콜) → v1.0.25 @3 역전(+0.97→−0.53%p / 전이 승격 흑연7+Si7 / R²·피크역 RMSE) → v1.0.26 HANDOVER "@3 +0.67%p 유일 실효"(별개 ablation·블렌드 p-OCV) → v1.0.26 A/B(regsol-4 흑연 R² 0.91506·BIC 2609.6·면적 결손 +12.05% vs logistic-7 0.97389·BIC 1765.1 / 스윕 N=3~8 / skew-logistic-7 BIC 991.5 최선 / BDD 99_Backend 방식 dQ/dV) — 조건(전이 수·프로토콜·소재·지표 R²/BIC/피크·벨리 RMSE/면적 보존)을 열로 분리 (b) **LCO Ω 커널(eq:lcoomega-kernel) 지위 확인** — v1.0.25 삭제 대상 커널인지(sec16b 에는 sifr 와 달리 지위 warnbox 없음 G12) 코드 대조는 Non-goal 이라 문건·인계 기록으로 판정, 불가 시 "미검증" (c) **관측 폭 vs 평형 폭 층위 분리**(R4b DQ-9 G18) 를 판정 기준 항목으로 등재 (d) 흑연 0.104 V 피크 FWHM ≲1 mV(RT/F 의 1/25) 정체(두-상 vs 비평형 인공물, R2:R-2) (e) v1.0.26 `regsol_kernel.py`(혼화갭 닫힌형 + 밀도⊛FFT 합성곱 = 정칙용액+Maxwell 구현)를 TH-2.1 평가의 **선행 데이터**로 등재 (f) N4 흑연 두-상 4 vs 2 표기(Dahn 1991 본문 확인 → 2.4 서지와 연동).
- **Step 31 — 정식화 문서 (i)~(v)**: 세 후보 커널(정칙용액+Maxwell 공존 / 로지스틱 gallery 세분 / skew-regsol 결합) + skew-logistic(v1.0.26 최선) 에 대해 — (i) 현 근거: LIT §6(R² 0.943 vs 0.938·Ω_j/RT 전부 >2RT·Cordoba DFT ~2.5RT 앵커·"가치 = 파라미터 물리성")·`HANDOVER_v25.md`:85–89·IMPROVEMENT #4(near-delta 천장 R²≈0.96 — R2 §2.6·R3 B-4; v2 의 "0.95–0.96" 은 원천에 없는 표기)·v1.0.26 A/B 수치(원천 path+line) (ii) 판정 기준: 개형 지표(R² + 피크역 RMSE + 벨리역 RMSE + BIC + 면적 보존)·파라미터 물리성(Ω 해석 가능·DFT 앵커·탐색 경계 부착 여부)·XRD 상 수 불변(gallery ≠ 상)·다중셀 n>1·관측/평형 폭 층위 (iii) 필요 데이터: GITT/p-OCV+hold 평형(SINTEF Zenodo 20086298 기확보 CSV 재사용 / 신규 다운로드 `dl_sintef.ps1` = DR-6) (iv) 실행 경로: `test_skew_regsol_v2.py`·`test_gallery_vs_regsol.py`(폐기분 `test_skew_regsol.py` 아님) — 기확보 CSV 위 재실행은 Non-goals 의 "기존 확보 데이터 재사용 허용" 안이므로 **2.6 세부 계획서의 nonblocking 구현 선택**(DR-6 과 무관·코드 무수정); 신규 다운로드(GITT/p-OCV+hold)만 DR-6 (iii) (v) **커널 단위 기본값 = 상 전이 4**(R6 DQ-12 제안), 소재별 갈림(흑연 두-상 / Si 연속 고용체[Frumkin] / 블렌드 중첩), DR-1 해석과 무관하게 흡수됨을 명시, **DG-1(코드 삭제)과 문건 이론 채택은 별개**임을 명시(R3 DQ-7·DR-10).

**게이트 2.6.** 상충표 4행 × 조건 열 빈 셀 0 · 정식화 문서 (i)~(v) 전항 · 수치는 원천 path+line 인용(새 수치 생성 0) · 판정 기준 ≥5 항목 · 커널 단위 기본값 명기. **중단 조건.** 없음(판정 상충은 표로 분리·정지 아님). **다음 조건.** Step 30·31 이력 + `PHASE_2.6_V1027_<topic>_RESULT.md`+`.json` + Ledger 행.

## Phase 2.7 — Result: GAP REGISTER (Step 32)

- **Step 32**: OUT-GAP `V1027_GAP_REGISTER.md`(+`.json`) = 2.1~2.6 산출 통합 · 각 GAP = GAP-ID·기준(①~⑤)·위치·성격·4-tier·별칭(R4a/R4b/R7 원 ID)·챕터 3 인계 여부·v2 처리 후보(저작 4.x 배치) · 챕터 통합 Result `PHASE_2_V1027_GAP_RESULT.md`+`.json`(2.1~2.6 Phase Result 위) · Ledger 행 2.1~2.7 · Phase audit(문서 렌즈셋 6종) 3-Pass · 검수 sub 청크 검수 ≥1R + 연속 2R 수렴(GAP REGISTER = 통상 등급 — DR-23).
- **게이트 2.7.** GAP 전건 4-tier 라벨 · Read Coverage(**본 arc Read 만 계수** — 2.1 Step 14 마스터 3본+지원 4본(332줄) + 2.2 Step 17~19 53본(8,882줄) = v1.0.25.1 9214줄 전 영역 cover; 판독 R4a/R4b 커버리지는 참조 열) · **v1.0.25 커버리지 = v1.0.25.1 전 영역 + diff hunk 4건 정독**(`ch3v22_sec02b_sifr.tex`:40–44·:144–145 / `ch1_sec05_width.tex`:303–304 / `ch1_sec06_eqpeak.tex`:107–108 — brief:33 "1.0.25 두 가지 버전을 검토" 의 감사 가능 게이트) · md+json 쌍 · R4a DQ 10·R4b DQ 10·R7 DQ 15 각각 "해소/이관/미해소". **중단 조건.** 없음. **다음 조건.** Result 없이 챕터 3 진입 금지.

---

## Phase 3.1 — 후보 이론 조사·평가 (Steps 33–37) ★핵심

**목적.** 열역학·통계역학·동역학·히스테리시스·열의 다섯 축(+구조·형식 축)에서 **진보 후보를 카탈로그화**하되, 기존 서베이(B1~B5)와 판독 카탈로그(R5·R6)를 전건 흡수해 재조사 0·기각군 승계로 시작한다. **시드 = R5(TH-1.1~9.3: A 6·B 10·C 11·D 12) · R6(K/E/T/R/S/H/Q: A 7·B 10·C 7·D 20항) · R7 §4(주제별 후보 DOI 74건 확인) · R3 B(재개방 후보 판정)**. 등급은 R5·R6 의 판정이며 본 Phase 는 검수 sub refute·master 삼각검증을 거쳐 등급을 **재판정**한다.

**축과 시드(brief §5 3.1 승계 + 판독 명단).**
- 열역학: lattice gas 일반 Hamiltonian(TH-1.1) → 정칙용액(regular solution) → Ω(ξ)/Redlich–Kister(TH-3.1) → sublattice/staging(TH-4.1·4.2·4.3) → Cahn–Hilliard/phase-field(TH-5.1·5.2).
- 통계역학: 대정준(grand canonical)·요동-응답 SM2-A/B/C(집행 확정·승계)·일반 요동 항등(TH-1.2)·Maxwell 관계 2계(TH-6.3)·transfer matrix staging(TH-4.3)·준화학/CVM(TH-2.2).
- 동역학: Eyring/TST 척추(K-1)·투과계수(K-2)·Butler–Volmer 일반화(E-1)·Marcus(E-2, C)·Nernst–Planck 농도 분극(E-3)·Onsager 선형 비가역 열역학(R6:T-1·R6:T-2)·master equation/Fokker–Planck(R-1)·KWW/장벽분포(R-2)·Watson 전개(R-3)·확산 제한(R-4)·Fredholm ratio·부록 E 3층(S-1)·refs 6/7(S-2)·dependency graph(S-5).
- 히스테리시스: spinodal·CNT(H-1·H-2·TH-5.2)·Preisach(H-3 명명 노트만)·cusp(H-4)·Si 분리 branch(H-5).
- 열: entropy production(R6:T-1)·Bernardi(Q-1·Q-2·Q-3·TH-7.4)·엔트로피 분해(TH-7.1·7.2·7.3)·Kirchhoff 일반 U(T)(TH-7.5).
- 구조·형식: 일반→특수 대조표(TH-9.1)·기호 통합표(TH-9.2)·tier 규약(TH-9.3).

**승계 표(재조사 0 의 기준 — OUT-REG3 확정 상태 + R5 §1·R6 §6).** 집행 완료군(재제안 금지): SM2-A/B/C·SM2 축 D·DIRECTION (i)~(iv)·ROADMAP 제안 1·제안 5(부분)·IMPROVEMENT #1 gallery opt-in·#2 α opt-in(단 함수형이 원 제안 양측 폭과 다름 — R5 DQ-9)·LIT G4·L1·L2·SURV Tier1 Fredholm ratio+전달함수·Tier3 cusp(각주)·SM2 (v) 부분 해소. 기각군(승계·재조사 X): R5 §1.2 12건·R6 §6 20항(§Non-goals 열거). 미집행·보류·선검증군(평가 대상): ROADMAP 제안 2·3·4 · IMPROVEMENT #3(조건부)·#4 · LIT ◐군 G3·G5·L4~L6·S4·S5·M1·M4 + ★군 미반영분(1.2 확정) · SURV Tier2 Fisher·정합점근/Watson·Tier3 명명 노트 · SM2 축 B(재판정)·축 C(조건부)·flow-1/3 · FABLE 명시 결정 5건(Eyring·§1.18·S0–S5·KWW·자기완결) · 문건 자체 후보 2건(Einstein 경화형·두-θ 차분형 / ∂Ω/∂T).

- **Step 33 — 승계 표 확정**: OUT-REG3 등록부 + R5 §1.1~1.3 + R6 §6 대조 → 후보 항목 = ID·축·출처(B1~B5/A9/R5/R6/문건 자체)·기존 등급·현행 상태(파일:행)·본 계획 지위{개방/기각 승계/완료 승계/재판정}. 재판정 항목 = SM2 축 B(R3 DQ-16·R5 DQ-8)·Preisach(명명 한정, R3 DQ-15)·[C-92]·[MODEL-1] KWW(1.3 분류 결과에 따라).
- **Step 34 — R5·R6 통합 카탈로그 + 경계 정리**: 두 카탈로그의 이름공간(TH-x / K·E·T·R·S·H·Q-x)을 유지하며 **경계 정리**(R5 DQ-11: 열역학 축 = ΔG*(ξ)·Maxwell·binodal 함수형, 동역학 축 = 이탈 시점(율속)·L_V 합성; TH-5.2 ↔ H-1, TH-2.1 (iv) ↔ H-2 (e), TH-7.4 ↔ R6:T-1/Q-1/Q-2 중복 계상 해소) · **A 등급 명단(R5·R6 판정)** = TH-1.1 일반 격자기체 Hamiltonian 정점 · TH-2.1 정칙용액+Maxwell 두-상 dQ/dV 사슬 · TH-3.1 Redlich–Kister → α_j 승격 · TH-5.1 상분리 부록 본문 승격 · TH-9.1 일반→특수 대조표 · TH-9.2 기호 통합표 · K-1 Eyring/TST 척추 재배열 · R6:T-1 entropy production 일반 상태식 · S-1 부록 E 3층 승계 · S-2 refs 6/7 5항 완결 · S-5 dependency graph·4분류 표 · H-2 정칙용액→로지스틱 rung(극한 회수 A / 커널 채택 조건부) · Q-1 Q̇_irr 분해(옴·지연·분기) — 13건 · **B 등급 명단** = TH-1.2 감수율 일반형·판정자·LCO 커널 통일 · TH-2.4 Frumkin 계보 서지 · TH-4.1 다중 부분격자 staging 일반식 · TH-4.2 Daumas–Hérold/Safran 배경 · TH-5.2 CNT/CH → γ_j 함수형 · TH-6.3 Maxwell 관계 2계 · TH-7.1 세 분포 분리 가정 · TH-7.2 포논 DOS 일반 → Einstein/Debye · TH-7.4 일반 엔트로피 수지 → Bernardi → 소산 · TH-7.5 Kirchhoff 일반 U(T) · E-1 조성 의존 교환전류 ↔ κ(ξ) 통일 · E-3 농도 분극(NP·Warburg·Nernst shift) · R6:T-2 선형 flux–force 회수창(회수 없는 노드·warnbox 필수) · R-1 master equation → OU·Kramers · R-2 KWW/장벽분포 커널 · R-3 Watson 전개·큐뮬런트 · R-4 확산 제한 완화 · H-1 γ_j 예측식(CNT/CH) · H-5 Si 분리 branch · Q-2 히스 소산 entropy production — 20건 · C 18건·D 승계 전량. 모델 차원 증가·데이터 입력 의존 후보 = TH-3.1 L_1(α 대체 시 0)·E-1(+1 조건부)·E-3(+1~2)·R-2(+1)·R-4(+1)·**H-1(γ_j 예측식 — 계면 에너지·시도 빈도 입력, −1~+1; R6 §7)**·H-5(+1/Si)·TH-2.3(+1)·TH-7.2(+1 opt-in) — "율속·상분리·다온도 데이터 패키지" 로 묶어 DG-B 일괄(R6 §7 제안).
- **Step 35 — 신규 문헌 검색(축별, DR-6)**: R7 §4 체크리스트 X 48건(DOI 확인 38·서적 10)·R5 §5 (N) 32건·(S) 7건·R6 미검증 서지(de Groot–Mazur·Prigogine·Onsager 1931·de Donder·Kramers 1940·Kohlrausch/Williams–Watts·Marcus/Chidsey·Warburg) 를 통합 후보 서지 표로 → DR-6 허용 시 Crossref 5-필드 대조(R7 규약 4) · 불허 시 "신규 검색 미수행·DOI 미검증" 정직 표기. Verbrugge–Koch 2003 후보 DOI 오해소·Daumas–Hérold 1969 실물 미확보(R7 DQ-7·14) 처리. 서지는 DOI/원문 링크 확인된 것만 등재(기억 서지 0).
- **Step 36 — 평가**: 각 후보 = 등급(A/B/C/D; R5·R6 판정 → 검수 refute → master 재판정) · 모델 차원(신규 파라미터 수) · 침습도(낮/중/높; Part 0 코어/N-노드/부록→본문 승격) · 서지(V1/S/N + DOI 상태) · 선행 데이터 자기완결 여부(v1.0.26 실측·SINTEF·회사 데이터 의존) · 기준 1~5 기여 · 회수 조건(기존 boxed 로 환원되는 극한) · 재검산 대상 표시(R5 §6 추정: TH-2.1 (v) 델타 무게 (T_c−T)^{1/2} 연속 소멸 vs §5b "불연속 갈아탐" 양립·TH-3.1 3차식·TH-7.2 Debye 닫힌 꼴 — SymPy).
- **Step 37 — 축별 정리**: 다섯 축 + 구조축 각각 "일반식 후보 → 현행 특수식" 대응 예비표(3.2 입력) + 권고 저작 순서(R5: TH-9.2 → 1.1 → 5.1 → 1.2 → 2.1 → 3.1 → 9.1 — 의존 사슬 / R6: A 7건 골격 + 차원 0 B 기본 채택 후보 R6:T-2·R6:R-1·R6:R-3·R6:Q-2) 통합안.

**게이트 3.1.** 카탈로그 = 승계 표 항목 전건 포함(누락 0) + R5·R6 후보 전건(A 13·B 20·C 18) 재판정 열 + 신규 항목 서지 DOI/링크 · 평가 열 8 빈 셀 0 · 기각군 재조사 0(기각군에 재평가 행 없음) · 경계 정리 표(중복 계상 0) · 데이터 의존 패키지 목록(H-1 포함). **중단 조건.** 없음. **다음 조건.** Step 33~37 이력 + `PHASE_3.1_V1027_<topic>_RESULT.md`+`.json` + Ledger 행.

## Phase 3.2 — 통합 골격 설계: "일반 → 특수" 사다리 (Steps 38–41)

**목적.** 사용자 기준 5 의 핵심. **가장 일반적인 식에서 출발해 가정을 하나씩 얹어 현행 boxed 식으로 내려오는 사다리**를 설계하고, 각 단(rung)에 가정·레퍼런스·회수 조건을 붙인다. 기존 boxed 64 가 사다리 어느 단에서 회수되는지 매핑해 자산 무유실을 설계 단계에서 보장한다. **시드 = R5 §2(L0~L7 23단·굵은 단 11) · R6 §5(L0~L5 6 rung·정직 조건 4) · 2.3 계보도.**

- **Step 38 — 열역학·통계역학 사다리**: R5 §2 를 정본화 — L0 공준 → **L1 일반 격자기체 Hamiltonian(cluster expansion·ECI, Ising 동치)** → L1′ 내부 자유도 → **L2a 다중 부분격자 평균장(J_⊥)** / **L2b 준화학·CVM** / L2c Bragg–Williams 정칙용액 / **L2d Redlich–Kister 비정칙** / **L2e Ω(T)** → L3a 전기화학 결선 → L3b 단상 등온선(같은 곡률식 세 곳 통일) → L3c Ω→0 로지스틱 → **L3d 두-상(Ω>2RT) 평형 dQ/dV(볼록 포락 → Maxwell 델타 + 단상 꼬리)** → L3e spinodal·gap → **L3f 핵생성 이탈 → γ_j** → L4 Cahn–Hilliard → L5 요동 항등(일반형·앙상블 동등성·켤레·2계 Maxwell 관계) → **L6 일반 엔트로피 분해·포논 DOS·전자·Kirchhoff U(T)** → **L7 일반 엔트로피 수지**. 각 단 = 일반식·가정(레퍼런스 키)·회수되는 현행 식(라벨·행)·신규/승계 표시. Ω 정의식 통일(부록 vs 본문, R5 DQ-10)·부록 ξ↔θ 배향(R5 DQ-4) 규칙.
- **Step 39 — 동역학 사다리**: R6 §5 정본화 — **L0 일반 비평형 상태식(국소 Gibbs·엔트로피 수지 σ=ΣJX≥0)** → **L1 준평형(Marcelin–de Donder J=k⁺(1−e^{−𝒜/RT}), 𝒜→0)** → L2 평형(정칙용액→로지스틱; 두-상 커널은 2.6 종속) → L3 TST 일반(K-1 재배열: eq:tst-rate → eq:bv → eq:db → eq:kuniv → eq:tst-box → 세 인자의 자리 → L_q·L_V·동결) → L4 lag(R-1 master equation 극한·R-2/R-4 옵션) → L5 동결(부록 E 3층 S-1·eq:sc-valid) + 교차(정지점·분포 관점). **정직 조건 4 명기**: 선형 flux–force 는 회수 없는 노드(𝒜_cut=4RT — R6:T-2 warnbox 필수) / 두-상 커널은 2.6 판정 없이는 극한 회수까지만 / L4 옵션은 각 +1 차원·부록 E rank-1 등가 상실 위험 / 등온-per-curve 유지(Q-4 D). E-1 채택 시 κ(ξ) 출발식을 일반 BV 에 접속. Marcus 는 상단 일반형 소개 + BV 회수 조건 + 채택 안 함(R6 DQ-10).
- **Step 40 — 열·히스테리시스 사다리**: 열 = L7 σ → Bernardi 일반 수지 → Rao–Newman 삽입 전극 → 단일활물질 eq:qrev(가역) + **Q-1 비가역 분해(옴 I²R_n·지연 η_kin·분기 소산)** + Q-2 히스 소산(완전 cycle 한정, [C-92] 재설정 DR-18) → 엔트로피 세 분포(TH-7.1 분리 가정) → Einstein/Debye/FD 코너 → CLOSING Part 4 (4) n(T)↔config 규칙. 히스 = spinodal 상한(γ_j=1) ← CNT 이탈(γ_j<1, TH-5.2/H-1 함수형) ← CH 성장률 / Dreyer 다입자 plateau / Si Larché–Cahn 가역 결합 → 분리 branch(H-5) / Preisach 명명 노트(C) / cusp 3/2 각주(C). 회수 조건 포함.
- **Step 41 — 자산 회수 매핑표**: boxed 64 각각 → 사다리 단(축·단 번호)·회수 조건·신규/승계/회수 표시 + 비박스 핵심식 15 + 중복 유도 4쌍·다중 수록 3계열의 **통합안**(정본 1곳 원칙·나머지는 alias 라벨 또는 대입형 참조 — 자산 무유실과의 정합은 3.4 라벨 alias 정책). 회수되지 않는 boxed 가 있으면 "설계 GAP" 으로 등재. 부재 단 11+2 에 대응하는 신규 절 목록.

**게이트 3.2.** 사다리 3축 각 단 = 가정·레퍼런스·회수 조건 3열 빈 셀 0 · 부재 단 전건 신규 절 대응 · 정직 조건 4 명기 · 매핑표 64/64 + 15 · 회수 불가 항목 0(또는 설계 GAP 명시) · 통합안 3계열. **중단 조건.** 없음. **다음 조건.** Step 38~41 이력 + `PHASE_3.2_V1027_<topic>_RESULT.md`+`.json` + Ledger 행.

## Phase 3.3 — 문건 구조 설계: 확정 구조의 내부 배열안 (Steps 42–43)

**목적.** 사용자가 확정한 구조(재료별 3장 유지 · 분리 빌드+xr · Ch1 흑연 = 이론 집중 · **통계역학 전체 = Ch1 후반부 부록(교과서급)** · Ch2/Ch3 = Ch1 에 없는 분기) 안에서 **내부 배열안**을 만든다 — 구조 자체는 결정하지 않는다(DR-3·DR-11·DR-12·신규 요구). **시드 = R6 §2(원구상 ↔ 현행 ↔ 작업 챕터 4 대응) · R4b §8(다중 수록 3계열·orphan·명명 유산·sec16b 접합부) · R3 A-6 · R5 TH-5.1(부록 승격) · 현행 Part 0 sec02a/02b·Part T 미시 유도부(부록 D 이전 원천).**

- **Step 42 — Ch1 내부 배열안**: (i) **본문/부록 분할 규칙** — 본문 = 거시 열역학·동역학 유도(중심·폭·상분리·regular solution→logistic·Eyring/TST 척추·lag·tail·히스·열특성 결과) / **후반 부록 D = 통계역학 전체**(앙상블·분배함수·격자기체 Hamiltonian·평균장/준화학·요동-응답(감수율·앙상블 동등성·켤레 쌍)·엔트로피 미시 분해(config·vib·electronic)·Einstein/Debye·FD/BE·Sommerfeld·Maxwell 관계 — 현행 Part 0 sec02a/02b + Part T 의 미시 유도부 + SM2-A/B/C 전부 이전) — 부록은 교과서 수준으로 **더 길고 상세하게**(전제 개념 선행 도입·중간식 전부·본문 회수 표 — **독자 참여형 섹션 X** — 비전공자·타전공 석박사 가독) 재편하고 본문은 그 결과식을 전방 참조로 쓴다 (ii) 현행 `_sections` 56 + 독립 부록 1 = 57 파일의 **이동 맵**(Ch1 본문 절 / 부록 D / 기타 부록 / 문건 밖 코드 문건 / Ch2·Ch3 분기) (iii) 상분리 독립 부록 **편입**(DR-11 master 판단: 본문 상분리 절 = 결과·binodal·spinodal·Maxwell·CNT, 유도 = 부록; ξ↔θ 배향·Ω 정의식 통일) (iv) 코드 절·코드맵(`ch1_appB_codemap`·`ch2_appB_codemap`·`ch3v22_sec05_code`·부록 E 대응 지도) **문건 밖 이전**(DR-14) (v) 3.2 사다리 각 단이 본문·부록 D 어디에 앉는지 좌표 (vi) 페이지 추정(부록 확장분 포함, "추정" 표기).
- **Step 43 — Ch2·Ch3 분기안 + 빌드 설계**: Ch2 LCO·Ch3 Si·블렌드는 **Ch1 에 없는 것만**(LCO: σ_d 재배선·order-disorder·전자 엔트로피 항·Ω 커널 지위 / Si: 연속 고용체(Frumkin)·c-Li15Si4 두-상·분리 branch·블렌드 중첩·유효경계·GS-1/GS-2) — 각 절이 Ch1 의 어느 결과식을 xr 로 받는지 대응표 · **음극(흑연·Si) 예측 강화**를 우선 축으로 Si 장 이론 보강 목록(R5 S-계열·R6 H-5·GS-1/GS-2 해소 후보) · 분리 빌드+xr 유지(DR-12: ch1→ch2→ch3→ch1 재패스, 병합 빌드는 완성 후 옵션) · 파일 접두·라벨·xr 키 승계표(현행 접두 반전 해소 여부) · 배열안 문서(Ch1 배열·부록 D 목차·Ch2/Ch3 분기·이동 맵·빌드) → 3.7 보고.

**게이트 3.3.** Ch1 배열안(본문/부록 분할 규칙·부록 D 목차·상분리 편입 절·코드 이전 목록) · 자산 이동 맵 **57/57**(`_sections` 56[orphan 포함] + 독립 부록 1; 파일 집합은 T-15 출력에서 기계 생성) · Ch2/Ch3 분기표(Ch1 결과식 xr 대응 열 빈 셀 0) · 승계표 · 분리 빌드 순서·xr 키 설계 · 페이지 추정. **중단 조건.** 없음. **다음 조건.** Step 42·43 이력 + `PHASE_3.3_V1027_<topic>_RESULT.md`+`.json` + Ledger 행.

## Phase 3.4 — 수식 사슬 원형(derivation skeleton) (Steps 44–46)

- **Step 44**: 새 구조(3.3 배열안 기준 — 본문/부록 D 좌표 포함) 절별 **목표 boxed 식** 목록 + 각각 (a)출발식 (b)연산 (c)중간식 (d)박스 사슬 **계획**(실제 유도는 챕터 4) · 현행 보강 대상(2.2 부분·없음 + 비박스 14)의 보강 계획 · 부재 단 신규 절의 목표 boxed.
- **Step 45**: 각 목표 식 = 신규(카탈로그 키) / 승계(현행 boxed ID) / 회수(사다리 단) 표시 · **라벨 alias 정책**(중복 유도 통합 시 한쪽 라벨을 alias 로 보존 — 자산 무유실 원칙과 "비약 없는 단일 사슬" 의 충돌 해소, R4a DQ-2) · 자산 태그 3분류(승계/회수/신규) 설계(R3 A-7 판단) · 부록 승격 시 기호 전면 치환 여부(R5 DQ-4 기본값 = 전면 치환·TH-9.2 표 선행) · orphan `ch1_appD_si` 이동 기록 + [V21-Q7-01~05] 승계표(R4b DQ-3).
- **Step 46 — P3 #3·#4 (S-5)**: 순환 의존 dependency graph(ξ_j·Q_bg·dQ/dV·dV/dQ·U_oc·L_V(ξ)·V_n) 1본 + 4분류 표(정의상 implicit / 수치해법 필요 / 논리 공백 / 물리 가정 충돌) — 분류 재료 = 부록 E warnbox(전하보존 반전·배경 = 대수 근, 유일성 = 요동 양성)·지연 = 비선형 Volterra·`eq:implicit`·SURV1 3종 적분방정식 대조·SURV3 "두 '역'"·sec17 고정점·blend 음함수·GS-1/GS-2 를 새 구조에서 재표시(R6 S-5 확정 재료).

**게이트 3.4.** 목표 boxed 목록(현행 64 + 신규 ≥ 부재 단 수) · 사슬 계획 4열 + **목표 boxed 별 사다리 좌표(축·단 ID)·가정 ID·레퍼런스 V1 키 열 빈 셀 0(T-19 계획판 — 기준 5 의 저작 게이트를 저작 전에 고정)** · 신규/승계/회수 표시 100% · alias 정책 문서 · dependency graph 1본 + 4분류 표(행 = 순환, 열 = 관여 식·변수·종·분류·해법·유일성 근거). **중단 조건.** 없음. **다음 조건.** Step 44~46 이력 + `PHASE_3.4_V1027_<topic>_RESULT.md`+`.json` + Ledger 행.

## Phase 3.5 — 레퍼런스 마스터 원장 설계 (Steps 47–48)

- **Step 47 — 원장 재개설 설계 + 인용 규약 확정**: R7 §5 10조항(단일 원장·단일 진실 + json / V1 키만 + 빌드 게이트 / 기억 서지 금지의 조작적 정의 / Crossref 5-필드 대조 절차 + `refcheck/` 응답 보존 + 서적은 출판사·WorldCat / 저자 전원 명기 / 한 문헌 한 키 + 별칭 표 / 1차 문헌 우선·tier 병기 / 절별 인용 하한 / bib 는 원장에서 생성 / 언어·표기·[A#] 폐지)을 검수 sub 대조 후 확정(DR-19) · v1.0.20~v1.0.25.1 전건 소급 전사 설계(V1023 사본·미등재 6·only 4 해소, R7 DQ-2·3) · 도구 확장 후보("cite 키 ⊆ 원장 V1" 검사 — `tools_tex_strict_check.py` 실물 미정독[R7 추정]) · 장별 bib vs 통합 bib 는 DG-A 종속(R7 DQ-6).
- **Step 48 — 주제별 필수 문헌 맵(리뷰급)**: R7 §4 12주제 ~150행 × 3.2 사다리 단 → 각 셀 = 현행 bib O/△/X · DOI 상태(Crossref 확인/서적/미검증) · v1.0.27 Phase 4.1~4.9 배치 · 성격(원전/교재/리뷰) · 필수/선택 판정 권위(R7 DQ-13: 다공전극군은 Non-goal 경계 표기용 한정 여부 master 삼각검증) · 2.4 공백 + 3.1 신규 → 원장 초판 골격(OUT-REFLEDGER). 정본 후보 표기 = 원장 상태 V0 후보/V1/V2/V3.

**게이트 3.5.** 규약 10조항 확정 문서 · 문헌 맵 축×단 셀 빈 칸 0(공백은 "공백" 명기) · 소급 전사 설계(키 93 + 부록 5 + 후보) · 검증 절차 문서. **중단 조건.** 없음(DR-6 불허 시 미검증 표기). **다음 조건.** Step 47·48 이력 + `PHASE_3.5_V1027_<topic>_RESULT.md`+`.json` + Ledger 행.

## Phase 3.6 — 설계 적대검토 (Step 49)

- **Step 49**: 3.1~3.5 산출 전체를 검수 sub(Fable 5.1)가 **refute mandate** 로 검토 — 최약점 1곳 지목·빈 통과 금지 · 렌즈 = **완주 렌즈셋 6종(구조·적대검산·follow·usable·완결성·regression) 전부** × 매 라운드 청크 스킴 전환 — **커버리지×렌즈 완주 + 연속 2R 확정결함 0 수렴 + 10R 하한**(THEORY BLUEPRINT 는 DG-A/B/C 결정과 챕터 4 전부의 유일 근거인 reference 급 → 헌법 §3 "애매하면 고가치" — 등급은 DR-23, 기본값 = 고가치) · FABLE 교훈 3("설계서 자체를 검증 대상으로") 적용 · **설계 doc 순응 검수의 한계**(Ch2 v4 w_eff narrowing 이 적대 2R 통과·v10 ρ(U_j) 자기모순 — R1 §4 관통 패턴) 회피를 위해 실행 기반 검증(SymPy 재검산 표시 항목: TH-2.1 (v)·TH-3.1·TH-7.2·Q-1 부호·양성) 포함 · master 삼각검증 후 수정.

**게이트 3.6.** 검수 보고서(최약점 ≥1·발견 건 4-tier) · 라운드 표(DR-23 기본값 10행) + 커버리지×렌즈 6종 매트릭스 missing 0 · 연속 2R 확정결함 0 · SymPy 재검산 결과 ≥3 항목 · master 삼각검증·수정 이력 · 수정 후 재게이트. **중단 조건.** 없음(FAIL 은 수정·재검). **다음 조건.** Step 49 이력 + `PHASE_3.6_V1027_<topic>_RESULT.md`+`.json` + Ledger 행.

## Phase 3.7 — Result: THEORY BLUEPRINT + 보고(비차단) (Step 50)

- **Step 50**: OUT-BP `V1027_THEORY_BLUEPRINT.md`(+`.json`) · 챕터 통합 Result `PHASE_3_V1027_BLUEPRINT_RESULT.md`+`.json`(3.1~3.6 Phase Result 위) · Ledger 행 3.1~3.7 · **Phase audit(문서 렌즈셋 6종) 3-Pass · 3.6 검수 라운드 표(커버리지×렌즈 매트릭스·연속 2R 확정결함 0) · R5 DQ 12·R6 DQ 12 각각 "해소/이관/미해소" 표** · **DG-B 채택 이론 목록을 master 가 확정**(사용자 위임 DR-11·15·16·17·18·23 — A 13·B 20 후보 각각 채택·조건부·보류 + 데이터 의존 패키지; master 판단은 "[master 판단]" 으로 표시) · DG-A(구조)·DG-C(라벨 v1.0.27)는 사용자 기확정(DR-3·DR-2·DR-12) · **사용자에게 BLUEPRINT 요지·채택 목록을 보고하고 정지 없이 챕터 4~7 세부 계획서 작성으로 진행**(DR-9; Correction History 재baseline 기록). **중단 조건.** 없음 — 사용자만 결정 가능한 항목이 **새로** 생기면 그 항목만 정지.

---

## Phase 4.0~4.9 — 저작 v1.0.27 (Steps 51– ; 3.7 Result 후 세부 계획서 작성)

> 골격 = 사용자 확정 구조(DR-3 재료별 3장 유지 · Ch1 흑연 = 이론 집중 + **후반부 부록 D = 통계역학 교과서급** · Ch2 LCO/Ch3 Si·블렌드 = Ch1 에 없는 분기 · 분리 빌드+xr DR-12 · 코드 문건 밖 DR-14). 각 Phase = **절 단위 루프**(정독 → 구성 → 자체검수 → 앞 절 정합 → 빌드 → ledger) + 빌드 게이트(xelatex 3-pass err 0·undefined ref/cite 0·STRUCTURE PASS·STRICT ALL PASS) + **전 tex 코드 토큰 0**(DR-14 — 부록 포함) + 버전 번호·검수 ID·**tier 표기** 0(DR-21) + **학술 용어 영어 원어**(DR-20) + Phase Result. 통째 배치 Write 금지(FABLE 교훈 1 — V4.1 σ 3중 충돌 29개소 사고·헌법 ①③). 아래 "내용" 열의 후보 ID 는 R5·R6 배치 열의 전사이며 **DG-B 채택 목록에 따라 갱신**된다. 권고 순서(R5 §4·R6 §7)는 A 군 의존 사슬(TH-9.2 → 1.1 → 5.1 → 1.2 → 2.1 → 3.1 → 9.1)을 따른다. **boxed 회수 게이트의 기준 좌표** — 현행 분포(Ch1 곡선 사슬 27·Part T 10·부록 E 4·독립 부록 3·Ch2 16·Ch3 4 = 64)는 참고이며, **3.2 Step 41 매핑표 기준으로 Phase 4.1~4.7 별 회수 건수를 재부여한다(합 64 불변; 부록 D 로 이동하는 Part 0·Part T 미시 boxed 는 4.4 에서 계수)**. [master — 비평 #2·DR-3]

| Phase | 이름 | 내용(후보 배치 — DG-B 확정 시 갱신) | 게이트 |
|---|---|---|---|
| 4.0 | 골격·프리앰블·기호표·용어표·분리 빌드 baseline | `Claude/docs/v1.0.27/` 신규 사본(DR-13) · 마스터 tex 3본(ch1/ch2/ch3 — 분리 빌드+xr, 파일명·xr 키 = v1.0.27) · `_sections/` 골격(3.3 이동 맵·새 접두 규약) · 공통 프리앰블(F-06 조판 승계·`\newtheorem` 정의·정리·증명 환경·keybox 통일 G41·tier 매크로 제거·**독자 지시형 박스(verifybox 류) 폐지 → 저자 확인은 서술**) · **기호 통합표 TH-9.2**(g·q·u_j·γ·F·z·ξ↔θ·Ω 정의식·h_η·U_oc) · **용어 결정표(DR-20: 문장 골조 한글·학술 용어 영어 원어·한국 학술용어 존중·일본식/중국식 배제)** · 두문자어 표(11종+) · 라벨 네임스페이스(429 보존/alias 매핑표) · 자산 태그 3분류 · 원장→bib 파이프라인(리뷰 논문 포맷 DR-19) · **코드 이전**(코드맵·코드 절·부록 E 대응 지도 → OUT-CODEDOC; 문건 tex 코드 토큰 0) · 동기 층 서론 1문단(M-보정 인자의 정체 = broadening, R3 A-9·anodefit MASTER §2) · CRLF/LF 규약 · 도구 동작 확인 · 빈 절 빌드 | 분리 빌드 3-pass err 0 · STRUCTURE PASS · 라벨 매핑표 429/429 · 기호표 충돌 0 · T-5(전 tex 0) · T-6(용어·노테이션) · `tier` 0 · T-19 대조표 골격 |
| 4.1 | Ch1 Part I — 평형 열역학(일반→특수) | 중심(eq:Uj + TH-7.5 Kirchhoff U(T)) · 폭 · regular solution(Bragg–Williams 원전; 일반 격자기체 Hamiltonian·평균장은 부록 D 결과 전방 참조) · **TH-2.1 regular solution + Maxwell 두-상 dQ/dV 사슬**(볼록 포락 → Maxwell 델타 + 단상 꼬리 → 폭 합성·Dreyer 연결·Ω→2RT⁺ 연속성) · **상분리 편입**(DR-11: binodal·spinodal·Maxwell·CNT 결과는 본문, 유도는 부록) · **TH-3.1 Redlich–Kister → α_j 회수**(opt-in 분기·식별 가드) · Frumkin 계보 srcbox · staging(TH-4.1·4.2 설명층)·gallery≠상·해상도 사다리·U_j 간격의 열역학 해석·N4 두-상 표기 확정 | 회수 검산(Ω→0 eq:eqpeak·Ω≤2RT eq:lcoomega-kernel·L_1=0 eq:dUhys) SymPy · 독립 부록 boxed 3/3 회수(ξ↔θ 치환 후 SymPy 동치) · Step 41 매핑표 회수 건수 · T-19/T-20/T-21 · 빌드 |
| 4.2 | Ch1 Part I — 동역학 | **K-1 Eyring/TST 척추 재배열**(DR-16 master 판단 = 회복: 출발식 = TST 일반식 → eq:bv → eq:db → eq:kuniv → eq:tst-box → 세 인자의 자리 → L_q·L_V·동결) · K-2 가정 등록 · **R6:T-1 entropy production·affinity 일반 상태식 → R6:T-2 선형 flux–force 회수창**(warnbox) · E-1 일반 BV↔κ(ξ) 통일(B) · E-2 Marcus 일반형 + BV 회수(C) · **R-2 KWW/장벽분포 일반형**(DR-15 master 판단: 일반형 + ρ=δ 회수는 본문, 파라미터화는 opt-in) · R-1 master equation → 완화 ODE·Kramers · R-3 Watson 큐뮬런트 · (E-3 농도 분극·R-4 확산 = DG-B 데이터 패키지) · lag·tail(N8 승계) · **S-1 부록 E 3층 승계**(자기일관 부록 → 4.5) · 전달함수·S-3 Kubo 정적 극한 명명·S-4 각주 | 동결극한·평형극한 회수 검산 · 부록 E boxed 4/4(4.5 에서 계수 시 이관 명기) · L4 옵션 채택 시 rank-1 상실 warnbox · T-19/T-20/T-21 · 빌드 |
| 4.3 | Ch1 Part T — 열특성·히스테리시스 | TH-7.1 세 분포 분리 가정(결과; 미시 유도는 부록 D) · config·vib·electronic 결과식(부록 D 회수) · **TH-7.4 일반 엔트로피 수지 → Bernardi → 단일활물질** · **Q-1 Q̇_irr 분해(옴·지연·분기)** · Q-2 완전 cycle 히스 소산(DR-18 master 판단 = 부분 해제: 완전 cycle 소산은 범위 안·부분 cycle·경로의존·Jarzynski 는 밖·∂Ω/∂T 는 일반식만 opt-in) · Q-3 소거 항 조건 · TH-6.3 Maxwell 관계 2계 · CLOSING Part 4 (4) n(T)↔config 규칙 명문화 · 히스 = spinodal·gap(승계)·**H-2 regular solution→logistic rung**(극한 회수; 커널 채택은 DG-B/2.6)·**TH-5.2/H-1 CNT+CH → γ_j 함수형**·Dreyer 다입자·cusp 각주(C)·TH-8.2 비대칭 binodal/spinodal/Maxwell 일반화 · **§1.18 적층 준안정·athermal 훅**(DR-17 master 판단: 3.1 에서 Opus v4 §1.18 원문 정독 후 설명층 채택 / 부록화 중 택1 — 영구 배제 X) | Part T 자산 회수 boxed 10/10(Step 41 기준) · σ≥0 검산 · γ_j→1 spinodal·γ_j→0 Maxwell 극한 회수 · T-19/T-20/T-21 · 빌드 |
| 4.4 | **Ch1 후반부 부록 D — 통계역학(교과서급, 신규 요구)** | 현행 Part 0(sec02a·02b) + Part T 미시 유도부(분배함수·config·vib/electronic·Einstein·mixing·극한) + SM2-A/B/C + Sommerfeld + Einstein/Debye 전부 이전·**확장**: 앙상블·분배함수·Boltzmann/Gibbs 인자 → 격자기체 Hamiltonian(cluster expansion·Ising 동치, TH-1.1) → 평균장/Bragg–Williams·준화학/CVM(TH-2.2) → 요동-응답(감수율 항등·앙상블 동등성·켤레 쌍·일반 요동 항등 TH-1.2) → 엔트로피 분해(config·vib·electronic) → 포논 DOS → Einstein/Debye(TH-7.2) → FD/BE → Sommerfeld(TH-7.3) → Maxwell 관계 — 각 항목 = 전제 개념 선행 도입 → (a)~(d) 전 중간식 → 본문 어느 식으로 회수되는지 표(**독자 참여형 섹션 X** — 사용자 확정; 이해를 돕는 장치는 전제 설명·중간식·회수 표로). **비전공자·타전공 석박사 가독을 게이트로**(T-21 전항) — "대학원에서 통계역학을 오래 한 독자도 어려웠다" 는 사용자 판정을 기준 삼아 본문보다 느린 호흡으로 쓴다 | (a)~(d) 100% · 부록 D↔본문 회수 표 100%(Part 0 boxed 9 + Part T 미시 boxed 전건) · T-20(예제·연습 제외) · T-21 7항목 전건 O · 학술 용어 영어 원어 · 빌드 |
| 4.5 | Ch1 기타 부록 | 기호(통합표 정본) · 부호검산 · 자기일관(부록 E 승계 · **S-2 refs 6/7 ② JCP147 PDF 재대조·⑤ dossier 대조 — DR-8: 리포 내 `JCP_147…pdf`·`jcp_extract.txt`·`PHASE_DIAG_REFS67_DOSSIER.md` 사용, refs 6·7 원문 미소장 정직 표기**) · **S-5 dependency graph·4분류 표**(P3 #3·#4) · 상분리 유도(편입 후 잔여) · 수학 방법 노트(SURV Tier3 각주군) · numverif2026 이관 · **코드 대응 지도는 문건 밖(OUT-CODEDOC) — 부록에서 제거** | 부록 전건 · P3 ⑤ 5항(② 미완 0) · P3 #3 graph 1본 · T-19 대조표 전건 완성(TH-9.1 실물) · 코드 토큰 0 · 빌드 |
| 4.6 | Ch2 LCO 분기 | **Ch1 에 없는 것만**(F-08 차이 선도): σ_d 재배선·order-disorder·전자 엔트로피 항·Ω 커널 지위·G01 사다리 뒤집기(일반 적분형 박스·상수형 회수)·sec16b 분리(Ω 커널 → Ch1 일반 / 전자항 옵션 → 서술)·G04 Ω↔ECI 축약 보강·G11 순환 논증 제거·Sommerfeld 정본 참조(부록 D)·검수 ID·버전 라벨·tier 0 · Ch1 결과식 xr 대응표 | boxed 회수 16/16 · Ch1 중복 유도 0 · T-19/T-20/T-21 · 빌드 |
| 4.7 | Ch3 Si·블렌드 분기(**음극 예측 강화**) | **Ch1 에 없는 것만**: Si 연속 고용체(Frumkin)·c-Li15Si4 두-상·분리 branch(H-5)·블렌드 중첩·유효경계(S2)·eq:blend-dqdv 박스 승격·eq:sifr-blend 지위(G21)·G23 Larché–Cahn 유도 + Λ_σ 닫힘·GS-1/GS-2 4분류 유지·SiO_x 정직 공백·orphan `ch1_appD_si` 이동 기록 · **Si 예측 보강 목록(3.1·3.3 확정분 — 흑연·Si 를 제대로 예측하는 것이 사용자 우선 목표)** · 코드 절 §3.5 제거(문건 밖) | boxed 회수 4/4 · T-19/T-20/T-21 · 코드 토큰 0 · 빌드 |
| 4.8 | 3장 정합·분리 빌드 마감 | xr 교차참조 전건 해소(ch1→ch2→ch3→ch1 재패스) · 장간 중복 유도 0(정본 1곳 + alias) · 라벨 429 매핑 · 병합 빌드는 완성 후 옵션(DR-12) · Ch2/Ch3 가 Ch1 결과식만 받고 재유도하지 않는지 대조 | 3장 err 0·undefined 0 · T-15 orphan 0 · xr 대응표 빈 셀 0 · 빌드 |
| 4.9 | 챕터 4 통합 Result·게이트 재실행 | **boxed 회수 합 64/64 확인(Step 41 매핑표 기준 — T-4·T-12)** · T-5/T-6/T-7 전 tex 재실행 · T-19/T-20/T-21 전건 · 부록 D↔본문 회수 표 · `PHASE_4_V1027_AUTHOR_RESULT.md`+`.json` · Ledger | 게이트 전건 GREEN · Result md+json · Ledger 행 4.0~4.9 |

## Phase 5.1~5.3 — 서지 완결 (3.7 Result 후 세부화)

| Phase | 내용 | 게이트 |
|---|---|---|
| 5.1 | 원장 확장·DOI 전수 검증 | 원장 전건 DOI 검증 ∈ {검증/DOI 없음 확인(서적·내부)/미검증} · 기억 서지 0 · **한 문헌 한 키(동일 DOI 2키 = FAIL, R-01)** · 저자 전원 명기(R-06) · R-02~R-05 정정 · 부록 [A1]~[A5] 키화 · 미등재 6 소급 · `refcheck/` 응답 보존 · bib 생성(손편집 0·헤더 카운트 = 실물) · **서지 포맷 = 전문 리뷰 논문 표준(DR-19: 번호 인용·저자 전원·저널·권·쪽·연도·DOI, 3장 통일 스타일)** |
| 5.2 | 인용 밀도·1차 문헌 매핑 | 절별 밀도 표 · 유도 절 출발식마다 표준 출처 ≥1 · 실측 수치 1차 문헌 ≥1 · 본문 무인용 절 0(요약·검산·코드 절 제외) · 이론 원전 층 X 48 → 등재 또는 "공백" 명기 · Daumas–Hérold 실물/대체 인용 결정 |
| 5.3 | 서지 감사 Result | `PHASE_5_V1027_BIB_RESULT.md`+`.json` · Ledger |

## Phase 6.1~6.3 — 검수·수렴·마감 (3.7 Result 후 세부화)

| Phase | 내용 | 게이트(정량) |
|---|---|---|
| 6.1 | 가변 청크 검수 | **10라운드 + 커버리지×렌즈 6종(구조·적대검산·follow·usable·완결성·regression) 완주 둘 다 충족**(고가치 reference 등급) · 매 라운드 청크 스킴·렌즈 전환 · coverage missing 0 · 수렴 = 연속 2R 확정결함 0 · **follow 렌즈 변형 = 산문을 가리고 수식·박스·라벨만 노출한 청크로 ≥1회 따라오기**(기준 1 "수식만으로도 80~90%" 의 조작적 근사 — proxy 임을 Result 에 명기; 실독자 reading-test 는 미수행) · usable 렌즈 입력 = T-21 표 · **실행 기반 검증 렌즈**(SymPy 재유도(T-12 회수 boxed 64 전건)·수치 극한 Ω→0·L_V→0·α=1·L_1=0·T 극한·기존 코드로 회수 가능한 식의 수치 대조 — 코드 수정 없이) · **샘플 이미지 QA**(코드 무수정 조건에서 기존 게이트·샘플 스크립트가 낸 곡선의 연속·매끄러움·미분가능성 육안·수치 점검 — R2 P-7·비평 #11) · 수렴 후 편집 시 게이트 재실행(V5.R8 미게이트 회귀 사고 방지, R1 §2-보충) |
| 6.2 | 규범 게이트 | CLAUDE.md P3 8항(현행 기호·조립 단위로 재해석한 확인 가능 조건, T-13) + 헌법 3종(D1~D6 grep/수동 분해) + F-04/F-10/F-11 grep 0 + 버전 번호·검수 ID·고백조·**tier 표기** 0(T-7 확장·DR-21) + **학술 용어 영어 원어 규약(T-6·DR-20)** + **전 tex 코드 토큰 0(T-5·DR-14)** + **T-19 사다리 대조표 전건(간소화 지점 × 가정·유효범위·레퍼런스·회수 조건 빈 셀 0) + T-20 교재 형식 요소 절별 O/X + T-21 가독성 7항목** + 자산 무유실(라벨 429 매핑·boxed 64 회수 = 27+10+4+3+16+4·태그 승계) |
| 6.3 | 마감 | 빌드 GREEN·PDF·렌더 육안 점검(좌측 넘침 F-07) · `Claude/docs/HANDOVER_v1.0.27.md` · `docs/INDEX.md`·`plans/INDEX.md` 갱신 · **OUT-CLAUDEMD CLAUDE.md 개정안 문서 제출(DR-13)** · commit·push(master) · `PHASE_6_V1027_CLOSING_RESULT.md`+`.json` · Ledger |

## Phase 7.1~7.3 — 코드 동기(doc-leads) (챕터 6 종료 후 세부 계획서 작성 — DR-4·DR-9)

> 코드와 이론은 별개(DR-10). 문건 v1.0.27 이 authoritative 이며 코드는 그것을 따른다(doc-leads). 문건 tex 는 코드를 언급하지 않고, 코드 대응은 문건 밖 코드 문건(OUT-CODEDOC)에 둔다(DR-14). 챕터 6 Result 뒤에 세부 계획서를 쓴다.

| Phase | 내용 | 게이트(정량) |
|---|---|---|
| 7.1 | 문건↔코드 대응 지도(OUT-CODEDOC 갱신) | v1.0.27 boxed 전건 ↔ 코드 함수 1:1 표(현행 `ch1_appB_codemap`·`ch2_appB_codemap`·부록 E 대응 지도·`ch3v22_sec05_code` 이전분 갱신) · 미구현 식 목록 · 채택 커널(2.6·DG-B 결과)의 구현 명세 · `CODE_GUIDE`·`FITTING_GUIDE` 갱신 계획 · Result |
| 7.2 | 코드 개정(`Anode_Fit_v1.0.27.py`) | additive·기본 경로 bit-exact 폴백 · 신규 게이트 · 기존 게이트 4종 GREEN 불변 · 골든 max\|d\|=0 · 문건 boxed ↔ 코드 1:1 감사 · Result |
| 7.3 | 검증·마감 | 공개데이터(기확보 SINTEF + 필요 시 조사 서브 확보분) 재현 · 문건이 서술한 극한·수치 결과 = 코드 출력 · `PHASE_7_V1027_CODE_RESULT.md`+`.json` · Ledger · HANDOVER 갱신 · commit·push |

---

## Implementation Interfaces

> 비코드 프로파일: **운용**(모델·유닛·기록·재독·정지·git·구조 맵·검수 강도·스크립트 인터페이스·시드 취급).

- **모델** = **본작업(저작·분석·검수·감사·통합) = Fable 5.1**(사용자 명시 예외, brief:45) · **조사(문헌 검색·DOI 검증·공개데이터 확보·기계 추출) = Haiku(A4) / Sonnet 4.6(A3) 서브**(DR-5·DR-6 사용자 확정 — 토큰 절약 기본 골조; 조사 서브는 본작업 유닛과 별개로 운용 가능, 산출은 파일로 인계하고 본작업 sub 가 정독 후 사용). 지정 모델 런타임 장애 시 silent substitution 없이 정지·보고.
- **유닛** = master + 작업 sub + 검수 sub, **직렬**(DR-5 확정: 내용 연속성). 동시 산 서브 ≤1. **조사 서브(Haiku/Sonnet)는 사용자 허가 carve-out**(DR-5·DR-6)으로 본작업 유닛과 겹쳐 살아도 유닛 수에 넣지 않는다 — 단 shared mutable state 무접근(읽기·파일 산출만). 그 밖의 fan-out 은 자의 금지. 판독 단계(2026-09-03)의 8 에이전트 병렬 승인 출처 = 사용자 2026-09-02 발화 "울트라 코드로 다시 시작해"(헌법 §1-병렬 ③).
- **역할 경계** = master: 맥락·계획·통합·최종 판단·commit·git log 대조 / 작업 sub: 지정 산출물 구성 + 자체검수 / 검수 sub: refute mandate·최약점 1곳·빈 통과 금지·등록부 근거 행 원천 전건 대조 / master 삼각검증 후 직접 수정. **시드 취급** = R1~R7·v1 초안은 작업 sub 판정이므로 그대로 확정하지 않는다 — 해당 Phase 의 작업 sub 가 보강·통합하고 검수 sub 가 refute 한 뒤 master 가 확정.
- **sub prompt 5항목 고지** = 역할 · 분업 경계(담당 범위·commit 권한 없음·Codex 무접근) · 범위 밖 자의 금지 · 허위 attribution 금지(verbatim/요지 등급 규약 포함) · 필요 memory 맥락 주입(전문 정독·4-tier·흐름 보호·소통).
- **기록** = 스텝 이력 `Claude/results/Step <N> — <제목>.md`(step 하나 = 파일 하나 · 5항목 · 즉시 기록) · Result `Claude/results/PHASE_<id>_V1027_<topic>_RESULT.md`+`.json`(12항목) · Ledger `Claude/results/PHASE_1-7_V1027_EXECUTION_LEDGER.md`(12-col) · 세부 계획서 = 챕터 1 은 마스터 내 Phase 절 / 챕터 2 이후 = `Claude/plans/2026-MM-DD-v1027-phase-<id>-plan.md`(헤더의 3단 구분) · 핸드오프 `Claude/results/handoffs/<task>/` · 인계 `Claude/docs/HANDOVER_v1.0.27.md`.
- **재독 강제** = 매 Phase 착수 시 마스터 플랜 본문 재독(첫 Step 이력에 `[Phase N 착수 — 마스터 플랜 재독]` 기록) · 매 Step 착수 시 세부 계획서 재독 · 매 Phase(1.1~7.3 전건) 종료 시 Result 12항목(md+json) + Ledger(Result 없이 다음 Phase 금지 — 챕터 말 Phase 1.5·2.7·3.7·4.9·5.3·6.3·7.3 은 챕터 통합 Result 를 겸함) · 컴팩션·재개 직후 5-check.
- **유연성(DR-9)** = 마스터 플랜은 헌법이다 — 실행 중 필요한 신규 Phase·Step 은 **추가**할 수 있으나(cumulative 번호 부여·Correction History 기록) 기존 Phase·Step·게이트를 **삭제·축소하지 않는다**.
- **정지 조건** = 파괴·비가역 · 사용자만 결정 가능한 blocking 이 **새로** 생길 때(DG-A/C 는 사용자 확정·DG-B 는 위임 — 3.7 은 보고점) · 권한 부족 · 보호영역 침범 · 새 의존성(SymPy 부재 등) · confirmed FAIL gate · 사용자 stop · 통제문서 모순(1.3 — 더 제한적 지시 채택·사용자만 결정 가능하면 정지). **병렬 승인 필요는 정지 사유 아님**(직렬·DQ). DQ 항목은 blocker 아님. 중간 "재확인" 지점은 두지 않는다(DR-6 확정: 외부 논문·데이터는 필요 시 즉시 확보).
- **git** = 각 Step/Phase 종료 commit(master 전용) · **매 Phase = [작업 commit] + [검토·정정 commit] 페어**(스킬 3c — 작업과 검토를 한 commit 에 뭉치면 누적 오류가 묻힌다; 변경량 <30라인의 소규모 Phase 만 간소 통합 commit 가능·Result 는 필수) · push 는 Phase 종료 시 · merge X · 파괴·비가역 직전 commit(복원 지점) · 삭제·덮어쓰기는 git 안에서도 평문 사전 확인 · 동결 폴더 무수정.
- **구조 맵** = §2.8. 폴더·파일 추가·삭제·이동·이름변경 시 그 자리에서 즉시 갱신(갱신 없으면 미완).
- **검수 강도** = A1·A2 고가치 reference(v1.0.27 문건): 10R + 6렌즈 완주 둘 다(6.1) · **THEORY BLUEPRINT(3.6~3.7): 고가치 reference 등급 — 10R + 커버리지×렌즈 6종 완주 둘 다 + 연속 2R 수렴**(DG-A/B/C 와 챕터 4 전부의 유일 근거 → 헌법 §3 "애매하면 고가치"; DR-23 사용자 위임 → master 확정: 이대로) · 챕터 1~2 산출물(등록부 3종·GAP REGISTER): 검수 sub 1R 이상 + 연속 2R 확정결함 0 수렴(통상 — DR-23 에서 상향 가능) · 정형·기계 작업(카운트·grep·Crossref 조회): 자체검수 1회.
- **보고** = 4-tier(확정/근거 미발견/추정/미검증) · 확정에 path+line · 확정 사안 재질의 X · 결정 요청은 본문 평문 + 기본값(팝업 도구 X) · verbatim/요지 등급 병기.
- **스크립트 인터페이스**(읽기 전용·기존 도구 재사용) = 자산 카운트 = T-4(정의 문서 동반) · 구조 검사 = `python tools_check_structure.py check <dir> <master.tex …>`(`check` 만) · 엄격 검사 = `python tools_tex_strict_check.py` · 빌드 = `xelatex -interaction=nonstopmode <master.tex>` 3-pass(v1.0.27 순서는 4.0 확정) · 코드 게이트(수치 대조 목적 읽기·실행만) = `python test_gates_v1024.py`·`_reflect.py`·`_selfconsistent.py`·`test_gates_v1025.py` · Crossref = `Invoke-RestMethod https://api.crossref.org/works/<DOI>`(DR-6) · 서지 원장 → bib 생성 스크립트(4.0 신설) · 조사 코드 `regsol_kernel.py`·`test_gallery_vs_regsol.py`(2.6 실행 여부 = DR-6·DQ).
- **문체** = 문장 골조 한글 + **학술 용어는 영어 원어**(DR-20: 한국 학술용어는 존중, 일본식·중국식 번역어 배제, 애매하면 영어 — 예: regular solution·entropy production·affinity·implicit function·perturbation) · 두문자어 첫 출현 병기 · **tier 표기 X**(DR-21) · 메타 발언 X(계획·이력 문서 포함).

---

## Test Plan

> 전부 **확인 가능한 조건**(명령 + 증거 + 범위). "적절해 보임" 은 게이트가 아니다. 직전 v1 초안의 T-1~T-14 를 승계(번호·이름 유지)하고 판독이 요구한 정의 확정·신규 게이트(T-15~T-18)와 감사가 요구한 사용자 기준 2·4·5 의 확인 가능 게이트(T-19~T-21)를 더했다.

| ID | 게이트 | 명령/방법 | 증거 | 범위·기준 | 적용 Phase |
|---|---|---|---|---|---|
| T-1 | LaTeX 빌드 | PowerShell: `& 'C:\Users\lksz1\AppData\Local\Programs\MiKTeX\miktex\bin\x64\xelatex.exe' -interaction=nonstopmode <master>.tex` × 3-pass(전체 경로 — PATH 미검증 Assumptions 1; xr 순서는 4.0 확정; Bash 도구면 같은 경로를 큰따옴표로) | `.log` `!` 오류 0 · undefined references/citations 0 · 페이지 수 | 오류 0·undefined 0(전 마스터) · 대형 overfull 0 · 렌더 기반 좌측 넘침 점검(F-07) | 4.0~4.9 · 6.3 |
| T-2 | 구조 검사 | PowerShell: `$env:PYTHONIOENCODING='utf-8'; python tools_check_structure.py check <dir> <masters…>`(`check` 만; Bash 도구면 `PYTHONIOENCODING=utf-8 python …` — v2 의 bash 접두 구문은 PowerShell 에서 미실행) | `STRUCTURE_CHECK: PASS` | 미해소 ref 0·env 짝 0·dup 라벨 0·cite-undef 0·bibitem-uncited 0 | 4.x·6.3 |
| T-3 | 엄격 검사 | `python tools_tex_strict_check.py`(+ "cite 키 ⊆ 원장 V1" 검사 확장 후보 — 도구 실물 미정독) | `STRICT CHECK: ALL PASS` | $ 패리티·중괄호 depth 0·미확인 매크로 0·원장 밖 cite 0 | 4.x·5.1·6.3 |
| T-4 | 자산 카운트(정의 고정) | PowerShell/Python — **카운트 집합 정의: 파일 집합 60 tex(마스터 3 + `_sections` 56 + 독립 부록 1) = 빌드 포함 58 + 빌드 미포함 2(orphan `ch1_appD_si`·독립 부록), 열별 부분합 병기(빌드 포함 58 만 세면 boxed 61·label 392); 주석 제외 여부 명시** — **정의 문서**: display = `equation/align/gather/multline(*)` 230 과 `\[…\]` 38 분리 · boxed 64 전 문건(27+10+4+3+16+4) · cite 명령 265(262+3)/키 단위 315 · bibitem 95/distinct 93 | 카운트 표 + 정의 문서 | v1.0.25.1 = brief §4.2 전건 일치(파일 집합 60 기준) · v1.0.27 = 자산 무유실(라벨 429 전건 존재 또는 alias 매핑표 · boxed 64 회수표 100% = 27+10+4+3+16+4 · 태그 승계표) | 2.1·4.0·6.2 |
| T-5 | 코드 = 문건 밖(DR-14) | **v1.0.27 전 tex(본문·부록 전부)** grep: `\\code\{|\\texttt\{|func_|solve_U_oc|_regsol|regsol2|regsol_si|BlendedAnodeDQDV|LCOCathodeDQDV|GraphiteAnodeDischargeDQDV|include_electronic_entropy|use_si_constants|\.py\b|\.md\b` — 토큰 정의는 2.5 Step 28 확정(DR-14) | 히트 수 + 파일:행 | **0**(DR-10·DR-14 — P3 ⑧ 를 "문건 밖" 으로 강화) · base 현행 3~7 은 GAP 등재 · 코드 대응은 OUT-CODEDOC 에만 | 2.5·4.x·6.2 |
| T-6 | 용어(F-10·DR-20) | grep: `요동|양성|유일근` → 0 · `음함수|섭동|준위|정칙|정규용액` → **영어 원어**(implicit function·perturbation·energy level·regular solution; 한글 병기는 첫 출현 선택) · `정준|대정준` 은 사용자 확정 유지 · 용어 결정표(4.0) 밖 한글 번역 학술어 0 · 두문자어 표 대조 · **F-02/F-03 노테이션: 확률 대문자 `P(`·`P_i` 류 0(압력 P·전력 등은 수동 판정 제외) · 총량 대문자 F/S vs 자리당 소문자 `f_\mathrm{int}`·`s_\mathrm{int}` 규약 grep(대문자 `F_\mathrm{int}`·`S_\mathrm{int}` 0)** | 히트 수 + 병기 표 + 노테이션 표 | 본문·부록 0 · 학술 용어 = 영어 원어(용어표 외 한글 번역 학술어 0) · P/p·F/f 규약 위반 0 | 2.5·4.0·6.2 |
| T-7 | 헌법 ① D1/D2 + register | grep(자기 diff `구판|이전에는|폐지했|v1\.0\.\d+`) + 검수 ID(`#\d+ 정정`) + 고백조(`우리 진단|우리 ablation|회사가 .*검산`) + 프로세스 어휘(`opt-in|round-trip|bit-exact|골든|G-SI|@\d`) + 방어 어투 후보 → 수동 판정 분해 + `tier|Tier` grep | 후보 목록 + 판정 | 렌더링 텍스트 0(채택/미채택 지위는 버전 번호 없이 서술) · **tier A/B/C 표기 0**(DR-21 — 신뢰·가정 상태는 서술로; 매크로·각주 정의 제거) | 2.5·6.2 |
| T-8 | 헌법 ③ D3 | boxed 각각 (a)(b)(c)(d) 존재 표(4단 척도·항목 분해) + "대입하면|풀면|수치 확인|표준" 류 점프 grep 후보 | 표 | 현행 64/64 진단 · v1.0.27 목표 boxed 100% 완결(비유도 박스는 해제 또는 규약 표시) · 비박스 결과식 15 판정(라벨 단위) · 6.1 에서 산문 가림 follow 변형 ≥1회(proxy 명기) | 2.2·4.x·6.1 |
| T-9 | 서지 | Crossref 조회(DR-6) 또는 원문 대조 · 원장 ↔ bib 대조 스크립트 | DOI 검증 표 · 대조표 | bibitem 전건 ∈ {검증/DOI 없음 확인/미검증} · 기억 서지 0 · **한 문헌 한 키(동일 DOI 2키 = FAIL)** · 헤더 카운트 = 실물 · 저자 전원(et al. 0) · 원장 미등재 키 0 · **리뷰 논문 서지 포맷 통일(DR-19)** | 2.4·3.5·5.1 |
| T-10 | Read Coverage | Result 12항목 Read Coverage 에 파일·행 범위(판독 R# 커버리지 병기) | 표 | 배정표 합계와 일치(차이 = 미검독 명시) | 1.5·2.7·3.7·매 Result |
| T-11 | 검수 하한 | 라운드별 청크 스킴·렌즈·발견 건 기록 | 라운드 표 10행 + 커버리지×렌즈 6종 매트릭스 | 10R **and** 6렌즈 완주 · 연속 2R 확정결함 0 · 수렴 후 편집 시 재게이트 | 6.1 |
| T-12 | 실행 기반 검증 | SymPy 재유도 스크립트(**회수 boxed 64 전건의 식-수준 동치 — 사다리 단 특수화 → 현행 boxed, 위치 이동·기호 치환(ξ↔θ)·재라벨을 겪는 부록 E 4·독립 부록 3 포함** + R5 §6 추정 항목 TH-2.1 (v)·TH-3.1·TH-7.2 + Q-1 부호) · 수치 극한(Ω→0·L_V→0·α=1·L_1=0·T 극한) · 기존 코드 게이트 재실행(수치 대조) | 스크립트 출력(검산 ID = T-19 회수 조건 열과 1:1) | 재유도 동치 64/64 · 극한 회수 항등 · 기존 게이트 GREEN 불변(코드 무수정) · SymPy 부재 시 정지·확인 | 3.6·4.x·6.1 |
| T-13 | P3 8항(현행 기호·조립 단위 재해석) | ① `V_app`·`V_n`·`U_j`·`U_oc` 구분 일관 grep·표 ② 전하 보존식 boxed 위치·중심식 유지 ③ dependency graph 존재 ④ 4분류 표 ⑤ 5항 sub-section + ② 페이지·문단 확정 ⑥ 전달 정합 표(Ch1↔Part T↔Ch2↔Ch3·다중 수록 0) ⑦ 5축 명칭 표 ⑧ T-5 | 표·grep | 8/8 · CLAUDE.md 원문 개정은 OUT-CLAUDEMD 문서로 분리 | 3.4·6.2 |
| T-14 | 기록 완결 | Step 파일 수 = 수행 Step 수 · **Result md+json 쌍 = 종료 Phase 수(1.1~7.3 전건; 챕터 말 Phase 는 통합 Result 로 계수)** · Ledger 행 | 파일 목록 | 누락 0 | 매 Phase |
| T-15 | 빌드 포함/orphan 검사(신규) | 마스터 tex `\input{…}` 집합 vs `_sections/*.tex` 집합 차집합 | 목록 | v1.0.25.1 = orphan 1(`ch1_appD_si`) + 독립 1 확인 · v1.0.27 = orphan 0(이동 기록 있는 파일 제외) | 1.1·2.1·4.0·6.2 |
| T-16 | 원장 ↔ bib 전건 대조(신규) | 원장 `.json` 키 집합 vs bib 키 집합 · 상태 V1 만 cite 허용 | 대조표 | 미등재 0 · 원장 only 는 상태 V2/V3 로 표시 · V1023 사본 문제 해소 | 2.4·3.5·5.1 |
| T-17 | 라벨 없는 boxed·비유도 박스(신규) | `\boxed` 환경별 `\label` 존재 + 4단 척도 "비유도" 박스 목록 | 표 | v1.0.27: 라벨 없는 boxed 0 · 비유도 박스는 해제 또는 규약 박스(keybox 등)로 전환 | 2.2·4.x |
| T-18 | 판정 상충·조건 분리(신규) | 2.6 상충표(전이 수·프로토콜·소재·지표 열) | 표 | 4행 × 조건 열 빈 셀 0 · 수치는 원천 path+line | 2.6 |
| T-19 | 사다리 대조표(기준 5 저작 게이트 · R5 TH-9.1 의 문건 측 실물)(신규 v3) | 표: 행 = 간소화 지점 전건(2.3 등록부 65 + 3.2 신규 단의 특수화 지점 + 3.4 목표 boxed) · 열 = 사다리 좌표(축·단 ID)·가정 ID(가정 문장 verbatim 링크)·유효범위·레퍼런스(원장 V1 키)·회수 조건(극한 + T-12 검산 ID) | 표 파일 + 빈 셀 카운트 | 빈 셀 0 · 레퍼런스 열 = V1 키만(원장 밖 0) · 회수 조건 열 = T-12 검산 ID 와 1:1 · 3.4 = 계획판(목표 boxed) / 4.1~4.9 = 절별 완성 / 6.2 = 전건 | 3.4·4.1~4.9·6.2 |
| T-20 | 교재 형식 요소(기준 2 저작 게이트)(신규 v3) | 절별(section·subsection) O/X 표: 정의·정리(명제) 환경(4.0 `\newtheorem` 신설 후) ≥1 또는 "N/A(적용 절)" 사유 · (a)~(d) 표지(유도 절 100%) · **독자 참여형 섹션(예제·연습문제·풀어보기·독자 지시형 박스) = 제외**(사용자 2026-09-03 "이 문건은 논리 전개가 주고, 독자 참여형 섹션 즉 예제나 연습 문제를 풀거나하는 일을 하지 않게") — 저자가 수행한 극한·부호·크기 확인은 독자에게 시키는 형식이 아니라 논리 전개의 문장으로 서술 · 절 요약 keybox · 기호 첫 출현 정의(기호표 대조) · 도입/마무리 다리 · 연습문제 = 제외(사용자 확정 2026-09-03) | 표 | 빈 셀 0 · 유도 절 (a)~(d) 100% · 요약·정의 열의 X 는 사유 명기(빈 통과 금지) · **독자 참여형 섹션 열 = 0(제외 확인)** | 2.5(Step 27 진단판)·4.1~4.9·6.2 |
| T-21 | 타전공 석박사 가독성(기준 4)(신규 v3) | 2.5 Step 29 의 7항목 — (i) 전제 개념 선행 도입 (ii) 기호 첫 등장 정의 (iii) 두문자어 첫 출현 병기 (iv) 절 도입/마무리 다리 (v) 극한·코너·tier 표기 (vi) 전방 참조 밀도(정의 전 사용 수/절) (vii) 오독 유발 문장·명명 충돌 — 절별 O/X | 표 | 빈 셀 0 · (ii)(iii) = 100% · (vi) 정의 전 사용 0(또는 사유) · 6.1 usable 렌즈의 입력 표 | 2.5(Step 29 진단판)·4.1~4.9·6.1·6.2 |

---

## Assumptions

> load-bearing 전제. **실행 직전(GO 후 Step 1 전) 실물 대조** 대상. 거짓이면 STOP → Correction History 재baseline. 검증 상태 = sub 실측 ✓ / R# 확정 / brief 인용·미검증 / 추정.

1. `xelatex.exe` 가 위 MiKTeX 경로에 존재하고 빌드가 가능하다 — 존재 **sub·master 실측 ✓ 2026-09-03**(대조 명령 = `Test-Path 'C:\Users\lksz1\AppData\Local\Programs\MiKTeX\miktex\bin\x64\xelatex.exe'`); 실행 가능 = 2026-07-26 빌드 실증(A4:55)·PATH 무관(T-1 은 전체 경로 호출).
2. `Claude/docs/v1.0.25.1/` 은 동결 base 이며 자산 카운트가 brief §4.2 와 같다 — **sub 실측 ✓**(60 tex·9214줄) · 단 자산 태그 계열은 v1 실측과 R3 grep 이 상충(§2.2) → 2.1 확정 전까지 "다계열" 로만 취급.
3. v1.0.25 vs v1.0.25.1 차이 = `_sections` 3파일(sifr 2 hunk·width 1·eqpeak 1) + 마스터 3(표시 버전) · 코드·독립 부록 동일 — **sub 실측 ✓ hash · R4a·R4b diff 확정**.
4. `Claude/docs/v1.0.27/` 은 부재(신규 생성) — **sub 실측 ✓**.
5. JCP147 PDF·`jcp_extract.txt`·refs 6/7 dossier 존재 — **sub 실측 ✓**(내용 미검독; 대조 = `Test-Path`). refs 6·7 원문 미소장 — brief·`ch1v22_bib.tex`:46–47 확정(GO 전 대조 = Glob `Claude/**/*121102*`·`Claude/**/*164123*` 0건 확인). dossier "임시 열람 후 삭제" 기록 vs PDF 현 소장 불일치는 **표면화 상태**(R6 DQ-6) — 1.3 에서 기록.
6. 구조 검사 도구 3본 존재 — **sub 실측 ✓**. v1.0.27 새 파일명 동작 여부 **미검증**(4.0 확인; 안 되면 도구 사본을 v1.0.27/results 에 두고 인자 갱신 — 원본 무수정).
7. Python 3.12.10 + numpy/scipy/matplotlib/pandas import OK + **SymPy 1.14.0 설치 확인** — **master 실측 ✓ 2026-09-03**(대조 명령 = `python -c "import sympy,numpy,scipy,matplotlib,pandas;print(sympy.__version__)"`). T-12 의 새 의존성 정지 조건은 해소.
8. git: main = `4069cb3`(이후 master 커밋 `79b4c34`·`82b5b38` = handoff 산출 추가만), tracked 변경 0 — 확정. origin/main 동기·버전 브랜치(v1.0.25.1·v1.0.25-surgical·v1.0.24.1)가 main 의 조상 — **master 실측 ✓ 2026-09-02**(`git merge-base --is-ancestor <branch> main` 전건 YES).
9. **본작업 Fable 5.1 · 조사 Haiku/Sonnet** 배정 — 사용자 명시(brief:45 + 2026-09-03 DR-5·DR-6). 참고 사실(판단 X): v1.0.25 는 Opus 5.0 master 직접 편집 + Opus 4.8·Fable 5.0 서브로 저작됐다(`HANDOVER_v25.md`:48,65, R3 B-12).
10. 부록 E ②항(사용자 논문 내 ref 위치 page·paragraph)은 유보 상태(`ch1_appE_selfconsistent.tex`:120–121) — dossier 는 p.144111-1 Sec. I 우단 2번째 문단·p.144111-4 Eq.(32) 직후를 기록(`PHASE_DIAG_REFS67_DOSSIER.md`:14–17, R6 S-2) → v1.0.27 4.9 에서 JCP147 PDF 로 재대조 확정(DR-8).
11. 이력 문서군 규모 = plans 91(9503줄) + docs/**/PLAN_* 16 + HANDOVER 25(1612줄) + Fable 8(885줄) + CLOSING 106 + INDEX 401 + ledger 30(+docs/vN/results) + 조사 문서군 + v1.0.26 실물 3본 + 서지 원장 4본 — 측정분 ≈ 12,500줄(9,567+1,612+885+106+401 = 12,571 — master 재실측 plans 9,567 기준; PLAN_* 15·ledger 30 미포함) + 미측정분 + 유실 자산 원문 5본(Assumptions 23)(DR-7 비용 근거). 판독 8본이 그중 인계·감사·계획서·조사 문서 약 60본을 1회 정독했다(§2.9). 정독 범위는 DR-7 사용자 확정(핵심 문건 전문 + 세부 계획서·ledger·result 토픽 한정).
12. brief §3-C "plans 90·9567줄·HANDOVER 28(old/ 제외)·1612줄" — **master 재실측 2026-09-03**: plans **92 파일·9,567줄**(날짜 계획서 89 + `INDEX.md` + `MASTER_ROADMAP_*` 2) / HANDOVER **25(old/ 제외)·1,612줄**, old/ 포함 28 / `docs/**/PLAN_*.md` 15. brief 의 "28(old/ 제외)" 은 old/ 포함 건수의 오기, v1 sub 의 91/9,503 은 집계 기준 차이. 1.1 게이트에서 파일명 단위로 정본 고정.
13. **SM2-A/B/C 는 v1.0.22 에서 집행됐다** — **R3·R5 확정**(`ch1_sec06_eqpeak.tex`:74–119·`ch1_sec02b_part0.tex`:387–409·`ch2_sec07_revheat.tex`:74–95 자산 태그). v1 Assumptions 13 "미확정" 을 정정. 1.4 Step 11 에서 실물 재확인.
14. 기존 확보 공개데이터(`results/comp_v24/sintef_data/` 존재 **sub 실측 ✓** · `comp_v26_data/` CSV) 는 2.6·3.1 판정에 재사용 가능 · GITT/p-OCV+hold 신규 다운로드는 DR-6.
15. v1.0.25.1 PDF 페이지 102/30/22 — **master 실측 ✓ 2026-09-02**(pypdf `len(PdfReader(f).pages)` = 102/30/22).
16. `Codex/` 는 어느 Phase 에서도 읽지 않는다 — 규약.
17. **v1.0.26 A/B 는 실행 완료·두 판 산출 상태**이며 미완의 실질은 평형 데이터 재검 미실행 + 사용자 결정 미기록이다 — **R2 확정**(`results/comp_v26_data/README.md`:23–24,46–48·`docs/v1.0.26A-regsol/README.md`:19,162–174). brief §4.3·v1 §2.3 "실행 차단·미완" 정정.
18. Crossref REST API 가 이 환경에서 접근 가능하다 — **R7 실증**(2026-09-03, 84+74 DOI 조회). 계속 사용 여부는 DR-6.
19. 판독 산출 R1~R7 의 path:line 근거는 정확하다 — **미검증(통합·수정 에이전트는 원천 실물을 열지 않음)** → **GO 전 1g 표본 대조 = 각 판독 R1~R7 의 path:line 근거 2건씩(합 16건)을 master 가 Read 로 실물 대조해 Step 1 이력에 기록**(비평 #3); 전건 재대조는 1.1~1.2·2.1~2.5. master 기확인분(2026-09-02~03) = 유실 원문 tex 5본·v1.0.26A/B 폴더·SymPy·xelatex·PDF 페이지·git 위상·plans/HANDOVER 건수(항목 1·5·7·8·12·15·17·23). 판독 간 상충 항목 = 자산 태그 계열·display 집계·P3 #8 건수 3~7(§2.2·§2.4) · **v1.0.26 상태: R5:12·R6:224 "실행 차단·미완" vs R2 §2.10 실물 "두 판 산출 완료·평형 재검 미실행" — R2 실물 근거 우선** · **[MODEL-1 선택] 시점: R6 R-2·DQ-3 "v1.0.15" vs R1 L-04·R3 B-1 "6-30 → v1.0.11" — R1/R3 우선(부록 A DQ-I17)**.
20. "필요한 식만(v7) vs 자기완결 교과서" 긴장은 2026-09-02 기준 1·2 로 자기완결 쪽에서 해소된 것으로 본다 — **사용자 확인됨 — DR-22 "엄격" 선택 = 자기완결 쪽**(R3 DQ-13).
21. 현행 문건의 [C-92]·"∂Ω/∂T 범위 밖"·SM2 축 B "스코프 밖"·[MODEL-1] KWW scope-out 선언은 사용자 결정 기록이 확인되지 않은 서브 판단이다 — **근거 미발견(R3·R5·R6)** → 1.3 Step 9 에서 분류 확정; DR-15·17·18 은 사용자 위임(master 판단 — 3.1/3.7 에서 확정·기록).
22. **신규 예정 파일 전건 부재(GO 전 Glob — 1g "없다/신규 작성" 전제)**: `Claude/plans/2026-09-02-v2-master-plan.md` · `Claude/results/PHASE_1-7_V1027_EXECUTION_LEDGER.md` · `Claude/results/V1027_*.md`(등록부 3종·GAP·BLUEPRINT·인벤토리) · `Claude/results/Step <N> — *.md`(N ≥ 1, 본 arc 명명) · `Claude/results/PHASE_*_V1027_*_RESULT.*` · `Claude/docs/v1.0.27/`(항목 4) — 하나라도 존재하면 STOP → Correction History 재baseline. 근거 = 스킬 1g·§2.8 구조 맵 "신규 예정" 목록.
23. **유실 자산 원문 실물 존재**(1.4 Step 11 (i)·DR-15/16/17 의 전제) = `Claude/old/_archive/graphite_ica_ch1_Fable_v2.tex`(183,693 B)·`…_Fable_v3.tex`(205,225 B)·`…_Opus_v4.tex`(218,389 B)·`…_Opus_v5.tex`(153,592 B)·`…_Opus_v6.tex`(156,166 B) — **master 실측 ✓ 2026-09-03**(비평 #5; 대조 명령 = `ls -l Claude/old/_archive/graphite_ica_ch1_{Fable_v2,Fable_v3,Opus_v4,Opus_v5,Opus_v6}.tex`). 1.1 인벤토리에 이 5본을 등재하고 Step 11 (i) 는 이 경로로 정독한다.
24. **통계역학 부록 D(4.4)의 분량**은 현행 Part 0(sec02a 391 + sec02b 475 = 866줄) + Part T 미시 유도부 + SM2 블록의 **확장**이라 페이지가 크게 는다 — 3.3 Step 42 (vi) 추정 전까지 **미측정**(추정 금지). 사용자 요구 = "더 길고 자세하게, 완전 교과서 수준".

---

## Correction History

- **2026-09-02 v1 초안(작업 sub, Fable 5.1)**: brief(`Claude/results/handoffs/2026-09-02-v2-master-plan/brief.md`) §5 골격을 11-section 으로 확장. 원천 21본 전문 정독 + §3-C 구조 확인 + load-bearing 전제 읽기 전용 실측(자산 카운트 전건 일치·diff 3+3 확정·도구/PDF/JCP/dossier 존재·v1.0.27 부재). brief 와 어긋난 곳(plans/HANDOVER 건수·display 230 집계 정의)은 원천/실측을 따르고 work_log(DQ 17건)에 기록. 결정은 하나도 확정하지 않음(DR-1~9 · DG-A/B/C 는 사용자).
- **2026-09-03 v2 통합(워크플로 integrator, Fable 5.1)**: 판독 8본(R1~R7) 전문 정독 후 반영. **반영한 판독·변경 요지** — (1) Current Ground Truth 정정 3건: v1.0.26 A/B 상태(실행 차단·미완 → A/B 산출 완료·평형 재검 미실행·사용자 결정 미기록, R2 §2.10) · 계보에 v1.0.11 삽입(R1 DQ-3) · v1.0.24 "검증 캠페인" 표현(R2 DQ-4); SM2-A/B/C 집행 확정(R3 B-7·R5 §1.1 — brief §4.5·v1 Assumptions 13 정정); 자산 태그 계열 상충 표면화(v1 실측 vs R3 grep); P3 #1·#6·P5 스테일·P3 #8 base 위반 3~7건(R3 A-3·R4a §5.2·R4b §7.2); orphan `ch1_appD_si`·독립 부록 미편입(R3·R4b); 서지 정량(bibitem 95/distinct 93/cite 265=262+3/키 315/DOI 84/결함 R-01~R-06/V1023 사본/미등재 6/only 4, R7 §1); 판정 정량 표 §2.6 신설(R4a·R4b·R7). (2) **Phase/Step 규모 조정(늘리는 방향만, 1h)**: 챕터 1 Steps 1–10 → 1–13 — 근거 = 세 시드(R1 §5 23·R2 §4 33·R3 B 12절)의 ID 통일·통합 작업 신설(1.4 +1), 수치 불일치 4건·날짜·verbatim 등급 실물 확정 Step 신설(1.2 +2, R1 DQ-2·8·10·R2 DQ-6·7), 정독 대상 추가(v1.0.26 실물 3본·reflect 계획·서지 원장 4본·Fable 02/03, R2 DQ-2·3·R7 §1.2); 챕터 2 Steps 11–24 → 14–32 — 근거 = 9214줄 ≥19 청크(≤500 하한, R4a 12 + R4b 7)·판정 척도 통일 Step 신설(R4a DQ-1·R4b DQ-8)·비박스 결과식 14 및 중복 유도 등재 Step(R4a §2.1·§7·R4b §3·§8.1)·간소화 지점 65 를 두 범위로 분할(R4a §3·R4b §5)·원장 체인 대조 Step(R7 §1.2·R3 DQ-5)·헌법 ① register 잔존 4종 grep 추가(R4b §7.3)·네 판정 상충표 Step(R2 DQ-5); 챕터 3 Steps 25–40 → 33–50 — 근거 = R5·R6 두 카탈로그 통합·경계 정리 Step 신설(R5 DQ-11)·서지 규약 10조항 + 원장 재개설 설계 Step 신설(R7 §5·DQ-2). 챕터 4~6 은 51 부터 연속(3.7 확정 후 세부화) — Phase 목록에 R5·R6 배치 열을 전사. (3) Phase Range 상단 이름공간 주석을 5축으로 고정(R6 DQ-11). (4) Test Plan T-4 정의 고정·T-5 토큰 정의·T-7 register 4종·T-9 한 문헌 한 키·T-15~T-18 신규. (5) Decisions Required: DR-1(v1.0.26 상태 정정 반영)·DR-6(Crossref 기실행 반영·세분 유지)·DR-7(판독 커버리지 반영)·DR-8(dossier vs PDF) 갱신 + **DR-10~DR-22 신설**(regsol 재개방·상분리 부록 편입·D22 supersede/빌드 방식·CLAUDE.md 스테일·P3 #8 게이트 정의·KWW·Eyring·§1.18·[C-92]·서지 원장 재개설·역어·register 규약·판정 하한). (6) 골격(작업 챕터 1~6·Phase ID·게이트 축·Non-goals·운용)은 재설계하지 않았다. 판독 DQ 97건(R1 10 + R2 12 + R3 16 + R4a 10 + R4b 10 + R5 12 + R6 12 + R7 15) + v1 work_log DQ 17 = 114건은 각각 DR 승격 / Phase Step 흡수 / 부록 A Decision Queue 이관으로 처리하고 처리표를 부록 A 에 두었다.
- **2026-09-03 v3(워크플로 fixer, Fable 5.1)**: 검수 sub 감사 발견 55건 반영 — SPEC-01·02·03·04·05·06·07·08·09·10·11·12·13 · FORMAT-01·02·03·04·05·06·07·08·09·10·11·12·13·14·15·16·17·18·19·20·21·22 · LOGIC-01·02·03·04·05·06·07·08·09·10·11·12·13·14·15·16·17·18·19·20(전건 반영; 반영 방식의 이견·부분 반영 4건 = SPEC-04 수치 정정(8·13)·LOGIC-02 접두 규약 방식·LOGIC-10 v1 참조 정의 방식·FORMAT-01 Result 편입 방식 — `fix_change_log.md`). 골격(작업 챕터 1~6·Phase ID·Step 번호 1–50·게이트 축·Non-goals 골자·운용)은 불변; 변경 = 매 Phase Result 편입(Step 수 불변)·DR-7/DR-6/DR-9 문안·DR-23 신설·T-19~T-21 신설·산출물 ID `OUT-` 재명명·수치 정정(36/36·57/57·15·23단·64 분포·97+17=114·3,428/2,130/3,324·23=8+13 등)·1.4 Step 11 (i) 유실 자산 원문 정독·2.2 작업 sub 정독 단 명시·11-section 밖 절을 부록 A~C 로 격하. cumulative step 1–50 단조성·11-section 순서 재검산 완료(부록 A DQ-I13).
- **2026-09-03 v4 최종본(master, Fable 5.1)**: v3 를 전문 정독하고 감사 3본·수정 로그·완결성 비평(14건)을 삼각검증한 뒤 직접 반영 — HIGH #1(R6 후보 `T-1`/`T-2` 를 본문 전건 `R6:T-1`·`R6:T-2` 로 접두 + 이름공간 표에 Test Plan ID·D-계열 행) · MED #2(4.x boxed 회수 게이트 = Step 41 매핑표 기준·4.6 이관 문면) · #3(Assumptions 19 GO 전 표본 대조 16건) · #4(F-01 재판정 → 2.5 Step 27·게이트 1.3 이관 표기) · #5(유실 원문 tex 5본 실물 = Assumptions 23·Step 11 (i) 경로 확정) · LOW #6~#14 전건(DR-16 S0–S5 부기·Step 3/4 행 22/9·≈12,500줄·Assumptions 1/5/7/8/12/15 대조 명령·실측 갱신·T-20 연습문제 N/A·key finding 4건 Step 배정·1.5/3.7 중단 조건·DR-6 승계/재조회 선택지·D-계열 이름공간). master 실측(2026-09-02~03) = origin/main 동기·버전 브랜치 main 조상·PDF 102/30/22·xelatex 존재·Python 3.12.10·SymPy 1.14.0·v1.0.26A/B 폴더·유실 원문 tex 5본·plans 92파일/9,567줄·HANDOVER 25/1,612(old/ 제외; brief 의 28 은 old/ 포함 수치)·PLAN_* 15·신규 예정 파일 전건 부재·`Step *` 0건. DQ-I2(Step 40→50)·DQ-I14(매 Phase Result)·DQ-I15(유실 원문 정독 확장) = master 승인 · DQ-I16 = 승인 출처 기재. 11-section 밖 부록 A~C 는 `wf/plan_v3_appendix_ABC.md` 로 분리(FORMAT-12). 골격·Step 1–50·DR-1~23 불변.
- **2026-09-03 v5 재baseline(master, Fable 5.1 — 사용자 결정 DR-1~23 + 신규 요구 반영, 스킬 1j "중대" 편입 · 기존 계획서에 편입·삭제 없음)**: 목표 라벨 v2.0.0 → **v1.0.27**(DR-2 순차 번호; 파일 접두 V2_/PHASE_*_V2_/HANDOVER_v2.0.0/-v2-phase- → V1027_/…/HANDOVER_v1.0.27/-v1027-phase-) · 진단 대상 = v1.0.25·v1.0.25.1·v1.0.26A/B(DR-1 A+B) · **구조 확정**(DR-3·11·12·신규 요구): 재료별 3장 유지·분리 빌드+xr·Ch1 흑연 = 이론 집중 + **후반부 부록 D = 통계역학 전체(교과서급, 비전공자 가독)** + 상분리 편입(DR-11 master 판단)·Ch2 LCO/Ch3 Si·블렌드 = Ch1 에 없는 분기만(음극 예측 강화) — 3.3 을 "두 안 비교" 에서 "확정 구조의 내부 배열안" 으로, 4.x 를 Ch1-중심(4.1 평형 열역학·4.2 동역학·4.3 열특성·히스·4.4 부록 D 통계역학·4.5 기타 부록·4.6 LCO 분기·4.7 Si·블렌드 분기·4.8 3장 정합·4.9 챕터 Result)으로 재편(Phase 수 10 유지) · DG-A/DG-C 사용자 기확정·DG-B master 위임(DR-11·15·16·17·18·23) → **3.7 정지 → 비차단 보고점**(DR-9) · **코드 = 문건 밖**(DR-10·14: 코드맵·코드 절·부록 E 대응 지도 → OUT-CODEDOC; T-5 전 tex 0) · **작업 챕터 7 코드 동기(doc-leads) 신설**(DR-4·9; OUT-CODEDOC·OUT-CODE 행) · 정독 범위 = 핵심 문건 전문 + 세부 계획서·ledger·result 토픽 한정(DR-7 — 1.1 목적·Step 2·1.2 Step 3/4·§2.9·Assumptions 11 갱신) · 모델 = 본작업 Fable 5.1·조사 Haiku/Sonnet 서브 carve-out(DR-5·6) · 외부 논문·데이터 즉시 확보 허용(DR-6) · 유연성(DR-9: Phase/Step 추가 가능·삭제 불가 — Interfaces) · 용어 = 문장 골조 한글·학술 용어 영어 원어(DR-20 — T-6·4.0 용어표·문체) · **tier 표기 폐지**(DR-21 — T-7·6.2·Non-goals) · 유도 완결 하한 엄격(DR-22 — Assumptions 20) · 검수 등급 = BLUEPRINT 고가치·등록부/GAP 통상(DR-23 위임 확정) · 서지 = 전문 리뷰 논문 포맷(DR-19 — 5.1·T-9) · refs 6/7 = 리포 내 JCP147 PDF·jcp_extract·dossier·부록 E 로 자족, 원문 미소장(Glob `*121102*`·`*164123*` 0건 재확인, DR-8) · 신규 사본 작업 원칙(DR-13). master 판단 기록: DR-11 편입 / DR-15 일반형·ρ=δ 회수 본문·파라미터화 opt-in / DR-16 회복(K-1) / DR-17 v4 원문 정독 후 설명층·부록화 중 택1(3.1) / DR-18 부분 해제 / DR-23 기본. 삭제한 Phase·Step·게이트 없음(3.3·3.7·4.x 는 내용 갱신·번호 유지).
- **2026-09-03 v5.1(master)**: 사용자 추가 지시 "예제같은 풀어야할 문제같은건 넣지 말자" 반영 — T-20 예제·연습문제 = 제외, 4.4 부록 D·3.3 Step 42 (i)의 예제 요건 삭제, 7.3 "문건 예제 수치" → "수치 검산값(verifybox)", Non-goals·확정표 신규-2 추가. 골격·Step·게이트 수 불변.
- **2026-09-03 v5.2(master)**: 사용자 명확화 "이 문건은 논리 전개가 주고, 독자 참여형 섹션 … 하지 않게" — 예제·연습문제에 더해 독자 지시형 박스(verifybox 류)도 제외, 저자 수행 확인은 논리 전개 서술로(T-20·4.0·4.4·3.3·7.3·Non-goals·확정표 신규-2). 사용자 GO("쭉 진행할것") 접수 — 본 v5.2 가 실행 기준 정본. **GO 직전 1g 실물 대조(2026-09-03 09:24, 기록 = handoffs/…/wf/go_1g_check_2026-09-03.txt)**: Assumptions 1·2·3·4·5·6·7·8·15·17·22·23 전건 참(xelatex 존재·60 tex/9214줄·diff 10 파일 = sections 3+masters 3+ARCHIVE_NOTE+PDF 3·v1.0.27 부재·JCP 3/3·refs67 원문 0건·도구 3/3·Python 3.12.10/SymPy 1.14.0·HEAD 8d9362f tracked 0·PDF 102/30/22·v1.0.26A/B 2/2·신규 예정 파일 전건 부재·유실 원문 5/5). **정정 1건 — Assumptions 14**: comp_v26_data/ 에 CSV 0건(v1.0.26 실측 CSV 는 세션 스크래치에만 있었고 미보존 — HANDOVER_v25 N6) → 기확보 데이터 = results/comp_v24/sintef_data/ CSV 3본만; v1.0.26 수치는 README·params 기록으로만 사용(2.6 Step 30 (e) 반영). 규모 재실측: plans 93파일/10,383줄(본 계획서 포함).

---

## Decisions Required

> **확정 기록(사용자 2026-09-03).** 아래 원문 DR-1~23 은 제안 시점 문안(기록용·무수정 보존)이며, 실행 규칙은 이 표와 본문 v5 반영분이 정본이다. DG-A(구조)·DG-C(라벨)는 확정, DG-B(채택 이론)는 master 위임(3.7 보고).

| DR | 사용자 결정(요지 · 큰따옴표 = verbatim) | 계획 반영 위치 |
|---|---|---|
| 1 | 대상 = "1.0.25~1.0.26 과 그 파생 버전들" → A+B | Summary·2.1 Step 15·Phase Range 2.1 |
| 2 | "1.0.27 버전으로 명명" — "순서대로 버전 숫자를 수정하고 있는건 지켜야한다" | 전 문서 v1.0.27·V1027_ 접두 |
| 3 | 소재별 3문건 구조 유지 · "챕터 1은 흑연이어야하고, 대부분의 논리, 이론은 여기 집중작성" · Ch2/3 = "챕터1 에 없던 내용을 분기로" · "흑연이랑 실리콘을 좀 제대로 예측" | Phase Range 이름공간·3.3·4.x 재편 |
| 4 | 코드는 "이론이 완성되면 따라오는거니까. 후순위" | 작업 챕터 7 |
| 5 | "직렬기본" · 논문 조사는 "하이쿠/소넷 서브 세션을 별도 운용" 허용 | Interfaces 모델·유닛 |
| 6 | 외부 논문·데이터 "필요시 바로 찾아서 써도 된다" · 조사 = "하이쿠, 소넷을 쓰는 것을 기본 골조" | Non-goals·Interfaces·T-9 |
| 7 | 정독 = "토픽이 있는곳만 제한적으로 한정하여 정독" | 1.1 목적·Step 2·1.2 Step 3/4·§2.9·Assumptions 11 |
| 8 | 이전 조사 이력·논문 제공됨 → 리포 내 `JCP_147(14)_144111_(2017)…pdf`·`jcp_extract.txt`(724줄)·`PHASE_DIAG_REFS67_DOSSIER.md`·부록 E 를 입력으로 사용; refs 6·7(2011·2013 JCP) 원문 파일은 리포·`_local_only/` 에 없음(Glob 0건) → 자족 경로, 제공 시 4.5 에서 대조 | 4.5·Assumptions 5·10 |
| 9 | "챕터 전체를 쭉 이어진행" · 마스터플랜 = "절대 헌법" · 신규 Phase/Step 추가 허용 · "있던걸 없애는건 안됨" · 코드 동기 챕터 추가 | 3.7 보고점·Interfaces 유연성·챕터 7 |
| 10 | 코드·이론 별개 · "코드에 대한 내용, 언급은 본문에서는 없어야됨" · 이전 코드·산출물 문제점은 유도 동기로만, "참고는 하되 언급은하지 않을것" | Summary 정직 프레임·T-5·Non-goals |
| 11 | master 판단 → 상분리 독립 부록 **편입**(본문 결과 + 부록 유도) | 3.3 Step 42 (iii)·4.1 |
| 12 | "분리 빌드 우선"(병합은 완성 후) | 3.3 Step 43·4.8·Phase Range |
| 13 | "신규 사본을 만들어서 하던가 아니면 아예 처음부터 새로 작성" · 이전 산출물은 기록용 | Non-goals·OUT-DOC |
| 14 | "코드는 그냥 따로 빼 아예 따로빼" → 코드 = 문건 밖 | OUT-CODEDOC·T-5·4.0·4.5 |
| 15 | (질문에 답) KWW = 꼬리 완화를 단일 지수가 아니라 장벽(활성화 에너지) 분포로 일반화한 stretched-exponential 꼴 → master 판단: 일반형·ρ=δ 회수는 Ch1 본문, 파라미터화는 opt-in | 4.2 |
| 16 | master 판단 → Eyring/TST 척추 **회복**(K-1) | 4.2 |
| 17 | master 판단 → 3.1 에서 Opus v4 §1.18 원문 정독 후 설명층 채택 / 부록화 중 택1(영구 배제 X) | 4.3 |
| 18 | master 판단 → [C-92] 부분 해제(완전 cycle 소산은 범위 안·경로의존·Jarzynski 밖) | 4.3 |
| 19 | "전문 리뷰 논문의 그것과 포맷을 맞춰줘" | 3.5·5.1·T-9 |
| 20 | "한국 학술용어를 존중" · "일본식, 중국식은 피해줘" · "학술 단어들은 영문으로" · "문장의 구조 전체는 한글" | 4.0 용어표·T-6·Interfaces 문체·Non-goals |
| 21 | "티어를 왜써" → tier 표기 폐지 | T-7·6.2·Non-goals |
| 22 | "엄격" | 2.2 Step 16·Assumptions 20 |
| 23 | master 판단 → BLUEPRINT 고가치(10R + 렌즈 6종)·등록부/GAP 통상 | Interfaces 검수 강도 |
| 신규-2 | "아무리 교과서 약식이라곤 해도 예제같은 풀어야할 문제같은건 넣지 말자" → 독자 참여형 섹션(예제·연습문제·풀어보기·독자 지시형 박스) 제외; 저자 수행 확인은 논리 전개로 서술("검산이 뭘 의미하는지 모르겠는데 이 문건은 논리 전개가 주") | T-20·4.0·4.4·3.3 Step 42·7.3·Non-goals |
| 신규 | "통계역학 부분은 전체를 따로 챕터1의 후반부의 부록으로 빼버리고, 부록 답게 더 길고 자세하게 완전 교과서 수준의 상세한 내용으로 개편" — 비전공자·타전공자 가독 | 3.3 Step 42 (i)·4.4·T-21·Assumptions 24 |

> (아래 = 제안 시점 원문. 각 항목 = 실제 내용 · 근거 · 기본값 · 한 줄 응답 선택지 — 기록용.)

- **DR-1 — "1.0.25 두 가지 버전" 의 해석.**
  - 내용: 사용자 발화 "현재의 가장 1.0.25 두 가지 버전" 을 (A) `docs/v1.0.25/`(base, 무수정 보존) + `docs/v1.0.25.1/`(검증 + touch-up 4건, 현행 최신)로 읽는다. 실물 차이 = `_sections` 3파일(sifr 2 hunk·width·eqpeak) + 마스터 3(표시 버전) + ARCHIVE_NOTE + PDF(sub 실측 hash·R4a·R4b diff). 대안 (B) = v1.0.26 A/B 두 산출(A regsol-4 물리 4전이 vs B logistic-7 gallery 7전이 — main HEAD 커밋 제목)로 읽는다.
  - 근거: (A) 는 `docs/INDEX.md`:7–14 의 "현행 최신 v1.0.25.1 / base v1.0.25" 구분과 일치. (B) 는 HEAD 커밋 제목이며 **판독 정정**에 따르면 v1.0.26 은 "실행 차단·미완" 이 아니라 두 판 산출 완료·평형 재검 미실행 상태(R2 §2.10)라 (B) 해석의 실물 근거가 v1 초안 시점보다 강해졌다. 그러나 v1.0.26 은 tex 리비전이 아니라 판정용 실측 조사(문건 무변경)다.
  - 기본값: **(A)**. 어느 쪽이든 regsol 미결은 2.6/3.1/DG-B 로 흡수되며, (B) 또는 (A+B) 채택 시 2.1 Step 15 에서 v1.0.26 자산 지도를 추가한다.
  - 응답 선택지: `DR-1: A` / `DR-1: B` / `DR-1: A+B(둘 다 자산 지도에 포함)`.

- **DR-2 — 목표 버전 라벨·폴더.**
  - 내용: 새 문건의 라벨과 폴더. 기본 = **v1.0.27**, `Claude/docs/v1.0.27/`(일반→특수 재구조 = major). 대안 = v1.1.0.
  - 근거: 3.3 (b) 채택 시 구조가 바뀌므로 semantic major 가 자연스럽다(master 판단·brief §8). v1.0.x 계보의 "국소 수정 = patch"·"2-버전 = 폴더명 접미" 관행(v1.0.18.1/.2·v1.0.24.1·v1.0.25.1, R1 §4·R2 DQ-9)과 구분된다. 마스터 tex 파일명·xr 키는 DG-2(v1.0.25 한정) 규약에서 풀리므로 4.0 에서 새로 정한다(DG-C 에서 재확인).
  - 기본값: **v1.0.27**.
  - 응답 선택지: `DR-2: v1.0.27` / `DR-2: v1.1.0` / `DR-2: 기타 <라벨>`.

- **DR-3 — 문건 구조(사전 선호만 · 결정은 3.7).**
  - 내용: (a) 현행 재료별 3장 유지 + 내부 일반화 vs (b) Part I 일반 이론(열역학·통계역학·동역학·열·히스테리시스) + Part II 재료 적용(흑연·LCO·Si·블렌드). 3.3 이 두 안의 장단·자산 이동 맵·xr 영향·페이지 추정·D22 supersede 문안을 산출한 뒤 **3.7 에서 정지해 DG-A 로 결정**한다.
  - 근거(master 사전 선호 = (b), brief §8): 사용자 기준 5 와 CLAUDE.md P1 원구상(Chapter 1 전하보존 → 2~5 발열·반응속도론·통합 상태방정식·히스테리시스)이 "이론 층 → 적용 층" 과 정합. 판독이 더한 지지 근거 = 같은 유도의 다중 수록 3계열(정칙용액 커널 3곳·Sommerfeld 2곳·spinodal 3곳)이 (b) 에서 사라짐(R4b §8.1 판단) · 원구상 Chapter 2~5 의 내용은 현행에 있으나 계층 순서로 배열돼 있지 않음(R6 §2 추정) · A 등급 후보(TH-1.1·2.1·5.1·K-1·T-1)의 배치가 Part I 일반 절을 전제(R5 §4·R6 §7). 반대 근거 = v1.0.22 사용자 확정 D22 "활물질별 재편" 을 되돌리는 결정이며(R3 DQ-3, DR-12) 침습도·페이지 증가가 크다.
  - 기본값: 지금은 **선호 기록만**((b)). 3.3 산출 없이는 결정하지 않는다.
  - 응답 선택지: `DR-3: (b) 선호 확인` / `DR-3: (a) 선호` / `DR-3: 3.7 까지 유보`.

- **DR-4 — 코드 동기 = 별도 후속 플랜.**
  - 내용: 본 계획은 문건만. 코드 `Anode_Fit_v1.0.24.py`(release 1.0.25)·조사 코드·`CODE_GUIDE_v24`·`FITTING_GUIDE`(미갱신 R2:P-14)는 수정하지 않고 v1.0.27 문건 확정 후 별도 doc-leads 동기 플랜에서 다룬다. 기존 코드의 **읽기·게이트 실행(수치 대조 목적)** 은 허용(T-12).
  - 근거: doc-leads 규약(문건이 authoritative, `docs/INDEX.md`:67) · 게이트 4종 GREEN·골든 bit-exact 계약(A4)을 문건 저작 중에 흔들지 않기 위함. v1.0.26 조사 코드 `regsol_kernel.py` 는 TH-2.1 평가의 선행 데이터로만 쓴다(R2 DQ-5).
  - 기본값: **별도 플랜**.
  - 응답 선택지: `DR-4: 별도` / `DR-4: 본 계획에 코드 챕터 추가(범위 확장 — 계획서 정정 필요)`.

- **DR-5 — 병렬(fan-out) sign-off.**
  - 내용: 기본은 직렬(유닛 1개·동시 산 서브 ≤1). 옵션 = (i) 챕터 2.2~2.5 진단 청크 병렬(예: 2.2 Step 17~19 를 3 유닛 동시) (ii) 챕터 4.x 저작 파트 병렬(4.1~4.5 이론 파트 vs 4.6~4.8 적용 파트). 비용 = 유닛 수 × Fable 5.1 세션 + master 통합·삼각검증 부하 증가(구체 수치는 원천에 없어 제시하지 않음). 병렬이라도 shared mutable state(같은 `_sections` 파일·ledger·원장 json)는 직렬화한다. 참고: 판독 단계에서 8 에이전트 병렬이 이미 한 번 쓰였고 그 산출이 본 초안의 시드다(그 병렬의 승인 출처는 본 문서 원천에 기록 없음 — 근거 미발견, 부록 A DQ-I16) — 같은 방식이 2.2~2.5 에도 유효하다는 것이 [integrator 판단]이나 승인은 사용자 몫.
  - 근거: 헌법 §1-병렬(자의 fan-out 금지·sign-off 만이 승인). 사용자 기준 6(효율 < 완성도).
  - 기본값: **직렬**.
  - 응답 선택지: `DR-5: 직렬` / `DR-5: (i) 승인` / `DR-5: (ii) 승인` / `DR-5: (i)+(ii)`.

- **DR-6 — 외부 접근.**
  - 내용: (i) 문헌 검색(3.1 Step 35·챕터 5) (ii) DOI 검증 Crossref 조회(2.4·3.5·5.1) (iii) 공개데이터 재다운로드(2.6 — SINTEF Zenodo 20086298 GITT/p-OCV+hold `dl_sintef.ps1`; 기확보 CSV 는 별개로 재사용). **판독 단계에서 (ii) 가 이미 실행됐다**(R7: 2026-09-03 Crossref 84+74 DOI 조회, 응답은 세션 스크래치·json 부본) — 그 결과를 승계할지, 본 arc 에서 재조회할지도 이 결정에 포함된다. 기본 = **읽기 전용 허용**(다운로드 파일은 `Claude/results/` 하위·`SOURCES.md` 관행대로 출처 기록·`refcheck/` 응답 보존). 불허 시 해당 게이트는 "미검증" 으로 정직 표기하고 진행.
  - 근거: 사용자 기준 3(리뷰급 레퍼런스)은 DOI 검증 없이는 충족을 주장할 수 없다(헌법 ②). 데이터는 A7·R2:R-1 이 GITT 평형 데이터 필요를 확정. 서적 11건은 Crossref 로 확인 불가(R7 DQ-9 — DR-19 연동).
  - 기본값: **brief §8 그대로 = (i)(ii)(iii) 전부 읽기 전용 허용** · R7 조회 결과 승계(재조회는 결함 항목 R-01~R-06 만) · (iii) 불허 시 2.6 은 기확보 CSV 만으로 정식화하고 신규 다운로드 필요는 DQ 기록(정지 아님). v2 가 (iii) 를 "2.6 진입 시 재확인" 으로 쪼갰던 것(v1 작업 sub 제안 유지)은 3.7 외 중간 확인 지점을 만들어 정지 조건 목록·세 선택지와 어긋나므로 brief 기본값으로 환원했다(감사 SPEC-10·FORMAT-15·LOGIC-19).
  - 응답 선택지: `DR-6: 전부 허용(R7 조회 결과 승계·결함 6건만 재조회)` / `DR-6: 전부 허용(전건 재조회)` / `DR-6: (i)(ii) 만` / `DR-6: 불허`.

- **DR-7 — 이력 정독 범위와 판독 기정독분의 취급.**
  - 내용: 대상 = plans 91(+docs/**/PLAN_* 16)·HANDOVER 25(또는 28 — 1.1 정본화)·Fable 8·CLOSING·INDEX·ledger 30(+docs/vN/results)·조사 문서군·v1.0.26 실물 3본·서지 원장 4본·유실 자산 원문 4건(1.4 Step 11 (i)). 판독 8본이 그중 약 60본(인계 전건·감사 6·CLOSING·서베이 전건·계획서 8·v1.0.26 실물·원장·dossier)을 1회 정독했다(§2.9). 선택지 세 가지 — **(i) 전부: 기정독분 포함 본 arc 작업 sub 가 전건 신규 전문 정독**(판독 커버리지는 참조 열·Read Coverage 미계수·검수 sub 는 근거 행 대조로 cross-check) / (ii) 기정독분은 검수 sub 근거 행 대조로 대체하고 잔여(plans 83·PLAN_* 16·ledger 30+·results 문서군)만 신규 정독 / (iii) 마스터플랜·인계·감사·CLOSING 전문 + 페이즈 세부 계획서(docs/**/PLAN_*·`*-P1~P8-*`·`*-phaseR*-*` 류)는 구조 추출(Phase 표·게이트·결정만).
  - 근거: 사용자 기준 6 "효율이 아닌 결과물의 완성도 신뢰도" · brief:138 1.1 게이트 "전문 정독 = 전부 — 효율 이유로 축약하지 않음" · brief:4 "요약을 믿지 말고 원천을 직접 Read" · CLOSING 2-1/2-2 · F-11 "이력 무시" 지적. (ii)·(iii) 는 비용을 줄이지만 (ii) 는 arc 안에서 head→tail 정독이 0 인 파일(약 60본)을 만들고, (iii) 는 세부 계획서 안의 결정·게이트 이력 누락 위험이 있다. 판독이 확인한 미집행·근거 미발견 항목(V-계획·Campaign A·LIT ★군·D1~D7 응답)은 바로 그 세부 계획서·ledger 안에 있을 가능성이 크다[integrator 판단]. v2 는 라벨 "전부" 아래 실제 규칙을 (ii) 로 적어 하한을 가렸다(감사 SPEC-02·FORMAT-02·LOGIC-01) — v3 는 라벨과 규칙을 일치시켰다.
  - 기본값: **(i) 전부(기정독분 포함 신규 전문 정독)** — 비용 = 측정분 ≈ 12,500줄 + 미측정분 + 유실 자산 원문 5본(Assumptions 23). (ii) 채택 시에도 등록부 확정 근거 파일(§2.0 A1~A14·B1~B7 + v1.0.26 실물 3본 + 서지 원장 4본)은 전문 정독 필수 집합으로 고정한다.
  - 응답 선택지: `DR-7: (i) 전부` / `DR-7: (ii) 기정독분 검수 대조 대체` / `DR-7: (iii) 구조 추출`.

- **DR-8 — refs 6·7 원문 제공 여부와 ② 위치 확정 근거.**
  - 내용: CLAUDE.md P1 은 refs 6/7 방법론을 "실제 확인한 뒤" 반영하라고 요구한다. 현행 = JCP147 자족 + dossier + 부록 E 5항으로 이행, refs 6·7 원문(`lee2011jcp`·`son2013jcp`) 미소장. 판독이 더한 사실: dossier 는 ② 위치를 page·paragraph 로 기록했으나 "임시 열람 후 삭제" 표기(dossier:3)이고, JCP147 PDF 는 현재 `Claude/` 에 소장(brief §4.1) → 부록 E ② "페이지·문단 세부 유보" 는 **소장 PDF 재대조로 본 arc 안에서 닫을 수 있다**(R6 DQ-6·R4a DQ-6). 기본 = JCP147 PDF 재대조로 ② 확정 + dossier 교차 근거 + Crossref 서지 확정 + refs 6·7 "원문 미소장" 정직 표기. 대안 = 사용자가 refs 6·7 원문 PDF 를 `Claude/` 에 제공 → 4.9 에서 원 유도(Fredholm 2종 ratio 구조) 대조·⑤ 가정 차 재검증.
  - 근거: B6:43·A14:120–121·dossier:14–17. R7 DQ-8 도 동일 결정을 요구.
  - 기본값: **자족 + PDF 재대조 + 정직 표기**.
  - 응답 선택지: `DR-8: 자족` / `DR-8: 원문 제공 예정(경로 <…>)`.

- **DR-9 — GO 범위.**
  - 내용: 기본 = 작업 챕터 1 → 2 → 3 연속 진행 후 3.7 에서 정지(DG-A/B/C). 대안 = 챕터 1 만 먼저(1.5 Result 후 정지·재GO).
  - 근거: 챕터 1~3 은 조사·설계라 파괴·비가역 작업이 없고, **사용자만 결정 가능한 blocking 정지는 3.7 하나**다(그 밖의 일반 정지 조건 — 1.3 통제문서 모순·SymPy 부재 등 새 의존성·confirmed FAIL — 은 Implementation Interfaces 정지 조건 목록대로 별도 적용된다). 판독 시드가 있어도 챕터 1 등록부는 arc 내 신규 전문 정독 위에 선다(DR-7 (i)); 챕터 1 결과를 먼저 보고 싶으면 대안.
  - 기본값: **1→2→3 연속, 3.7 정지**.
  - 응답 선택지: `DR-9: 1→2→3` / `DR-9: 챕터 1 만`.


- **DR-10 — regsol(정칙용액+Maxwell) 재개방의 결정 구조: 코드 결정 DG-1 과 문건 이론 채택의 분리.**
  - 내용: v1.0.25 사용자 verbatim "regsol 삭제"(DG-1)는 코드 커널 삭제 결정이고, v1.0.26 사용자 verbatim "두상으로 분리되는 걸 표현하려면 regsol이 들어가야 한다."·"그 결과를 이미지로 확인하고 나서 정할려니까."(`HANDOVER_regsol_investigation.md`:12–13)는 되살리기 결정을 **사용자 자신이 열어 둔** 상태이며 결정 기록은 없다. 판독은 (a) 문건 이론으로서 정칙용액+Maxwell 두-상 dQ/dV 사슬(TH-2.1)은 A 등급이고, (b) dQ/dV **커널** 채택은 v1.0.26 A/B 판정("regsol-4 가 gallery-7 을 대체 = 거짓·흑연 Ω≈2RT = 참·skew-logistic-7 최선")과 평형 데이터 재검에 종속된다고 분리했다(R5 DQ-2·R6 DQ-4·R3 DQ-7). 결정 사항 = ① "DG-1 은 코드 결정이며 문건 일반 이론에 정칙용액+Maxwell 을 적는 것은 별개" 임을 확인할지 ② 커널 채택(소재별: 흑연 = regsol+유한 δ 검토 / Si = Frumkin 고용체 / 블렌드 중첩)과 v1.0.26 skew-logistic-7 발견의 문건 반영을 지금 결정할지 3.7 DG-B 로 미룰지 ③ 평형 데이터 재검(DR-6 (iii))을 본 arc 에서 실행할지.
  - 근거: `HANDOVER_v25.md`:46·85–89·136–137 · `docs/v1.0.26A-regsol/README.md`:19,134–143,162–174 · `docs/v1.0.26B-gallery/README.md`:16–18 · brief §4.4 "Ω 물리 전량 유효".
  - 기본값: ① 확인(분리) · ② 3.7 DG-B 로 이관(2.6 정식화 결과와 함께) · ③ DR-6 응답에 따름.
  - 응답 선택지: `DR-10: 분리 확인·DG-B 이관` / `DR-10: 지금 결정 — 커널 <채택/불채택/소재별 …>` / `DR-10: 평형 재검 먼저 실행`.

- **DR-11 — 상분리 독립 부록(`appendix_phase_separation.tex`)의 본문 편입.**
  - 내용: v1.0.14 에서 사용자가 "spinodal 부록은 별도 문건으로 그냥 놔두자"(인계 문건 요지 표기, `HANDOVER_v1.0.14.md`:15 — verbatim 보증 없음)로 별도 유지를 결정했고, 부록 자체(`:7`)와 v1.0.19 인계(:35)는 "편입 여부는 사용자 검토 후 결정" 으로 남겨 두었다. 판독은 이 부록이 스코프 내 유일한 완전 "일반→특수" 유도(eq:app-fxi)이자 binodal·spinodal·Maxwell·CNT·Cahn–Hilliard 의 정본 후보이며, TH-2.1·TH-5.2·H-1·H-2 가 이 부록의 식에 매달리므로 (b) 구조에서는 Part I 상분리 절로 승격(TH-5.1 A)하는 것이 자연스럽다고 판정했다(R4b DQ-2·R5 TH-5.1·R6 DQ-1). 편입 시 작업 = ξ↔θ 배향 통일·Ω 정의식 통일·[A1]~[A5] V1 키화·keybox 구현 통일·spinodal 정본 1곳.
  - 근거: `appendix_phase_separation.tex`:7–13,100–102 · `ch1_sec04_hys.tex`:254–255 · `results/INDEX_v25.md`:35.
  - 기본값: **DG-A 에서 (b) 채택 시 편입, (a) 시 독립 유지 + 본문 참조 강화** — 즉 3.7 로 이관하되 사전 선호는 편입.
  - 응답 선택지: `DR-11: 편입(사전 확정)` / `DR-11: 독립 유지` / `DR-11: 3.7 에서 결정`.

- **DR-12 — v1.0.22 사용자 확정 D22 "활물질별 재편" 의 supersede 와 빌드 방식.**
  - 내용: brief 3.3 (b) 안은 D22-1~8(`docs/v1.0.21/HANDOVER_v1.0.21.md`:18·`plans/2026-07-17-v1022-master-plan.md`:3) 가운데 "활물질별 3챕터 재편" 을 되돌리는 구조다. 또 D22-8 "병합 빌드 금지·3장 분리+xr" 을 v1.0.27 에도 적용할지(단일 문서 vs 분리 빌드 + xr)가 자산 이동·라벨·원장(장별 bib vs 통합 bib, R7 DQ-6) 설계를 가른다. 판독은 DG-A 에 "D22 를 supersede 한다" 문안을 사용자 결정 항목으로 포함해야 한다고 봤다(R3 DQ-3).
  - 근거: R3 A-6 · `plans/2026-07-18-v1023-…-plan.md`:72 · `HANDOVER_v1.0.22.md`:124–129(병합 이관 5항 착수 근거 미발견).
  - 기본값: **3.7 DG-A 에서 함께 결정**(지금은 인지만). 빌드 방식의 사전 선호는 두지 않는다 — 3.3 Step 42 가 xr 영향·페이지·원장 방식과 함께 옵션을 낸다.
  - 응답 선택지: `DR-12: DG-A 에서 함께` / `DR-12: D22 유지(재료별 구조 고정 = (a))` / `DR-12: 단일 문서 사전 확정` / `DR-12: 분리 빌드+xr 사전 확정`.

- **DR-13 — CLAUDE.md 스테일 조항의 처리.**
  - 내용: `CLAUDE.md` P1 원구상 "Chapter 1~5"·P3 #1 네 기호(`V_{n,app}`·`V_{n,drive}`·`V_{n,OCV}` — 현행 0건, 현행 = `V_app`·`V_n`)·P3 #6·P5 둘째·셋째 조항의 `ver.N` 절(현행 0건)은 v1.0.22 재편 이전 표기다(R3 A-3). 본 계획은 이를 **현행 기호·구조로 재해석해 승계**(T-13)하고 CLAUDE.md 원문은 건드리지 않는다. 결정 사항 = CLAUDE.md 개정을 (a) 6.3 마감 시 개정안 문서(OUT-CLAUDEMD)로 제출만 할지 (b) GO 시점에 사용자가 직접 개정할지 (c) 개정 없이 재해석만으로 갈지.
  - 근거: `CLAUDE.md`:13–17,34,44,63–67 · R3 DQ-2·DQ-4 · P3 #8 도 v1.0.24 이후 추가된 선례(:46).
  - 기본값: **(a) 개정안 문서 제출·원문 무수정**.
  - 응답 선택지: `DR-13: 개정안 제출` / `DR-13: 사용자 직접 개정` / `DR-13: 재해석만`.

- **DR-14 — P3 #8 "코드 = 부록 전용" 게이트의 정의(판정 단위·토큰 범위).**
  - 내용: 게이트 문면 "부록 아닌 `_sections/*.tex` grep 코드토큰 = 0" 은 (i) 판정 단위가 파일명(`sec05` = 본문)인지 조립(`\appendix` 뒤 = 부록)인지, (ii) 토큰 범위에 진단 스크립트명(`regsol2`·`regsol_si`)·문서 파일명(`\texttt{V1025_DATA_ADDENDUM.md}`)·상수 함수명(`use_si_constants()`)을 넣을지에 따라 현행 위반 수가 3~7 로 달라진다(R3 B-12·R4a §5.2·R4b §7.1–7.2). §3.5 코드절은 조립상 부록이나 파일명·라벨·본문 참조 6곳이 본문 표기(3중 불일치).
  - 근거: `CLAUDE.md`:46 · `ch3_si_v1.0.24.tex`:30–31 · `ch2_appB_codemap.tex`:10–11("함수명은 부록에만").
  - 기본값: **조립 단위(부록 아닌 절) + 토큰 범위 = 코드 식별자·스크립트명·문서 파일명 전부(넓게)** · v2 에서 §3.5 부록 명명 정합화·eq:si-code-bitexact 식별자는 부록 표로 이동 · base 는 무수정·GAP 등재.
  - 응답 선택지: `DR-14: 조립 단위·넓은 토큰(기본)` / `DR-14: 파일 단위` / `DR-14: 토큰 = 코드 식별자만(파일명 제외)`.

- **DR-15 — KWW/장벽분포 꼬리 일반형의 재개방.**
  - 내용: v3~v5 보유 → v7 절삭 → 6-30 [MODEL-1 선택] → v1.0.11 Non-goals "ρ_G 기계장치 도입 금지·진단 prose 예고만 허용" 으로 scope-out 됐고(R1 L-04·R3 B-1; R6 R-2·DQ-3 의 "v1.0.15 [MODEL-1 선택]" 은 시점 오기 — 부록 A DQ-I17), FABLE §5-8 은 "KWW 진단 prose" 를 명시 결정 항목으로 남겼다(결정 기록 근거 미발견). 판독은 R6:R-2(지수 커널의 Laplace 중첩·ρ=δ 회수·큐뮬런트 → 폭 예산 ① 확장)를 B 등급(모델 차원 +1·부록 E rank-1 ODE 등가 상실 위험)으로 카탈로그화했다(R6 R-2·DQ-3). [MODEL-1 선택] 이 사용자 결정인지 master 결정인지는 1.3 에서 확인(미검증). 원문 = v3/v4/v5 §1.10(1.4 Step 11 (i) 정독 대상 — 미정독이면 안건에 "원문 미정독" 표기).
  - 근거: `FABLE_AUDIT_01`:52,64 · `HANDOVER_v1.0.11.md`:27–29 · `ch1_appE_selfconsistent.tex`:70.
  - 기본값: **3.1 카탈로그 B 로 평가 → DG-B 에서 결정**(사전 선호 없음).
  - 응답 선택지: `DR-15: DG-B 에서` / `DR-15: 재개방 확정(일반형 + ρ=δ 회수)` / `DR-15: scope-out 유지(진단 prose 만)`.

- **DR-16 — Eyring 근본식 척추 회복.**
  - 내용: 사용자 2026-06-11 지시(`HANDOVER_2026-06-11_ch1-v2-blank-rewrite.md`:7 — "전문 요지, 왜곡 없이" 표기)「(1.21) Eyring 식에서 시작해 풀어나가는 문건일 줄 알았다 … 이 문건은 그 식이 들러리」는 Fable v2 만 완전 구현했고 v7 이후 미계승, FABLE 감사가 "v12 척추 결정 필요(F-1)" 로 넘겼으나 결정 기록이 없다(근거 미발견). 판독은 내용은 100% 보유·배열만 미계승이라 K-1(재배열, 모델 차원 0·침습도 높)을 A 로 판정하고 3.3 구조 결정과 동시에 결정할 것을 제안했다(R6 K-1·R3 DQ-14). 원문 = Fable v2 tex 의 17단위 배열(1.4 Step 11 (i) 정독 대상 — master 실측 ✓ 존재·Assumptions 23·미정독이면 안건에 "원문 미정독" 표기). **S0–S5 역방향 식별 사슬의 본문 편입**(Non-goals 둘째 갈래·R1 DQ-7·R3 B-1)은 별도 DR 없이 본 항목에 인접해 DG-B 에서 함께 결정한다(비평 #6).
  - 근거: `FABLE_AUDIT_01`:47,58,64 · `ch1_sec00_intro.tex`:37–40 vs :42–88 · `ch1_sec05_width.tex`:13–44,46–121.
  - 기본값: **회복 — 동역학 장의 (a)출발식을 TST 일반식으로 두는 재배열(K-1)을 3.2 사다리에 채택**, 최종 확정은 DG-A/DG-B.
  - 응답 선택지: `DR-16: 회복(K-1 채택)` / `DR-16: 현행 코드 spine 유지` / `DR-16: DG-B 에서`.

- **DR-17 — §1.18 적층 준안정·athermal 절편 바닥 훅의 재개방/영구 배제/부록화.**
  - 내용: Opus v4 가 순수 추가(+158줄·6식·문헌 6편)하고 v5 부터 park(배제 결정 기록에 손실 명시 없음 — 근거 미발견), v1.0.18.2 로드맵에도 없다. FABLE 교훈 5 가 "재개방/영구 배제/부록화" 명시 결정을 요구했다(R1 L-03·R3 B-1). 판독은 이 항목을 열역학 축 다중 부분격자 staging 후보(TH-4.1·4.2 — 설명층 B)와 같은 자리로 봤고, 6-30 조사가 metastable AAAA stacking(Mercer 2021)을 GITT 잔여 원인으로 인용해 물리 연관은 살아 있다고 기록했다.
  - 근거: `note_A1`:118–120,181 · `FABLE_AUDIT_01`:51 · `HANDOVER_2026-06-30`:35 · `HANDOVER_v1.0.18.2.md`:16.
  - 기본값: **3.1 열역학 축(TH-4.1 자리)에서 v4 §1.18 원문 정독 후 재판정 → DG-B**(사전 선호 없음).
  - 응답 선택지: `DR-17: DG-B 에서` / `DR-17: 재개방(설명층)` / `DR-17: 영구 배제` / `DR-17: 부록화`.

- **DR-18 — Part T [C-92] "히스 소산·경로의존 정량 범위 밖" 선언과 "∂Ω/∂T 범위 밖" 선언의 부분 해제.**
  - 내용: 현행 `ch2_sec05_mixing.tex`:230–238 warnbox 는 히스 gap 소산(∝IΔU^hys)을 "본 장 범위 밖" 으로, :193–194 는 상호작용 엔트로피 ∂Ω/∂T 를 "범위 밖" 으로 선언한다. 둘 다 서브 저작이며 사용자 결정 기록은 원천에서 미발견(R5 DQ-6·R6 DQ-2). 판독 후보 Q-2(완전 cycle 소산 W_diss,j=Q_jγ_jh_ηΔU^hys 를 entropy production σ 항으로 정식화, 모델 차원 0)·TH-7.4(일반 엔트로피 수지에 히스 소산을 "같은 수지의 다른 항" 으로 위치)·TH-2.3/1.4(Ω(T), opt-in·tier C)는 이 선언의 개정을 전제한다.
  - 근거: 위 행 · R6 Q-2·T-1 · R5 TH-7.4·TH-2.3.
  - 기본값: **완전 cycle 소산은 범위 안(Q-2·TH-7.4 채택 시), 부분 cycle(h_η)·경로의존 불확실도 정량·Jarzynski/Crooks 는 범위 밖 유지; ∂Ω/∂T 는 일반식만 적고 파라미터화는 opt-in·tier C** — 1.3 Step 9 에서 "서브 판단(개정 가능)" 분류 확인 후 적용.
  - 응답 선택지: `DR-18: 부분 해제(기본)` / `DR-18: 선언 유지` / `DR-18: DG-B 에서`.

- **DR-19 — 서지 원장 재개설과 인용 규약 10조항.**
  - 내용: `V1023_REFERENCE_LEDGER.md` 는 V1022 와 바이트 동일 사본이라 v1.0.23~v1.0.25.1 의 원장 기록이 없고, bib 에 있으나 원장 미등재 키 6·원장에만 있는 키 4·동일 DOI 2키·et al. 4건·헤더 카운트 스테일이 확인됐다(R7 §1). R7 §5 는 (1) 단일 원장·단일 진실(+json, 소급 전사) (2) V1 키만 + 빌드 게이트 (3) 기억 서지 금지의 조작적 정의 (4) Crossref 5-필드 대조 + `refcheck/` 보존 + 서적은 출판사/WorldCat (5) 저자 전원 명기 (6) 한 문헌 한 키 + 별칭 표 (7) 1차 문헌 우선·tier 병기 (8) 절별 인용 하한 (9) bib 는 원장에서 생성 (10) 언어·표기·[A#] 폐지 를 초안했다. 결정 사항 = 재개설(소급 전사) vs 승계 방식 V1025 원장 추가 · 저자 전원 명기 채택 · 서적 검증 절차(출판사/WorldCat 대조 vs "장 수준 인용·ISBN 미대조" 정직 표기).
  - 근거: `V1020_REFERENCE_LEDGER.md`:3,33 · V1022:3–4 · R7 DQ-2·4·9.
  - 기본값: **재개설·소급 전사 · 저자 전원 명기 · 서적은 출판사/WorldCat 대조(DR-6 허용 시) 아니면 정직 표기**.
  - 응답 선택지: `DR-19: 기본` / `DR-19: 승계 방식(V1025 원장 추가)` / `DR-19: et al. 허용` / `DR-19: 서적 정직 표기만`.

- **DR-20 — 용어 결정: regular solution 역어와 신규 개념 용어 정책.**
  - 내용: 현행 문건은 "정규용액"(sec11·sec13·mech·appD·독립 부록 — 24회)과 "정칙용액"(sec16b·sifr·ch3 bib — 12회)을 섞어 쓰고 어느 쪽도 영어 원어 병기가 없다(R4b G26). brief·판독 카탈로그는 "정칙용액" 을 쓴다. v1.0.27 이 새로 도입하는 개념(entropy production·affinity·flux–force·cluster expansion·Redlich–Kister·Daumas–Hérold·Marcelin–de Donder 등)의 한글 표기 정책도 F-10 규약(억지 한글화 금지·첫 출현 영어 병기·정준/대정준 유지)에 따라 4.0 용어 결정표에서 확정해야 한다.
  - 근거: `USER_FEEDBACK_v1024_READING.md`:165–176 · `HANDOVER_v24.md`:83 · R4b DQ-6·DQ-10.
  - 기본값: **"정칙용액(regular solution)" 으로 통일·첫 출현 병기 · 신규 개념은 영어 원어 우선 + 필요 시 한글 병기(용어 결정표 4.0 에서 제출)**.
  - 응답 선택지: `DR-20: 정칙용액` / `DR-20: 정규용액` / `DR-20: 용어표 제출 후 결정`.

- **DR-21 — tier A/B/C 본문 표기와 교재 register 의 양립 · 채택/미채택 지위의 서술 규약.**
  - 내용: 현행 본문은 tier 표기 21건(정직성 규약, `ch1_sec07_broadening.tex`:64 각주 정의)과 함께 버전 라벨(Ch1 본문 13줄·Ch3 12곳 "v1.0.25 …")·검수 ID("#7 정정" 5회)·고백조("우리 진단" 등 6곳)로 채택/미채택 지위를 서술한다(R4a §5.3·R4b G13/G33/G34). 헌법 ①(자기 diff·내부 라벨·고백조 금지)과 충돌한다. 결정 사항 = tier 표기를 본문 유지(정직성 규약)할지 각주·부록 원장으로 이관할지 · 지위 서술을 "버전 번호·검수 ID 없이" 하는 규약 + grep 게이트(T-7 확장) 채택 여부.
  - 근거: `CLOSING_v1.0.15.md`:13–15 · R4a DQ-3 · R4b DQ-7.
  - 기본값: **tier 표기는 본문 유지(각주 정의 존속) · 버전 번호·검수 ID·고백조 0 규약 + T-7 게이트 채택**.
  - 응답 선택지: `DR-21: 기본` / `DR-21: tier 도 각주·부록 이관` / `DR-21: 현행 허용`.

- **DR-22 — 유도 완결성 판정의 "없음" 하한(기준 1 의 조작적 정의).**
  - 내용: R4a 는 (a)~(c) 중 둘 이상 부재를 "없음" 으로 두어 없음 1·부분 16 을 냈고, 기준 1 을 엄격히 읽어 "(c) 중간식 0 이면 없음" 으로 두면 부분 16 중 12 가 추가로 떨어져 보강 대상이 늘어난다(R4a DQ-1). R4b 는 완결/부분/비유도 3분류를 썼다(DQ-8). 이 하한이 2.2 게이트·4.x 저작 게이트·6.1 검수 렌즈의 기준이 된다. 관련 확인 = "필요한 식만(v7) vs 자기완결 교과서" 긴장이 2026-09-02 기준 1·2 로 해소된 것으로 보는 가정(Assumptions 20).
  - 근거: brief:36 사용자 verbatim "비약, 누락, 생략 없는 거의 유도에 가까운 수식 전개" · `CLOSING_v1.0.15.md`:25 [D3] "대입하면 [박스]" 점프 0 · R4a §2.
  - 기본값: **엄격 — (c) 중간식 ≥1 이 없으면 보강 대상(4단 척도 완결/부분/없음/비유도), 긴장 해소 가정 확인**.
  - 응답 선택지: `DR-22: 엄격(기본)·긴장 해소 확인` / `DR-22: R4a 하한(둘 이상 부재)` / `DR-22: 긴장 미해소 — 별도 지시`.

- **DR-23 — 챕터 1~3 산출물의 검수 등급(THEORY BLUEPRINT 의 고가치 판정).**
  - 내용: 헌법 §3 은 A1·A2 고가치 reference 산출물에 "10라운드 + 커버리지×렌즈 6종 완주 둘 다", 통상 산출물에 "연속 2R 수렴", 그리고 "고가치·reference 여부가 애매하면 고가치로 취급" 을 요구한다. v2 는 등록부 3종·GAP REGISTER·THEORY BLUEPRINT 를 모두 통상(검수 sub 1R + 연속 2R)으로 자체 분류했고 3.6 은 적대검토 1회 + 재검 1R 이었다(감사 SPEC-05·FORMAT-09·LOGIC-03). BLUEPRINT 는 DG-A/B/C 결정과 챕터 4 저작 전부의 유일 근거이므로 reference 성격이 강하다. 등록부·GAP 은 판독 시드 위의 통합·검수 산출이라 통상으로 두되 상향 여지를 남긴다.
  - 근거: 헌법 §3·§3-coverage(완주 렌즈셋 6종) · brief:155 "★핵심" · R1 §4 관통 패턴(설계 doc 순응 검수의 한계 — Ch2 v4 w_eff 오류가 적대 2R 통과·v10 ρ(U_j) 자기모순) · 사용자 기준 6.
  - 기본값: **BLUEPRINT = 고가치(3.6 에서 10R + 커버리지×렌즈 6종 완주 둘 다 + 연속 2R 수렴) · 등록부 3종·GAP REGISTER = 통상(검수 sub ≥1R + 연속 2R 수렴)**. 비용 고지: 3.6 라운드 수가 1 → 10 으로 늘어 Step 49 의 세션 수가 증가한다(구체 수치는 원천에 없어 제시하지 않음).
  - 응답 선택지: `DR-23: 기본(BLUEPRINT 만 고가치)` / `DR-23: 챕터 1~3 산출물 전부 고가치` / `DR-23: 전부 통상(2R)`.

> DR-1~23 전건 확정(위 표). **GO 사인이 오면** 실행 직전 load-bearing 전제(§Assumptions 1~24)를 실물 대조(1g)한 뒤 Step 1 부터 5-stage 루프로 진행한다(DR-9: 챕터 1→7 연속, 3.7 은 보고점). 판독·통합·수정 에이전트의 Decision Queue 처리표·미해결·Read Coverage 는 `Claude/results/handoffs/2026-09-02-v2-master-plan/wf/plan_v3_appendix_ABC.md`(11-section 밖 handoff 노트)에 있다.

---

