# R4a — 현행본 Chapter 1(흑연 §0~§10 + Part T + §18 + 부록 A/B/E) 진단 스코핑

> 작성 = 워크플로 서브 [diag_ch1](Fable 5.1), 2026-09-03. 원천 = `D:\Projects\Project_Anode_Fit\Claude\docs\v1.0.25.1\_sections\` 29 파일(전문 정독, 말미 Read Coverage) + `v1.0.25` 동명 2파일 diff. 판정 기준 = brief §2 사용자 기준 1)~5). 사용자 결정으로 적은 것은 brief §2 verbatim 과 `CLAUDE.md` P3 뿐이고, 나머지 판정은 전부 이 서브의 판단이다. 수치는 기계 추출(`count_assets.py`, 주석 줄 `%` 제외) 또는 정독 중 확인한 행 번호이며, 원천에 없는 판정은 "추정"으로 표기했다.

---

## 0. 요지

현행 Chapter 1 은 헌법 ③ 수식-주도 서식((a)출발→(b)연산→(c)중간식→(d)박스)을 **흑연 §1~§9 와 Part 0 에는 대체로 실제로 구현**하고 있으나, **Part T 다섯 절(§2.1·2.2·2.3·2.5·2.7)과 §7 broadening 은 서술형 유도**라 서식이 불균일하다. 범위 내 boxed 식 41건 중 사슬 완비 22·부분 16·없음 1·요약 박스 2 로, 기준 1)(비약·누락·생략 없는 유도) 대비 **17 boxed 가 보강 대상**이고 boxed 밖 결과식 8건이 "수치 확인"·"풀면" 한 마디로 대체돼 있다. 기준 5)(일반→특수 간소화의 가정·유효범위·레퍼런스) 대비 간소화 지점 35건 중 **레퍼런스 부재 17·유효범위 미명시 5** 다. 기준 3)(리뷰급 서지) 대비 장 서지 44건은 인용 키와 1:1 정합하고 DOI 도 단행본·내부자료 9건 외 전건 있으나, **인용 0 인 절이 9/28** 이고 원전급 1차 문헌(Bragg–Williams·Hildebrand·Langmuir·Butler–Volmer·Gibbs–Thomson·Cahn–Hilliard·Daumas–Hérold·fluctuation–dissipation·CLT 등) 이 대부분 교과서 2차 인용이거나 부재다. 기준 2)·4)(교재 형식) 대비 **정의·정리·증명 환경 0·예제 2·연습 0** 이며, F-11(코드=부록) 위반 본문 토큰 **4건**·F-04 버전 태그 본문 줄 **13건** 이 잔존한다. v1.0.25→v1.0.25.1 touch-up 2건(§5·§6)은 식·라벨 불변의 한정 조항 삽입으로 판정에 영향 없다.

---

## 1. 절별 자산 표 (기계 추출 — 주석 줄 제외)

`disp` = `equation/align/gather/multline(*)` + `\[ \]` 환경 수. `cite` = `\cite` 호출 수 / distinct 키 수. 박스 열은 환경 수.

| 파일 | 줄 | disp | boxed | label | cite/키 | sec/sub | fig/tab | warn | key | bg | verify | src | deriv | sign | code | proc |
|---|---:|---:|---:|---:|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ch1_sec00_intro | 95 | 0 | 0 | 1 | 2/4 | 1/0 | 1/0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| ch1_sec01_n0n1 | 245 | 4 | 1 | 11 | 8/7 | 1/4 | 1/1 | 0 | 1 | 1 | 0 | 1 | 0 | 0 | 0 | 0 |
| ch1_sec02a_part0 | 391 | 22 | 5 | 26 | 7/5 | 1/3 | 1/0 | 0 | 0 | 1 | 4 | 1 | 0 | 0 | 0 | 0 |
| ch1_sec02b_part0 | 475 | 20 | 4 | 25 | 3/2 | 0/4 | 3/0 | 0 | 1 | 1 | 3 | 0 | 0 | 1 | 0 | 0 |
| ch1_sec03_center | 122 | 6 | 1 | 10 | 0/0 | 1/2 | 1/0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| ch1_sec04_hys | 337 | 10 | 2 | 16 | 3/2 | 1/3 | 3/0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| ch1_sec05_width | 425 | 12 | 2 | 18 | 6/5 | 1/3 | 3/0 | 0 | 1 | 1 | 1 | 1 | 0 | 1 | 0 | 0 |
| ch1_sec05b_gr2L | 239 | 6 | 1 | 6 | 12/6 | 0/1 | 0/0 | 1 | 1 | 0 | 1 | 1 | 0 | 1 | 0 | 0 |
| ch1_sec06_eqpeak | 132 | 6 | 3 | 5 | 0/0 | 1/0 | 0/0 | 0 | 0 | 1 | 1 | 0 | 0 | 0 | 0 | 0 |
| ch1_sec07_broadening | 376 | 6 | 0 | 10 | 15/10 | 1/3 | 2/0 | 0 | 1 | 1 | 0 | 1 | 0 | 0 | 0 | 0 |
| ch1_sec08_lag | 149 | 10 | 3 | 14 | 0/0 | 1/4 | 0/0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| ch1_sec09_tail | 254 | 13 | 4 | 18 | 0/0 | 1/3 | 2/0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| ch1_sec10_sum | 188 | 4 | 1 | 6 | 7/5 | 1/2 | 1/1 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 |
| ch2_sec00_intro (Part T 서) | 72 | 2 | 1 | 0 | 0/0 | 1/0 | 0/0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| ch2_sec01_partition | 150 | 8 | 1 | 12 | 3/5 | 1/3 | 0/0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| ch2_sec02_config | 191 | 4 | 1 | 10 | 7/5 | 1/4 | 1/1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| ch2_sec03_vibel | 119 | 4 | 1 | 7 | 5/3 | 1/3 | 0/0 | 0 | 1 | 0 | 0 | 1 | 0 | 0 | 0 | 0 |
| ch2_sec04_einstein | 208 | 7 | 2 | 8 | 1/1 | 1/3 | 1/0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| ch2_sec05_mixing | 256 | 10 | 2 | 16 | 6/4 | 1/5 | 1/0 | 2 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 |
| ch2_sec06_limits | 54 | 0 | 0 | 2 | 0/0 | 1/0 | 0/1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| ch2_sec07_revheat | 103 | 2 | 1 | 5 | 5/4 | 1/3 | 0/0 | 0 | 0 | 1 | 0 | 2 | 0 | 0 | 0 | 0 |
| ch2_sec08_synthesis | 239 | 4 | 1 | 8 | 1/1 | 1/3 | 1/2 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| ch2_sec09_method | 65 | 0 | 0 | 3 | 6/5 | 1/2 | 0/0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 1 |
| ch2_sec10_closing | 30 | 0 | 0 | 0 | 0/0 | 1/0 | 0/0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| ch1_sec18_inputs | 93 | 0 | 0 | 3 | 0/0 | 1/1 | 0/1 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| ch1_appA_signcheck | 90 | 0 | 0 | 3 | 1/1 | 1/0 | 0/2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| ch1_appB_codemap | 185 | 0 | 0 | 4 | 0/0 | 1/0 | 0/3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 |
| ch1_appE_selfconsistent | 218 | 9 | 4 | 17 | 8/3 | 1/6 | 0/1 | 2 | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 0 |
| ch1v22_bib | 57 | 0 | 0 | 0 | (bibitem 44) | 0/0 | 0/0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| **합계(범위)** | **5558** | **169** | **41** | **264** | **109 / 44** | **26 / 65** | **22 / 13** | 8 | 11 | 8 | 11 | 10 | 1 | 3 | 2 | 1 |

전 문건 교차검증(60 tex, 주석 제외): boxed **64**(범위 41 + LCO §11~§17 16 + Si 4 + 상분리 부록 3) = brief §4.2 의 64 와 일치. bibitem = ch1 44 + ch2 15 + ch3 36 = **95** = brief 일치. 범위 내 인용 키 44 와 `ch1v22_bib` bibitem 44 는 **집합 동일**(미인용 bibitem 0·미수록 인용 0, `count_assets.py` 출력). `\section` 26 = 서론·§1~§10(§2 는 sec02a 한 절, sec02b 는 그 하위)·§18 = 12 + Part T 11 + 부록 3.

박스 환경의 정의(확정): `ch1_preamble.tex:31-36` 이 `\newtheorem*` 으로 keybox(핵심)·codebox(코드 대응)·signbox(부호 검산)·verifybox(검산)·derivbox(유도)·bgbox(배경)를, `ch2_preamble.tex:31-35` 가 keybox·srcbox(문헌 근거)·warnbox(주의)·procedurebox(계산 절차)·bgbox 를 정의한다. 곧 **정리·정의·보조정리·증명 환경은 정의돼 있지 않다**(`\newtheorem*` 는 박스 이름용).

---

## 2. boxed 식 전건 유도 사슬 판정 (기준 1 — 비약·누락·생략 스코핑)

판정 규칙(이 서브의 기준): (a) 출발식이 본문에 식 또는 명시 전제로 있는가 · (b) 적용 연산이 명명돼 있는가 · (c) 번호 있는(또는 무번호 display) 중간식이 1개 이상 있는가 · (d) 박스가 있는가. **있음** = (a)~(d) 전부 실재. **부분** = (c) 부재 또는 (a)/(b) 중 하나가 "위임·서술·수치 확인" 으로 대체. **없음** = (a)~(c) 중 둘 이상 부재. **N/A** = 로드맵·요약 박스(유도 대상 아님).

| # | 파일:행 | label | (a) | (b) | (c) | (d) | 판정 | 비약·누락·생략 지점 |
|---|---|---|---|---|---|---|---|---|
| 1 | ch1_sec01_n0n1:183 | eq:vn | eq:vapppol(169) | 이항(175) | eq:vnmid(177) | ○ | 있음 | 표지가 (a)(b)(c)로 끝나 (d) 표지 없음(형식만) |
| 2 | ch1_sec02a_part0:12 | (sec:sm-ensemble 앞 사다리) | — | — | — | ○ | N/A | Part 0 로드맵 박스 |
| 3 | ch1_sec02a_part0:76 | eq:sm-gc | eq:sm-S·eq:sm-fund(26,31) | eq:sm-resv·sm-taylor(46,52) | eq:sm-gibbsfactor(59) | ○ | 있음 | canonical $F=-k_BT\ln Z$ 가 열역학 $F$ 와 같다는 근거(64–66)는 선언만 — 부수 갭 |
| 4 | ch1_sec02a_part0:152 | eq:sm-bare | 가정1·2(114–121) | eq:sm-baresum(129) | eq:sm-baremid(140) | ○ | 있음 | — |
| 5 | ch1_sec02a_part0:285 | eq:fermifn | (a′)(233) | eq:partfn(241) | eq:sm-occmid·sm-epstilde(263,272) | ○ | 있음 | $q=(k_BT/\hbar\omega_0)^3$·$\prod[2\sinh]^{-1}$(252–255)는 결과 인용(적분 미시행) |
| 6 | ch1_sec02a_part0:379 | eq:sm-muideal | M 자리(342) | eq:sm-factor(349) | eq:sm-Smix·sm-mucount(360,366) | ○ | 있음 | Stirling 대입 전개 한 단계 생략(358–361, 경미) |
| 7 | ch1_sec02b_part0:58 | eq:sm-thresh | eq:sm-mf(10) | eq:sm-omega(19) | eq:sm-gtheta·eq:mu·eq:gxi(34,40,49) | ○ | 있음 | $g''$ 계산은 결과 한 줄(56) — §4 eq:gpp 가 재유도 |
| 8 | ch1_sec02b_part0:191 | eq:sm-logistic | eq:sm-emu·sm-workbal(143,151) | eq:sm-refbal·뺄셈(159–166) | eq:sm-muV·sm-eqcond(169,178) | ○ | 있음 | 접촉 전위차 흡수(164–168) "전기화학의 표준 처리" — 레퍼런스 0 |
| 9 | ch1_sec02b_part0:346 | eq:sm-mc-balance | 클래스 프레이밍(290) | eq:sm-mc-factor(303) | eq:sm-mc-occ + 무번호(321,336) | ○ | 있음 | — |
| 10 | ch1_sec02b_part0:448 | eq:sm-nernst | eq:sm-mubridge(428) | $\Delta G=\Delta H-T\Delta S$(436–438) | 없음(441–443 "박스는 그 절의 것") | ○ | 부분 | Nernst 반전은 "로그" 한 마디(445–446) — 중간식 0 |
| 11 | ch1_sec03_center:55 | eq:Uj | eq:gibbsdef·mudef(13,18) | eq:eqbalance(26) | eq:eqcond·eq:Ujmid(35,47) | ○ | 있음 | 상수 덩이 $C$ 흡수(31–34): Li⁺ 활동도 상수 가정 명시되나 레퍼런스 0 |
| 12 | ch1_sec04_hys:102 | eq:dUhys | eq:Veq(74) | eq:hyssub(83) | eq:hysdiff(91) | ○ | 있음 | 완결 사례(Taylor 함정 111–119 까지) |
| 13 | ch1_sec04_hys:240 | eq:Ubranch | eq:hyssym(233) | "한 자유도로"(237) | 없음 | ○ | 부분 | $\gamma_j\cdot h_{\eta,j}$ 는 현상학 정의(정의상 유도 불요) — 유효범위·상한 명시(246–252) |
| 14 | ch1_sec05_width:93 | eq:tst-box | 두 전제(52–55) | eq:tst-qrc·tst-freq(59,67) | eq:tst-rate·tst-dG(78,84) | ○ | 있음 | 반쪽 Maxwell 평균 $\langle v\rangle$(64) 결과 인용 |
| 15 | ch1_sec05_width:283 | eq:xieq | eq:bv(17) | eq:db(24) | eq:logisticsolve·eq:wbase(33,267) | ○ | 부분 | bare logistic 은 완결; **$n_j$ 다중도 일반화(266–271)는 정의 삽입** — 물리 기원·레퍼런스 0 |
| 16 | ch1_sec05b_gr2L:140 | eq:gr2l-box | eq:gr2l-mu(32) | eq:gr2l-disc(39) | eq:gr2l-split(113) | ○ | 있음 | eq:gr2l-fwhm(66) 반높이 폭은 "풀면"·"수치 확인"(62–75) — 별건(§2.1 비-boxed 목록) |
| 17 | ch1_sec06_eqpeak:25 | eq:eqpeak | 보존식(8) | eq:belliden(13) | 연쇄율(19–20) | ○ | 있음 | — |
| 18 | ch1_sec06_eqpeak:43 | eq:skewpeak | 재모수화 정의(39–41) | "위 (b)(c)와 똑같은 연쇄율"(41) | 없음 | ○ | 부분 | 연쇄율 1줄 생략; eq:skewapex(52) 정점 조건은 "수치 확인"(58,63) |
| 19 | ch1_sec06_eqpeak:91 | **(라벨 없음)** | eq:sm-flucres·sm-mc-fluc(77–78) | 무번호(82–87) | $k_B/R=1/N_A$(88–89) | ○ | 있음 | **boxed 인데 `\label` 부재** — 참조 불가(형식 결함) |
| 20 | ch1_sec08_lag:21 | eq:Lq | 운동방정식(10) | 지연변수(12) | eq:Lqmid(14) | ○ | 있음 | — |
| 21 | ch1_sec08_lag:73 | eq:dHeff | 합-1(57) | eq:chid(59) | 무번호 정리식(77–84, 박스 뒤) | ○ | 부분 | "장벽 흡수" 논증(65–71)이 극한 대입 서술; "보강 미적용 시 그대로"(85)는 구현 토글 |
| 22 | ch1_sec08_lag:125 | eq:LV | eq:kuniv(27) | eq:Lqmid2(105) | eq:Lqfull(114) | ○ | 있음 | $\lvert dV/dq\rvert_{q_a}$ 환산 논리 한 줄(122–123); eq:Acut $z_\mathrm{cut}=4.357$(44) 근거 없음 |
| 23 | ch1_sec09_tail:59 | eq:lag | eq:intfactor(14) | eq:memory(21) | eq:memory-Vaxis·lag-byparts·lag-mid(36,43,51) | ○ | 있음 | 완결 사례 |
| 24 | ch1_sec09_tail:110 | eq:peakshape | 서술(105–108) | 서술 | 없음 | ○ | 부분 | $d\xi_j/dV = d\xi_{eq}/dV - dr_j/dV = r_j/L_V$ 의 한 줄 대수 부재(105–108 문단만) |
| 25 | ch1_sec09_tail:144 | eq:tail-limit | eq:tail-limit-start(120) | eq:tail-limit-sub(126) | eq:tail-limit-mid(136) | ○ | 있음 | 지배수렴정리 레퍼런스 0(교재급이면 각주 필요) |
| 26 | ch1_sec09_tail:179 | eq:reversal | 서술(159–163) | 서술(165–168) | 없음("같은 부분적분 반복" 172–175) | ○ | 부분 | 거울 유도 반복 생략 — 중간식 0 |
| 27 | ch1_sec10_sum:9 | eq:sum | 보존식(5) | 미분(5–6) | 없음 | ○ | 부분 | 중간식 0(§6 (a)와 동일 대수라 실질 갭 작음); "서로소 자리 분해" 가정 명시·레퍼런스 0 |
| 28 | ch2_sec00_intro:47 | (사슬 박스) | — | — | — | ○ | N/A | Part T 로드맵 |
| 29 | ch2_sec01_partition:73 | eq:logistic | eq:Z1(20) | eq:occ(27) | eq:muV·단위환산(53,66–70) | ○ | 있음 | Part 0 eq:sm-logistic 과 **중복 유도**(통합 후보) |
| 30 | ch2_sec02_config:15 | eq:Sconfig | 베르누이 서술(12) | 없음 | 없음 | ○ | 부분 | $-R\sum p\ln p$ 가 배치 엔트로피인 근거는 Part 0 eq:sm-Smix(sec02a:360) 가 대신 — 이 절 안에는 정의 인용만 |
| 31 | ch2_sec03_vibel:73 | eq:Se-ch2 | eq:Se_start(60) | Sommerfeld 적분 결과 인용(65–66) | $C_e\to S_e$ 적분(67–71) | ○ | 부분 | Sommerfeld 적분 자체 미유도(LCO §15 위임, 범위 밖); ashcroftmermin 인용은 sec02a 에만 |
| 32 | ch2_sec04_einstein:34 | eq:Svib-einstein | (a)(27) | (b)(29) | (c) 항등(30–31, "대수적으로") | ○ | 있음 | 항등 대수 생략(경미); eq:Svib_mode(ch2_sec03:24) 는 서술형 유도 |
| 33 | ch2_sec04_einstein:97 | eq:dUvib | (a)(75) | (b)(81) | (c)(88) | ○ | 있음 | "Kirchhoff $\Delta C_p$ 상쇄"(106–108) 근거 서술만 |
| 34 | ch2_sec05_mixing:75 | eq:weighted | eq:implicit(16) | eq:implicit_diff(31) | eq:gj·eq:dxidT(38,48) | ○ | 있음 | eq:dxidT 연쇄율 전개 생략(45–47, 경미) |
| 35 | ch2_sec05_mixing:220 | eq:hys_rev | eq:hys_branch(212) | "한 사이클 상쇄" 서술(217) | 없음 | ○ | 부분 | 선형화·$O(\Delta U^2)$ 논증(224–229) 서술만 |
| 36 | ch2_sec07_revheat:18 | eq:qrev | **Bernardi 원식 미기재**(11–14 인용만) | 소거 서술(22–25) | 없음 | ○ | **없음** | 일반 에너지 수지→두 항 축약 유도 부재 — srcbox(27–45) 항 대응표만; 가정·레퍼런스는 명시 |
| 37 | ch2_sec08_synthesis:17 | eq:complete | eq:weighted+single_config | 조립 서술(ch2_sec05:85–88 "마저 넣으면") | 없음 | ○ | 부분 | 둘째 조각을 eq:implicit_diff 에 넣는 한 줄 대수 생략 |
| 38 | ch1_appE_selfconsistent:52 | eq:sc-true | eq:sc-frozen(32) | $\kappa(\xi)$ 정의(50) | 없음 | ○ | 부분 | 지수 인수 $2\chi_d$ 의 기원($-\Omega(1-2\xi)-(+\Omega)=-2\Omega(1-\xi)$) 미기재(46–56) |
| 39 | ch1_appE_selfconsistent:87 | eq:sc-ratio | eq:sc-volterra-eq(62) | eq:sc-split(78) | 치환 서술(83–85) | ○ | 있음 | — |
| 40 | ch1_appE_selfconsistent:150 | eq:sc-valid | 오차원 서술(146) | $\delta\kappa L_V\approx\delta\ln L_V$(147) | 없음 | ○ | 부분 | $\Delta\xi_\mathrm{supp}\approx L_V/(4w)$ 근거 미기재 |
| 41 | ch1_appE_selfconsistent:185 | eq:sc-transfer | eq:sc-frozen LTI(181) | Fourier 서술 | 없음 | ○ | 부분 | 1계 완화 전달함수 1줄 유도 생략(경미) |

**집계**: 있음 22 · 부분 16 · 없음 1 · N/A 2 = 41. 기준 1) 대비 보강 대상 = 부분 16 + 없음 1 = **17 boxed**.

### 2.1 boxed 밖 결과식 중 "풀면·수치 확인·표준" 으로 대체된 지점(기준 1 추가 목록)

| # | 파일:행 | 식 | 대체 표현 | 성격 |
|---|---|---|---|---|
| N1 | ch1_sec05b_gr2L:66 | eq:gr2l-fwhm(FWHM 닫힌형·$\lambda^{3/2}$ 점근) | "풀면"(62–64)·"수치 확인"(75) | 반높이 조건 → artanh 닫힘 → 급수 전개 3단 생략 |
| N2 | ch1_sec06_eqpeak:53 | eq:skewapex | "수치 확인"(58,63) | 정점 조건 $\xi=\alpha/(\alpha+1)$ 미분 생략 |
| N3 | ch1_sec07_broadening:158 | eq:widthbudget | "logistic 분산 $\pi^2w^2/3$"(165–167) 결과 인용 | 분산 적분·합성곱 분산 가법 미유도 |
| N4 | ch1_sec07_broadening:264 | eq:gibbsthomson | 결과식만 | Gibbs–Thomson 원전·유도 0 |
| N5 | ch1_sec08_lag:44 | eq:Acut $z_\mathrm{cut}=4.357$ | "이 5% 컷에 대응하는 선택값"(41–42) | $\xi(1-\xi)=0.05/4$ 의 근이 $z=4.357$ 임을 미기재(수치는 정합함 — 서브 검산) |
| N6 | ch2_sec03_vibel:24 | eq:Svib_mode | 서술형(14–22) | 식 전개는 문장 안에 — display 중간식 0 |
| N7 | ch2_sec03_vibel:66 | Sommerfeld $\int(-\partial f/\partial E)(E-E_F)^2dE=\tfrac{\pi^2}{3}(k_BT)^2$ | "표준"(65) | 범위 밖 §15 위임 |
| N8 | ch2_sec05_mixing:48 | eq:dxidT | 연쇄율 서술(45–47) | $\partial\xi/\partial a\cdot\partial a/\partial T$ 전개 생략 |

### 2.2 서식 균일성(헌법 ③ (a)~(d) 표지 실재 여부 — `\textbf{(a` 류 카운트)

Part 0(sec02a a=b=c=d=4, sec02b 4/4/4/4)·§3(2/2/1/2)·§4(3/3/2/2)·§5(3/2/3/2)·§5b·§6·§10(각 1/1/1/1)·§8(4/4/1/4)·§9(5/4/4/4)·Part T §2.4(2/2/2/2)·§2.8(1/1/1/1)·§1(1/1/1/0) 은 표지가 있으나, **§7 broadening·Part T §2.1·§2.2·§2.3·§2.5·§2.7·부록 E 는 표지 0**(서술형). 곧 헌법 ③ 서식이 절의 약 3분의 1 에서 적용되지 않았다(확정 — grep 카운트).

### 2.3 v1.0.25 → v1.0.25.1 diff 반영

- `ch1_sec05_width.tex:303-304`(+1줄): "$w_\mathrm{eff}$ 는 중심 높이 척도이지 반높이 폭이 아니다 — FWHM 은 $\lambda^{3/2}$" 포인터 삽입. 식·라벨·boxed 불변. 판정 #15 불변, 기준 5 지점 S16 의 유효범위 서술이 한 단계 강화됨.
- `ch1_sec06_eqpeak.tex:107-108`(+1줄): 감수율 항등 유도 서식이 "이상 격자기체이자 **대칭 종($\alpha_j=1$)**에서 정확" 으로 한정. 판정 #19 불변, 유효범위 명시 강화.
- 두 건 모두 brief §4.2 의 "M-w·L-bg" 에 대응(추정 — brief 는 4건을 열거하나 이 범위 파일 diff 는 2건이며 나머지 F1·F3 은 `ch3v22_sec02b_sifr` 한 파일에 있는 것으로 추정).

---

## 3. 간소화 지점 — 가정·유효범위·레퍼런스 유무 (기준 5)

"일반식 → 특수식" 으로 내려가는 지점 35건. ○ = 본문에 명시, △ = 부분·암묵, × = 부재.

| # | 파일:행 | 간소화(일반→특수) | 가정 명시 | 유효범위 | 레퍼런스 |
|---|---|---|---|---|---|
| S1 | ch1_sec02a:116 | 다중 점유 → hard-core 배타 $n\in\{0,1\}$ | ○ | △(정전·입체 반발 서술) | × |
| S2 | ch1_sec02a:119 · sec02b:6 | 자리 상관 → 독립(가정 2) → 평균장 완화 | ○ | ○(강상관 $\Omega>2RT$ 예외 sec02b:403) | ×(Part 0) / ○ huggins2009·bazant2013(ch2_sec01:110) |
| S3 | ch1_sec02a:51 | 저장조 엔트로피 1차 Taylor 절단 | ○ | △("훨씬 크다") | × |
| S4 | ch1_sec02a:252 | 내부 자유도 → 3D 등방 조화 우물 $q(T)$ | ○ | △(등방 풀기 언급) | ○ hill1960·fowler1939·mcquarrie1976 |
| S5 | ch1_sec02a:358 | $\ln m!$ Stirling | ○ | ×($M\gg1$ 암묵) | × |
| S6 | ch1_sec02b:11 | 정확 상호작용 → Bragg–Williams $\frac{Mz}{2}u\theta^2$ | ○ | ○(클래스 간 상관 배제 sec02b:315) | ○ hill1960·mcquarrie1976(sec02b:309) — 원전 Bragg–Williams × |
| S7 | ch1_sec02b:164 | 접촉 전위차 → 측정 전위 정의에 흡수 | ○ | △ | ×("표준 처리") |
| S8 | ch1_sec02b:188 | $\Omega_j\ne0$ 암시 등온선 → $\Omega_j=0$ 닫힌 logistic | ○ | ○(211–216 (iii)) | — |
| S9 | ch1_sec02b:429 | $\mu=\partial G/\partial n\vert_{T,P}\simeq\partial F/\partial n\vert_{T,V}$ | ○ | ○($P\Delta v\ll RT$ 수치) | × |
| S10 | ch1_sec03:45 | $\Delta G_j(T)=\Delta H-T\Delta S$ 에서 $\Delta H,\Delta S$ 온도 무관 | × (암묵 — $\Delta C_p=0$) | × | ×(Kirchhoff 언급은 ch2_sec04:106 에만) |
| S11 | ch1_sec03:31 | Li⁺ 활동도·기준 퍼텐셜 → 상수 $C$ | ○ | ×(전해질 조성 의존 미언급) | × |
| S12 | ch1_sec04:247 | spinodal 상한 → 실측 gap $\gamma_j$ 축소 | ○ | ○(이상 단일 입자 상한) | △ dreyer2010 부호만·CNT 는 별도 부록 |
| S13 | ch1_sec04:250 | 완전 cycle → 부분 cycle $h_{\eta,j}$ | ○ | × | × |
| S14 | ch1_sec05:52–55 | TST 두 전제·$\kappa=1$·변분 TST/터널링 배제 | ○ | ○ | ○ laidlerking1983·glasstone1941·eyring1935 |
| S15 | ch1_sec05:149 | 조성 의존 교환전류 → 상수 $k_0e^{-\Delta G_a/RT}$ | ○ | ○ | ○ bazant2013(가정차 명시) |
| S16 | ch1_sec05:266 | bare $RT/F$ → 다중도 $n_j$ 폭 | ×(정의 삽입) | △(이중지위 299–320) | ×(MSMR $\omega_j$ 는 appB:42 에만) |
| S17 | ch1_sec05b:96 | 다중 부분격자 staging → 단일 $\Omega_j$ | ○ | ○ | ○ persson2010b |
| S18 | ch1_sec07:28 | Maxwell 값 vs Dreyer 순차 경로 | ○ | ○ | ○ dreyer2010·2011 |
| S19 | ch1_sec07:105 | $U_j$ 입자 무관 상수 | ○ | ○(tier C 표기) | △ park2021(전극 수준) |
| S20 | ch1_sec07:135 | 다수 독립 $\eta_k$ 합 → CLT Gaussian | ○ | ○(Lindeberg·$m=1$ 이탈) | × |
| S21 | ch1_sec07:153 | 합성곱 분산 가법·logistic 분산 | ○ | ○ | × |
| S22 | ch1_sec07:264 | Gibbs–Thomson $\Delta U=2\gamma V_m/(Fr)$ | ○ | ○(마이크론 배제 수치) | ×(원전) / cogswell2012 는 $\gamma$ 논의만 |
| S23 | ch1_sec08:38 | $L_V(\xi)$ → 컷점 동결 상수 | ○ | △(appE $\varepsilon$ 로 후행) | ×($z_\mathrm{cut},A_\mathrm{cap}$ 선택값) |
| S24 | ch1_sec08:68 | 상호작용 몫 → 깊은 꼬리 $\xi\to1$ 상수 $+\Omega$ | ○ | ○ | × |
| S25 | ch1_sec09:31 | $q_0$ 유한 → $-\infty$ | ○ | ○(유계·$L_q>0$) | — |
| S26 | ch1_sec10:6 | 전이 진행 서로소 자리 분해 | ○ | × | × |
| S27 | ch1_sec10:16 | $C_\mathrm{bg}(V)$ → 창-국소 상수 | ○ | ○(3 조건) | ×(공개 4셀 실측은 내부 자료) |
| S28 | ch2_sec03:47 | $\Delta S_\mathrm{vib}(x)$ → 중심 상수 흡수(고전 극한) | ○ | ○ | ○ reynier2003·jpcc2021 |
| S29 | ch2_sec03:64 | Fermi–Dirac 적분 → Sommerfeld 축퇴 $k_BT\ll E_F$ | ○ | ○(ch2_sec06 표) | △ ashcroftmermin 은 sec02a 에만 |
| S30 | ch2_sec04:18 | 포논 스펙트럼 → Einstein 단일 모드 | ○ | ○(연화형 한정 51–58) | ○ jpcc2021 |
| S31 | ch2_sec07:22 | Bernardi 일반 수지 → 두 항(혼합 엔탈피·상변화 소거) | ○ | ○(고율 잔여) | ○ bernardi1985 |
| S32 | ch2_sec05:224 | 분기 평균 = 가역 몫(선형화 $\Delta U^\mathrm{hys}\ll w_j$) | ○ | ○ | × |
| S33 | ch2_sec00:59 | 전셀 → 하프셀 단독 | ○ | ○ | — |
| S34 | ch1_appE:150 | 참 Volterra → 1차 ratio ($\varepsilon\ll1$) | ○ | ○(수치·열화 warnbox) | ○ lee2017jcp·lee2011jcp·son2013jcp |
| S35 | ch1_appE:70 | Fredholm(논문) vs Volterra(문건) 구조 차 | ○ | ○ | ○ |

**집계**: 레퍼런스 × = 17(S1·S3·S5·S7·S9·S10·S11·S13·S16·S20·S21·S22·S23·S24·S26·S27·S32; S2 는 Part 0 쪽만 ×) · 유효범위 × = 5(S5·S10·S11·S13·S26) · 가정 미명시 = 2(S10·S16). 기준 5)가 요구하는 "레퍼런스가 확실한 가정" 에서 가장 먼 지점은 **S10(ΔC_p=0 암묵)·S16(n_j 다중도의 물리 기원 부재)·S23(z_cut·A_cap 선택값)** 이다.

---

## 4. 서지 — 절별 인용 밀도와 1차 문헌 공백 (기준 3)

### 4.1 절별 인용 밀도(`\cite` 호출 / 100줄)

| 절 | cite | 줄 | /100줄 | 절 | cite | 줄 | /100줄 |
|---|---:|---:|---:|---|---:|---:|---:|
| §0 서론 | 2 | 94 | 2.1 | Part T 서 | 0 | 71 | **0.0** |
| §1 N0N1 | 8 | 244 | 3.3 | T§1 partition | 3 | 149 | 2.0 |
| §2a Part 0 | 7 | 390 | 1.8 | T§2 config | 7 | 190 | 3.7 |
| §2b Part 0 | 3 | 474 | 0.6 | T§3 vibel | 5 | 118 | 4.2 |
| §3 center | 0 | 121 | **0.0** | T§4 einstein | 1 | 207 | 0.5 |
| §4 hys | 3 | 336 | 0.9 | T§5 mixing | 6 | 255 | 2.4 |
| §5 width | 6 | 424 | 1.4 | T§6 limits | 0 | 53 | **0.0** |
| §5b gr2L | 12 | 238 | 5.0 | T§7 revheat | 5 | 102 | 4.9 |
| §6 eqpeak | 0 | 131 | **0.0** | T§8 synthesis | 1 | 238 | 0.4 |
| §7 broadening | 15 | 375 | 4.0 | T§9 method | 6 | 64 | 9.4 |
| §8 lag | 0 | 148 | **0.0** | T 맺음 | 0 | 29 | 0.0 |
| §9 tail | 0 | 253 | **0.0** | §18 inputs | 0 | 92 | **0.0** |
| §10 sum | 7 | 187 | 3.7 | 부록 A | 1 | 89 | 1.1 |
| 부록 B | 0 | 184 | 0.0 | 부록 E | 8 | 217 | 3.7 |

인용 0 인 절 = §3·§6·§8·§9·§18·Part T 서·T§6·맺음·부록 B(9/28). 이 중 **§3(Gibbs·전기화학 평형)·§6(전하 보존·감수율)·§8·§9(Eyring 완화·인과 기억)** 는 열역학·동역학 핵심 절인데 원전 인용이 한 건도 없다(확정).

### 4.2 서지 원장 상태(`ch1v22_bib.tex`, 44 항)

- 인용 키 ↔ bibitem 1:1(미인용·미수록 0). DOI 부재 9건은 전부 단행본(hill1960·fowler1939·glasstone1941·mcquarrie1976·ashcroftmermin1976·mckinnon1983·newman·huggins2009)과 내부 자료(numverif2026) — 정상.
- 리뷰급 기준에서 문제 있는 항: **numverif2026**(`ch1v22_bib.tex:44` — "본 연구 내부 수치 검증" 을 참고문헌으로 등재; 리뷰 논문 규범상 부록·각주 이관 대상), **schmitt2022**(`:48` — 저자 전체·권쪽 "사용 시 Crossref 최종 대조" 미완 표기), **rsc2021**(`:25` — K-graphite 비교 인용을 Li-graphite staging 분류 근거로 사용, tier B), **occupation2019·chemmater2015·jpcc2021**(`:37–39` — "원문 식 미확보·abstract tier" 명시), **msmr_partI**(`:40` — 별개 논문 함정 각주 존재).
- 판정: 서지 검증 수준은 정직하나 리뷰급에는 미달 — 1차 원문 미확인 4건·내부 자료 1건.

### 4.3 1차 문헌 공백 후보(리뷰급 주제별 필수 문헌 대조 — 이 서브의 조사 후보 제시이며 서지 확정은 작업 챕터 2.4·5 소관)

| 주제(본문 위치) | 현행 인용 | 공백(원전급 후보 — 서지 확정 전 "후보") |
|---|---|---|
| lattice gas·Langmuir 두-상태(sec02a:156) | hill1960·fowler1939·mckinnon1983 | Langmuir 1918 원전 × ; lattice gas–Ising 동치(Lee–Yang 1952) × |
| Bragg–Williams·정규용액(sec02b:9·29) | (Part 0) × / huggins2009·bazant2013(Part T) | Bragg & Williams 1934 × ; Hildebrand regular solution 원전 × ; Guggenheim 1952 × |
| Nernst·전기화학 평형(sec02b:140·sec03) | × | Nernst 원전·Newman 교과서(newman 은 Part T 에만) |
| spinodal·binodal·Maxwell(sec04·sec07) | dreyer2010·2011 | Cahn–Hilliard 1958·Cahn 1961 × (상분리 부록에 있을 가능성 — 미검증, 범위 밖) |
| staging 이론(sec01·sec05b) | dahn1991·ohzuku1993·persson2010b | Daumas–Hérold 1969 × ; Safran 1980 staging 이론 × |
| Eyring·TST(sec05) | eyring1935·glasstone1941·laidlerking1983 | 충분(원전 있음) |
| Butler–Volmer·전하전달(sec05:124) | bazant2013 | Butler 1924·Erdey-Grúz & Volmer 1930 × ; Marcus 1956/1965 × (동역학 축 후보) |
| detailed balance(sec05:28) | × | Onsager 1931 / Tolman × |
| fluctuation–dissipation·감수율(sec06:75–101) | × | Callen–Welton 1951·Kubo 1957 × ; 대정준 요동 항등은 mcquarrie(sec02b:369)만 |
| CLT·Lindeberg(sec07:135) | × | 확률론 교과서(Feller 등) × |
| Gibbs–Thomson(sec07:264) | × | Thomson/Gibbs 원전 또는 Porter–Easterling 류 교재 × |
| 인과 기억·Volterra·지배수렴(sec09·appE) | lee2017jcp 계열 | 적분방정식 교과서(Tricomi/Linz)·해석학 정리 각주 × |
| Bernardi 에너지 수지(ch2_sec07) | bernardi1985·newman | 충분(원전 있음); Thomas–Newman 2003 열 수지 확장 후보 |
| Sommerfeld·전자 엔트로피(ch2_sec03) | ashcroftmermin(sec02a 에만) | 절 내 인용 0 — 이동 필요 |
| 흑연 엔트로피 실측(ch2_sec02·03) | reynier2003·allart2018·baek_pilon2022 | Reynier 2004 JES(엔트로피 전위차법 상세) 후보 |
| ICA 방법론(sec00) | bloom2005·dubarry2012 | 충분 |

---

## 5. 교재 형식 요소 존재 체크와 F-04/F-10/F-11 잔존 (기준 2·4)

### 5.1 형식 요소(확정 — grep + preamble 확인)

| 요소 | 존재 | 근거 |
|---|---|---|
| 정의(definition) 환경 | **0** | `\newtheorem`/`\begin{definition}` 없음(preamble·본문 전건). 정의는 본문 문장·keybox 로만 |
| 정리·보조정리·명제·증명 환경 | **0** | 동상. verifybox(11)가 "검산" 역할을 대신하나 정리-증명 구조는 아님 |
| 유도 서식 (a)~(d) | 부분 | §2.2 참조 — 절의 약 1/3 미적용 |
| 예제(worked example) | **2** | `ch1_sec10_sum.tex:136`(끝-대-끝 $V_n=0.085$ V)·`ch2_sec08_synthesis.tex:41`($\bar x=0.25$ 가역 발열) |
| 연습문제 | **0** | 없음 |
| 절 요약 | 부분 | keybox 11(§1·§2b·§5·§5b·§7·T§1·T§3·T§6·T§8·§18·appE) + Part T 맺음 + §18 진행 요약; §3·§4·§6·§8·§9·§10 은 요약 박스 없음 |
| 기호표 | ○ | `tab:notation`(ch1_sec01_n0n1:43–89, longtable); Part T 별도 `ch2v22_notation.tex` 존재(범위 밖 — 목록 확인만, 미정독) |
| 노드↔식 색인 | ○ | `tab:nodemap`(ch1_sec18_inputs:55–86) |
| 검산표 | ○ | 부록 A S1–S8·R1–R6 |
| tier 신뢰 등급 규약 | ○ | ch1_sec07_broadening:64 각주에 전역 정의 |

판정(기준 2·4): 대학원 열역학·통계역학 교재 형식과 대조하면 정의·정리·증명의 구조화 요소가 전무하고 예제가 문건 전체에 2건뿐이며, 각 절의 "핵심 박스" 가 절반의 절에만 있다. 타전공 석박사 가독성 관점에서 가장 큰 부담은 **절 도입부의 전방 참조 밀도**(예: sec01:31–35 의 $s$ vs $\sigma_d$ 구분이 §2b·§5 를 미리 참조)와 **역사적 리비전 어휘의 잔존**(아래 5.3)이다 — 정성 판정(추정).

### 5.2 F-11(코드 = 부록 전용) 잔존 — 본문 25 파일, 주석 줄 제외(확정)

| 파일:행 | 토큰 | 성격 |
|---|---|---|
| ch1_sec05b_gr2L.tex:85 | `regsol2` | 진단 스크립트 식별자 |
| ch1_sec05b_gr2L.tex:212 | `regsol2` | 동상 |
| ch1_sec10_sum.tex:145 | `\code{use\_si\_constants()}` | 각주 안 코드 함수명 |
| ch2_sec08_synthesis.tex:56 | `\code{use\_si\_constants()}` | 각주 안 코드 함수명 |

**4건**. `CLAUDE.md` P3 #8 게이트("부록 아닌 `_sections/*.tex` grep 코드토큰 = 0")에 대해 현행본은 **FAIL 상태**다(확정). 부록 B·E 의 코드 토큰은 규범상 허용.

### 5.3 F-04(교과서 register — 자기 diff·내부 라벨·버전 태그) 잔존(확정 — 본문 25 파일, 주석 제외, 101 hit)

- **버전 태그가 본문 문장에 든 줄 13**: ch1_sec05_width:324–325 · ch1_sec05b_gr2L:54,179 · ch1_sec07_broadening:231,233 · ch1_sec09_tail:66 · ch1_sec10_sum:16,142,145 · ch2_sec05_mixing:196 · ch2_sec08_synthesis:55 · ch1_sec18_inputs:17 ("(v1.0.25 --- opt-in)"·"(v1.0.25 정정)"·"각주(v1.0.25)" 등).
- **프로세스·구현 어휘**: `opt-in` 8 · `round-trip` 14 · `bit-exact` 2 · `골든` 1 · `게이트 G-SI` 1 · `CODATA`(상수 opt-in 각주) 3 · `regsol` 3 · `@2/@5`(피드백 번호) 5 · `gate-6/gate-7/P5/brief/master 재조정/refine_b/self-test` — 마지막 군은 `ch1_sec05b_gr2L.tex:1–12` 헤더 주석(`%` 줄)에 있어 조판에는 안 나오나 소스에 남아 있다.
- `tier A/B/C` 표기 21건은 문건 규약(sec07:64 각주 정의)이라 register 위반이 아니라 정직성 표기 — 단 교재 register 와의 양립 여부는 Decision Queue.
- 판정: 헌법 ① "자기 diff·내부 라벨·고백조 금지" 대비 **본문 13줄 + 각주 3곳**이 직접 위반(추정 — 헌법 ①의 정의 원문은 CLOSING_v1.0.15 이며 이 서브는 brief §4.4 요약으로만 대조).

### 5.4 F-10(억지 한글화) 잔존(확정 — grep)

- "요동": ch1_sec02b_part0:409,418 — **주석 줄**(`% 자산` 태그) — 조판 본문 0. 본문은 전부 "fluctuation" 로 정정돼 있음.
- "섭동": ch1_appE_selfconsistent:163 — 표 안 "비등방 섭동(perturbation)" 병기 ○.
- "평탄역(plateau)"·"과주행(overshoot)"·"음함수(implicit function)" 첫 출현 병기 ○(sec04:15–16·sec07:20·sec02b:286).
- "되먹임"(ch2_sec08_synthesis:37·233): 영어 원어(feedback) 병기 × — 경미 1건.
- 판정: F-10 본문 잔존 0~1(되먹임).

---

## 6. CLAUDE.md P3 8항 대조(범위 내, 확정 근거 첨부)

| P3 | 현행 상태 | 근거 |
|---|---|---|
| #1 $V_n/V_\mathrm{app}$ 구분 | ○ 일관(`V_{n,drive}`·`V_{n,OCV}` 기호는 현행본에 없음 — 구트랙 명칭) | sec01:163–188·tab:notation |
| #2 전하 보존식 = 중심식 | ○ Part 0 eq:sm-mc-balance → §6 (a) → Part T eq:implicit 세 곳 동일 | sec02b:346·sec06:8·ch2_sec05:17 |
| #3 순환 의존 dependency graph/표 | **×** — 서술만(sec02b:353–357 "정의상 implicit"; appE:19–27 warnbox) · 표·그래프 형태 없음 | — |
| #4 4분류 진단 | △ "정의상 implicit formulation"(sec02b:356)·"수치 유일한 근"(sec02b:380) 2분류만 언급, "논리 공백·물리 가정 충돌" 분류는 미적용 | sec02b:353–357 |
| #5 refs 6·7 5항 sub-section | ○ appE `sec:sc-p35`(113–135) 5항 존재 — 단 ② "페이지·문단 세부는 원문 대조로 확정" 미완 명시 | appE:118–121 |
| #6 Ch1↔Ch2~5 전달 정합 | 판정 범위 밖(현행은 재료별 3장 구조 — brief §4.5) | — |
| #7 ver.N↔Chapter 명칭 | ○ 본문에 "ver." 명칭 0; stage 번호 가드(sec05b:24–25) | — |
| #8 코드 = 부록 전용 | **× 4건**(§5.2) | — |

---

## 7. 진단 결론 — 어느 Phase 에 얼마나 큰 작업이 필요한가(정량)

brief §5 골격의 작업 챕터·Phase 번호로 적는다(작업 챕터 ≠ 문건 Chapter ≠ ver.N).

| 작업 Phase | 대상 정량(범위 내 확정) | 예상 작업 규모(추정) |
|---|---|---|
| 2.1 자산 지도 | 29 파일·5558줄·display 169·boxed 41·label 264·cite 109/44·bibitem 44·박스 55(9종) | 기계 표 완성 — 본 문건 §1 이 시드. 전 문건 카운트(230/64/429/95/265·93)와 정합 확인 완료 |
| 2.2 유도 완결성(기준 1) | boxed 41 = 있음 22·부분 16·없음 1·N/A 2; 비-boxed 결과식 8건 대체 표현 | 청크 ≤500줄 기준 **12 청크**(5558/500 올림); 판정 행 41 + 8 = 49 행은 본 문건이 초안 — 검수 sub 의 적대검산 대상 |
| 2.3 가정 사다리(기준 5) | 간소화 지점 35 — 레퍼런스 × 17·유효범위 × 5·가정 미명시 2 | "일반식→특수식" 계보도 35 노드 초안 = 본 문건 §3; 최우선 3건 S10·S16·S23 |
| 2.4 서지(기준 3) | bibitem 44 전건 DOI/서지 검증(DOI 없는 9 는 단행본·내부); 인용 0 절 9/28; 1차 원전 공백 후보 15 주제 | 신규 후보 문헌 ≈ 20~25 건(추정) — Crossref 확인은 DR-6 외부 접근 결정에 의존 |
| 2.5 형식·register(기준 2·4) | 정의/정리/증명 환경 0·예제 2·연습 0·keybox 없는 절 6; F-11 4건·F-04 본문 13줄+각주 3·F-10 0~1 | 형식 요소 신설은 3.3 구조 결정(DG-A) 이후 저작 4.x 소관; F-11/F-04 제거는 국소 |
| 2.6 regsol 미결 | 본 범위에서 확인된 관련 서술: sec05b:85–92 regsol2 $\Omega_j/RT=[4.06,2.02,3.55,4.07]$·경계값 2.02 민감 지점; sec07:12–26 두-상 지목 근거 = 실측 plateau(문턱 부등식 아님); appB:20–23 커널 삭제 | 정식화 입력 3건 — 이 문건은 위치만 등록 |
| 4.x 저작(기준 1·2·5 통합) | 보강 유도 = 부분·없음 17 boxed + 비-boxed 8 = **25 사슬**; 일반→특수 사다리 신설 시 신규 boxed 는 별도 | 신규·보강 유도 총수 **≈ 25(보강) + 10~15(사다리 신설, 추정)** ; Part 0↔Part T 중복 유도 4쌍(eq:sm-logistic/eq:logistic·eq:mu/eq:Veq_BW·eq:sm-Smix/eq:Sconfig·eq:sm-thresh/eq:slope_BW) 통합 여부 DQ |

한 줄 결론: 기준 1) 은 "절반은 이미 유도되어 있고 절반은 표지만 있거나 서술형" 이라 **보강·정렬 작업(25 사슬 + 서식 균일화 7 절)**이고, 기준 5) 는 **레퍼런스 부재 17 지점의 원전 확보**가, 기준 3) 은 **핵심 열역학·동역학 절 4곳(§3·§6·§8·§9) 의 인용 0 해소와 원전급 15 주제 확보**가, 기준 2)·4) 는 **정리·정의·증명 골격 신설(현재 0)** 이 각각 지배 작업이다. 국소 정정(F-11 4건·F-04 16곳·라벨 없는 boxed 1건)은 즉시 가능하나 v1.0.25.1 동결 원칙(brief §6) 상 v2 저작 안에서만 반영한다.

---

## Decision Queue (이 서브의 이견·오류·추가 후보 — 결정은 master·사용자)

1. **boxed 판정 하한 "없음" 의 정의**: 이 서브는 (a)~(c) 중 둘 이상 부재를 "없음" 으로 뒀다(#36 eq:qrev 1건). 기준 1) 을 더 엄격히 읽어 "(c) 중간식 0 이면 없음" 으로 두면 없음 = 부분 16 중 12건이 추가로 떨어져 13건이 된다. 어느 하한을 2.2 게이트로 쓸지 결정 필요(근거: §2 표의 (c) 열).
2. **Part 0 ↔ Part T 중복 유도 4쌍**(#29·#30·ch2 eq:Veq_BW·eq:slope_BW): 자산 무유실 원칙(brief §4.4 — `\label` 체계 보존) 과 "비약 없는 단일 사슬" 이 충돌한다. v2 재구조(brief 3.3 (b) Part I 일반 이론) 에서 한쪽 라벨을 alias 로 남길지, 두 유도를 모두 유지할지 결정 대상.
3. **tier A/B/C 표기와 교재 register 의 양립**: 본문 21건의 tier 표기는 정직성 규약(sec07:64)이나 헌법 ① 의 "내부 라벨" 로도 읽힐 수 있다. v2 에서 각주·부록 원장으로 이관할지, 본문 유지할지 결정 필요.
4. **numverif2026(내부 자료) 참고문헌 등재**: 리뷰급 서지 규범상 참고문헌이 아니라 부록·각주로 이관해야 한다고 판단(근거: `ch1v22_bib.tex:44` 서지 형식 부재). 2.4 원장 설계에서 결정.
5. **P3 #3 dependency graph 부재**: sec02b:353–357·appE warnbox 의 서술을 "표" 로 인정할지, 4.x 에서 별도 그림·표를 신설할지. 이 서브 판단은 신설 필요(P3 #3 문언이 "dependency graph 또는 표").
6. **P3 #5 ② 항 미완**(appE:120–121 "페이지·문단 세부는 원문 대조로 확정"): brief §4.1 에 따르면 JCP147 PDF 와 `jcp_extract.txt` 가 소장돼 있으므로 페이지·문단 확정은 작업 챕터 2 안에서 가능하다 — DR-8 과 연동해 결정.
7. **brief §4.2 "본문 39" 와 이 범위 41 의 차이**: 이 서브의 범위(흑연 §0~§10 + Part T + §18 + 부록 E) boxed 는 41 이고 그중 부록 E 4·요약 박스 2 를 빼면 35 다. brief 의 "본문 39" 가 어느 집합(LCO §11~§17 16 포함 시 57)인지 정의가 다르므로 2.1 게이트 문구를 "boxed 64/64(전 문건)" 로 통일할 것을 제안.
8. **v1.0.25→v1.0.25.1 touch-up 건수**: 이 범위 파일 diff 는 2건(M-w·L-bg)이고 brief 의 4건 중 F1·F3 은 범위 밖 `ch3v22_sec02b_sifr` 로 추정 — master 확인 요청.
9. **범위 밖 파일 미정독 명시**: `ch2v22_notation.tex`·`ch1v22_partT_divider.tex`·`ch2_appA_traps.tex`·`ch2_appB_codemap.tex`(부록 C/D)·`appendix_phase_separation.tex`·LCO §11~§17·Si 는 배정 밖이라 읽지 않았다. §4.3 의 "Cahn–Hilliard 원전이 상분리 부록에 있을 가능성" 등 이들에 의존하는 판정은 미검증이다.
10. **추가 후보(실제 수정 아님)**: (i) boxed #19 에 `\label` 부여, (ii) §3·§6·§8·§9 에 원전 인용 최소 1건씩, (iii) Part T §2.1~2.3·2.5·2.7 과 §7 에 (a)~(d) 표지 적용, (iv) 예제를 절당 1건 수준으로 확장(현재 2), (v) F-11 4건·F-04 버전 태그 13줄 제거 — 전부 v2 저작 4.x 에서.

---

## Read Coverage (파일·행 범위 전건 — head→tail 전문)

| 파일 | 행 범위 | 비고 |
|---|---|---|
| `Claude/results/handoffs/2026-09-02-v2-master-plan/brief.md` | 1–219 | 전문 |
| `Claude/docs/v1.0.25.1/_sections/ch1_sec00_intro.tex` | 1–95 | 전문 |
| `…/ch1_sec01_n0n1.tex` | 1–245 | 전문 |
| `…/ch1_sec02a_part0.tex` | 1–391 | 전문 |
| `…/ch1_sec02b_part0.tex` | 1–475 | 전문 |
| `…/ch1_sec03_center.tex` | 1–122 | 전문 |
| `…/ch1_sec04_hys.tex` | 1–337 | 전문 |
| `…/ch1_sec05_width.tex` | 1–425 | 전문 (+ v1.0.25 동명 파일과 `diff -u`, 차이 303–304) |
| `…/ch1_sec05b_gr2L.tex` | 1–239 | 전문 |
| `…/ch1_sec06_eqpeak.tex` | 1–132 | 전문 (+ v1.0.25 동명 파일과 `diff -u`, 차이 107–108) |
| `…/ch1_sec07_broadening.tex` | 1–376 | 전문 |
| `…/ch1_sec08_lag.tex` | 1–149 | 전문 |
| `…/ch1_sec09_tail.tex` | 1–254 | 전문 |
| `…/ch1_sec10_sum.tex` | 1–188 | 전문 |
| `…/ch2_sec00_intro.tex` | 1–72 | 전문 |
| `…/ch2_sec01_partition.tex` | 1–150 | 전문 |
| `…/ch2_sec02_config.tex` | 1–191 | 전문 |
| `…/ch2_sec03_vibel.tex` | 1–119 | 전문 |
| `…/ch2_sec04_einstein.tex` | 1–208 | 전문 |
| `…/ch2_sec05_mixing.tex` | 1–256 | 전문 |
| `…/ch2_sec06_limits.tex` | 1–54 | 전문 |
| `…/ch2_sec07_revheat.tex` | 1–103 | 전문 |
| `…/ch2_sec08_synthesis.tex` | 1–239 | 전문 |
| `…/ch2_sec09_method.tex` | 1–65 | 전문 |
| `…/ch2_sec10_closing.tex` | 1–30 | 전문 |
| `…/ch1_sec18_inputs.tex` | 1–93 | 전문 |
| `…/ch1_appA_signcheck.tex` | 1–90 | 전문 |
| `…/ch1_appB_codemap.tex` | 1–185 | 전문 |
| `…/ch1_appE_selfconsistent.tex` | 1–218 | 전문 |
| `…/ch1v22_bib.tex` | 1–57 | 전문 |
| `Claude/docs/v1.0.25/_sections/ch1_sec05_width.tex`·`ch1_sec06_eqpeak.tex` | diff 만 | 전문 정독 아님(diff 출력으로 차이 2건 확인) |
| `…/ch1_preamble.tex`·`ch2_preamble.tex` | grep 만(31–36·31–35) | 박스 환경 정의 확인 목적 부분 |
| `…/_sections/*.tex`(LCO·Si·notation·divider·ch2 부록)·`appendix_phase_separation.tex` | 카운트 grep 만 | 미정독 — boxed 64 교차검증 목적 |

기계 추출 스크립트: `C:\Users\lksz1\AppData\Local\Temp\claude\D--Projects-Project-Anode-Fit\1ebfda83-368e-48d5-8020-2555f36fa668\scratchpad\count_assets.py`(휘발 스크래치). `Codex/` 는 접근하지 않았다. 기존 파일 수정·git 명령 없음.
