# RAW — 흑연 스트림 리서치 산출 (agent a73cec48, 2026-07-19)

> 원본 보존. 검증: WebSearch+WebFetch(CrossRef/Semantic Scholar 저자·DOI). 매핑=MSMR 모델(Σ Q_j ξ_j(1−ξ_j)/w_j, w_j=ω_j·RT/F, ∂U_j/∂T=ΔS_j/F, XRD 4전이, stage-2L, Ω>2RT).

## A. 확인 논문 (가치순)

**1. Paul, Wolfe, Verbrugge, Koch, Lowe, Trembly, Staser, Garrick (2024)** *JES* 171(10) 103505. DOI 10.1149/1945-7111/ad70d9.
- MSMR 온도 파라미터화 Part II — 5-gallery MCMB 흑연 params + 엔트로피계수 dU_j/dT@25℃.
- U_j⁰={0.289,0.211,0.132,0.126,0.089}V; X_j={0.083,0.061,0.307,0.179,0.368}; ω_j={4.249,0.112,0.826,0.090,0.113}; dU_j/dT={+1.388,+0.011,−0.142,−0.218,−0.015}×10⁻³ V/℃.
- 매핑 → **U_j, ω_j(=w_j), ΔS_j=F·dU_j/dT 직접 시드(gallery별)**. ΔS_j 최강 외부앵커.
- VERDICT: **REFLECT**(시드/검증). 위험: MCMB≠임의흑연; gallery별≠전이별; gallery-2/5 dU/dT(~1e−5) 측정노이즈. **ω_1=4.25(넓은 dilute) vs ω_4=0.09(near-delta) = 우리 고용체↔두-상 대비가 ω 로 표현됨.**

**2. Paul, Magee, Wilczewski … Garrick (2024)** *JES* 171(2) 020507-region. DOI 10.1149/1945-7111/ad2061.
- 상용+석탄유래 흑연 MSMR; 6 gallery; 전위오차 5.1mV.
- 상용흑연: U_j⁰={0.3329,0.2098,0.1281,0.1263,0.0886,0.0888}V; X_j={0.0723,0.0846,0.3253,0.1590,0.2600,0.0987}; ω_j={3.9609,0.2425,0.6571,0.0860,0.1598,0.0469}.
- 매핑 → **U_j,X_j,ω_j 2차 독립시드**. gallery 쌍: G3≈G4(0.128/0.126)·G5≈G6(0.0886/0.0888) = 각 주전이가 **분리 doublet** = 우리 stage-2L 45℃ split 과 같은 현상.
- VERDICT: **REFLECT**(시드+sub-peak split 지지). 위험: 6 gallery vs 우리 4전이; doublet 이 피팅 degeneracy 일 수도 → 데이터서 식별성 TEST 후 채용.

**3. Koch, Gao, Taha, Garrick (2026)** *JES* 173(2) 023504. DOI 10.1149/1945-7111/ae352a. (2026-01 최신)
- 분리막장착 기준전극으로 흑연단독 dU/dT vs SOL 디컨볼브.
- +0.3mV/K@저SOL(220mV plateau 위)→<0.1mV/K@plateau→**음, ~−0.2mV/K 최소@"liquid-like"(stage-2L)**→88mV plateau 접근시 급상승.
- 매핑 → **실측 ΔS(x)=F·dU/dT 로 ΔS_j 부호패턴·T-split 검증/시드**; 음의 dip 이 stage-2L 국소 = 엔트로피안정화 2L 정합.
- VERDICT: **REFLECT**(ΔS 프로파일 형상 검증타깃). 위험: 기준전극 아티팩트 전이서 최악(공지); 절대값 셀특이 → 형상만.

**4. Cordoba, Chandesris, Plapp (2024)** arXiv:2401.13108 (다층 Cahn–Hilliard; PRE 판본 언급되나 미확인 → arXiv id 인용).
- 평균장 다층 자유E fit → 명시 상호작용E; 1′→3→2→1 공존서열.
- **Ω_a(면내)=64.3meV; Ω_b(1차 층간)=23.1meV; Ω_c(2차 층간)=4.1meV**; κ=3×10⁻⁶ J/m. **64.3meV≈2.5·RT(298)** (RT=25.7meV) → **>2RT ⇒ miscibility gap**.
- 매핑 → **우리 Ω>2RT 기준의 유일 구체 수치앵커**: Ω_a 가 2RT 바로 위 = 면내 ordering 이 near-delta dQ/dV 구동하는 영역.
- VERDICT: **REFLECT**(Ω>2RT 임계 실수치 근거; Ω_a≈2.5RT). 위험(중요): 이 Ω 는 staging 재현 *fit* 값(독립 아님); 부호규약이 면내항을 상분리로 처리하나 DFT(6)는 면내 bare 쌍상호작용을 *반발*로 봄. Ω_a 는 유효 평균장 파라미터로만, 쌍결합E 로 혼동 X. stage-4·2L 붕괴(1′/3/2/1만) → 전이수 과소해상.

**5. Rykner & Chandesris (2022)** *JPCC* 126(12) 5457. DOI 10.1021/acs.jpcc.1c10800.
- 평균장 자유E(면내+층간)+**stacking 순서파라미터**로 liquid-like **2L 을 stage 2 서 형식 구분**.
- 매핑 → **stage-2L 을 엔트로피/stacking-안정화 자체 전이로 취급하는 물리근거**(우리 3↔2L·2L↔2), 피팅편의 아님.
- VERDICT: **TEST-FIRST**(구조수준). 위험: logistic-합 형식에 없는 stacking 순서파라미터 도입; 물리반영=결합추가(구조변경)→Ch1 전하보존 정합 게이트.

**6. Pande & Viswanathan (2018)** *PRM* 2, 125401. arXiv:1607.05658.
- 고정밀 BEEF-vdW DFT+Ising 상도, phonon+configurational entropy; ~13 안정상 stage 4→3→2→1.
- 면내 쌍: **J_i1=0.41eV(최근접, 지배, ∝1/r), J_i2..4=0.11/0.10/0.01eV; 층간 J_o≤0.03eV**; config entropy≈0.02eV(x<0.25),≪0.01(x>0.25); 상도 **T-무관 −25→50℃**(최종 plateau 0.01V만 이동).
- 매핑 → **면내≫층간 결합**·두-상 plateau 가 T-강건 → 우리 T-효과는 plateau 존재 아닌 **ΔS_j 피크분리**로 진입해야.
- VERDICT: **TEST-FIRST**(Ω-매핑). 위험(치명): 면내 bare 상호작용 **반발→ordering/초격자, 상분리 아님**. 우리 정칙용액 Ω>2RT 는 유효 *인력* Ω → 0.41eV 를 Ω 로 대입 X. 유효 상분리 Ω 는 창발(탄성+staging), Cordoba 64meV 에 가까움.

**7. Fujimoto et al. (2022)** *JES* 169(7) 070529-region. DOI 10.1149/1945-7111/ac7e77.
- operando 싱크로트론 XRD+정밀 C/250 → **9 환원피크(A–I)** incl dilute 8→7→6→5.
- 배정: A(0.19–0.21V,stage8-5)·B(~0.162V,stage4 LiC36)·C/D(stage3 LiC27)·E(stage2L)·F(stage2 LiC12)·G/H/I(0.05–0.08V,2→1 via 초격자). **2L 을 "큰 층간 stage 2"(공존 LiC9+LiC6 초격자), 액체 아님 으로 재해석.**
- 매핑 → **우리 4전이 개수·2L 정의 직접 검증.** 1′↔4 아래 dilute 서브스테이지(8-4) 추가.
- VERDICT: **TEST-FIRST**(핵심 XRD 근거). 위험: 9피크는 C/250 서만; 실율서 병합 → 우리 4전이가 옳은 coarse-graining 일 수. 단 2L "큰층간 초격자"(vs "액체") 는 엔트로피안정화 2L 언어와 조율 필요(P3-1 명명정합).

**8. Takagi, Shimoda, Haruyama … Abe (2023)** *Carbon* 215, 118414. DOI 10.1016/j.carbon.2023.118414.
- 동시 operando 중성자+싱크로트론 → 탈리튬화서 **ab면(면내) ordering 을 c축 staging 서 분리**.
- LiC6형→LiC9형 배열 전이 near LiC18, stage 수와 독립 추적.
- 매핑 → 단일 logistic 이 w_j 하나로 접는 **면내 ordering 성분** 근거; 전이를 면내 vs stage 로 분할 지지.
- VERDICT: **TEST-FIRST/부분REFLECT**. 위험: 탈리튬화(히스영향); 구조만; 면내/stage 분할=전이 배가→Ch1↔Ch5 정합 필요.

**9. Didier, Pang, Guo, Schmid, Peterson (2020)** *Chem. Mater.* 32(6). DOI 10.1021/acs.chemmater.9b05145.
- operando 중성자회절 → **"간헐적 무질서"**: 격자가 ordered stage 사이 disordered 창 통과(전구간 clean 두-상 아님).
- 매핑 → 이진 두-상/고용체 기준 뉘앙스: 전이 *가장자리*가 무질서(broadening) 보유.
- VERDICT: **TEST-FIRST**(피크형상 뉘앙스). 위험: 해석의존; near-delta 위 작은 고용체 broadening → w_j 하한 동기부여 가능하나 과적합 X.

**10. Takagi, Shimoda, Kiuchi, Hase, Ogumi, Abe (2025)** *Carbon* (2025) PII S0008622325002209.
- 고율(5C)서 **stage 4·6 kinetic 우회**; 탈리튬화 1→2→3→8; 전극내 불균일서 다상공존.
- 매핑 → **KINETICS층 직접증거**(율의존 staging, V_n+causal-memory lag): *방문 stage 집합* 자체 율의존.
- VERDICT: **TEST-FIRST**(kinetic broadening/shift). 위험: 여기 효과는 전극수준 공간불균일(단입자 kinetics 아님); L_V lag 는 shift/broaden 잡으나 stage-skip 못함 — 우회 재현 주장 X.

**11. Mercer, Otero, Ferrer-Huerta … Leiva (2019)** *Electrochimica Acta* 324, 134774. DOI 10.1016/j.electacta.2019.134774.
- **희박점유(0<x<0.1) 전이**를 고차 staging 과 별개 기제로; 비선형 Li–host 상호작용.
- x<0.05 급 dV + x≈0.07 plateau 를 농도의존(비상수) 상호작용항으로 재현.
- 매핑 → 우리 **stage 1′↔4 dilute 영역**(최약근거); U_j/w_j 가 저x서 단일 logistic 아닌 농도의존 보정 필요 시사.
- VERDICT: **REFLECT/TEST-FIRST**(dilute). 위험: 한 전이에 비-logistic 도입→균일 Σ logistic 깨짐; 전하보존 불안정 없이 fit 개선하는지 검증(P3-2).

**12. Persson, Hinuma, Meng, Van der Ven, Ceder (2010)** *PRB* 82, 125416. DOI 10.1103/PhysRevB.82.125416.
- 정본 DFT cluster-expansion; **쌍상호작용만으로** 기저상 재현; vdW 필수; staging+전압 재현.
- 매핑 → **쌍(정칙용액형) 해밀토니안 충분** 이론근거 = 우리 Ω 두-상 기준 제1원리 발판.
- VERDICT: **REFLECT**(쌍/정칙용액 형식 정당화). 위험: 오래됨; 상호작용 위상만, 임계용 Ω-in-RT 수치 아님.

**13. Reynier, Yazami, Fultz (2003)** *JPS* 119–121, 850. DOI 10.1016/S0378-7753(03)00285-4.
- 정초 측정 ΔS(x)·ΔH(x); 엔트로피가 plateau+**stage 2↔1 서 급 anomaly**.
- 매핑 → **ΔS_j 검증타깃** + ∂U_j/∂T 부호변화 물리기원.
- VERDICT: **REFLECT**(검증). 위험: 오래됨; 절대 ΔS 흑연특이 → 추세/anomaly 위치. (동반 Reynier JES 2004 DOI 10.1149/1.1646152 존재하나 2003 JPS 검증함.)

**14. Haruyama, Takagi, Shimoda … (2021)** *JPCC* 125(51) 27891. DOI 10.1021/acs.jpcc.1c08992.
- 제1원리 자유E, **진동+configurational entropy** 8 stage/stacking.
- 진동+config < −20meV/Li_xC6 for 0≤x≤1/3.
- 매핑 → 저-중 x 에서 ΔS_j 공급 **엔트로피 크기** 한정; 전기화학 ΔS(1,3,13) 보완.
- VERDICT: **TEST-FIRST**(ΔS 근거). 위험: 값 작고 x범위 제한; DFT entropy≠전위측정 entropy(기준 다름).

**15. Hu & Schwartz (2022)** *JES* 169(3) 030539. DOI 10.1149/1945-7111/ac5a1a.
- 전셀 OCV/dV서 전하보존제약으로 half-cell MSMR params 추출; **오픈 Jupyter(GitHub+Zenodo)**; bootstrap(500) 강건성.
- Verbrugge 시드, U_j⁰ ±20mV·X_j/ω_j ±25% bound, SLSQP.
- 매핑 → **셀간 fit 일관성(산업사용) 직접**; bounded·seeded·전하보존제약 프로토콜 템플릿.
- VERDICT: **REFLECT**(셀간 일관성 방법론+벤치마크 오픈코드). 위험: 전셀 디컨볼브 가정; 새 흑연 params 아닌 방법+코드.

**16. Wang, Gong, Li, Xiao, Li (2025)** arXiv:2508.06156.
- ML-potential MD staging; 삽입/탈리 간 **근본 kinetic 비대칭**(층 sliding/재구성).
- 매핑 → causal-memory lag L_V + charge/discharge 비대칭 지지.
- VERDICT: **TEST-FIRST**. 위험: preprint 미심사; 정성적, 이전가능 파라미터 없음.

**17. Gavilán-Arriazu et al. (2025)** *Entropy* 27(7) 663. DOI 10.3390/e27070663.
- 격자 kMC 정전류(Butler–Volmer) V–SoC; 현 구현 Langmuir(비상호작용→상전이 없음).
- VERDICT: **DON'T-REFLECT(아직)**. 위험: 상호작용 없이 staging 피크 불가; 상호작용 해밀토니안 추가 후에만.

**18. Han et al. (2025)** arXiv:2509.21047.
- operando 광학현미경+random-field Ising; dilute stage 를 micron avalanche(Barkhausen)로.
- VERDICT: **DON'T-REFLECT**(맥락만). 위험: 단입자 stochastic, 연속 dQ/dV 커널 경로 없음.

**19. Azizi, Groß, Euchner (2025)** *ACS AMI* 17(23) 33965. DOI 10.1021/acsami.5c04287.
- 희박 알칼리 삽입 DFT; **Li 삽입E≈상수 −0.2eV(희박 전영역), 층왜곡 최소**(K 는 희박서 불안정).
- 매핑 → Li **dilute 를 near-ideal/약상호작용**으로 취급 지지(Mercer(11) 비선형항과 긴장).
- VERDICT: **TEST-FIRST**(dilute 물리체크). 위험: Li/Na/K 비교 — Na/K 범위밖, Li 결과만.

**20. Wang, Gao, Liu, Liao, Wang, He (2024)** *Small Methods* 8(3) 2301084. DOI 10.1002/smtd.202301084.
- operando XRD 흑연(NCM811/graphite 셀); 율의존 전극-SOC vs 셀-SOC 불일치·완화.
- VERDICT: **DON'T-REFLECT**(전셀·양극결합; half-cell 모델엔 간접). kinetics 맥락만.

## B. 교차 테마
- **현대 staging 서열 합의:** dilute 1′(L)→4(L)→3(L)→2L→2→1, "L"=면내무질서 채운 gallery(Fujimoto2022·Takagi2023/2025·이중층흑연 Nat.Commun.2024 DOI 10.1038/s41467-024-51196-x·Dahn1991). **우리 4전이(1′↔4·3↔2L·2L↔2·2↔1)=방어가능 coarse-graining**, 단 준평형 XRD 는 1전이 아래 dilute 서브스테이지(8–4) 추가해상.
- **stage-2L 실재하나 성격 논쟁:** 고전 "액체" vs Fujimoto "큰층간 stage2/공존초격자" vs Rykner–Chandesris "엔트로피/stacking-order 안정화 중간상". **엔트로피안정화 해석 지지** = 2L 국소 음 ΔS dip(Koch2026·Reynier2003·Paul2024).
- **면내≫층간 결합**(Persson2010·Pande2018: 0.41 vs ≤0.03eV). 피크 sharpness=면내 ordering; staging=어느 plateau 존재.
- **유효 상분리 Ω≈2–2.5RT** 가 우리 Ω>2RT 임계를 위서 bracket(Cordoba Ω_a=64.3meV≈2.5RT); 면내 bare 는 반발 → **우리 기준 Ω 는 창발 유효 파라미터, DFT 결합E 아님** — 모델 무결성 최중요 단서.
- **엔트로피 부호패턴 재현가능:** ΔS>0 dilute→~0/음 plateau→2↔1 급 anomaly·2L dip(Reynier2003·Paul2024·Koch2026). 다출처 ∂U_j/∂T 타깃.
- **삽입/탈리 kinetic 비대칭**+**율의존 stage 우회** 현재 잘 문서화(Takagi2025·Wang MLP2025·Fujimoto2022) — V_n+causal-memory lag 지지, 단 실계는 stage *skip* 도(shift/broaden 넘어).

## C. 공개 데이터 (흑연 half-cell OCV/GITT/dQ-dV)
- **Zenodo 20086298** — 다소재 pseudo-OCV vs GITT incl 흑연. https://zenodo.org/records/20086298 . OCV→dQ/dV 직접; 프로토콜(GITT vs pseudo-OCV) 민감도로 U_j/ω_j 테스트.
- **Zenodo 10.5281/zenodo.15470746** — 흑연/LNMO 1Ah, 전극수준 GITT+quasi-OCV+율성능, Battery Data Format(청사진 arXiv:2601.10507). 흑연전극 OCV/GITT half-cell식 피팅 가능.
- **Hu&Schwartz MSMR 툴** — 오픈 Jupyter+예제데이터(GitHub+Zenodo, DOI 10.1149/1945-7111/ac5a1a). bootstrap CI 있는 MSMR dQ/dV 피팅 레퍼런스 — 우리 피터·일관성 프로토콜 벤치마크.
- **LiionDB** (liiondb.com; arXiv:2110.09879) — MSMR/흑연 OCV 파라미터셋+출처추적.
- **PyBaMM MSMR example** — 기본 흑연 MSMR gallery 파라미터; U_j/X_j/ω_j 규약 교차확인(동일 logistic).

## D. 정직 갭·제외
**진짜 갭:**
- **흑연 dQ/dV 용 logistic-초과 비대칭 폐형커널을 제안한 최근논문 없음.** charge/discharge·kinetic 비대칭은 문서화(Takagi2025·Wang2025·Didier2020) 되나 ξ(1−ξ) 대체 권장 비대칭 형상 미발표 → 비대칭 원하면 *창시*(skew-logistic/disorder-convolved logistic), 문헌형식 채용 아님. 변경시 TEST-FIRST.
- **흑연 정칙용액 Ω 의 독립(비-fit) RT단위 측정 없음.** 최선 앵커=Cordoba 평균장(Ω_a≈2.5RT). Ω>2RT 임계 이론건전(Persson 쌍 정당화)하나 전이별 제1원리 Ω-값 교차확인 부재.
- **dilute 영역 긴장:** Mercer2019(비선형 Li-host, 비상수) vs Azizi2025(Li 삽입E≈상수 −0.2eV). 1′↔4 형상 지배자 미해결 → dilute 보정 하드코딩 전 해소.

**불확실/제외:**
- **Schmitt et al. (2022)** "Understanding the Influence of Temperature on Phase Evolution… Operando XRD," *ChemElectroChem* 9, DOI 10.1002/celc.202101342 — 제목/venue/DOI 검색확인, 전문 HTTP402(유료) → 정량 온도계수 주장 **미검증**. 실논문·findings 미검증 → lead 로만.
- **Cordoba 2024 저널판:** arXiv:2401.13108 확인; 2차 스니펫이 PRE 2024 주장하나 저널판 미확인 → arXiv id 인용.
- **Oka et al., *JPS* 482, 228926 (2021), DOI 10.1016/j.jpowsour.2020.228926** — 실재확인이나 330℃ 열안정성(stage-1/2 격자misfit 4.58%→1.43%), 25–45℃ 전기화학 피크분리 아님 → off-target 제외.
- **Hölderle 2024** *Batt.&Supercaps* DOI 10.1002/batt.202300499 + **Strobl 2025** *AEM* DOI 10.1002/aenm.202405238(=arXiv 2411.08476) — 실재확인이나 전극/열 스케일, 단입자 평형+kinetics 범위밖 → 저직접가치 제외.
- 범위규칙 제외(Na/K/전고체): K-GIC staging, Mercer 2023 hard-carbon *sodiation* entropy(JMCA), 이중층흑연 모델계(맥락만).
- 서지단서: 전 DOI/arXiv 는 CrossRef/Semantic Scholar/arXiv/MDPI/PubMed/IOP 랜딩서 반환. 전문차단 2건(Schmitt2022 유료; ScienceDirect 403) inline 플래그; 메타=검색헤더+CrossRef, findings=스니펫(전문 아님). 조작 없음.
