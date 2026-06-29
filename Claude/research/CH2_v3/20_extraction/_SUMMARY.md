# CH2 v3 추출 SUMMARY — 문헌×핵심 정량·tier + 상충/공백

> sub(정독-추출) 산출. 종합·Ch1 대조·초안·결정은 master. 모든 정량은 출처·tier 병기, tier 없이 단정 X.
> **공통 부호 규약(MSMR Part I Eq.22/27/28 + Newman 교과서로 확정에 준함)**: ΔG=−nFE_eq, **ΔS=nF·(∂E_eq/∂T) [+부호]**, ΔH=−nFE_eq+nFT·(∂E_eq/∂T), 가역발열 **Q̇_rev=−I·T·(∂U/∂T)** (I>0 방전).

## 문헌 × 핵심 정량 1줄 × 정독범위 × tier

| key | 축 | 핵심 정량/식 1줄 | 정독범위 | tier |
|---|---|---|---|---|
| bernardi1985_energy_balance | A2 | Q̇=I(U−V)−I·T·∂U/∂T; 가역항=−IT·∂U/∂T; ∂U/∂T=ΔS/nF | snippet+2차(원문 X) | 식=확정준함; 부호1건 미해소→Part I로 해소 |
| standardised_potentiometric_2024 | A2 | full cell ∂U/∂T: 0–20%SOC 0.3–0.5 mV/K, 20–100% −0.1~+0.1; std.dev 3.13 µV/K; T35-T0 protocol | **full-text(IOP)** | 정량=확정준함(full cell); 부호 미검증 |
| msmr_partI_quantify_2024 | A5 | **ΔS=nF·dU/dT(Eq.27,+), ΔH=nFU−nFT·dU/dT(Eq.28)**; graphite 6갤러리(Allart ref) | **full-text(IOP)** | 식·부호=확정준함(1급) |
| msmr_partII_entropy_2024 | A5 | MCMB graphite ∂U/∂T: +3~4 mV/K@low-x, ~0.2 부호반전; 반응별 dU_j⁰/dT(j1=+1.39,j4=−0.22 mV/K); 5갤러리,15–35°C | **full-text(IOP)** | 식·한계=확정준함; Fig값 정밀화 권장 |
| reynier2003_entropy_enthalpy | A1 | ΔS(x): x<0.25 양(config), x>0.25 음(vib); ΔH(x)<0 모든 x, 고-x 덜 음(Li–Li 반발) | snippet+abstract(원문 X) | 부호·정성=확정준함; 절대수치 미검증 |
| allart2018_potentiometric_model | A1 | ΔS: +29 J/mol/K@x=0.08(regIV), −15~0@regII(히스), −5~−16@regI(x>0.5); ΔS=nF·dE/dT | **full-text(IOP)** | 식·정량=확정준함; 정밀 region경계 원도확인 |
| chemmater2015_LiH_graphite_calorimetry | A4 | ΔH_form(455K): LiC6 −13.9±1.2, LiC12 −24.8±1.0 kJ/mol Li; 상전이 T·ΔH | snippet+abstract | ΔH=추정(확정준함); ΔS 미확인 |
| jpcc2021_firstprinciples_vib_config | A4 | DFT config↔vib 분해; vib+config 기여 <−20 meV/LixC6 (0≤x≤1/3) | snippet+abstract | 추정; 식·상도 미검증 |
| electrochimacta2019_occupation_transitions | A3 | **dQ/dV+entropy profiling→부분몰 ΔS·ΔH**; dilute 0<x<0.1; plateau@x≈0.07=ΔS·ΔH 길항; Bragg–Williams 확장 | snippet+abstract(원문 X) | 방법·물리=확정준함; 식·절대값 미검증 |
| newman_electrochemical_systems | A6 | ΔS=nF·∂E/∂T, ΔH=−nFE+nFT·∂E/∂T, Q_rev=−IT·dU/dT [+부호] | snippet+LibreTexts 2차 | 관계식=확정준함; 원교과서 페이지 미검증 |

## full-text 직접 본 것 (4): standardised_potentiometric_2024, msmr_partI, msmr_partII, allart2018 — 모두 IOP HTML 본문 구조화 추출.
## abstract/snippet 강등 (6): bernardi1985, reynier2003, chemmater2015, jpcc2021, electrochimacta2019, newman — 유료(ScienceDirect/ACS)·원문 PDF 미파싱·403. ★tier 강등 명시함.

## 핵심 정량 3–5 (tier)
1. graphite 전극 ΔS: **+29 J/mol/K @ x=0.08**, **−5~−16 J/mol/K @ x>0.5** (Allart 2018, full-text, 확정준함).
2. MCMB graphite ∂U/∂T: **+3~4 mV/K @ low-x, ~0.2 SOC 부호반전** (MSMR Part II, full-text, 확정준함; Reynier 부호와 정합).
3. 형성 ΔH: **LiC6 −13.9±1.2, LiC12 −24.8±1.0 kJ/mol Li @455K** (Chem.Mater.2015, abstract, 추정).
4. 정전 식: **ΔS=nF·dU/dT(+), Q̇_rev=−I·T·∂U/∂T** (MSMR Part I Eq.27 + Newman, 확정준함).
5. full cell ∂U/∂T: **0.3–0.5 mV/K @0–20%SOC** (Standardised 2024, full-text, 확정준함, 단 full cell).

## 상충/긴장
- **부호(해소됨)**: standardised_potentiometric 추출이 ∂U/∂T=−ΔS/nF 출력(추출 오류 의심) ↔ MSMR Part I Eq.22/27 + Newman + Reynier + Allart 가 모두 +ΔS/nF. **→ +부호로 확정에 준함**(master 최종 승인만 남음). Bernardi/Standardised 카드의 −부호는 폐기 권장.
- **graphite 갤러리 수**: MSMR Part I=6 (Allart ref) vs Part II=5. 같은 그룹·흑연인데 불일치 — master 두 본문 대조 필요.
- **ΔS 정량 단위·기준 혼재**: full cell mV/K (Standardised) vs 전극 J/mol/K (Allart) vs 반응별 mV/K (MSMR). 비교 시 n·F 환산·전극분리 유의(master 종합 시).

## 공백 (master/후속 sub 채울 것)
1. **Reynier 2003 절대 수치**(dE/dT mV/K, ΔS J/mol/K vs x): 부호·정성만 확보, 절대값 미정독. → Caltech open thesis(6nmrn-e2m11, 403)·academia PDF·full-text 정독 필요.
2. **Electrochim.Acta 2019 본문 식·절대 ΔS/ΔH**: 우리 방법 **prototype(dQ/dV→ΔS·ΔH)**인데 abstract 만 — 우선순위 높음, full-text 정독 필요.
3. **히스테리시스 JPS 2018 정량 불확실도**(±%, µV/K, 최적 온도 여기 protocol): 방법·정성만, 수치 미확보. 가역경계(Q6) 정량 핵심 공백.
4. **Chem.Mater.2015 ΔS_form**: ΔH 만 확보, ΔS 정량 본문 확인 필요. 455K→상온 환산 정당성도.
5. **JPC C 2021 본문 식·상도**: abstract 만(<−20 meV/LixC6). 해석 anchor 라 정량 필요성은 master 판단.

## 가장 불확실한 1곳
**Electrochim.Acta 2019(electrochimacta2019_occupation_transitions)** — 우리 의도(dQ/dV 측정→부분몰 ΔS·ΔH)에 방법이 가장 근접한 prototype 인데, full-text 미파싱(유료·bohrium 인코딩)으로 모델 식(Bragg–Williams 확장 항)·절대 ΔS/ΔH 수치를 못 확보. dilute(0<x<0.1) 한정이라 고-x 적용 한계도 미확인. master 의 full-text 정독 최우선 권장.
