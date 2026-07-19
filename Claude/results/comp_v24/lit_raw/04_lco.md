# RAW — LCO 스트림 리서치 산출 (agent ab35bad7, 2026-07-19)

> 원본 보존. 전부 intrinsic O3-LiCoO₂ 상열역학(플래그 제외). 규약주의: (i)일부 고전(Ohzuku)은 Li₁₋ₓCoO₂ → "그들 x"=제거된 Li. 여기선 전부 Li **함량** x. (ii)"H1/H2" 두-상 x≈0.75–0.94=**절연체(α)–금속(β) miscibility gap**(~3.94V); "x=0.5"=**단사정 Li/vac order-disorder** split(~4.1–4.2V); "H1-3/O1"=심탈리튬 stage(~4.55/4.62V).

## A. 확인 논문 (가치순)

**1. Reynier, Graetz, Swan-Wood, Rez, Yazami, Fultz (2004)** *PRB* 70, 174304. DOI 10.1103/PhysRevB.70.174304.
- Li_xCoO₂ 삽입 엔트로피 측정(평형셀 dU/dT) 0.5<x≤1. ΔS 최대 9.0 k_B/atom 전체, 4.2 k_B/atom O3 육방영역.
- ΔS 3분해: **phonon/진동**(큼, *음* ΔS 대부분, x 거의평탄), **configurational**(Li/vac 무질서; **조성형상 지배**), **electronic**(전자구조계산: **작음**).
- 매핑 → **ΔS_rxn(∂U_j/∂T=ΔS_j/F) + ΔS_e 전자항.** 엔트로피축 최중요 논문. feature별 ΔS_rxn fit 의 실증기반, ΔS_e 직접 관련.
- VERDICT: **REFLECT(ΔS_rxn 근거)+TEST-FIRST(ΔS_e).** 위험: **전자 엔트로피가 IMT 창(0.75–0.94, 0.5–1.0 내) 서도 작다.** ΔS_e 는 *fit*(가정 X); 과대가중=config+phonon 이중계상. ΔS_e 는 작은 검증가능 보정으로.

**2. Yao & Viswanathan (2024)** *JPCL* 15(4) 1143. DOI 10.1021/acs.jpclett.3c03129 (+오픈코드).
- OCV 열역학정합 필수; 12소재(**LCO 포함**)를 8-param Redlich–Kister 초과-Gibbs 로 fit.
- 미분가능 열역학 — g(x)→μ=∂g/∂x(autodiff); **공통접선(두-상) 을 고정점**·음함수정리; OCV SOC 단조. PyBaMM 통합.
- 매핑 → **평형층 전체(U_j,w_j,Ω).** MSMR-합·RK 초과-Gibbs=동일 정칙용액 물리 2인코딩; 공통접선=우리 Ω>2RT 스위치의 엄밀판.
- VERDICT: **TEST-FIRST(방법 채용가치).** 위험: C 데이터셋 단서 — 그들 "LCO" 곡선=**O2 폴리타입**(O3 아님). *방법*(공통접선/정합) 반영, 그들 LCO 파라미터 X.

**3. Hudak, Davis, Nagasubramanian (2014)** *JES* 162(3) A315-ish. DOI 10.1149/2.0071503jes.
- 실 O3-LCO half-cell **OCV+dE/dT(엔트로피) vs SOC**. 3영역: (i)x≈0.95–0.83 평탄 dE/dT=1차 금속↔반도체 두-상; (ii)x≈0.83–0.6 단조상승=lattice-gas 랜덤삽입; (iii)x≈0.6–0.49 육방→단사 order-disorder 특유 **"틸데"(x≈0.5 국소max 옆 국소min)**.
- 형상=configurational entropy(Reynier 인용: 전자 무시, 진동 작음).
- 매핑 → **x=0.5 feature U_j·ΔS_j; 두-상영역 x≈0.83–0.95.** 틸데=x=0.5 order-disorder 피크의 엔트로피 지문.
- VERDICT: **REFLECT(디지타이즈 실 dU/dT 로 ΔS_j fit).** 위험: 코인셀 분극이 두-상 plateau 근처 dE/dT 오염; 평형점만 디지타이즈.

**4. Ménétrier, Saadoune, Levasseur, Delmas (1999)** *J. Mater. Chem.* 9, 1135. DOI 10.1039/a900016j.
- Li_xCoO₂(0.5≤x≤1) 전도도+열전능+⁷Li NMR → 점진 국소→비국소 전자; **절연체–금속 전이가 x 0.75–0.94 biphasic(두-상) 도메인의 *구동력***.
- 전자(Mott형) 전이가 금속상 자유E 낮춤 → miscibility gap.
- 매핑 → **~3.94V 두-상 feature 물리기원 + 전자엔트로피항 *근거*.** LCO 가 왜 거기 step 있는지의 인용.
- VERDICT: **REFLECT(H1/H2 gap 물리근거).** 위험: 엔탈피/자유E 전자구동 정당화지 큰 ΔS_e 아님 — Reynier 와 병용(혼동 X).

**5. Flores, Mozhzhukhina, Aschauer, Berg (2021)** *ACS AMI* 13(19). DOI 10.1021/acsami.1c04383 (+ChemRxiv 10.26434/chemrxiv.14113109).
- operando Raman+DFT of IMT: **Mott-절연체 α상 x>0.87 → 금속 β상 x→0.75.** 결정적: **두-상 경로는 극저율서만; ~20mA/g(~C/10) 위서 kinetic 억제되어 고용체 경로.** 고율서 히스 좁아짐.
- 율제어 nucleation(두-상) vs 단일상(고용체) 경쟁.
- 매핑 → **평형 Ω-스위치와 kinetics(V_n,R_n,L_V) 결합.** 우리 "Ω>2RT⇒near-delta"=*저율극한만*; 실율서 같은 feature 가 **kinetic**(열역학 아님) 으로 broaden.
- VERDICT: **TEST-FIRST(중요 뉘앙스).** 위험: 3.94V 폭 전부를 열역학 w_j 로=율시리즈 오fit. R_n/L_V 가 율의존 broadening 흡수; w_j(Ω)=평형 envelope.

**6. Reimers & Dahn (1992)** *JES* 139, 2091. DOI 10.1149/1.2221184. *(필수 고전)*
- 정본 고정밀 V(x)+in-situ XRD. x:1→0.4 **3전이** — **1차 두-상 0.75≤x≤0.93**, **x=1/2 브래킷 2 order-disorder**(단사왜곡 a=4.865,b=2.806,c=14.420Å,β=90.77°).
- 매핑 → **U_j 중심 + feature별 두-상/고용체 분류.** x=0.5 지문=*두* 근접 narrow 피크(하나 아님).
- VERDICT: **REFLECT(feature topology 정의).** 위험: 물리 없음, 해상만 — x=0.5 doublet 렌더에 ≥2 반응 필요.

**7. Teichert, Das, Aykol, Gopal, Gavini, Garikipati (2021)** arXiv:2104.08318; 출판 (2024) *J. Mech. Phys. Solids* DOI via S0022509624001923.
- DFT+적분가능 심층신경망 → **Li_xCoO₂ 자유E(조성/온도)**; **x=0.5 order-disorder** phase-field(반위상경계·계면E 계산).
- IDNN 이 MC/cluster-expansion 서 μ(x) 학습, 해석적분→g(x); order-disorder=자유E landscape feature.
- 매핑 → **x=0.5 피크 w_j/ω_j·Ω + T-의존 자유E 경로.** 우리 w_j 인코딩 정칙용액/lattice-gas 의 현대유도.
- VERDICT: **TEST-FIRST(물리레퍼런스, drop-in 아님).** 위험: 전장 자유E 가 파라미터 MSMR 보다 무거움; U_j(T)/w_j(T) *검산*용, 폐형 대체 X.

**8. Motohashi et al. (2009)** *PRB* 80, 165114. DOI 10.1103/PhysRevB.80.165114 (arXiv:0909.3556).
- 0<x<1 전자상도: 자기/전자 임계점 **x≈0.35–0.40**; 전하정렬 이상 **x=0.5·0.67**(~175K).
- 매핑 → ΔS_e·x=0.5 넘어 feature 의 전자구조 맥락. 탈리튬시 전자엔트로피 비영 확인.
- VERDICT: **TEST-FIRST/맥락.** 위험: 자기전이 극저온(≪실온); 실온 dU/dT 에 문자적 도입 X — 금속측 전자엔트로피 보유 증거로만.

**9. Ohnishi, Mitsuishi, Takada (2021)** *ACS AEM* 4(9). DOI 10.1021/acsaem.1c03046.
- 박막 전고체 LCO in-situ XRD+EIS: **O3→H1-3(~4.5V,x≈0.3) 이 전극저항 급증과 상관.**
- 매핑 → **분극 R_n(및 SOC 의존).** R_n 비상수 직접증거 — 고전압 상전이서 spike.
- VERDICT: **TEST-FIRST.** 위험: 박막/고체전해질 측정; 크기 다공액체셀 미이전, 단 *정성 SOC-의존 R_n(x)* 는 >4.4V fit 시 인코딩 가치.

**10. Kim, Park, Kwon … Yazami, Choi (2020)** *EES* 13, 286. DOI 10.1039/c9ee02964h.
- LCO(+Ni도핑) "entropymetry": dS vs SOC 피크가 구조이질성/order-disorder 추적; crack 유발 XRD broadening 과 엔트로피 broadening.
- 매핑 → ΔS_j·x=0.5 order-disorder 피크의 순환/이질성 w_j broadening.
- VERDICT: **TEST-FIRST.** 위험: Ni도핑=범위밖; pristine-LCO 곡선만.

**11. Xia, Lu, Meng, Ceder (2007)** *JES* 154, A337. DOI 10.1149/1.2509021. *(고전, 고전압)*
- LCO 박막 4.2–4.9V: dQ/dV plateau **~4.55·4.62V=O3→H1-3→O1 staging.**
- 매핑 → 심탈리튬 feature U_j(>4.4V 확장시).
- VERDICT: **TEST-FIRST(>4.5V 모델시만).** 위험: 비가역/산소손실 영역 — 위치 drift; 가역평형 fit X.

**12. Ohzuku & Ueda (1994)** *JES* 141, 2972. DOI 10.1149/1.2059267. *(필수 고전)*
- 정본 4V 고체 redox 맵: 만충근처 두-상, 단일상 0.25<x<0.75, x=0.5 단사 order.
- 매핑 → Reimers-Dahn 동일(feature topology/U_j).
- VERDICT: **REFLECT(정본 인용).** 위험: Li₁₋ₓ 규약 — 주의변환.

**13. Li, Sun, Gao, Zhang, Lu, Lu (2022)** *PNAS* 119(20) e2120060119. DOI 10.1073/pnas.2120060119.
- in-situ XRD+STEM: "고용체" 영역이 실은 **CoO₆ slab 집단 준연속 glide**; "고용체" 는 과단순 라벨.
- 매핑 → 우리 Ω<2RT "broad=고용체" 가정. 물리적으로 broad 영역=glide 매개, 이상혼합 아님.
- VERDICT: **DON'T-REFLECT(기제, 형상불변).** 위험: 흥미롭지만 dQ/dV *형상* 예측 불변; 산문서 "고용체" 과claim 방지.

**14. Barcellona, Codecasa, Colnago (2024)** *Energies* 17(20) 5137. DOI 10.3390/en17205137. *(오픈)*
- 경험적 **double-Gaussian** q(V_eq) fit LCO 셀 OCV 10–50℃(R²>0.997); 2 param T-다항.
- 매핑 → MSMR sum-of-peaks 의 현상론 사촌(2-Gaussian≈2-반응 dQ/dV). *열역학/엔트로피 근거 없음*; x=0.5·H1/H2 구조 없음.
- VERDICT: **DON'T-REFLECT(물리)/데이터만.** 위험: 전 상용 LCO/graphite 셀 → OCV 음극합성(C 참조).

*보조 고전(배경):* **Van der Ven, Aydinol, Ceder, Kresse, Hafner (1998)** *PRB* 58, 2975 — 제1원리 Li_xCoO₂ 상안정성/configurational 열역학(Ω·정렬 기저상의 DFT 뿌리). **Mercer, Finnigan, Kramer, Richards, Hoster (2017)** *Electrochim. Acta* 241, 141 — 점결함이 order-disorder 엔트로피 피크 흐리는 lattice-gas MC(방법, LCO특이 아님).

## B. 교차 테마
1. **세 물리적 구분 dQ/dV feature, 세 다른 물리** — 단일기제 X:
   - **~3.94V(x≈0.75–0.94):** 절연체→금속 **두-상** gap. 구동=전자(Mott)(Ménétrier); 엔트로피는 여전히 config 지배(Reynier). → 평형서 near-delta w_j, 단 #3.
   - **~4.1–4.2V(x≈0.5):** 단사 **order-disorder doublet**(Reimers-Dahn·Ohzuku·Teichert). → 2 narrow 반응; 엔트로피 "틸데"(Hudak).
   - **~4.55/4.62V(x≈0.3–0.2):** **H1-3/O1 staging**, 부분 비가역(Xia·Ohnishi).
2. **전자엔트로피 기원은 실재, 크기는 작음.** Ménétrier/Motohashi 가 전자항 *보유* 정당화; Reynier/Hudak 은 측정 전자*엔트로피* 가 config+phonon 대비 작음. ΔS_e 합의: **유지하되 작게 fit·TEST-FIRST**, 지배 dU/dT step 절대 아님.
3. **"두-상 vs 고용체"는 율의존, 순열역학 아님(Flores 2021).** 평형 Ω-기준=*저율* envelope; 유한율 피크 broadening=**kinetics**(R_n,L_V). 열역학↔kinetic 모듈 최청정 링크.
4. **열역학정합이 분야표준화**(Yao–Viswanathan; 공통접선/단조). MSMR 이미 만족; sum-of-sigmoid 현대정당화로 인용가능·원하면 두-상 feature 에 공통접선 solve 채용.
5. **현대 DFT/ML 자유E 파이프라인(Teichert; cluster-expansion+베이지안opt)이 동일 정칙용액 물리 재현** — U_j(T),w_j(T),x=0.5 ordering 온도의 독립 검산.

## C. 공개 데이터 — 실 fittable LCO(고우선) URL
**최선 실fittable+정합모델:**
- **diffthermo repo(Yao–Viswanathan):** https://github.com/BattModels/Diffthermo_OCV_paper → `data_for_manuscripts/RK_fit_JPCL_Jan2024/LCO/8_RK_params`. **디지타이즈 LCO 방전 OCV CSV+8-param RK fit.** **경고(중요):** 폴더 출처=**JES 10.1149/1.1503075 Fig.4a**=**Carlier, Saadoune … Delmas (2002) "Li Electrochemical Deintercalation from O2-LiCoO₂"** = **O2 폴리타입**(우리 O3 아님). O2 는 다른 ordering·동일 3.94V plateau 없음. *방법/템플릿*으로만, **폴리타입 확인 후 O3 ground truth 취급.**

**디지타이즈 실 O3-LCO(DOI 그림 — 정직 1차경로):**
- **Reynier 2004**(10.1103/PhysRevB.70.174304): O3-LCO **dU/dT vs x, 0.5<x≤1** — ΔS_j fit 직접 주는 유일 공개원.
- **Hudak 2014**(10.1149/2.0071503jes): O3-LCO half-cell **OCV+dE/dT vs SOC** 전범위 incl x=0.5 틸데.
- **Reimers & Dahn 1992**(10.1149/1.2221184)·**Ohzuku & Ueda 1994**(10.1149/1.2059267): 정본 O3-LCO **V(x)** 상라벨.
- **Barcellona 2024**(10.3390/en17205137, MDPI 오픈 CC-BY): 다온도(10–50℃) OCV — 단 **전 LCO/graphite 상용셀**(음극합성; half-cell 아님). T-의존 검산용, 양극 U_j 분리엔 부적.

**파라미터 DB(문헌유래, raw 아님):**
- **LiionDB** — https://www.liiondb.com · https://github.com/ndrewwang/liiondb (Wang, O'Kane, Brosa Planella et al. 2022 *Prog. Energy* DOI 10.1088/2516-1083/ac692c; **MIT**, PostgreSQL/Colab). 문헌 OCP/파라미터 집성; **LCO OCP 존재 plausible 하나 랜딩서 특정 LCO 항목 미확인 — 직접쿼리**(material=LiCoO₂, parameter=OCP/entropy).
- **PyBaMM LCO**(현 프록시): `Ramadass2004` 셋 LCO OCP → **Zhao et al. 2018 JES 165(13) A3169** = **해석fit**(Marquis2019 프록시 동류, 독립1차 아님).

**LCO 명시제외 셋(시간낭비 방지):**
- Zenodo **20086298**(Flores 2026 half-cell OCV GITT/p-OCV) — 흑연·Si·LNMO·LFP·NMC111·NMC532; **LCO 없음.** https://zenodo.org/records/20086298
- **Argonne CAMP**(https://acdc.alcf.anl.gov/mdf/detail/camp_2023_v3.5/) — NMC 계·HE5050·5V-spinel; **LCO 없음.**
- Battery Archive(batteryarchive.org) — 대부분 전 상용셀, half-cell 양극 OCV 아님.

## D. 정직 갭·제외
**갭(실상):**
- **clean 오픈 1차 O3-LCO *half-cell* GITT/저율-dQ-dV 셋이 현대 repo(Zenodo/CAMP/BatteryArchive) 에 없음.** "실 fittable O3-LCO" 현실경로=**DOI 그림 디지타이즈**(Reynier2004 엔트로피; Hudak2014/Reimers-Dahn1992 OCV) — "DOI 있는 디지타이즈 그림" 허용 하 정당.
- **ΔS_e 항이 최소실증:** 최선측정(Reynier2004)=전자엔트로피 *작음*. ΔS_e 를 fit·bound 보정으로 강등·Reynier/Hudak dU/dT 대조 후 신뢰 권장.
- **두-상 feature 율의존(Flores2021)** 이 현 평형스위치에 미모델 — 열역학↔kinetic 층 결합 갭.

**제외(범위밖 — 코팅/도핑/구조공학, intrinsic 열역학 아님):**
- Zan et al. 2024 *Small Science*(O3→O2 고전압; 10.1002/smsc.202400162); "High-entropy doping high-V LCO"(*JPS* 2024 S0378775324016781); Mg/F 공도핑(S2468606923000692); 표면부동태(*Nat.Commun.* 2018 s41467-018-07296-6); figshare "표면개질 LCO/Li-vac ordering" — 전부 코팅/도핑.
- 검색 표출 NMC/NCA/LFP/spinel/Na/전고체 전부.

**불확실(플래그, 미의존):**
- **arXiv:1201.2248** "Electronic phase diagram of Li_xCoO₂ revisited … single crystals" — 실 preprint(안정상 x≈0.87,0.72,0.53,0.50,0.43,0.33; AFM x≈0.87&0.50), 저널판 미확인 → arXiv 인용.
- **PRM 7, 115402 (2023)** "Structural changes in LCO … cluster expansion+Bayesian opt" — 제목/venue 검색표출, 내용 미독립fetch → lead, 인용전 확인.
- Van der Ven 1998·Mercer 2017 — 완전인용 검색표출, abstract 미개별fetch; 확립됨, 배경 열거.

**이월 2 매핑주의:** (1)diffthermo "LCO"=**O2 폴리타입**(O3 사용전 확인); (2)Ohzuku **Li₁₋ₓ** 규약=우리 Li-함량 x 축반전.
