# R4b — 현행본 진단 스코핑: Chapter 2(LCO) · Chapter 3(Si·혼합) · 독립 부록 및 부록 3종

> 작성 = 판독·등록부 초안 에이전트 [diag_ch2ch3](Fable 5.1), 2026-09-03. 워크플로 = 「v2.0.0 수식 연구 진보 마스터 플랜」.
> 역할 경계 = 본 파일 1건만 산출. 원천은 읽기 전용, `Codex/` 무접근, git 명령 미실행.
> 판정 규약 = 4-tier(확정 / 근거 미발견 / 추정 / 미검증). 확정에는 `path:line` 을 붙인다. 모든 경로는 `D:\Projects\Project_Anode_Fit\Claude\docs\v1.0.25.1\` 기준이며, `_sections\` 아래 파일은 파일명만 적는다.
> 사용자 기준 1)~5)는 brief §2 verbatim(`Claude\results\handoffs\2026-09-02-v2-master-plan\brief.md:36-40`)을 그대로 축으로 쓴다 — ① 비약·누락·생략 없는 유도, ② 대학원 교재 수준 형식, ③ 리뷰 논문급 레퍼런스, ④ 타전공 석박사 청중, ⑤ 일반식→간소화의 레퍼런스 확실한 가정.
> 이 문건이 "사용자 결정"이라 부르는 것은 brief §2 발화, `CLAUDE.md` P3(코드=부록 · 사용자 반복 지시 F-11), 마스터 tex 주석의 "DG-2 사용자 확정"뿐이다. 그 밖의 판단은 전부 본 에이전트의 것이며 tier 로 표시한다.

---

## 0. 범위와 산출 형식

정독 대상은 지시대로 24건이다 — Chapter 2 의 LCO 본문 8절(`ch1_sec11`~`ch1_sec17`, 삽입 소절 `ch1_sec16b` 포함)과 보조 3건(`ch2v22_sec00_intro`·`ch2v22_notation`·`ch2v22_bib`), Chapter 3 의 본문 6절(`ch3v22_sec01_map`~`ch3v22_sec05_code`, 삽입 소절 `ch3v22_sec02b_sifr` 포함)과 보조 3건(`ch3v22_sec00_intro`·`ch3v22_notation`·`ch3v22_bib`), 부록 3건(`ch1_appD_si`·`ch2_appA_traps`·`ch2_appB_codemap`), 독립 부록 `appendix_phase_separation.tex`, 그리고 diff 용 `v1.0.25\_sections\ch3v22_sec02b_sifr.tex`. 전 파일을 head→tail 로 Read 했고 행 범위는 말미 「Read Coverage」에 전건 적었다. 기계 카운트는 Python 스크립트(스크래치패드 `count_r4b.py`, 주석 제거 후 정규식)로 뽑았으며 Git Bash grep 은 이스케이프 오류로 폐기했다.

산출 항목은 지시된 R4a 동형 6종이다 — (1) 절별 자산 표, (2) boxed 전건 (a)~(d) 사슬 판정, (3) 가정·레퍼런스 등록부, (4) 인용 밀도, (5) 형식·잔존 grep, (6) 정량 결론. 여기에 §3.5 코드=부록 충돌을 별도 절(§7.1)로 두었고, 정독 중 발견한 구조 사실(orphan 파일·독립 부록 미편입·중복 유도)을 §8 에 모았다.

---

## 1. 절별 자산 표 (기계 카운트, v1.0.25.1)

### 1.1 Chapter 2 — LCO (마스터 `ch2_lco_v1.0.24.tex:22-32` 조립 순서)

| 파일 | 절 라벨 | 행 | boxed | display(eq/multline/`\[`) | label | cite 호출/키/distinct | sub | fig/tab | 박스 환경 | (a)(b)(c)(d) 마커 |
|---|---|---|---|---|---|---|---|---|---|---|
| ch2v22_sec00_intro | (서두) | 12 | 0 | 0 | 0 | 0 | 0 | 0/0 | — | — |
| ch2v22_notation | (기호 2단) | 14 | 0 | 0 | 0 | 0 | 1* | 0/0 | — | — |
| ch1_sec11_lcointro | sec:lco-intro | 175 | 1 | 1/0/0 | 7 | 8/9/7 | 3 | 1/1 | — | 0/0/0/0 |
| ch1_sec12_lcocenter | sec:lco-center | 112 | 1 | 3/0/2 | 6 | 2/2/1 | 2 | 0/0 | verifybox 1 | 1/1/1/1 |
| ch1_sec13_lcohys | sec:lco-hys | 223 | 3 | 10/0/3 | 16 | 13/16/6 | 5 | 0/0 | srcbox 1 | 1/1/1/1 |
| ch1_sec14_lcodecomp | sec:lco-decomp | 143 | 1 | 6/0/0 | 11 | 3/3/1 | 4 | 0/0 | srcbox 1 | 1/1/1/1 |
| ch1_sec15_lcoelec | sec:lco-electronic | 396 | 4 | 11/0/2 | 19 | 20/28/8 | 6 | 1/0 | bgbox 1·verifybox 1·srcbox 1 | 2/2/2/1 |
| ch1_sec16_lcopeak | sec:lco-peak | 70 | 1 | 4/0/0 | 5 | 1/3/3 | 0 | 0/0 | — | 1/1/1/1 |
| ch1_sec16b_lcoomega | ssec:lco-omega | 160 | 3 | 3/1/0 | 5 | 8/9/5 | 1* | 0/0 | warnbox 1·keybox 1 | 1/1/1/1 |
| ch1_sec17_msmr | sec:lco-code | 176 | 2 | 10/0/0 | 13 | 6/7/3 | 2 | 0/0 | srcbox 1 | 2/2/2/2 |
| ch2v22_bib | — | 21 | 0 | 0 | 0 | bibitem **15** | — | — | — | — |
| **소계(본문 8절)** | | **1455** | **16** | **48 eq + 1 multline + 7 `\[`** | **82** | **61 호출 / 77 키 / 15 distinct** | 23 | 2/1 | 9 | |

(`*` = `\subsection*` 또는 파일 자체가 소절.) Chapter 2 의 bibitem 은 파일 헤더 주석이 "14종"이라 적었으나 실제 15건이다(`ch2v22_bib.tex:2` vs 본문 6-20행 — 확정).

### 1.2 Chapter 3 — Si·혼합 (마스터 `ch3_si_v1.0.24.tex:23-32` 조립 순서)

| 파일 | 절 라벨 | 행 | boxed | display | label | cite 호출/키/distinct | sub | fig/tab | 박스 환경 | (a)(b)(c)(d) |
|---|---|---|---|---|---|---|---|---|---|---|
| ch3v22_sec00_intro | (서두) | 12 | 0 | 0 | 0 | 0 | 0 | 0/0 | — | — |
| ch3v22_notation | (기호표) | 46 | 0 | 0 | 1 | 0 | 1* | 0/1 | — | — |
| ch3v22_sec01_map | sec:si-map | 129 | 0 | 0 | 7 | 15/17/14 | 5 | 0/1 | keybox 1·bgbox 1 | 0/0/0/0 |
| ch3v22_sec02_cases | sec:si-cases | 173 | 0 | 0 | 7 | 33/36/23 | 4 | 1/1 | srcbox 1 | 0/0/0/0 |
| ch3v22_sec02b_sifr | ssec:si-fr | 220 | 2 | 5/0/0 | 6 | 7/10/7 | 1* | 0/0 | warnbox 2·keybox 1·signbox 1 | 1/1/1/1 |
| ch3v22_sec03_blend | sec:si-blend | 278 | 1 | 5/0/0 | 9 | 10/11/7 | 2 | 1/0 | warnbox 1·keybox 1·verifybox 1·srcbox 1 | 2/2/1/1 |
| ch3v22_sec04_mech | sec:si-mech | 110 | 1 | 5/0/0 | 8 | 9/9/8 | 2 | 0/0 | warnbox 1·keybox 1·verifybox 1 | 1/1/1/1 |
| ch3v22_sec05_code | sec:si-code(조립상 부록, §7.1) | 70 | 0 | 1/0/0 | 6 | 3/3/3 | 4 | 0/0 | warnbox 1·codebox 1 | 0/0/0/0 |
| ch3v22_bib | — | 44 | 0 | 0 | 0 | bibitem **36** | — | — | — | — |
| **소계(본문 6절+기호표)** | | **1026** | **4** | **16 eq** | **44** | **77 호출 / 86 키 / 36 distinct** | 19 | 2/3 | 12 | |

Chapter 3 의 bibitem 도 헤더 주석("14종" + "R5 신규 등재 19종" = 33)과 실제(36)가 어긋난다(`ch3v22_bib.tex:2,21` — `artrith2018`·`verbrugge2017` 등 sifr 소절 신규 키가 주석에 미반영, 확정).

### 1.3 부록군

| 파일 | 제목(본문) | 조립 위치 | 행 | boxed | display | label | cite 키/distinct | 박스 | (a)(b)(c)(d) |
|---|---|---|---|---|---|---|---|---|---|
| ch2_appA_traps | 부록 C — 열특성 기호·부호 함정 검산표 | Ch1 마스터 `:56` | 75 | 0 | 0 | 1 | 0 | longtable 1 | — |
| ch2_appB_codemap | 부록 D — 열특성 코드 구현 요구명세 | Ch1 마스터 `:57` | 77 | 0 | 0 | 1 | 1/1 (`numverif2026`) | longtable 1 | — |
| ch1_appD_si | Si 계열 접목 예비 지도 | **마스터 3본 어디에도 `\input` 없음(orphan)** | 91 | 0 | 0 | 7 | 20/14 | table 1 | — |
| appendix_phase_separation | Appendix — 상분리의 열역학 | **독립 문서(자체 `\documentclass`, 마스터 미편입)** | 497 | 3 | 19 eq | 30 | 0 (자체 [A1]–[A5]) | keybox 2·fig 2 | 7/7/6/5 |

orphan 판정 근거: `ch1_graphite_v1.0.24.tex:25-60` 의 `\input` 목록은 `ch1_appA_signcheck`·`ch1_appB_codemap`·`ch2_appA_traps`·`ch2_appB_codemap`·`ch1_appE_selfconsistent` 이고, `ch2_lco_v1.0.24.tex:22-32`·`ch3_si_v1.0.24.tex:23-32` 에도 `ch1_appD_si` 는 없다. `ch3_si_v1.0.24.tex:3` 헤더가 "원천 = v1.0.21 부록 D(Si 예비 지도) 승격"이라 적어, 승격 후 원 파일이 `_sections/` 에 남은 상태다(확정). 독립 부록 미편입 근거: 세 마스터 grep 에 `appendix_phase_separation` 무, `results/INDEX_v25.md:35` 가 "독립 부록 · 편집 없음 · 무변경"으로 등재(확정). 두 파일 모두 brief §4.2 의 "`_sections/` 56 + 독립 부록 497줄" 카운트 안에는 들어 있으므로 인벤토리 수치와는 모순되지 않는다.

### 1.4 스코프 합계와 Chapter 1 라벨 의존 맵(자산 이동 맵 시드)

스코프 24건(v1.0.25 sifr 제외 23건 + 독립 부록) 합계 = 3324행 · boxed 23 · display 84(equation 83 + multline 1) + `\[` 7 · label 165 · cite 키 Ch2 77 + Ch3 86 + appD 20 + appB 1. brief §4.2 의 전체 boxed 64 대비 스코프 몫은 23/64 = 36 %, 이 중 Chapter 2 16 · Chapter 3 4 · 독립 부록 3 이다.

Chapter 2·3 이 `\eqref` 로 끌어오는 Chapter 1 라벨(스코프 밖 정의)은 다음과 같다. v2 가 "일반 이론 Part I → 재료 Part II" 로 재구조할 때 이 표가 그대로 자산 이동의 종속 리스트가 된다.

| 참조 파일 | Chapter 1 식 라벨(스코프 밖) |
|---|---|
| ch1_sec11 | eq:n0map · eq:eqcond · eq:gxi · eq:xieq · eq:wbase · eq:eqpeak · eq:vn · eq:Ubranch · eq:reversal |
| ch1_sec12 | eq:n0map · eq:eqcond · eq:eqbalance · eq:Ujmid · eq:Uj · eq:gibbsdef |
| ch1_sec13 | eq:mu · eq:gxi · eq:spinodal · eq:gpp · eq:Veq · eq:hyssub · eq:hysdiff · eq:hyssym · eq:dUhys · eq:Ubranch |
| ch1_sec14 | eq:sum |
| ch1_sec15 | eq:fermifn · eq:belliden · eq:sum · eq:sm-mc-balance · eq:complete |
| ch1_sec16 | eq:xieq · eq:belliden · eq:wbase |
| ch1_sec16b | eq:Uj · eq:gr2l-disc |
| ch1_sec17 | eq:xieq · eq:wbase · eq:sum |
| ch2v22_notation | eq:Uj · eq:xieq · eq:dUhys · eq:Ubranch · eq:sm-mc-balance · eq:sum |
| ch3v22_notation · sec01 | eq:sm-mc-balance · eq:sm-mc-fluc · eq:logisticsolve · eq:dUhys · eq:sum |
| ch3v22_sec02b | eq:eqpeak · eq:xieq · eq:wbase · eq:gr2l-fwhm · eq:skewpeak |
| ch3v22_sec03 | eq:sm-workbal · eq:sm-mc-balance · eq:sm-mc-factor · eq:sm-gc · eq:sm-mc-occ · eq:sm-logistic · eq:sm-eqcond · eq:sm-mc-fluc · eq:sum |
| ch3v22_sec04 | eq:sm-muV · eq:dUhys · eq:Ubranch |
| ch2_appA · appB | eq:muV · eq:implicit · eq:complete · eq:logistic · eq:qrev · eq:sm-mc-balance |

절·표·그림 참조(`\ref`)까지 합치면 Chapter 2 는 Chapter 1 의 §center·§hys·§width·§eqpeak·§broadening·§sum·§dist·§einstein·§revheat·§sm-* 와 표 tab:staging, Chapter 3 는 §sm-mc·§sm-electro·§width·§eqpeak·§lag·§tail·fig:hysgap·fig:sumcurve 에 걸린다. 스코프 안에서 정의된 라벨을 스코프 안에서 잘못 참조한 사례는 없다(구조 검사 PASS 와 정합 — `results/V1025_DOC_EDIT_REPORT.md:211-213` 미해소 0).

---

## 2. v1.0.25 → v1.0.25.1 diff — `ch3v22_sec02b_sifr.tex`

`diff -u` 결과는 두 hunk 뿐이고 식·라벨·boxed·cite 는 불변이다(확정).

| hunk | v1.0.25 행 | v1.0.25.1 행 | 변경 내용 | 판정 |
|---|---|---|---|---|
| 1 | 40 | 40-44 | 지위 warnbox 안 문장 "더 적은 가정으로 설명한다" → "별도 커널 계열 도입 없이 기존 로지스틱 자유도만으로 설명한다(gallery 세분은 오히려 모수가 더 많으므로 … 새 커널 계열 불추가다)" + "단, 이 순효과 역전은 단일 셀·부분적으로 불일치한 기준 구성에서의 관측이며, 다중 셀 통계와 모수 절약(AIC/BIC) 비교는 미확정이다(재현 위임 = `\texttt{V1025\_DATA\_ADDENDUM.md}` M6)" 추가 | brief §4.2 의 touch-up **F1(regsol 삭제근거 정직화)** 에 해당. 정직성은 올라갔으나 본문에 `\texttt{…md}` 파일명 토큰(코드/문서 식별자)이 새로 들어왔다(§7.2). |
| 2 | 140 | 144-145 | eq:sifr-blend 직후 "(단 우변 Frumkin-Si 항은 위 지위 상자대로 해석적 기록이며, 채택 경로·블렌드 구현 코드는 로지스틱 단일계다)" 삽입 | 같은 F1 의 연장 — 박스식과 채택 경로의 괴리를 박스 바로 아래서 재고지. |

두 hunk 모두 "미채택 해석적 기록" 지위를 강화하는 방향이며 물리·수식 변경은 0 이다. 나머지 세 touch-up(F3 inline 표식·M-w §5 폭 포인터·L-bg §6 α=1 한정)은 Chapter 1 파일 소관이라 본 스코프에 없다(brief §4.2 대조 — 확정).

---

## 3. boxed 전건 (a)~(d) 사슬 판정 (23건)

판정 열은 셋으로 갈랐다 — **완결**(출발식·연산·중간식·박스가 그 절 또는 명시 인용된 Chapter 1 식으로 닫힘), **부분**(사슬 중 한 고리가 말로만 있거나 출발식이 유도 없이 세워짐), **비유도**(규약·정의·옵션·도식·진술을 박스로 감싼 것 — 기준 ① 의 판정 대상이 아니라 박스 용법의 문제). "의존"은 Ch1 식 없이 그 절만으로 따라올 수 있는가(follow 렌즈)를 적었다.

| # | 라벨 | 파일:행 | 사슬 판정 | 근거·최약 고리 | Ch1 의존 |
|---|---|---|---|---|---|
| 1 | eq:lco-sigmaslot | sec11:90-96 | 비유도(규약) | 방향 슬롯 규약. (a)~(d) 마커 없음. 규약으로서는 자족. | eq:vn·Ubranch·reversal 을 작용처로 인용 |
| 2 | eq:lco-dUdT | sec12:53-60 | 완결 | (a) 세 진입점 → (b) ΔG=−FU 대입 → (c) 이중 경로(직접 미분·Gibbs 항등식) → (d). 단 박스는 ΔS 상수 특수형이고 일반 적분형 eq:lco-kirchhoff(`:74-77`)는 미박스(§4 G01). | eq:eqcond·Uj·gibbsdef |
| 3 | eq:lco-dUhys | sec13:80-90 | 완결(대입형) | (b) gpp → spinodal → (c) Veq 대입·극대−극소 차. 차의 전개는 "흑연 식 hysdiff 의 전개 재사용"(`:69`)으로 위임 — 본 절만으로는 artanh 항이 어디서 오는지 못 따라간다(G02). 대수 자체는 본 에이전트가 재유도해 일치 확인(u 정의·부호·Taylor 극한 8RT/3F 까지). | eq:gpp·Veq·hyssub·hysdiff·hyssym |
| 4 | eq:lco-Ubranch | sec13:91-96 | 완결(대입형) | Ch1 eq:Ubranch 의 상첨자 치환. γ_j·h_{η,j} 가 "유도되지 않는 현상학 인자"임을 명시(`:98-101`) — 정직. | eq:Ubranch |
| 5 | eq:lco-mit | sec13:195-201 | 비유도(도식) | 슬롯 분리 선언(gap 슬롯 ‖ ∂U/∂T 슬롯). 식이 아니라 관계 도식. | — |
| 6 | eq:lco-decomp | sec14:62-67 | 완결 | (a) Z 인수분해(F^×≈0) → (b) 로그 가법 → (c) 슬롯 정의 → (d). 가법성 정당화 "(가)"가 박스 뒤 불릿(`:71-77`)에 사후 배치(G05). | eq:sum |
| 7 | eq:dSe | sec15:174-178 | 완결 | (a) Fermi–Dirac → (b) 정보 엔트로피 합 → (c) Sommerfeld C_e 적분 + 직접 경로 교차검증(eq:Sedirect) → (d). 각주에 O(T³) 보정 차수. 교과서 레퍼런스 부재(G07). | eq:fermifn |
| 8 | eq:U1T2 | sec15:224-227 | 완결(인라인) | ΔS(T)=ΔS_0+a_eT 적분 — ½ 인자 근거 명시. sec12 의 Kirchhoff 논의와 정합함을 본 에이전트가 검산(ΔH(T)=ΔH_0+a_eT²/2 → 동일 U(T)). | eq:lco-dUdT(스코프 내) |
| 9 | eq:ggate | sec15:241-245 | 비유도(모델 가정) | logistic 게이트 postulate. 정당화 (i)~(iv)(`:269-283`)는 사후·정성. 대안 함수형 검토 없음(G08). | — |
| 10 | eq:dSegate | sec15:255-261 | 완결(1줄 대입) | ggate 를 dSe 에 대입, σ'=σ(1−σ) 항등. 골 깊이 −46 J/(mol K) 수치는 본 에이전트 재계산과 일치(3.29×8.314×0.02585×65 = 46.0). | eq:belliden |
| 11 | eq:lco-eqpeak | sec16:43-49 | 완결 | (a) 전하 보존식 LCO 판 → (b) 종 항등식·연쇄율 → (c) 위치·높이·면적 → (d). | eq:xieq·belliden·wbase |
| 12 | eq:lcoomega-kernel | sec16b:24-31 | 부분 | gpp 에서 커널로 "⟹" 한 줄. dξ/dV = F/(∂²g/∂ξ²) 관계는 말(`:33-34`)로만 있고 중간식이 없다(G10). Ω→0 환원은 명시·정확. | eq:gr2l-disc(같은 커널) |
| 13 | eq:lcoomega-hash7 | sec16b:63-69 | 비유도(문구 정정) | "Ω = 평균장 축약, ΔS^config ⊥ Ω" 선언. 검수 ID "#7" 이 본문 제목·본문에 노출(G13). | — |
| 14 | eq:lcoomega-toggle | sec16b:98-105 | 비유도(옵션 규칙) | on/off 규칙 박스. 물리식 아님. | — |
| 15 | eq:lco-msmrpeak | sec17:103-109 | 완결 | (a) MSMR 점유식 → (b) 정규화 → (c) 여집합 항등·계수비교로 f=+σ_d 유일 → (d). | eq:xieq |
| 16 | eq:lco-plugin | sec17:160-168 | 비유도(흐름도) | forward 사슬 화살표 도식. 직전 (a)~(c)(xmap·SeV·U1V)는 완결이나 박스 자체는 식이 아님. | eq:xieq |
| 17 | eq:sifr-kernel | sifr:83-87 | 완결 | (b) V(θ) → dV/dθ → dQ/dV 절댓값. 다만 (a) 가 "실측 판정"이고 출발식 eq:sifr-V(`:70-73`)는 "정칙용액 화학퍼텐셜을 전위로 환산"이라고만 세움 — Ch1 eq:mu·eq:eqcond 인용 없음(G19). | eq:eqpeak·xieq·wbase(의존 명시 부족) |
| 18 | eq:sifr-blend | sifr:139-143 | 비유도(진술) | 가산 중첩 진술. 정당화 = "공통 μ" 한 줄 + tu_blend2024 인용. 미채택 기록인데 박스(G21). | — |
| 19 | eq:blend-balance | blend:69-75 | 완결 | (a) 두 host 한 저장조 → (b) host 곱 인수분해 → (c) ⟨N⟩ → (d). verifybox 3건(유일근 이월·f_Si→0 회수·부호). 각주 환산식 수치를 본 에이전트가 재계산해 f_Si=0.230/0.402/0.535·Q=1.26/1.62/2.09 일치. | eq:sm-mc-factor·sm-gc·sm-mc-occ·sm-logistic·sm-eqcond |
| 20 | eq:si-coupling | mech:50-55 | 부분 | (b)(c)(d)는 닫히나 (a) eq:si-lcmu(`:22-26`) 가 "선형 결합의 1차 항"으로 postulate — Larché–Cahn 자유에너지에서의 유도 없음(G23). Λ_σ 정량은 "확인 필요"로 남김(`:66-68`). | eq:sm-muV |
| 21 | eq:app-fxi | appendix:106-109 | 완결 | (a) 격자 모형 → (b) Stirling 혼합 엔트로피 → (c) 평균장 쌍 에너지 → (d). 스코프 내 유일하게 "일반(격자 모형) → 특수(정규용액)"가 완전히 적힌 예. | — (독립) |
| 22 | eq:app-gain | appendix:157-161 | 완결 | 현의 기하·볼록성 정의로 닫힘. | — |
| 23 | eq:app-binodal | appendix:213-218 | 완결 | 변분 정류 → 공통접선 → 대칭 특수화. 수치 예(Ω=3RT: ξ_b=0.0707/0.9293, f/RT=−0.0583, ξ_s=0.2113/0.7887, f/RT=−0.0157)를 본 에이전트가 재계산해 4자리까지 일치. | — |

집계: 완결 14(#2,3,4,6,7,8,10,11,15,17,19,21,22,23) · 부분 2(#12,#20) · 비유도 7(#1,5,9,13,14,16,18). 곧 스코프 boxed 23 중 기준 ① 의 유도 대상은 16 이고 그 중 14 가 닫힌다. 그러나 "닫힘"의 절반 이상이 Chapter 1 식의 대입·재사용이라, 본 두 장만으로 따라올 수 있는 유도는 #7·#8·#10·#15·#19·#21~#23 의 8건뿐이다(follow 렌즈).

박스가 안 붙었으나 실제 사용·핵심인 식(박스 우선순위 역전 후보): eq:lco-kirchhoff(sec12:74-77, 일반 적분형) · eq:lco-SeV·eq:lco-U1V(sec17:131-149, 전자항 forward 실식) · eq:blend-dqdv(blend:118-122, 그림·코드가 실제로 쓰는 블렌드 합성식) · eq:si-vshift(mech:43-46) · eq:app-spinodal(appendix:246-251) · eq:app-maxwell(appendix:372-375).

---

## 4. 비약·누락·생략·논리 결함 목록 (기준 ① 중심, ②~⑤ 교차 표기)

| ID | 파일:행 | 성격 | 기준 | tier | 내용 |
|---|---|---|---|---|---|
| G01 | sec12:53-60 vs 74-77 | 사다리 역전 | ⑤① | 확정 | 상수-ΔS 특수형이 박스, 일반 적분형(Kirchhoff 정합)은 미박스. v2 에서는 적분형을 일반 박스로, 상수형을 회수 조건과 함께 특수 박스로 뒤집어야 기준 ⑤ 에 맞는다. |
| G02 | sec13:69-73 | 생략(위임) | ①④ | 확정 | 극대−극소 차 전개를 Ch1 eq:hysdiff 재사용으로 위임. 본 절만 읽는 독자는 artanh 항의 출처를 못 본다. 대수는 정확(본 에이전트 재유도 일치). |
| G03 | ch2v22_notation:7-10 | 기호표 누락 | ②④ | 확정 | 계승 목록에 γ_j 는 있으나 h_{η,j}(부분 cycle 인자, Ch1 `ch1_sec04_hys.tex:238-246` 정의)가 없다. sec13:25·94·123 에서 쓰인다. |
| G04 | sec13:147-156 | 비약(등치 선언) | ①⑤ | 확정 | Ω^cat ↔ ECI 최근접 쌍 평균장 축약을 "접으면 … 이다"로 선언. 클러스터 전개에서 단일 쌍상호작용으로 내려오는 수학(어떤 항을 어떤 조건에서 버리는가)이 없다. 스코프에서 "일반→특수 사다리 결손"의 대표 사례. |
| G05 | sec14:12-16, 71-77 | 정당화 사후·정량 부재 | ①⑤ | 확정 | F^×≈0(config·elec 직교) 가정이 박스 뒤 불릿에서 정당화되고, 결합 잔차의 크기 척도(예: MIT 창 안에서 얼마나 작은가)가 없다. |
| G06 | sec14:34-41 | 단언 | ① | 확정 | eq:lco-configsplit 밑 "w_j=n_jRT/F 서식의 일반형은 n_jR ln[·]" — 폭 다중도 n_j 가 config 부분몰 엔트로피 일반형에 들어가는 근거 유도 없음. |
| G07 | sec15:123-149 | 레퍼런스 부재 | ③ | 확정 | Sommerfeld 전개·Fermi 적분 항등식 ∫ŝ dζ=π²/3 에 교과서 인용 0. 절 전체 cite 는 MIT 물리(mott·imada·marianetti·menetrier·motohashi)와 reynier 뿐. |
| G08 | sec15:241-283 | 모델 가정 | ⑤ | 확정(가정)·추정(대안) | logistic 게이트는 postulate. 결함 농도 의존(`:275`)이 유효범위. 대안 함수형(퍼콜레이션형·불순물 띠 임계 농도형)과의 비교 검토는 없다 — 작업 챕터 3.1 후보. |
| G09 | sec17:123-127, 154-159 | tier C 근사 | ⑤ | 확정(자인) | x↔ξ 선형 보간 tier C · 고정점 1회 갱신 근사(되먹임 상한 14 mV — 본 에이전트 검산 45.7/96485×30 = 14.2 mV 일치) 수렴 미확인 자인. |
| G10 | sec16b:24-34 | 중간식 생략 | ① | 확정 | 곡률 → 커널 사이 dξ/dV = F/(∂²g/∂ξ²) 중간식이 없다(말로만). |
| G11 | sec16b:91-95, 114-116 | 논리 비약(순환) | ① | 확정(문면) | "T_ref 재기준으로 상온 커브 불변"은 ΔH^eff 정의에 의한 항등이고, 이를 "실측 뒷받침 — plain MSMR R²=0.944 ≈ 흑연 0.940"으로 받치는 것은 무관한 비교다(흑연 대비 R² 유사성은 전자항 유무를 검증하지 않는다). |
| G12 | sec16b 전체 vs sifr:33-50 | 지위 불일치 | ②① | 확정(문건 내)·미검증(코드) | brief §4.4 "regsol 은 dQ/dV 커널만 삭제됨" 에 따르면 eq:lcoomega-kernel 도 삭제 대상 커널인데, sec16b 에는 sifr 와 달리 지위 warnbox 가 없고 "+1.25 %p 개선"(`:57`,`:121-122`)·keybox(`:144-146`)가 v1.0.24 문면 그대로다. 코드 실물 대조는 Non-goal 이라 미검증. |
| G13 | sec16b:13, 59, 123, 139, 146 | 내부 라벨 노출 | ② | 확정 | 검수 ID "#7 정정"이 소절 도입·(b) 제목·정리·warnbox·keybox 에 5회. 헌법 ①(내부 라벨·자기 diff 금지) 위반 후보. |
| G14 | sec17:160-168 | 박스 용법 | ② | 확정 | eq:lco-plugin 은 흐름도. 박스 = 결과식 규약과 어긋남. |
| G15 | sec11:90-96 | 박스 용법 | ② | 확정 | 규약 박스. 기준 ① 대상 아님(기록). |
| G16 | sec11:54-65, 67-77 | usable 결함 | ④ | 확정(자인) | 표 캡션이 "시연값(3.930/3.880/4.050)은 표의 물리 anchor 와 전이 구성·순서가 다르다"고 자인 — 같은 T1/T2/T3 이름이 두 다른 세트를 가리킨다. `:38` "전위 오름차순" 서술과 시연 세트(3.93 > 3.88)가 충돌. |
| G17 | sec13:169-178; sec11:63-65; sec14:136-141 | 1차 문헌 공백(자인 G1) | ③⑤ | 확정(자인) | config ΔS 0.47/1.49 J/(mol K) 값·배정 모두 tier C, 원전 미확정, 조성 anchor(x=2/3) 가 실측 질서상(1/2·5/6)·T2/T3 창(0.55/0.48)과 불일치. |
| G18 | sifr:52-66, 151-155 | 논리 약점 | ① | 추정(본 에이전트 판단) | "a-Si = 단일상"의 실측 근거를 우리 피팅 폭 w/(RT/F)=[1.45,2.74,1.09] > 1 로 두고 흑연 두-상 평형 폭 ≪0.12 와 대조한다. 그러나 대조 상대는 흑연의 *평형 예측*(델타)이고 a-Si 쪽은 *관측·피팅* 폭이라 층위가 다르다 — 관측 흑연 peak 도 broadening 으로 유한 폭을 가지므로 이 대조만으로는 단일상이 유일하게 귀결되지 않는다. 문헌(chevrier·artrith)이 실질 근거. |
| G19 | sifr:68-73 | 비약(출발식 근거) | ① | 확정 | eq:sifr-V 를 Ch1 eq:mu·eq:eqcond 인용 없이 "환산해 얻는다"로 제시. 여집합 부호 동치 설명은 있음. |
| G20 | sifr:116-121, 199-204 | 스코프 밖 위임 | ① | 미검증 | 반높이 폭 λ^{3/2}·"0.66/√λ 배 과대평가"는 Ch1 eq:gr2l-fwhm(`ch1_sec05b_gr2L.tex:69` 존재 확인) 소관. |
| G21 | blend:118-122 vs sifr:139-143 | 박스 우선순위 역전 | ② | 확정 | 실제 사용식 eq:blend-dqdv 미박스, 미채택 기록 eq:sifr-blend 박스. |
| G22 | blend:25-27, 42-46, 229-266 | 가정 정직 분류 | ⑤ | 확정 | host 간 독립·평균장 가정 명시, 유한 율속 편차를 GS-2 "물리 가정 충돌"로 4분류 — CLAUDE.md P3 #4 양식 준수. |
| G23 | mech:16-30, 61-69 | 비약(출발식) + 정량 미완 | ①⑤ | 확정 / 추정(수치) | μ = μ⁰ − v̄σ_h 를 postulate. Larché–Cahn 의 개방계 자유에너지(변형 에너지·조성 고유변형)에서 hydrostatic 1차 항으로 내려오는 유도가 없다. Λ_σ 정량은 "확인 필요"로 남겼는데, v̄_Li ≈ 9–10 cm³/mol(Si 몰부피 12.06 cm³/mol 의 ~300 % 팽창을 3.75 Li 로 나눈 어림, 본 에이전트 산술)이면 Λ_σ ≈ 95–105 mV/GPa 로 실측 100–120 과 규모 일치 — v2 에서 닫을 수 있는 항목. |
| G24 | sec01·sec02·sec05 | 유도 밀도 | ② | 확정 | 세 절은 boxed 0·사슬 0 의 등록부·표·명세 절. Chapter 3 본문 1026행 중 유도 박스 4(그 중 2 는 미채택 기록). |
| G25 | appendix:1-13, 41 | 독립·미편입 | ②⑤ | 확정 | 자체 `\documentclass`·자체 [A1]–[A5]·라벨 미공유·ξ 배향 반전(부록 ξ = 본문 θ)·본문 참조는 절 번호 텍스트. v1.0.14 Step 7 의 "편입 여부 사용자 검토 후 결정"(`:7`)이 v1.0.25.1 까지 미해소. |
| G26 | appendix:230-461; sec13 등 | 용어 잔존·불일치 | ②(F-10) | 확정 | "요동" 13회(본문 계열은 `ch3v22_notation.tex:6` 처럼 "fluctuation"). regular solution 의 역어가 "정규용액"(sec11 1·sec13 12·mech 2·appD 2·appendix 7) 과 "정칙용액"(sec16b 4·sifr 7·ch3 bib 1) 으로 갈림. |
| G27 | ch1_appD_si 전체 vs sec01_map | orphan | ② | 확정 | 내용이 §3.1 로 승격된 뒤 원 파일이 `_sections/` 에 잔존(§1.3). 자산 태그 [V21-Q7-01~05]가 이 파일에만 남아 있어 무유실 원칙상 "이동 기록"이 필요. |
| G28 | ch2_appB_codemap:4 / ch1_appD_si:7 | 명명 충돌 | ②(P3 #7 유형) | 확정 | 파일명 `ch1_appD_si` 의 "D" 와 실제 부록 D(`ch2_appB_codemap` 제목 "부록 D")가 충돌. orphan 이라 PDF 에는 안 나오지만 인벤토리 혼동 원인. |
| G29 | ch2v22_bib:17 / ch3v22_bib:43 | 서지 모순 | ③ | 확정(모순)·미검증(정답) | `msmr_origin2017` 과 `verbrugge2017` 이 동일 DOI 10.1149/2.0341708jes·동일 JES 164(11) E3243–E3253 인데 제목이 다르다("… Iron Phosphate, and Layered Nickel-Manganese-Cobalt Oxide" vs "… Silicon, and Their Alloys"). 최소 한쪽은 오기. Crossref 대조 필요(DR-6). |
| G30 | ch2v22_bib:2; ch3v22_bib:2,21 | 주석 스테일 | ③ | 확정 | 헤더 "14종"/"19종" vs 실제 15/36. |
| G31 | ch3v22_bib:13, 19, 31 | 서지 미완 | ③ | 확정(자인) | sethuraman_stresspot2010 쪽 미기재·koebbing2024 권호연 미기재(둘 다 "Crossref 최종 대조" 자인)·lee_sic2025 "e04250" 형식 비정형. |
| G32 | sec15:55; sec11:63; sec14:101; sec01:58; sec02:22,55-57,70,80,86,92-94; sifr:43; sec12:96 | 두문자어 미전개·표기 혼용 | ④ | 확정(스코프 내)·미검증(Ch1 전개 여부) | DFT·NMR·XRD·INS·SEI·XPS·CMC·SBR·FEC·AIC/BIC 미전개, η_ICE 의 풀네임 없음, pOCV/p-ocvhold 프로토콜명 무설명, SOC/SoC/SoH 표기 혼용. |
| G33 | sifr:34,36,45,90-91,116,127,164,167,194,211; sec02_cases:54 | 버전 라벨·자기 diff 본문 노출 | ② | 확정 | "v1.0.25" 11곳·"v1.0.24 까지 있던 … 코드 계약"·"(v1.0.25)" 굵은 소제목 — 합 12곳. 헌법 ① 위반 후보. |
| G34 | sec16b:57,95; sifr:52-53,59,175-176; sec02:21 | 고백조·내부 관점 | ② | 확정(문면) | "우리 ablation 진단"·"우리 진단"·"우리 정칙용액 피팅 진단"·"회사가 자기 dQ/dV 에서 검산 가능"·"본 조사 미확보" — 6곳. 교과서 register 정책 판단 필요. |
| G35 | sifr:43,53,175; sec12:105; sec05 전건 | 코드·도구 토큰 본문 | ②(P3 #8) | 확정 | §7.2 표 참조. sifr:43 은 v1.0.25.1 touch-up 이 새로 들여온 토큰. |
| G36 | sec16b:13,25,27,65,67 vs sec11–17 | 매크로 혼용 | ② | 확정 | sec16b 만 `\cat`·`\config` 매크로(`common_preamble_v1024.tex:56,60` 정의), 나머지는 `\mathrm{cat}`·`\mathrm{config}`. 저자 패치워크 흔적. |
| G37 | ch2v22_sec00_intro:5 vs sec11:32-36,114-117 | 오독 유발 문장 | ④ | 확정(문면) | 서두 "방향 부호 σ_d 의 재배선(… 흑연과 부호 반대)" vs sec11 "부호 골격은 같다 … 층위 구분(모순 아님)". 모순은 아니나 서두가 슬롯 규약 불변을 말하지 않는다. |
| G38 | sec17:4 라벨 `sec:lco-code` | 역사 명칭 | ②(P3 #7) | 확정 | MSMR 동형 절의 라벨이 "code". 타 절에서 "§lco-code 의 변환 대응표" 식으로 12회 참조. |
| G39 | sec05 전체 | 코드=부록 충돌 | ②(P3 #8) | 확정 | §7.1 별도. |
| G40 | sec05:15-19 | 수식 자산에 코드 토큰 | ② | 확정 | eq:si-code-bitexact 안에 `\code{BlendedAnodeDQDV}` 등 식별자. |
| G41 | appendix:30 | 편입 시 preamble 충돌 후보 | ② | 확정(문면)·추정(충돌) | `\newtheorem*{keybox}` — 본문의 keybox(tcolorbox 계열) 와 같은 이름 다른 구현. |
| G42 | sec15:340-391 | 재현 불가(문건 내) | ①④ | 확정 | 한 점 시연 수치(3.9243 V·−0.312 mV/K 등)의 재현 근거가 "구현을 실행"(`:388-390`)이며 완전식·입력 전체는 Ch1·부록 코드 참조. 문건만으로 손 계산 재현은 불가. |

---

## 5. 가정·간소화 지점·레퍼런스 등록부 (기준 ⑤)

각 행은 "일반식 → 특수식"으로 내려오는 지점 하나다. "일반형 제시" 열은 그 절이 특수화 이전의 일반형을 식으로 보여주는지, "레퍼런스" 열은 그 가정에 붙은 외부 근거다.

| # | 파일:행 | 간소화 지점 | 가정·조건 | 유효범위(문건 명시) | 일반형 제시 | 레퍼런스 | tier(문건) |
|---|---|---|---|---|---|---|---|
| A01 | sec11:42-49, 75 | 전이 집합 {T1,T2,T3} | 하프셀 상한 ≤4.2–4.5 V → T4(O3→H1-3) 제외 | 코인 하프셀 | — | xia2007·reynier2004·motohashi2009 | 초기값(tier B/C 혼재) |
| A02 | sec11:19-20; sec13:10-12 | LCO 팔면체 자리 = "동등한 자리" | 격자기체 정규용액 적용 | — | Ch1 eq:gxi | 없음(단언) | — |
| A03 | sec11:60-61; sec17:150-154 | 전자항 T_ref 동결(단일-기준) | ΔS_e 를 상수 오프셋·조성 x_center 동결 | 상온 단일 커브 | eq:lco-U1V(일반) → 동결형 | — | tier C(시연) |
| A04 | sec12:37-39, 68-73 | ΔH T-무관 | Kirchhoff: ΔH 고정 ∧ ∂_TΔS≠0 는 모순 → 적분형으로 읽어야 | 다온도 | eq:lco-kirchhoff(미박스) | 없음(열역학 항등) | — |
| A05 | sec12:79-82 | vib ΔS T-무관 | 고전 극한 k_BT ≫ ħω; LCO 포논 수백 K → 300 K 준양자, 잔여 T-의존 소량 | 다온도 곡률 피팅 | Einstein 절(Ch1 §einstein) 위임 | 없음 | — |
| A06 | sec12:89-92 | 대표 dφ/dT = +0.83 mV/K | 단전극·SOC-무관 대표 스케일 | 크기·부호 sanity 만 | — | swiderska2019 | tier B |
| A07 | sec13:19-25, 147-166 | 전이별 단일 평균장 Ω_j^cat | 클러스터 전개 → 최근접 쌍 평균장 축약 | gap 유무는 피팅 Ω 로 결정 | 없음(G04) | vanderven1998·ml2024 | 초기값 미배정(Ω=0 기본) |
| A08 | sec13:98-101 | γ_j·h_{η,j} 현상학 축소 | spinodal 대칭 평균까지만 엄밀 | — | eq:hyssym | 없음 | 모델 가정(자인) |
| A09 | sec13:204-221 | 도핑 = Ω^pure → Ω^dop 감소 | Al/Mg 비-redox 치환이 상전이 억제 | 우리 시료(갭 G3) | eq:lco-dope Taylor 극한 | reimers1992·vanderven1998(pure) | 갭(자인) |
| A10 | sec14:8-16, 71-77 | Z = Z^config Z^vib Z^elec | 자유도 독립, F^×≈0 선도 차수 | MIT 부근 결합 잔차 무시 | eq:lco-Zfact(일반) | reynier2004(실측 분해) | — |
| A11 | sec14:42-51 | 슬롯 규칙(config = 중심 표준값만) | 혼합항은 w_j 가 담음 → 재기입 금지 | — | eq:lco-configsplit | — | — |
| A12 | sec15:124-131, 150-160 | Sommerfeld 동결 g(E)≈g(E_F) | 축퇴 k_BT ≪ E_F; 보정 O(T³); MIT 중심에서 가장 약함 | 금속상 E_F~eV, k_BT/E_F~0.03 | eq:Sedirect(일반 정보 엔트로피 적분) | 없음(G07) | tier A(함수형) |
| A13 | sec15:237-283 | g(E_F,x) logistic 게이트 | 결함 분산이 유한 폭을 만든다(step 아님) | MIT 창 | — | motohashi2009(g_max)·menetrier1999/reimers1992(창) | 함수형 tier 없음(갭 G2) |
| A14 | sec15:274-279 | Δx_MIT ≈ 0.05 | 2상역 폭 0.19 ≈ ±2Δx | 결함 농도 의존 | — | menetrier1999 | 초기값 |
| A15 | sec16:17-19, 59-62 | 평형 추종·폭 현상학 | dξ/dV = 평형 기울기; w_j = n_jRT/F 자유 폭(두-상 측) | — | Ch1 eq:xieq·wbase | — | — |
| A16 | sec16b:39-51 | Ω→0 폴백·폭 슬롯 분리 | 이상 핵 w^eq=RT/F 와 관측 폭 w_j 별개 층 | — | 명시 | — | — |
| A17 | sec16b:83-95 | ΔH^eff 재기준 | T_ref 오프셋을 유효 엔탈피에 흡수 | 상온 커브 | eq:lcoomega-Tref | — | 정의(항등) |
| A18 | sec17:18-22, 53-60 | MSMR 재모수화 | F/RT 를 폭에 흡수, 방향 부호만 지수에 | 함수형 동형 ≠ 물리량 동일 | eq:br-msmr-1 | msmr_origin2017·bakerverbrugge2018 | — |
| A19 | sec17:120-127 | x(ξ) 선형 보간 | T1 창 두 끝점만 사용 | — | — | 없음 | tier C |
| A20 | sec01:24-29 | Chapter 3 전체 = 문헌 기반 지도 | 자체 실측 Si 대조 없음 | — | — | 8건 사실 목록 | — |
| A21 | sifr:52-66, 170-177 | a-Si 단일상·Ω_Si 범위 시드 | Ω<2RT 단일상 가드, 시드 0.2RT≲Ω<2RT, 점값 피팅 위임 | 상온 단일 곡선은 Ω 민감도 낮음 | eq:sifr-V | chevrier_dahn2009·artrith2018·verbrugge2017 | tier B(폭)·시드 |
| A22 | sifr:183-193 | Ω>2RT 는 Maxwell binodal 로 처리 | 공존역 평탄 + 유한 폭 δ=w_j | 재구현 명세(현행 코드 없음) | 서술만 | — | — |
| A23 | blend:25-27, 42-46 | host 간 독립·평균장 | hard-core·자리 독립을 host 사이로 확장 | 평형(OCV) 정확 | eq:blend-factor | Ch1 §sm-mc | — |
| A24 | blend:78-84 | 질량↔용량 환산 | q_Si=1000(1차 가역)·q_gr=372 | m_Si∈[0,0.30] | 각주 식 | limthongkul2003 | tier A(q_Si) |
| A25 | blend:229-266 | 완전 동시반응 = 평형 극한 1차 근사 | 유한 율속 host 전환·비가산은 범위 밖(GS-2) | — | — | ai_composite2022·chatzogiannakis_blend2025·zhan_siox2026·tu_blend2024 | 공백(4분류: 물리 가정 충돌) |
| A26 | mech:16-30 | 응력항 선형 1차·정수압만 | μ = μ⁰ − v̄σ_h | — | 없음(G23) | larchecahn1973 | — |
| A27 | mech:71-87 | 탄성 가역 → 히스 0; 소성 구성식 범위 밖 | σ_h(θ,이력) 경로 의존 | GS-1 | — | sethuraman_stressevo2010·koebbing2024·jiang_sihys2020 | 공백(4분류: 물리 가정 충돌 + 유도 범위 밖) |
| A28 | appendix:87-102 | 무작위 혼합 평균장 | 이웃 점유 확률 = ξ | — | 격자 모형(일반) | [A3]·[A4] | — |
| A29 | appendix:134-135 | 계면 기여 무시 | 두 상 균일 | 현의 기하 | — | — | — |
| A30 | appendix:402-427, 430-453 | 구형 핵·선형화 CH | 고전 핵생성; 미소 요동 선형 | 동역학 초기 | eq:app-ch-F(범함수 일반) | [A1]·[A2]·[A5] | — |

관찰: "일반형 제시" 열이 식으로 채워진 행은 A03·A04·A10·A12·A17·A18·A23·A28·A30 의 9건이고, 그 중 일반형이 박스인 것은 A28(eq:app-fxi)뿐이다. 스코프의 특수식은 대부분 Chapter 1 의 이미 특수화된 식(정규용액 logistic)을 출발점으로 삼기 때문에, 기준 ⑤ 가 요구하는 "일반식→간소화" 계보는 두 장 안에서는 거의 형성되지 않고 독립 부록이 유일하게 그 꼴을 갖췄다.

---

## 6. 서지·인용 밀도 (기준 ③)

### 6.1 cite ↔ bibitem 대조

| 장 | cite 키 합 | distinct | bib 건수 | cite 됐으나 그 장 bib 에 없음 | bib 에 있으나 스코프에서 미인용 | DOI 부착 |
|---|---|---|---|---|---|---|
| Chapter 2(본문 8절 + appA/appB) | 78 | 16 | 15 | `numverif2026`(appB — Ch1 마스터에서 `ch1v22_bib` 로 해소, 정상) | 0 | 15/15 |
| Chapter 3(본문 6절 + 기호표 + appD) | 106 | 36 | 36 | 0 | 0 | 36/36 |
| 독립 부록 | 0(자체 [A1]–[A5]) | 5 | 5 | — | — | 2/5(단행본 3 은 DOI 없음) |

인용 빈도 상위: Chapter 2 = motohashi2009 14 · reynier2004 11 · reimers1992 9 · vanderven1998 8 · menetrier1999 7 · msmr_origin2017 4 · ml2024 4 · marianetti2004 4; Chapter 3 = chevrier_dahn2009 8 · verbrugge_lisi2016 7 · limthongkul2003 6 · obrovac_chevrier2014 6 · sethuraman 두 편 각 5 · naboka_sic2021 5.

### 6.2 절별 인용 밀도 (distinct 키 / 100행)

| 절 | 행 | cite 키 | distinct | 밀도(키/100행) | 성격 |
|---|---|---|---|---|---|
| sec11 lcointro | 175 | 9 | 7 | 5.1 | anchor 등록 |
| sec12 lcocenter | 112 | 2 | 1 | 1.8 | 유도 절 — 교과서 인용 0 |
| sec13 lcohys | 223 | 16 | 6 | 7.2 | 유도 + srcbox |
| sec14 lcodecomp | 143 | 3 | 1 | 2.1 | 유도 절 — 통계역학 인용 0 |
| sec15 lcoelec | 396 | 28 | 8 | 7.1 | 물리 배경 + 유도(Sommerfeld 인용 0) |
| sec16 lcopeak | 70 | 3 | 3 | 4.3 | 대입 |
| sec16b lcoomega | 160 | 9 | 5 | 5.6 | 정정·옵션 |
| sec17 msmr | 176 | 7 | 3 | 4.0 | 동형 대응 |
| sec01 map | 129 | 17 | 14 | 13.2 | 문헌 등록부 |
| sec02 cases | 173 | 36 | 23 | 20.8 | 문헌 등록부 |
| sec02b sifr | 220 | 10 | 7 | 4.5 | 유도 |
| sec03 blend | 278 | 11 | 7 | 4.0 | 유도 + GS-2 srcbox |
| sec04 mech | 110 | 9 | 8 | 8.2 | 유도 |
| sec05 code | 70 | 3 | 3 | 4.3 | 명세 |
| appD | 91 | 20 | 14 | 22.0 | 등록부(orphan) |
| appendix | 497 | 0 | 5(자체) | 1.0 | 교과서 유도 |

패턴은 뚜렷하다 — 문헌 등록부 절(§3.1·§3.2)은 밀도 13–21, 유도 절(sec12·sec14·sec15 유도부·appendix)은 1–2 이며, 유도 절의 낮은 밀도는 "표준 교과서 결과를 인용 없이 쓴다"는 뜻이다. 리뷰 논문급(기준 ③)은 표준 결과에도 원전·교과서 인용을 요구하므로 v2 의 서지 원장(작업 챕터 3.5·5.1)은 유도 절의 교과서·원전 층을 채워야 한다.

### 6.3 서지 결함(확정)과 1차 문헌 공백 후보(추정)

확정 결함은 §4 의 G29(동일 DOI 2키 제목 상이)·G30(헤더 주석 스테일)·G31(3건 서지 미완)이다. 아래는 리뷰급 필수 문헌 체크리스트(작업 챕터 2.4 게이트)를 위한 **후보**이며 본 에이전트의 추정이다 — 서지 확정은 Crossref 단계에서 하고, Chapter 1 원장(`ch1v22_bib`, 스코프 밖)에 이미 있는지는 미검증이다.

- Chapter 2: LCO 3.9/4.05/4.17 V 전이의 전기화학 원전(Ohzuku–Ueda 1994 계열)·CoO₂ 끝점(Amatucci 1996 계열)·Sommerfeld 전개와 Fermi 적분의 교과서(Ashcroft–Mermin 류)·분배함수 인수분해·부분몰 엔트로피의 통계역학 교과서(Hill/McQuarrie 류)·Gibbs–Helmholtz/Kirchhoff 의 열역학 교과서(Callen/Denbigh 류).
- Chapter 3: Frumkin 등온선 원전 및 삽입 전극 적용(Frumkin 1925·Levi–Aurbach 1997 계열)·Larché–Cahn 후속(1978/1985)과 응력–확산–소성 결합 모델(Bower–Guduru–Sethuraman 2011 계열)·비평형 열역학 관점의 상분리 전기화학(Bazant 2013 계열 — GS-2·v2 일반 이론 후보와 직결).
- 독립 부록: [A1]–[A5]로 자족. 편입 시 V1 키 체계로 이관 필요.

---

## 7. 형식·register·잔존 grep (기준 ②④)

### 7.1 §3.5 코드 명세 절 — 코드=부록 규칙 충돌 (별도 지목)

사실관계(확정): (i) `ch3v22_sec05_code.tex` 본문에 `\code{}` 13행(`:11,12,13,16,28,31,32,33,34,38,56` + `docstring` `:60`)과 `codebox` 환경(`:41-52`), 라벨된 수식 eq:si-code-bitexact(`:15-19`) 안의 클래스명. (ii) 그러나 마스터 `ch3_si_v1.0.24.tex:30-31` 은 `\appendix` 를 이 파일의 `\input` **앞**에 두어, 조립·PDF 상으로는 이 절이 Chapter 3 의 부록(절 번호 A)이다. (iii) 반면 파일명은 `sec05`, 본문 다른 절은 이 절을 "§3.5 코드"라고 부른다(`ch3v22_sec01_map.tex:123` 1회, `ch3v22_sec03_blend.tex:88,109,132,260,272` 5회). (iv) Chapter 1 부록 D(`ch2_appB_codemap.tex:10-11`)는 "함수명은 부록에만 등장한다(본문은 교과서 register)"를 명문화하고 있어, 문건 자신의 규칙과 (i)+(iii)이 어긋난다. (v) `CLAUDE.md` P3 #8 의 확인 게이트 "부록 아닌 `_sections/*.tex` grep 코드토큰 = 0"을 파일 단위로 적용하면 이 파일은 `_sections/` 에 있으면서 이름이 sec 이므로 게이트 문면상 FAIL 이고, 조립 단위로 적용하면 PASS 다 — 게이트 정의 자체가 모호하다.

판정: 물리 규칙(코드는 부록에)과 조립은 이미 일치하고, 어긋난 것은 **파일명·본문 참조 텍스트·라벨(sec:si-code)** 이다. 최소 수정으로 해소되지만 v1.0.25.1 은 동결 base 이므로 v2 에서 "부록으로 명명 정합화 + 본문 6곳 참조를 '부록 A' 로 교체 + eq:si-code-bitexact 를 물리 계약(eq:blend-limit 의 코드판)으로만 남기고 식별자는 부록 표로 이동"이 기본안이다. 사용자 결정 항목으로 DQ-1 에 올린다(사용자가 P3 #8 을 "본문 절 기준"으로 읽는지 "조립 기준"으로 읽는지에 따라 게이트 문면이 달라진다).

### 7.2 코드·도구 토큰 잔존 (본문 절, 부록 제외)

| 파일:행 | 토큰 | 판정 |
|---|---|---|
| sifr:43 | `\texttt{V1025\_DATA\_ADDENDUM.md}` | v1.0.25.1 touch-up 이 새로 도입. 문서 파일명이지만 `\texttt` 토큰이며 헌법 ①(내부 라벨)에도 걸림. |
| sifr:53, 175 | `regsol\_si` | 피팅 진단 도구명. |
| sec12:105 | "코드 시연의 T1 config 기여" | 단어 수준, 토큰 아님 — 경계. |
| sec05 전건 | §7.1 | 조립상 부록. |
| sec03_blend ×5, sec01_map ×1 | "§3.5 코드" | 참조 텍스트(토큰 아님). |

부록 3건(`ch2_appA_traps` 2행·`ch2_appB_codemap` 9행·`ch1_appD_si` 0행)의 `\code{}` 는 규칙상 허용. 단 `ch2_appA_traps.tex:67-68` 은 코드가 아닌 **라벨명**(`eq:Se-ch2`·`eq:Se`)을 `\code{}` 로 감쌌다 — 용법 오류(확정, 경미).

### 7.3 헌법 ① register 잔존(자기 diff·내부 라벨·고백조)

G13(#7 검수 ID 5회)·G33(버전 라벨 12곳)·G34(우리 진단·회사 검산 6곳)·G38(라벨 sec:lco-code). 이 중 G33 의 sifr 11곳은 v1.0.25 "해석적 기록" 지위 표기를 위해 의도적으로 넣은 것이라(파일 헤더 `:13-18` 이력 주석), 지위 표기 자체는 필요하나 "버전 번호로 지위를 말하는" 방식이 교과서 register 와 충돌한다. v2 는 "채택/미채택" 을 버전 번호 없이 말하는 표기 규약이 필요하다(DQ-7).

### 7.4 용어·표기(F-10·F-02·F-03 정합)

- F-10(억지 한글화 금지): "요동" 13회는 전부 독립 부록(`appendix_phase_separation.tex:230-461`) — 부록이 F-10 집행 범위 밖이었음을 시사(확정). 본문 절에서는 0(sec03_blend:277 의 1회는 % 주석).
- regular solution 역어 이원화(G26). 어느 쪽이든 F-10 취지대로 영어 원어 병기가 없다(sec13 도입 `:10` "정규용액 자유에너지" 등).
- F-02(확률 p 소문자)·F-03(f_int/s_int 소문자): 스코프에 해당 기호 출현 없음(근거 미발견 — 해당 없음).
- 두문자어 첫 출현 병기: MIT(sec11:42)·OD(sec13:18)·MSMR(sec17:9)·ECI(sec13:140)·GS/G$n$(sec14:128)는 병기됨. 미병기 목록은 G32.

### 7.5 교재 형식 요소 체크 (기준 ②)

| 요소 | Chapter 2 | Chapter 3 | 독립 부록 |
|---|---|---|---|
| 장 서두·목차 | 있음(sec00 + `\tableofcontents`) | 있음 | 있음(서론 단락) |
| 기호표 | 2단 문장형(표 없음, h_η 누락 G03) | 표 tab:si-notation(신규 기호 12행) | 서두 단락(ξ 배향 주의) |
| 정의/정리 환경 | 없음(bgbox·srcbox 로 대체) | 없음 | keybox(newtheorem*) 2 |
| (a)~(d) 유도 사슬 | 7절 중 6절 | 3절(sifr·blend·mech) | 5절(kinetics 2소절은 축약 자인 `:397-398`) |
| 계산 예제 | sec15 §lco-worked 1건(tier C, 문건 내 재현 불가 G42) | 없음(그림 실계산이 대체) | 수치 예 1건(Ω=3RT, 재현 확인) |
| 검산 박스 | verifybox 2 | verifybox 2 | — |
| 절 요약 | keybox 1(sec16b) | keybox 4 | keybox 2 |
| 원전 다리(srcbox) | 4 | 2 | — |
| 정직 한계(warnbox) | 1 | 5 | — |
| 그림 | 2 | 2 | 2 |
| 표 | 1 | 3 | 분류표 2(비-float) |

Chapter 2 는 "정의·요약" 층이 얇고, Chapter 3 는 "유도·예제" 층이 얇다. 독립 부록이 형식적으로 가장 교재에 가깝다.

---

## 8. 구조 관찰 (v2 설계 입력)

### 8.1 같은 유도의 다중 수록

- 정규용액 미분용량 커널 dQ/dV = QF/|RT/[ξ(1−ξ)] − 2Ω| 가 세 곳에서 따로 세워진다: Ch1 `ch1_sec05b_gr2L.tex:43`(eq:gr2l-disc) · Ch2 sec16b:24-31(eq:lcoomega-kernel) · Ch3 sifr:83-87(eq:sifr-kernel). 세 곳 모두 Ω→0 로지스틱 회수를 각자 설명한다(확정).
- Sommerfeld 전자 엔트로피가 두 곳: Ch1 Part T `ch2_sec03_vibel.tex:56-76`(eq:Se-ch2) · Ch2 sec15:113-149(eq:Se). `ch2_appA_traps.tex:66-69` 가 "동명 식 라벨 충돌 회피"를 함정 표로 기록할 만큼 중복이 구조화돼 있다(확정).
- spinodal·히스 gap: Ch1 §4(eq:spinodal·dUhys) · Ch2 sec13:45-90(대입형) · 독립 부록 §A.4(eq:app-spinodal). 부록은 자기 식이 "본문 §4.1 의 근과 동일"(`:252`)이라고 텍스트로만 잇는다(확정).

이 세 사례가 brief §5 작업 챕터 3.3 의 구조 결정(DG-A)에서 (b) "Part I 일반 이론 + Part II 재료 적용" 쪽을 지지하는 스코프 내 실증이다 — 일반 커널·일반 전자 엔트로피·일반 상분리를 한 번 유도하고 재료 장은 파라미터 치환만 남기면 위 중복이 사라지고 기준 ①·⑤ 가 동시에 충족된다(본 에이전트 판단, DR-3 근거로 제공).

### 8.2 orphan·독립 파일

`ch1_appD_si.tex`(orphan, §1.3)와 `appendix_phase_separation.tex`(독립, 미편입)는 둘 다 "자산 무유실" 원칙(brief §4.4)의 경계 사례다 — 전자는 내용이 §3.1 로 이미 이동했으니 파일 삭제 대신 "이동 기록 + 자산 태그 승계"가, 후자는 v2 Part I 열역학 상분리 절의 시드로 편입이 자연스럽다(DQ-2·DQ-3).

### 8.3 명명·라벨 유산(P3 #7 유형)

파일 접두 `ch1_sec11~17`(Chapter 2 본문)·`ch2_sec00~10`(Chapter 1 Part T)·`ch2_app*`(Chapter 1 부록 C/D)·`ch1_appD`(orphan)은 v1.0.22 재편 이전 명명이 그대로다. DG-2(파일명 유지)는 v1.0.25 한정 규약이었으므로(brief §4.4) v2 에서 정리 가능하나, xr `\externaldocument` 키와 자산 태그 [B2-xxx]·[V22-R5-xx]·[SIFR-x]·[LCOΩ-x]·[V21-Q7-xx] 가 파일에 박혀 있어 이동 맵(§1.4)과 함께 태그 승계표가 필요하다.

### 8.4 Chapter 2 두 축의 접합부

sec16b 는 v1.0.24 에 "per-peak Ω(@3) + 전자항 토글" 두 주제를 한 소절에 넣은 삽입물이고(`ch2_lco_v1.0.24.tex:30` 주석), 매크로·문체·검수 ID 노출이 나머지 7절과 다르다(G12·G13·G36). v2 에서 Ω 커널은 일반 이론으로, 전자항 토글은 구현 옵션(부록)으로 분리되는 것이 자연스럽다(본 에이전트 판단).

### 8.5 CLAUDE.md P3 8항 대조 (스코프 내, R4a 동형 절)

| P3 항 | 스코프 판정 | 근거 |
|---|---|---|
| #1 V_n 계열 구분 | 유지. 본문에 등장하는 것은 V_app(sec11:101 "V_app > V_n")·V_n(Ch3 그림 축·§3.5)·U_oc 셋이고 V_{n,drive}·V_{n,OCV}는 스코프에 없다(해당 없음). 단 U_oc 표기가 `U_\mathrm{oc}`(Ch2·Ch3 본문 25회)와 `U_\oc` 매크로(`ch2_appB_codemap` 11회·sec01 1회)로 소스가 이원화돼 있다 — 조판 출력 동일 여부는 미검증. | grep(주석 제외) |
| #2 전하 보존식 = 중심식 | 유지. sec16:8-15 eq:lco-charge 가 LCO peak 의 (a) 출발식이고, Ch3 는 sec01:102-109 keybox 가 "내부 전위를 결정하는 중심 구조 = 반전 eq:sm-mc-balance"를 앵커로 선언하며 eq:blend-balance(blend:69-75)가 그 host 판이다. OCV 에서 읽는 흐름으로의 회귀 없음. | 확정 |
| #3 순환 의존 dependency graph·표 | 부분. sec17:154-159 가 x↔ξ_eq,1↔U_1 고정점 구조를 문장으로만 서술(그래프·표 없음). blend:84-87 은 U_oc 음함수를 "정의상 implicit formulation"으로 분류하는 문장이 있다. | 확정 |
| #4 4분류 진단 | Ch3 준수 — GS-1(mech:89-99 "물리 가정 충돌 + 유도 미완결")·GS-2(blend:251-266 "물리 가정 충돌"). Ch2 는 sec17 고정점을 분류 라벨 없이 "동결 근사는 순환 없음·정밀형 1회 갱신"으로만 서술. | 확정 |
| #5 refs 6·7 5항 sub-section | 스코프 밖(Chapter 1 부록 E 소관). | 해당 없음 |
| #6 Ch1 기준식 ↔ Ch2~ 전달식 충돌 | 라벨 미해소 0(`results/V1025_DOC_EDIT_REPORT.md:211-227`). 잠재 충돌 = G12(sec16b 커널 지위)·§8.1 다중 수록 3계열(같은 식이 세 곳에서 따로 유도되어 갱신 시 어긋날 구조). | 확정 |
| #7 ver.N ↔ Chapter 명칭 혼동 | 본문에 "ver."·"Part II" 문자열 0(확정 clean). 단 "Part I(흑연)"(sec11:5,12,83·sec12:5·appA:56·appB 2회)와 "Chapter 1"(12파일 21회)이 같은 대상을 가리키며 병존 — Chapter 1 내부 3층(Part 0/I/T, brief A13) 정의로는 합법이나 v1.0.19 "Part I/Part II" 구명칭과 겹쳐 오독 소지(경계). 파일 접두 유산은 G28·G38. | 확정 |
| #8 코드 = 부록 전용 | §7.1·§7.2 — sifr 본문 3행(1행은 v1.0.25.1 신규)·§3.5 는 조립상 부록이나 파일명·라벨·본문 참조 6곳이 본문 절 표기. | 확정 |

---

## 9. 정량 결론

1. 스코프 = 24건 3324행(전문 정독) · boxed 23 · display 84 + `\[` 7 · label 165 · cite 키 Ch2 77(distinct 16)/Ch3 86(distinct 36) · bibitem 15+36+5.
2. 기준 ①(유도 완결): boxed 23 중 유도 대상 16, 완결 14 · 부분 2(eq:lcoomega-kernel·eq:si-coupling) · 비유도 7(규약 1·도식 2·모델 가정 1·정정 1·옵션 1·진술 1). 완결 14 중 본 두 장만으로 따라올 수 있는 것은 8. 문건이 자인하지 않은 논리 결함 3(G11 순환 논증 · G18 층위 혼합 · G04 등치 선언).
3. 기준 ⑤(가정 사다리): 간소화 지점 30 등록, 일반형을 식으로 제시한 지점 9, 일반형이 박스인 지점 1(독립 부록). 일반형 미박스·특수형 박스 역전 1(G01). 출발식 postulate 2(G08 게이트·G23 Larché–Cahn).
4. 기준 ③(서지): DOI 부착 51/51(V1 키), 확정 결함 3건(G29 동일 DOI 2키·G30 주석 스테일·G31 미완 3건), 유도 절 교과서 인용 0(sec12·sec14·sec15 유도부), 리뷰급 필수 후보 8계열(추정).
5. 기준 ②(형식): 코드 토큰 본문 잔존 = sifr 3행(그 중 1행은 v1.0.25.1 신규) + §3.5(조립상 부록·명명 불일치 3중); 헌법 ① 잔존 = 검수 ID 5·버전 라벨 12·고백조 6; 용어 이원화 1(regular solution)·F-10 잔존 13(독립 부록 한정); 박스 우선순위 역전 2(G01·G21); 기호표 누락 1(h_η).
6. 기준 ④(가독성): 두문자어 미전개 11종·표기 혼용 1(SOC/SoC)·오독 유발 서두 1(G37)·시연 세트 명명 충돌 1(G16)·문건 내 재현 불가 예제 1(G42).
7. 구조: orphan 1(`ch1_appD_si`)·독립 미편입 1(`appendix_phase_separation`)·다중 수록 유도 3계열(커널 3곳·Sommerfeld 2곳·spinodal 3곳)·Chapter 1 의존 식 라벨(distinct) Chapter 2 27건/Chapter 3 18건.
8. v1.0.25→v1.0.25.1: sifr 2 hunk, 식·라벨·boxed 불변, touch-up F1 판정 확정.

---

## 10. Decision Queue

골격·결정을 바꾸지 않고, 통합 초안(master)이 판단할 항목을 근거와 기본값 제안과 함께 적는다. 전부 본 에이전트 출처다.

- **DQ-1 §3.5 코드 명세의 처리(P3 #8 게이트 정의)** — 근거 §7.1. 조립은 이미 `\appendix` 뒤(`ch3_si_v1.0.24.tex:30-31`), 어긋난 것은 파일명·라벨·본문 참조 6곳. 기본값 제안 = v2 에서 부록으로 명명 정합화 + eq:si-code-bitexact 의 식별자는 부록 표로 이동, 본문에는 eq:blend-limit(물리 계약)만. 게이트 문면은 "조립상 부록 아닌 절"로 명확화. 한 줄 응답 선택지: 부록 정합화(기본) / 본문 절 유지·게이트 예외 명문화.
- **DQ-2 독립 부록 `appendix_phase_separation.tex` 편입 여부** — v1.0.14 Step 7 미결(`:7`), 마스터 미편입 확정(§1.3). 스코프에서 유일한 완전 "일반→특수" 유도이자 3중 spinodal 수록의 정본 후보. 제안 = v2 Part I 열역학 상분리 절의 시드로 편입(ξ 배향을 본문 θ 로 통일, [A1]–[A5] 를 V1 키로 이관, keybox 구현 통일 G41). 선택지: 편입(기본) / 독립 유지.
- **DQ-3 orphan `ch1_appD_si.tex` 처리** — 내용은 §3.1 에 승격됨(`ch3_si_v1.0.24.tex:3`). 제안 = 이동 기록 + 자산 태그 [V21-Q7-01~05] 승계표 작성 후 v2 인벤토리에서 제외. brief 작업 챕터 1.1 인벤토리 게이트에 "마스터 `\input` 대조 orphan 검사" 추가 제안. 선택지: 이동 기록 후 제외(기본) / 보존.
- **DQ-4 sec16b 지위 불일치(G12)** — LCO per-peak Ω 커널이 v1.0.25 삭제 대상 커널인지는 코드 대조(Non-goal)로만 확정된다. 제안 = 작업 챕터 2.6(regsol 미결 정식화)에 "LCO Ω 커널 지위 확인" 항목을 넣고, 결과에 따라 v2 저작 시 sifr 와 같은 지위 규약 적용. 선택지: 2.6 흡수(기본) / 별도 조사.
- **DQ-5 동일 DOI 2키 서지 정정(G29)** — Crossref 확인이 필요해 DR-6(외부 접근) 결정에 종속. 제안 = DR-6 허용 시 작업 챕터 2.4 첫 검증 항목으로; 불허 시 두 키를 병합하되 제목은 "미검증" 표기. 선택지: 2.4 에서 Crossref(기본) / 병합·미검증 표기.
- **DQ-6 regular solution 역어 통일 및 원어 병기** — G26. 제안 = F-10 취지대로 첫 출현에 "regular solution" 병기하고 한 역어로 통일(어느 역어인지는 사용자 선호). 선택지: 정규용액 / 정칙용액 (+병기는 공통).
- **DQ-7 register 표기 규약(버전 라벨·검수 ID·고백조)** — G13·G33·G34. 제안 = v2 저작 게이트에 "채택/미채택 지위는 버전 번호·검수 ID 없이 서술" 규칙과 grep 게이트(`v1\.0\.`·`#[0-9]`·"우리 진단") 추가. 선택지: 게이트 추가(기본) / 현행 허용.
- **DQ-8 brief 작업 챕터 2.2 게이트 "boxed 64/64 사슬 판정"의 열 추가** — 스코프 23 중 7 이 비유도 박스라 "완결/부분/비유도" 3분류 열이 없으면 64/64 판정이 뒤섞인다. 제안 = 게이트 표에 분류 열과 "비유도 박스의 박스 해제 여부" 결정 열 추가. 골격 변경은 아니고 게이트 산출 형식 보강이다.
- **DQ-9 §3.2b 단일상 판정 논거 재검토(G18)** — 작업 챕터 3.1(열역학 축: 정칙용액→Cahn–Hilliard)과 2.6 판정 기준에 "관측 폭 vs 평형 폭 층위 분리" 를 입력. 결정 아님, 설계 입력 등록 요청.
- **DQ-10 두문자어 전개 위치 정책(G32)** — Ch1 에서 이미 전개됐는지 미검증. 제안 = v2 기호표에 두문자어 표를 두고 장별 첫 출현 병기를 게이트화. 선택지: 기호표 통합(기본) / 장별 병기만.

---

## 11. Read Coverage (파일·행 범위 전건)

전문 정독(Read 도구, head→tail, 생략 없음). 행수는 파일 실측(개행 기준).

| # | 파일 | 행 범위 | 비고 |
|---|---|---|---|
| 1 | `Claude\results\handoffs\2026-09-02-v2-master-plan\brief.md` | 1–219 | 지시·골격 |
| 2 | `_sections\ch1_sec11_lcointro.tex` | 1–175 | |
| 3 | `_sections\ch1_sec12_lcocenter.tex` | 1–112 | |
| 4 | `_sections\ch1_sec13_lcohys.tex` | 1–223 | |
| 5 | `_sections\ch1_sec14_lcodecomp.tex` | 1–143 | |
| 6 | `_sections\ch1_sec15_lcoelec.tex` | 1–396 | |
| 7 | `_sections\ch1_sec16_lcopeak.tex` | 1–70 | |
| 8 | `_sections\ch1_sec16b_lcoomega.tex` | 1–160 | |
| 9 | `_sections\ch1_sec17_msmr.tex` | 1–176 | |
| 10 | `_sections\ch2v22_sec00_intro.tex` | 1–12 | |
| 11 | `_sections\ch2v22_notation.tex` | 1–14 | |
| 12 | `_sections\ch2v22_bib.tex` | 1–21 | |
| 13 | `_sections\ch3v22_sec00_intro.tex` | 1–12 | |
| 14 | `_sections\ch3v22_notation.tex` | 1–46 | |
| 15 | `_sections\ch3v22_sec01_map.tex` | 1–129 | |
| 16 | `_sections\ch3v22_sec02_cases.tex` | 1–173 | |
| 17 | `_sections\ch3v22_sec02b_sifr.tex` (v1.0.25.1) | 1–220 | |
| 18 | `Claude\docs\v1.0.25\_sections\ch3v22_sec02b_sifr.tex` | 1–216 | diff 대조용 |
| 19 | `_sections\ch3v22_sec03_blend.tex` | 1–278 | |
| 20 | `_sections\ch3v22_sec04_mech.tex` | 1–110 | |
| 21 | `_sections\ch3v22_sec05_code.tex` | 1–70 | |
| 22 | `_sections\ch3v22_bib.tex` | 1–44 | |
| 23 | `_sections\ch1_appD_si.tex` | 1–91 | |
| 24 | `_sections\ch2_appA_traps.tex` | 1–75 | |
| 25 | `_sections\ch2_appB_codemap.tex` | 1–77 | |
| 26 | `appendix_phase_separation.tex` | 1–497 | |

부분 확인(구조 확인용 grep·부분 read — brief §3-C 허용 범위, 전문 정독 아님): `ch1_graphite_v1.0.24.tex`(`\input`·`\externaldocument` 행 8-60) · `ch2_lco_v1.0.24.tex`(6-32) · `ch3_si_v1.0.24.tex`(1-32) · `_sections\common_preamble_v1024.tex`(매크로 정의 행 56·60·63) · `_sections\ch2_sec03_vibel.tex`(ssec:elec·eq:Se-ch2 행 56-76·116) · `_sections\ch1_sec04_hys.tex`(h_η 정의 행 238-246) · `_sections\ch1_sec05b_gr2L.tex`·`ch1_sec06_eqpeak.tex`(라벨 존재 행 43·69·46) · `ARCHIVE_NOTE.md`(31-35·91-93) · `results\INDEX_v25.md`(34-35·120-121) · `results\V1025_DOC_EDIT_REPORT.md`(211-213·226-227) · `results\V1025_T13_T14_REPORT.md`(76-78·291-315). 미정독 = 위 부분 확인 파일들의 나머지 영역, Chapter 1 본문 전체(R4a 소관), 코드 `Anode_Fit_v1.0.24.py`(Non-goal), `Codex/`(무접근).
