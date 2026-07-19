# 최근문헌(2021–2026) 고도화 방향성 — 종합 결정 패키지 (v1.0.24)

> B트랙 심화. 최근 5년 XRD·DFT·이론물리·수식해석 논문으로 문건 모델 고도화 **방향성 확정+검증**.
> 대상 **LCO·흑연·흑연+Si 한정**(NCM·NCA·LFP·Na·전고체 제외). **문건·코드 무수정** — 반영은 사용자 최종 "가자".
> 4창 병렬 리서치(흑연/LCO/흑연+Si/교차방법론) union. 전 인용 실검증(DOI/arXiv). raw = `lit_raw/01~04`.

---

## 0. 판정 4-tier (본 문건 규약)
- **★ 반영준비(REFLECT-READY)**: XRD/DFT 근거 확실·저위험·실측 시드값 확보 → 사용자 승인시 즉 반영가능.
- **◐ 선검증(TEST-FIRST)**: 유망하나 우리 데이터/구조 대조 필요 → 반영 전 실험 1회.
- **○ 인용만(JUSTIFY-ONLY)**: 물리 정당화·서지로만, 모델 변경 아님.
- **✗ 미반영(DON'T)**: 명시 기각(이유 포함).

## 1. 헤드라인 — 4창 독립 수렴 (가장 중요)
**near-delta 천장(우리 기존 R²~0.95 한계: 로지스틱 MSMR 이 두-상 진짜 delta 못냄)의 해법을 4 스트림이 독립적으로 같은 곳으로 지목:**

> **로지스틱을 정칙용액(Frumkin) 으로 최소일반화 — 상호작용 Ω 복원 + Ω>2RT 서 공통접선(Maxwell)= 진짜 두-상 plateau → near-delta. 이를 기존 kinetic 폭과 합성.**

- 우리 `ξ_j=1/(1+exp((V−U_j)/w_j))` 은 **정확히 이상(g=0) Frumkin/Fowler 삽입 등온선**. 상호작용항을 0 에서 복원하면 그대로 정칙용액이 됨(방법론 A10 Levi–Aurbach 1999; 흑연 적용). → **재작성 아닌 기존식의 자연확장.**
- 두 등가 경로: **(i)** 자유E+공통접선(Yao–Viswanathan 2024 *JPCL* 15,1143; 코드 `diffthermo` MIT) — g=이상엔트로피+Redlich–Kister 초과, 음함수정리로 미분관통 → **PDE 없이 gradient 피팅**. **(ii)** gallery별 Frumkin(음함수 site-fraction, 1-D root-find). 둘 다 "곡선 생성+피팅" 영역 유지.
- **결정적 2단 구조**: 평형 near-delta(sharp) **⊗ kinetic V_n/L_V broadening(유한폭)** = 현실 피크. 즉 R²~0.95 천장은 *평형 형상* 한계이고, **기존 kinetic 층을 안 건드리고** 평형층만 정칙용액화하면 닫힘.
- **우리 이전 실패 재해석**: `regsol_proto`(R²=0.79) 는 **단일상 Frumkin(Ω<2RT, Maxwell 없음)** 이라 실패한 것. 문헌은 **Ω>2RT + Maxwell(진짜 miscibility gap)** 이 정답이라 확증 → §5 에서 이 정정판을 실검증.

## 2. 두 번째 수렴 — "두-상 vs 고용체는 율의존" (3 스트림 공통)
- LCO(Flores 2021 *ACS AMI* 13, 10.1021/acsami.1c04383): IMT 두-상은 **극저율서만**; ~C/10 위서 kinetic 억제→고용체 경로.
- 흑연(Fujimoto 2022 *JES* 169,070529: 9피크는 C/250 서만·실율서 병합; Takagi 2025 *Carbon*: 5C 서 stage 우회).
- **함의(아키텍처 정합)**: 우리 **Ω>2RT 기준 = 저율(평형) envelope 만**. 유한율 피크폭은 **kinetic 층(R_n, L_V)** 소관. → **회사 GITT/저율(C/50) = 평형 Ω / 0.1·0.2C = kinetic** 로 자연 분담. 율의존 폭을 열역학 w_j 로 우겨넣으면 오fit(명시 경계 필요).
- 이는 사용자 "조건 따라 피크 잡힘" + 앞선 stage-2L(45℃/25℃) 관측과 **한 그림**: 평형 열역학(Ω·ΔS) 이 *언제* 두-상인지, kinetic 이 *얼마나* broaden 하는지.

## 3. 실측 시드값 확보 (사용자 원 요구 "실측값으로 시작점, Ω 텀 기반")
사용자가 원한 "무시했던 Ω 텀을 넣고 실측 시드" 가 이제 **구체 수치로** 가능:

### 흑연
| 소스 | 시드 제공 | 값 |
|---|---|---|
| **Paul 2024** *JES* 171,103505 (MCMB) | U_j·ω_j·**dU_j/dT** 5-gallery | U⁰={0.289,0.211,0.132,0.126,0.089}V·ω={4.25,0.112,0.826,0.090,0.113}·dU/dT={+1.39,+.01,−.14,−.22,−.02}e-3 V/℃ |
| **Paul 2024** *JES* 171,020507 (상용) | U_j·X_j·ω_j 6-gallery | doublet: G3≈G4(0.128/0.126)·G5≈G6(0.0886/0.0888) = **우리 stage-2L split 독립 확증** |
| **Cordoba 2024** arXiv:2401.13108 | **Ω>2RT 실수치 앵커** | Ω_a(면내)=64.3meV≈**2.5·RT**(>2RT ⇒ miscibility gap) |
| **Reynier 2003·Koch 2026** | ΔS(x) 검증타깃 | +0.3mV/K dilute→음 dip@2L→2↔1 anomaly |

- **ω_1=4.25(넓은 dilute) vs ω_4=0.09(near-delta)** = 우리 "고용체↔두-상" 대비가 이미 MSMR ω 로 표현됨(문헌 실측). → **폭 시드를 Ω>2RT 기준으로 잡자**는 사용자 제안이 문헌 수치로 뒷받침.

### LCO (최약축 — 물리 골격 대폭 보강)
- **3 feature = 3 물리**(단일기제 X): **~3.94V**(x0.75–0.94 절연체–금속 두-상, Ménétrier 1999 구동력)·**~4.1–4.2V**(x=0.5 단사 order-disorder **doublet**, Reimers-Dahn 1992·Ohzuku 1994)·**~4.55/4.62V**(H1-3/O1 staging, 부분비가역).
- **ΔS 분해**(Reynier 2004 *PRB* 70,174304): config 지배·phonon 큼(음)·**전자 작음**. → 우리 **ΔS_e 전자항은 작게 fit·과대가중 금지**(config+phonon 이중계상 위험).
- x=0.5 는 **1 피크 아닌 2 근접 narrow** = 모델에 ≥2 반응 필요.

### 흑연+Si
- **Si=연속 고용체**(소수 broad gallery), 다중 narrow 아님(Chevrier-Dahn 2009·Artrith 2018). 유일 진짜 두-상=**c-Li₁₅Si₄ 1차 심리튬 plateau**(~50–60mV).
- **히스테리시스=준정적 branch offset**(Köbbing 2024·Fu 2023), 단순 |I|-lag 아님 → Si-host **리튬화/탈리튬화 분리 U_j**.
- **가산 Gr+Si 중첩 = 준평형서 문헌 지지**(Tu-Dao-Verbrugge-Koch 2024 "clearly a superposition"·Berhaut 2023 휴지 공통μ) — §4 참조.

## 4. 소재별 결정표

### 4.1 흑연
| # | 방향 | 판정 | 근거·위험 |
|---|---|---|---|
| G1 | Ω>2RT 기준 폭시드(두-상 sharp/고용체 broad) | **★반영준비** | Cordoba Ω_a≈2.5RT·Paul ω 스펙트럼. 위험 낮음(문건 Ω 와 정합) |
| G2 | U_j·ΔS_j 실측 시드(Paul 2024) | **★반영준비** | 5-6 gallery 실측; 위험: MCMB≠임의흑연(범위 시드로만) |
| G3 | near-delta = 정칙용액+Maxwell(§1) | **◐선검증**(§5) | 헤드라인; 위험: 음함수화·kinetic 합성 검증 필요 |
| G4 | stage-2L doublet(3↔2L·2L↔2) 명시 | **○인용/이미내장** | Paul 6-gallery·Koch 엔트로피 dip 확증. 코드 이미 별도명명(T_SPLIT_FINDING) |
| G5 | dilute 1′↔4 농도의존 보정 | **◐선검증** | Mercer 2019 vs Azizi 2025 **상충**(비선형 vs 상수) → 해소 전 하드코딩 X |
| G6 | 전이 6+ 로 증설 | **✗미반영** | XRD 미지원 curve-fitting(기존 판정 유지) |
| G7 | DFT 결합E(0.41eV)를 Ω 로 대입 | **✗미반영** | 면내 bare=반발(ordering), 상분리 아님. 유효 Ω 는 창발(~2.5RT) |

### 4.2 LCO
| # | 방향 | 판정 | 근거·위험 |
|---|---|---|---|
| L1 | 3 feature 3 물리 골격(두-상/order-disorder/staging) | **★반영준비** | Reimers-Dahn·Ohzuku·Ménétrier 정본. 위험 낮음 |
| L2 | x=0.5 를 ≥2 narrow 반응(doublet) | **★반영준비** | XRD 확정 단사 order-disorder |
| L3 | ΔS_rxn 실측 시드(Reynier 2004·Hudak 2014 dU/dT) | **★반영준비** | 디지타이즈 실 dU/dT |
| L4 | ΔS_e 전자항 유지·**작게 fit** | **◐선검증** | Reynier: 전자엔트로피 작음 → bound 보정으로 강등·검증 |
| L5 | 3.94V 두-상 = near-delta(정칙용액, §1) | **◐선검증** | Ménétrier IMT 구동. 단 Flores: 율의존(kinetic 분담) |
| L6 | R_n(x) SOC 의존(HV 전이서 spike) | **◐선검증** | Ohnishi 2021; >4.4V fit 시만. 박막→다공 미이전 |
| L7 | diffthermo LCO 파라미터 그대로 | **✗미반영** | **O2 폴리타입**(우리 O3 아님). 방법만 |
| L8 | double-Gaussian 경험식(Barcellona) | **✗미반영** | 열역학 근거 없음·전셀 합성 |

### 4.3 흑연+Si
| # | 방향 | 판정 | 근거·위험 |
|---|---|---|---|
| S1 | 가산 Gr+Si 중첩(공통전위) 유지 | **★반영준비**(이미) | Tu2024·Berhaut2023 지지. 우리 R²=0.94–0.998 정합 |
| S2 | 중첩 유효경계 명기(~200mV·≲C/20) | **★반영준비** | Schweigart 2025·Frankenstein 2025(고율/부하서만 결합) |
| S3 | Si=연속 고용체(소수 broad gallery) | **★반영준비** | Chevrier-Dahn·Artrith. 위험 낮음 |
| S4 | Si 히스테리시스 = 분리 U_j branch | **◐선검증** | Köbbing 2024; 우리 L_V lag 는 잔여 율의존만 |
| S5 | c-Li₁₅Si₄ 1차 plateau 별도항 | **◐선검증** | 1차/심SOC 전용; 순환 a-Si 엔 부재 |
| S6 | 블렌드 역학결합(Si팽창→흑연전위 shift) | **✗미반영**(현) | 평형 dQ/dV 스코프밖(kinetic/mechanical 확장=스코프크립) |

## 5. 교차 방법론 결정 (산업 방어력 직결)
| # | 방향 | 판정 | 근거·도구 |
|---|---|---|---|
| M1 | **near-delta = 정칙용액+공통접선⊗kinetic**(§1) | **◐선검증→§6** | Yao-Viswanathan·Levi-Aurbach. `diffthermo`(MIT, PyBaMM/MATLAB 내보내기) |
| M2 | **일관성: 열역학제약+전역/베이지안+공유셋** | **★반영준비(방법론)** | PyBOP(arXiv2412.15859)·Hu-Schwartz(Zenodo5847378)·Kuhn2026. 자유 per-cell w_j 산포를 unidentifiable 방향으로 노출 |
| M3 | stoich/endpoint 정렬 선행(폭 산포 숨은원인) | **★반영준비** | Lu-Trimboli-Plett 2021 |
| M4 | U_j(T)·ω_j 온도의존 단일셋(조건별 refit X) | **◐선검증** | Paul 온도-MSMR. 결정필요: 폭이 ω·RT/F(고정ω) vs ω(T) |
| M5 | dV/dQ 강건성(평탄영역 dQ/dV 발산 회피)·GP 미분 | **○인용/보강** | Olson-Dickinson·Beatty. 우리 BDD 에 dV/dQ 경로 보완 |
| M6 | Bazant/Dreyer PDE 를 생성기로 | **✗미반영** | 무거운 PDE(회피대상). 물리 정당화로만 인용 |
| M7 | 비대칭 폭 커널 창시 후 "문헌근거" 주장 | **✗미반영** | 흑연 비대칭 폐형 커널 미발표(창시=우리 몫, 문헌 아님) |

## 6. 즉시 검증 대상 (본 phase 실행)
**M1/G3(near-delta 정칙용액+Maxwell)** 을 우리 흑연 두-상 피크로 실검증 → §1 헤드라인을 "문헌 주장"에서 "우리 데이터 확인"으로. (실행: `v24_regsol2.py` → `regsol2.png`; 이전 단일상 실패의 Ω>2RT+Maxwell 정정판.)

## 7. 정직한 갭 (문헌에 없는 것)
- **Si 정칙용액 Ω_Si fitted 값 없음**(조각만: Artrith 형성E·Braga CALPHAD) → Ω_Si 유도=모델링 스텝(인용 아님).
- **Si gallery별 ΔS_j 데이터 없음**(흑연-MCMB 만) → Si U_j(T) 는 측정/DFT 필요.
- **clean 오픈 1차 O3-LCO half-cell dQ/dV 셋 없음**(Zenodo/CAMP/BatteryArchive 전부 LCO 결여) → 현실경로=**DOI 그림 디지타이즈**(Reynier2004·Hudak2014·Reimers-Dahn1992).
- **흑연 비대칭 peak 폐형 커널 미발표**·**독립(비-fit) 전이별 Ω-in-RT 없음**(Cordoba fit 이 최선).
- **"다셀 공유+per-cell nuisance 계층 전역fit" turnkey 논문 없음**(PyBOP+Hu-Schwartz+온도MSMR 조립).

## 8. 데이터·도구 획득 타깃 (B트랙 후속)
- **LCO**(최우선): Reynier2004 dU/dT·Hudak2014 OCV+dE/dT·Reimers-Dahn1992 V(x) **디지타이즈**. diffthermo LCO=O2(주의). LiionDB 직접쿼리(material=LiCoO₂).
- **벤치마크 도구**: `diffthermo`(near-delta)·`PyBOP`(베이지안 식별)·`Hu-Schwartz`(전역 MSMR)·PyBaMM MSMR(규약대조).
- **흑연/Si**: Zenodo 20086298(기확보)·Zenodo 15470746(흑연/LNMO GITT).

## 서지 요약 (전부 실검증 — 상세 raw)
Dahn PRB44,9170(1991)·Paul *JES*171,103505/020507(2024)·Koch *JES*173,023504(2026)·Cordoba arXiv2401.13108(2024)·Rykner-Chandesris *JPCC*126,5457(2022)·Pande-Viswanathan *PRM*2,125401(2018)·Fujimoto *JES*169,070529(2022)·Reynier *JPS*119-121,850(2003) & *PRB*70,174304(2004)·Reimers-Dahn *JES*139,2091(1992)·Ohzuku-Ueda *JES*141,2972(1994)·Ménétrier *JMC*9,1135(1999)·Flores *ACS AMI*13(2021)·Hudak *JES*162(2014)·Teichert arXiv2104.08318·Yao-Viswanathan *JPCL*15,1143(2024)·Levi-Aurbach *EA*45,167(1999)·Karthikeyan-White *JPS*185,1398(2008)·Verbrugge *JES*164,E3243(2017) & Baker-Verbrugge *JES*165,A3952(2018)·Papadopoulos *EES Batt.* D6EB00061D(2026)·Tu-Dao-Verbrugge-Koch *JES*171,050520(2024)·Köbbing *AFM*34,2308818(2024)·Artrith *JCP*148,241711(2018)·Chevrier-Dahn *JES*156,A454(2009)·Hu-Schwartz *JES*169,030539(2022)·PyBOP arXiv2412.15859·Kuhn *JES*173,120509(2026)·Olson-Dickinson *ChemMater*35,1487(2023)·Beatty *Energies*17,4309(2024).
정직단서: 2건 전문 유료(EES Batt. Papadopoulos·Köbbing AFM)=abstract+2독립검색; Schmitt2022 *ChemElectroChem*(유료 미검증)=lead; Cordoba 저널판 미확인=arXiv; diffthermo-LCO=O2 폴리타입 주의; Ohzuku Li₁₋ₓ 규약.
