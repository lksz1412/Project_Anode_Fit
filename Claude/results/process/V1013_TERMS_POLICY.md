# v1.0.13 용어·약자 전수 감사 (P1.1 S2)

- 대상: `Claude/docs/v1.0.13/graphite_ica_ch1_v1.0.13.tex`(2230줄, 전문 정독)·`graphite_ica_ch2_v1.0.13.tex`(778줄, 전문 정독). head→tail 전 영역 커버.
- 성격: **표만 산출 — 대상 .tex 파일 수정 없음**(0 byte 변경).
- 출현 수는 Grep 라인-매치 기준(한 줄에 동일어 2회 이상 출현 시에도 그 줄은 1로 카운트) — 상대적 빈도 비교용 근사치이며 절대 정밀 어절 카운트가 아님. 정밀 카운트가 필요한 항목은 표에 "실측 n건"으로 별도 표기.
- 정책 원칙(작업지시 원문): 서술 베이스 한글 유지 + 물리·화학·수학 전문 명사는 영어 원어로 치환. 이미 굳은 일상어/조어는 유지 가능(근거 명시). 이미 영어 원어인 것은 유지.

---

## ① 용어표

| # | 현행 | 정정(원어) | 근거/판단 | 출현 수(ch1 / ch2) | 대표 위치(줄) | 처분 |
|---|------|-----------|-----------|---------------------|----------------|------|
| 1 | 절연체→금속 천이(MIT) | insulator-to-metal transition (MIT) | 이미 "(MIT)" 약자 병기되어 있으나 **영어 전체 표기가 문서 어디에도 없음** — 한국어 구+약자만 있고 "insulator-to-metal transition"이라는 영문 완전형이 등장하지 않음. MIT 관련 서술이 문서의 핵심 신규 물리(§lco-electronic 전체)라 정밀 English form 병기가 필요. | 13 / 0 | ch1:319(최초), 1145,1157,1203,1205,1214,1215,1282,1313,1314,1322,1339,1369 | **병기 보강** — 최초 출현(319)에 "절연체→금속 천이(insulator-to-metal transition, MIT)"로 확장 |
| 2 | 전이(轉移) — 일반 상전이/staging transition 의미 | transition | 이미 정착된 한국어 학술 표준어(상전이·전이금속·전이상태 등과 동계, 전지 문헌에서 보편적). 전 문서 핵심 반복어(149+61=210줄). 전량 영어 치환 시 오히려 가독성 저해. | 149줄 / 61줄 | 전역 | **유지**(치환 불요) — 이미 굳은 일상 학술어로 판단 |
| 3 | 천이(遷移) — MIT 국소 맥락 전용 | transition (MIT context) | **#1·#2와 동일 개념(transition)을 다른 한자어(천이 vs 전이)로 이원 표기** — 같은 문서 안에서 일반 상전이는 "전이", MIT만 "천이"로 갈림. 독자가 두 단어를 별개 개념으로 오인할 위험. | 13(#1과 동일 라인) | 319 | **병기+안내** — "천이"를 "전이"로 통일하거나, 최초 등장 시 각주로 "본 문건은 일반 상전이=전이, MIT 문맥=천이로 표기(동의어)" 명시 |
| 4 | 상분리 | phase separation | 정착 표준 한국어 물리 용어(상분리=phase separation, 한국 응집물질/전기화학 문헌 보편). | 8줄 / 11줄 | ch1:241(최초), ch2:200(최초) | **유지**, 최초 출현 1회 "(phase separation)" 병기 권고(선택) |
| 5 | 정규용액(상호작용) | regular solution | Hildebrand의 명명 모델("regular solution model")을 직역한 용어 — 특정 이론의 고유명사에 가까움. 영어 원어가 전혀 병기되지 않음(ch2 bibitem 764와 본문 199에서만 "regular-solution 형"으로 부분 노출). | 11줄 / 2줄(199 "regular-solution 형", 764 bibitem) | ch1:241(최초), 588 | **병기 필요** — 최초 출현(241 또는 588)에 "정규용액(regular solution)" 추가 |
| 6 | 격자기체 | lattice gas | ch2는 최초 정의 시 이미 "격자기체(lattice gas)"로 병기(ch2:114) — 모범 사례. 그러나 **ch1은 10회 전부 미병기**(583부터). 두 챕터가 독립적으로 읽힐 가능성이 있어(서론 각각 있음, 서로 참조하되 완결형 지향) ch1 단독 열람 시 영어형이 전혀 노출되지 않음. | 10줄 / 8줄(병기됨) | ch1:583(최초, 미병기), ch2:114(최초, 병기됨) | **병기 필요(ch1만)** — ch1 최초 출현(583 또는 587)에 "격자기체(lattice gas)" 추가 |
| 7 | 이중웰 | double-well | 영어형 "double-well"은 tikz **LaTeX 주석(%, 렌더링 시 비가시)** 에만 존재(line 54 버전이력, line 625 tikz 주석) — 실제 렌더링된 본문에는 한국어 "이중웰"만 노출되고 영어 대응어가 독자에게 전혀 보이지 않음. | 4 (584,604,849,860) | 0 | ch1:584(최초) | **병기 필요** — "이중웰(double-well)"로 최초 출현에 추가 |
| 8 | 배리어 | barrier | 같은 개념을 문서 내 이미 "장벽"(11회 이상, 활성화 장벽·유효 장벽 등 표준 번역어)으로 압도적으로 쓰면서, **국소적으로 2곳(1551, 1597)만 음차 "배리어"로 이탈** — 내부 비일관. | 2(1551,1597) 배리어 / 11+ 장벽 | — | ch1:1551 | **치환**(통일) — "배리어"→"장벽"으로 통일(문서 지배적 어휘와 정합) |
| 9 | 배치(configurational) → 이후 "config" 원어 혼용 | configurational (config) | ch1 §sec:center(444~648)는 "배치" 번역어 사용(1회는 "배치(configurational)" 명시 병기, line 1143). 그러나 §sec:lco-electronic 이후(1152~)부터는 번역 없이 영어 "config"를 그대로 국문 문장에 삽입(예: "config 몫", "config·vib", 절 제목조차 "config + vib + electronic", line 1970) — **같은 문서 내 번역어→원어 전환이 예고 없이 일어남**. | 배치 6회(444,449,484,495,648,+1143 "배치(config...)") / config(원어 그대로) 25회 이상(1152부터) | ch1:444(배치 최초), 1152(config 원어 전환 시작) | **표기 통일 권고** — ①"배치"를 초반부터 없애고 처음부터 "config"로 통일하거나 ②1152 이후에도 "config(배치)" 최소 1회 재확인 삽입 |
| 10 | 격자(格子) — "작업 격자"(수치 계산 grid) 와 "격자기체"(결정 lattice)에 동일어 사용 | grid (작업 격자) vs lattice (격자기체) | **다의어 충돌**: 같은 한자어 "격자"가 문서 안에서 물리적 결정 격자(lattice, 격자기체 맥락)와 수치 계산 격자(grid, $V_\mathrm{work}$ 맥락)를 모두 가리킴. 두 개념은 물리적으로 전혀 다른 대상(원자 배열 vs 수치 이산화)이라 혼동 위험. | "작업 격자" 6줄(386,387,398,990,1929,1940,2218,2235 등) / "격자기체" 10줄 | ch1:386("작업 격자" 최초) | **병기 필요** — "작업 격자(grid)" 최초 출현(386)에 "(grid)" 추가해 "격자기체(lattice)"와 명시적으로 구분 |
| 11 | 평탄역 | plateau | 같은 개념(전위 평탄부)을 "평탄역"(4회, 한국어 번역)과 "plateau"(22회, 영어 원어)로 이원 표기. 영어형이 압도적으로 우세하나 한국어형도 국소적으로 잔존해 두 단어가 같은 것인지 확인이 필요한 수준. | 4 (1506,1521,1542,1544) 평탄역 / plateau 별도 다수(≈22) | — | ch1:1506(평탄역 최초) | **병기 또는 통일** — "평탄역(plateau)" 1회 병기, 이후 "plateau" 원어로 통일 권고(문서 지배 어휘와 정합) |
| 12 | 코너 | corner case / edge case | ch2 전용어. "corner"의 한국어 음차이나, **물리적 "모서리"가 아니라 소프트웨어·공학 용법의 "corner case"(경계/예외 상황)의 뜻으로 전용** — 절 제목("극한과 코너", line 623)에까지 쓰여 비중이 크다. 물리학 독자에게는 생소한 전용 의미라 원어 병기 없이는 오독 소지(예: "코너"를 물리적 모서리로 오해). | 0 / 8(비주석: 96,216,421,623,625,631,647,756) | — | ch2:96(본문 최초), 623(절 제목) | **병기 필요(최우선급)** — "코너(corner case)" 또는 "코너(edge case)"로 절 제목·최초 본문 출현 양쪽에 추가 |
| 13 | 과전압 | overpotential / overvoltage | 정착 표준 전기화학 용어(교과서 수준). | 26 / 7(과전압·히스테리시스 합산 count 중 과전압 몫) | — | **유지** |
| 14 | 히스테리시스 | hysteresis | 음차 정착 표준어. | 7줄 | ch1:149(최초) | **유지** |
| 15 | 히스 (히스테리시스의 비공식 축약) | hys. (informal abbreviation of hysteresis) | "히스 gap", "히스 분기" 등 본문 곳곳에서 "히스테리시스"를 비공식적으로 "히스"로 줄여 쓰나, **최초 축약 시점에 "이하 히스로 축약"류의 명시 선언이 없음**(문맥상 이해는 가능). 코드 기호 \hys 매크로와도 연동. | 6+ (예: "히스 gap", "히스 분기" 등 산재) | ch1:581 부근(문맥상 최초 축약 인상) | **병기/안내 권고(낮은 우선순위)** — 최초 축약 지점에 "(이하 '히스'로 축약)" 각주 |
| 16 | 겉보기 전위/중심 | apparent potential / apparent center (symbol: apparent-U, $U_\mathrm{app}$) | 한국어 번역("겉보기")과 영어 조어("apparent-U")가 병존하나 첨자 $U_\app$로 양쪽이 명확히 연결되어 실질적 혼동은 낮음. | 5줄(1547,1560,1576,1608,1625 등) | ch1:1547 | **유지**, 선택적 "겉보기(apparent)" 1회 병기 |
| 17 | 초격자 | superlattice | 1회 출현("charge-order 초격자", line 1997). 표준 고체물리 번역어. | 1 | ch1:1997 | **유지**, 선택 병기 |
| 18 | pairing (영어 원어 그대로 국문 문장에 삽입) | pairing (짝짓기) | line 2109 "짝짓는(...) pairing"처럼 한국어 서술어 뒤에 영어 명사가 무번역 삽입 — 스타일상 하이브리드지만 국소 1회뿐. | 1 | ch1:2109 | **병기 권고(낮은 우선순위)** — "짝짓기(pairing)"로 순서 통일 |
| 19 | 무질서 | disorder | 표준 번역어("turbostratic 무질서"처럼 영어 형용사+한국어 명사 결합으로 이미 실질적 병기 효과 있음). | 다수 | — | **유지** |
| 20 | 다중도 ($n_j$) | multiplicity | 표준 번역어. | 다수 | ch1:235(표),925 | **유지** |
| 21 | Maxwell 공통접선 | (Maxwell) common tangent | 영어 고유명사(Maxwell)+한국어 번역(공통접선) 혼합, 열역학 표준 작도법 명칭. | 3(1504,1539 부근) | ch1:1504 | **유지**, 선택 병기 "(common tangent)" |
| 22 | 축퇴 (전자기체) | degenerate / degeneracy | 표준 고체물리 번역어(축퇴 전자기체 = degenerate electron gas). | 2(1171,1202) | ch1:1171 | **유지** |
| 23 | 되먹임 | feedback | 표준 번역어, 1회. | 1(2170 부근) | ch1:2170 | **유지** |
| 24 | 인과 기억 꼬리 / 인과 저역통과 | causal memory tail / causal low-pass | 표준 번역, 코드 식별자 \code{\_causal\_lowpass}와 정합. | 다수(§sec:tail 전역) | ch1:1782(절 제목) | **유지**, 선택 "(causal)" 1회 병기 |
| 25 | 배경(미분용량) | background (differential capacity, $C_\bg$) | 표준어. | 다수 | — | **유지** |
| 26 | 활성화 장벽 / 유효 장벽 | activation barrier / effective barrier | 표준 번역, 코드 대응 명확($\Delta H_a$, $\Delta H_a^\eff$). | 다수 | ch1:954 | **유지** |
| 27 | 반응 엔트로피 vs 활성화 엔트로피 | reaction entropy vs activation entropy | ch2 §sec:vibel 말미에서 이미 명시적으로 구분 서술("혼동 금지" warnbox, line 436-440) — 모범 사례. | — | ch2:436 | **유지**(이미 잘 처리됨, 추가조치 불요) |

---

## ② 약자표

| # | 약자 | 원어(완전형) | 첫 출현(파일:줄) | 현행 병기 여부 | 병기 문안 제안 |
|---|------|-------------|-------------------|-----------------|-----------------|
| 1 | ICA | incremental capacity analysis | ch1:133 | **예(완비)** — "incremental capacity analysis(ICA)" | 수정 불요(모범 사례) |
| 2 | MIT | insulator-to-metal transition | ch1:319 | **부분** — 한국어 구("절연체→금속 천이")+약자만, 영문 완전형 없음 | "절연체→금속 천이(insulator-to-metal transition, MIT)" |
| 3 | OD | order–disorder | ch1:759(수식 첨자 $\mathrm{OD}_a$ 로 최초 노출) | **간접** — 인접 문맥(표·본문)에 "order--disorder" 완전형이 반복되나, "OD"라는 약자 자체를 1:1로 정의하는 문장은 없음 | 수식 첨자 인근 본문(756-759)에 "order–disorder(OD)" 1회 명시 |
| 4 | MSMR | multi-species, multi-reaction | ch1: 코드 식별자 \code{LCO\_MSMR\_LIT} 최초 노출은 317-318(치환금지 구역이나 독자에게는 "MSMR" 문자열의 최초 시각 노출); 산문 정의는 ch1:2065-2066 — **약 1750줄(전체의 ~78%) 격차**. ch2:735 "MSMR (Multi-Species, Multi-Reaction) 절차" — 즉시 병기, 문제없음 | ch1: **지연됨**(정의 전 코드ID로 선노출) / ch2: **양호** | ch1의 표~ref{tab:lco-staging} 도입부(317 부근)에 각주 "MSMR = multi-species, multi-reaction 모델(상세 §lco-code)" 조기 예고 권고 |
| 5 | GITT | galvanostatic intermittent titration technique | ch1:1535 | **없음(0)** — 4회+bibitem 전부 약자만, 완전형 전무 | "GITT(galvanostatic intermittent titration technique)"를 1535에 추가 |
| 6 | OCV | open circuit voltage | ch1:254(표) / ch2:594 | **없음(0)** | "개회로전압(open circuit voltage, OCV)" |
| 7 | OCP | open circuit potential | ch1:1536 | **없음(0)** — OCV와 구분 설명도 없음(전셀 전압 vs 반쪽전지 전위 뉘앙스 차이 가능성이 있으나 미설명) | "개회로전위(open circuit potential, OCP; 본 문건의 OCV와 구분 — 반쪽전지 전위)" |
| 8 | SOC | state of charge | ch1:558 / ch2:78 | **없음(0)** | "충전상태(state of charge, SOC)" |
| 9 | DFT | density functional theory | ch1:1968 | **없음(0)** | "밀도범함수이론(density functional theory, DFT)" |
| 10 | **FD** | **(a) Fermi–Dirac** / **(b) finite difference(유한차분)** | (a) 개념은 전 구간 "Fermi--Dirac" 완전표기로만 사용(약자 미사용); "FD" 약자 자체의 첫 노출은 (b) 의미로 ch2:499(위첨자 $^\mathrm{FD}$) | **충돌 — 최우선 플래그.** ch2 한 챕터 안에서 "FD"가 서로 다른 두 개념(Fermi–Dirac 함수 / 유한차분 finite difference)을 가리킴: 표(642 "FD Sommerfeld")·맺음(752 "(FD Sommerfeld)")은 Fermi–Dirac 의미, srcbox(499,502,548)는 유한차분 의미. 앞 절들에서 "Fermi--Dirac"이 완전표기로 압도적으로 반복돼 독자가 "FD"를 Fermi–Dirac으로 선입견할 위험이 있는 채로, 정작 문서에 드러나는 "FD" 약자 자체는 유한차분 쪽에 더 많이 등장 | **권고**: 유한차분 쪽 기호를 "FD"→"FDiff" 또는 "num"으로 개명하거나, ch2:499 인근에 "(이하 FD = 유한차분(finite difference); Fermi–Dirac 의 약자가 아님)" 명시 각주 추가 |
| 11 | BW | Bragg–Williams | 가시 본문에는 약자 미노출(전부 "Bragg--Williams" 완전표기: ch2:190,192,197,199,230,231). "BW" 문자열은 \label/주석에만 존재(치환금지 구역) | **해당없음(모범 사례)** — 완전표기만 일관 사용 | 수정 불요 |
| 12 | KWW | Kohlrausch–Williams–Watts | ch1:51(버전이력 % 주석 — 치환금지 구역) | **해당없음** — 본문(비주석)에는 전혀 등장하지 않음 | 조치 불요(본문 미사용 확인) |
| 13 | AIC | Akaike Information Criterion(추정) | — | **근거미발견** — ch1·ch2 어디에도 "AIC" 문자열 없음 | 해당사항 없음(v1.0.13 두 챕터 범위 밖 — 다른 버전/문서 유물 가능성) |
| 14 | PSD | particle size distribution | ch1:1592(본문), 주석 22 | **부분** — "입자 크기 분포(PSD)"로 한국어 구+약자 병기(영문 완전형 없음, MIT와 동일 패턴) | 선택: "입자 크기 분포(particle size distribution, PSD)" |
| 15 | P4 | (미상 — 추정: 내부 로드맵 "Phase 4") | ch1:1246 | **없음(0)** — 정의·설명이 전혀 없는 내부 참조 | 1246 인근에 "P4 = (내부 로드맵) Phase 4 코드 구현 단계" 각주 또는 상위 문서 교차참조 추가 |
| 16 | G1 / G2 / G4 | (미상 — 추정: 문헌 공백/갭 추적 코드) | ch1:1212(G2 최초) | **없음(0)** — "갭 G2", "갭 G1·G2·G4"처럼 코드만 반복 사용, 정의된 목록/범례 없음 | 1212 인근에 "(갭 목록 출처: [내부 추적 문서명])" 각주 또는 본문 내 갭 목록 요약표 신설 |
| 17 | H-1, H-2, M-1~M-11 | (Fable 감사 이슈 코드, 추정) | ch1:3-4(버전이력 % 주석) | **해당없음** — 치환금지 구역(주석) 전용, 본문 미사용 | 조치 불요 |
| 18 | tier A / B / C | (신뢰도 등급: A=1차 문헌·확정값, B=대표/부분 스케일, C=추정·placeholder — 문서 내 정성 서술로 추론됨) | ch1:최초 등장 1209 부근(§lco-Se) | **없음(통합 범례 없음)** — 개별 사례마다 정성적 근거는 붙으나("tier A 이다" 식), tier A/B/C 등급 기준 자체를 정의하는 legend가 문서 어디에도 없음. 21회 반복 사용(ch1 전용, ch2는 0회). | §lco-Se 도입부 또는 §lco-gate 최초 사용 지점에 1회 범례 표 삽입: "tier A(1차 문헌 정량 확정) · tier B(대표/부분 스케일 anchor) · tier C(추정·placeholder, round-trip 피팅으로 갱신 예정)" |

---

## ③ 치환 금지 구역 목록

정정 작업(향후 실제 편집 시) 시 아래 구역의 문자열은 **원문 그대로 보존**해야 하며, 위 ①·②의 어떤 치환/병기 권고도 이 구역 안에서는 적용하지 않는다.

1. **수식 내부 전체** — `$...$`, `\[...\]`, `equation`/`align`/`boxed` 환경 안의 모든 기호·아래첨자·위첨자(예: `$\Omega_j$`, `$U_j(T)$`, `$z_\mathrm{cut}$`, `\mathrm{config}`, `\mathrm{vib}`, `\mathrm{cat}`, `\mathrm{MSMR}`, `\mathrm{elec}` 등). 두 파일 전 구간 해당.
2. **코드 식별자 `\code{...}`** — 예: `\code{GRAPHITE_STAGING_LIT}`, `\code{LCO_MSMR_LIT}`, `\code{func_U_j}`, `\code{func_w}`, `\code{func_ksi_eq}`, `\code{func_dU_hys}`, `\code{func_U_branch}`, `\code{func_chi_d}`, `\code{func_dH_a_eff}`, `\code{func_L_q}`, `\code{_causal_lowpass}`, `\code{_width}`, `\code{_n_factor}`, `\code{dqdv}`, `\code{curve}`, `\code{Anode_Fit_v1.0.13.py}`, `\code{V_n = V_in - sigma_d * I_abs * self.Rn}` 등 — Ch1·Ch2 전 구간의 모든 `\code{}` 매크로.
3. **`\bibitem{...}` 전체** — 저자명·논문 제목·저널명·DOI 문자열. 예: `bloom2005, dubarry2012, dahn1991, ohzuku1993, xia2007, reynier2004, motohashi2009, menetrier1999, reimers1992, dreyer2010, dahn1995, fly2020, leviaurbach1999, eyring1935, bazant2013, park2021, rsc2021, msmr2024, cogswell2012, ml2024`(ch1) / `bernardi1985, newman, huggins2009, bazant2013, reynier2003, allart2018, occupation2019, chemmater2015, jpcc2021, msmr_partI, msmr_partII, standardised2024, hysteresis2018, numverif2026`(ch2). 영문 원문 그대로 보존.
4. **주석(`%`로 시작하는 라인) 전체** — ch1 라인 1-57(버전이력·계보 블록), ch2 라인 1-17(버전이력 블록), 및 tikz 환경 내부의 개별 `%` 주석(예: ch1:288-297 근방의 좌표 설명 주석, ch2:274 근방). `KWW`, `H-1`, `H-2`, `M-1~M-11`, `BW`(주석형) 등은 전부 이 구역 안에서만 등장 — 렌더링 시 비가시이므로 용어 정정 대상에서 제외.
5. **라벨/참조 매크로 내부 키** — `\label{...}`, `\ref{...}`, `\eqref{...}`, `\cite{...}` 의 중괄호 안 키 문자열(예: `\label{eq:Uj}`, `\label{sec:hys}`, `\label{ssec:BW}`, `\cite{dahn1991,ohzuku1993}`). 이 키들은 영어 슬러그 그대로 유지(렌더링되지 않는 내부 식별자).

---

## 반환 요약

- **용어 27건**, **약자 18건** 표로 정리(위 ①·②). 치환 금지 구역 5범주 목록화(③).
- 주요 판단 5건:
  1. **FD 이중 의미 충돌**(ch2) — Fermi–Dirac 과 finite difference(유한차분)가 같은 챕터에서 같은 약자를 공유. 가장 시급한 정정 대상으로 판단(오독 위험 최고).
  2. **천이 vs 전이 이원 표기** — 동일 개념(transition)에 다른 한자어를 국소적(MIT)·전역적(일반 상전이)으로 나눠 씀. 통일 또는 명시적 안내 필요.
  3. **MSMR 정의 지연**(ch1) — 코드 식별자로 317줄에 선노출되나 산문 정의는 2065줄(약 1750줄 격차); ch2는 즉시 병기로 모범적.
  4. **GITT·OCV·OCP·SOC·DFT 전량 미병기** — 5개 약자 모두 완전영문형이 문서 어디에도 없음(문서가 다른 약자는 대체로 최소 1회 병기하는 관례와 대비).
  5. **격자(lattice/grid) 다의어 충돌 + 코너(corner case) 비표준 용법** — "격자"가 물리적 lattice 와 수치 grid 두 뜻을 겸함, ch2 "코너"는 물리적 모서리가 아닌 공학 용어 "corner/edge case" 전용 의미로 쓰여 원어 병기 없이는 오독 소지.
- **대상 .tex 파일 수정 없음**(정책대로 표만 산출) — 산출물 경로: `D:\Projects\Project_Anode_Fit\Claude\results\process\V1013_TERMS_POLICY.md`.
