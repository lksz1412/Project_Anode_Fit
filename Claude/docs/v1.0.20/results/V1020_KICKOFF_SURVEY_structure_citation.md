# V1020 킥오프 조사 ① — v1.0.19 절 구성·인용 전수 실태 (기획 세션 sub-agent 조사, 2026-07-16)

> 목적: v1.0.20 마스터플랜의 Current Ground Truth + P1(서지 원장) baseline. 대화 소실 대비 디스크 보존본.
> 조사 대상 = `docs/v1.0.19/` 전 tex. 아래 수치는 2026-07-16 조사 시점 스냅샷 — P1 gate 에서 재확정.

## 1. 구조 인벤토리

### 조립
- Ch1 마스터(43줄): preamble + 24 `\input`(sec00~sec18, appA/appB, bib).
- Ch2 마스터(37줄): preamble + 14 `\input`(sec00~sec10, appA/appB, bib).

### Ch1 절 파일 (파일 | 행수 | 절/소절)
| 파일 | 행수 | 구성 |
|---|---|---|
| ch1_sec00_intro | 91 | §* 서론 |
| ch1_sec01_n0n1 | 205 | § 기호·규약·매핑·분극(N0,N1) — 소절: 매핑(9)·기호 마스터표(36, tab:notation L42–88)·분극(158)·점별 원칙(185) |
| ch1_sec02a_part0 | 268 | § 통계역학 기초 Part 0 — 앙상블(20)·단일 자리(106)·lattice gas(220) |
| ch1_sec02b_part0 | 329 | (★`\section` 없음 — §2 연속) 평균장(5)·전기화학 연결(139)·거시 열역학·Nernst(280) |
| ch1_sec03_center | 74 | § U_j(T)(N2) |
| ch1_sec04_hys | 196 | § 히스테리시스(N3) — spinodal(11)·gap 닫힌꼴(58)·분기 중심(111) |
| ch1_sec05_width | 299 | § ξ_eq·폭(N5,N4) — logistic(11)·폭(150)·분포 관점(264) |
| ch1_sec06_eqpeak | 43 | § 평형 peak(N6) |
| ch1_sec07_broadening | 305 | § 두-상 broadening(N6 확장) — 출발(12)·세 출처(34)·범위(179) |
| ch1_sec08_lag | 128 | § L_V(N7) |
| ch1_sec09_tail | 244 | § 인과 기억 꼬리·반전(N8) |
| ch1_sec10_sum | 61 | § 합산·staging 초기값(N9) |
| ch1_sec11_lcointro | 172 | § Part II 도입(N0′) |
| ch1_sec12_lcocenter | 112 | § LCO 중심·∂U/∂T(N2′) |
| ch1_sec13_lcohys | 169 | § LCO order–disorder·MIT 2상역(N3′) |
| ch1_sec14_lcodecomp | 100 | § 반응 엔트로피 삼분해(N9′) |
| ch1_sec15_lcoelec | 249 | § LCO 전자 엔트로피(N5+) — MIT 물리(12)·FD→Sommerfeld(22)·단위·부호(90)·MIT-logistic 게이트(146)·크기 검산(195) |
| ch1_sec16_lcopeak | 67 | § LCO peak 3종 |
| ch1_sec17_msmr | 133 | § MSMR 동형·plug-in |
| ch1_sec18_inputs | 68 | § 전체 입력·피팅 준비 |
| ch1_appA_signcheck | 89 | § 부호 검산표(번호 붙음, longtable 2) |
| ch1_appB_codemap | 157 | § 구현 대응표(번호 붙음, longtable 3 — tab:symcode) |

### Ch2 절 파일
| 파일 | 행수 | 구성 |
|---|---|---|
| ch2_sec00_intro | 68 | §* 서 |
| ch2_sec01_partition | 144 | § 분배함수→점유 분포 — 단일 자리 Ξ₁(16)·전기화학·Ch1 logistic 기원(51)·Bragg–Williams(103) |
| ch2_sec02_config | 188 | § S_config — 부분몰(11)·∂V/∂T(34)·이중계산 금지(108)·문헌 검증(132) |
| ch2_sec03_vibel | 95 | § vib(포논 BE, 11)·electronic(FD·Sommerfeld, 37)·세 분포 총괄(73) |
| ch2_sec04_einstein | 115 | § Einstein 보정 |
| ch2_sec05_mixing | 240 | § 섞임·겹침 — 파생 A(12·67)·B(143)·C(158)·D(193) |
| ch2_sec06_limits | 52 | § 극한·코너 |
| ch2_sec07_revheat | 58 | § 가역 발열(Bernardi) |
| ch2_sec08_synthesis | 144 | § 종합식·계산 예제 |
| ch2_sec09_method | 43 | § 방법론·정직한 한계 |
| ch2_sec10_closing | 25 | §* 맺음 |
| ch2_appA_traps | 74 | §* 부록 A 함정표(무번호) |
| ch2_appB_codemap | 69 | §* 부록 B 코드 요구명세(무번호) |

### 구조 특이점 (v1.0.20 유의)
- ch1_sec02b 는 `\section` 없이 §2 를 잇는다(§2 = 두 파일 스팬).
- **부록 번호 방식 챕터 간 불일치**: Ch1 부록 = 번호 `\section`, Ch2 부록 = `\section*`(무번호). (P6 컨벤션 통일 후보 — 단 라벨·참조 영향 검토 후.)
- 무번호 `\section*`: ch1_sec00, ch2_sec00, ch2_sec10, ch2_appA, ch2_appB.

## 2. 인용 실태 (핵심 수치)

- **Ch1**: `\cite` 명령 41회 / `ch1_bib.tex` 정의 **28건**(★헤더 주석 "24종"은 실제 28 과 불일치 — stale count). 전 항목 DOI 병기(단행본 4권 제외: hill1960·fowler1939·mcquarrie1976·mckinnon1983·(+newman/huggins 는 Ch2)).
- **Ch2**: `\cite` 27회 / `ch2_bib.tex` 정의 **14건**(헤더와 일치; numverif2026 = 내부 검증 노트, DOI 없음).
- **(i) 인용됐으나 미정의 키 = 0 / (ii) 정의됐으나 미인용 항목 = 0** (양 챕터 clean). ※ch2 bazant2013 은 여러 줄 `\cite{huggins2009, bazant2013}`(ch2_sec01:105–106) 한 곳뿐 — reflow 시 유실 주의.
- **영인용(0-cite) 절**: Ch1 8(sec01, sec02b, sec03, sec06, sec08, sec09, sec16, sec18) + Ch2 3(sec00, sec06, sec10) + 부록 2(ch1_appB, ch2_appA).
- **챕터 간 서지 키 함정**: ①MSMR 계열 — ch1 `msmr2024`(Paul, ECS Adv. Part I) vs ch2 `msmr_partI`(Garrick)+`msmr_partII`(Paul) 별도 키(ch2_bib:14 에 정체 함정 명시 있음) ②`bazant2013`·`reynier2003` 양 bib 중복 정의(분리 컴파일 하 무해, 병합 시 충돌) ③ch1_bib 헤더 수 불일치(24→28).

### 주요 서지(요지) — P1 온라인 전수 검증 대상 42건 중 대표
dahn1991(PRB 44,9170)·ohzuku1993(JES 140,2490)·bazant2013(Acc.Chem.Res 46,1144)·eyring1935(JCP 3,107)·hill1960(서적)·mckinnon1983(서적 chapter)·dreyer2010(Nat.Mater 9,448)·reimers1992(JES 139,2091)·menetrier1999(J.Mater.Chem 9,1135)·motohashi2009(PRB 80,165114)·xia2007(JES 154,A337)·reynier2004(PRB 70,174304 — LCO 엔트로피)·reynier2003(JPS 119–121,850 — 흑연)·swiderska2019(PCCP 21,2115)·msmr2024(ECS Adv 3,042501)·ml2024(JMPS 190,105727)·leviaurbach1999(Electrochim.Acta 45,167)·rsc2021(JMCA 9,11187)·fly2020(J.Energy Storage 29,101329)·dahn1995(Science 270,590)·park2021(Materials 14,4683)·persson2010(JPCL 1,1176)·persson2010b(PRB 82,125416)·cogswell2012(ACS Nano 6,2215)·bloom2005(JPS 139,295)·dubarry2012(JPS 219,204) / Ch2: bernardi1985(JES 132,5)·newman(서적)·huggins2009(서적)·allart2018(JES 165,A380)·occupation2019(Electrochim.Acta 324,134774)·chemmater2015(Chem.Mater 27,2566)·jpcc2021(JPCC 125,27891)·msmr_partI(JES 171(2))·msmr_partII(JES 171(10))·standardised2024(JES 171,050535)·hysteresis2018(JPS 395).

## 3. 무인용 문헌성 주장 (±3행 내 \cite 부재 — F-6 해소 대상 baseline)

| 위치 | 요지 | 비고 |
|---|---|---|
| ch1_sec16_lcopeak:56 | "pure-LCO 문헌 물리에서 세 peak" | ★파일 인용 0 |
| ch1_sec16_lcopeak:63 | "∂U_1/∂T 의 T 선형 증가가 전자항의 관측 신호" | ★파일 인용 0 |
| ch1_sec13_lcohys:32 | "문헌 물리에서 T1·T2·T3 전부 같은 문턱" | 최근접 cite L122 |
| ch1_sec13_lcohys:153 | "pure-LCO 문헌 물리 Ω 를 도핑 피팅값과" | 〃 |
| ch1_sec01_n0n1:91 | "staging 초기값(문헌 기반, tab:staging)" | 파일 인용 0(값 출처는 §10) |
| ch1_sec07_broadening:25 | "실측 plateau·staging 문헌의 상평형" | 근접 cite 밖 |
| ch1_sec10_sum:28 | "(tier C — 문헌 간 5–15 mV 편차 통상)" | 편차 주장 자체 무근거 |
| ch1_sec04_hys:125 | "방전>충전 전위 관측 일치" | dreyer2010 은 절 서두(118행 위) |
| ch2_sec05_mixing:168–169 | "실측 plateau·staging 문헌 상평형 / 문헌 상평형은…" | 근접 cite 밖 |
| ch2_sec02_config:9 | "문헌 흑연 측정과의 정합으로 닫는다"(서두 예고) | 실제 검증부(L135–138)는 인용 有 |
| ch2_sec02_config:142 | "문헌 프로파일과 부호·규모 정합" | cite 가 4행 위(경계) |

※ "1차 문헌 공백(G1–G3)" 선언(ch1_sec14:85–86, sec15:9·75–76·147, sec07:204, sec10:50·52)은 의도적 공백 정직 노출 — 무인용 결함 아님(유지).
※ 한국어 활용형 스캔 한계: P1 에서 어간 확장(보고|관측|측정|알려|제안|실험적|최근) 재스캔 필요. ch2_sec02:135·138 의 "보고한다/보고된다"는 인용 있음(clean).

## 4. 표기 스냅샷 (F-1·F-2·F-5 대상 좌표)

- **기호 마스터표** = ch1_sec01 L42–88 `tab:notation`(N0/N2·4·5/N3/N7·8/상수 그룹). 기호→코드 표 = ch1_appB `tab:symcode`. Ch2 는 마스터표 없음(Ch1 재사용 + appA 함정표).
- **q(T) 등장 좌표**: ch1_sec02a 126–218(유도 본거지·각주 133 = 용량 좌표 q 와 구분)·ch1_sec05:271·ch2_sec01:41–46. → D7(정통 유도 선행) 1차 대상.
- **Fermi–Dirac 계열**: ch1_sec02a:181(동형 가드)·sec05:287·294·**sec15(8–191, 최밀집 — 전자 엔트로피 유도)**·ch2_sec00:23·35·sec01:34·36·sec02:101·**sec03:7–76**·sec06:26·sec10:10.
- **보손/Bose–Einstein**: ch1_sec02a:211·ch2_sec00:34·**sec03:7–76(보손 명시 13·15)**·sec10:9.
- **페르미온(한글) 단 1회**: ch2_sec01:36("페르미온 전자가 아니라"). → F-1 배경 다리의 접속점 = ch1_sec02a(동형 가드 주변) + ch2_sec03 도입 + ch1_sec15 도입.
- Sommerfeld: ch1_sec15:32–72·ch2_sec03:46·57·sec06:26·appA:66·sec10:10.
