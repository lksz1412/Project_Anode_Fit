# Ch1 v9 LCO — 수집 마스터·선별 (Phase A.2)

> 2026-06-30 master 검색. ★=정독 1순위. 정량은 *검색-grounding(미검증)* — 정독 후 확정. DOI/URL 병기.

## C1/C4 LCO 엔트로피 계수·calorimetry
| ★ | 출처 | venue/year | URL | grounding(미검증) |
|---|---|---|---|---|
| ★ | Reynier/Yazami — Entropy of lithiation of LixCoO2(0.5<x≤1) | (JES/JPS) | — | ΔS 최대 ~9 kB/atom, O3 내 ~4.2 kB/atom; 4.0V 부근 이상(상전이) |
| | Single Electrode Entropy Change for LiCoO2 Electrodes | — | academia 143468519 | 단일 전극 ΔS(x) |
| ★ | Effect of entropy change of Li intercalation in cathodes/anodes on thermal mgmt | JPS 2009 | S0378775309021119 | LCO ΔS ≫ NMC·LFP; 가역열 큰 비중 |
| | Entropy Changes…Graphite Anode & Phase Change of LiCoO2 Cathode | — | RG 234998456 | 음극·양극 ΔS 동시 |
| | Thermodynamic properties of stoichiometric LiCoO2 | Thermochim. Acta 2016 | S0040603116300880 | Cp·H(calorimetry) |

## C2 ★상전이·전자 엔트로피 (전자 엔트로피 anchor)
| ★ | 출처 | venue/year | URL | grounding |
|---|---|---|---|---|
| ★ | **Reimers & Dahn — Electrochemical & in-situ XRD of Li intercalation in LixCoO2** | JES 139, 2091 (1992) | 10.1149/1.2221184 | ★3 상전이(x=1→0.4); x≈0.5 **order–disorder**(Li 정렬)·hex→monoclinic; **metal–insulator @x≲1** 2상역 |
| ★ | Insulator–metal transition upon Li deintercalation from LiCoO2(전자·7Li NMR) | J. Mater. Chem. 1999 | 10.1039/a900016j | MIT 전자 물성 |
| | Electronic phase diagram of LixCoO2(0≤x≤1) | arXiv 2009 | 0909.3556 | 전자 상도 |
| | Bridging scales ML: first-principles stat-mech→phase-field, order–disorder LixCoO2 | J. Mech. Phys. Solids 2024 | S0022509624001923 | ★통계역학적 order–disorder(config 엔트로피) |
| | Enthalpy of Formation of LixCoO2(0.5≤x≤1) | — | RG 244687969 | 형성 ΔH |

## C3 LCO dQ/dV 전이
| ★ | 출처 | URL | grounding |
|---|---|---|---|
| ★ | Staging Phase Transitions in LixCoO2 | RG 216328876 | O3↔monoclinic↔O3; ~4.1V 한 쌍 peak; 고전압 4.55/4.63V plateau(stage-2 @x=0.12) |
| | Phase Transitions & High-Voltage Behavior(Ceder/Xia) | ceder.berkeley JES-Xia | 고전압 상전이 |

## C5 도핑·코팅 영향
| ★ | 출처 | venue | grounding |
|---|---|---|---|
| ★ | High-entropy doping for high-voltage LiCoO2 | JPS 2024 | S0378775324016781 | O3↔H1-3 억제 |
| | (co-doping Ti/Mg/Al) | — | ★Al·Mg = Fermi 레벨서 멀어 **비-redox**·구조/열역학 안정화·전자 요동 억제 → *우리 시료 보정의 물리* |

## C6 양극 엔트로피 추정
| ★ | 출처 | venue | grounding |
|---|---|---|---|
| ★ | MSMR Part I/II(graphite, 프레임 양극 적용) | JES 2024 (ad7d1c·ad70d9) | dU/dT 5%SOL·15–35°C·연속함수 |
| | Entropymetry of Active Materials / Non-destructive LiCoO2 | RG | entropy 구조 진단 |

## ★전자 엔트로피 핵심(L2) — 설계 입력
- LiCoO2(x=1) 절연체 → 탈리튬화 시 **metallic**(전도 전자 출현) → 축퇴 전자기체 → 전자 엔트로피 $S_e\simeq\frac{\pi^2}{3}k_B^2 T\,g(E_F)$(Sommerfeld, $\propto T$). MIT(@x≲1)·order–disorder(@x≈0.5)가 LCO ΔS(x) 의 특징("tilde" 모양·~9 kB/atom). config(Li 정렬)+전자 기여 합.

## Gate (A.2)
6축 ★ 확보·DOI·tier(전부 미검증). → 정독-추출(서브) → A.3 종합·전자 엔트로피 설계.
