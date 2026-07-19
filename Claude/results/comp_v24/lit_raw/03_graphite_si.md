# RAW — 흑연+Si 스트림 리서치 산출 (agent a2c5f6c, 2026-07-19)

> 원본 그대로 보존(종합 전 raw). 검증: 각 항목 WebSearch/WebFetch 확인. 2건(EES Batteries A1·Köbbing A6) 전문 403/파싱불가 → abstract+2독립검색 교차확인 플래그.

## A. 확인 논문 (가치순)

**A1. Papadopoulos et al. (2026)** "Electrochemical modeling of silicon … multi-species, multi-reaction framework with atomistic insights." *EES Batteries* 2(3), 894–910. DOI: 10.1039/D6EB00061D. *(메타+abstract 확인; 전문 403)*
- 우리 MSMR 기구를 Si에 그대로 적용. **상별 독립 평형전위**(수정 Nernst), DFT/MD 파라미터화. **리튬화/탈리튬화 비대칭·상분율 진화** 재현.
- 매핑 → Si-host Σξ(1−ξ)/w + 히스테리시스층(분리 branch). VERDICT: **REFLECT**(Si-host 구성·히스테리시스 branch-U_j 의 1차 문헌 템플릿). 위험: 파라미터가 명시 상분율+atomistic 결합 → dQ/dV 단독 식별성 약함, 구조만 채용·소수 gallery 피팅.

**A2. Baker & Verbrugge (2016)** *JES* 163(2), A277. DOI: 10.1149/2.0581602jes. **+ Verbrugge & Baker (2015)** *JPCC* 119(10), 5341. DOI: 10.1021/jp512585z.
- Li-Si MSMR speciation 정초 유도(우리 Si-host 조상)+대부피변화 열역학. 매핑 → Si-host 평형 dQ/dV. VERDICT: **REFLECT**(정초·필수). 위험 없음.

**A3. Tu, Dao, Verbrugge, Koch (2024)** "…SiO/Graphite Blended Electrode … Reduced Order Model … Perturbation Theory." *JES* 171(5), 050520. DOI: 10.1149/1945-7111/ad4823.
- 직접 인용: "**three graphite potential plateaus on a sloped Si voltage curve with large voltage hysteresis, which is clearly a superposition of the contributions of graphite and Si.**" 동일 Baker/Verbrugge 계보.
- 매핑 → §3.5 가산 블렌드(공통전위)+f_Si. VERDICT: **REFLECT**(가산중첩 가정의 최강 직접 문헌지지, 정확히 같은 학파). 위험: 기질이 **SiO**(1차 비가역 Li₂O 추가) → 프레임만.

**A4. Jiang, Niu, Offer, Xuan, Wang (2022)** "…Silicon/Graphite Blended Electrodes … Multi-Material Porous Electrode Model." *JES* 169(2), 020568. DOI: 10.1149/1945-7111/ac5481.
- Si·흑연 **분리 기여**; Si 히스테리시스가 탈리튬화서 흑연 feature 에 **plateau shift** 부과.
- VERDICT: **분해=REFLECT / plateau-shift=TEST-FIRST**(shift 일부는 kinetic porous → 준평형(GITT)서 얼마 남는지 검증 후). 위험: kinetic shift 를 열역학 shift 로 혼동.

**A5. Zenodo — Flores et al. (2026 v3)** "Half-Cell OCV of Several LIB Active Materials … Various Protocols." DOI: 10.5281/zenodo.20086298. CC-BY-4.0.
- **half-cell OCV**: Si(Si-AQ-1)·Si-Gr(SiGr-AQ-1/2/3 Si% 변화)·Graphite(Gr-AQ-1). 4프로토콜: p-OCV(C/50)·p-OCV+hold·GITT(C/50+150min rest)·GITT+hold, ~5cyc, 상온. Parquet+메타(질량·wt%·이론용량) → dQ/dV·dV/dQ 정규화 직접.
- VERDICT: **REFLECT**(Si-host·블렌드중첩·히스테리시스 gap 준이상 외부검증셋. 최고가치). ※저자경고: Si OCV 는 입도·결정도 의존, 한 realization.
- ※주석: 이것은 우리가 이미 확보·피팅한 SINTEF 셋(20086298)과 동일 — 소스 재확인.

**A6. Köbbing, Kuhn, Latz, Horstmann (2024)** "Voltage Hysteresis of Silicon Nanoparticles: Chemo-Mechanical Particle-SEI Model." *AFM* 34, 2308818. DOI: 10.1002/adfm.202308818. arXiv: 2305.17533. *(메타+기제 확인; PDF 미파싱)*
- 큰 Si OCV 히스테리시스 = **딱딱한 무기 SEI 의 소성/점탄소성 변형**(압축응력 리튬화 V↓·인장 탈리튬화 V↑). 나노-Si 내부 농도구배만으론 부족.
- 매핑 → 히스테리시스층의 **물리적 기원**(gap 이 거의 일정·완화후 rate-무관인 이유). VERDICT: **TEST-FIRST/부분REFLECT**(결론 채용: Si 히스=branch간 준정적 OCV offset, 단순 |I|-lag 아님 → Si-host 리튬화/탈리튬화 분리 U_j). 전체 역학상태(응력변수)는 dQ/dV 생성기에 과함. 위험: 과모델링.

**A7. Jiang, Offer, Jiang, Marinescu, Wang (2020)** "Voltage Hysteresis Model for Silicon … Multi-Step Phase Transformations, Crystallization and Amorphization." *JES* 167(13), 130543. DOI: 10.1149/1945-7111/abbbba.
- 0-D 기구모델; **이산 반응단계**로 슬로프+plateau; c-Li₁₅Si₄ 결정화/비정질화 표면에너지장벽 **E\*=0.15V**; dQ/dV 탈리튬화 피크 **~0.25V·~0.52V**; 소입자서 피크소멸=슬로프.
- 매핑 → 히스테리시스층+c-Li₁₅Si₄ 두-상+구체 dQ/dV 피크위치(검증용). VERDICT: **TEST-FIRST**(피크위치·E\* 타깃 추출, 전체 kinetic 다파라미터 스킴은 이식 X). 위험: 파라미터 팽창.

**A8. Artrith, Urban, Ceder (2018)** "…amorphous LixSi … ML-assisted sampling … evolutionary algorithm." *JCP* 148(24), 241711. DOI: 10.1063/1.5017661.
- DFT+ANN 비정질 Li_xSi 전영역 상도/형성E; a-Li_xSi 는 **매끈 고용체**(형성E 연속 → 슬로프·featureless OCV).
- 매핑 → **Si 슬로프=연속 고용체항**(소수 broad gallery) 근거. VERDICT: **REFLECT**(물리근거, 필수). 위험 없음.

**A9. Chevrier & Dahn (2009)** "First Principles Model of Amorphous Silicon Lithiation." *JES* 156(6), A454. DOI: 10.1149/1.3111037.
- a-Si 매끈 전위-조성곡선 재현(단일상, sharp 없음). 매핑 → Si-host 평형 OCV **형상** 검증. VERDICT: **REFLECT**(a-Si 고용체 형상 고전). 위험 없음.

**A10. Fu et al. (2023)** "…Phase Transformations and Structural Evolutions during (de)Lithiation in Si Anodes." *AFM* 33, 2303936. DOI: 10.1002/adfm.202303936.
- deep-potential MD; **히스테리시스 주로 c-Li₁₅₋δSi₄ ↔ a-Li₁₅₋δSi₄** 변환서 기원; a-Si 는 단일상·저응력.
- 매핑 → 심리튬화 히스테리시스를 c-Li₁₅Si₄ 에 귀속(a-Si 슬로프와 구별). VERDICT: **DON'T-REFLECT(파라미터)/정보성**(atomistic, 피팅항 없음, branch split 위치 지침). 위험 없음.

**A11. Gao, Sun, Zhang, Shi, Zhang (2023)** "Determination of half-cell OCP curve of silicon-graphite …" *Applied Energy* 349, 121621. DOI: 10.1016/j.apenergy.2023.121621.
- Si-Gr half-cell OCP(히스테리시스 포함) 추출 알고리즘; 리튬화/탈리튬화 branch 명시. 매핑 → branch-resolved 블렌드 OCP 방법+f_Si 교차검증. VERDICT: **TEST-FIRST**(방법 재사용, 데이터는 in-paper/SI). 위험: OCP 가 모델-fit(직접측정 아님).

**A12. Kirkaldy, Samieian, Offer, Marinescu, Patel (2022)** "…Measuring Rapid Loss of Active Silicon in Si–Graphite Composite Electrodes." *ACS AEM* 5(11), 13367. DOI: 10.1021/acsaem.2c02047.
- **dV/dQ 가 Si·흑연 기여를 깨끗이 분리**(노화추적 가능). 매핑 → 가산 Si+Gr dV/dQ 분해 실증지지. VERDICT: **REFLECT**. 위험: Si 열화·broaden 시 분리성 붕괴(A17).

### 2차/보조 (확인·저순위)
- **Schweigart et al. (2024)** Si-rich Si-Gr operando XRD, *Small* 21(4), 2406615, DOI: 10.1002/smll.202406615. **≈200mV 위 a-Si 우선리튬화; 아래 Gr/a-Si/c-Si 경쟁; 전류의존.** → 가산중첩 **유효경계** 정의. TEST-FIRST(Theme B1).
- **Frankenstein et al. (2025)** "Transfer-Lithiation from Graphite to Si," *ChemSusChem* 18(7), e202401290, DOI: 10.1002/cssc.202401290. Li 가 전위차로 **Gr→Si 이동**(⁷Li NMR/XRD)·Si 과리튬화. → 결합항. TEST-FIRST/DON'T(공통전위 지지하나 느린 재분배·과리튬화 경고).
- **Berhaut et al. (2023)** lithiation heterogeneity Si-Gr, *AEM* 13, 2301874, DOI: 10.1002/aenm.202301874 (open: cea.hal.science/cea-04351203). **부하시 Li구배; 완화중 다상 이질성 소멸·화학퍼텐셜 평형화.** → **휴지시 Gr·Si 공통전위 직접지지**(중첩 전제). REFLECT(개념).
- **"Assessment of the Impact of Silicon on Loss of Active Material Quantification…"** (2025) *JES* DOI: 10.1149/1945-7111/adfca1. Si 의 넓은 히스 dV/dQ 가 Si/Gr 분리 왜곡 경고. TEST-FIRST(위험플래그).
- **Braga et al. (2014)** "Li–Si phase diagram: Enthalpy of mixing…" *J. Alloys Compd.* pii S0925838814017009. CALPHAD+**비정질 Si(Li) 근사 용액모델·혼합엔탈피** → 정칙용액 Ω 소스. TEST-FIRST(대부분 결정상; 비정질항 근사).
- **Verbrugge, Baker, Koch, Xiao, Gu (2017)** "Thermodynamic Model for Substitutional Materials," *JES* 164(11), E3243, DOI: 10.1149/2.0341708jes. MSMR **정칙용액 ω 상호작용 형식** 자체. REFLECT(w_j 에 형식적 Ω 진입점).
- 블렌드+히스 모델군: "Modeling the Influence of Silicon Content…Voltage Hysteresis"(2025) DOI 10.1149/1945-7111/adeecd; "Probing Silicon Lithiation in Si-C…Multi-Scale Porous Electrode"(2020) DOI 10.1149/1945-7111/abaa69; "Porous Agglomerate Model…Lithium-Silicon"(2025) DOI 10.1149/1945-7111/adbf51; "Mechanical stress-driven electrochemical-thermal model for graphite-silicon blended anode"(2025) *JPS* pii S0378775325004902(Si팽창→응력→흑연전위 shift=역학결합채널). 전부 TEST-FIRST 배경.
- Li₁₅Si₄ plateau: "Current density induced growth of Li₁₅Si₄…first lithiation"(2021) *J.EnergyStorage* pii S2352152X21006472 — plateau **60mV@0.1A/g→120mV@1A/g**(율의존·1차만). DON'T-REFLECT(순환 dQ/dV엔; 1차/결정).

## B. 교차 테마
**B1. 가산 Gr+Si 중첩 유효한가? → 준평형서 YES·부하서 NO.** 지지: Tu2024("clearly a superposition")·Jiang2022·Berhaut2023(휴지 공통μ)·Kirkaldy2022(dV/dQ분리). 도전(kinetic/mechanical만): Schweigart2025·Frankenstein2025·응력모델2025. 순판정: **평형/GITT dQ/dV 생성기엔 REFLECT·유효경계(rate≲C/20, ~200mV 위) 명기·율분해 데이터는 TEST-FIRST.** 빠른율 피팅 안하면 결합항 추가 X.
**B2. Si 슬로프: 다중 MSMR vs 연속 고용체? → 연속 고용체(단일상)가 물리 정답.** a-Si=단일상 반응→슬로프·featureless(Chevrier-Dahn2009·Artrith2018). 매핑: **소수 broad gallery(큰 ω/w)=이산화 고용체**, 다중 narrow 아님(비물리 staging 피크 주입). 유일 진짜 두-상=c-Li₁₅Si₄(1차 심리튬화 ~50-60mV plateau·탈리 spike ~0.43-0.45V) → 필요시 **1차/심SOC 전용 별도 narrow/plateau 항**, 순환 a-Si 엔 거의 부재. Papadopoulos2026 "상별 독립전위(소수)"=같은 결론.
**B3. 히스테리시스=준정적 OCV offset, 단순 kinetic lag 아님.** Köbbing2024(SEI소성)·Fu2023(c↔a Li₁₅Si₄)·Jiang2020 수렴: ~300-450mV gap 완화후 지속 → path/branch. 방향: Si-host **리튬화/탈리튬화 분리 U_j(branch 중심)**·L_V 는 잔여 율의존만. dQ/dV서 charge/discharge **피크 shift**(Jiang2022)=검증타깃.
**B4. 온도층 U_j(T).** MSMR 갤러리별 엔트로피/엔탈피 방법론은 **MCMB 흑연**서 시연(Part I DOI 10.1149/2754-2734/ad7d1c·Part II DOI 10.1149/1945-7111/ad70d9) — Si 범위 밖. **Si 갤러리별 ΔS 데이터 없음** → 갭(D2). U_j(T) 형식은 맞으나 Si 엔트로피계수는 측정/DFT 필요.

## C. 공개 데이터 (URL+내용)
1. **Zenodo 10.5281/zenodo.20086298** — https://zenodo.org/records/20086298 — Flores, CC-BY. half-cell OCV Si·Si-Gr(3조성)·Graphite; p-OCV(C/50)·+hold·GITT·GITT+hold; Parquet+메타. **최적**(dQ/dV·dV/dQ·히스 branch). [Primary — 기확보 SINTEF]
2. **PyBaMM `Chen2020_composite`** — https://github.com/pybamm-team/PyBaMM · data https://github.com/pybamm-team/pybamm-data — 흑연+Si 복합 음극(Si 2차상) OCP 함수. 출처 Chen2020 LG M50+복합(O'Kane). **주의:** Si-phase OCP 원출처를 docstring서 확인 후 인용. [Secondary — 코드/파라미터]
3. **Gao 2023 Applied Energy 349,121621** — Si-Gr half-cell OCP branch in-paper/SI. [방법+내장데이터]
4. **Schmitt, Schindler, Jossen 2021 JPS** pii S0378775321007606; open: https://mediatum.ub.tum.de/doc/1640045/document.pdf — Si-Gr half-cell OCP(노화변화); 디지타이즈 가능. [Secondary]
- 제외: Zenodo 15470746(흑연/LNMO, Si 없음) → 범위밖(GITT 포맷 템플릿만).

## D. 정직 갭·제외
- **D1.** half-cell Si(또는 Si-Gr) dQ/dV 를 명시 연속고용체항으로 피팅+a-Li_xSi 정칙용액 Ω 보고 논문 **없음**. 조각은 존재(MSMR ω=Verbrugge2017·비정질형성E=Artrith2018·CALPHAD혼합엔탈피=Braga2014)나 fitted Ω_Si 를 주는 단일소스 없음. Artrith/Braga 서 Ω_Si 유도=모델링 스텝(인용 아님).
- **D2.** Si 갤러리별 ΔS_j 데이터 없음(흑연-MCMB MSMR-온도만, 범위밖). U_j(T) 용 Si dU/dT 미측정.
- **D3.** 블렌드 율/역학 결합 실재하나 평형생성기에 넣을 폐형 없음 — Schweigart/Frankenstein/응력모델은 결합 *존재*만 정량, 평형 가산중첩 보정폐형 아님. 반영=kinetic/mechanical 확장(스코프크립).
- **D4.** EES Batteries A1·Köbbing A6 전문 미fetch(RSC403·AFM PDF바이너리). 메타+2독립검색 교차확인 — 이 둘의 정량 파라미터표는 PDF 대조 후 사용.
- 제외: Braga2014 숫자DOI 미표시(venue+year+pii 로 인용); 특허·HEA·순흑연/NMC 결과 폐기. 그 외 미확인 인용 없음.

**Bottom line:** 문헌은 우리 2대 가정 지지 — (i) 공통전위 가산 Gr+Si 중첩(준평형 dQ/dV), (ii) Si=고용체(소수 broad gallery). 3대 저후회 업그레이드: **branch-의존 Si U_j 히스테리시스**(A6/A7/B3), **1차 c-Li₁₅Si₄ plateau 별도항**(A7/A10/B2), **중첩 유효경계 ~200mV/저율 명기**(B1).
