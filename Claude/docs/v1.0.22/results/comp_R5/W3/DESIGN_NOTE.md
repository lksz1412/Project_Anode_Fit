# DESIGN_NOTE — comp_R5 W3 (교육·서사 우선 창) Ch3(Si·혼합음극) 저작 초안

> 산출 = `s31_map.tex`·`s32_cases.tex`·`s33_blend.tex`·`s34_mech.tex`·`s35_code.tex`·`notation.tex`(+본 노트).
> 규칙 준수: 초안 전용(기존 파일 무수정)·git 무조작·Codex 무접근·W1/W2 무열람(경쟁 독립)·조기 저장(절별 즉시).
> 강조축(W3) = 교육·서사 정합. 물리 핵심·GS-1/GS-2·서지 규율은 BRIEF_R5 명문 그대로.

---

## 1. 설계 근거 — 교육·서사 축을 어디에 실었나

**중심 서사 = "생존 지도가 곧 이 장의 목차"**. 흑연 Ch1(골격 N0~N9 세움) → LCO Ch2("같은 식·파라미터 교체·전자항 하나 추가") → Si Ch3(저장 기작이 바뀌는 최대 stress test)의 교과서 arc 를 §3.1 서두에 명시(ssec:si-arc)하고, 장 전체를 "흑연에서 배운 것 중 무엇이 Si 에서도 성립하는가" 한 물음으로 관통시켰다.

- **§3.1(최심 강조)**: 부록체 `ch1_appD_si`(tab:simap) → 본문체 승격. 5소절 구성 — (a) 세 활물질 arc·지도=목차 서사, (b) 확립 사실 8건을 **노드별 압박**으로 재배열(사실→판정 인과를 독자가 따라오게), (c) 생존 판정표 tab:si-survival(흑연→LCO 의 "전부 이월+전자항"과 대비해 "다섯 결로 갈라짐"을 캡션에 명시), (d) 최강 자산 keybox(전하 보존 전극 중립성 = §3.3 host 곱 예고), (e) 읽는 순서=동선. 라벨은 신규(sec:si-map/tab:si-survival) — 기존 부록 라벨 재정의 0.
- **읽는 흐름 배치**: 각 절 말미가 다음 절을 호명(§3.1 지도→§3.2 케이스가 재해석 노드 실증→§3.3 앵커 host 일반화→§3.4 새 물리 1개 대면→§3.5 코드 합성). keybox/verifybox/srcbox/warnbox/bgbox/codebox 를 흑연·LCO 장 관행대로 배치(핵심 요약·검산·문헌 근거·공백 경고·배경·코드 대응).
- **대칭 강조**: eq:blend-balance 를 "흑연 반전에 host 합 한 겹"으로, eq:blend-dqdv 를 "eq:sum 의 host 판"으로, eq:si-code-bitexact 를 "eq:blend-balance 검산(ii)의 코드판"으로 — 세 층위(통계역학·미분용량·코드)가 같은 한 줄 일반화임을 반복 가시화.

**단, 전 절(패키지 6항)을 모두 저작**했다 — 강조는 배분이지 생략이 아님(§3.2 케이스·§3.3 블렌드 물리·§3.4 GS-1·§3.5 코드·notation 전건).

---

## 2. 공백 4분류 표 (P3-4 / BRIEF 물리 핵심 준수)

4분류 = **정의상 implicit formulation / 수치해법 필요 / 논리 공백 / 물리 가정 충돌**. 각 공백을 분리 진단:

| # | 항목 | 절 | 4분류 진단 | 근거·처리 |
|---|---|---|---|---|
| 1 | 블렌드 반전 `U_oc` 음함수 | §3.3 (eq:blend-balance) | **정의상 implicit formulation** | eq:sm-mc-balance 계승 — 고정 전하 Legendre-켤레 반전. 논리 공백 아님(정의상 implicit). |
| 2 | N_p≥2·두 host 겹침 근 | §3.3 | **수치해법 필요** | 닫힌 역 없음 → 수치 유일근(요동 양성이 유일성 보증, eq:sm-mc-fluc 이월). |
| 3 | GS-2 완전 동시반응 | §3.3 (ssec:blend-gs2) | **물리 가정 충돌** | Ai2022 SoC별 host 전환·Chatzogiannakis2025 비가산 → 공통-μ 완전 동시반응 = **1차 근사**. 평형 OCV 앵커로는 유효, 운전 중 전환은 동역학 지배. **구간별 전환 모델링 = 범위 밖 선언.** |
| 4 | GS-1 (i) 이중웰 히스 | §3.4 (ssec:mech-gap) | **물리 가정 충돌** | 정규용액 이중웰(eq:dUhys, 상한 ≈55 mV) ≠ Si 지배 기작(소성 응력 결합, 수백 mV). |
| 5 | GS-1 (ii) 응력 폐합 | §3.4 (ssec:mech-gap) | **유도 미착수 = 범위 선언**(4분류상 '논리 공백'에 인접하나 **명시적으로 아님**) | 결합 항 eq:si-lc-U 자체는 **닫힘**(스텝 1). σ_h(x,경로)의 폐합만 골격 밖(소성 구성식+코어-쉘 기하) → 후속 Si 전용 장 선결과제. 폐합 후보 등재(koebbing2024·jiang_sihys2020). |
| 6 | SiOₓ 평균 전위·절대 히스 mV | §3.2 (ssec:si-siox) | **데이터 공백(확인 필요)** — 이론-구조 공백 아님 | 1차 문헌 미확보 → placeholder/None 계승, 임의값 미충전. |

- **정의상 implicit** 1건 · **수치해법 필요** 1건 · **물리 가정 충돌** 2건(GS-2·GS-1(i)) · **논리 공백 0건**(GS-1(ii)는 유도 미착수/범위 선언으로 명시 분리) · **데이터 공백(확인 필요)** 1항목군(2건).
- GS-1 은 흑연 부록의 판정을 **한 스텝 전진**시킴: 부록은 "이론틀 후보만 등재(범위 밖)"였으나, 본 초안은 Larché–Cahn 스칼라 결합형을 **import(스텝 1 닫힘)** 하고 **자릿수 검산(스텝 2 부분)** 까지 진행한 뒤 폐합만 공백 선언 — "닫히는 데까지만" 명령 준수.

---

## 3. 서지 채택 목록 (BRIEF 규칙 2: V1 + comp_R4 검증 후보 키만)

### 3.1 V1 키 (ch3v22_bib 등재분 — 그대로 \cite, 전 14종 중 14종 사용)
`wen_huggins1981`·`limthongkul2003`·`li_dahn2007`·`obrovac_christensen2004`·`chevrier_dahn2009`·`beaulieu2001`·`sethuraman_stressevo2010`·`sethuraman_stresspot2010`·`liu_sizefracture2012`·`obrovac_chevrier2014`·`verbrugge_lisi2016`·`jiang_sihys2020`·`larchecahn1973`·`koebbing2024`.

### 3.2 comp_R4 검증 후보 키 (upgraded 표 원문 doi 검증분 — **마스터 등재 필요**. 아래 bibitem 제안)
tier 표기는 R4 upgraded 원표 그대로. `et al.` 은 R4 표가 전 저자를 안 준 항목(마스터가 등재 전 저자 완성).

| 제안 키 | 서지(bibitem 초안) | DOI | tier | 사용 절 |
|---|---|---|---|---|
| `wang_asi2013` | Wang et al., "Two-Phase Electrochemical Lithiation in Amorphous Silicon," *Nano Lett.* **13**(2), 709–715 (2013). | 10.1021/nl304379k | A | §3.2 |
| `mcdowell_coreshell2013` | McDowell et al., *Nano Lett.* **13**(2), 758–764 (2013). | 10.1021/nl3044508 | A | §3.2 |
| `ogata_nmr2014` | Ogata et al., *Nat. Commun.* **5**, 4217 (2014). | 10.1038/ncomms4217 | A | §3.1·§3.2 |
| `miyachi_sio2005` | K. Miyachi, H. Yamamoto, H. Kawai, T. Ohta, M. Shirakata, *J. Electrochem. Soc.* **152**(10), A2089–A2091 (2005). | 10.1149/1.2013210 | A | §3.2 |
| `kitada_sio2019` | K. Kitada, O. Pecher, P. C. M. M. Magusin, M. F. Groh, R. S. Weatherup, C. P. Grey, *J. Am. Chem. Soc.* **141**(17), 7014–7027 (2019). | 10.1021/jacs.9b01589 | A | §3.2 |
| `zhang_sio2018` | Y. Zhang, W. Qin, F. Liu, Y. Liu, W. Ren, K. W. Jansen, S. Lu, *J. Electrochem. Soc.* **165**(10), A2102–A2107 (2018). | 10.1149/2.0431810jes | A | §3.2 |
| `yom_sio2016` | J. H. Yom, S. W. Hwang, S. M. Cho, W. Y. Yoon, *J. Power Sources* **311**, 159–166 (2016). | 10.1016/j.jpowsour.2016.02.025 | A | §3.2 |
| `andersen_sic2019` | H. F. Andersen, C. E. L. Foss, J. Voje, R. Tronstad, T. Mokkelbost, P. E. Vullum, A. Ulvestad, M. Kirkengen, J. P. Mæhlen, *Sci. Rep.* **9**, 14814 (2019). | 10.1038/s41598-019-51324-4 | A | §3.2 |
| `naboka_sic2021` | O. Naboka, C.-H. Yim, A. Abu-Lebdeh, *ACS Omega* **6**(4), 2644–2654 (2021). | 10.1021/acsomega.0c04811 | A | §3.2·§3.3 |
| `lee_sic2025` | S. Lee et al., *Adv. Energy Mater.* (2025). | 10.1002/aenm.202504250 | B | §3.2 |
| `bohm_entropy2024` | M. Böhm, L. Zintel, A. Ganninger, M. Jäger, T. Markus, J. F. R. V. Henriques, *Energies* **17**(22), 5790 (2024). | 10.3390/en17225790 | A | §3.2 |
| `arnot_calorimetry2021` | D. J. Arnot, E. Allcorn, K. L. Harrison, *J. Electrochem. Soc.* **168**(11), 110536 (2021). | 10.1149/1945-7111/ac315c | A | §3.2 |
| `tu_blend2024` | H. Tu, T. S. Dao, M. W. Verbrugge, S. Koch, *J. Electrochem. Soc.* **171**(5), 050539 (2024). | 10.1149/1945-7111/ad4823 | A | §3.3 |
| `ai_composite2022` | W. Ai, N. Kirkaldy, Y. Jiang, G. Offer, H. Wang, B. Wu, *J. Power Sources* **527**, 231142 (2022). | 10.1016/j.jpowsour.2022.231142 | A | §3.3 |
| `gautam_blend2024` | M. Gautam, A. Mishra, Bhawana, S. Kalwar, P. Dwivedi, A. Yadav, S. Mitra, *ACS Appl. Mater. Interfaces* **16**(35), 45809–45820 (2024). | 10.1021/acsami.4c10178 | A | §3.3 |
| `moyassari_blend2022` | E. Moyassari, T. Roth, S. Kücher, C.-C. Chang, S.-C. Hou, F. B. Spingler, A. Jossen, *J. Electrochem. Soc.* **169**(1), 010504 (2022). | 10.1149/1945-7111/ac4545 | A | §3.3 |
| `chatzogiannakis_blend2025` | D. Chatzogiannakis, M. Ghilescu, A. Giannadaki, A. Cabello, M. Casas-Cabanas, M. R. Palacín, *Batteries & Supercaps* **8**(10), e202500104 (2025). | 10.1002/batt.202500104 | A | §3.3 |
| `zhan_siox2026` | X. Zhan, C. Jin, F. Stapf, F. Meyer, K. P. Birke, A. Fill, *J. Energy Storage* **154**, 121227 (2026). | 10.1016/j.est.2026.121227 | A | §3.3 |

- **후보 키 사용 18종**(A 17·B 1). 미사용 가용 후보(등재 불요): `mcdowell_review2013`·`verbrugge_stressdiff2015`·`yamada_sio2012`(B)·`wojtala_entropy2022`·`garrick_msmr2024`(B)·`bohm_thermal2025`·`thomas_lisi2013`(B)·`zhang_prismatic2024`(B)·`mertin_entropy2023`(B).
- **기억 서지 0**: 모든 후보 키는 comp_R4 upgraded 표(doi 실검증 완료)에서만 왔다. bibitem 저자·권호도 그 표 전사이며, `et al.`/일부 이니셜은 마스터 등재 전 Crossref 최종 대조 대상(과잉 귀속 방지).

---

## 4. "확인 필요" 건수

**데이터 공백 2건**(모두 SiOₓ, §3.2 ssec:si-siox·tab:si-cases·warnbox — 5곳 표기):
1. **SiOₓ 평균 전위(V)** — 1차 문헌 미확보(2차 리뷰 0.2–0.4 V 류는 원전 DOI 미확정 → 미인용).
2. **SiOₓ 절대 히스테리시스 mV** — 순수 SiOₓ 단독 1차 문헌 미특정("결정질 대비 저감" 정성까지만).

두 건 모두 코드(§3.5)에서 tier-C placeholder 또는 `None`(공백)으로 계승 — 임의값 미충전.
tier-B 인용분(원문 대조 권고, 확인 필요와는 구분): `obrovac_chevrier2014`(Si 평균 전위 0.2–0.5 V)·`lee_sic2025`(서지만).

---

## 5. 절별 통계

| 파일 | 절 | 행수 | 신규 식(라벨) | 신규 표/절 라벨 | 주요 인용(V1 / 후보) |
|---|---|---|---|---|---|
| s31_map.tex | §3.1 생존 지도 | 133 | 0 | tab:si-survival·sec:si-map·ssec×5 | V1: 8사실 전건 / 후보: ogata_nmr2014 |
| s32_cases.tex | §3.2 케이스 | 103 | 0 | tab:si-cases·sec:si-cases·ssec×4 | V1: wen/limthongkul/chevrier/obrovac/sethuraman / 후보: wang·mcdowell·ogata·miyachi·kitada·zhang_sio·yom·andersen·naboka·lee·bohm·arnot |
| s33_blend.tex | §3.3 블렌드 | 122 | 4 (blend-occ/balance/fsi/dqdv) | sec:si-blend·ssec×3 | V1: verbrugge_lisi2016 / 후보: tu·ai·zhan·gautam·moyassari·chatzogiannakis·naboka |
| s34_mech.tex | §3.4 기계 히스 | 81 | 3 (si-lc-mu/U/hys) | sec:si-mech·ssec×3 | V1: larchecahn1973·sethuraman×2·koebbing2024·jiang·obrovac |
| s35_code.tex | §3.5 코드 명세 | 68 | 1 (si-code-bitexact) | sec:si-code·ssec×4 | (코드 — 인용 없음, xr 식 참조) |
| notation.tex | 기호표 | 47 | 0 | tab:si-notation | (계승 xr) |
| **합계** | | **554** | **8 식** | **5 sec·19 ssec·3 tab (=35 신규 라벨 포함 식)** | V1 14종 전건 · 후보 18종 |

- **신규 라벨 총 35**: 식 8(eq:blend-occ·eq:blend-balance·eq:blend-fsi·eq:blend-dqdv·eq:si-lc-mu·eq:si-lc-U·eq:si-lc-hys·eq:si-code-bitexact) + 절 5(sec:si-*) + 소절 19(ssec:*) + 표 3(tab:si-survival·tab:si-cases·tab:si-notation).
- **자산 앵커 28건**([V22-R5-01]~[V22-R5-28], 절 말미 `% 자산:` 신설).

---

## 6. xr 라이브 참조 인벤토리 (실확인 라벨만 — 추측 0)

Ch3 드라이버가 `\externaldocument{ch1_graphite_v1.0.22}`·`{ch2_lco_v1.0.22}` 로딩 → 아래 전건 소스 실확인:
- **Ch1(graphite)**: `eq:sm-mc-balance`·`eq:sm-mc-factor`·`eq:sm-mc-occ`·`eq:sm-mc-fluc`·`sec:sm-mc`·`sec:sm-electro`·`eq:logisticsolve`·`eq:dUhys`·`eq:sum`·`eq:vn`(sec:pol)·`sec:center`·`sec:width`·`sec:hys`·`sec:eqpeak`·`sec:broadening`·`sec:lag`·`sec:tail`·`fig:hysgap`·`tab:staging`.
- **Ch2(LCO)**: `sec:lco-code`·`sec:lco-code-msmr`·`tab:lco-staging`·`eq:msmr`.
- 전 라벨 `grep -rl "label{...}"` 로 소스 파일 위치 확인 완료(BRIEF 규칙 4 — 라벨 실확인, 추측 금지).

---

## 7. 마스터 체리픽 참고 (판정 도움)

- **§3.1 강점(W3 고유)**: 부록→본문 승격 시 "지도=목차" 서사 프레임과 흑연→LCO→Si arc 의 명시적 대칭. 판정표 캡션이 "다섯 결 갈라짐 vs LCO 전부 이월+전자항"을 대비 — 교육 가치 최대.
- **물리 정합**: eq:blend-balance 는 재유도 아닌 한 줄 일반화(eq:sm-mc-factor→host 곱), 유일근 이월(요동 가법)·f_Si=0/1 회수 검산 포함. GS-1 은 스텝 1 닫힘+스텝 2 자릿수까지 전진 후 폐합 공백(닫히는 데까지만).
- **접합 주의**: s31_map.tex 는 현행 `ch1_appD_si` 의 **본문체 대체 후보**(라벨 신규라 병존 시 충돌 0, 대체 시 부록 xref 갱신 필요). §3.2~3.5 는 신규 절 파일로 순차 append.
- **후보 서지 18종**: §3.2·§3.3 이 후보 키에 크게 의존 → 마스터가 ch3v22_bib+원장 등재 후 빌드해야 undef 0. 미등재 시 §3.4(V1 only)·§3.1(대부분 V1)이 먼저 안정.
