# RAW — 교차 방법론 스트림 리서치 산출 (agent a3046a8d, 2026-07-19)

> 원본 보존. 검증: 실검색/fetch(title+저자+year+venue+DOI/arXiv). 소재: 흑연/LCO/Si 예시만. NMC/NCA/LFP/Na/전고체는 명시 off-target 정초이론(Dreyer/Bazant, 사용자 지명)만.
> 핵심 관찰: 우리 logistic ξ_j=1/(1+exp((V−U_j)/w_j)) = **이상(g=0) Frumkin/Fowler 삽입 등온선**, MSMR 폭 ω_j = Verbrugge "비-Nernst 편차". near-delta 천장 = "이상혼합 등온선은 miscibility gap 못 만듦" → 해법 지시.

## A. 확인 논문 (pain point 가치순)

**1. Yao & Viswanathan 2024** "OCV Models Should Be Thermodynamically Consistent." *JPCL* 15, 1143. DOI 10.1021/acs.jpclett.3c03129 (오픈 PMC10839898).
- OCV 는 SOC 단조여야(2법칙). **몰 Gibbs** g=g_pure+RT(x ln x+(1−x)ln(1−x))+Σ Ωᵢ x(1−x)(1−2x)ⁱ (이상 config entropy+**Redlich–Kister** 초과)+**공통접선(Maxwell)**. miscibility gap 내 dU/dx=0 → 진짜 평탄 plateau → **dQ/dV 가 plateau 가장자리서 발산**(진짜 near-delta). LFP 는 3차 RK 만(비제약 fit 는 >10차).
- 핵심수학: 공통접선을 고정점 x*=f(x*,θ)로, **음함수정리**로 미분관통 → gradient fit, PDE·Newton추적 없음. "곡선 생성+피팅" 워크플로 부합.
- 매핑 → pain(1) near-delta + (2) 일관성(단조=아티팩트 제거); per-gallery ξ_j 를 자유E 층으로 보강/대체. 소재: **흑연·Si(Li₁₅Si₄)·LCO**.
- VERDICT: **REFLECT(최고가치).** 위험: 순수 Maxwell plateau 는 dQ/dV→∞; 실피크 유한 → **kinetic V_n/L_V broadening 과 합성 필요** — 평형(RK+공통접선)·kinetic 층 깨끗이 조합(재작성 아닌 가산). 2위험: RK 초과=소재별; 셀간 일관성은 여전히 item2/3.

**2. PyBOP — Hallett et al. 2025** *JOSS*, arXiv 2412.15859, DOI 10.21105/joss.07874. github.com/pybop-team/PyBOP.
- **PyBaMM** 모델(내장 **MSMR** 포함) 피팅, frequentist+**Bayesian**; **식별성**(Hessian·Sobol)+**사후분포**(UQ).
- 매핑 → pain(2) 단일셋 일관성 + (3) U_j,ω_j,X_j 원리적 불확실성. 자유 per-cell w_j 산포가 ill-posed/degenerate 방향 아티팩트임을 탐지·공유파라미터+prior 부과 수단.
- VERDICT: **REFLECT(식별 harness).** 위험: MSMR 다-gallery 는 진짜 trade-off; 평탄 OCV 는 약한 식별성 → 다-SOC/다-조건 목적함수 설계 필수.

**3. Hu & Schwartz 2022** *JES* 169, 030530. DOI 10.1149/1945-7111/ac5a1a. data+code Zenodo 5847378.
- **MSMR half-cell 열역학모델**을 저C 전셀데이터에 순차최소제곱 → <5mV MAE; 오픈툴.
- 매핑 → pain(2): 값싼 순환데이터서 **단일 일관 MSMR셋** 추출 레시피+코드(per-cell 자유fit 아님).
- VERDICT: **REFLECT(방법+코드).** 위험: 최소제곱 점추정 UQ 없음 → item2 와 병용.

**4. 정초 MSMR — Verbrugge, Baker, Koch, Xiao, Gu 2017** *JES* 164, E3243. DOI 10.1149/2.0341708jes; **Baker & Verbrugge 2018** *JES* 165, A3952. DOI 10.1149/2.0771816jes (Part II: 10.1149/2.0091904jes).
- 우리 모델의 원 MSMR 정의(gallery=logistic; ω_j RT/F 폭). Part I/II=**다공전극+섭동 LSV**(제1원리 유한율 피크 broadening).
- 매핑 → 평형 코어 전체 + V_n식 kinetic broadening.
- VERDICT: **REFLECT(정의 기반; 이미 우리 프레임).** 위험 없음. 흑연/LCO on-target; NMC 예시는 부수.

**5. Baker/Garrick 온도-MSMR 2024 — Paul, Wolfe, Verbrugge, Koch, Lowe, Trembly, Staser, Garrick.** Part 1: *ECS Advances* 3, 042501. DOI 10.1149/2754-2734/ad7d1c. Part II: *JES* 171, 103505. DOI 10.1149/1945-7111/ad70d9.
- 흑연 **MSMR params 를 T 함수로**(X_j·U0_j·ω_j) 피팅 → **엔트로피계수 ∂U/∂T** 재구성.
- 매핑 → pain(2) 다-**온도** 일관성, U_j(T)=(−ΔH+T·ΔS)/F ⇒ ∂U_j/∂T=ΔS_j/F 직접. "전조건 단일 물리셋" 문헌 템플릿.
- VERDICT: **REFLECT(T-일관성 템플릿).** 위험: ω_j(T) drift 허용 → 폭이 ω_j·RT/F(T 는 RT 만, ω_j 고정)인지 진짜 ω_j(T)인지 결정(아티팩트 재도입 방지).

**6. Papadopoulos et al. 2026** Si-MSMR. *EES Batteries* DOI 10.1039/D6EB00061D.
- Si MSMR — Li–Si 상별 **독립 평형전위**(수정 Nernst), 실험+atomistic; **비대칭 리튬화/탈리튬화**+상분율.
- 매핑 → 흑연+Si + pain(1)/비대칭; PDE 없이 MSMR 를 Si 확장.
- VERDICT: **TEST-FIRST.** 위험: 최신(2026), Porsche/VW; 자체 Si 데이터로 검증 후; 비대칭 경로가 파라미터↑→식별성 압박.

**7. Lu, Trimboli, Plett et al. 2021** *JES* 168, 070533. DOI 10.1149/1945-7111/ac11a4 (Part II: ...ac11a5).
- 히스토그램법+5접근으로 **"결측·비접근 리튬" 문제**(측정 half-cell→clean MSMR OCP(stoich)). 흑연 데모.
- 매핑 → pain(2): 피팅 전 **일관 OCP/stoich 정렬**(w_j 산포 숨은원인=나쁜 endpoint/stoich 정렬).
- VERDICT: **REFLECT(전처리 규율).** 위험: NMC 도 데모 — 흑연 부분이 on-target.

**8. Olson, López, Dickinson (NPL) 2023** *Chem. Mater.* 35, 1487. DOI 10.1021/acs.chemmater.2c01976.
- **dQ/dV·dV/dQ** 해석 권위가이드("square-plot" heuristic; 미분선택이 피크 왜곡).
- 매핑 → pain(d) ICA/DVA 모범, dV/dQ-vs-dQ/dV 강건성.
- VERDICT: **REFLECT(해석/강건성 레퍼런스).** 위험 없음.

**9. Karthikeyan, Sikha, White 2008** *JPS* 185, 1398. DOI 10.1016/j.jpowsour.2008.07.077.
- **Redlich–Kister 초과-Gibbs/정칙용액** 평형전위모델 for **LCO·흑연·hard carbon** — item1 이 열역학정합화하는 RK 전구체.
- 매핑 → pain(1): LCO·흑연 plateau 정칙용액 경로.
- VERDICT: **REFLECT(item1 정초 RK).** 위험: 비제약 RK 는 단조위반 — 항상 공통접선(item1)과 병용.

**10. Levi & Aurbach 1999** "Frumkin intercalation isotherm — a tool for … lithium insertion: a review." *Electrochimica Acta* 45, 167. DOI 10.1016/S0013-4686(99)00202-9.
- **Frumkin/Fowler–Guggenheim** 등온선(인력 lateral g). g<임계(⇔ **Ω>2RT**) → **S-형(van der Waals) loop** → miscibility gap; **흑연 적용**.
- 기제/수학: **우리 logistic 의 최소 일반화** — 상호작용 0 → Frumkin 이 ξ_j 로 붕괴. g 복원 → 음함수 x(V); Maxwell/공통접선이 loop 평탄화 → 진짜 두-상 plateau+near-delta dQ/dV.
- 매핑 → pain(1), ξ_j/w_j 직접.
- VERDICT: **REFLECT(개념 핵심; 최경량 fix).** 위험: 명시 ξ_j(V)→gallery별 음함수 solve(여전히 1-D root-find, PDE 아님); 오래됐으나 정초·정확히 기제.

**11. Kuhn, Adachi, Philipp, Howey, Horstmann 2026** "A Primer on Bayesian Parameter Estimation and Model Selection for Battery Simulators." *JES* 173, 120509. DOI 10.1149/1945-7111/ae73f3. arXiv 2512.10055.
- **베이지안 추정+모델선택**(prior·posterior·evidence/Occam 로 #gallery 선택) 현대 모범.
- 매핑 → pain(3) 식별성/UQ + "몇 반응 정당한가".
- VERDICT: **REFLECT(item2 방법론 근거).** 위험 없음.

**12. Beatty, Strickland, Ferreira 2024** *Energies* 17, 4309. DOI 10.3390/en17174309.
- **미분+후처리 필터**(이동평균·Gaussian·Savitzky–Golay…) ICA/DVA 체계비교, 공개데이터.
- 매핑 → pain(d) 스무딩/미분(savgol vs Gaussian).
- VERDICT: **REFLECT(미분 레시피).** 위험: SOH 지향; 필터지침만(노화결론 아님). (보완: GP 회귀 ICA=불확실밴드 보너스, PHME 2022 papers.phmsociety.org/…/4915.)

**13. Köbbing, Latz, Horstmann 2024** Si 히스테리시스 chemo-mech. *AFM* 34, 2308818. DOI 10.1002/adfm.202308818. arXiv 2305.17533. (완화동반: *ACS AMI* 2024, DOI 10.1021/acsami.4c12976 / arXiv 2408.01106.)
- **Si OCV 히스=딱딱 무기 SEI 소성변형**; SEI 점성이 율의존+완화후 gap 설명.
- 매핑 → Si 경로 + L_V(현상론적 완화의 물리기원).
- VERDICT: **TEST-FIRST.** 위험: chemo-mech(응력·SEI) — 우리 타깃보다 무거움; L_V 를 Si 용으로 *정당화/형성*만, 전면대체 X.

**14. 비평형/히스 이론(정초·LFP 예시 — off-target, 정당화로만).**
- **Dreyer et al. 2010** *Nat. Mater.* 9, 448. DOI 10.1038/nmat2730 — 다입자, **비단조 화학퍼텐셜→입자별 채움→열역학 히스**(I→0 서도 잔존).
- **Ferguson & Bazant 2012** *JES* 159, A1967. DOI 10.1149/2.048212jes / arXiv 1204.2934; **Bazant 2013** *Acc. Chem. Res.* 46, 1144. DOI 10.1021/ar300145c — 반응율=변분 화학퍼텐셜 구동력 비선형; Cahn–Hilliard 자유E→진짜 상분리.
- VERDICT: **DON'T-REFLECT(곡선생성기 변경)**(PDE/다입자=회피대상 무거운 PDE), **REFLECT(물리정당화)**(Maxwell/공통접선 plateau 가 옳은 평형극한·히스=열역학 인 이유). 위험: PDE 스코프크립.

**2차 확인(on-target 보조):**
- **Gao et al. 2023** *Applied Energy* 349, 121621. DOI 10.1016/j.apenergy.2023.121621 — Si-graphite OCP 분리. **REFLECT(Si-Gr OCP 방법).**
- **Schmitt, Schindler, Oberbauer, Jossen 2022** *JPS* 532, 231296. DOI 10.1016/j.jpowsour.2022.231296 — Si–graphite 전극밸런스/열화 via OCP. **REFLECT(우리 정확한 블렌드 전극밸런스).**
- **Paul et al. 2024** "Coal-Derived Graphite MSMR." *JES* 171, 020530. DOI 10.1149/1945-7111/ad2061 — 실 6-gallery 흑연 MSMR, **Excel Solver 최소제곱(24 params) 5.1mV**. VERDICT: **TEST-FIRST/경고** — 우리가 벗어나려는 *비제약 per-cell 비일관 fit* 의 구체 예 → "before" 기준선.
- **Garrick, Koch, Choi … Choe 2024** *JES* 171, 020520. DOI 10.1149/1945-7111/ad1d27 — MSMR **소재별 엔트로피 분해**; 흑연 음극 on-target(양극 NMC 무시). **TEST-FIRST(흑연 엔트로피계수 방법).**
- **Pilon group (Mendez…) 2022** *JPCC* 126, 8143. DOI 10.1021/acs.jpcc.1c10414 — config/vib/electronic entropy; ∂U/∂T 서 고용체 vs ordering vs 1차 두-상 구분. **REFLECT(엔트로피 해석).**
- 흑연 두-상/엔트로피 앵커: "Model of Li Intercalation into Graphite by Potentiometric Analysis" *JES* 2018, DOI 10.1149/2.1251802jes; "Shedding Light on Entropy Change Stage II→I Graphite" *JES* 2017, DOI 10.1149/2.0231701jes(2준위 **lattice-gas** config entropy); "Voltage hysteresis … meta-stable carbon stackings" *JMCA* 2021, 9, 492, DOI 10.1039/D0TA10403E. **REFLECT(흑연 plateau/엔트로피).**

## B. 교차 테마
**T1 — near-delta 를 PDE 없이 닫기(깨끗한 답).** 2 조합가능 대수경로:
- (i) **자유E+공통접선(Yao–Viswanathan/diffthermo, item1)** — g(x)=이상엔트로피+RK 초과 fit·Maxwell; plateau+발산 dQ/dV 자동·단조보장. 최경량·최일반(흑연·LCO·Si).
- (ii) **Frumkin/Fowler per-gallery(Levi–Aurbach item10·Karthikeyan–White item9)** — 기존코드 *최소*변경: ξ_j=g=0 Frumkin; 상호작용항 복원→각 gallery 가 Ω_j>2RT 서 miscibility gap. gallery 부기 유지, 음함수 site-fraction 만.
- 둘 다 "곡선생성+피팅" 영역. Bazant/Dreyer PDE(item14)는 *이유*지 생성기로 도입 X. **결정적: 평형 near-delta 를 kinetic V_n/L_V broadening 과 합성** — 평형 plateau(sharp)⊗kinetic 커널(유한폭)=현실피크. R²~0.95 천장=평형형상 한계, kinetic 층 안건드리고 제거.

**T2 — 조건무관 파라미터 일관성(산업요건).** 단일논문 없음; 문헌 조립:
- **열역학제약**(공통접선 단조, item1)으로 per-cell w_j 방황 자유도 제거.
- **명시 T-의존 단일 물리셋** U_j(T),ω_j(T)(온도-MSMR item5) 조건별 refit 아님; 엔트로피=∂U_j/∂T=ΔS_j/F.
- **전역/베이지안 식별 harness**(PyBOP item2·Hu–Schwartz item3·베이지안 primer item11)+prior/정규화+셀간 공유+**posterior 보고**(비일관 w_j 를 평탄 unidentifiable 방향으로 노출).
- **stoich/endpoint 정렬 먼저**(Lu–Trimboli–Plett item7) — 오정렬이 폭 비일관 가장.
반복 진단(2·3·11): **평탄 OCV→약한 식별성**; 일관성=다-SOC/다-조건 목적, 자유파라미터↑ 아님.

**T3 — 미분·강건성.** dV/dQ 가 평탄(near-두-상) 영역서 dQ/dV(발산)보다 강건; endpoint/전극밸런스=dV/dQ·피크식별=dQ/dV(Olson–Dickinson item8; Dahn dV/dQ 4-param 전극밸런스). 필터선택 중요(Beatty item12); GP 미분=불확실밴드 보너스.

## C. 도구/데이터/코드(확인 URL)
- **diffthermo** — github.com/BattModels/Diffthermo_OCV_paper (MIT). OCV+SOC CSV→열역학정합 OCV(RK 자유E+미분가능 공통접선); **PyBaMM(Python)+MATLAB 내보내기**. 흑연+LFP 예제. (논문=item1.) *pain1 최직접 산물.*
- **PyBaMM MSMR** — docs.pybamm.org/…/models/MSMR.html. 내장 MSMR OCV/half-cell+노트북(U0_j,X_j,ω_j). 방정식 규약 대조 레퍼런스.
- **PyBOP** — github.com/pybop-team/PyBOP. PyBaMM(MSMR 포함) 베이지안+frequentist 식별; Hessian·Sobol·posterior UQ. (논문=item2.) *pain2·3 harness.*
- **Hu&Schwartz 오픈툴+데이터** — Zenodo 5847378(item3 data+code). 전셀서 MSMR half-cell 파라미터 추정.
- **GalvAnalyze** — McNulty et al. *Batt.&Supercaps* 2023, DOI 10.1002/batt.202300038. 정전류 ICA/DVA 추출.
- **DVA freeware** — *JES* 2012, DOI 10.1149/2.013209jes.
- **Dahn dV/dQ 방법** — dal.ca/…/dV-dQ_analysis.html. 4-param(양극질량·음극질량·양극slippage·음극slippage) 전극정렬 fit.
- **LiionDB** — arXiv 2110.09879 — OCP 함수 등 연속모델 파라미터 DB, prior/초기추정.

## D. 정직 갭·제외
- **"다셀 공유 MSMR 파라미터+per-cell nuisance 항 계층 전역fit" 기성품 없음.** item2(harness)·3(전셀 전역LSQ)·5(T-의존)·11(베이지안 모델선택)서 조립 — 단일인용 아님. turnkey 논문 기대 X 플래그.
- **diffthermo(item1) 논문 검증 대부분 LFP/흑연.** Si·LCO *열거*하나 우리 특정 LCO·Si 데이터셋 fit 은 TEST-FIRST(슬로프 Si 는 plateau 불필요할수·LCO 온화 ordering 미묘).
- **Maxwell plateau→dQ/dV→∞; 실데이터 유한.** kinetic broadening 과 합성해야 완결 — 결함 아닌 필수 2단계.
- **비대칭(리튬화 vs 탈리튬화 폭):** 확인 on-target 중 2026 Si-MSMR(item6)만 정면; 비대칭-ω_j MSMR 는 신흥·미정착 확장.
- **화학 제외(hard rule 3), on-target 근거로 미계상:** Dreyer2010·Ferguson–Bazant2012·Bazant2013 + 최근 입자분포/입자내히스(Katrašnik/Gaberšček *Adv.Mater.* 2023 DOI 10.1002/adma.202210937; "Modeling Phase Separation and Hysteresis … Particle Distribution" *JES* 2026 DOI 10.1149/1945-7111/ae5fdd) = **LFP/일반** → 지명 정초 히스 이론으로만, 생성기엔 DON'T-REFLECT. "Cation Mixing … Multi-Site Multi-Reaction"(*Front.Energy Res.* 2022)=**NMC** → 전면제외.
- **불확실:** 온도-MSMR **Part II**(JES 171,103505) 제목/venue/DOI 확인·저자 Part1 팀 일치하나 전문 미개봉(유료) → 엔트로피계수 세부 2차. 여러 1차 PDF(ACS·IOP·ScienceDirect·Nature) 403/redirect; 전 사실 ≥2 독립출처 교차확인. 조작 없음.
