# DESIGN_NOTE — comp_R5 W2 (실측·데이터 우선 강조축) Ch3 저작 설계 근거

> 창 = W2(오푸스 3창 경쟁 중 실측·데이터 정합 강조). 산출 = `s31_map`·`s32_cases`·`s33_blend`·`s34_mech`·`s35_code`·`notation` .tex + 본 노트. 초안 전용(기존 파일 수정·git·Codex 접근 없음).
> 저작 규칙 준수: V1 키 + comp_R4 검증 후보 키만 \cite·수치는 comp_R4 표 원문 확인분만·기억 서지 0·조기 저장(절별)·표 열구조 고정.

## 1. 강조축 설계 근거 (W2 = 실측·데이터)

전 절(패키지 6항)을 모두 저작하되, **배분**으로 두 절을 가장 깊게 팠다(강조는 생략이 아님):

- **§3.2 케이스별(`s32_cases`, 102행) — 최심.** comp_R4 4본(SI_CASES·SIOX·SIC·SI_ENTROPY)의 tier-A 실측을 케이스별 파라미터 셋 표(`tab:si-cases`)로 확정. 각 수치에 tier 명기, 계열 간 값이 어긋나는 곳(특히 $\eta_\mathrm{ICE}$)은 **채택 근거를 캡션 각주 6건**($a$~$f$)으로 드러냄 — "문헌 간 상충이 아니라 처리·조성·바인더 차"를 명시. 엔트로피 계수 실측(−40~−105 μV/K)까지 열특성 소절로 추가.
- **§3.3 블렌드(`s33_blend`, 120행) — 최심 2.** 공통-μ 대정준 반전을 eq:sm-mc-balance 의 **한 줄 일반화**(클래스곱→host 곱)로 세운 뒤, **GS-2 비가산 공백을 BLEND_UP 8건으로 정밀 반영**: `tab:blend-evidence` 가 각 문헌의 공통-μ 함의(지지/한계)를 4열로 정리하고, Ai2022(구간별 host 교대)·Chatzogiannakis2025(비가산 결합)·Zhan2026(전위중첩 지지+균열 대가)를 가정 A/B 반례로 국소화.

나머지 4절(§3.1 지도·§3.4 기계·§3.5 코드·notation)은 물리 골격·공백 규율·계약을 정확히 쓰되 실측 앵커를 곳곳에 결합(예: §3.4 는 100–120 mV/GPa·−1.75 GPa 실측으로 닫힘/미닫힘 지점을 데이터로 국소화).

## 2. 물리 핵심 준수 (마스터 지정 — 전 창 공통)

- **§3.3 중심식**: `eq:blend-balance` = $\sum_{\mathrm{host}\in\{\mathrm{gr,Si}\}}\sum_j Q_j^{\mathrm{host}}\xi_{\eq,j}^{\mathrm{host}}(U_\oc,T)=Q\bar x$, $f_\mathrm{Si}\in[0,0.3]$ — eq:sm-mc-balance 의 한 줄 일반화(재유도 아님). 요동 양성 유일근은 xr 이월(eq:sm-mc-fluc), 재증명 안 함.
- **GS-2**: 공통-μ 완전 동시반응·가산 합성 = 1차 근사 → 물리 가정 충돌로 정직 선언. 구간별 host 전환 kinetic 모델링 = 범위 밖 명시.
- **GS-1**: Larché–Cahn 유도를 닫히는 데까지(고정 응력 강체 중심이동 `eq:si-lc-shift` + 히스 gap 구조 `eq:si-lc-gap`)만. 소성 구성식은 수치 소관으로 공백 선언 — 유사 유도 날조 없음.
- **Si 합금화 ≠ 삽입**: 생존 지도 N4~N6 재해석(유효 성분≠상전이)을 §3.1·§3.2·§3.5(warnbox)가 존중.
- **서지**: V1 14 키 전건 + comp_R4 검증 후보 20 키만 \cite. 기억 서지 0. 수치는 comp_R4 표 확인분만, 그 외 "확인 필요".
- **기호·라벨**: ch3v22_notation 계승(재정의 0). 신규 라벨 전부 `sec:si-*`/`eq:si-*`/`eq:blend-*`/`tab:si-*` 네임스페이스, 도입 절 명시(`notation.tex` 표 tab:si-notation).

## 3. 공백 4분류 표 (정의상 implicit / 수치해법 필요 / 논리 공백 / 물리 가정 충돌)

| 공백 | 위치 | 4분류 | 닫힌 부분 / 범위 밖 |
|---|---|---|---|
| eq:blend-balance 의 $U_\oc$ 음함수 | §3.3 `ssec:blend-derivation` | **정의상 implicit formulation** | 고정-함량 반전(대정준→정준 Legendre 켤레) — eq:sm-mc-balance 계승. 수치 유일근 존재(요동 양성). 공백 아님, 지위 명시. |
| GS-2 블렌드 비가산·구간교대 | §3.3 `ssec:blend-gs2` | **물리 가정 충돌** | 평형 가산-동시반응 가정 vs 실측 비가산(Chatzogiannakis2025)·구간교대(Ai2022). 평형 반전은 정확. **범위 밖**: 구간별 host 전환 kinetic 결합 모델. |
| GS-1 기계 히스(σ→μ) | §3.4 `ssec:si-gs1` | **물리 가정 충돌 + 수치해법 필요** | 닫힘: 고정 σ 강체 중심이동 ΔU_σ·gap 구조(경로차). 충돌: 가역 이중웰 vs 소성 경로의존 소산(55 mV 상한 vs 수백 mV). 수치: 구성식 σ(θ,이력)=탄소성 모델(koebbing2024·jiang_sihys2020). |
| Si 유효 클래스 ≠ 진짜 staging | §3.1 N5 / §3.2 / §3.5 | **물리 가정 충돌**(경계) | 성분=곡선기술 성분(비정질), 미시 자리 해석 소멸. 재해석으로 흡수(공백 아님, 해석 경계 명시). |

**데이터 공백(4분류와 별개 — "확인 필요")**: SiO_x 절대 평균전위·SiO_x 히스 절대 mV·Si 저온 ΔS(T) 정량·V_Li 절대 수치·tier-B 정량값(yamada_sio2012·lee_sic2025·zhang_150ah2024·mertin_entropy2023) — 표에 수치로 싣지 않고 명시적 "확인 필요"로 표기.

## 4. 서지 채택 목록 (마스터 등재용)

### 4.1 V1 키 (ch3v22_bib 기존 14 — 전건 사용)
wen_huggins1981 · limthongkul2003 · li_dahn2007 · obrovac_christensen2004 · chevrier_dahn2009 · beaulieu2001 · sethuraman_stressevo2010 · sethuraman_stresspot2010 · liu_sizefracture2012 · obrovac_chevrier2014 · verbrugge_lisi2016 · jiang_sihys2020 · larchecahn1973 · koebbing2024.

### 4.2 comp_R4 검증 후보 키 (신규 20 — \cite 사용분, 마스터 등재 대상)

제안 키 형식 = `저자_주제+연도`. tier·전거 = comp_R4 표. SI_CASES-계열 4건은 표에 제목 미기재 → 등재 시 Crossref 제목 대조 권고(★).

| 제안 키 | 서지 | DOI | tier | 원천 |
|---|---|---|---|---|
| wang_asi2013 ★ | Wang et al., *Nano Lett.* **13**(2), 709–715 (2013) | 10.1021/nl304379k | A | SI_CASES 1.2 |
| mcdowell_coreshell2013 ★ | McDowell et al., *Nano Lett.* **13**(2), 758–764 (2013) | 10.1021/nl3044508 | A | SI_CASES 1.4 |
| mcdowell_review2013 ★ | M. T. McDowell, S. W. Lee, W. D. Nix, Y. Cui, *Adv. Mater.* **25**(36), 4966–4985 (2013) | 10.1002/adma.201301795 | B | SI_CASES 1.4 |
| ogata_nmr2014 ★ | Ogata et al., *Nat. Commun.* **5**, 4217 (2014) | 10.1038/ncomms4217 | A | SI_CASES 1.5 |
| miyachi_sio2005 | M. Miyachi, H. Yamamoto, H. Kawai, T. Ohta, M. Shirakata, "Analysis of SiO Anodes for Lithium-Ion Batteries," *J. Electrochem. Soc.* **152**(10), A2089–A2091 (2005) | 10.1149/1.2013210 | A | SIOX #1 |
| kitada_sio2019 | K. Kitada, O. Pecher, P. C. M. M. Magusin, M. F. Groh, R. S. Weatherup, C. P. Grey, "Unraveling the Reaction Mechanisms of SiO Anodes…," *J. Am. Chem. Soc.* **141**(17), 7014–7027 (2019) | 10.1021/jacs.9b01589 | A | SIOX #3 |
| zhang_sio2018 | Zhang, Qin, Liu, Liu, Ren, Jansen, Lu, "Capacity Fading Mechanism and Improvement of Cycling Stability of the SiO Anode…," *J. Electrochem. Soc.* **165**(10), A2102–A2107 (2018) | 10.1149/2.0431810jes | A | SIOX #4 |
| yom_sio2016 | Yom, Hwang, Cho, Yoon, "Improvement of irreversible behavior of SiO anodes… by a solid state reaction at high temperature," *J. Power Sources* **311**, 159–166 (2016) | 10.1016/j.jpowsour.2016.02.025 | A | SIOX #5 |
| andersen_sic2019 | Andersen, Foss, Voje, Tronstad, Mokkelbost, Vullum, Ulvestad, Kirkengen, Mæhlen, "Silicon-Carbon composite anodes from industrial battery grade silicon," *Sci. Rep.* **9**, 14814 (2019) | 10.1038/s41598-019-51324-4 | A | SIC #1 |
| naboka_sic2021 | Naboka, Yim, Abu-Lebdeh, "Practical Approach to Enhance Compatibility in Silicon/Graphite Composites…," *ACS Omega* **6**(4), 2644–2654 (2021) | 10.1021/acsomega.0c04811 | A | SIC #2 |
| lee_sic2025 | Lee et al. (14인), "Multiscale Carbon-Integrated Silicon Anode for Stable Cycling Under Practical Li-Ion Battery Conditions," *Adv. Energy Mater.* (2025) | 10.1002/aenm.202504250 | B | SIC #3 |
| bohm_entropy2024 | Böhm, Zintel, Ganninger, Jäger, Markus, Henriques, "Exploring the Impact of State of Charge and Aging on the Entropy Coefficient of Silicon–Carbon Anodes," *Energies* **17**(22), 5790 (2024) | 10.3390/en17225790 | A | SI_ENTROPY #1 |
| arnot_calorimetry2021 | Arnot, Allcorn, Harrison, "Effect of Temperature and FEC on Silicon Anode Heat Generation Measured by Isothermal Microcalorimetry," *J. Electrochem. Soc.* **168**(11), 110536 (2021) | 10.1149/1945-7111/ac315c | A | SI_ENTROPY #2 |
| wojtala_entropy2022 | Wojtala, Zülke, Burrell, Nagarathinam, Li, Hoster, Howey, Mercer, "Entropy Profiling for the Diagnosis of NCA/Gr-SiOₓ Li-Ion Battery Health," *J. Electrochem. Soc.* **169**(10), 100527 (2022) | 10.1149/1945-7111/ac87d1 | A | SI_ENTROPY #3 |
| bohm_thermal2025 | Böhm, Bracht, Kallfa, Markus, Henriques, "Temperature-Dependent Thermal Effects and Capacity Characteristics of Silicon Anodes…," *J. Electrochem. Soc.* **172**(5), 050537 (2025) | 10.1149/1945-7111/adda7a | A | SI_ENTROPY #5 |
| ai_composite2022 | Ai, Kirkaldy, Jiang, Offer, Wang, Wu, "A composite electrode model for lithium-ion batteries with silicon/graphite negative electrodes," *J. Power Sources* **527**, 231142 (2022) | 10.1016/j.jpowsour.2022.231142 | A | BLEND #2 |
| chatzogiannakis_blend2025 | Chatzogiannakis, Ghilescu, Giannadaki, Cabello, Casas-Cabanas, Palacín, "Decoupling Silicon and Graphite Contribution in High-Silicon Content Composite Electrodes," *Batteries & Supercaps* **8**(10), e202500104 (2025) | 10.1002/batt.202500104 | A | BLEND #5 |
| zhan_siox2026 | Zhan, Jin, Stapf, Meyer, Birke, Fill, "Unraveling the vertical expansion and hysteresis in SiOx/graphite composite electrodes…," *J. Energy Storage* **154**, 121227 (2026) | 10.1016/j.est.2026.121227 | A | BLEND #6 |
| gautam_blend2024 | Gautam, Mishra, Bhawana, Kalwar, Dwivedi, Yadav, Mitra, "Relationship between Silicon Percentage in Graphite Anode…," *ACS Appl. Mater. Interfaces* **16**(35), 45809–45820 (2024) | 10.1021/acsami.4c10178 | A | BLEND #3 |
| moyassari_blend2022 | Moyassari, Roth, Kücher, Chang, Hou, Spingler, Jossen, "The Role of Silicon in Silicon-Graphite Composite Electrodes…," *J. Electrochem. Soc.* **169**(1), 010504 (2022) | 10.1149/1945-7111/ac4545 | A | BLEND #4 |

**표에만 등장(text 참조, 미-\cite — 등재 선택 사항)**: tu_blend2024(A, BLEND #1)·zhang_150ah2024(B, BLEND #7)·mertin_entropy2023(B, BLEND #8)·yamada_sio2012(B, SIOX #2). 채택 시 tier·전거 위와 동일.

## 5. 라벨 이관 주의 (마스터 그래프팅용)

- 본 W2 §3.1(`s31_map`, `sec:si-survival`)이 현행 `ch1_appD_si`(`sec:appendix-si`)를 대체하면, **`ch3v22_notation.tex` 의 `\S\ref{ssec:si-gap}` 는 본 패키지 §3.4 `sec:si-mech`(또는 `ssec:si-gs1`)로 재지정**해야 한다(기존 라벨 미사용 → xr 미해소 방지). 본 창은 기존 파일을 수정하지 않으므로 이 재지정은 마스터 집행 소관.
- 본 W2 라벨은 전부 신규 네임스페이스라 기존 `ssec:si-*`/`tab:simap` 과 **충돌 없음**(대체 시 구 라벨 은퇴).
- Ch1/Ch2 xr 참조 라벨(eq:sm-mc-balance·eq:sm-mc-fluc·eq:sm-mc-factor·eq:sm-mc-occ·eq:sm-eqcond·eq:sm-logistic·eq:sm-nernst·eq:sm-thresh·eq:mu·eq:sum·eq:logisticsolve·eq:eqpeak·eq:dUhys·eq:Ubranch·fig:hysgap·sec:sm-mc·sec:lco-code)은 **전건 소스 실확인**(추측 0).

## 6. 절별 요약

| 절 | 파일 | 행수 | 신규 식(라벨) | 신규 표 | 자산 |
|---|---|---|---|---|---|
| §3.1 지도 | s31_map | 100 | 0 | tab:si-nodemap | V22-R5-02~05 |
| §3.2 케이스 | s32_cases | 102 | 0 | tab:si-cases | V22-R5-06~10 |
| §3.3 블렌드 | s33_blend | 120 | 3 (eq:blend-factor·eq:blend-balance·eq:blend-dqdv) | tab:blend-evidence | V22-R5-11~14 |
| §3.4 기계 | s34_mech | 75 | 3 (eq:si-lc-mu·eq:si-lc-shift·eq:si-lc-gap) | — | V22-R5-15~17 |
| §3.5 코드 | s35_code | 58 | 0 | — | V22-R5-18~20 |
| 기호표 | notation | 50 | 0 | tab:si-notation | V22-R5-01 |
| **계** | | **505** | **6 식·31 라벨** | **4 표** | **20 앵커** |

신규 라벨 31 = 식 6 + 절 5(sec:) + 소절 16(ssec:) + 표 4(tab:). box 관행: keybox×4·srcbox×3·verifybox×1·codebox×1·warnbox×1.
