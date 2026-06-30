# Ch1 v9 LCO — 정독-추출 SUMMARY (Phase A.2 서브 산출)

> 9개 추출카드 종합. ★수치는 출처·tier 병기. 종합·설계·초안은 master(이 서브는 추출만).
> 정독: full(pdftotext 본문) = Motohashi 2009·Xia 2007·ML 2024·PMC7825324(도핑)·PyBaMM MSMR식. abstract+다중-cross = 나머지(원논문 유료/gated).

## 문헌 × 핵심 1줄 × tier

| key | 축 | 핵심 1줄 | 정독 | tier(핵심값) |
|---|---|---|---|---|
| **motohashi_2009** | C2★ | **D(E_F)=13 e/eV(CoO2)**; charge-order ΔS=0.47(x½)/1.49(x⅔) J/K·mol; dV/dx dip x=0.94–0.75/0.55/0.48/0.36/0.25–0.12; Pauli↔Curie-Weiss xc=0.35–0.40 | **full** | A |
| **xia_ceder_2007** | C3★ | dQ/dV: **3.9 V=MIT, 4.05–4.20 V=order–disorder(x≈½), 4.55=O3→H1-3, 4.62=H1-3→O1**; D_Li max@x≈0.4 | **full** | A |
| **reynier_yazami_2004** | C1·C2★ | ΔS_lith max **~9.0 kB/atom(overall)·~4.2(O3내)**; **★전자 ΔS_e≈0.18 kB/atom(x=0.833,LDA)**; config>½ 지배; $S_e\propto T g(E_F)$ | abstract+cross | A(ΔS)/B(0.18) |
| **ml_orderdisorder_2024** | C2★ | x≈½ order–disorder **Tc>330 K**; ★**config 만으론 MIT 2상역(x≈0.7–0.9) 재현 불가→전자항 필수** | **full** | A |
| **reimers_dahn_1992** | C2★·C3 | 3 전이(x:1→0.4), x≈½ order–disorder(hex→monoclinic), x≈0.75–0.93 **MIT 2상역** (정설 seminal) | abstract+cross | A(구조)/B(수치) |
| **menetrier_delmas_1999** | C2★ | MIT(국재→비국재 전자)=**2상역 driving force**; 발현 **x=1−δ(δ≪1)**, 결함민감 | abstract+cross | A(본질)/C(전도도) |
| **msmr_partI_II_2024** | C6·L5★ | **$x_j=X_j/(1+\exp[f(U-U_j^0)/\omega_j])$** = Ch1 transition-logistic 동형; ∂U/∂T←Uⱼ⁰(T); 양극 적용선례 | MSMR식 full | A(식)/C(수치) |
| **reynier_thermal_2009** | C1·C4 | LCO dφ/dT≈+0.83 mV/K(단전극); ΔS 70–120 J/mol·K; **LCO ΔS≫NMC/LFP**; heat +51/−46 kJ/mol | abstract+cross | A(≫)/B(수치) |
| **enthalpy_formation** | C2·C4 | ΔH_f 선형↓(x↓ 불안정); **monoclinic Li0.5CoO2 > undistorted O3 안정** | abstract+cross | A(정성)/C(절대값) |
| **high_entropy_doping** | C5 | **Al³⁺·Mg²⁺ 비-redox**(작은반경→격자압축·낮은원가→hole trap)→O3↔H1-3 상전이 억제; La-Al-Mg-Y high-entropy 4.6 V 안정 | PMC full+abstract | A(기구)/C(정량) |

## ★4 우선 추출 타깃 — 확보 현황

**(a) 전자 엔트로피 식·크기·발현 x** — ★확보:
- 식: $S_e \simeq \dfrac{\pi^2}{3}k_B^2\,T\,g(E_F)$ (Sommerfeld, 축퇴 전자기체). [Reynier LDA·Motohashi]
- 크기: O3 내 전자 ΔS_e **≈0.18 kB/atom @x=0.833** (Reynier, tier B); g(E_F)**=13 e/eV @CoO2** (Motohashi, tier A).
- 발현 x: MIT 2상역 **x≈0.75–0.94**(절연체 x≈1, g(E_F)≈0 → metal x↓, g(E_F)↑). 발현 onset **x=1−δ**(Ménétrier). 전자항은 이 구간에서 "켜짐".
- ★정당화: config stat-mech 단독으로 MIT 2상역 재현 불가(ML 2024) → 전자항 **독립 필수**.

**(b) LixCoO2 ΔS(x) 정량** — 확보:
- ΔS_lith max **~9.0 kB/atom(overall, 0.5<x≤1)·~4.2 kB/atom(O3 내)** [Reynier, A]. config>½ 지배, phonon=음의 baseline, 전자=작음(0.18).
- charge-order 전이 ΔS **0.47(x½)/1.49(x⅔) J/K·mol** [Motohashi, A] vs 이상 mixing 5.76/5.29.
- 단전극 dφ/dT≈**+0.83 mV/K** [thermal_2009, B]. (단위 환산: 1 mV/K ≈ 96.5 J/mol·K)

**(c) dQ/dV 전이 위치·plateau (U_j 초기값)** — ★확보(tier A):
- **3.9 V = MIT**, **4.05–4.20 V = order–disorder(x≈½, 2 peak)**, 4.55 V=O3→H1-3, 4.62 V=H1-3→O1 [Xia, A]. Ch1 하프셀(≤4.2–4.5 V) 핵심 = **3.9 + 4.05–4.20 V (2~3 전이)**.

**(d) 도핑이 ΔS/상전이에 주는 변화** — 부호·기구 확보(정량 미확보):
- Al³⁺/Mg²⁺ 비-redox → Co redox/전자 엔트로피 항 보존; 상전이(order–disorder·MIT·O3↔H1-3) 억제→logistic 폭·U_j 보정. high-entropy 화→도핑 site config 엔트로피 추가. [doping, A 기구 / C 정량]

## 상충(conflict)

1. **MIT 발현 x**: 통상 인용 "x≈0.94"(Reimers·Motohashi dV/dx dip 상한) vs Ménétrier "x=1−δ(δ≪1)". → **결정 결함 농도 의존**(Motohashi 가 명시 해소): 고화학량 시료일수록 빠름. 우리 시료는 dip 상한 x≈0.94 부근을 실용 기준.
2. **전자 엔트로피 비중**: master 가설("tilde ~9 kB/atom 에 전자 기여 큼") vs Reynier 실측("O3 내 전자항 ~0.18 kB/atom로 작음, config 가 지배"). → **해소**: 전자항은 O3 평균으론 작으나 **MIT 2상역에 국소 집중**(g(E_F) 급변). overall 9.0 의 큰 폭은 고전압 전이+config, O3 4.2 는 config 주도. *전자항은 "작지만 MIT 게이트로 필수"*가 정확한 framing.
3. **엔트로피계수 부호 프로파일**: 단전극 LCO dφ/dT 양(+, 0.83) vs 전셀(LCO−Gr) 부호전환(−0.37~+0.1 mV/K). → 전셀은 graphite 항 합산 — **Ch1 LCO 하프셀(vs Li)은 단전극 LCO 만** 적용(혼동 주의).

## 공백(gap) — master A.3 종합 시 보완 필요

- **G1**: ΔS(x) **연속 곡선 수치표**(J/mol·K vs x, 0.5–1.0) 미확보 — Reynier/thermal full-text 유료. peak 위치·폭 정량 없음(전이 위치만). → 우리 데이터 round-trip 피팅으로 식별 or 추가 open 소스.
- **G2**: g(E_F)(x) **연속 함수** 미확보 — Motohashi 는 x=0(13 e/eV)·정성 추세만. 중간 조성 g(E_F) 보간 필요(전자 엔트로피 x-게이트 정량화).
- **G3**: MSMR LCO **파라미터(Xⱼ,Uⱼ⁰,ωⱼ,∂Uⱼ⁰/∂T)** 직접값 없음(graphite 만) — 우리가 Xia 전이 위치+Reynier ΔS 로 채워야.
- **G4**: 도핑 **정량 shift**(ΔU_j, ΔS 변화 %) 미확보 — 우리 시료 피팅으로 식별.
- **G5**: ΔH_f **절대 kJ/mol** 미확보(Wang&Navrotsky 유료) — U_j 절대 anchor 는 OCV plateau(3.9 V 등)로 대체 가능.

## 가장 불확실 1곳

**전자 엔트로피의 정량적 x-프로파일** (G2): 식($S_e\propto T g(E_F)$)·O3 평균크기(0.18 kB/atom)·단일 anchor(g(E_F)=13 e/eV @CoO2)는 확보됐으나, **g(E_F)(x) 연속곡선**(절연체 x≈1 의 0 → metal x↓ 의 13 e/eV 로의 천이 형태)이 1차 문헌에 정량으로 없음. 전자 엔트로피 항을 forward 에 plug-in 할 때 이 x-천이(MIT logistic 형태로 근사할지 step 으로 할지)가 가장 미검증 — master A.3 에서 모델 가정으로 명시 필요.
