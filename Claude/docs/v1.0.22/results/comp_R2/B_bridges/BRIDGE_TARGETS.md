# BRIDGE_TARGETS — 인용 다리(흑연분) 대상 선별표 (v1.0.22 R2 · O-B)

> 산출: 초안 전용. 마스터 .tex 수정 없음. 대상 = 신 Ch1(`ch1_graphite_v1.0.22.tex` 조립분 = 곡선사슬 ch1_sec00~10 · Part T ch2_sec00~10 · sec18 · 부록 ch1_appA/appB·ch2_appA/appB · ch1v22_bib)만. LCO 절(ch1_sec11~17, `ch2_lco` 소관) = R3 · Si 부록(ch1_appD_si) = R5 → 스캔 제외(그 파일들은 graphite master 에 \input 되지 않음).
> 서지 규칙: `results/V1022_REFERENCE_LEDGER.md`(v1.0.21 승계) V1 키만. 아래 전건 V1 확인.

## 1. D22-5 핵심 12곳 (마스터플랜 `2026-07-17-v1022-master-plan.md` §7 line 71) 대조 — 소관 분류

| # | 키 | D22-5 표기 | 소관 | 신 Ch1 cite 실재? |
|---|---|---|---|---|
| 1 | dreyer2010 / dreyer2011 | 히스 다입자 | **R2(본 창)** | O — sec04:7,14,244 · sec07:72 |
| 2 | mckinnon1983 | 등온선 | **R2(본 창)** | O — sec02a:158 |
| 3 | bazant2013 | χ 분해 | **R2(본 창)** | O — sec05:16 |
| 4 | marianetti2004 | Mott | R3(LCO) | (ch1_sec15:59 — graphite master 밖) → 제외 |
| 5 | vanderven1998 | 상도표 | R3(LCO) | (ch1_sec13:109 — master 밖) → 제외 |
| 6 | msmr_origin2017 / bakerverbrugge2018 | MSMR 계보 | R3(LCO) | (ch1_sec17 — master 밖) → 제외 |
| 7 | weppner_huggins1977 | GITT | **R2(본 창)** | O — sec01:208 (측정원리 bgbox) |
| 8 | sethuraman(응력) | 응력 | R5(Si) | (ch1_appD_si — master 밖) → 제외 |
| 9 | larchecahn1973 | 응력-화학퍼텐셜 | R5(Si) | (ch1_appD_si:74 — master 밖) → 제외 |
| 10 | verbrugge_lisi2016 | MSMR-Si | R5(Si) | (ch1_appD_si — master 밖) → 제외 |
| 11 | baek_pilon2022 | 엔트로피 측정 | **R2(본 창)** | O — sec01:213 (측정원리 bgbox) |

**12곳 판정**: R2 소관 = 5 키군(#1·2·3·7·11). R3 소관 4 키군(#4·5·6 + reynier2004 LCO)·R5 소관 3 키군(#8·9·10)은 graphite master 에 \input 되는 파일에 cite 가 없음(전부 LCO/Si 전용 절) → 월권 0 으로 자동 제외 확인.

## 2. 신 Ch1 본문 \cite 전수 스캔 — Part T 등 추가 load-bearing 판정

BRIEF 지시("Part T 의 allart2018·reynier 등 load-bearing 판정 포함")대로 12곳 밖 신Ch1 cite 를 전수 스캔해 다리 필요도 판정.

| 키 | 본문 cite 위치(파일:행·절) | load-bearing 판정·사유 | 다리 필요도 |
|---|---|---|---|
| **dreyer2010/2011** | sec04:14(§4 히스 기원)·sec07:72(§7 iii-a 평탄역) | **상** — 우리 spinodal gap(eq:dUhys)·앙상블 평탄역(iii-a)이 이 논문의 다입자 준안정성·순차전환 결과에 직접 의존 | 상 |
| **mckinnon1983** | sec02a:158(Part 0 eq:sm-bare 직후) | **상** — 우리 격자기체 등온선(eq:sm-bare 원형 → eq:Veq 상호작용형)의 삽입전극 적용 원전 | 상 |
| **bazant2013** | sec05:16(§5 eq:bv 직전 χ 분해) | **상** — 우리 정·역 속도식(eq:bv)의 구동력 χ 분해가 이 논문의 비평형열역학 전하전달 정식화 | 상 [원문 검증완료] |
| **weppner_huggins1977** | sec01:208(§1 측정원리 bgbox (i)) | **중** — 우리 준평형 $U_\oc$·분극보정 $V_n$(eq:vn)이 GITT 준평형 OCV 의 연속 근사판 | 중 |
| **baek_pilon2022** | sec01:213(§1 측정원리 bgbox (ii)) | **중** — 엔트로피계수 부호·모양 ↔ 상전이유형 해석지도(우리 단상폭·broadening·질서화 구분의 판독틀), tier B | 중 |
| **bernardi1985** | ch2_sec07:11(§2.7 eq:qrev)·ch2_sec09:25 | **상** — 우리 가역발열식(eq:qrev)이 이 논문 일반 에너지수지의 항 축약(혼합·상변화 항 소거) | 상 |
| **allart2018** | ch2_sec02:137,139,153,168·ch2_sec09:22(procedurebox 4) | **중** — 우리 중심표준값 $\Delta S^0_j=F\dd U_j/\dd T$ 의 실측 검증 앵커(표 tab:ds 부호·규모 대조) | 중 |
| **reynier2003** | ch2_sec03:31(§2.3 eq:Svib_mode 직후)·sec01:211·ch2_sec02:137·sec10:30 | **중** — 우리 $\Delta S_\vib=\partial S_\vib/\partial x$ 고-$x$ 음 baseline 의 실측 부호 앵커("second contribution") | 중~하 |

## 3. 다리 불필요(비-load-bearing) — 스캔했으나 제외, 사유

| 키(들) | 위치 | 제외 사유 |
|---|---|---|
| hill1960·fowler1939·mcquarrie1976·ashcroftmermin1976 | sec02a·sec02b·sec05 | 통계역학 교과서 앵커 — 본문이 이미 자족 유도(Part 0·TST bgbox)로 다리 내장 |
| eyring1935·glasstone1941·laidlerking1983 | sec05:15,54,82 | TST 원전 — 본문 §5 bgbox(eq:tst-qrc~eq:tst-dG)가 이미 $k_BT/h$·$\Delta G_a$ 다리 완비 |
| dahn1991·ohzuku1993 | sec00:9·sec01:91·sec07:25·sec10:24·ch2_sec05:172 | staging 상도표·전이 초기값 앵커(값 인용) — 유도 대상 아님 |
| newman·huggins2009 | ch2_sec01:7·ch2_sec07:37 | 격자기체·Bragg–Williams 교과서 앵커 — Part 0 이 이미 유도 |
| msmr_partI·msmr_partII | ch2_sec07:37·ch2_sec09:20·ch2_sec02:140 | MSMR 계보 = R3 소관(마스터플랜 §7 R3 "MSMR 계보") → 침범 금지 |
| standardised2024·hysteresis2018 | ch2_sec07:51·ch2_sec08:105·ch2_sec09:37·ch2_sec05:198 | calorimetry·경로의존 관측/틀 인용 — 서술 정합, 식 전환 없음 |
| jpcc2021·occupation2019·chemmater2015 | ch2_sec03:33·ch2_sec04:24·ch2_sec02:60,177 | abstract/방법수준(원문 식 미확보 명기됨) — 다리화 부적격 |
| park2021·leviaurbach1999·cogswell2012·dahn1995 | sec07 다수 | 확산계수·Frumkin·계면E·용량한계 — 보조 근거(tier B/C), 유도 비의존 |
| persson2010/2010b·fly2020·rsc2021·bloom2005·dubarry2012 | sec10·sec07·sec00 | DFT 경향·rate·상순서·DVA 관측 앵커 — 서술 인용 |
| swiderska2019 | sec01:211·ch1_appA:82 | LCO 단전극 계수(tier B) — LCO 검산용, graphite 유도 비관여 |
| numverif2026 | ch2_sec05·ch2_appB | 내부 수치검증 자료 — 외부 논문 아님 |

## 4. 요약
- **대상 다리 = 8건**(D22-5 핵심 5 + Part T load-bearing 추가 3). 월권(R3/R5) 0, 12곳 대조 누락 0.
- 초안·삽입위치는 `BRIDGE_DRAFTS.md` + `br_<키>.tex`. 충돌 점검은 `BRIDGE_RISK.md`.
