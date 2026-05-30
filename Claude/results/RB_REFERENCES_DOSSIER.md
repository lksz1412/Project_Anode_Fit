# RB_REFERENCES_DOSSIER — 참고문헌 grounding + DOI 실측 검증 (Phase 0.2, step 6–12)

> **위치**: RB Phase 0.2. **방법**: web 실측(Crossref/IOPscience/AIP/APS/ACS/Wiley/RSC/ACM/SIAM) + 사용자 PhD 원문(`jcp_extract.txt`) 직접 read.
> **목적**: 방향-5(근거 논문 필수) + 5-30 경고(무근거 무리한 가정 적발). 모든 가정식의 grounding 원천을 검증된 DOI 와 함께 확정.
> **계획서**: `2026-05-30-undergrad-rederivation-rebuild-plan.md` Phase 0.2.
> **DOI 검증 워크플로**: wf_d5ee0a03-49d (5배치 병렬, 30종) + 문제 3건 집중 재검증(macdonald/funabiki/johnston).

---

## ★ 핵심 발견 — 무근거/오귀속 grounding 2건 (5-30 경고의 실제 사례)

### ⚠️ G-1 [CRITICAL] macdonald2000 = 오귀속 (stretched-tail 핵심 물리의 근거가 틀림)
- **폰 주장**: `macdonald2000` = J. R. Macdonald, "Stretched exponentials with T-dependent exponents from fixed distributions of energy barriers," Phys. Rev. B **61**, 228 (2000).
- **실측 결과**: DOI 10.1103/PhysRevB.61.228 의 \emph{실제} 논문 = "Comparison of methods for estimating continuous distributions of relaxation times" (2000). **폰이 단 제목은 이 DOI 의 논문이 아니다** (제목 오귀속/환각).
- **영향**: 이 문헌은 폰이 \emph{stretched tail 메커니즘}("고정 barrier 분포 → T-의존 stretched 완화")을 grounded 로 격상한 근거(폰 ledger AL-8 novelty 정정의 핵심). 즉 \textbf{문서 전체 핵심 물리(꼬리=spectrum kernel integral)의 grounding 이 오귀속}. → 방향-3(재작성) + 정직 처리 대상.
- **올바른 대체 근거(실측 확정)**: **D. C. Johnston, "Stretched exponential relaxation arising from a continuous sum of exponential decays," Phys. Rev. B 74, 184430 (2006), DOI 10.1103/PhysRevB.74.184430** (Crossref 제목 verbatim 일치). 이 논문이 정확히 "지수 완화의 연속 합/분포 → stretched exponential" 을 다룸 = graphite tail = relaxation-length spectrum 의 kernel integral 과 \emph{구조적으로 정확히 대응}. → `johnston2006` 키로 등재, stretched-tail grounding 의 1차 근거로 사용.
- **조치**: RB 재구성에서 `macdonald2000`(오귀속) 제거. stretched-tail 은 `johnston2006`(correct) + `lindsey1980`(KWW 분포) + `plonka` 로 grounding. 만약 stretched 물리가 이들로도 완전히 닫히지 않으면 해당 부분 FLAGGED.

### ⚠️ G-2 [MEDIUM] funabiki — 권/페이지 오기 (correction)
- **폰 주장**: A. Funabiki, M. Inaba, T. Abe, Z. Ogumi, Electrochim. Acta **45**, 865 (1999).
- **실측 결과**: 실제 = A. Funabiki, M. Inaba, Z. Ogumi, S. Yuasa, J. Otsuji, A. Tasaka, "Stage transformation of lithium-graphite intercalation compounds caused by electrochemical lithium intercalation," **Electrochim. Acta 45(3), 365–377 (1999), DOI 10.1016/S0013-4686(99)00262-4** (Crossref 제목 verbatim 일치). 권 45 맞으나 **페이지 865→365, 저자 목록 다름**(Abe 없음, Yuasa/Otsuji/Tasaka 추가).
- **조치**: `funabiki1999` 서지를 실측값으로 정정.

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
| funabiki1999 | CORRECTED | 10.1016/S0013-4686(99)00262-4 | Funabiki, Inaba, Ogumi, Yuasa, Otsuji, Tasaka, "Stage transformation of lithium-graphite intercalation compounds...," Electrochim. Acta **45(3), 365–377** (1999) [권 맞음, 페이지 865→365, 저자 정정] |
| dubarry2022 | CONFIRMED | 10.3389/fenrg.2022.1023555 | Dubarry, Anseán, "Best practices for incremental capacity analysis," Front. Energy Res. 10, 1023555 (2022) |
| fly2020 | CONFIRMED | 10.1016/j.est.2020.101329 | Fly, Chen, "Rate dependency of incremental capacity analysis (dQ/dV)...," J. Energy Storage 29, 101329 (2020) |
| **stretched 완화·disorder·히스테리시스 (Ch1·5)** | | | |
| johnston2006 | CONFIRMED (신규) | 10.1103/PhysRevB.74.184430 | **D. C. Johnston, "Stretched exponential relaxation arising from a continuous sum of exponential decays," Phys. Rev. B 74(18), 184430 (2006)** [stretched-tail 1차 근거; macdonald2000 오귀속 대체] |
| ~~macdonald2000~~ | REPLACED | — | ⚠️ 오귀속(DOI 61.228 = 다른 논문). 제거. → johnston2006 로 대체 |
| lindsey1980 | CONFIRMED | 10.1063/1.440485 | Lindsey, Patterson, "Detailed comparison of the Williams-Watts and Cole-Davidson functions," JCP 73, 3348–3357 (1980) [KWW 분포] |
| baessler1993 | CONFIRMED | 10.1002/pssb.2221750102 | Bässler, "Charge Transport in Disordered Organic Photoconductors: A Monte Carlo Simulation Study," Phys. Status Solidi B 175(1), 15–56 (1993) |
| plonka1998 | CONFIRMED(부분) | 10.1021/jp9831808 | Plonka, J. Phys. Chem. B 102, 5835 (1998); 별개로 *Dispersive Kinetics*, Kluwer/Springer (2001), ISBN 978-0-7923-6932-7 [논문/책 분리 명시] |
| dreyer2010 | CONFIRMED | 10.1038/nmat2730 | Dreyer, Jamnik, Guhlke, Huth, Moškon, Gaberšček, "The thermodynamic origin of hysteresis in insertion batteries," Nature Materials 9, 448–453 (2010) |
| sethna1993 | CONFIRMED | 10.1103/PhysRevLett.70.3347 | Sethna, Dahmen, Kartha, Krumhansl, Roberts, Shore, "Hysteresis and hierarchies...," PRL 70, 3347–3350 (1993) |
| mckinnon1983 | (book ch.) | — | McKinnon, Haering, "Physical mechanisms of intercalation," *Mod. Aspects Electrochem.* 15, 235 (1983) [book chapter] |
| **수치·closure (Ch1·6)** | | | |
| hindmarsh2005 | CONFIRMED | 10.1145/1089014.1089020 | Hindmarsh et al., "SUNDIALS: Suite of Nonlinear and Differential/Algebraic Equation Solvers," ACM TOMS 31(3), 363–396 (2005) |
| brenan1996 | BOOK | 10.1137/1.9781611971224 (ISBN 978-0-89871-353-4) | Brenan, Campbell, Petzold, *Numerical Solution of IVPs in DAEs*, SIAM Classics 14 (1996) |
| lee2011 | CONFIRMED | 10.1063/1.3568936 | S. Lee, Son, Sung, Chong, "Communication: Propagator for diffusive dynamics of an interacting molecular pair...," JCP 134, 121102 (2011) [사용자 PhD Refs6] |
| son2013 | CONFIRMED | 10.1063/1.4802006 | Son, J. Kim, J.-H. Kim, J. S. Kim, S. Lee, "An accurate expression for the rates of diffusion-influenced reactions with long-range reactivity," JCP 138, 164123 (2013) [사용자 PhD Refs7] |
| jcp2017 | CONFIRMED | 10.1063/1.5000882 | K. Lee, S. Lee, C. H. Choi, S. Lee, "Effects of external electric field and anisotropic long-range reactivity on charge separation probability," JCP 147, 144111 (2017) [사용자 PhD; Plan A closure 원천] |

## JCP2017 원문 직접 검증 (closure 구조, jcp_extract.txt read)
- DOI **10.1063/1.5000882** 원문 직접 확인(View online). 저자 Kyusup Lee, Seonghoon Lee, Cheol Ho Choi, Sangyoub Lee (Seoul Nat'l Univ / Kyungpook Nat'l Univ).
- closure 구조 원문 일치(폰 dossier (c)(d)(e) 검증): **Eq.(32) Fredholm 2종 적분방정식 → Eq.(33) formal exact(ratio form) → Eq.(34) ratio-substitution 근사 → Eq.(39) closed-form.**
- **자기명시 유효범위 원문 확인** (Eq.34 직후, p.144111-5): "the accuracy of the approximation given by Eq.(34) gets worse when the reaction zone becomes very broad." → broad-kernel 열화 = graphite 의 넓은 spectrum(=stretched tail, 저온 관심영역)과 정면 충돌. Plan A 단독 채택 금지, Plan B(g-grid) validator 필수. (Ch1 §closure / Ch6 gate 에 반영)
- Refs [6]=lee2011, [7]=son2013 = Fredholm 2종 해법 원천. dossier `PHASE_DIAG_REFS67_DOSSIER.md` (d) 변수매핑·(e) 가정차이 원문 정합 확인.

## tier 분류 요약 (AL 등재 입력 — Phase 0.3)
- **GROUNDED (확립)**: bernardi1985·rao1997·thomasnewman2003·doyle1993·reynier2004·eyring1935·evanspolanyi1938·marcus1956·bazant2013·onsager1931·schnakenberg1976·dahn1991·ohzuku1993·funabiki1999·dreyer2010·sethna1993·hindmarsh2005·lee2011·son2013·jcp2017·johnston2006·lindsey1980·baessler1993 + 교과서(newman/bardfaulkner/degrootmazur/prigogine/brenan).
- **재확인 필요/주의**: plonka(논문·책 분리), mckinnon(book ch.).
- **REPLACED**: macdonald2000(오귀속) → johnston2006.

## 다음
Phase 0.3 (통합 AL 체계 골격 `RB_AL_MASTER.md`): 본 dossier 의 검증 DOI + tier 를 AL row 로 등재. macdonald→johnston 교체를 stretched-tail AL 항목에 반영. funabiki 정정 반영.
