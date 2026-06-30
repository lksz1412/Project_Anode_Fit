# 12 — 축 C: 역문제 (전기화학 신호 → 입자크기분포 PSD 추출) + OCV/dQ/dV 분포 해석

> 역할: 4세션 분업 중 **조사 sub (축 C 전담)**. 배정 1축 web search 1차 문헌 검증 + 본 카드 1개 Write. 종합·verdict·타 축 카드 X (master 전담).
> 대상 가설(사용자): 실측 흑연 dQ/dV 의 치우친 종모양 peak = (단일입자 ≈델타) ⊛ (U_j 분포), 그리고 U_j 분포 ↔ 입자 반경 분포. ∴ peak 을 deconvolution 하면 반경 분포 추산.
> 본 축 = **그 역변환(peak→분포)의 선례·성립조건·ill-posedness** 를 1차 문헌으로 판정. 모델·코드 수정 X.
> 정독범위 표기: F=full text 정독 / A=abstract·landing·검색 스니펫만(tier 강등 사유).

---

## 소절 1 — 전기화학 측정으로 PSD/이질성 분포를 *실제로 추출*한 선례

핵심 결론: **PSD-역추출 선례는 존재하나, 거의 전부 "분포 형태를 가정(lognormal 등)하고 forward 모델을 fit" 하는 parametric 방식**이다. 모델-자유(non-parametric) 직접 deconvolution 으로 PSD 를 뽑은 선례는 EIS/diffusion-impedance 계열에 한정되며, dQ/dV·DVA 에서 PSD 를 직접 역변환한 1차 선례는 **근거 미발견**(이 축에서 확인된 범위 내).

- **(가장 강한 선례·EIS) Song & Bazant 2012 — diffusion impedance 로 PSD 역추정.** Fredholm 1종 적분방정식 틀에서 "impedance image" 로 nanoparticle shape/size distribution 을 infer 하는 **명시적 inverse problem** 제시. forward(분포→임피던스)는 well-posed, inverse 는 functional form(lognormal 등) 가정 + best-fit 으로 풀이 — 즉 **정규화/형태가정 없이는 직접 역변환 불가**임을 사실상 시인("in some cases, more accurately than by direct image analysis" 라는 조건부 표현). → 사용자 가설과 **같은 구조의 역문제**가 임피던스 영역에서 실재함을 입증하나, 동시에 **형태가정 의존**이라는 한계도 입증.
- **(DVA/dV-dQ 진단) Bloom et al. 2005 — DVA 기법.** dV/dQ peak 을 half-cell 기준으로 귀속해 열화/용량손실 원인 분리. 그러나 목적은 **전극 balance·LLI/LAM 진단**이지 PSD 추출이 아님. PSD 를 dV/dQ 에서 직접 역산하지 않음.
- **(forward 다입자 모델) Kirk, Evans, Please, Chapman 2022 (SIAM J. Appl. Math.) — uni/bimodal PSD 전향 모델.** PSD 를 *입력*으로 주고 전압/dV 응답을 예측(forward). bimodal PSD → 방전곡선 double-plateau 재현. **역방향(전압→PSD) 은 다루지 않음.** ★중요: peak smoothing 이 PSD 만으로 설명되지 않고 narrow PSD 는 SPM 의 작은 보정항으로 근사된다는 점 → "치우친 종모양"을 PSD 만으로 귀속하기 전에 다른 broadening 원과 분리 필요.
- **(독립 PSD 대조 표준) SEM 단면·레이저 회절.** 문헌 공통적으로 PSD 의 ground truth 는 SEM 단면 히스토그램 또는 레이저 회절. 전기화학 역추출은 반드시 이들과 **cross-validate** 해야 신뢰 — 단독 전기화학 PSD 는 미검증으로 취급되는 게 관행.
- **(함정) dQ/dV broadening ≠ PSD.** Cell Reports Phys. Sci. 2023(전극 불균일 profiling): 0 V 이상 흑연 dQ/dV 의 broad peak 은 "wide **potential** distribution among graphite particles" = **전극 불균일/반응 불균일**의 표현이며 "rather than particle size distribution alone" 로 명시. → 사용자 가설의 핵심 약점(broadening 의 다중 원인 혼입)을 직접 지적.

## 소절 2 — OCV/삽입 등온선 = site-energy 분포/DOS 적분 해석 틀

핵심 결론: **이 해석 틀은 1차 문헌으로 확립**(lattice-gas/Frumkin 계열). dQ/dV(=dx/dμ 류)가 자리-에너지 밀도(일종의 "DOS")에 대응한다는 사상은 표준이며, **peak 폭 ↔ 에너지 분포 폭** 사상도 이 틀 안에서 자연스럽다. 단, 이 틀에서의 "분포"는 **자리(site) 에너지/조성 분포**이지 곧바로 **입자 반경 분포**가 아니다 — 반경→U_j 매핑(축 B/3의 결과)이 별도로 성립해야 사용자 가설로 연결.

- **McKinnon & Haering lattice-gas (고전).** 삽입 등온선·dμ/dx 를 강체 host 격자 위 guest 배열의 configurational transition 으로 설명. dμ/dx(↔ dV/dx, 그 역수 ↔ dx/dV ∝ dQ/dV)가 상호작용·자리 에너지로 결정 → **dQ/dV peak = 자리 에너지 밀도의 봉우리**라는 해석의 모태.
- **Frumkin intercalation isotherm review (Levi & Aurbach 계열, Electrochim. Acta).** Frumkin 등온선(상호작용항 g 포함)으로 Li 삽입 기술 — 평형 등온선 형상↔상호작용 파라미터·자리 에너지 분포 폭의 정량 사상 제공. dQ/dV 폭이 RT·상호작용·분포 폭으로 결정됨을 보임. → 본 모델의 `Ω`(상호작용)·`w_eff` 와 직접 대응.
- **dQ/dV ∝ 일종의 DOS.** ICA(incremental capacity) 의 peak = 전압 plateau(상전이/자리 채움)에 대응(diagnostic 문헌 다수). dI/dV ∝ DOS 의 전기화학적 유비 — peak 위치/폭/면적이 자리 에너지 분포의 통계량을 담음. (유비는 강하나 "DOS" 라는 표현 자체는 전자구조 STM 맥락이 1차 — 전기화학 dQ/dV 를 문자 그대로 DOS 라 부른 1차 문헌은 이 축에서 abstract 수준만 확인 → 해석 틀은 확정, 용어 동일성은 추정.)

## 소절 3 — ★역문제 수학: peak = 커널 ⊛ 분포 의 deconvolution 성립조건

핵심 결론: **forward(분포→peak)는 well-posed, inverse(peak→분포)는 전형적 ill-posed**. 동일 구조(1종 Fredholm)인 DRT(distribution of relaxation times) 가 "intrinsically ill-posed, requires regularization(Tikhonov)" 로 **1차 문헌에서 명시적으로 ill-posed 판정**되는 것이 가장 강한 유비 근거. 따라서 사용자의 deconvolution 은 **정규화 없이는 불안정·비유일**.

- **성립조건(문헌·표준 deconvolution 이론 종합):**
  1. **커널 기지(known kernel):** 단일입자 본질 응답(델타 또는 유한폭 커널)이 정확히 알려져야 함. 본 모델에서 단일입자가 진짜 델타인지 floor-clip 극협 종인지(00_scope §전제: `w_eff` floor ≈1.3 mV vs 기본 `nRT/F`≈25.7 mV)에 따라 커널이 달라짐 → **커널 자체가 미확정이면 deconvolution 출발점 부재.**
  2. **커널 폭 ≪ 분포 폭:** 내재 커널이 분포보다 좁아야 측정 peak ≈ 분포. 커널이 분포만큼 넓으면 측정 peak 은 분포 정보를 거의 못 담아 역변환이 무의미.
  3. **단조·전단사 매핑:** U_j ↔ 반경 사상이 단조·일대일이어야 분포 보존. (비단조면 다대일 → 유일성 파괴.)
  4. **노이즈/ill-posedness:** 작은 측정 노이즈가 역해를 크게 진동(고주파 증폭) → **유일·안정해 없음**. Tikhonov/MaxEnt 등 정규화 필수, 정규화 파라미터 α 선택이 결과 지배(과소=불안정, 과대=과평활).
  5. **유일성:** 비음(non-negative)·정규화 제약을 줘도 일반적으로 **유일성 보장 X**; 형태가정(lognormal 등 parametric)으로 좁혀야 실용해.
- **1종 Fredholm·ill-posed 직접 근거(DRT):** DRT 계산은 "intrinsically ill-posed problem often requiring regularization" 이며 Tikhonov 정규화가 표준, "selection of the regularization parameter has always been a problem". → 사용자 deconvolution 과 **수학적으로 동형**(peak = ∫ 커널(·;θ)·분포(θ) dθ). 이 ill-posedness 판정이 본 축의 핵심 산출.
- **state-dependent identifiability:** 배터리 inverse problem 일반에서 "multiple parameter combinations can yield nearly indistinguishable voltage-time curves" — 즉 서로 다른 분포가 거의 같은 곡선을 줄 수 있음(비유일의 실증). 균일 ill-posed 가 아니라 **상태/구간 의존**이라, 일부 SOC 구간에선 식별 가능, 일부는 불가.
- **Song & Bazant 2012 가 이미 같은 처방:** PSD 역추정 시 lognormal 형태가정 + best-fit → **non-parametric 직접 deconvolution 을 피하고 parametric 으로 ill-posedness 우회**. 사용자도 동일 전략(반경 분포에 형태가정)을 써야 실용적.

---

## 카드 (schema: 주장 | 근거문헌 | 방법/정량값 | 흑연 적용성 | 타당/한계 | 사용자가설 관련성 | 정독범위 | tier)

| # | 주장 | 근거문헌 (저자·연도·DOI/URL) | 방법/정량값 | 흑연 적용성 | 타당/한계 | 사용자가설 관련성 | 정독범위 | tier |
|---|------|------|------|------|------|------|------|------|
| C1 | 전기화학(diffusion impedance)으로 입자 size distribution 을 역추정하는 inverse problem 이 실재 — 단, 형태가정+fit | Song & Bazant 2012, arXiv:1205.6539, DOI 10.48550/arXiv.1205.6539 | Fredholm 1종 적분, "impedance image"→shape/size dist. infer; lognormal 등 형태가정 best-fit | 임피던스 기반·재료 일반(흑연 직접 사례 아님) | forward well-posed; inverse 는 형태가정 의존("in some cases more accurately than direct imaging" 조건부) | **사용자와 동일 구조 역문제의 실재 선례 + 형태가정 필수성 입증** | A(abstract) | 추정(abstract-only; 구조·결론은 확정에 가까우나 정량은 미정독) |
| C2 | PSD 는 forward 로 전압/dV 곡선을 결정(다입자 모델); bimodal→double-plateau, narrow unimodal→SPM 소보정 | Kirk·Evans·Please·Chapman 2022, SIAM J. Appl. Math. 82, DOI 10.1137/20M1344305 (arXiv:2006.12208) | 점근해석; PSD 입력→전압 예측; DPM 이 double-plateau 재현 | LFP 예시 중심·흑연 일반화는 모델 구조상 가능 | forward 확립; **역방향 미수행**; narrow PSD 효과는 작음(SPM 보정항) | peak smoothing 을 PSD 만으로 귀속 못함 → **분리 필요성**의 정량 근거 | A(landing/abstract) | 확정(서지·forward 결론) / 역문제 부분은 근거미발견 |
| C3 | 흑연 dQ/dV broad peak = 입자간 **전위 분포**(전극 불균일)이며 "PSD alone" 아님 | Electrochemical profiling, Cell Rep. Phys. Sci. 2023, https://www.cell.com/cell-reports-physical-science/fulltext/S2666-3864(23)00096-6 | 전극 profiling; 0V↑ broad dQ/dV ↔ wide potential distribution among particles | 흑연 음극 직접 | broadening 다원인(불균일·kinetic) — PSD 와 혼입 | **사용자 가설 핵심 약점 직격**: 종모양=반경분포 단정 위험 | A(스니펫) | 추정(스니펫 기반; 본문 미정독) |
| C4 | dV/dQ(DVA) peak 은 PSD 가 아니라 전극 balance/열화 진단용 — PSD 직접 역산 선례 아님 | Bloom et al. 2005, J. Power Sources 139, 295, https://ui.adsabs.harvard.edu/abs/2005JPS...139..295B | half-cell 귀속으로 peak 분해; LLI/LAM 진단 | 흑연 포함 full-cell | PSD 추출 목적 아님 | dV/dQ→PSD 직접 선례 **근거미발견** 의 한 증거 | A(ADS landing) | 확정(기법 목적) / PSD-역산 부재는 근거미발견 |
| C5 | 삽입 등온선·dμ/dx = lattice-gas 자리에너지/상호작용으로 결정 → dQ/dV peak ≈ 자리에너지 밀도 봉우리 | McKinnon & Haering lattice-gas (Solid State Ionics 계열, 검색 확인); Frumkin review Levi&Aurbach, Electrochim. Acta, DOI 10.1016/S0013-4686(99)00202-9 | dμ/dx↔등온선; Frumkin g항↔분포폭 정량 사상 | 흑연 staging 직접 적용 가능 | 해석틀 확립; "분포"=자리/조성 분포(≠반경 자동) | OCV=분포적분 해석틀 확정; **반경분포로 가려면 반경→U_j 매핑(축B/3) 필수** | A(검색 종합) | 확정(해석틀) / 반경 직결은 미검증 |
| C6 | dQ/dV peak = 단일입자 커널 ⊛ 분포 의 역변환은 **ill-posed**, 정규화(Tikhonov) 필수 — DRT 와 동형 | DRT 문헌: Tikhonov for DRT (Wan/Ciucci 계열), e.g. ResearchGate 318040011; ACS Electrochem. DRTtools DOI 10.1021/acselectrochem.5c00334 | 1종 Fredholm; "intrinsically ill-posed, requires regularization"; α 선택이 결과 지배 | 측정원 무관 수학 구조(흑연 dQ/dV 포함) | **유일·안정해 없음**; 정규화/형태가정 의존 | 사용자 deconvolution 의 **ill-posedness 직접 판정 근거(본축 핵심)** | A(스니펫/추상) | 확정(ill-posed·정규화 필요는 수학적 표준+DRT 1차 명시) |
| C7 | 서로 다른 분포가 거의 동일 전압곡선 → 비유일(state-dependent identifiability) | Identifiability of SPM, arXiv:1702.02471; 일반 inverse 논의(검색 종합) | "multiple parameter combos yield nearly indistinguishable voltage-time curves" | 배터리 inverse 일반 | 균일 ill-posed 아닌 **구간의존** 식별성 | 일부 SOC 구간만 반경분포 식별 가능할 수 있음 | A(스니펫) | 추정(스니펫; 본문 미정독) |

---

## 이 축 요약

- **PSD 추출 선례 존재 여부 = "존재하되 조건부".** 전기화학으로 입자 size distribution 을 역추정한 1차 선례는 **diffusion-impedance(EIS) 영역에 명확히 존재**(Song & Bazant 2012, arXiv:1205.6539). 그러나 (i) **형태가정(lognormal 등) + forward-fit** 방식이지 non-parametric 직접 deconvolution 이 아니고, (ii) **dQ/dV·DVA 에서 PSD 를 직접 역변환한 1차 선례는 근거 미발견**(이 축 검색 범위 내). 사용자의 "dQ/dV peak→반경 분포 직접 역변환"은 **신규 시도**에 가까움.
- **가장 강한 근거 DOI:**
  - 역문제 실재 선례: **10.48550/arXiv.1205.6539** (Song & Bazant 2012, PSD from impedance).
  - forward PSD↔전압 정량: **10.1137/20M1344305** (Kirk et al. 2022).
  - ill-posedness 동형 근거: **DRT = 1종 Fredholm, intrinsically ill-posed, Tikhonov 필수** (DRTtools 10.1021/acselectrochem.5c00334 외 DRT-Tikhonov 문헌군).
  - 가설 약점(broadening≠PSD): Cell Rep. Phys. Sci. 2023 (S2666-3864(23)00096-6).
- **역문제 ill-posedness 판정 = ★ ill-posed(확정).** peak=커널⊛분포 는 1종 Fredholm 적분방정식이고, 동일 구조 DRT 가 1차 문헌에서 "intrinsically ill-posed" 로 명시됨. ∴ peak→반경분포 역변환은 **정규화(Tikhonov/MaxEnt) 또는 형태가정 없이는 비유일·불안정**. forward(반경분포→peak)만 well-posed.

## 역변환 성립조건 목록 (사용자 가설이 통하려면 동시 충족)

1. **커널 확정:** 단일입자 본질 dQ/dV(델타 vs 유한폭 종)를 모델·실험으로 먼저 못박을 것. (현 모델은 `w_eff` floor/기본폭 선택에 따라 커널이 1.3 mV~25.7 mV 로 흔들림 → 선결.)
2. **커널 폭 ≪ 분포 폭:** 내재폭이 관측 종폭보다 충분히 좁아야 역변환에 신호가 남음.
3. **반경→U_j 단조·일대일:** (축 B/3 결과 의존) 매핑이 단조여야 분포 보존·유일성.
4. **broadening 원 분리:** kinetic lag(00_scope ★경고: N7/N8)·전극 전위 불균일(C3)·접촉저항·조성 이질성·온도를 **먼저 공제**해야 잔여 broadening 을 반경분포로 귀속 가능.
5. **정규화 또는 형태가정:** non-parametric 직접 deconvolution 대신 Tikhonov/MaxEnt 정규화 또는 lognormal 등 parametric 형태가정 도입(Song&Bazant 처방).
6. **독립 PSD 대조:** SEM 단면·레이저 회절 PSD 와 cross-validate 전까지 미검증 처리.

## 열린 문제

- dQ/dV(전압영역)에서 PSD 를 직접 역추정한 **1차 선례 부재** — EIS 선례를 전압영역으로 이식 가능한지, 커널/적분핵 구조가 옮겨지는지 미검증.
- 사용자 모델의 단일입자 커널이 **진짜 델타냐 floor-clip 극협 종이냐**가 미확정(00_scope §전제) → 커널 미정이면 deconvolution 출발 불가. 이 결정이 본 가설의 선결 게이트.
- broadening 의 정량 분해(반경분포 vs kinetic vs 전위불균일 vs 조성)가 **실측에서 실제로 분리 가능한지** — 비유일성(C7) 상 동일 곡선을 여러 원인이 재현할 수 있어, 분리에는 추가 독립 측정(가변 C-rate, 온도, 단입자 실험)이 필요. (이 분리 판정은 축 6/master 전담 — 본 축 경계 밖, 표시만.)
- ACS Chem. Mater. 2022 (10.1021/acs.chemmater.2c01976, ICA/DVA convolution·broadening 해석)과 Cell Rep. Phys. Sci. 2023 본문은 paywall/미정독 → 본문 정독 시 C3·broadening 정량 보강 가능(현재 abstract/스니펫 tier).
