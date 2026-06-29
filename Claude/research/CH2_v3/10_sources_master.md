# Ch2 v3 — 문헌 수집 마스터·선별 (Phase 1.1)

> 2026-06-30 검색(master 직접) 기반 수집·중복제거·축별 선별. ★표시 = 정독 1순위. **tier**: 모든 정량은 *검색-grounding(미검증)* — Phase 2 정독으로 *확정* 격상 전까지 단정 금지. DOI/URL 병기.

## A1 — 엔트로피 계수 측정·흑연 프로파일
| ★ | 출처 | venue/year | DOI/URL | 검색-grounding 핵심(미검증) |
|---|---|---|---|---|
| ★ | Reynier, Yazami, Fultz — The entropy and enthalpy of Li intercalation into graphite | J. Power Sources 2003 | S0378775303002854 | OCV(T) 로 ΔS·ΔH; ΔS 저x(<0.2) 양수 configurational, 고x(>0.2) 음수; stage2→1(x=0.5) 이상 재증가 |
| ★ | Model of Li intercalation into graphite by potentiometric analysis (equilibrium+entropy curves) | JES 2018 | 10.1149/2.1251802jes | potentiometric 평형·ΔS 곡선 모델 |
| | Reynier et al — Thermodynamics & crystal structure anomalies in Li-graphite | J. Power Sources 2005 | S0378775305007500 | ΔS·구조 이상(stage2→1) 상관 |
| | Entropy Profiles for Li-Ion Batteries—Chemistries & Degradation (review) | 2024 | PMC12025376 | 흑연 ∂U/∂T ~+250→−100 µV/K; stage4(~10%) 평탄·stage2(40–60%) 넓은 peak |
| | Interpreting entropy of Si–graphite blended electrodes | J. Energy Storage 2023 | S2352152X23005157 | 혼합전극 엔트로피 해석(흑연 기여 분리) |

## A2 — 가역 발열·Bernardi·열모델
| ★ | 출처 | venue/year | DOI/URL | 검색-grounding 핵심 |
|---|---|---|---|---|
| ★ | Bernardi, Pawlikowski, Newman — A General Energy Balance for Battery Systems | JES 132(1):5–12, 1985 | 10.1149/1.2113792 | ★정전. $\dot Q=I(U-V)-I\,T\,\partial U/\partial T$; 가역 엔트로피항 = $I\,T\,\partial V_{OCV}/\partial T$ |
| ★ | A Standardised Potentiometric Method for…Reversible Heating in a Li-Ion Cell | JES 2024 | 10.1149/1945-7111/ad4918 | 가역 발열 파라미터화 표준 protocol |
| | Direct Observation of Reversible Heat Absorption…(ultra-sensitive thermometry) | arXiv 2021 | 2107.00625 | 가역 흡열 직접 관측(calorimetric 검증) |
| | Entropy and heat generation of lithium cells/batteries (review) | Chin. Phys. B 2016 | cpb 25(1):010509 | 엔트로피·발열 종설 |

## A3 — ICA/dQ-dV 열역학
| ★ | 출처 | venue/year | DOI/URL | 검색-grounding 핵심 |
|---|---|---|---|---|
| ★ | Transitions of Li occupation in graphite: physically informed model (dilute limit) + 열역학 측정 | Electrochim. Acta 2019 | S0013468619316457 | ★우리 의도 근접 — 부분몰 ΔS·ΔH 로 occupation transition; dilute stage |
| | Differential Analysis of Galvanostatic Cycle Data: interpretive insights | Chem. Mater. 2022 | acs.chemmater.2c01976 | dQ/dV·dV/dQ peak 해석 heuristics |
| | ICA(dQ/dV) ambient temperature·clamping degradation | J. Electroanal. Chem. 2023 | S1572665723004873 | dQ/dV 온도효과(진단) |

## A4 — Li-graphite staging 열역학(실험·DFT)
| ★ | 출처 | venue/year | DOI/URL | 검색-grounding 핵심 |
|---|---|---|---|---|
| ★ | Intercalation Compounds from LiH and Graphite…(calorimetry) | Chem. Mater. 2015 | acs.chemmater.5b00235 | ★형성 ΔH: LiC6 −13.9±1.2, LiC12 −24.8±1 kJ/mol Li(455K); 고x Li–Li 반발 |
| ★ | Thermodynamic Analysis of Li-Graphite by First-Principles(vibrational+configurational) | J. Phys. Chem. C 2021 | acs.jpcc.1c08992 | configurational↔vibrational 분해 DFT |
| | Robust high-fidelity DFT — Li-graphite phase diagram | arXiv 2016 | 1607.05658 | 상도·DFT interlayer 신뢰성 한계 |

## A5 — 파라미터 추정(회귀·MSMR·system-ID)
| ★ | 출처 | venue/year | DOI/URL | 검색-grounding 핵심 |
|---|---|---|---|---|
| ★ | Quantifying Entropy & Enthalpy of Insertion Materials via MSMR | JES 2024 | 10.1149/1945-7111/ad1d27 | ★MSMR(다반응=우리 다전이) 로 ΔS·ΔH 정량 |
| ★ | MSMR Temperature Dependence Part II — Entropy Coefficient for MCMB Graphite | JES 2024 | 10.1149/1945-7111/ad70d9 | 흑연 엔트로피 계수 연속함수 추정 |
| | A System Identification Approach to Estimate Entropy Coefficients | JES 2025 | 10.1149/1945-7111/adfe1f | system-ID, potentiometric 대비 57%↓ 시간 |
| | Dynamic measurement of entropy coefficient | J. Energy Storage 2022 | S2352152X22003851 | 동적법(potentiometric 대비 13.4×↓ 시간) |
| | Unifying Chemical & Electrochemical Thermodynamics of Electrodes | arXiv 2025 | 2507.10677 | 통합 열역학 틀(최신) |

## A6 — 교과서·정전
| ★ | 출처 | DOI/URL | 핵심 |
|---|---|---|---|
| ★ | Newman & Thomas-Alyea — *Electrochemical Systems*(3rd) | (교과서) | OCV(T): slope=ΔS, intercept=ΔH; 발열·entropy 정전 |
| | Huggins — *Advanced Batteries: Materials Science Aspects* | (교과서) | intercalation 열역학 정전 |

## A-add — 히스테리시스/가역경계(Q6)
| ★ | 출처 | venue/year | DOI/URL | 핵심 |
|---|---|---|---|---|
| ★ | Uncertainties in entropy due to temperature path dependent voltage hysteresis | J. Power Sources 2018 | S0378775318305287 | ★히스→엔트로피 측정 불확실성(가역/비가역 경계) |
| | Voltage hysteresis during lithiation/delithiation…meta-stable carbon stackings | J. Mater. Chem. A 2021 | 10.1039/D0TA10403E | OCV history-dependent; stage II disorder; >50°C 잔류 |

## 선별 결과 / Gate
- 정독 1순위(★) = A1(Reynier 2003·JES 2018)·A2(Bernardi 1985·JES 2024)·A3(Electrochim.Acta 2019)·A4(Chem.Mater.2015·JPC C 2021)·A5(JES 2024 ad1d27·ad70d9)·A6(Newman)·히스(JPS 2018).
- 중복제거 완료(Reynier/potentiometric/MSMR 계열 통합). 1차·peer 우선·리뷰=진입점.
- **Gate PASS_SOURCES**: 6축+히스 축별 ★ 확보·DOI 병기·tier(전부 미검증, Phase 2 정독 대상). → Phase 2.1 정독·추출(master 핵심 + 서브1 클러스터 순차).
