# 조사 카드 — 축 A: 단일입자 1차상전이 형상 + 다입자 ensemble 평균화

> 작성: 학술 조사 sub (web search 1차 문헌 기반)
> 대상 가설(이 축): "Ω≥2RT면 단일 입자 dQ/dV는 (유사)델타여야 하는데 실측 코인 하프셀은 치우친 종모양 → 종모양 = 단일입자 델타가 전이 전위 U_j의 입자간 분포로 퍼진 통계역학적 형상."
> tier 범례: 확정(1차문헌 직접확인) / 근거미발견 / 추정 / 미검증
> 정독범위: 본 조사는 Nature/Springer 본문이 인증벽으로 차단되어 다수 abstract-only. PDF 본문 직접 정독한 항목만 full 표기.

---

## 소절 1 — 단일 입자(균질·평형 2상)의 1차 상전이 시 dQ/dV는 정말 델타/극협 peak인가?

### 핵심 논리 (Maxwell 공통접선 → plateau → dQ/dV 델타)
정규용액(regular solution) 격자기체 자유에너지
g(ξ) = RT[ξ ln ξ + (1−ξ) ln(1−ξ)] + Ω ξ(1−ξ) (+ 기준 화학퍼텐셜항)
에서 Ω > 2RT 이면 g(ξ)가 이중웰(double-well)이 되고, 두 웰 사이 구간이 miscibility gap.
화학퍼텐셜 μ(ξ)=dg/dξ 는 비단조(non-monotone, van der Waals loop)가 되어
평형 등온선 V_eq(ξ)=U_j+(RT/F)ln[ξ/(1−ξ)]+(Ω/F)(1−2ξ) 가 N자형 loop을 그린다.
**평형 단일 입자**는 이 loop을 따라가지 않고 Maxwell 공통접선(common-tangent) 작도로
두 상의 화학퍼텐셜을 같게 하는 **단일 평형 전위 = 평탄 plateau**에 머문다.
Q(V)가 그 전위에서 수직 상승 → **dQ/dV = 그 전위에 모인 (유사)델타/극협 spike**. (사용자 가설의 단일입자 부분과 정합)

### 카드 1-1
| 항목 | 내용 |
|---|---|
| 주장 | 1차 상전이(miscibility gap) 영역에서 평형 단일 입자의 voltage는 평탄 plateau → dQ/dV는 그 전위의 델타형 spike |
| 근거문헌 | Bai, Cogswell, Bazant, "Suppression of Phase Separation in LiFePO₄ Nanoparticles During Battery Discharge", *Nano Letters* 11(11) 4890–4896 (2011); DOI 10.1021/nl202764f; arXiv:1108.2326 |
| 지배식/정량값 | 전기화학 phase-field 모델. 저전류(near-equilibrium)에서 spinodal decomposition/nucleation → 입자 내 이동 상경계(moving phase boundary) = 한 입자 안에서 전위 일정(plateau). Ω>2RT가 이중웰 조건 |
| 흑연 적용성 | 모델은 LiFePO₄ 대상이나 정규용액·이중웰·Maxwell 논리는 흑연 staging(stage 2↔1 등 1차 전이)에 그대로 이식 가능(동일 lattice-gas 틀) |
| 타당/한계 | 타당: 평형 1차 전이 = plateau는 교과서 열역학. 한계: 이 논문 핵심은 오히려 *고전류에서 spinodal 소멸→균질 충전*(아래 1-3)이라 "평형 plateau"는 저전류 극한에서만 |
| 사용자 가설 관련성 | 가설의 "단일입자 = (유사)델타" 전제를 1차문헌으로 뒷받침 |
| 정독범위 | abstract-only + 검색요약(본문 PDF는 인증/바이너리로 직접 정독 실패; arXiv 1108.2326 존재) |
| tier | 확정(논리)·근거미발견(흑연 직접 dQ/dV 델타 실측은 별도) |

### 카드 1-2 (단일 입자 실험 형상)
| 항목 | 내용 |
|---|---|
| 주장 | single-particle microelectrode 흑연 실측에서 staging 전이는 voltage plateau로 나타나며, 일부 전이(stage 2→1)는 nucleation-growth(intercalation wave)로 입자 전체를 가로지르는 1차 biphasic 전이 |
| 근거문헌 | (검색요약) 단일 흑연입자 microelectrode 연구: "Elucidating the impact of non-spherical morphology on kinetic behavior of graphite using single-particle microelectrode", *Electrochimica Acta* (2024), ScienceDirect S0013468624011186; 및 "Interplay of Lithium Intercalation and Plating on a Single Graphite Particle" S254243512030619X |
| 지배식/정량값 | "Phase transformation characterized by a plateau in the voltage curve except for 4L–3L transition"; stage 2–1 전이는 단일 신상(new phase)의 입자 전역 nucleation-growth(intercalation-wave) |
| 흑연 적용성 | 직접 흑연 (높음) |
| 타당/한계 | 타당: plateau 형상 = 1차 전이 신호. 한계: 검색요약 기반, 실제 dQ/dV "델타" 정량폭은 미확인. 4L–3L 등 일부는 solid-solution(연속)이라 모든 전이가 델타는 아님 |
| 사용자 가설 관련성 | 단일입자 1차 전이 = plateau(델타 경향) 확인. 단, 흑연 전이 중 일부만 1차(나머지는 연속) — 가설을 전이별로 분리 필요 |
| 정독범위 | abstract-only / 검색요약 |
| tier | 추정→근거미발견(정량 dQ/dV 폭 직접확인 안 됨) |

### 카드 1-3 (단일 입자라도 항상 plateau는 아니다 — 고전류 균질 충전)
| 항목 | 내용 |
|---|---|
| 주장 | 임계 전류 위(Tafel 영역)에서는 spinodal이 사라지고 **단일 입자가 균질(homogeneous)하게 충전** → 입자 내 상분리 없이 연속 채움 |
| 근거문헌 | Bai, Cogswell, Bazant, *Nano Lett.* 11(11) 4890 (2011), DOI 10.1021/nl202764f. 동반: "Phase Separation Dynamics in Isotropic Ion-Intercalation Particles", arXiv:1309.4543 |
| 지배식/정량값 | "Above a critical current density (in the Tafel regime), the spinodal disappears, and particles fill homogeneously" |
| 흑연 적용성 | 흑연도 율속·크기 의존으로 평형 plateau ↔ 동역학 균질충전 사이 이동 가능 |
| 타당/한계 | 타당: "단일입자=항상 델타"는 평형/저전류 극한에서만. 실측 코인셀은 유한 율속 → 단일입자조차 plateau가 완전 델타가 아닐 수 있음(가설의 대안 폭원) |
| 사용자 가설 관련성 | ★ 가설 약점: 종모양 폭의 일부는 입자간 U_j 분포가 아니라 *단일입자 동역학(유한 율속·균질충전)*에서도 생길 수 있음 |
| 정독범위 | abstract-only / 검색요약 |
| tier | 확정(원리)·추정(흑연 정량 기여) |

---

## 소절 2 — 전이 전위 U_j가 입자마다 분포할 때, 다입자 전극 평균 dQ/dV가 매끈한(비대칭) peak이 되는가?

### 카드 2-1 (many-particle: 입자 순차 충전 = 평탄 plateau)
| 항목 | 내용 |
|---|---|
| 주장 | 비단조 단일입자 화학퍼텐셜 + 입자간 빠른 Li 교환 → 다입자계는 **입자가 하나씩 순차(particle-by-particle)로 채워지며** 그 결과 거시 voltage는 평탄 plateau + 히스테리시스 |
| 근거문헌 | Dreyer, Jamnik, Guhlke, Huth, Moškon, Gaberšček, "The thermodynamic origin of hysteresis in insertion batteries", *Nature Materials* 9, 448–453 (2010); DOI 10.1038/nmat2730 |
| 지배식/정량값 | 비단조 single-particle chemical potential μ(ξ) 가정. 다입자계가 자유에너지 최소화 → 한 입자씩 한 상에서 다른 상으로 전이(순차). LiFePO₄·TiO₂ 나노입자 galvanostatic(예: C/20)에서 검증 |
| 흑연 적용성 | 메커니즘 일반(insertion 일반). 흑연 staging도 비단조 μ → 동일 순차충전 가능 |
| 타당/한계 | 타당·고영향(foundational). 한계: 입자간 *빠른* 평형 교환 가정(느린 교환이면 다른 양상). Nature 본문 인증벽으로 abstract+검색요약 |
| 사용자 가설 관련성 | ★핵심: "다입자 평균이 단일입자 델타를 퍼뜨린다"의 메커니즘적 근거. 단, Dreyer는 *동일* 입자라도 순차충전으로 plateau가 나옴을 보임 → 종모양 폭이 반드시 U_j *분포* 때문만은 아님 |
| 정독범위 | abstract-only / 검색요약(Nature nmat2730 + 검색) |
| tier | 확정(서지·핵심주장)·추정(흑연 정량 이식) |

### 카드 2-2 (many-particle Fokker–Planck = U_j 분포의 ensemble 진화)
| 항목 | 내용 |
|---|---|
| 주장 | 단일입자 평형이 ensemble 충전보다 빠른 극한에서, "어떤 상태에 있는 입자 확률분포"의 진화가 비국소 Fokker–Planck형 보존법칙으로 기술됨 → ensemble dQ/dV = 입자 상태분포의 사상 |
| 근거문헌 | Dreyer, Guhlke, Herrmann, "Hysteresis and phase transition in many-particle storage systems", *Continuum Mechanics and Thermodynamics* 23, 211–231 (2011); DOI 10.1007/s00161-010-0178-1 |
| 지배식/정량값 | non-local Fokker–Planck-type conservation law for P(state); 비단조 material behavior → 2상 공존+히스테리시스 |
| 흑연 적용성 | 일반 storage 이론(풍선 ensemble 비유 포함). 흑연 적용 직접언급 없음 |
| 타당/한계 | 타당(수학적). 한계: 입자 *분포*를 명시 모델링 → ensemble 평균이 분포를 어떻게 사상하는지의 정식 틀. 본문 abstract-only |
| 사용자 가설 관련성 | 가설의 "통계역학적 형상 = 입자분포의 평균"을 정식화하는 틀. 분포→형상 사상이 1:1이 아닐 수 있음(히스테리시스·순차성 개입) |
| 정독범위 | abstract-only / 검색요약 |
| tier | 확정(서지·주장)·미검증(흑연 dQ/dV 비대칭 정량) |

### 비대칭/치우침의 출처 정리
- 종모양 비대칭(skew)은 (a) ln[ξ/(1−ξ)] 항의 본질적 비대칭, (b) Ω(1−2ξ) 항, (c) U_j의 비대칭 분포, (d) 동역학(순차/율속) 모두가 기여 가능 — **단일 원인으로 환원 금지**. (확정 원리 / 흑연 분해는 추정)

---

## 소절 3 — ★결정적: 입자가 독립 전이 vs 상호작용(autocatalytic) 전이 시, ensemble이 정적 U_j 분포를 그대로 반영하는가, 왜곡/소실되는가?

### 카드 3-1 (electro-autocatalysis: 단일상 물질에서도 가짜 상분리 plateau)
| 항목 | 내용 |
|---|---|
| 주장 | 입자가 **상호작용(autocatalytic, 탈리튬 진행될수록 교환전류↑)**하면, **miscibility gap이 없는 단일상 물질에서도** ensemble이 상분리처럼 보이는 plateau를 만든다 = "fictitious phase separation"(비평형 다입자 인공물) |
| 근거문헌 | Park, Zhao, Kang, Lim, Chen, Yu, Braatz, Shapiro, Hong, Toney, Bazant, Chueh, "Fictitious phase separation in Li layered oxides driven by electro-autocatalysis", *Nature Materials* 20(7), 991–999 (2021); DOI 10.1038/s41563-021-00936-1; PMID 33686277 |
| 지배식/정량값 | population-dynamics 모델. 핵심 = 계면 교환전류가 탈리튬 정도에 따라 증가(autocatalytic). 검증물질 Liₓ(Ni₁/₃Mn₁/₃Co₁/₃)O₂ (0.5<x<1, 단일상). operando 회절+나노스케일 산화상태 매핑으로 비평형 반복효과 입증. 탈리튬 시 관측, 리튬화 시 미관측(비대칭) |
| 흑연 적용성 | 직접대상은 층상 산화물(양극). 그러나 "다입자 population dynamics가 ensemble 형상을 지배"한다는 원리는 흑연 음극에도 경고로 적용 |
| 타당/한계 | ★강력·고영향. 한계: 흑연 직접 아님. 시사 = ensemble plateau가 단일입자 열역학(미시 U_j 분포)을 반영한다는 *단순 사상이 깨질 수 있다* |
| 사용자 가설 관련성 | ★가설의 가장 큰 반례/단서: ensemble 종모양이 "단일입자 델타의 U_j 분포 퍼짐"이라는 *정적·열역학적* 해석은, 입자 상호작용(autocatalysis)이 있으면 **부분적으로 비평형 동역학 인공물**일 수 있어 분포정보가 왜곡됨 |
| 정독범위 | abstract-only(PubMed 전문 abstract + 검색요약; Nature 본문 인증벽) |
| tier | 확정(서지·핵심주장, abstract 직접확인) |

### 카드 3-2 (흑연: avalanche-like 상관 전이 = 입자내/입자간 상관)
| 항목 | 내용 |
|---|---|
| 주장 | 흑연 입자는 독립 채움이 아니라 **국소 avalanche-like (de)intercalation**(미크론 영역이 수초 내 전이)으로 강한 intraparticle 상관을 보이며, 정적 disorder가 staging을 pseudo-continuous로 만든다 |
| 근거문헌 | Han, Phillips, Merryweather, Lim, Schnedermann, Jack, Grey, Rao, "Avalanche-like lithium intercalation and intraparticle correlations in graphite", arXiv:2509.21047 (2025); DOI 10.48550/arXiv.2509.21047 |
| 지배식/정량값 | operando 광학현미경 + random-field Ising 모델링. avalanche = 무질서계 상전이(마르텐사이트 변태·Barkhausen noise)와 동형(order parameter step 변화). disorder가 dilute stage에서 공간적 이질 연결성 생성 |
| 흑연 적용성 | 직접 흑연 (최고) |
| 타당/한계 | 타당·최신(2025, preprint이므로 peer-review 미확정→tier 강등). 한계: arXiv preprint |
| 사용자 가설 관련성 | ★결정적: 흑연 ensemble dQ/dV는 정적 U_j 분포의 단순 평균이 아니라 **disorder+avalanche(상관) 동역학**으로 매끄러워진다 → "정적 분포 퍼짐" 해석은 불완전. random-field Ising은 "U_j에 quenched disorder" 그림과 정합하나, 평균화는 상관 때문에 비단순 |
| 정독범위 | full(arXiv abstract+상세 검색요약 직접확인; PDF 바이너리 본문은 미정독) |
| tier | 추정→미검증(preprint, peer-review 전) |

### 독립 vs 상호작용 — 종합 판정(이 축 한정, verdict는 master 전담)
- **독립 전이 가정** 하에서는 ensemble dQ/dV ≈ Σ(단일입자 델타) ⊛ ρ(U_j) (분포의 컨볼루션) → 사용자 가설과 정합. 이 컨볼루션 그림 자체의 1차문헌 명시적 검증은 **근거미발견**(원리는 표준이나 흑연 직접 "델타⊛분포=종모양" 피팅 논문 미확인).
- **상호작용(autocatalysis/avalanche)** 이 있으면 ensemble이 (a) 단일상에서도 가짜 plateau(카드3-1), (b) avalanche 상관으로 분포정보 부분 소실/왜곡(카드3-2) → 분포가 **그대로 반영되지 않음**.

---

## 이 축 요약 (3~5줄) + 열린 문제

**요약**: (1) 평형/저전류 단일 입자가 1차 상전이(Ω>2RT)에서 Maxwell 작도로 plateau→dQ/dV 델타가 되는 것은 표준 열역학으로 확정(Bai-Cogswell-Bazant 2011). (2) 다입자 전극이 비단조 단일입자 화학퍼텐셜로 인해 입자를 순차 충전하며 거시 plateau를 만든다는 메커니즘은 Dreyer 2010(Nat. Mater. 9, 448; nmat2730)으로 확정 — 다만 *동일* 입자라도 순차성만으로 plateau가 나오므로 종모양 폭이 반드시 U_j 분포 때문만은 아니다. (3) ★결정적으로, 입자가 상호작용하면(electro-autocatalysis: Park-Chueh-Bazant 2021, s41563-021-00936-1; avalanche: Han-Grey-Rao 2025, arXiv:2509.21047) ensemble은 단일상에서도 가짜 plateau를 만들거나 상관으로 분포정보를 왜곡한다 → **ensemble 평균이 정적 U_j 분포를 1:1로 반영한다는 사용자 가설의 전제는 조건부(독립·near-equilibrium 극한)에서만 성립**.

**열린 문제**:
- 흑연에서 "단일입자 델타 ⊛ U_j 분포 = 실측 종모양"을 직접 피팅·검증한 1차문헌은 이번 조사에서 **근거미발견** — 원리는 표준이나 흑연 dQ/dV 정량 분해 논문 확인 필요.
- 종모양 비대칭(skew)의 정량 분해: ln[ξ/(1−ξ)]·Ω(1−2ξ)·U_j 분포·동역학(순차/율속/avalanche) 각 기여 비중 미검증.
- Nature/Springer 본문 인증벽으로 다수 abstract-only — 본문 정독 시 정량값(폭 w=nRT/F 대비 분포폭, autocatalysis 임계조건) 보강 필요.
