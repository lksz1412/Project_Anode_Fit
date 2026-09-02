# v2.0.0 Plan — 수식 연구 진보 마스터 플랜 (열역학·동역학 관점의 일반화 재구축)

> **초안 v1 · 작업 sub(Fable 5.1) · 2026-09-02.** master 통합·검수 sub 감사 전의 **초안**이다. 최종본은 master 가 `Claude/plans/2026-09-02-v2-master-plan.md` 로 저장한다(본 파일은 handoff 산출물).
> **성격** = 마스터 플랜(top-level). 실행은 사용자 GO 뒤의 일이며, 본 문서는 계획만 담는다. 페이즈별 세부 계획서는 각 Phase 착수 시 작성한다(작업 챕터 1 은 본 문서 안에서 Step 단위까지 세부화 — 진행 예정 Phase).
> **양식** = 11-section(Summary / Current Ground Truth / Phase Range / Non-goals / Implementation Changes / Phase N — \<name\> / Implementation Interfaces / Test Plan / Assumptions / Correction History / Decisions Required) · cumulative step · 챕터→Phase→step · 게이트 = 명령/증거/범위 정량 · 비코드 프로파일(Implementation Changes = 산출물 변경 대장 · Implementation Interfaces = 운용 · Test Plan = 실제 게이트).
> **원천** = `Claude/results/handoffs/2026-09-02-v2-master-plan/brief.md`(master 명세) + 그 §3-A 14본·§3-B 7본 전문 정독 + §3-C 구조 확인(본 초안의 Read Coverage 는 같은 폴더 `work_log.md`). 요약과 원천이 어긋난 곳은 원천을 따랐고 그 사실을 work_log 에 적었다.
> **모델 배정** = 전원 **Fable 5.1**(master·분석·저작·검수·감사 서브 전부 — 사용자 명시 예외, brief §2 추가 발화).
> **Codex 측** = 무접근(읽기 포함). Codex 산출물은 비교 대상이 아니다.

---

## Summary

**과제 한 줄.** Claude 측 전 작업 이력(v3 → v1.0.26, 계획서·인계·감사·클로징·ledger)을 파악한 뒤, 현행 v1.0.25 두 버전(`Claude/docs/v1.0.25/` base + `Claude/docs/v1.0.25.1/` 현행 최신)을 검토하고, **물리적·화학적, 특히 열역학적·동역학적 관점에서 이 수식 연구를 진보시키는 새 버전(기본 라벨 v2.0.0)** 을 저작한다. 통합·수정·새 이론 접목 중 무엇이 됐든 "진보"가 목표이며, 그 진보의 품질 기준은 사용자가 지정한 다음 여섯이다(brief §2 verbatim 요지).

| # | 사용자 기준(2026-09-02 verbatim 요지) | 본 계획에서의 지위 |
|---|---|---|
| 1 | 수식만으로도 80~90% 이상을 이해할 수 있을 만큼 비약·누락·생략 없는, 거의 유도에 가까운 수식 전개 | 진단 축(작업 챕터 2.2 유도 완결성 감사) · 저작 게이트(챕터 4 (a)~(d) 사슬) · 검수 렌즈(챕터 6 follow·적대검산) |
| 2 | 대학원 수준 열역학·통계역학·동역학 교재 수준의 상세한 설명 | 진단 축(2.5 형식·register 감사) · 저작 게이트(교재 형식 요소 존재) |
| 3 | 리뷰 논문급의 빈틈 없는 레퍼런스 작업 및 내용 | 진단 축(2.4 서지 감사) · 설계(3.5 원장) · 완결(챕터 5) |
| 4 | 청중 = 전공은 달라도 석박사급 인력 | 진단 축(2.5 가독성 판정) · 저작 규약(전제 개념부터 단계적 전개·두문자어 병기) |
| 5 | 최대한 일반화된 식을 유도하고 거기서 필요한 방향으로 간소화할 수 있는, 레퍼런스가 확실한 가정 | 진단 축(2.3 일반성·가정 사다리) · 설계 핵심(3.2 "일반→특수" 사다리) · 구조 결정(3.3) |
| 6 | 작업 방식 = 사용자 계획 스킬·지침(마스터플랜 → 세부계획서 → 작업이력서). 효율이 아닌 완성도·신뢰도 | 방법론 전체(본 문서·세부 계획서·Step 이력·Result·Ledger·검수 하한) — 효율을 이유로 어떤 하한도 낮추지 않는다 |

**왜 새 버전인가.** 현행 v1.0.25.1 은 v1.0.24 계보(활물질별 3챕터: 흑연 / LCO / Si·혼합 + Part T 열특성 + 부록 E 자기일관)의 국소 수정판이다. 사용자 평은 **v1.0.19 = 구문 최고 · v1.0.23 = 논리 최고**(`Claude/results/comp_v24/VERSION_COMPARISON_v19_v23_v24.md`:3)이고, v24 이후 변경은 사용자 피드백 집행(품질 하락 0, 의도된 voice 평탄화, 같은 문서 §0)이다. 그러나 (i) 문건의 평형 커널은 로지스틱 단일계(MSMR 동형)이고 정칙용액(regular solution)+Maxwell 은 삭제(코드)·해석적 기록(문건)으로만 남아 있으며(`docs/v1.0.25.1/results/HANDOVER_v25.md`:85–89), (ii) Eyring 근본식 척추·역방향 식별 사슬·적층 준안정 등 사용자 방향 지시의 미계승분이 이력 감사에 기록돼 있고(`docs/Fable_점검/FABLE_AUDIT_01_history_v3-v1011.md` §4), (iii) 선행 서베이가 "일반화된 열역학 포텐셜(정칙용액 자유에너지·Ω(ξ)·Cahn–Hilliard)·비평형 열역학·통계역학 상위 항등"을 반복해서 다음 단계로 지목했으나(`docs/v1.0.18.2/ROADMAP_future_physics.md` · `results/comp_v24/IMPROVEMENT_DIRECTIONS.md` §3 #4 · `results/comp_v24/LIT_ADVANCE_SYNTHESIS.md` §1 · `docs/v1.0.22/results/comp_SM2/SM2_SURVEY.md`) 집행되지 않았다. 사용자 기준 5(일반식 → 간소화)와 기준 1(유도에 가까운 전개)은 국소 수정으로는 닿지 않는 요구이므로, 이력 통합 → 진단 → 이론 설계 → (사용자 결정) → 저작의 **새 arc** 를 연다.

**범위(여섯 작업 챕터).** 작업 챕터 1 이력 통합(등록부 3종) → 2 현행본 진단(GAP REGISTER) → 3 이론 진보 설계(THEORY BLUEPRINT, ★사용자 결정 정지) → 4 저작 v2.0.0 → 5 서지 완결 → 6 검수·수렴·마감. 챕터 1~3 은 조사·설계이고, 챕터 4 이후는 3.7 의 사용자 결정(DG-A 구조 · DG-B 채택 이론 · DG-C 버전 라벨) 확정 뒤에 세부 계획서를 쓴다.

**핵심 정직 프레임.** (1) 코드는 본 계획의 Non-goal 이다 — 문건 확정 후 별도 doc-leads 동기 플랜(DR-4). (2) 새 이론을 "접목"할 때는 선행 서베이가 확정한 **기각군**(Wiener–Hopf·WKB·다중척도·중심다양체·Langevin·Preisach 연산자 채택·Kubo 동적 χ 가정 충돌 — `docs/v1.0.22/results/comp_v23/SURV_SYNTHESIS.md`)을 승계해 재조사하지 않는다. (3) 기존 자산(`\label` 429·`\boxed` 64·식 번호 체계·자산 태그 `[A-xxx]`/`[E-xxx]`)은 **무유실**로 승계한다 — v1.0.22 계보 감사 ③=0건 기준(`docs/INDEX.md`:33). (4) regsol 미결(v1.0.26)은 결정이 아니라 **설계 입력**으로 흡수한다(2.6·3.1). (5) 근거 없는 수치·서지·결정은 만들지 않는다 — 추정은 "추정"으로 표기한다.

---

## Current Ground Truth

> brief §4 의 master 실측 수치를 그대로 옮기되, 본 초안 저작 시점에 작업 sub 가 **읽기 전용으로 실물 대조한 항목**은 `[sub 실측 ✓]`, brief 를 인용만 한 항목은 `[brief 인용·미검증]`, 안 읽은 것은 **미검독**으로 표시한다. 4-tier: 확정 / 근거 미발견 / 추정 / 미검증.

### 2.1 git·환경

| 항목 | 값 | 근거·검증 상태 |
|---|---|---|
| 브랜치 `main` HEAD | `4069cb3`(2026-07-27, "feat(v1.0.26 A/B): regsol 재검증 — 물리 4전이 vs gallery 7전이 두 버전 산출") | 확정 — 세션 시작 git status 스냅샷(하네스 제공)·brief §4.1. 본 sub 는 git 명령을 실행하지 않았다(경계) |
| origin/main | main 과 동일 | brief 인용·미검증 |
| tracked 변경 / untracked | 0 / 21(전부 `Codex/work/*`·`Claude/docs/v1.0.17~18.2/figs·sample_test`·`Claude/results/process/C3_*`·`Claude/results/regsol_test/`) | 확정 — 세션 시작 스냅샷에 21건 열거 |
| 버전 브랜치 | `v1.0.25.1`·`v1.0.25-surgical`·`v1.0.24.1` 전부 main 의 조상 | brief 인용·미검증 |
| XeLaTeX | MiKTeX 25.12 `C:\Users\lksz1\AppData\Local\Programs\MiKTeX\miktex\bin\x64\xelatex.exe` | **[sub 실측 ✓ 존재]**. 2026-07-26 빌드 102/30/22p 실증 = `docs/v1.0.25.1/results/V1025_1_TOUCHUP_NOTE.md`:55. PATH 등재 여부 미검증 |
| Python | 3.12 + numpy/scipy/matplotlib/pandas | brief 인용·미검증(A7:50 "기존 설치됨" 부합) |
| 구조 검사 도구 | `docs/v1.0.25.1/results/tools_check_structure.py`(`check` 서브커맨드만 — JSON 모드는 과거 마스터 tex 덮어쓰기 사고, `docs/v1.0.25.1/results/INDEX_v25.md`:85·`HANDOVER_v24.md`:50) · `tools_tex_strict_check.py` · `tools_doc_code_audit.py` | **[sub 실측 ✓ 3본 존재]** |
| 사용자 논문 | `Claude/JCP_147(14)_144111_(2017) - Effects of external electric field.pdf` + `Claude/jcp_extract.txt` | **[sub 실측 ✓ 존재]**(내용 미검독) |
| refs 6·7 원문 | JCP 134, 121102 (2011) · JCP 138, 164123 (2013) — **미소장** | 확정(부재) — brief §4.1·`plans/2026-07-18-v1023-ratio-and-advanced-methods-plan.md`:43. 방법론 추출본 = `Claude/old/Archive_oldtrack/PHASE_DIAG_REFS67_DOSSIER.md` **[sub 실측 ✓ 존재·미검독]** + 부록 E ⑤항(`_sections/ch1_appE_selfconsistent.tex`:129–134) |
| `Claude/docs/v2.0.0/` | 부재 | **[sub 실측 ✓ 부재]** — 저작 시 생성(DR-2) |

### 2.2 현행 문건 v1.0.25.1 (동결 base — 무수정)

- **구조**: 3 마스터 tex(파일명 `ch1_graphite_v1.0.24.tex`·`ch2_lco_v1.0.24.tex`·`ch3_si_v1.0.24.tex` 유지 = DG-2 규약) + `_sections/` 56(`common_preamble_v1024.tex` 포함) + `appendix_phase_separation.tex`(독립 부록) = **60 tex · 9214줄** **[sub 실측 ✓ 일치]**. PDF **102/30/22p** — PDF 3종 존재 **[sub 실측 ✓]**, 페이지 수는 brief·A4:55 인용(미열람).
- **자산 카운트**(brief §4.2 = master 스크립트 실측; **[sub 재계수 ✓ 전건 일치]**, 빌드 세트 60 tex 한정 — `docs/v1.0.25.1/results/` 하위의 경쟁 초안 tex 는 제외):

| 자산 | 값 | 비고 |
|---|---|---|
| display 수식 환경 | **230** | = `equation(*)` 228 + `align(*)` 1 + `gather/multline` 1. 이 밖에 `\[ … \]` 38개가 별도로 있다(sub 실측 — brief 미기재·추가 정보) |
| `\boxed` | **64** | 본문 39 + 부록·기타(brief). 파일별 분포는 §2.2-보 참조 |
| `\label` | **429** | |
| `\bibitem` | **95** | |
| `\cite` 호출 / distinct 키 | **265 / 93** | |
| section / subsection | **49 / 115** | |
| figure / table+longtable | **28 / 20** | |
| 박스 8종 | warnbox 14 · keybox 18 · bgbox 10 · verifybox 15 · srcbox 16 · derivbox 1 | (bgbox·derivbox 포함 6종 실측 + brief 의 8종 표기 승계) |
| 자산 태그 | `[A-xxx]` 159 · `[E-xxx]` 8 | sub 실측(각 절 말미 `%` 주석) — brief 는 체계 존재만 언급 |

**§2.2-보 `\boxed` 파일별 분포(sub 실측, 챕터 2.2 청크 배정의 근거)**: Ch1 곡선 사슬 = sec01 1·sec02a 5·sec02b 4·sec03 1·sec04 2·sec05 2·sec05b 1·sec06 3·sec08 3·sec09 4·sec10 1 → **27** / Part T = ch2_sec00 1·sec01 1·sec02 1·sec03 1·sec04 2·sec05 2·sec07 1·sec08 1 → **10** / 부록 = appE 4 + `appendix_phase_separation` 3 → **7** / Ch2 LCO = sec11 1·sec12 1·sec13 3·sec14 1·sec15 4·sec16 1·sec16b 3·sec17 2 → **16** / Ch3 Si = sec02b 2·sec03 1·sec04 1 → **4**. 합 27+10+7+16+4 = **64**.

- **조립**(마스터 tex 3본 `\input` 순서 — **[sub 실측 ✓]**): **Ch1 흑연** = §0 서론(`ch1_sec00_intro`) · §1 N0N1 · §2a/§2b Part 0 통계역학 · §3 중심 · §4 히스 · §5 폭 · §5b gr2L(v1.0.24 신규) · §6 평형 peak · §7 broadening · §8 lag · §9 tail · §10 합산 → Part T 열특성(`ch1v22_partT_divider` + `ch2_sec00~10`: 분배함수·config·vib/전자·Einstein·mixing·극한·가역발열·종합·방법·종결) → §18 입력(`ch1_sec18_inputs`) → 부록 A 부호검산·B 코드맵·C/D(`ch2_appA_traps`·`ch2_appB_codemap`)·E 자기일관 → `ch1v22_bib`. **Ch2 LCO** = `ch2v22_sec00_intro`·`ch2v22_notation`·sec11~17(intro·center·hys·decomp·elec·peak·16b omega·MSMR)·`ch2v22_bib`. **Ch3 Si·혼합** = `ch3v22_sec00_intro`·`notation`·sec01 map·sec02 cases·sec02b sifr·sec03 blend·sec04 mech·`\appendix` sec05 code·`ch3v22_bib`. 장간 `\externaldocument` xr 교차참조(빌드 순서 ch1→ch2→ch3→ch1 재패스; `ch1_graphite_v1.0.24.tex`:11).
- **문건의 자기 규정**(`_sections/ch1_sec00_intro.tex`): spine N0~N9(N0 입력 환산·N1 분극·N2 중심 $U_j(T)$·N3 히스 분기·N4/N5 폭·$\xi_\mathrm{eq}$·N6–N8 peak 모양·N9 합산), 세 층 = Part 0(분배함수 첫 원리) → Part I(흑연 곡선 사슬) → Part T(열), 관측 3인자(T·전위·C-rate)가 한 속도식 $k\simeq k_0\exp[-\Delta G_a/RT]$ 의 서로 다른 자리로 들어온다는 서론 명제(:37–40).
- **부록 E**(`_sections/ch1_appE_selfconsistent.tex`, 218줄): 참 문제 = 비선형 Volterra(Markov 지수핵)·동결 0차 = 가해 기준(eq:sc-ref) · 1차 ratio 닫힘(eq:sc-ratio) · 동결극한 정확 회수 · refs 6/7 5항 기록(①서지 ②논문 내 위치 — "페이지·문단 세부는 원문 대조로 확정" 유보 ③수학 구조 ④변수 매핑 ⑤가정 차) · 타당성 부등식(eq:sc-valid, $\varepsilon=2\chi_d(\Omega/RT)\Delta\xi_\mathrm{supp}$) · 전달함수 $H(\omega)=1/(1+i\omega L_V)$ · 구현 대응 지도. 적용 범위 = 동역학 지연에만(전하 보존 반전·배경 자기일관은 대수 근 — 명시 배제 warnbox :19–27). CLAUDE.md P1 의 "refs 6/7 실제 확인" 요구는 이 부록이 JCP147 자족 기술로 이행했고 원문(refs 6·7)은 미소장 상태다.
- **코드** `Anode_Fit_v1.0.24.py` = **1917줄** **[sub 실측 ✓]**(release 문자열 1.0.25 는 brief·A5 인용·미정독). doc-leads 정합·게이트 4종 GREEN·골든 bit-exact = A4 §②·§④ 인용(미재실행). **본 계획에서 코드는 Non-goal.**
- **v1.0.25 vs v1.0.25.1 차이** **[sub 실측 ✓ hash 대조]**: `_sections` 3파일 DIFF(`ch1_sec05_width`·`ch1_sec06_eqpeak`·`ch3v22_sec02b_sifr`) + 마스터 tex 3본 DIFF(표시 버전) · `appendix_phase_separation.tex` SAME · 코드 SAME. touch-up 4건(A4 §③) 매핑 = F1·F3 → sifr / M-w → sec05_width / L-bg → sec06_eqpeak. 식·라벨·boxed(39)·코드 불변(A4:49). ARCHIVE_NOTE·PDF 3종 차이는 미측정.

### 2.3 계보 (확정 — A2·A9·A12 근거)

5-28 구트랙 RB(전하보존 6장 → Ch1~5 통합 107p, `Claude/old/Archive_oldtrack` — ★동명이물 주의: `COMPARISON_*` 는 구트랙 기록, A9:10) → 6-10~12 Fable v2/v3(★Eyring 근본식 척추·200KB, A9:11) → Opus v4(§1.18 적층 준안정·athermal 훅, 순수 추가 158줄) / v5(수식-구동 장르 전환, 97식 verbatim·산문 32% 소거) / v6(흐름도 재조립, 손실 0) → 6-29 v7(코드 플로우차트 척추로 **의도 절삭** 17p) · v8(유도 4단 복원) · v9(LCO 전자 엔트로피) · v10(broadening 복원·w 이중지위·$w_\mathrm{eff}$ 제거) → 7-01 v1.0.10(코드-문건 동기) → 7-02 Fable 이력 감사(`docs/Fable_점검/` 8본) → v1.0.12(N=10 경쟁·체리픽) · v1.0.13(Part 0 신설·LCO Part II) · v1.0.14(Hill 유도·부록 A/B·그림 경연) · v1.0.15(격자 퇴출·점별 인과 기억 적분·★CLOSING 헌법 3종) · v1.0.16(n(T)) · v1.0.17(register·서지) · v1.0.18.1/.2(vib Einstein·로드맵 제안 2~5) → 7-08~13 v1.0.19(Fable 전면 재작성 Ch1+Ch2·Part II 7분할·doc-leads) → v1.0.20(서지 원장·품질 정정·동결) · v1.0.21(대정준 전하보존·TST bgbox·항법·Si 부록) · v1.0.22(★활물질별 3챕터 재편·계보 감사 ③=0건·CLT/CNT) → 7-18 v1.0.23(★JCP147 Fredholm ratio 부록 E·전달함수·고등수학 서베이) → 7-18~22 v1.0.24(공개데이터 검증 캠페인·@3 regsol/@5 stage-2L·XRD 상 판정·CODE_GUIDE) · v1.0.24.1(피드백 리비전 FB0~9 동결) → 7-26 v1.0.25(국소 수정: @2 skew opt-in·인과 pad·SI opt-in·regsol 삭제·FWHM $\lambda^{3/2}$) · v1.0.25.1(검증+touch-up·빌드) → 7-27 v1.0.26 A/B(regsol 재검증 조사, 실행 차단·미완).

Ch2 트랙(A9:16): v3 skeleton(5p) → v4 통계열역학(13p) → v5($w_\mathrm{eff}$ 파생 C 제거) → v1.0.10 동결 → v1.0.19 재작성 → v1.0.22 에서 Ch1 Part T 로 병합. 코드 트랙: v11_final(706줄) → v1.0.10(742줄) → … → v1.0.25(1917줄).

사용자 평(A12:3 verbatim): "v19=구문 최고·v23=논리 최고". v24 이후 = 사용자 피드백 집행, 품질 하락 0, 의도된 voice 평탄화(A12 §0·§3).

### 2.4 현재 구속력 있는 결정·제약 (초안 Non-goals·Assumptions 로 승계)

- **헌법 3종**(`docs/v1.0.15/CLOSING_v1.0.15.md` Part 1, 사용자 verbatim :9): ① 교과서 register(자기 diff·버전 이력 서술 금지 [D1] · 방어 어투 금지 [D2] · 내부 라벨·고백조 누출 금지 · 연속성) ② 논문 깊이(완결 유도·코너/극한/전제/tier A/B/C 정직 분리 · 실측 검증 vs 자기일관 검증 구분 · DOI 병기·1차 문헌 공백 정직 노출) ③ 수식-주도((a)출발식/전제 → (b)적용 연산 → (c)중간식 ≥1 → (d)박스, [D3] "대입하면 [박스]" 점프 0 · 보편식 먼저·극한은 코너 · 부호·차원·극한 검산 병기) + 공통 하위 규율(완결 문장·절 도입/마무리 다리·orphan 0·한글 prose + 영어 학술 원어·[D4~D6] 격자 잔재/대조 수식어/스위치 잔재 0·분량은 콘텐츠의 자연 결과).
- **CLAUDE.md P3 8항**(`CLAUDE.md`:30–46): ① $V_n$ 계열 구분 일관 ② 전하 보존식 = 내부 전위 결정 중심식 ③ 순환 의존 dependency graph ④ 4분류 진단(정의상 implicit / 수치해법 필요 / 논리 공백 / 물리 가정 충돌) ⑤ refs 6/7 5항 sub-section ⑥ Ch1 ↔ Ch2~5 전달 정합 ⑦ ver.N ↔ Chapter 명칭 혼동 금지 ⑧ **코드 = 부록 전용(본문 `_sections/*.tex` 코드 토큰 grep = 0)**.
- **사용자 피드백 F-01~F-11**(`results/comp_v24/USER_FEEDBACK_v1024_READING.md`, 집행 완료 FB0~9 · 규범으로 존속): F-01 §1.1.4 압축 · F-02 확률 $p$ 소문자(압력 $P$ 유지) · F-03 자리당 $f_\mathrm{int}/s_\mathrm{int}$ 소문자 규약(총량 $F,S$ 대문자와 구분 보존) · **F-04 전공서적 문체(전역·최우선·재발)** · F-05 제목 N-태그 제거 · F-06 조판(여백 25mm·줄간 1.16·문단 0.55em·microtype — `HANDOVER_v24.md`:82) · F-07 E.3 라벨 잘림 · F-08 LCO 도입 = 차이 선도 · F-09 식 2.39 cases 넘침 · **F-10 억지 한글화 금지(요동→fluctuation·양성→positivity 등, 정준/대정준은 사용자 판단)** · **F-11 코드 = 부록(전역·최우선·POLICY)**.
- **D-D 국소 원칙·DG-2 파일명 유지**는 v1.0.25 한정 규약(`plans/2026-07-26-v1025-surgical-skew-consistency-plan.md`:15·17). v2.0.0 은 새 폴더·새 파일명이 가능하나 **기존 `\label`·기호·식 번호 체계의 자산 무유실 원칙**(v1.0.22 계보 감사 ③=0건, `docs/INDEX.md`:33·38)은 승계한다. 자산 태그 `[A-xxx]`·`[E-xxx]` 체계 존재(sub 실측 159·8).
- **Ω 물리 전량 유효**(regsol 은 dQ/dV 커널만 삭제, `HANDOVER_v25.md`:136–137) · **gallery ≠ 상**(XRD 상 수 불변, :95–97) · **@2 α = 현상학 형상 파라미터(tier C)**(:74–77) · **$w_\mathrm{eff}$ 를 폭으로 읽기 금지**(:90–94·145–147) · **$C_\mathrm{bg}$ = 창-국소 상수 근사**(:101–102).
- **미완·미결**(`HANDOVER_v25.md` §② N4·N6~N9·N13 · `results/comp_v26_data/HANDOVER_regsol_investigation.md`): 흑연 두-상 4 vs 2 표기(Dahn 1991 본문 확인) · 신규 CSV 8종 리포 보존 · 재현 스크립트 등재 · regsol 철회 다중셀(n>1) 확인 · **skew-regsol 결합 커널 vs GITT 평형 데이터 판정(v1.0.26, 미실행)** · 회사 다온도 데이터 의존 정량(Task #38).

### 2.5 방향성 유실·park·미착수 (작업 챕터 1.4 등록부의 시드 — A9 §4·B1~B7)

Eyring 근본식 척추(Fable v2, 미계승 — A9:47) · 역방향 식별 사슬 S0~S5·16-울타리(v5/v6, v7 절삭 — A9:50) · §1.18 적층 준안정·athermal 훅(park — A9:51) · KWW/장벽분포 꼬리 일반형(scope-out·진단 prose gap — A9:52) · "자기완결 교과서 vs 필요한 식만" 두 지시의 긴장(A9:54) · 원구상 Chapter 2~5(발열·반응속도론·통합 상태방정식·히스테리시스 계층, `CLAUDE.md`:17 — 현행은 재료별 3장 + Part T 로 재편) · 로드맵 제안 2 Ω(ξ)·3 Cahn–Hilliard→$\gamma_j$·4 BV+Nernst–Planck·5 PSD(B1; 제안 1 vib Einstein 은 v1.0.18.2 구현 완료) · IMPROVEMENT #3 coupling·#4 정칙용액 자유에너지(B2; #1·#2 는 opt-in 반영됨) · LIT_ADVANCE ◐선검증군(G3 정칙용액+Maxwell·G5·L4~L6·S4·S5·M1·M4)과 ★반영준비군(G1·G2·L1~L3·S1~S3·M2·M3)의 집행 여부(B3) · SURV Tier2 Fisher/정합점근·Tier3 명명노트·기각군(B4) · SM2-A/B/C(B5 — **집행 여부 미확정**: brief §4.5 는 v1.0.25.1 §6·§2b·§2.7 에 "감수율·var(N)·앙상블 동등성" 18건 존재를 보고 → 작업 챕터 1.4 Step 9 에서 실물 확인) · anodefit 캠페인 B 전셀·C T/I/V·E 상태추론(B7 — 미착수; A·D 는 v1.0.24 V0~V3 로 착수, `results/V1024_EXECUTION_LEDGER.md`).

### 2.6 cumulative step 좌표

직전 arc(v1.0.25 계획)는 Step 1~31 로 종결(`plans/2026-07-26-v1025-…-plan.md` Phase P0~P4)·v1.0.26 조사는 ledger 없음(A7). 본 마스터 플랜은 **새 arc** 이므로 **Step 1 부터** 단조 누적한다(Phase 를 넘어도 리셋 없음). Step 이력 파일 = `Claude/results/Step <N> — <제목>.md`(step 하나 = 파일 하나).

### 2.7 구조 맵

```
D:\Projects\Project_Anode_Fit\
├─ CLAUDE.md                                   프로젝트 지침 P1~P5(89줄)
├─ Claude\
│  ├─ docs\
│  │  ├─ INDEX.md                              문건 MOC(197줄, v1.0.10→v1.0.25.1)
│  │  ├─ v1.0.25.1\  ★현행 최신(동결 base·무수정) — ch1/ch2/ch3 *_v1.0.24.tex · appendix_phase_separation.tex
│  │  │   · _sections\(56) · Anode_Fit_v1.0.24.py(1917) · test_gates_*.py · results\(HANDOVER_v25·v24·TOUCHUP_NOTE·INDEX_v25·tools_*.py …) · PDF 3
│  │  ├─ v1.0.25\    base(무수정 보존) · v1.0.24.1\ · v1.0.24\  동결 아카이브(비교 기준)
│  │  ├─ v1.0.15\CLOSING_v1.0.15.md            헌법 3종 · v1.0.18.2\ROADMAP_future_physics.md
│  │  ├─ v1.0.20\plans\(PLAN_P0~P8 + v1020 master) · v1.0.22\plans\(PLAN_R1/R2/R3/R5/RA/FR) · v1.0.22\results\comp_v23\SURV_SYNTHESIS.md · comp_SM2\SM2_SURVEY.md
│  │  ├─ Fable_점검\(8 md·885줄)               이력 전수감사
│  │  └─ v1.0.10~v1.0.24\ · _archive\          구버전(HANDOVER_* 각 폴더)
│  ├─ plans\  INDEX.md(65, 스테일) + 91 계획서(9503줄)
│  ├─ results\
│  │  ├─ V1024_EXECUTION_LEDGER.md · V1024_FEEDBACK_EXECUTION_LEDGER.md   12-col 실례
│  │  ├─ comp_v24\(USER_FEEDBACK·VERSION_COMPARISON·IMPROVEMENT_DIRECTIONS·LIT_ADVANCE_SYNTHESIS·sintef_data\ …)
│  │  ├─ comp_v26_data\(HANDOVER_regsol_investigation·test_skew_regsol.py …)
│  │  ├─ process\(ledger 26·HANDOVER 4 …) · research\(ledger 2)
│  │  └─ handoffs\2026-09-02-v2-master-plan\{brief.md, iter_1\{plan_draft.md, work_log.md}}   ← 본 유닛
│  ├─ old\Archive_oldtrack\(PHASE_DIAG_REFS67_DOSSIER.md · HANDOVER_RB_* 3)
│  ├─ JCP_147(14)_144111_(2017) - Effects of external electric field.pdf · jcp_extract.txt
└─ Codex\   ★무접근(읽기 포함)
```

**신규 예정(저작 시 생성 — 생성 시점에 이 맵을 즉시 갱신)**: `Claude/plans/2026-09-02-v2-master-plan.md`(master 최종 저장) · `Claude/plans/2026-MM-DD-v2-phase-<id>-plan.md`(Phase 가 큰 경우 별도 세부 계획서) · `Claude/results/Step <N> — <제목>.md` · `Claude/results/PHASE_<id>_V2_<topic>_RESULT.md`(+`.json`) · `Claude/results/PHASE_1-6_V2_EXECUTION_LEDGER.md` · 등록부·레지스터·블루프린트(§Implementation Changes 의 파일명 — 작업 sub 제안, master 확정) · `Claude/docs/v2.0.0/`(챕터 4.0) · `Claude/docs/HANDOVER_v2.0.0.md`(챕터 6.3).

### 2.8 이력 인벤토리 실측(작업 챕터 1.1 의 시드 — sub 읽기 전용 실측)

| 군 | 실측 | brief §3-C 표기 | 비고 |
|---|---|---|---|
| `Claude/plans/*.md`(INDEX 제외) | **91 파일 · 9503줄**(INDEX 65줄 포함 시 92·9568) | 90 파일·9567줄 | near-match(INDEX 포함 줄수 ±1). 1.1 Step 1 에서 정본화 |
| `Claude/docs/**/PLAN_*.md` | **15**(v1.0.20/plans 9 · v1.0.22/plans 6) + `docs/v1.0.20/plans/2026-07-16-v1020-master-plan.md` 1 | (미기재) | 페이즈 세부 계획서 실물 — 정독 범위(DR-7)에 포함해야 한다. 줄수 미실측 |
| `HANDOVER*.md` | **25**(old/ 제외) · **1612줄** / old/ 포함 28 | 28본(1612줄, old/ 제외) | brief 의 "28" 은 old/ 3본 포함 수, "1612줄" 은 old/ 제외 실측과 일치. `HANDOVER_v24.md` 는 v1.0.24·v1.0.24.1·v1.0.25·v1.0.25.1 네 폴더에 사본이 있어 실질 고유본은 더 적다(중복 판정은 1.1) |
| `docs/Fable_점검/*.md` | **8 · 885줄** | 8 | |
| `CLOSING*.md` | 1(`v1.0.15/CLOSING_v1.0.15.md`, 106줄) | 1 | |
| INDEX | `docs/INDEX.md` 197 · `plans/INDEX.md` 65 | 2 | |
| `Claude/results/**/*LEDGER*.md` | **30**(results 2 · process 26 · research 2) | "results 마스터 ledger 전건" | `docs/vN/results/` 안의 ledger(V1022·V1023·V1024_REFLECT·V1025_CHANGE 등)는 본 실측 밖 — 1.1 에서 추가 실측 |
| 정독 완료(초안 단계) | §3-A 14본 · §3-B 7본 · §3-C 마스터 tex 3본 전문 · INDEX_v25 전문 · V1024 ledger 부분(1–15행) | | Read Coverage = `work_log.md` |

**미검독(초안 단계에서 읽지 않은 것 — 추정 금지)**: plans 91 중 3본(A8·B6·B7)만 정독 · docs/**/PLAN_* 16본 전부 · HANDOVER 25 중 3본(A5·A6·A7)만 정독 · Fable 감사 8 중 1본(A9)만 · `_sections` 56 중 2본(A13·A14)만 · 코드 전문 · PDF 3종 · `comp_v24/` 나머지(FIT_CHECK·DATA_REGISTRY·ABLATION·GRAPHITE_STAGING_XRD·AUDIT·SOURCES 등) · `comp_v26_data/` 나머지(MULTI_DATASET_REVIEW·스크립트) · `docs/v1.0.25.1/results/` 나머지(MERGE_READINESS·CHANGE_LEDGER·DATA_ADDENDUM·DOC_EDIT_REPORT·T13_T14·CASCADE_TODO·REFLECT_SEED_TABLE·CODE_GUIDE·FITTING_GUIDE) · ledger 30 중 1본 부분 · dossier · `jcp_extract.txt` · JCP PDF · `_archive/` · `old/` 전부.

---

## Phase Range

> ★ **3축 대응 주석(P3 #7)**. 아래 "작업 챕터 1~6" 은 **본 계획의 작업 단위**이며, 문건의 "Chapter 1~3"(재료별: 흑연 / LCO / Si·혼합)과도, 역사적 "ver.1~ver.5"(`graphite_ica_dynamic_ver5.tex` 적층, `CLAUDE.md`:14)와도, `CLAUDE.md` P1 의 원구상 "Chapter 1~5"(전하보존 / 발열 / 반응속도론 / 통합 상태방정식 / 히스테리시스)와도 **다른 축**이다. 챕터 3.3 이 제안하는 새 문건 구조(예: Part I 일반 이론 + Part II 재료 적용)는 또 다른 축이며 3.7 에서 사용자가 결정한다. 보고서·이력에서 둘 이상을 함께 쓸 때는 "작업 챕터 N / 문건 Chapter N / ver.N / 원구상 Chapter N" 으로 명시한다.

| 축 | 단위 | 값 | 출처 |
|---|---|---|---|
| 작업 챕터(본 계획) | 1~6 | 이력 통합 / 진단 / 이론 설계 / 저작 / 서지 / 검수·마감 | brief §5 |
| 문건 Chapter(현행) | 1~3 | 흑연(+Part 0·Part T·부록 A~E) / LCO / Si·혼합 | 마스터 tex 3본 |
| 역사적 ver. | 1~5 | `graphite_ica_dynamic_ver5.tex` 적층 구조 | `CLAUDE.md`:14 |
| 원구상 Chapter | 1~5 | 전하보존 / 발열 / 반응속도론 / 통합 상태방정식 / 히스테리시스 | `CLAUDE.md`:15–17 |
| 후보 신구조(3.3) | (a)/(b) | (a) 재료별 3장 유지 + 내부 일반화 / (b) Part I 일반 이론 + Part II 재료 적용 | brief §5 3.3 · DR-3 |

| Phase | 이름 | Steps(cumulative) | 게이트 요지(정량) | 정지·결정 | 상태 |
|---|---|---:|---|---|---|
| **1.1** | 인벤토리·정독 배정 | 1–2 | 인벤토리 전건 path+줄수(Test-Path True 100%) · 정독 배정표 = 전문 정독 전부 | DR-7 | 대기 |
| **1.2** | 버전별 변경점 등록부(v3→v1.0.26) | 3–5 | 버전 행 30/30 누락 0(§2.3 목록 대조) · 8열(구조/물리/식/코드/게이트/결정/페이지/근거) 빈 셀 0 · 사용자 평 반영 | — | 대기 |
| **1.3** | 유효 결정·제약 등록부 | 6–7 | 헌법 3종·P3 8항·F-01~11·D/DG·용어·노테이션 전건 = 출처 path+line + verbatim + 상태{존속/v1.0.25 한정/폐기} | — | 대기 |
| **1.4** | 방향성 유실·park·미결 등록부 | 8–9 | §2.5 시드 전건 + 정독 발견분 · 각 항목 4열(원 지시 시점/현행 처리/재개방 후보/근거) 빈 셀 0 · SM2 집행 여부 실물 판정 | — | 대기 |
| **1.5** | Result — 챕터 1 | 10 | `PHASE_1_V2_HISTORY_RESULT.md`+`.json` · Ledger 행 · Read Coverage 행 범위 | — | 대기 |
| **2.1** | 자산 지도 | 11–12 | 카운트 표 = brief §4.2 와 일치(스크립트 재실행) · boxed 64 ID 표 · 두 버전 diff 3파일·touch-up 4건 판정 | — | 대기 |
| **2.2** | 유도 완결성 감사(기준 ①) | 13–16 | boxed 64/64 (a)(b)(c)(d) 판정 행 · 비약/누락/생략 목록(ID·파일·행·성격) · 청크 ≤~500줄·렌즈 follow+적대검산 | — | 대기 |
| **2.3** | 일반성·가정 사다리 감사(기준 ⑤) | 17–18 | 간소화 지점 등록부(가정·유효범위·레퍼런스 유무) · "일반식→특수식" 계보도 | — | 대기 |
| **2.4** | 서지 감사(기준 ③) | 19–20 | bibitem 95/95 검증 표 · 절별 인용 밀도(49 section) · 1차 문헌 공백 · 필수 문헌 체크리스트 대조 | DR-6 | 대기 |
| **2.5** | 형식·register 감사(기준 ②④) | 21–22 | 교재 형식 요소 체크표(절별) · F-04/F-10/F-11 잔존 grep 수치 · 가독성 판정 항목 분해 | — | 대기 |
| **2.6** | v1.0.26 regsol 미결의 설계 입력화 | 23 | 두-상 커널 문제 정식화(판정 기준·필요 데이터·현 근거) | DR-1·DR-6 | 대기 |
| **2.7** | Result — GAP REGISTER | 24 | `PHASE_2_V2_GAP_RESULT.md`+`.json` · GAP REGISTER 4-tier | — | 대기 |
| **3.1** | 후보 이론 조사·평가 | 25–28 | B1~B5 전건 흡수(재조사 0·기각군 승계) + 신규 검색 → 카탈로그(등급·모델차원·침습도·서지·선행 데이터) | DR-6 | 대기 |
| **3.2** | 통합 골격 설계("일반→특수" 사다리) | 29–32 | 열역학/동역학/열·히스 사다리 각 단계 가정+레퍼런스+회수 조건 · boxed 64/64 회수 매핑 | — | 대기 |
| **3.3** | 문건 구조 결정안 | 33–34 | (a)/(b) 장단·자산 이동 맵·xr 영향·페이지 추정 → DG-A 안건서 | (DG-A 예고) | 대기 |
| **3.4** | 수식 사슬 원형(derivation skeleton) | 35–37 | 새 구조 절별 목표 boxed + (a)~(d) 사슬 계획 + 신규/승계/회수 표시 · P3 #3 graph·#4 4분류 | — | 대기 |
| **3.5** | 레퍼런스 마스터 원장 설계 | 38 | 주제별 필수 문헌 맵·DOI 검증 절차·인용 규약 | DR-6 | 대기 |
| **3.6** | 설계 적대검토 | 39 | refute mandate·최약점 1곳·빈 통과 금지 | — | 대기 |
| **3.7** | Result — THEORY BLUEPRINT + ★정지 | 40 | md+json · **사용자 결정 게이트 DG-A/B/C 확정 전 저작 착수 금지** | ★정지 | 대기 |
| **4.0~4.9** | 저작 v2.0.0 | 41– | 절 단위 루프 · 빌드 게이트(xelatex 3-pass err 0·undefined 0·STRUCTURE PASS) · 본문 코드 토큰 0 · Phase 별 Result | 3.7 확정 후 세부화 | 대기 |
| **5.1~5.3** | 서지 완결 | (4 에 이어 연속 부여) | 원장 확장·DOI 전수 검증 · 인용 밀도·1차 문헌 매핑 · 서지 감사 Result | 3.7 확정 후 세부화 | 대기 |
| **6.1~6.3** | 검수·수렴·마감 | (5 에 이어 연속 부여) | 10R + 커버리지×렌즈 6종 완주 **둘 다** · P3 8항+헌법 3종+F 게이트 · 빌드 GREEN·PDF·HANDOVER·INDEX·commit·push | 3.7 확정 후 세부화 | 대기 |

> 챕터 4~6 의 Step 번호는 3.7 확정 후 세부 계획서 작성 시 41 부터 연속 부여한다(단조 누적·리셋 없음). Phase/step 수·범위는 최소 기준점이며 검토 필요 시 확장·신규 Phase 추가가 가능하다(silent 누락 금지·명시 deferral + Decision Queue 등재).

---

## Non-goals

> brief §6 그대로. 본 계획에서 **절대 하지 않는다**.

- **코드 동기(doc-leads)** — 문건 확정 후 **별도 플랜**(DR-4). 본 계획은 문건. 기존 코드(`Anode_Fit_v1.0.24.py`)는 읽기·실행(수치 대조 목적)만 허용하고 수정하지 않는다.
- `Claude/docs/v1.0.25/`·`v1.0.25.1/`·`v1.0.24*/` 수정 X(동결 base·비교 기준). `docs/v1.0.24/`·`v1.0.24.1/` 불가침(`HANDOVER_v25.md`:153–154).
- `Codex/` 접근 X(읽기 포함).
- 역문제·상태추론(anodefit 캠페인 E)·전셀 합성(캠페인 B) X.
- 회사 데이터 의존 정량(Task #38: stage-2L 0.30 mV/℃·Ω 점값·LCO 전자항 T-의존·α↔$L_V$ 율속 분리) X — 필요 항목은 warnbox·tier 로 정직 표기.
- 새 공개데이터 상시 파이프라인 X(단 2.6/3.1 판정에 **기존 확보 데이터**(`results/comp_v24/sintef_data/` 등) 재사용은 허용 · 신규 다운로드는 DR-6/Decision Queue).
- 효율을 이유로 정독·검수 하한을 낮추는 것 X(사용자 기준 6).

---

## Implementation Changes

> 비코드 프로파일: **산출물 변경 대장**. 파일명 중 brief §7 에 규정된 것(Step 이력·Result·Ledger·세부 계획서·핸드오프·인계·`docs/v2.0.0/`)은 규정대로, 규정에 없는 등록부·레지스터·블루프린트 파일명은 **작업 sub 제안**(기존 `Claude/results/V1024_*` 접두 관행 승계)이며 master 가 확정한다(work_log DQ-4).

| ID | 산출물 | 위치(제안 포함) | 생성/갱신 | 소유 Phase | 게이트 |
|---|---|---|---|---|---|
| P-0 | 마스터 플랜(본 문서의 최종본) | `Claude/plans/2026-09-02-v2-master-plan.md` | 생성(master) | — | 11-section 순서·이름 보존 · `plans/INDEX.md` 행 갱신 |
| P-1 | 페이즈별 세부 계획서 | 본 문서 Phase 절(챕터 1~3) / 챕터 4~6 = `Claude/plans/2026-MM-DD-v2-phase-<id>-plan.md` | 생성 | 각 Phase 착수 시 | Phase 착수 전 존재 · 매 Step 착수 시 재독 |
| R-1 | 이력 인벤토리 | `Claude/results/V2_HISTORY_INVENTORY.md`(제안) | 생성 | 1.1 | Test-Path 100% · 줄수 실측 · 정독 배정표 |
| R-2 | 등록부 ① 버전별 변경점 | `Claude/results/V2_REG1_VERSION_CHANGES.md`(제안) | 생성 | 1.2 | 30행 · 8열 빈 셀 0 |
| R-3 | 등록부 ② 유효 결정·제약 | `Claude/results/V2_REG2_BINDING_DECISIONS.md`(제안) | 생성 | 1.3 | 전건 path+line+verbatim+상태 |
| R-4 | 등록부 ③ 방향성 유실·park·미결 | `Claude/results/V2_REG3_LOST_DIRECTIONS.md`(제안) | 생성 | 1.4 | 시드 전건 + 4열 |
| R-5 | GAP REGISTER | `Claude/results/V2_GAP_REGISTER.md`(+`.json`, 제안) | 생성 | 2.1~2.7 | 4-tier · boxed 64 판정 · 서지 95 표 |
| R-6 | THEORY BLUEPRINT | `Claude/results/V2_THEORY_BLUEPRINT.md`(+`.json`, 제안) | 생성 | 3.1~3.7 | 카탈로그·사다리·구조안·skeleton·원장 설계·적대검토 · DG-A/B/C 안건서 |
| D-1 | 새 문건 v2.0.0 | `Claude/docs/v2.0.0/`(DR-2) — 마스터 tex·`_sections/`·프리앰블·bib·PDF | 생성 | 4.0~4.9 | 빌드 GREEN·STRUCTURE PASS·본문 코드 토큰 0 |
| D-2 | 서지 마스터 원장 | `Claude/docs/v2.0.0/results/V2_REFERENCE_LEDGER.md`(제안 — v1.0.20 `REFERENCE_LEDGER` 관행 승계) | 생성 | 3.5 설계 → 5.1~5.3 확장 | DOI 검증 100% · 기억 서지 0 |
| S-1 | 스텝 이력 | `Claude/results/Step <N> — <제목>.md` | 생성(step 하나=파일 하나) | 전 Step | 5항목(수행/근거·판단/변경·생성 파일/게이트/다음) |
| S-2 | Phase Result | `Claude/results/PHASE_<id>_V2_<topic>_RESULT.md` + `.json` | 생성 | 각 Phase 종료 | 12항목 · Read Coverage 행 범위 |
| S-3 | Ledger | `Claude/results/PHASE_1-6_V2_EXECUTION_LEDGER.md` | 생성·갱신 | 각 Phase 종료 | 12-col |
| S-4 | 핸드오프 | `Claude/results/handoffs/<task>/` | 생성 | 서브 스폰 시 | brief + iter_N |
| H-1 | 인계 | `Claude/docs/HANDOVER_v2.0.0.md` | 생성 | 6.3 | 5항목 + chain |
| I-1 | `Claude/docs/INDEX.md` | 갱신(행 추가 — 기존 행 무수정) | 갱신 | 6.3(및 v2.0.0 폴더 생성 시) | 본문이 진실·INDEX 갱신 |
| I-2 | `Claude/plans/INDEX.md` | 갱신(현재 활성 = v2.0.0 마스터 행 추가; 스테일 표기 정정은 별도 작업 — DQ) | 갱신 | P-0 저장 시 | |
| — | **불변** | `docs/v1.0.25/`·`v1.0.25.1/`·`v1.0.24*/` · 코드 · `Codex/` · `comp_v24/` 원본(정정은 addendum) · 이전 Result/Ledger/HANDOVER(immutable history) | 무수정 | — | 결과 문건 보호(Addendum/Supersession/Correction) |

---

## Phase 1.1 — 인벤토리·정독 배정 (Steps 1–2)

**목적.** 작업 챕터 1(이력 통합)의 정독 대상 전건을 실물로 고정하고, "효율을 이유로 축약하지 않는" 전문 정독 배정표를 만든다. 이것이 등록부 3종의 Read Coverage 근거가 된다.

**입력.** §2.8 실측 표 · `docs/INDEX.md` · `plans/INDEX.md`(스테일 — 실제 최신 = v1.0.25) · `docs/v1.0.25.1/results/INDEX_v25.md` · 세션 시작 git 스냅샷.

- **Step 1 — 인벤토리 파일 생성(R-1)**: 다음 군을 **전건 path + 줄수 + 버전 귀속 + 문서 종류**로 등재한다 — (i) `Claude/plans/*.md` 91 + `INDEX.md` (ii) `Claude/docs/**/PLAN_*.md` 15 + `docs/v1.0.20/plans/2026-07-16-v1020-master-plan.md` (iii) `HANDOVER*.md` 25(old/ 제외) + old/ 3(별도 표시·구트랙) — 동일 파일명 사본(`HANDOVER_v24.md` ×4 폴더)은 hash 로 중복 판정해 고유본만 정독 대상 (iv) `docs/Fable_점검/*.md` 8 (v) `CLOSING_v1.0.15.md` (vi) `docs/INDEX.md`·`plans/INDEX.md`·각 `docs/vN/results/INDEX_v*.md` (vii) ledger = `Claude/results/**/*LEDGER*.md` 30 + `docs/vN/results/*LEDGER*.md`(실측 필요) (viii) 각 버전 `MERGE_READINESS_*`·`CHANGE_LOG/LEDGER`·`PHASE_*_RESULT.md`(docs/vN/results 및 results/process) (ix) `results/comp_v24/*.md`·`results/comp_v26_data/*.md`·`docs/v1.0.22/results/comp_v23/*.md`·`comp_SM2/*.md`·`docs/v1.0.18.2/ROADMAP_future_physics.md` (x) `Claude/old/Archive_oldtrack/PHASE_DIAG_REFS67_DOSSIER.md`·`jcp_extract.txt`. 각 행에 **정독 여부(초안 단계 기정독 21본 표시)** 열을 둔다.
  - 명령(예시·재현 가능): `Get-ChildItem -Recurse -Filter '*.md' | ForEach-Object { "$($_.FullName)`t$((Get-Content $_.FullName).Count)" }` 를 위 (i)~(x) 각 경로에 적용, Test-Path 전건 True.
  - 증거: R-1 표 + 합계(파일 수·줄수) + 실측 명령 출력 첨부.
- **Step 2 — 정독 배정표**: R-1 의 전건을 **계보 순(§2.3)** 으로 정렬해 정독 순서·청크(≤~500줄 창, 최대 ~700; 800줄 미만 파일만 통째)·담당(작업 sub 직렬 — 유닛 1개)·Read Coverage 기록 양식(파일·행 범위)을 확정한다. **전문 정독 = 전부**(DR-7 기본값). 대안(DR-7 대안 채택 시)은 "마스터플랜·인계 전문 + 페이즈 세부 계획서는 구조 추출" 로 배정표를 다시 쓴다.
  - 게이트: 배정표의 파일 집합 = R-1 파일 집합(차집합 0) · 각 파일에 청크 경계(행) 명시 · 총 줄수 합계 = R-1 합계.

**게이트 1.1(정량).** R-1 Test-Path True 100% · 줄수 열 빈 셀 0 · 배정표 차집합 0. **중단 조건.** 인벤토리 군 (i)~(x) 중 실물 부재 군 발견 → 미검독·부재로 표기하고 진행(정지 아님). **다음 조건.** Step 1·2 이력 파일 저장.

## Phase 1.2 — 버전별 변경점 등록부 v3→v1.0.26 (Steps 3–5)

**목적.** 계보의 각 버전이 **무엇을 바꿨고(구조/물리/식/코드/게이트/결정/페이지) 그 근거가 어디에 있는지** 한 표로 고정한다. 이것이 챕터 3.2 자산 회수 매핑과 3.3 구조 결정의 이력 근거다.

**등록부 행(30, 누락 0 의 기준 집합).** RB(구트랙) · Fable v2 · v3 · v4(Opus) · v5 · v6 · v7 · v8 · v9 · v10 · v1.0.10 · v1.0.11 · v1.0.12 · v1.0.13 · v1.0.14 · v1.0.15 · v1.0.16 · v1.0.17 · v1.0.18.1 · v1.0.18.2 · v1.0.19 · v1.0.20 · v1.0.21 · v1.0.22 · v1.0.23 · v1.0.24 · v1.0.24.1 · v1.0.25 · v1.0.25.1 · v1.0.26 A/B. (Ch2 트랙 v3/v4/v5·코드 트랙은 각 행의 "구조" 열에 병기.)

**열(8).** 구조 / 물리 / 식(신설·삭제·라벨 증감) / 코드 / 게이트(빌드·구조검사·회귀) / 결정(D·DG·사용자 verbatim) / 페이지 / 근거 path(+line).

- **Step 3 — RB → v1.0.14**: `docs/Fable_점검/` 8본 전문 + 해당 구간 plans(2026-05-29~07-04)·HANDOVER(process/ 4·v1.0.10~v1.0.14)·ledger(process/ 해당) 정독 → 행 1~15.
- **Step 4 — v1.0.15 → v1.0.22**: `CLOSING_v1.0.15.md` · HANDOVER v1.0.15~v1.0.22 · plans(07-05~07-17) · docs/v1.0.20/plans 10 · docs/v1.0.22/plans 6 · ledger(V1015~V1019·docs/v1.0.20~22/results) 정독 → 행 16~24. v1.0.19 "구문 최고"·v1.0.22 계보 감사 ③=0건을 "결정" 열에 근거와 함께.
- **Step 5 — v1.0.23 → v1.0.26**: plans(07-18~07-26 6본) · HANDOVER v23·v24(+FB절)·v25·regsol 인계 · TOUCHUP_NOTE · MERGE_READINESS v24/v25 · CHANGE_LEDGER · DATA_ADDENDUM · V1024 ledger 2본 · comp_v24 문서군 · comp_v26_data 정독 → 행 25~30. v1.0.23 "논리 최고"·v24 이후 "품질 하락 0"(A12) 반영.

**게이트 1.2(정량).** 행 30/30 · 8열 빈 셀 0(근거 없는 셀은 "근거 미발견" 명기 = 빈 셀 아님) · 각 행 근거 path ≥1 · 사용자 평(v19·v23) 행에 A12 line 인용. **중단 조건.** 없음(부재 근거는 4-tier 로 표기). **다음 조건.** Step 3~5 이력 파일 + R-2 저장.

## Phase 1.3 — 유효 결정·제약 등록부 (Steps 6–7)

**목적.** v2.0.0 저작이 **반드시 지켜야 할 것 / v1.0.25 한정이라 풀리는 것 / 폐기된 것**을 출처 line 단위로 확정한다. 챕터 4 의 저작 게이트와 챕터 6.2 의 규범 게이트가 여기서 나온다.

- **Step 6 — 규범군**: 헌법 3종 + D1~D6 + 프로세스 규율 2-1~2-6(`CLOSING_v1.0.15.md` Part 1·2 전건) · CLAUDE.md P3 8항·P5 · F-01~F-11(각 항목 = 사용자 지적 verbatim + 집행 상태 FB0~9 = `results/V1024_FEEDBACK_EXECUTION_LEDGER.md`·`HANDOVER_v24.md` §6) · `HANDOVER_v25.md` §③ 다음 세션 주의 11항.
- **Step 7 — 결정군·규약군**: 버전별 결정(D-1~5·D21-1~6·D22-x·D-A~D-D·DG-1/DG-2·v1.0.23 D1~D5·v1.0.18 2-버전 등 — 각 HANDOVER·plans 에서 추출) · 용어·노테이션 규약(확률 $p$ 소문자·$f_\mathrm{int}/s_\mathrm{int}$·억지 한글화 금지 용어 표(FB3 집행 규약 `HANDOVER_v24.md`:83 — 요동/양성 → 영문(body 0) · 음함수/섭동/준위 → 국문 + 첫 병기 · 유일근 → "유일한 근"; 정준/대정준 = 사용자 판단 보류)·제목 N-태그 제거·조판 수치·기호표 `tab:notation` 규약·자산 태그 체계·서지 V1 키만 인용) · 파일명·xr 규약(DG-2 = v1.0.25 한정) · 데이터 프로토콜 규약(`gr.csv`=p-ocv·`si.csv`=p-ocvhold·comp_v24 원본 무수정·addendum 우선).
  - 각 행 = 출처 path+line + verbatim(있으면) + **상태 ∈ {존속 / v1.0.25 한정 / 폐기}** + v2.0.0 적용 방식(게이트 ID 예약).

**게이트 1.3(정량).** 전건 출처 line 존재 · 상태 열 3값 중 하나 · 빈 셀 0 · 헌법 3종·P3 8항·F-01~11 = 각각 3·8·11 행 존재. **중단 조건.** 두 통제문서 지시 모순 발견 → 더 제한적인 지시를 채택하고 DQ 등재(정지 아님; 사용자만 결정 가능한 blocking 이면 정지). **다음 조건.** R-3 저장.

## Phase 1.4 — 방향성 유실·park·미결 등록부 (Steps 8–9)

**목적.** 과거에 지시됐으나 계승되지 않은 방향, park 된 항목, 미착수 후보, 미결 사안을 **재개방 후보 여부**와 함께 고정한다. 챕터 3.1 후보 카탈로그의 시드이자 "재조사 0" 의 근거다.

- **Step 8 — 시드 전건 등록**: §2.5 항목 전건 = A9 §4 표 8행 · B1 제안 2~5(+제안 1 완료) · B2 #1~#4(+§4 정직 한계·§5 관찰 2) · B3 결정표 G1~G7·L1~L8·S1~S6·M1~M7 + §6 실측 + §7 정직 갭 5 · B4 Tier1(집행됨 v1.0.23 부록 E)·Tier2 2·Tier3 6·기각군 6·가정 충돌 1·역문제 군 · B5 SM2-A~E·(v)·축 B/C·flow-1~3 · B6 D1~D5(v1.0.23 결정 — P4 Tier2 실행 여부 등) · B7 캠페인 A~G · A5 N1~N13 · A7 §⑥⑧ · A6 §6 차기 옵션. 각 항목 = **원 지시 시점 · 현행 처리 상태 · 재개방 후보 여부{재개방/유지/폐기/DQ} · 근거 path**.
- **Step 9 — 정독 중 발견분 + 실물 확인**: (a) 1.2·1.3 정독에서 새로 발견한 유실·park 항목 추가. (b) **SM2-A/B/C 집행 여부 실물 판정**: `docs/v1.0.25.1/_sections/ch1_sec06_eqpeak.tex`·`ch1_sec02b_part0.tex`·`ch2_sec07_revheat.tex` 에서 "감수율|var(N)|앙상블 동등성|켤레" grep(brief §4.5 = 18건) → SM2_SURVEY §2 의 삽입처·핵심 수학과 대조해 집행/부분/미집행 판정. (c) B4 Tier2(Fisher·정합점근)·Tier3 명명 노트의 집행 여부를 `HANDOVER_v23.md`·v1.0.23 ledger 로 확인. (d) B3 ★반영준비군(G1·G2·L1~L3·S1~S3·M2·M3)의 v1.0.24 반영 여부를 `REFLECT_SEED_TABLE.md`·`HANDOVER_v24.md` 로 확인.

**게이트 1.4(정량).** 시드 전건 등재(항목 수 = Step 8 열거 합계, 누락 0) · 4열 빈 셀 0 · (b)(c)(d) 판정에 grep 수치·path 첨부. **중단 조건.** 없음. **다음 조건.** R-4 저장.

## Phase 1.5 — Result: 챕터 1 (Step 10)

- **Step 10**: `Claude/results/PHASE_1_V2_HISTORY_RESULT.md` + `.json`(12항목: Summary / Step Range 1–10 / Inputs / Files Created(R-1~R-4) / Files Updated / **Read Coverage(파일·행 범위 전건)** / Execution Evidence / Validation·Gate·Confirmed / Non-Changes / Open Issues / Decision Queue / Next=Step 11) · Ledger `PHASE_1-6_V2_EXECUTION_LEDGER.md` 행 1.1~1.5 · Phase audit(문서 렌즈셋: 사실 정합·출처/번호/카운트 일치·orphan 0·라벨·용어 잔존·follow·usability, 3-Pass).
- **게이트 1.5.** Result md+json 쌍 존재 · Read Coverage 합계 = 배정표 합계(차이 = 미검독 명시) · Ledger 행 5. **다음 조건.** Result 없이 챕터 2 진입 금지.

---

## Phase 2.1 — 자산 지도 (Steps 11–12)

**목적.** 진단의 기준 좌표계. 현행 두 버전의 자산을 기계 추출로 고정한다.

- **Step 11**: 카운트 스크립트(§Test Plan T-4)를 v1.0.25.1 빌드 세트 60 tex 에 재실행 → brief §4.2 표와 **전건 일치** 확인. `\boxed` 64 각각 = ID·파일·행·`\label`(있으면)·절·문건 Chapter·spine 노드(N0~N9/Part T/부록)·현행 지위(채택/해석적 기록/opt-in) 표. `\label` 429 목록·`\bibitem` 95 목록·distinct cite 93 목록을 기계 추출로 첨부(2.4·챕터 5·6 자산 무유실 게이트의 기준 파일).
- **Step 12**: v1.0.25 vs v1.0.25.1 diff = `_sections` 3파일 + 마스터 3 + (ARCHIVE_NOTE·PDF) hash 대조 확정 · touch-up 4건(F1/F3/M-w/L-bg) 각각의 행 범위·성격(산문 additive)·식/라벨 불변 판정. **DR-1 대안(v1.0.26 A/B) 채택 시** `results/comp_v26_data/` 두 산출의 자산 지도를 추가한다.

**게이트 2.1.** 카운트 표 = brief §4.2 (display 230·boxed 64·label 429·bibitem 95·cite 265/93·section 49·subsection 115·figure 28·table 20·박스 8종) 전건 일치 · boxed 표 64행 · diff 파일 집합 = {3+3} 확정. **중단 조건.** 카운트 불일치 → 원인(빌드 세트 정의) 규명 후 정본 확정(정지 아님). **다음 조건.** Step 11·12 이력.

## Phase 2.2 — 유도 완결성 감사(기준 ①) (Steps 13–16)

**목적.** "수식만으로 80~90% 이해" 기준을 **boxed 64 각각의 (a)출발식 → (b)연산 → (c)중간식 ≥1 → (d)박스 사슬** 존재 여부로 판정하고, 비약·누락·생략을 ID 로 등록한다.

**청크(§2.2-보 분포 기준, 각 ≤~500줄 창 — 실제 행 범위는 세부 계획서에서 확정).**

- **Step 13 — Ch1 곡선 사슬(sec01~sec10, boxed 27)**: 렌즈 = follow(앞에서 여기까지 따라올 수 있는가) + 적대검산(부호·차원·극한). 각 boxed 행 = (a)(b)(c)(d) 존재 O/X + 비약 ID.
- **Step 14 — Part T(ch2_sec00~10, boxed 10) + 부록 A/B/C/D/E + `appendix_phase_separation`(boxed 7)**: 같은 판정. 부록 E 는 P3 ⑤ 5항 sub-section 존재 확인 + ②항 "페이지·문단 세부 유보" 를 GAP 으로 등록.
- **Step 15 — Ch2 LCO(sec11~17, boxed 16)**: 같은 판정 + Ch1 결과식 xr 참조의 사슬 단절 여부(참조만 하고 유도를 건너뛰는 지점).
- **Step 16 — Ch3 Si·혼합(boxed 4) + 비박스 display 식 중 사슬 핵심(스크리닝)**: boxed 외 display 166(=230−64) 중 "결과식으로 쓰이나 박스가 없는 식" 을 스크리닝해 목록화(전수 판정은 아니고 후보 등재 — 챕터 3.4 에서 목표 boxed 로 승격 검토).

**게이트 2.2.** boxed 64/64 판정 행 · 비약/누락/생략 목록 = ID·파일·행·성격{점프(D3)/중간식 부재/전제 미명시/차원·부호 검산 부재/참조 단절} · 청크 창 ≤~700줄 · 두 렌즈 각 1회 이상. **중단 조건.** 없음(발견은 GAP 이지 정지 아님). **다음 조건.** Step 13~16 이력.

## Phase 2.3 — 일반성·가정 사다리 감사(기준 ⑤) (Steps 17–18)

**목적.** 현행 문건이 **어디서 일반식을 특수식으로 간소화했는지**, 그 가정·유효범위·레퍼런스가 명시돼 있는지를 등록한다. 챕터 3.2 사다리 설계의 진단 입력.

- **Step 17 — 간소화 지점 등록부**: 후보 예(원천에 기록된 것만 — 정독에서 확정): lattice gas 이상 → 정칙용액 Ω 상수 → 로지스틱(Ω=0·MSMR 동형, B2 §1) · Ω 상수 vs Ω(ξ)(B1 제안 2) · $L_V$ 동결(부록 E eq:sc-frozen) · $C_\mathrm{bg}$ 창-국소 상수 · 등온/점별 $T(V)$ · 단일 입자·PSD 배제(B1 제안 5) · 대칭 종 α=1(skew 는 tier C) · 두-상 폭 = 현상학 자유 피팅(폭 이중지위) · $R_n$ lumped(B1 제안 4) · 히스 $\gamma_j$ 현상학(B1 제안 3) · 전자항 토글 · 대정준↔정준 동등성(SM2-B) · 각 항목 = 위치(파일·행·라벨)·가정 문장 verbatim·유효범위 명시 여부·레퍼런스 유무(V1 키)·tier.
- **Step 18 — "일반식 → 특수식" 계보도**: 등록부를 그래프/표로 재배열(뿌리 = 가장 일반적인 식, 잎 = 현행 boxed) + 각 간선에 가정 ID. 레퍼런스 없는 간선·유효범위 없는 간선을 GAP 으로.

**게이트 2.3.** 등록부 각 행 6열(위치/가정/유효범위/레퍼런스/tier/GAP) 빈 셀 0 · 계보도의 잎 = boxed 64 전건 포함(누락 0). **다음 조건.** Step 17·18 이력.

## Phase 2.4 — 서지 감사(기준 ③) (Steps 19–20)

- **Step 19 — bibitem 95 검증 표**: 각 항목 = 키·저자·저널·권·쪽·연도·DOI·검증 방법(Crossref/원문/미검증)·검증 결과·1차/2차 문헌 구분. 외부 접근은 **DR-6 기본(읽기 전용 허용)** 하에 Crossref 조회; 불허 시 "미검증" 으로 정직 표기.
- **Step 20 — 인용 밀도·공백**: section 49 × cite 호출 265 의 절별 밀도 표 · 인용 0 인 절 목록 · 결과식 boxed 64 중 1차 문헌 인용 없는 식 목록 · 리뷰급 주제별 필수 문헌 체크리스트(열역학 삽입 등온선·정칙용액/Frumkin·staging·MSMR·TST/Eyring·BV·Marcus·Nernst–Planck·Onsager·Cahn–Hilliard·CNT·Preisach·엔트로피/가역발열·Bernardi·Fredholm/Volterra — 체크리스트 자체는 챕터 3.5 에서 설계, 여기서는 **현행 95 대비 공백 스크리닝**) 대조.

**게이트 2.4.** 95/95 행 · DOI 열 값 ∈ {검증 DOI / DOI 없음(서지 확인) / 미검증} · 절별 밀도 표 49행 · 공백 목록. **다음 조건.** Step 19·20 이력.

## Phase 2.5 — 형식·register 감사(기준 ②④) (Steps 21–22)

- **Step 21 — 교재 형식 요소 체크표**: 절별(49 section·115 subsection)로 정의·정리(또는 명제)·유도·예제(worked example)·요약·기호표·다리(도입/마무리) 존재 O/X. F-04/F-10/F-11 잔존 grep: F-11 = 비부록 `_sections/*.tex` 코드 토큰(`\code{`·`\texttt{`·`func_`·`solve_U_oc`·`_regsol`·클래스명) 카운트(기준 0) · F-10 = 요동/양성/유일근 카운트(기준 0) + 음함수/섭동/준위 첫 출현 병기 여부(FB3 규약 `HANDOVER_v24.md`:83) + 정준/대정준 카운트만(판단 보류) · F-04 = 물음형 제목·"까닭"·"곳"·"진짜" 등 F-04 표의 패턴 카운트 + 수동 판정.
- **Step 22 — 타전공 석박사 가독성 판정(정성 → 항목 분해)**: 각 절에 대해 (i) 전제 개념이 앞에서 도입됐는가 (ii) 기호 첫 등장에 정의가 있는가(`tab:notation` 대조) (iii) 두문자어 첫 출현 병기 (iv) 절 도입/마무리 다리 (v) 극한·코너·tier 표기 — 5항목 O/X 표.

**게이트 2.5.** 체크표 49(+115)행 · grep 수치 3종 첨부 · 가독성 5항목 표 빈 셀 0. **다음 조건.** Step 21·22 이력.

## Phase 2.6 — v1.0.26 regsol 미결의 설계 입력화 (Step 23)

**목적.** "두-상 커널 문제"를 **결정하지 않고** 판정 기준·필요 데이터·현 근거를 정식화해 챕터 3.1(후보 평가)·3.2(사다리)의 입력으로 넘긴다.

- **Step 23**: 세 후보 커널(정칙용액+Maxwell 공존 / 로지스틱 gallery 세분 / skew-regsol 결합)에 대해 — (i) 현 근거: B3 §6(SINTEF 흑연 4전이: 로지스틱 R² 0.938 vs 정칙용액+Maxwell 0.943, $\Omega_j/RT=[4.06,2.02,3.55,4.07]$ 전부 >2RT·Cordoba DFT 앵커 ~2.5RT 정합 · "R² 개선 미미·가치는 파라미터 물리성") · `HANDOVER_v25.md`:85–89(@3 이득 역전 +0.97→−0.53 %p·gallery 중복) · B2 §3b(near-delta 천장 R²≈0.95–0.96 = MSMR 구조 한계·해법 #4) · A7(skew-regsol 결합 **미실행**·"개판 피팅" 원인 = 데이터 프로토콜·GITT/hold 평형 데이터 필요·소재별 커널 갈림: 흑연 두-상 / Si 연속 고용체 / 블렌드 중첩) (ii) 판정 기준: 피크·벨리 개형 지표(R² + 피크역 RMSE + 벨리역 RMSE, `HANDOVER_v25.md`:42)·파라미터 물리성(Ω 해석 가능·DFT 앵커)·XRD 상 수 불변·다중셀 n>1 (iii) 필요 데이터: GITT/p-OCV+hold 평형(SINTEF Zenodo 20086298 — 기확보 CSV 재사용 허용, 신규 다운로드 = DR-6) (iv) 실행 경로: `results/comp_v26_data/test_skew_regsol.py`(준비 완료·미실행, A7 §⑤) — 본 계획에서 실행할지는 DR-6·Decision Queue (v) DR-1 의 해석과 무관하게 이 항목이 흡수됨을 명시.

**게이트 2.6.** 정식화 문서에 (i)~(v) 전항 · 수치는 원천 path+line 인용(새 수치 생성 0). **다음 조건.** Step 23 이력.

## Phase 2.7 — Result: GAP REGISTER (Step 24)

- **Step 24**: R-5 `V2_GAP_REGISTER.md`(+`.json`) = 2.1~2.6 산출 통합 · 각 GAP = ID·기준(①~⑤)·위치·성격·4-tier·챕터 3 인계 여부 · `PHASE_2_V2_GAP_RESULT.md`+`.json` · Ledger 행 2.1~2.7 · Phase audit 3-Pass.
- **게이트 2.7.** GAP 전건 4-tier 라벨 · Read Coverage(2.2~2.5 정독 행 범위 = v1.0.25.1 9214줄 전 영역 cover) · md+json 쌍. **다음 조건.** Result 없이 챕터 3 진입 금지.

---

## Phase 3.1 — 후보 이론 조사·평가 (Steps 25–28) ★핵심

**목적.** 열역학·통계역학·동역학·히스테리시스·열의 다섯 축에서 **진보 후보를 카탈로그화**하되, 기존 서베이(B1~B5)를 전건 흡수해 재조사 0·기각군 승계로 시작한다.

**축과 시드(brief §5 3.1 verbatim 승계).**
- 열역학: lattice gas → 정칙용액(regular solution) → Ω(ξ)/Redlich–Kister → sublattice/staging → Cahn–Hilliard/phase-field.
- 통계역학: 대정준(grand canonical) · 요동-응답 SM2-A/B/C · transfer matrix staging.
- 동역학: Eyring/TST 척추 · Butler–Volmer · Marcus · Nernst–Planck · Onsager 선형 비가역 열역학 · master equation/Fokker–Planck · KWW/장벽분포 · Fredholm ratio.
- 히스테리시스: spinodal · CNT(classical nucleation theory) · Preisach.
- 열: entropy production · Bernardi.

**승계 표(재조사 0 의 기준 — 1.4 등록부 R-4 에서 확정된 상태를 그대로 가져온다).** 집행 완료군(재조사 X): 제안 1 vib Einstein(v1.0.18.2) · #1 gallery opt-in·#2 α opt-in(v1.0.24/25) · Tier1 Fredholm ratio+전달함수(v1.0.23 부록 E) · DIRECTION (i)~(iv)(대정준 유도·TST bgbox·CLT·CNT, v1.0.21/R2) / 기각군(승계·재조사 X): Wiener–Hopf·WKB·다중척도·중심다양체·Langevin·Preisach 연산자 채택(B4) · G6 전이 6+ 증설·G7 DFT 결합E→Ω 대입·L7 diffthermo LCO 파라미터·L8 double-Gaussian·S6 역학결합·M6 PDE 생성기·M7 비대칭 커널 문헌 주장(B3) · (v) $w_\mathrm{eff}(\Omega)$ 각주(B5 보류) · 축 B staging 미시화·축 C Jarzynski/Crooks(B5 범위 밖) / 가정 충돌 경고군: Kubo 동적 χ(B4) / 별도 스코프: 역문제 군(Tikhonov·MaxEnt·볼록최적화 — Non-goal) / 개방 후보군(평가 대상): 제안 2~5(B1) · #3 coupling·#4 정칙용액 자유에너지(B2) · ◐선검증군 G3·G5·L4~L6·S4·S5·M1·M4 + ★반영준비군 중 미반영분(B3) · Tier2 Fisher·정합점근/Watson·Tier3 명명 노트(B4) · SM2-A/B/C(B5, 집행 여부 = 1.4 판정) · Eyring 척추·S0~S5·§1.18·KWW(A9 §4).

- **Step 25 — 승계 표 확정 + 카탈로그 초판**: R-4 와 위 승계 표를 대조해 후보 항목 = ID·축·출처(B1~B5/A9)·기존 등급·현행 상태·본 계획 지위{개방/기각 승계/완료 승계}.
- **Step 26 — 신규 문헌 검색(축별)**: DR-6 기본(읽기 전용 허용) 하에 축별 검색 → 후보 추가. 서지는 DOI/원문 링크 확인된 것만 등재(기억 서지 0). 불허 시 기존 서베이 서지(B3 §서지 요약 등)만으로 진행하고 "신규 검색 미수행" 정직 표기.
- **Step 27 — 평가**: 각 후보 = 등급(A/B/C·B3 4-tier 규약 승계 ★/◐/○/✗) · 모델 차원(신규 파라미터 수) · 침습도(Part 0 코어/N1~N9 노드/부록) · 서지(DOI) · 선행 데이터 자기완결 여부 · 기준 1~5 기여 · 회수 조건(기존 boxed 로 환원되는 극한).
- **Step 28 — 축별 정리**: 다섯 축 각각 "일반식 후보 → 현행 특수식" 대응 예비표(3.2 입력).

**게이트 3.1.** 카탈로그 = 승계 표 항목 전건 포함(누락 0) + 신규 항목 각 서지 DOI/링크 · 평가 열 7 빈 셀 0 · 기각군 재조사 0(기각군에 재평가 행 없음). **중단 조건.** 없음. **다음 조건.** Step 25~28 이력.

## Phase 3.2 — 통합 골격 설계: "일반 → 특수" 사다리 (Steps 29–32)

**목적.** 사용자 기준 5 의 핵심. **가장 일반적인 식에서 출발해 가정을 하나씩 얹어 현행 boxed 식으로 내려오는 사다리**를 설계하고, 각 단(rung)에 가정·레퍼런스·회수 조건을 붙인다. 기존 boxed 64 가 사다리의 어느 단에서 회수되는지 매핑해 자산 무유실을 설계 단계에서 보장한다.

- **Step 29 — 열역학 사다리**: 일반 비평형 열역학 상태식(affinity·flux–force, Onsager) → 준평형(local equilibrium) → 평형 자유에너지(lattice gas 일반 → 정칙용액 Ω(ξ) → Ω 상수 → Ω=0 로지스틱) → Nernst/OCV → 평형 peak. 각 단 = 가정 문장·레퍼런스(3.1 카탈로그 키)·회수 조건(예: Ω→0 에서 eq:eqpeak 정확 회수)·현행 boxed 회수 목록.
- **Step 30 — 동역학 사다리**: 일반 TST/Eyring(척추 — A9 §4 미계승분 재개방 여부는 DG-B) → master equation/Fokker–Planck → Butler–Volmer/Marcus 전하 이동 → Nernst–Planck 수송 → lag(Volterra 참 문제, eq:sc-true) → 1차 ratio → 동결 $L_V$ → $L_V\to0$ 평형 극한. 각 단 = 가정·레퍼런스·회수 조건.
- **Step 31 — 열·히스테리시스 사다리**: entropy production(비가역) → 가역 발열(Bernardi) → 엔트로피 세 분포 분해(config/vib/전자) → Einstein/FD 코너 / spinodal·CNT·Preisach → 히스 gap·$\gamma_j$. 회수 조건 포함.
- **Step 32 — 자산 회수 매핑표**: boxed 64 각각 → 사다리 단(축·단 번호)·회수 조건·신규/승계/회수 표시. 회수되지 않는 boxed 가 있으면 "설계 GAP" 으로 등재(무유실 위반 예고).

**게이트 3.2.** 사다리 3축 각 단 = 가정·레퍼런스·회수 조건 3열 빈 셀 0 · 매핑표 64/64 · 회수 불가 항목 0(또는 설계 GAP 명시). **중단 조건.** 없음. **다음 조건.** Step 29~32 이력.

## Phase 3.3 — 문건 구조 결정안 (Steps 33–34)

**목적.** DG-A 의 안건서. 결정은 하지 않는다.

- **Step 33 — 두 안 비교**: (a) 현행 재료별 3장 유지 + 각 장 내부 일반화 vs (b) Part I 일반 이론(열역학·통계역학·동역학·열·히스테리시스) + Part II 재료 적용(흑연·LCO·Si·블렌드). 각 안 = 장단 · 자산 이동 맵(`_sections` 56 파일 → 새 위치) · xr 교차참조 영향(`\externaldocument` 재설계) · 페이지 추정(현행 102/30/22 대비 — "추정" 표기) · CLAUDE.md P1 원구상 Chapter 1~5 와의 대응 · 사용자 기준 1~5 정합.
- **Step 34 — 안건서**: 3.2 사다리와 (a)/(b) 의 정합도 · master 사전 선호((b) — brief §8 DR-3, master 판단) 의 근거 · 권고안 + 대안 + 비용.

**게이트 3.3.** 두 안 각 6항목 빈 셀 0 · 자산 이동 맵 56/56. **다음 조건.** Step 33·34 이력. (결정은 3.7)

## Phase 3.4 — 수식 사슬 원형(derivation skeleton) (Steps 35–37)

- **Step 35**: 새 구조(3.3 권고안 기준·확정 시 갱신) 절별 **목표 boxed 식** 목록 + 각각 (a)출발식 (b)연산 (c)중간식 (d)박스 사슬 **계획**(실제 유도는 챕터 4).
- **Step 36**: 각 목표 식 = 신규(카탈로그 키) / 승계(현행 boxed ID) / 회수(사다리 단) 표시 · 자산 태그 예약.
- **Step 37**: **P3 #3** 순환 의존 dependency graph($\xi_j$·$Q_\mathrm{bg}$·dQ/dV·dV/dQ·$U_\mathrm{oc}$·$L_V(\xi)$)와 **P3 #4** 4분류(정의상 implicit / 수치해법 필요 / 논리 공백 / 물리 가정 충돌) 진단 갱신 — 부록 E 의 현행 분류(전하 보존 반전 = 대수 근 / lag = Volterra / 배경 = 대수 순환)를 새 구조에서 재표시.

**게이트 3.4.** 목표 boxed 목록 · 사슬 계획 4열 · 신규/승계/회수 표시 100% · dependency graph 1본 + 4분류 표. **다음 조건.** Step 35~37 이력.

## Phase 3.5 — 레퍼런스 마스터 원장 설계 (Step 38)

- **Step 38**: 주제별 필수 문헌 맵(리뷰급 — 3.1 축 × 3.2 단) · DOI 검증 절차(Crossref 조회·원문 대조·미검증 표기 규약) · 인용 규약(V1 키만·기억 서지 금지·1차 문헌 우선·tier 병기) · 현행 95 + 2.4 공백 + 3.1 신규 → 원장 초판 골격(D-2).

**게이트 3.5.** 문헌 맵 축×단 셀 빈 칸 0(공백은 "공백" 명기) · 절차 문서 · 규약 문서. **다음 조건.** Step 38 이력.

## Phase 3.6 — 설계 적대검토 (Step 39)

- **Step 39**: 3.1~3.5 산출 전체를 검수 sub(Fable 5.1)가 **refute mandate** 로 검토 — 최약점 1곳 지목·빈 통과 금지 · 렌즈 = 구조·적대검산·follow·완결성 · A9 교훈 3("설계서 자체를 검증 대상으로") 적용 · master 삼각검증 후 수정.

**게이트 3.6.** 검수 보고서(최약점 ≥1·발견 건 4-tier) · master 수정 이력 · 재검 1R. **다음 조건.** Step 39 이력.

## Phase 3.7 — Result: THEORY BLUEPRINT + ★사용자 결정 정지 (Step 40)

- **Step 40**: R-6 `V2_THEORY_BLUEPRINT.md`(+`.json`) · `PHASE_3_V2_BLUEPRINT_RESULT.md`+`.json` · Ledger 행 3.1~3.7 · **DG-A 문건 구조 / DG-B 채택 이론 목록 / DG-C 버전 라벨(DR-2 재확인)** 안건을 평문으로 제시하고 **정지**(사용자만 결정 가능한 blocking). 확정 전 챕터 4 착수 금지. 확정 뒤 챕터 4~6 세부 계획서를 작성한다(Correction History 에 재baseline 기록).

---

## Phase 4.0~4.9 — 저작 v2.0.0 (Steps 41– ; 3.7 확정 후 세부 계획서 작성)

> 기본 골격 = 3.3 (b) 기준(확정 시 갱신). 각 Phase = **절 단위 루프**(정독 → 구성 → 자체검수 → 앞 절 정합 → 빌드 → ledger) + 빌드 게이트(xelatex 3-pass err 0·undefined ref/cite 0·STRUCTURE PASS) + 본문 코드 토큰 0 + Phase Result. 통째 배치 Write 금지(A9 교훈 1·헌법 ①③).

| Phase | 이름 | 내용(목록) | 게이트 |
|---|---|---|---|
| 4.0 | 골격·프리앰블·기호표·빌드 baseline | `Claude/docs/v2.0.0/` 생성 · 마스터 tex(파일명 = DG-C) · `_sections/` 골격 · 공통 프리앰블(F-06 조판 승계) · 기호표(`tab:notation` 승계 + 신규) · 라벨 네임스페이스 계획(기존 429 보존/매핑표) · 빈 절 빌드 | xelatex 3-pass err 0 · STRUCTURE PASS · 라벨 매핑표 429/429 |
| 4.1 | 열역학·통계역학 기초(일반식) | 사다리 뿌리: 분배함수·앙상블·요동-응답(SM2 결정분)·비평형 상태식 | (a)~(d) 사슬 100% · 코드 토큰 0 · 빌드 |
| 4.2 | 평형 열역학 | 중심·폭·상분리·정칙용액/Ω(ξ)·staging·Maxwell·spinodal | 회수 조건 검산(Ω→0 등) · 빌드 |
| 4.3 | 동역학 | TST/Eyring·BV·(Marcus·Nernst–Planck = DG-B)·lag·tail·Fredholm ratio·전달함수 | 동결극한 회수 · 빌드 |
| 4.4 | 열특성 | 엔트로피 세 분포 분해·가역발열·entropy production | Part T 자산 회수 · 빌드 |
| 4.5 | 히스테리시스 | spinodal·CNT·(Preisach 명명)·$\gamma_j$ | 빌드 |
| 4.6 | 흑연 적용 | Part II 첫 장(현행 Ch1 곡선 사슬 회수·gr2L·gallery≠상) | boxed 회수 27/27 · 빌드 |
| 4.7 | LCO 적용 | 현행 Ch2 회수(차이 선도 F-08) | 16/16 · 빌드 |
| 4.8 | Si·블렌드 적용 | 현행 Ch3 회수·regsol 지위(2.6·DG-B 결과) | 4/4 · 빌드 |
| 4.9 | 부록 | 기호·부호검산·코드맵(코드 = 부록 전용)·자기일관(부록 E 승계·refs 6/7 5항)·상분리 | 부록 7/7 · P3 ⑤ 5항 · 빌드 |

## Phase 5.1~5.3 — 서지 완결 (3.7 확정 후 세부화)

| Phase | 내용 | 게이트 |
|---|---|---|
| 5.1 | 원장 확장·DOI 전수 검증 | 원장 전건 DOI 검증 ∈ {검증/DOI 없음 확인/미검증} · 기억 서지 0 |
| 5.2 | 인용 밀도·1차 문헌 매핑 | 절별 밀도 표 · 결과식마다 1차 문헌 ≥1 또는 "공백" 명기 |
| 5.3 | 서지 감사 Result | `PHASE_5_V2_BIB_RESULT.md`+`.json` · Ledger |

## Phase 6.1~6.3 — 검수·수렴·마감 (3.7 확정 후 세부화)

| Phase | 내용 | 게이트(정량) |
|---|---|---|
| 6.1 | 가변 청크 검수 | **10라운드 + 커버리지×렌즈 6종(구조·적대검산·follow·usable·완결성·regression) 완주 둘 다 충족**(고가치 reference 등급) · 매 라운드 청크 스킴·렌즈 전환 · coverage missing 0 · 수렴 = 연속 2R 확정결함 0 · **실행 기반 검증 렌즈**(SymPy 재유도·수치 극한·기존 코드로 회수 가능한 식의 수치 대조 — 코드 수정 없이) |
| 6.2 | 규범 게이트 | CLAUDE.md P3 8항(각 항 확인 가능 조건으로) + 헌법 3종(D1~D6 grep/수동 분해) + F-04/F-10/F-11 grep 0 |
| 6.3 | 마감 | 빌드 GREEN·PDF · `Claude/docs/HANDOVER_v2.0.0.md` · `docs/INDEX.md`·`plans/INDEX.md` 갱신 · commit·push(master) · `PHASE_6_V2_CLOSING_RESULT.md`+`.json` · Ledger |

---

## Implementation Interfaces

> 비코드 프로파일: **운용**(모델·유닛·기록·재독·정지·git·구조 맵·검수 강도·스크립트 인터페이스).

- **모델** = **전원 Fable 5.1**(master·분석·저작·검수·감사 서브 전부 — 사용자 명시 예외; 헌법 배분표의 예외). 지정 모델 런타임 장애 시 silent substitution 없이 정지·보고.
- **유닛** = master + 작업 sub + 검수 sub, **직렬**. 동시 산 서브 ≤1. 병렬(fan-out)은 DR-5 sign-off 시에만 · 미승인 병렬 필요는 안 묻고 직렬 진행 + Decision Queue 기록.
- **역할 경계** = master: 맥락·계획·통합·최종 판단·commit / 작업 sub: 지정 산출물 구성 + 자체검수 / 검수 sub: refute mandate·최약점 1곳·빈 통과 금지 / master 삼각검증 후 직접 수정.
- **sub prompt 5항목 고지** = 역할 · 분업 경계(담당 범위·commit 권한) · 범위 밖 자의 금지 · 허위 attribution 금지 · 필요 memory 맥락 주입.
- **기록** = 스텝 이력 `Claude/results/Step <N> — <제목>.md`(step 하나 = 파일 하나 · 5항목 · 즉시 기록) · Result `Claude/results/PHASE_<id>_V2_<topic>_RESULT.md`+`.json`(12항목) · Ledger `Claude/results/PHASE_1-6_V2_EXECUTION_LEDGER.md`(12-col) · 세부 계획서 = 마스터 내 Phase 절 또는 `Claude/plans/2026-MM-DD-v2-phase-<id>-plan.md` · 핸드오프 `Claude/results/handoffs/<task>/` · 인계 `Claude/docs/HANDOVER_v2.0.0.md`.
- **재독 강제** = 매 Phase 착수 시 마스터 플랜 본문 재독(첫 Step 이력에 `[Phase N 착수 — 마스터 플랜 재독]` 기록) · 매 Step 착수 시 세부 계획서 재독 · 매 Phase 종료 시 Result 12항목 + Ledger(Result 없이 다음 Phase 금지) · 컴팩션·재개 직후 5-check(직전 Result·마스터플랜·현재/직전 단위 재정독·계획 step 대조·분량 급감 확인).
- **정지 조건** = 파괴·비가역 · 사용자만 결정 가능한 blocking(**3.7 DG-A/B/C**) · 권한 부족 · 보호영역 침범 · 새 의존성 · confirmed FAIL gate · 사용자 stop · 통제문서 모순. **병렬 승인 필요는 정지 사유 아님**(직렬·DQ). DQ 항목은 blocker 아님.
- **git** = 각 Step/Phase 종료 commit(master 전용) · push 는 Phase 종료 시 · merge X · 파괴·비가역 직전 commit(복원 지점) · 삭제·덮어쓰기는 git 안에서도 평문 사전 확인.
- **구조 맵** = §2.7. 폴더·파일 추가·삭제·이동·이름변경 시 그 자리에서 즉시 갱신(갱신 없으면 미완).
- **검수 강도** = A1·A2 고가치 reference: 10R + 6렌즈 완주 둘 다(챕터 6.1) · 챕터 1~3 산출물(등록부·레지스터·블루프린트): 검수 sub 1R 이상 + 연속 2R 확정결함 0 수렴 · 정형·기계 작업(카운트·grep): 자체검수 1회.
- **스크립트 인터페이스**(읽기 전용·기존 도구 재사용) = 자산 카운트 = §Test Plan T-4 PowerShell · 구조 검사 = `python tools_check_structure.py check <dir> <master.tex …>`(`check` 만) · 엄격 검사 = `python tools_tex_strict_check.py` · 빌드 = `xelatex -interaction=nonstopmode <master.tex>` 3-pass(ch1 먼저 → ch2 → ch3 → ch1 재패스; v2.0.0 마스터 파일명·순서는 4.0 에서 확정) · 코드 게이트(수치 대조 목적 읽기·실행만) = `python test_gates_v1024.py`·`_reflect.py`·`_selfconsistent.py`·`test_gates_v1025.py`(`docs/v1.0.25.1/` 안에서).
- **보고** = 4-tier(확정/근거 미발견/추정/미검증) · 확정에 path+line · 확정 사안 재질의 X · 결정 요청은 본문 평문 + 기본값(팝업 도구 X).
- **문체** = 한글 prose + 영어 학술 원어 · 두문자어 첫 출현 병기 · 메타 발언 X(계획·이력 문서 포함).

---

## Test Plan

> 전부 **확인 가능한 조건**(명령 + 증거 + 범위). "적절해 보임" 은 게이트가 아니다.

| ID | 게이트 | 명령/방법 | 증거 | 범위·기준 | 적용 Phase |
|---|---|---|---|---|---|
| T-1 | LaTeX 빌드 | `xelatex -interaction=nonstopmode <master>.tex` × 3-pass, 순서 ch1→ch2→ch3→ch1 재패스(xr) — v2.0.0 마스터 구성은 4.0 확정 | `.log` 의 `!` 오류 0 · "undefined references/citations" 0 · 페이지 수 기록 | 오류 0·undefined 0(전 마스터) · 대형 overfull 0(F-06/F-07/F-09 렌더 기반 점검 병행 — overfull 경고를 안 내는 좌측 넘침은 렌더로만 잡힘, A11 F-07) | 4.0~4.9 · 6.3 |
| T-2 | 구조 검사 | `PYTHONIOENCODING=utf-8 python tools_check_structure.py check <dir> <masters…>`(`check` 만 — JSON 모드 금지) | `STRUCTURE_CHECK: PASS` | 미해소 ref 0·env 짝 0·dup 라벨 0·cite-undef 0·bibitem-uncited 0 | 4.x·6.3 |
| T-3 | 엄격 검사 | `python tools_tex_strict_check.py` | `STRICT CHECK: ALL PASS` | $ 패리티·중괄호 depth 0·미확인 매크로 0 | 4.x·6.3 |
| T-4 | 자산 카운트 | PowerShell(빌드 세트 tex 한정): `[regex]::Matches($txt,'\\boxed').Count` 등 — 본 초안 저작 시 실행한 스크립트(work_log 수록) | 카운트 표 | v1.0.25.1 기준 = display 230·boxed 64·label 429·bibitem 95·cite 265/93·section 49·subsection 115·figure 28·table 20·박스 8종(brief §4.2 와 일치) · v2.0.0 = 자산 무유실(라벨 429 전건 존재 또는 매핑표 등재 · boxed 64 회수표 100%) | 2.1·4.0·6.2 |
| T-5 | 코드 = 부록 | 비부록 `_sections/*.tex` grep: `\\code\{|\\texttt\{|func_|solve_U_oc|_regsol|BlendedAnodeDQDV|LCOCathodeDQDV|GraphiteAnodeDischargeDQDV|include_electronic_entropy` | 히트 수 | **0**(P3 ⑧ · F-11) | 2.5·4.x·6.2 |
| T-6 | F-10 용어 | grep: `요동|양성|유일근` → 0 대상 · `음함수|섭동|준위` → 국문 유지 + 첫 출현 영문 병기 확인 · `정준|대정준` → 카운트만(사용자 판단 보류) — 집행 규약 = `HANDOVER_v24.md`:83(FB3) | 히트 수 + 병기 표 | 요동·양성·유일근 본문 0 · 음함수·섭동·준위 첫 출현 병기 100% · 정준/대정준 규약은 1.3 등록부에서 확정 | 2.5·6.2 |
| T-7 | 헌법 ① D1/D2 | grep(자기 diff: `구판|이전에는|폐지했|v1\.0\.\d+ 에서는`) + 방어 어투(`일 뿐 .*가 아니다`) 후보 → 수동 판정 분해 | 후보 목록 + 판정 | 렌더링 텍스트 0 | 6.2 |
| T-8 | 헌법 ③ D3 | boxed 각각 (a)(b)(c)(d) 존재 표(수동·항목 분해) + "대입하면" 류 점프 grep 후보 | 표 | 64/64(현행 진단) · v2.0.0 목표 boxed 100% | 2.2·4.x·6.1 |
| T-9 | 서지 | Crossref 조회(DR-6) 또는 원문 대조 | DOI 검증 표 | bibitem 전건 ∈ {검증/DOI 없음 확인/미검증} · 기억 서지 0 | 2.4·5.1 |
| T-10 | Read Coverage | Result 12항목 Read Coverage 에 파일·행 범위 | 표 | 배정표 합계와 일치(차이 = 미검독 명시) | 1.5·2.7·3.7·매 Result |
| T-11 | 검수 하한 | 라운드별 청크 스킴·렌즈·발견 건 기록 | 라운드 표 10행 + 커버리지×렌즈 6종 매트릭스 | 10R **and** 6렌즈 완주 · 연속 2R 확정결함 0 | 6.1 |
| T-12 | 실행 기반 검증 | SymPy 재유도 스크립트(주요 boxed) · 수치 극한(Ω→0·$L_V\to0$·α=1·T 극한) · 기존 코드 게이트 재실행(수치 대조) | 스크립트 출력 | 재유도 일치 · 극한 회수 항등 · 기존 게이트 GREEN 불변(코드 무수정) | 3.6·6.1 |
| T-13 | P3 8항 | 각 항 확인 가능 조건: ① $V_n$ 계열 grep·표 ② 전하 보존식 boxed 위치·dependency graph ③ graph 존재 ④ 4분류 표 ⑤ 5항 sub-section 존재 ⑥ 전달 정합 표 ⑦ 3축 명칭 표 ⑧ T-5 | 표·grep | 8/8 | 3.4·6.2 |
| T-14 | 기록 완결 | Step 파일 수 = 수행 Step 수 · Result md+json 쌍 · Ledger 행 | 파일 목록 | 누락 0 | 매 Phase |

---

## Assumptions

> load-bearing 전제. **실행 직전(GO 후 Step 1 전) 실물 대조** 대상. 거짓이면 STOP → Correction History 재baseline. 검증 상태 = sub 실측 ✓ / brief 인용·미검증 / 추정.

1. `xelatex.exe` 가 위 MiKTeX 경로에 존재하고 빌드가 가능하다 — 존재 **sub 실측 ✓**, 실행 가능·PATH 미검증(2026-07-26 빌드 실증 = A4:55).
2. `Claude/docs/v1.0.25.1/` 은 동결 base 이며 초안 저작 시점의 자산 카운트가 brief §4.2 와 같다 — **sub 실측 ✓**(60 tex·9214줄·전 카운트 일치).
3. v1.0.25 vs v1.0.25.1 차이 = `_sections` 3파일 + 마스터 3(표시 버전) · 코드·독립 부록 동일 — **sub 실측 ✓**(hash).
4. `Claude/docs/v2.0.0/` 은 부재(신규 생성) — **sub 실측 ✓**.
5. JCP147 PDF·`jcp_extract.txt`·refs 6/7 dossier 존재 — **sub 실측 ✓**(내용 미검독). refs 6·7 원문 미소장 — brief·B6:43 확정.
6. 구조 검사 도구 3본 존재 — **sub 실측 ✓**. v2.0.0 새 파일명에 대해 도구가 인자만으로 동작하는지 — **미검증**(4.0 에서 확인; 안 되면 도구 사본을 v2.0.0/results 에 두고 인자 갱신 — 원본 무수정).
7. Python 3.12 + numpy/scipy/matplotlib/pandas(SymPy 는 T-12 에 필요 — **설치 여부 미검증**, 부재 시 새 의존성 = 정지 조건·확인) — brief 인용·미검증.
8. git: main = `4069cb3`, tracked 변경 0 — 세션 스냅샷 확정. 버전 브랜치가 main 조상 — brief 인용·미검증.
9. **전원 Fable 5.1** 배정 — 사용자 명시(brief §2 추가 발화).
10. 사용자 논문 ref 위치 "페이지·문단 세부" 는 부록 E ②항이 유보 상태(`ch1_appE_selfconsistent.tex`:120–121) — v2.0.0 에서 JCP147 원문 대조로 확정(DR-8).
11. 이력 문서군 규모 = plans 91(9503줄) + docs/**/PLAN_* 16 + HANDOVER 25(1612줄) + Fable 8(885줄) + CLOSING 106 + INDEX 262 + ledger 30(+docs/vN/results) + 조사 문서군 — 측정분 ≈ 12,400줄 + 미측정분(DR-7 비용의 근거).
12. brief §3-C 의 "plans 90·HANDOVER 28" 은 실측 91·25(old/ 제외)와 소폭 다르다 — 1.1 Step 1 에서 정본화(추정: brief 는 INDEX 포함·old/ 포함 등 집계 기준 차이).
13. SM2-A/B/C 의 집행 여부는 미확정(brief §4.5 — 18건 grep 히트) — 1.4 Step 9 에서 판정. 판정 전에는 "부분 집행 가능성" 으로만 취급.
14. 기존 확보 공개데이터(`results/comp_v24/sintef_data/` 존재 — **sub 실측 ✓** 폴더) 는 2.6·3.1 판정에 재사용 가능 · 신규 다운로드는 DR-6.
15. v1.0.25.1 PDF 페이지 102/30/22 — 파일 존재 ✓, 페이지 수 미열람(brief·A4 인용).
16. `Codex/` 는 어느 Phase 에서도 읽지 않는다 — 규약.

---

## Correction History

- **2026-09-02 v1 초안(작업 sub, Fable 5.1)**: brief(`Claude/results/handoffs/2026-09-02-v2-master-plan/brief.md`) §5 골격을 11-section 으로 확장. 원천 21본 전문 정독 + §3-C 구조 확인 + load-bearing 전제 읽기 전용 실측(자산 카운트 전건 일치·diff 3+3 확정·도구/PDF/JCP/dossier 존재·v2.0.0 부재). brief 와 어긋난 곳(plans/HANDOVER 건수·display 230 의 집계 정의)은 원천/실측을 따르고 work_log 에 기록. 결정은 하나도 확정하지 않음(DR-1~9 · DG-A/B/C 는 사용자).

---

## Decisions Required

> 사용자 결정 항목(평문). 각 항목 = 실제 내용 · 근거 · 기본값 · 한 줄 응답 선택지. 무응답 시 기본값으로 진행한다는 규약은 **사용자가 그렇게 지시할 때만** 적용한다(본 초안은 GO 대기). 사용자 결정 게이트 DG-A/B/C 는 챕터 3.7 에서 별도로 정지해 묻는다(지금은 예고만).

- **DR-1 — "1.0.25 두 가지 버전" 의 해석.**
  - 내용: 사용자 발화 "현재의 가장 1.0.25 두 가지 버전" 을 (A) `docs/v1.0.25/`(base, 무수정 보존) + `docs/v1.0.25.1/`(검증 + touch-up 4건, 현행 최신)로 읽는다. 실물 차이 = `_sections` 3파일 + 마스터 3(표시 버전) + ARCHIVE_NOTE + PDF(sub 실측 hash: 3+3 DIFF·코드·독립 부록 SAME). 대안 (B) = v1.0.26 A/B 두 산출(물리 4전이 vs gallery 7전이, main HEAD 커밋 메시지)로 읽는다.
  - 근거: (A) 는 `docs/INDEX.md`:7–14 의 "현행 최신 v1.0.25.1 / base v1.0.25" 구분과 일치. (B) 는 HEAD 커밋 제목이지만 A7 에 따르면 v1.0.26 은 "실행 차단·미완" 조사다.
  - 기본값: **(A)**. 어느 쪽이든 regsol 미결은 2.6/3.1 로 흡수된다.
  - 응답 선택지: `DR-1: A` / `DR-1: B` / `DR-1: A+B(둘 다 자산 지도에 포함)`.

- **DR-2 — 목표 버전 라벨·폴더.**
  - 내용: 새 문건의 라벨과 폴더. 기본 = **v2.0.0**, `Claude/docs/v2.0.0/`(일반→특수 재구조 = major). 대안 = v1.1.0(`Claude/docs/v1.1.0/`).
  - 근거: 3.3 (b) 채택 시 구조가 바뀌므로 semantic major 가 자연스럽다(master 판단·brief §8). v1.0.x 계보의 "국소 수정 = patch" 관행(A4)과 구분된다. 마스터 tex 파일명·xr 키는 DG-2(v1.0.25 한정) 규약에서 풀리므로 4.0 에서 새로 정한다(DG-C 에서 재확인).
  - 기본값: **v2.0.0**.
  - 응답 선택지: `DR-2: v2.0.0` / `DR-2: v1.1.0` / `DR-2: 기타 <라벨>`.

- **DR-3 — 문건 구조(사전 선호만 · 결정은 3.7).**
  - 내용: (a) 현행 재료별 3장 유지 + 내부 일반화 vs (b) Part I 일반 이론(열역학·통계역학·동역학·열·히스테리시스) + Part II 재료 적용(흑연·LCO·Si·블렌드). 3.3 이 두 안의 장단·자산 이동 맵·xr 영향·페이지 추정을 산출한 뒤 **3.7 에서 정지해 DG-A 로 결정**한다.
  - 근거(master 사전 선호 = (b), brief §8): 사용자 기준 5(일반식 → 간소화)와 CLAUDE.md P1 원구상(Chapter 1 전하보존 → 2~5 발열·반응속도론·통합 상태방정식·히스테리시스 계층)이 "이론 층 → 적용 층" 구조와 정합한다(작업 sub 판단: P1 은 흑연 중심 구상이었고 (b) 는 이를 재료 일반으로 확장하는 셈이므로, 3.3 에서 P1 과의 대응을 명시해야 한다).
  - 기본값: 지금은 **선호 기록만**((b)). 3.3 산출 없이는 결정하지 않는다.
  - 응답 선택지: `DR-3: (b) 선호 확인` / `DR-3: (a) 선호` / `DR-3: 3.7 까지 유보`.

- **DR-4 — 코드 동기 = 별도 후속 플랜.**
  - 내용: 본 계획은 문건만. 코드 `Anode_Fit_v1.0.24.py`(release 1.0.25)는 수정하지 않고, v2.0.0 문건 확정 후 별도 doc-leads 동기 플랜에서 다룬다. 단 기존 코드의 **읽기·게이트 실행(수치 대조 목적)** 은 허용(T-12).
  - 근거: doc-leads 규약(문건이 authoritative, `docs/INDEX.md`:67) · 코드 게이트 4종 GREEN·골든 bit-exact 계약(A4 §②)을 문건 저작 중에 흔들지 않기 위함.
  - 기본값: **별도 플랜**.
  - 응답 선택지: `DR-4: 별도` / `DR-4: 본 계획에 코드 챕터 추가(범위 확장 — 계획서 정정 필요)`.

- **DR-5 — 병렬(fan-out) sign-off.**
  - 내용: 기본은 직렬(유닛 1개·동시 산 서브 ≤1). 옵션 = (i) 챕터 2.2~2.5 진단 청크 병렬(예: 2.2 의 Step 13~16 을 4 유닛 동시) (ii) 챕터 4.x 저작 파트 병렬(4.1~4.5 이론 파트 vs 4.6~4.8 적용 파트). 비용 = 유닛 수 × Fable 5.1 세션 + master 통합·삼각검증 부하 증가(구체 수치는 원천에 없어 제시하지 않음). 병렬이라도 shared mutable state(같은 `_sections` 파일·ledger)는 직렬화한다.
  - 근거: 헌법 §1-병렬(자의 fan-out 금지·sign-off 만이 승인). 사용자 기준 6(효율 < 완성도).
  - 기본값: **직렬**.
  - 응답 선택지: `DR-5: 직렬` / `DR-5: (i) 승인` / `DR-5: (ii) 승인` / `DR-5: (i)+(ii)`.

- **DR-6 — 외부 접근.**
  - 내용: (i) 문헌 검색(3.1 Step 26·챕터 5) (ii) DOI 검증 Crossref 조회(2.4·3.5·5.1) (iii) 공개데이터 재다운로드(2.6 — SINTEF Zenodo 20086298 GITT/hold; 기확보 CSV 는 별개로 재사용). 기본 = **읽기 전용 허용**(다운로드 파일은 `Claude/results/` 하위에 두고 `SOURCES.md` 관행대로 출처 기록). 불허 시 해당 게이트는 "미검증" 으로 정직 표기하고 진행.
  - 근거: 사용자 기준 3(리뷰급 레퍼런스)은 DOI 검증 없이는 충족을 주장할 수 없다(헌법 ②). 데이터는 A7 이 GITT 평형 데이터 필요를 확정.
  - 기본값: **(i)(ii) 허용 · (iii) 는 2.6 진입 시 재확인**(작업 sub 제안 — brief 기본값은 "읽기 전용 허용" 일괄).
  - 응답 선택지: `DR-6: 전부 허용` / `DR-6: (i)(ii) 만` / `DR-6: 불허`.

- **DR-7 — 이력 정독 범위.**
  - 내용: 기본 = plans 91(+docs/**/PLAN_* 16)·HANDOVER 25·Fable 8·CLOSING·INDEX·ledger 30(+docs/vN/results)·조사 문서군 **전문 정독**. 비용 = 측정분 ≈ 12,400줄 + 미측정분(§2.8). 대안 = 마스터플랜·인계·감사·CLOSING 전문 + 페이즈 세부 계획서(docs/**/PLAN_*·`*-P1~P8-*`·`*-phaseR*-*` 류)는 구조 추출(Phase 표·게이트·결정만).
  - 근거: 사용자 기준 6("효율이 아닌 완성도·신뢰도") · CLOSING 2-1/2-2("제안 전 과거 이력 먼저 확인"·"지침·과거 이력을 실제로 확인") · A11 F-11 의 "이력 무시" 지적. 대안은 비용을 줄이지만 세부 계획서 안의 결정·게이트 이력이 누락될 위험이 있다(작업 sub 판단).
  - 기본값: **전문 정독 전부**.
  - 응답 선택지: `DR-7: 전부` / `DR-7: 대안(세부 계획서 구조 추출)`.

- **DR-8 — refs 6·7 원문 제공 여부.**
  - 내용: CLAUDE.md P1 은 refs 6/7 방법론을 "실제 확인한 뒤" 반영하라고 요구한다. 현행은 JCP147 자족 + dossier + 부록 E 5항으로 이행했고, refs 6·7 원문(JCP 134, 121102 (2011) · JCP 138, 164123 (2013))은 미소장이다. 기본 = JCP147 자족 + dossier + Crossref 서지 확정 + "원문 미소장" 정직 표기(부록 E ②항의 "페이지·문단 세부" 는 JCP147 원문 대조로 확정). 대안 = 사용자가 원문 PDF 를 `Claude/` 에 제공 → 3.1/4.9 에서 원 유도 대조.
  - 근거: B6:43(원문 미소장·자족 기술 경로) · A14:120–121(유보 문장).
  - 기본값: **자족 + 정직 표기**.
  - 응답 선택지: `DR-8: 자족` / `DR-8: 원문 제공 예정(경로 <…>)`.

- **DR-9 — GO 범위.**
  - 내용: 기본 = 작업 챕터 1 → 2 → 3 연속 진행 후 3.7 에서 정지(DG-A/B/C). 대안 = 챕터 1 만 먼저(1.5 Result 후 정지·재GO).
  - 근거: 챕터 1~3 은 조사·설계라 파괴·비가역 작업이 없고, 정지 조건은 3.7 하나뿐이다. 챕터 1 결과를 먼저 보고 싶으면 대안.
  - 기본값: **1→2→3 연속, 3.7 정지**.
  - 응답 선택지: `DR-9: 1→2→3` / `DR-9: 챕터 1 만`.

> 위 DR 확정 + GO 사인이 오면 master 가 최종 마스터 플랜을 `Claude/plans/2026-09-02-v2-master-plan.md` 로 저장하고, 실행 직전 load-bearing 전제(§Assumptions)를 실물 대조한 뒤 Step 1 부터 5-stage 루프로 진행한다. 작업 sub 의 추가 후보·이견은 `work_log.md` 「Decision Queue」에 있다(master 승격 판단).
