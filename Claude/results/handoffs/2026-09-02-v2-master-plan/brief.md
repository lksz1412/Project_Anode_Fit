# BRIEF — v2.0.0 수식 연구 진보 마스터 플랜 초안 저작 (작업 sub 용)

> 작성 = master(Fable 5.1), 2026-09-02. 유닛 = master + 작업 sub(초안) + 검수 sub(감사), 직렬.
> 이 brief 는 master 가 정독한 원천의 요약 + 계획서 골격이다. **요약을 믿지 말고 §3 의 원천 파일을 직접 Read 하라** — 요약과 원천이 어긋나면 원천이 정본이고, 그 사실을 work_log 에 적는다.

---

## 0. 5항목 고지 (필수·먼저 읽을 것)

1. **역할**: 너는 「v2.0.0 마스터 플랜 저작」 유닛의 **작업 sub** 다. 책임 = 이 brief 의 골격(§4~§8)을 표준 11-section 마스터 플랜 **초안**으로 확장하는 것뿐이다.
2. **분업 경계**: 산출물은 `Claude/results/handoffs/2026-09-02-v2-master-plan/iter_1/plan_draft.md` 와 같은 폴더의 `work_log.md` **두 파일만**. `Claude/plans/`·`Claude/docs/`·`Claude/results/` 의 다른 파일, 기존 파일 일체를 **생성·수정·삭제하지 않는다**. `Codex/` 폴더는 **읽지도 쓰지도 않는다**. commit 권한은 master 전용 — git 명령을 실행하지 않는다.
3. **brief 범위 밖 자의 작업 금지**: 골격을 재설계하거나 Phase 를 임의로 빼거나, 새 결정을 확정하지 않는다. 골격이 틀렸다고 판단되면 **고치지 말고** work_log 의 「Decision Queue」에 근거와 함께 적는다. 새 문건·새 표준·새 메모리를 만들지 않는다.
4. **허위 attribution 금지**: 초안·work_log 에 "사용자 결정"·"사용자 지적"이라고 쓸 수 있는 것은 §2 에 verbatim 으로 실린 사용자 발화와 §3 원천 문건에 사용자 결정으로 기록된 항목뿐이다. 너의 판단·추정은 너의 출처로 명시한다.
5. **memory 규범 주입** (서브는 헌법 CLAUDE.md 는 상속하나 개별 memory 는 상속하지 않는다):
   - **전문 정독**: §3 의 필독 원천은 head→tail 전 영역 Read. 부분 read 는 합쳐 전 영역을 cover. grep·샘플로 "읽었다" 보고 금지. work_log 에 Read Coverage(파일·행 범위) 기록.
   - **4-tier 보고**: 확정 / 근거 미발견 / 추정 / 미검증 을 구분. 확정에는 근거(path+line).
   - **흐름 보호**: AskUserQuestion·EnterPlanMode·Workflow 등 팝업 도구 사용 금지. 결정 필요 항목은 초안의 `## Decisions Required` 와 work_log 의 Decision Queue 에 평문으로.
   - **계획서 양식 정본** = `C:\Users\lksz1\.claude\skills\skill_LKS_original_plan-execution\SKILL.md` 「① 계획 착수 시」절(1b 11-section·1c cumulative step·1d 챕터→Phase→step·1e 세부 계획서·1f 7단계·1g load-bearing·1h 유연성) + `references/record-formats.md`. **반드시 Read** 한 뒤 저작한다.
   - **소통**: 문건은 한글 prose + 영어 학술 원어 유지(억지 한글화 금지). 두문자어 첫 출현 병기. 메타 발언·자기변명 없이.

---

## 1. 과제 한 줄

사용자 지시(§2)대로, **Claude 측 전 작업 이력을 파악한 뒤 현행 v1.0.25 두 버전을 검토하고, 열역학·동역학 관점에서 수식 연구를 진보시키는 새 버전(기본 라벨 v2.0.0)** 을 만드는 장기 작업의 **마스터 플랜(11-section)** 을 초안한다. 실행은 이 계획서에 사용자 GO 가 떨어진 뒤의 일이다 — 초안은 계획만 담는다.

---

## 2. 사용자 지시 (verbatim — 2026-09-02, 생략 없이)

> 코덱스가 지금 지 나름대로 뭔가를 하고 있는데 몇주가 걸린데 그래서 걘그냥 놔둬.
>
> 지금까지 클로드로 진행한 모든 작업 이력 버전 변경점들, 마스터 플랜들, 버전별 이력을 파악하고, 그 이력들을 기반으로 현재의 가장 1.0.25 두 가지 버전을 검토하고, 그것들을 통합하든 수정하든 전혀 다른 새로운 이론을 끌고와서 엮든 뭐가 됐든간에 물리적, 화학적, 특히 열역학적, 동역학적 관점에서 이 수식 연구의 진보를 이뤄야한다.
>
> 가장 중점으로 보는 것이 몇 가지 있다. 염두에 두고 진행하도록.
> 1) 수식만으로도 80~90% 이상의 내용을 이해할 수 있을정도로 비약, 누락, 생략 없는 거의 유도에 가까운 수식 전개
> 2) 포맷은 대학원 수준의 열역학, 통계역학, 동역학 교재 수준의 상세한 설명
> 3) 리뷰 논문급의 빈틈 없는 레퍼런스 작업 및 내용
> 4) 청중은 전공은 다를지언정 석박사급 인력인 상황.
> 5) 최대한 일반화된 식을 유도하고 거기서 우리가 필요한 방향으로 수식을 간소화할 수 있는 레퍼런스가 확실한 가정
> 6) 작업 방식은 나의 계획 스킬, 지침을 따를 것. 마스터플랜 - 세부계획서 - 작업이력서 단계. 무슨일이 있어도 절대 나의 지침을 따를것. 작업 방법론으로는 니가 더 효율적일지 모르나 나는 효율이 아닌 결과물의 완성도 신뢰도를 중요시한다.
>
> 작업을 위한 마스터 플랜을 짜오도록 하라.

> (추가, 같은 날) 그리고 이 작업은 모델 배정을 예외적으로 모두 페이블 5.1로 진행한다.

해석 고정(master 판단·초안에 그대로 반영):
- "1.0.25 두 가지 버전" = `Claude/docs/v1.0.25/`(base, 무수정 보존) 와 `Claude/docs/v1.0.25.1/`(검증+touch-up 4건, 현행 최신). 실물 차이 = `_sections` 3파일(ch1_sec05_width·ch1_sec06_eqpeak·ch3v22_sec02b_sifr) + 마스터 3파일 표시 버전 + ARCHIVE_NOTE + PDF 3종. 대안 해석(v1.0.26 A/B 두 산출 = 물리 4전이 vs gallery 7전이)은 Decisions Required 에 올린다.
- "Codex 놔둬" = `Codex/` 무접근. Codex 산출물은 비교 대상도 아니다.
- 기준 1)~5) = 산출물 품질 기준 = 진단(작업 챕터 2)의 감사 축이자 저작(작업 챕터 4)의 게이트 축.
- 기준 6) = 방법론: 마스터 플랜 → 페이즈별 세부 계획서 → 스텝 이력(step 하나 = 파일 하나) → Result(md+json) → Ledger. 효율보다 완성도·신뢰도.
- 모델 배정 = **전원 Fable 5.1**(master·분석·저작·검수·감사 서브 전부). 헌법 배분표(master=Opus 4.8 등)의 사용자 명시 예외다.

---

## 3. 원천 파일 (정독 배정) — 초안 저작 전 Read 필수

경로는 전부 `D:\Projects\Project_Anode_Fit\` 기준.

### 3-A 필독(전문) — 골격의 근거
| # | 파일 | 무엇 | 줄 |
|---|---|---|---|
| A1 | `CLAUDE.md` | 프로젝트 지침 P1~P5(목표·경계·검수 8항목·시작 체크리스트·이름 보존) | 90 |
| A2 | `Claude/docs/INDEX.md` | 문건 MOC — v1.0.10→v1.0.25.1 버전별 요약(계보 1차 정본) | 197 |
| A3 | `Claude/plans/INDEX.md` | 계획서 MOC(스테일 표기 주의: 실제 최신 = v1.0.25) | 65 |
| A4 | `Claude/docs/v1.0.25.1/results/V1025_1_TOUCHUP_NOTE.md` | 현행 권위 기록(v1.0.25.1 = v1.0.25 + touch-up 4건·빌드 102/30/22p) | 62 |
| A5 | `Claude/docs/v1.0.25.1/results/HANDOVER_v25.md` | v1.0.25 인계(지시 11건·미완 N1~N13·주의 11항) | 171 |
| A6 | `Claude/docs/v1.0.25.1/results/HANDOVER_v24.md` | v1.0.24 인계(@3/@5·FB0~7 리비전) | 89 |
| A7 | `Claude/results/comp_v26_data/HANDOVER_regsol_investigation.md` | v1.0.26 regsol 재검증 미완(실행 차단) | 56 |
| A8 | `Claude/plans/2026-07-26-v1025-surgical-skew-consistency-plan.md` | 직전 마스터플랜(11-section 양식 실례·Step 1~31) | 241 |
| A9 | `Claude/docs/Fable_점검/FABLE_AUDIT_01_history_v3-v1011.md` | 이력 전수감사(v3→v1.0.11) — ★방향성 유실 표 §4·교훈 §5 | 73 |
| A10 | `Claude/docs/v1.0.15/CLOSING_v1.0.15.md` | ★헌법 3종(교과서 register·논문 깊이·수식-주도)·D1~D6·프로세스 규율 | 106 |
| A11 | `Claude/results/comp_v24/USER_FEEDBACK_v1024_READING.md` | 사용자 정독 피드백 F-01~F-11 원문(문체·용어·노테이션·코드=부록) | 207 |
| A12 | `Claude/results/comp_v24/VERSION_COMPARISON_v19_v23_v24.md` | v19(구문 최고)·v23(논리 최고)·v24 비교 감사 | 80 |
| A13 | `Claude/docs/v1.0.25.1/_sections/ch1_sec00_intro.tex` | 현행 문건의 자기 규정(spine N0~N9·Part 0/I/T 3층·Chapter 1~3) | 95 |
| A14 | `Claude/docs/v1.0.25.1/_sections/ch1_appE_selfconsistent.tex` | 부록 E 자기일관(refs 6/7 ratio 닫힘 — CLAUDE.md P1 핵심) | 218 |

### 3-B 필독(전문) — 이론 진보 후보의 선행 조사(재조사 방지·기각군 승계)
| # | 파일 | 무엇 | 줄 |
|---|---|---|---|
| B1 | `Claude/docs/v1.0.18.2/ROADMAP_future_physics.md` | 제안 2 Ω(ξ)·3 Cahn-Hilliard→γ_j·4 BV+Nernst-Planck·5 PSD | 50 |
| B2 | `Claude/results/comp_v24/IMPROVEMENT_DIRECTIONS.md` | MSMR 동형 확인·개선 랭크 #1~#4(정칙용액 자유에너지=근본 해법) | 87 |
| B3 | `Claude/results/comp_v24/LIT_ADVANCE_SYNTHESIS.md` | 2021–2026 문헌 4창 종합(정칙용액+Maxwell 헤드라인·소재별 결정표·정직 갭) | 130 |
| B4 | `Claude/docs/v1.0.22/results/comp_v23/SURV_SYNTHESIS.md` | 고등수학 서베이(Tier1 Fredholm ratio+전달함수 / Tier2 Fisher / 기각군) | 45 |
| B5 | `Claude/docs/v1.0.22/results/comp_SM2/SM2_SURVEY.md` | 통계역학 심화 후보 SM2-A/B/C(감수율·앙상블 동등성·켤레 쌍) | 136 |
| B6 | `Claude/plans/2026-07-18-v1023-ratio-and-advanced-methods-plan.md` | refs 6/7 접목 계획(11-section 실례·조건검수 게이트) | 226 |
| B7 | `Claude/plans/2026-07-18-anodefit-MASTER-plan.md` | 북극성·캠페인 A~G(B 전셀·C T/I/V·E 상태추론 미착수) | 129 |

### 3-C 참조(구조 확인용·부분 read 허용)
- `Claude/docs/v1.0.25.1/ch1_graphite_v1.0.24.tex`·`ch2_lco_v1.0.24.tex`·`ch3_si_v1.0.24.tex` — `\input` 조립 순서(Ch1 = 흑연 §0~§10 + Part T(ch2_sec00~10) + §18 + 부록 A/B/C/D/E; Ch2 = LCO sec11~17; Ch3 = Si sec01~05).
- `Claude/docs/v1.0.25.1/results/INDEX_v25.md` — v1.0.25 산출물 색인·재현 명령.
- `Claude/results/V1024_EXECUTION_LEDGER.md` — 12-col ledger 실례.
- `Claude/plans/` 전체 목록(90 파일·9567줄)·`HANDOVER*.md` 28본(1612줄, old/ 제외) — **초안 단계에서는 목록·건수만 확인**(전문 정독은 계획의 작업 챕터 1 이 수행).

---

## 4. Current Ground Truth (master 실측 — 초안의 같은 절에 반영, 수치 변경 금지)

### 4.1 git·환경
- 브랜치 `main` = `4069cb3`(2026-07-27, v1.0.26 A/B). origin/main 동일. tracked 변경 0·untracked 21(전부 Codex/work·Claude 빌드 부산물·process 산출). 모든 버전 브랜치(v1.0.25.1·v1.0.25-surgical·v1.0.24.1)는 main 의 조상.
- 환경: XeLaTeX(MiKTeX 25.12) `C:\Users\lksz1\AppData\Local\Programs\MiKTeX\miktex\bin\x64\xelatex.exe` 존재(2026-07-26 빌드 102/30/22p 실증). Python 3.12 + numpy/scipy/matplotlib/pandas OK. 구조 검사 도구 `Claude/docs/v1.0.25.1/results/tools_check_structure.py`(`check` 서브커맨드만 사용 — JSON 모드는 과거 마스터 tex 덮어쓰기 사고)·`tools_tex_strict_check.py`·`tools_doc_code_audit.py` 존재.
- `Claude/JCP_147(14)_144111_(2017) - Effects of external electric field.pdf` + `Claude/jcp_extract.txt` 존재(사용자 논문). **refs 6·7 원문(JCP 134, 121102 (2011); JCP 138, 164123 (2013)) 미소장**. refs 6/7 방법론 추출본 = `Claude/old/Archive_oldtrack/PHASE_DIAG_REFS67_DOSSIER.md`(+ 부록 E ⑤항).

### 4.2 현행 문건 v1.0.25.1 (동결 base — 무수정)
- 구조: 3 마스터 tex(파일명 `*_v1.0.24.tex` 유지 = DG-2 규약) + `_sections/` 56 + `appendix_phase_separation.tex`(독립 부록 497줄) + `common_preamble_v1024.tex`. 총 60 tex·**9214줄**. PDF **102/30/22p**.
- 자산 카운트(master 스크립트 실측): display 수식 환경 **230**·`\boxed` **64**(본문 39 + 부록·기타)·`\label` **429**·`\bibitem` **95**·`\cite` 호출 **265**(distinct 키 **93**)·section 49·subsection 115·figure 28·table/longtable 20·박스 = warnbox 14·keybox 18·bgbox 10·verifybox 15·srcbox 16·derivbox 1.
- 조립: **Ch1 흑연**(§0 서론·§1 N0N1·§2a/b Part 0 통계역학·§3 중심·§4 히스·§5 폭·§5b gr2L·§6 평형 peak·§7 broadening·§8 lag·§9 tail·§10 합산 → Part T 열특성 = ch2_sec00~10(분배함수·config·vib/전자·Einstein·mixing·극한·가역발열·종합·방법·종결) → §18 입력 → 부록 A 부호검산·B 코드맵·C/D(ch2 app)·E 자기일관) / **Ch2 LCO**(sec11~17: intro·center·hys·decomp·elec·peak·omega·MSMR) / **Ch3 Si·혼합**(map·cases·sifr·blend·mech·code). 장간 `\externaldocument` xr 교차참조(빌드 순서 ch1→ch2→ch3→ch1 재패스).
- 코드 `Anode_Fit_v1.0.24.py`(release 1.0.25·1917줄) = doc-leads 정합. 게이트 4종 GREEN·골든 bit-exact. **본 계획에서 코드는 Non-goal**(문건 확정 후 별도 doc-leads 동기 플랜).
- v1.0.25 vs v1.0.25.1 차이 = touch-up 4건(F1 regsol 삭제근거 정직화·F3 inline 표식·M-w §5 폭 포인터·L-bg §6 α=1 한정) — 식·라벨·boxed(39)·코드 불변.

### 4.3 계보 (확정 — A2·A9·A12 근거)
5-28 구트랙 RB(전하보존 6장→Ch1~5 통합 107p, `old/Archive_oldtrack`) → 6-10~12 Fable v2/v3(★Eyring 근본식 척추·200KB) → Opus v4(§1.18 적층 준안정)/v5(수식-구동)/v6(흐름도 재조립) → 6-29 v7(코드 플로우차트 척추로 **의도 절삭** 17p)·v8(유도 복원)·v9(LCO)·v10(broadening 복원) → 7-01 v1.0.10(코드-문건 동기) → 7-02 Fable 이력감사 → v1.0.12(N=10 경쟁·체리픽)·v1.0.13(Part 0 신설·LCO Part II)·v1.0.14(Hill 유도·부록 A/B·그림 경연)·v1.0.15(격자 퇴출·점별 인과 기억 적분·★CLOSING 헌법 3종)·v1.0.16(n(T))·v1.0.17(register·서지)·v1.0.18.1/.2(vib Einstein·로드맵 제안 2~5) → 7-08~13 v1.0.19(Fable 전면 재작성 Ch1+Ch2·Part II 7분할·doc-leads) → v1.0.20(서지 원장·품질 정정·동결)·v1.0.21(대정준 전하보존·TST bgbox·항법·Si 부록)·v1.0.22(★활물질별 3챕터 재편·계보 감사·CLT/CNT) → 7-18 v1.0.23(★JCP147 Fredholm ratio 부록 E·전달함수·고등수학 서베이) → 7-18~22 v1.0.24(공개데이터 검증 캠페인·@3 regsol/@5 stage-2L·XRD 상 판정·CODE_GUIDE)·v1.0.24.1(피드백 리비전 FB0~9 동결) → 7-26 v1.0.25(국소 수정: @2 skew opt-in·인과 pad·SI opt-in·regsol 삭제·FWHM λ^{3/2})·v1.0.25.1(검증+touch-up·빌드) → 7-27 v1.0.26 A/B(regsol 재검증 조사, 실행 차단·미완).
- 사용자 평(A12): **v1.0.19 = 구문 최고 · v1.0.23 = 논리 최고**. v24 이후 변경은 사용자 피드백 집행(품질 하락 0, 의도된 voice 평탄화).

### 4.4 현재 구속력 있는 결정·제약 (초안 Non-goals·Assumptions 에 승계)
- **헌법 3종**(A10): ①교과서 register(자기 diff·방어 어투·내부 라벨·고백조 금지) ②논문 깊이(완결 유도·tier·실측 vs 자기일관 구분·DOI) ③수식-주도((a)출발식→(b)연산→(c)중간식≥1→(d)박스, "대입하면 [박스]" 점프 0) + 완결 문장·orphan 0·한글 prose+영어 원어.
- **CLAUDE.md P3 8항**(A1): V_n 계열 구분 일관·전하 보존식 = 중심식·순환 의존 dependency graph·4분류 진단·refs 6/7 5항 sub-section·Ch1↔Ch2~5 전달 정합·ver.N↔Chapter 명칭 혼동 금지·**코드 = 부록 전용(본문 코드 토큰 0)**.
- **사용자 피드백 F-01~F-11**(A11, 집행 완료·규범으로 존속): F-04 전공서적 문체·F-10 억지 한글화 금지(요동→fluctuation 등)·F-11 코드=부록·F-02 확률 p 소문자·F-03 자리당 f_int/s_int 소문자 규약·F-05 제목 N-태그 제거·F-06 조판(여백 25mm·줄간 1.16·문단 0.55em·microtype).
- **D-D 국소 원칙·DG-2 파일명 유지**는 v1.0.25 한정 규약이었다 — v2.0.0 은 새 폴더·새 파일명이 가능하나 **기존 `\label`·기호·식 번호 체계의 자산 무유실 원칙**(v1.0.22 계보 감사 ③=0건 기준)은 승계한다. 자산 태그 `[A-xxx]`·`[E-xxx]`(각 절 말미 % 주석) 체계 존재.
- **Ω 물리 전량 유효**(regsol 은 dQ/dV 커널만 삭제됨) · **gallery ≠ 상**(XRD 상 수 불변) · **@2 α = 현상학 형상 파라미터(tier C)** · **$w_\eff$ 를 폭으로 읽기 금지** · **$C_\bg$ = 창-국소 상수 근사**.
- 미완·미결(A5 N4·N6~N9, A7): 흑연 두-상 4 vs 2 표기(Dahn 1991 본문 확인) · 신규 CSV 8종 리포 보존 · 재현 스크립트 등재 · regsol 철회 다중셀 확인 · **skew-regsol 결합 커널 vs GITT 평형 데이터 판정(v1.0.26)** · 회사 다온도 데이터 의존 정량(Task #38).

### 4.5 방향성 유실·park·미착수 (작업 챕터 1.4 등록부의 시드 — A9 §4·B1~B7)
Eyring 근본식 척추(Fable v2, 미계승) · 역방향 식별 사슬 S0~S5·16-울타리(v5/v6, v7 절삭) · §1.18 적층 준안정·athermal 훅(park) · KWW/장벽분포 꼬리 일반형(scope-out) · 원구상 Chapter 2~5(발열·반응속도론·통합 상태방정식·히스테리시스 계층, CLAUDE.md P1 — 현행은 재료별 3장 + Part T 로 재편) · 로드맵 제안 2 Ω(ξ)·3 Cahn-Hilliard→γ_j·4 BV+Nernst-Planck·5 PSD(B1) · IMPROVEMENT #3 coupling·#4 정칙용액 자유에너지(B2) · LIT_ADVANCE ◐선검증군(G3 정칙용액+Maxwell·G5·L4~L6·S4·S5·M1·M4)(B3) · SURV Tier2 Fisher·Tier3 명명노트·기각군(B4) · SM2-A/B/C(B5 — **집행 여부 미확정**: v1.0.25.1 §6·§2b·§2.7 에 "감수율·var(N)·앙상블 동등성" 18건 존재 → 작업 챕터 1.4 에서 확인) · anodefit 캠페인 B 전셀·C T/I/V·E 상태추론(B7).

### 4.6 cumulative step 좌표
직전 arc(v1.0.25 계획)는 Step 1~31 로 종결·v1.0.26 조사는 ledger 없음. 본 마스터 플랜은 **새 arc** 이므로 Step 1 부터 단조 누적한다(Phase 를 넘어도 리셋 없음). 이 사실을 Current Ground Truth 에 명기.

---

## 5. 골격 — 작업 챕터 → Phase → step (초안이 그대로 확장할 것)

> ★ 여기의 "작업 챕터 1~6" 은 **작업 단위 이름**이고 문건의 "Chapter 1~3(재료별)"·역사적 "ver.1~5" 와 **다른 축**이다(P3 #7). 초안 Phase Range 표 상단에 3축 대응 주석을 둔다.

### 작업 챕터 1 — 이력 통합 (Steps 1–10) · 산출 = 등록부 3종 + Result
| Phase | 이름 | Steps | 게이트(확인 가능 조건) |
|---|---|---|---|
| 1.1 | 인벤토리·정독 배정 | 1–2 | 인벤토리 파일에 plans 90·HANDOVER 28·Fable 감사 8·CLOSING·INDEX 2·results 마스터 ledger 전건 path+줄수; 정독 배정표(전문 정독 = 전부 — 효율 이유로 축약하지 않음) |
| 1.2 | 버전별 변경점 등록부(v3→v1.0.26) | 3–5 | 버전 행 누락 0(§4.3 계보 목록 대조) · 각 행 = 구조/물리/식/코드/게이트/결정/페이지/근거 path · 사용자 평(v19 구문·v23 논리) 반영 |
| 1.3 | 유효 결정·제약 등록부 | 6–7 | 헌법 3종·P3 8항·F-01~11·D/DG 결정·용어·노테이션 규약 전건 = 출처 path+line + verbatim + 현재 상태(존속/v1.0.25 한정/폐기) |
| 1.4 | 방향성 유실·park·미결 등록부 | 8–9 | §4.5 항목 전건 + 정독 중 발견분 · 각 항목 = 원 지시 시점·현행 처리 상태·재개방 후보 여부·근거 |
| 1.5 | Result | 10 | `PHASE_1_..._RESULT.md`+`.json`·Ledger 행·Read Coverage(행 범위) |

### 작업 챕터 2 — 현행본 진단 (v1.0.25·v1.0.25.1) (Steps 11–24) · 산출 = GAP REGISTER
| Phase | 이름 | Steps | 게이트 |
|---|---|---|---|
| 2.1 | 자산 지도 | 11–12 | 기계 추출 표(boxed 64·display 230·label 429·bibitem 95·cite 키 93) 카운트 일치 · 두 버전 diff 3파일 확정·touch-up 4건 판정 |
| 2.2 | 유도 완결성 감사(기준 ①) | 13–16 | boxed 64/64 각각 (a)출발식·(b)연산·(c)중간식·(d)박스 사슬 판정 행 · 비약/누락/생략 목록(ID·파일·행·성격) · 청크 ≤ ~500줄·렌즈 follow+적대검산 |
| 2.3 | 일반성·가정 사다리 감사(기준 ⑤) | 17–18 | 모든 간소화 지점의 가정·유효범위·레퍼런스 유무 등록 · "일반식→특수식" 계보도 |
| 2.4 | 서지 감사(기준 ③) | 19–20 | bibitem 95 DOI/서지 검증 표 · 절별 인용 밀도 · 1차 문헌 공백 · 리뷰급 주제별 필수 문헌 체크리스트 대조 |
| 2.5 | 형식·register 감사(기준 ②④) | 21–22 | 교재 형식 요소(정의·정리·유도·예제·요약·기호표) 존재 체크 · F-04/F-10/F-11 잔존 grep · 타전공 석박사 가독성 판정(정성 → 항목 분해) |
| 2.6 | v1.0.26 regsol 미결의 설계 입력화 | 23 | 두-상 커널 문제(정칙용액+Maxwell vs 로지스틱 gallery vs skew-regsol)를 판정 기준·필요 데이터·현 근거와 함께 정식화 |
| 2.7 | Result — GAP REGISTER | 24 | 4-tier·Read Coverage·md+json |

### 작업 챕터 3 — 이론 진보 설계 (Steps 25–40) ★핵심 · 산출 = THEORY BLUEPRINT → ★사용자 결정 정지
| Phase | 이름 | Steps | 게이트 |
|---|---|---|---|
| 3.1 | 후보 이론 조사·평가 | 25–28 | 기존 서베이 B1~B5 전건 흡수(재조사 0·기각군 승계) + 신규 문헌 검색 → 후보 카탈로그(등급·모델차원·침습도·서지·선행 데이터). 축 = 열역학(lattice gas→정칙용액→Ω(ξ)/Redlich-Kister→sublattice/staging→Cahn-Hilliard/phase-field) · 통계역학(대정준·요동-응답 SM2-A/B/C·transfer matrix staging) · 동역학(Eyring/TST 척추·Butler-Volmer·Marcus·Nernst-Planck·Onsager 선형 비가역 열역학·master equation/Fokker-Planck·KWW/장벽분포·Fredholm ratio) · 히스테리시스(spinodal·CNT·Preisach) · 열(entropy production·Bernardi) |
| 3.2 | 통합 골격 설계("일반→특수" 사다리) | 29–32 | 일반 비평형 열역학 상태식(affinity·flux-force) → 준평형 → 평형(정칙용액→로지스틱) / 동역학 일반(TST) → lag → 동결 — 각 단계 가정+레퍼런스+회수 조건 · 기존 boxed 64 식이 사다리 어디서 회수되는지 매핑(자산 무유실) |
| 3.3 | 문건 구조 결정안 | 33–34 | (a) 현행 재료별 3장 유지+내부 일반화 vs (b) Part I 일반 이론(열역학·통계역학·동역학·열·히스) + Part II 재료 적용(흑연·LCO·Si·블렌드) — 장단·자산 이동 맵·xr 영향·페이지 추정 |
| 3.4 | 수식 사슬 원형(derivation skeleton) | 35–37 | 새 구조 절별 목표 boxed 식 + (a)~(d) 사슬 계획 + 신규/승계/회수 표시 · P3 #3 dependency graph·#4 4분류 |
| 3.5 | 레퍼런스 마스터 원장 설계 | 38 | 주제별 필수 문헌 맵(리뷰급)·DOI 검증 절차·인용 규약(V1 키만·기억 서지 금지) |
| 3.6 | 설계 적대검토 | 39 | 설계서 자체 adversarial(refute mandate·최약점 1곳) — A9 교훈 3 |
| 3.7 | Result — THEORY BLUEPRINT + ★정지 | 40 | md+json · **사용자 결정 게이트**: DG-A 구조(3.3)·DG-B 채택 이론 목록·DG-C 버전 라벨 확정 전 저작 착수 금지 |

### 작업 챕터 4 — 저작 v2.0.0 (Steps 41– ; 3.7 확정 후 세부 계획서 작성) · 기본 골격 = 3.3 (b) 기준(확정 시 갱신)
4.0 골격·프리앰블·기호표·빌드 baseline → 4.1 열역학·통계역학 기초(일반식) → 4.2 평형 열역학(중심·폭·상분리·정칙용액/Ω(ξ)·staging) → 4.3 동역학(TST/Eyring·BV·lag·tail·Fredholm ratio·전달함수) → 4.4 열특성(엔트로피 분해·가역발열·entropy production) → 4.5 히스테리시스 → 4.6 흑연 적용 → 4.7 LCO → 4.8 Si·블렌드 → 4.9 부록(기호·부호검산·코드맵·자기일관·상분리). 각 Phase = 절 단위 루프(정독→구성→자체검수→앞 절 정합→빌드→ledger) + 빌드 게이트(xelatex 3-pass err0·undefined 0·STRUCTURE PASS) + 본문 코드 토큰 0 + Result.

### 작업 챕터 5 — 서지 완결
5.1 원장 확장·DOI 전수 검증 → 5.2 인용 밀도·1차 문헌 매핑 → 5.3 서지 감사 Result.

### 작업 챕터 6 — 검수·수렴·마감
6.1 가변 청크 검수 **10라운드 + 커버리지×렌즈 6종(구조·적대검산·follow·usable·완결성·regression) 완주 둘 다 충족**(고가치 reference 등급) + 실행 기반 검증 렌즈(SymPy 재유도·수치 극한·코드 재현) → 6.2 CLAUDE.md P3 8항 + 헌법 3종 + F-04/F-10/F-11 게이트 → 6.3 빌드 GREEN·PDF·`Claude/docs/HANDOVER_v2.0.0.md`·INDEX 갱신·commit·push·Result.

---

## 6. Non-goals (초안에 그대로)
- 코드 동기(doc-leads) — 문건 확정 후 **별도 플랜**. 본 계획은 문건.
- `Claude/docs/v1.0.25/`·`v1.0.25.1/`·`v1.0.24*/` 수정 X(동결 base·비교 기준).
- `Codex/` 접근 X(읽기 포함).
- 역문제·상태추론(anodefit E)·전셀 합성(B) X.
- 회사 데이터 의존 정량(Task #38) X — 필요 항목은 warnbox·tier 로 정직 표기.
- 새 공개데이터 상시 파이프라인 X(단 2.6/3.1 판정에 기존 확보 데이터 재사용은 허용·신규 다운로드는 DQ).
- 효율을 이유로 정독·검수 하한을 낮추는 것 X(사용자 기준 6).

## 7. 운용(초안 「Implementation Interfaces」 또는 별도 절에)
- 모델 = **전원 Fable 5.1**(사용자 명시 예외). 유닛 = master + 작업 sub + 검수 sub, **직렬**. 병렬(fan-out)은 §11 sign-off 시에만.
- 기록 = 스텝 이력 `Claude/results/Step <N> — <제목>.md`(step 하나=파일 하나·5항목) · Result `Claude/results/PHASE_<id>_V2_<topic>_RESULT.md`+`.json` · Ledger `Claude/results/PHASE_1-6_V2_EXECUTION_LEDGER.md`(12-col) · 세부 계획서 = 마스터 내 Phase 절 또는 `Claude/plans/2026-MM-DD-v2-phase-<id>-plan.md` · 핸드오프 `Claude/results/handoffs/<task>/` · 인계 `Claude/docs/HANDOVER_v2.0.0.md`.
- 재독 강제: 매 Phase 착수 시 마스터 플랜 재독(첫 Step 이력에 기록), 매 Step 착수 시 세부 계획서 재독.
- 정지 조건: 파괴·비가역 · 사용자만 결정 가능한 blocking(3.7 DG-A/B/C) · 권한 부족 · 보호영역 침범 · 새 의존성 · FAIL gate · 사용자 stop · 통제문서 모순. 병렬 승인 필요는 정지 사유 아님(직렬 진행·DQ 기록).
- git: 각 Step/Phase 종료 commit(master) · push 는 Phase 종료 시 · merge X.
- 구조 맵(신규): `Claude/docs/v2.0.0/`(저작 시 생성) · `Claude/results/handoffs/2026-09-02-v2-master-plan/` · Step/Result/Ledger 위치 위와 같음.

## 8. Decisions Required (초안 §11 — 각 항목에 실제 내용·근거·기본값·한 줄 응답 선택지)
- DR-1 "두 가지 1.0.25 버전" 해석: 기본 = v1.0.25 + v1.0.25.1(A). 대안 = v1.0.26 A/B 두 산출(B). regsol 미결은 어느 쪽이든 2.6/3.1 로 흡수.
- DR-2 목표 버전 라벨·폴더: 기본 v2.0.0(`Claude/docs/v2.0.0/`, 일반→특수 재구조 = major). 대안 v1.1.0.
- DR-3 문건 구조: 3.3 산출 후 **3.7 에서 정지해 결정**(지금은 사전 선호만 — (b) Part I 일반 이론 + Part II 재료 적용이 기준 5)와 정합한다는 master 판단을 근거와 함께 제시).
- DR-4 코드 동기 = 별도 후속 플랜(기본).
- DR-5 병렬 sign-off: 기본 직렬. 옵션 = 2.2~2.5 진단 청크 병렬 / 4.x 저작 파트 병렬 — 비용(유닛 수 × Fable 5.1 + master 통합 부하) 고지.
- DR-6 외부 접근: 문헌 검색·DOI 검증(Crossref)·공개데이터 재다운로드 허용 여부(기본 = 읽기 전용 허용).
- DR-7 이력 정독 범위: 기본 = plans 90·HANDOVER 28·감사·CLOSING·INDEX·ledger **전문 정독**(비용 고지). 대안 = 마스터플랜·인계 전문 + 페이즈 세부 계획서 구조 추출.
- DR-8 refs 6·7 원문 제공 여부(CLAUDE.md P1 "실제 확인" 요구): 기본 = JCP147 자족 + dossier + Crossref 서지 확정·미소장 정직 표기.
- DR-9 GO 범위: 기본 = 작업 챕터 1→2→3 연속 진행 후 3.7 정지. 대안 = 챕터 1 만 먼저.

---

## 9. 초안 산출 규격
- 파일: `Claude/results/handoffs/2026-09-02-v2-master-plan/iter_1/plan_draft.md` (UTF-8, 한글 prose + 영어 원어).
- 11-section 순서·이름 보존: Summary / Current Ground Truth / Phase Range / Non-goals / Implementation Changes / Phase N — <name> / Implementation Interfaces / Test Plan / Assumptions / Correction History / Decisions Required. 비코드 프로파일: Implementation Changes 는 "산출물 변경 대장"으로, Implementation Interfaces 는 운용(모델·기록·정지·git·구조 맵)으로, Test Plan 은 실제 게이트(빌드·구조검사·카운트·grep·검수 하한)로 채운다.
- Phase 절: **작업 챕터 1 은 Step 단위까지 세부**(1e — 진행 예정 Phase). 챕터 2·3 은 Phase·Step 범위·게이트·중단 조건·다음 조건. 챕터 4~6 은 Phase 목록·게이트·"3.7 확정 후 세부화" 명시.
- 각 게이트 = 명령/증거/범위 정량(3a). "적절해 보임" 금지.
- Current Ground Truth = §4 수치 그대로 + 구조 맵 + "미검독" 표시(초안 단계에서 안 읽은 것은 안 읽었다고).
- Assumptions = load-bearing 전제 목록(1g: 실행 직전 실물 대조 대상) — 예: xelatex 존재·v1.0.25.1 동결·JCP147 소장·refs 6/7 미소장·전원 Fable 5.1.
- Correction History = "v1 초안(작업 sub) 2026-09-02" 1행.
- 분량 상한 없음. 단 §3 원천에 없는 수치·서지·결정을 만들지 않는다(추정은 "추정" 표기).

## 10. work_log.md 규격 (같은 폴더)
- 수행 / 근거·판단 / Read Coverage(파일·행 범위 전건) / 산출 파일 / **Decision Queue**(골격 이견·brief 오류·추가 후보) / 미해결.
