# RB_REFERENCES_DOSSIER — 참고문헌 grounding + DOI 실측 검증 (Phase 0.2, step 6–12)

> **위치**: RB Phase 0.2. **방법**: web 실측(Crossref/IOPscience/AIP/APS/ACS/Wiley/RSC/ACM/SIAM) + 사용자 PhD 원문(`jcp_extract.txt`) 직접 read.
> **목적**: 방향-5(근거 논문 필수) + 5-30 경고(무근거 무리한 가정 적발). 모든 가정식의 grounding 원천을 검증된 DOI 와 함께 확정.
> **계획서**: `2026-05-30-undergrad-rederivation-rebuild-plan.md` Phase 0.2.
> **DOI 검증 워크플로**: wf_d5ee0a03-49d (5배치 병렬, 30종) + 문제 3건 집중 재검증(svare(저자)/funabiki(title↔locator)/johnston).
> **정정 이력(GS-5)**: 1차 작성서 macdonald2000 을 "DOI 오귀속/제거" 로 잘못 기록 → 워크플로 전문 재독 후 "저자만 오귀속, DOI·물리 유효 → svare2000 으로 정정·사용" 으로 바로잡음.

---

## ★ 핵심 발견 — grounding 오류 (5-30 경고의 실제 사례)

### ⚠️ G-1 [HIGH] macdonald2000 = \emph{저자} 오귀속 (DOI·제목·물리는 정확, 저자만 틀림)
> **정정(2026-05-30, GS-5 정직성)**: 본 항목 1차 기록에서 "DOI 가 다른 논문" 이라 적었으나 \emph{틀렸다}. 워크플로 web 실측(Crossref+APS) 재확인 결과 DOI·제목·내용은 정확하고 \textbf{저자만 오귀속}이다.
- **폰 주장**: `macdonald2000` = **J. R. Macdonald**, "Stretched exponentials with T-dependent exponents from fixed distributions of energy barriers...," Phys. Rev. B **61**, 228 (2000).
- **실측 결과**: DOI 10.1103/PhysRevB.61.228 = 제목 "Stretched exponentials with T-dependent exponents from fixed distributions of energy barriers **for relaxation times in fast-ion conductors**" — 제목·권·페이지(228–233)·연도 \emph{전부 맞음}. 단 \textbf{저자 = I. Svare, S. W. Martin, F. Borsa} (Macdonald 아님; Macdonald 는 이 논문의 ref 28 로 인용돼 혼동 유발).
- **영향**: 이 문헌은 \emph{stretched tail 메커니즘}("고정 activation-barrier 분포 → T-의존 stretched 완화, fast-ion conductor")을 grounded 로 뒷받침한다 — 물리적으로 graphite tail = relaxation-length spectrum kernel integral 과 \textbf{정확히 부합·유효}. 즉 \textbf{근거 문헌 자체는 살아있고, 저자명만 틀렸다.}
- **조치**: 키 `macdonald2000` → **`svare2000`** 로 정정, 저자 = Svare/Martin/Borsa, DOI 10.1103/PhysRevB.61.228 유지. stretched-tail 1차 근거로 \emph{사용}.
- **보강(추가 유효)**: **D. C. Johnston, "Stretched exponential relaxation arising from a continuous sum of exponential decays," Phys. Rev. B 74, 184430 (2006), DOI 10.1103/PhysRevB.74.184430** (Crossref verbatim 확인) — "지수 완화의 연속 합 → stretched" 을 \emph{kernel integral 구조 그대로} 다룸. `johnston2006` 키로 추가. → stretched-tail grounding = svare2000(fast-ion DAE) + johnston2006(연속합) + lindsey1980(KWW). 셋으로 닫히지 않는 세부는 Ch1 S2 에서 FLAGGED.

### ⚠️ G-2 [MEDIUM] funabiki — title↔locator 불일치 (★사용자 결정 필요, D7)
> **정정(2026-05-30)**: 1차 기록의 "365–377, DOI ...00262-4" 는 \emph{내 추정이었고 web 미확인}. 워크플로 실측 결과 두 별개 논문이 충돌:
- **폰 주장(혼합)**: 제목 "Stage transformation of lithium-graphite intercalation compounds" + locator Electrochim. Acta **45**, 865 (1999).
- **실측 — locator 기준**: Electrochim. Acta 45(6), **865–871** (1999), 저자 Funabiki/Inaba/Abe/Ogumi = 제목 "**Nucleation and phase-boundary movement** upon stage transformation in lithium-graphite intercalation compounds", **DOI 10.1016/S0013-4686(99)00290-X**.
- **실측 — title 기준**: "**Stage Transformation** of Lithium-Graphite Intercalation Compounds Caused by Electrochemical Lithium Intercalation" = 다른 저널 **J. Electrochem. Soc. 146(7), 2443–2448 (1999), DOI 10.1149/1.1391953**.
- **즉**: 폰이 \emph{title 은 JES 논문, locator(권·페이지)는 Electrochim. Acta 논문} 을 섞었다(둘 다 실재하는 같은 그룹 1999 논문).
- **권고값(D7)**: 두 논문이 모두 staging 전이 kinetics 라 본 작업 grounding 에 \emph{둘 다 유효}. **둘 다 등재** — `funabiki1999ea`(Electrochim. Acta, nucleation/phase-boundary, DOI 00290-X) + `funabiki1999jes`(JES, stage transformation, DOI 10.1149/1.1391953). AL-3(staging) 에서 함께 인용. 사용자 이의 시 택일.

---

## 검증 결과 전건표 (30종 + 보강)

tier: GROUNDED(논문/교과서 확립) / status: CONFIRMED(서지·DOI 정확) · CORRECTED(서지 정정) · BOOK · REPLACED(오귀속 교체).

| key | status | 검증 DOI / ISBN | 서지(정정 반영) |
|---|---|---|---|
| **전기화학·전지 (Ch1·2·4·6)** | | | |
| bernardi1985 | CONFIRMED | 10.1149/1.2113792 | Bernardi, Pawlikowski, Newman, "A General Energy Balance for Battery Systems," JES 132(1), 5–12 (1985) |
| rao1997 | CONFIRMED | 10.1149/1.1837884 | Rao, Newman, "Heat-Generation Rate and General Energy Balance for Insertion Battery Systems," JES 144(8), 2697–2704 (1997) |
| thomasnewman2003 | CONFIRMED | 10.1149/1.1531194 | Thomas, Newman, "Thermal Modeling of Porous Insertion Electrodes," JES 150(2), A176–A192 (2003) |
| doyle1993 | CORRECTED | 10.1149/1.2221597 | Doyle, Fuller, Newman, "Modeling of Galvanostatic Charge and Discharge of the Lithium/Polymer/Insertion Cell," JES 140(6), 1526–1533 (1993) [제목 truncation 정정] |
| reynier2004 | CORRECTED | 10.1149/1.1646152 | Reynier, Yazami, Fultz, "Thermodynamics of Lithium Intercalation into **Graphites and Disordered Carbons**," JES 151(3), A422–A426 (2004) [제목 정정] |
| baker1999 | CONFIRMED | 10.1149/1.1391950 | Baker, Verbrugge, "Temperature and Current Distribution in Thin-Film Batteries," JES 146(7), 2413–2424 (1999) |
| doyle/newman 교과서 | BOOK | ISBN 978-0-471-47756-3 | Newman, Thomas-Alyea, *Electrochemical Systems*, 3rd ed., Wiley (2004) [키 `newman`≡`newman2004` 통합] |
| **반응속도론·비평형 열역학 (Ch1·3·4)** | | | |
| eyring1935 | CONFIRMED | 10.1063/1.1749604 | Eyring, "The Activated Complex in Chemical Reactions," JCP 3(2), 107–115 (1935) |
| evanspolanyi1938 | CONFIRMED | 10.1039/TF9383400011 | Evans, Polanyi, Trans. Faraday Soc. 34, 11 (1938) |
| marcus1956 | CONFIRMED | 10.1063/1.1742723 | Marcus, "On the Theory of Oxidation-Reduction Reactions Involving Electron Transfer. I," JCP 24(5), 966–978 (1956) |
| bazant2013 | CONFIRMED | 10.1021/ar300145c | Bazant, "Theory of Chemical Kinetics and Charge Transfer Based on Nonequilibrium Thermodynamics," Acc. Chem. Res. 46, 1144–1160 (2013) |
| onsager1931 | CONFIRMED | 10.1103/PhysRev.37.405 | Onsager, "Reciprocal Relations in Irreversible Processes. I," Phys. Rev. 37(4), 405–426 (1931) |
| schnakenberg1976 | CONFIRMED | 10.1103/RevModPhys.48.571 | Schnakenberg, "Network Theory of Microscopic and Macroscopic Behavior of Master Equation Systems," Rev. Mod. Phys. 48(4), 571–585 (1976) |
| prigogine1967 | (book) | ISBN — | Prigogine, *Introduction to Thermodynamics of Irreversible Processes*, 3rd ed., Interscience (1967) |
| degrootmazur1962 | (book) | ISBN — | de Groot, Mazur, *Non-Equilibrium Thermodynamics*, North-Holland (1962); Dover (1984) |
| bardfaulkner | (book) | ISBN 978-0-471-04372-0 | Bard, Faulkner, *Electrochemical Methods*, 2nd ed., Wiley (2001) |
| **흑연 staging·ICA (Ch1·5)** | | | |
| dahn1991 | CONFIRMED | 10.1103/PhysRevB.44.9170 | Dahn, "Phase diagram of Li$_x$C$_6$," Phys. Rev. B 44(17), 9170–9177 (1991) |
| ohzuku1993 | CORRECTED | 10.1149/1.2220849 | Ohzuku, Iwakoshi, Sawai, "Formation of Lithium-Graphite Intercalation Compounds...," JES 140(9), 2490–2498 (1993) |
| funabiki1999ea | CORRECTED | 10.1016/S0013-4686(99)00290-X | Funabiki, Inaba, Abe, Ogumi, "Nucleation and phase-boundary movement upon stage transformation in lithium-graphite intercalation compounds," Electrochim. Acta **45(6), 865–871** (1999) [locator 기준; 제목 정정] |
| funabiki1999jes | CONFIRMED | 10.1149/1.1391953 | Funabiki, Inaba, Abe, Ogumi, "Stage Transformation of Lithium-Graphite Intercalation Compounds Caused by Electrochemical Lithium Intercalation," JES **146(7), 2443–2448** (1999) [title 기준; D7 — 둘 다 등재] |
| dubarry2022 | CONFIRMED | 10.3389/fenrg.2022.1023555 | Dubarry, Anseán, "Best practices for incremental capacity analysis," Front. Energy Res. 10, 1023555 (2022) [+ 2023 Corrigendum 10.3389/fenrg.2023.1203569] |
| fly2020 | CONFIRMED | 10.1016/j.est.2020.101329 | Fly, Chen, "Rate dependency of incremental capacity analysis (dQ/dV)...," J. Energy Storage 29, 101329 (2020) |
| **stretched 완화·disorder·히스테리시스 (Ch1·5)** | | | |
| svare2000 | CONFIRMED (저자정정) | 10.1103/PhysRevB.61.228 | **I. Svare, S. W. Martin, F. Borsa, "Stretched exponentials with T-dependent exponents from fixed distributions of energy barriers for relaxation times in fast-ion conductors," Phys. Rev. B 61, 228–233 (2000)** [stretched-tail 1차 근거; 폰 키 macdonald2000 의 저자 오귀속 정정] |
| johnston2006 | CONFIRMED (신규보강) | 10.1103/PhysRevB.74.184430 | D. C. Johnston, "Stretched exponential relaxation arising from a continuous sum of exponential decays," Phys. Rev. B 74, 184430 (2006) [stretched=연속합 구조, kernel integral 대응] |
| lindsey1980 | CONFIRMED | 10.1063/1.440530 | Lindsey, Patterson, "Detailed comparison of the Williams-Watts and Cole-Davidson functions," JCP 73(7), 3348–3357 (1980) [KWW 분포; DOI 정정 440485→440530] |
| baessler1993 | CONFIRMED | 10.1002/pssb.2221750102 | Bässler, "Charge Transport in Disordered Organic Photoconductors: A Monte Carlo Simulation Study," Phys. Status Solidi B 175(1), 15–56 (1993) |
| plonka | NOT_FOUND(논문)/BOOK | 논문 DOI 미확인 / 책 ISBN 미확인 | Plonka, J. Phys. Chem. B 102, 5835 (1998) [DOI web 미확인 — FLAGGED, 페이지 5835 직접조회 필요]; *Dispersive Kinetics*, Kluwer (2001) [ISBN 미확인]. 둘 다 보조 근거로만, 미확인 표기 |
| dreyer2010 | CONFIRMED | 10.1038/nmat2730 | Dreyer, Jamnik, Guhlke, Huth, Moškon, Gaberšček, "The thermodynamic origin of hysteresis in insertion batteries," Nature Materials 9, 448–453 (2010) |
| sethna1993 | CONFIRMED | 10.1103/PhysRevLett.70.3347 | Sethna, Dahmen, Kartha, Krumhansl, Roberts, Shore, "Hysteresis and hierarchies...," PRL 70, 3347–3350 (1993) |
| mckinnon1983 | BOOK ch. | 10.1007/978-1-4615-7461-3_4 | McKinnon, Haering, "Physical Mechanisms of Intercalation," in *Modern Aspects of Electrochemistry* No.15 (eds. White, Bockris, Conway), Plenum, NY (1983), pp.235–304 |
| **수치·closure (Ch1·6)** | | | |
| hindmarsh2005 | CONFIRMED | 10.1145/1089014.1089020 | Hindmarsh et al., "SUNDIALS: Suite of Nonlinear and Differential/Algebraic Equation Solvers," ACM TOMS 31(3), 363–396 (2005) |
| brenan1996 | BOOK | 10.1137/1.9781611971224 (ISBN 978-0-89871-353-4) | Brenan, Campbell, Petzold, *Numerical Solution of IVPs in DAEs*, SIAM Classics 14 (1996) |
| lee2011 | CONFIRMED | 10.1063/1.3565476 | S. Lee, C. Y. Son, J. Sung, S.-H. Chong, "Communication: Propagator for diffusive dynamics of an interacting molecular pair," JCP 134, 121102 (2011) [사용자 PhD Refs6; DOI 정정 3568936→3565476] |
| son2013 | CONFIRMED | 10.1063/1.4802584 | C. Y. Son, J. Kim, J.-H. Kim, J. S. Kim, S. Lee, "An accurate expression for the rates of diffusion-influenced bimolecular reactions with long-range reactivity," JCP 138, 164123 (2013) [사용자 PhD Refs7; DOI 정정 4802006→4802584] |
| jcp2017 | CONFIRMED | 10.1063/1.5000882 | K. Lee, S. Lee, C. H. Choi, S. Lee, "Effects of external electric field and anisotropic long-range reactivity on charge separation probability," JCP 147, 144111 (2017) [사용자 PhD; Plan A closure 원천] |

## JCP2017 원문 직접 검증 (closure 구조, jcp_extract.txt read)
- DOI **10.1063/1.5000882** 원문 직접 확인(View online). 저자 Kyusup Lee, Seonghoon Lee, Cheol Ho Choi, Sangyoub Lee (Seoul Nat'l Univ / Kyungpook Nat'l Univ).
- closure 구조 원문 일치(폰 dossier (c)(d)(e) 검증): **Eq.(32) Fredholm 2종 적분방정식 → Eq.(33) formal exact(ratio form) → Eq.(34) ratio-substitution 근사 → Eq.(39) closed-form.**
- **자기명시 유효범위 원문 확인** (Eq.34 직후, p.144111-5): "the accuracy of the approximation given by Eq.(34) gets worse when the reaction zone becomes very broad." → broad-kernel 열화 = graphite 의 넓은 spectrum(=stretched tail, 저온 관심영역)과 정면 충돌. Plan A 단독 채택 금지, Plan B(g-grid) validator 필수. (Ch1 §closure / Ch6 gate 에 반영)
- Refs [6]=lee2011, [7]=son2013 = Fredholm 2종 해법 원천. dossier `PHASE_DIAG_REFS67_DOSSIER.md` (d) 변수매핑·(e) 가정차이 원문 정합 확인.

## tier 분류 요약 (AL 등재 입력 — Phase 0.3)
- **GROUNDED (확립, web 실측)**: bernardi1985·rao1997·thomasnewman2003·doyle1993·reynier2004·baker1999·eyring1935·evanspolanyi1938·marcus1956·bazant2013·onsager1931·schnakenberg1976·dahn1991·ohzuku1993·funabiki1999ea·funabiki1999jes·dreyer2010·sethna1993·hindmarsh2005·lee2011·son2013·jcp2017·svare2000·johnston2006·lindsey1980·baessler1993·dubarry2022·fly2020 + 교과서(newman/bardfaulkner/degrootmazur/prigogine/brenan/mckinnon).
- **저자/서지 정정 적용**: svare2000(폰 macdonald2000 저자 오귀속), funabiki(title↔locator 분리 → ea+jes 둘 등재, D7), lee2011·son2013·lindsey1980 DOI 정정, doyle/reynier/ohzuku 제목 정정, dubarry Anseán 철자+corrigendum.
- **미확인(FLAGGED, 보조만)**: plonka(논문 DOI·책 ISBN web 미확인).
- **결론**: 폰 키 `macdonald2000` 은 \emph{제거 아님} — 저자만 정정해 `svare2000` 으로 \emph{유효 사용}. johnston2006 은 보강 추가.

## 다음
Phase 0.3 (통합 AL 체계 골격 `RB_AL_MASTER.md`): 본 dossier 의 검증 DOI + tier 를 AL row 로 등재. macdonald2000→svare2000 저자 정정 + johnston2006 보강을 AL-14(stretched) 에 반영. funabiki ea+jes 둘 등재 반영. (완료)
