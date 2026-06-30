# Ch1 v9 — LCO 전자 엔트로피 항 설계 + Ch1 프레임 적용 (Phase A.3, master)

> 입력 = `20_extraction/_SUMMARY.md`(서브 정독, tier 병기). master 종합·설계. ★전자 엔트로피 항(파생 F)·코드 일반화(H)·모델 가정 명시.

## 1. 전자 엔트로피 항 — 닫힌식 (파생 F)
**출발(분포)**: 축퇴 전자기체의 전자 엔트로피는 Fermi–Dirac 분포에서 Sommerfeld 전개로
$$S_e(T,x)\;=\;\frac{\pi^2}{3}k_B^2\,T\,g(E_F,x)\qquad[\text{tier A 식, Reynier·Motohashi}]$$
($g(E_F,x)$ = Fermi 준위 상태밀도, 자리당). **부분몰 전자 엔트로피**(Li 1몰 제거당)는
$$\Delta S_{e}(x)=\frac{\partial S_e}{\partial x}\Big|_T=\frac{\pi^2}{3}k_B^2\,T\,\frac{\partial g(E_F,x)}{\partial x}.$$
탈리튬화(x↓) 시 절연체→metal 천이로 $g(E_F)$ 가 0→13 e/eV 로 증가 ⇒ $\partial g/\partial x<0$ ⇒ Li 제거당 $S_e$ 증가(부호: 양극 ∂U/∂T 에 +기여, MIT 구간 국소).

## 2. ★모델 가정 — g(E_F,x) 의 MIT-logistic 게이트 (G2 해소)
1차 문헌에 **g(E_F,x) 연속곡선 정량 없음**(G2; Motohashi 는 CoO2 의 13 e/eV 단일 anchor + 정성 추세만). Ch1 "문헌값=초기값·데이터로 피팅" 철학 적용 → **MIT 를 logistic 게이트로 근사**:
$$g(E_F,x)\;\approx\;g_{\max}\,\Big[1-\sigma\!\big(\tfrac{x-x_\mathrm{MIT}}{\Delta x_\mathrm{MIT}}\big)\Big],\quad g_{\max}=13\ \text{e/eV},\;x_\mathrm{MIT}\approx0.85,\;\Delta x_\mathrm{MIT}\approx0.05$$
($\sigma$=logistic; x↓ 으로 0→$g_{\max}$ 켜짐, 발현 2상역 x≈0.75–0.94[Reimers·Ménétrier]). ⇒ $\Delta S_e(x)$ = MIT 부근 *국소 양봉우리*(작지만 0 아님). **초기값**(피팅 대상): $g_{\max}$·$x_\mathrm{MIT}$·$\Delta x_\mathrm{MIT}$. step 대신 logistic 채택 사유 = 매끄러운 ∂U/∂T(Ch2 겹침 가중과 일관)·결함농도 의존(발현 x 분산)을 폭으로 흡수.
- ★크기 검산: $S_e/k_B=\frac{\pi^2}{3}(k_BT)g(E_F)=3.29\times0.0259\,\mathrm{eV}\times13/\mathrm{eV}=1.1\,k_B$/atom(완전 metal). O3(부분) 부분몰차 ≈0.18 kB/atom[Reynier B] — 같은 자릿수 ✓. ⇒ "작지만 MIT 게이트로 필수"(config 단독 MIT 2상역 재현 불가[ML 2024 A]).
- ★온도 의존: $S_e\propto T$ ⇒ 전자 기여 ∂U/∂T|_e $=\Delta S_e/F\propto T$ — 다른 항(상수 ΔS_rxn)과 달리 *T-선형*. v9 에 "전자항만 T 의존" 명시(Ch2 가역열로 확장 시 중요).

## 3. ΔS_rxn,j^cat 분해 (LCO 전이별)
$$\boxed{\;\Delta S_{\rxn,j}^\mathrm{cat}(x,T)=\underbrace{\Delta S^\mathrm{config}_j}_{\text{logistic }w=RT/F\text{ 가 담음}}+\underbrace{\Delta S^\mathrm{vib}_j}_{\text{음의 baseline}}+\underbrace{\Delta S_{e}(x,T)}_{\text{MIT 게이트, }\propto T}\;}$$
- config = O3 ΔS 지배(>½)[Reynier A] — 기존 Ch1 logistic 이 자동 생성(중심 표준값 $\Delta S^0_j$ + 봉우리 내부 $R\ln[(1-\xi)/\xi]$). **이중계산 금지**(B): $\Delta S^0_j$=중심 표준값.
- vib = 음의 baseline(phonon, 고-x). Ch1 흑연과 동형.
- $\Delta S_e$ = §2 신규 항(흑연엔 없음, LCO 고유).

## 4. LCO 하프셀 전이 표 (U_j 초기값, tier A=Xia; ΔS=Reynier/Motohashi)
| 전이 | U_j (V vs Li) | x 범위 | 성격 | ΔS_rxn 초기값 | 비고 |
|---|---|---|---|---|---|
| **T1 MIT** | ~3.90 | x≈0.94–0.75 | insulator→metal | config + **ΔS_e 게이트 ON** | 전자항 발현 핵심 |
| **T2 order–disorder a** | ~4.05 | x≈0.55 | hex→monoclinic 정렬 | config 주도(0.47 J/K·mol@x½[Moto A]) | 2상역 |
| **T3 order–disorder b** | ~4.17–4.20 | x≈0.48 | monoclinic→hex | config(1.49 J/K·mol@x⅔) | T2 와 한 쌍 peak |
| (T4 O3→H1-3) | ~4.55 | x≈0.2 | — | — | 고전압, 하프셀 ≤4.2–4.5V 면 *범위 밖*(옵션) |
- 하프셀(코인, ≤4.2–4.5 V) 핵심 = **T1·T2·T3** (3 전이). 흑연 4 전이와 대칭 구조.
- 단전극 dφ/dT≈+0.83 mV/K(≈+80 J/mol·K)[B] = 전체 부호 sanity(양극 양수).

## 5. forward 코드 LCO 일반화 (파생 H — 확정)
★**MSMR $x_j=X_j/(1+\exp[f(U-U_j^0)/\omega_j])$ = Ch1 transition-logistic 동형**[msmr A]. ⇒ Ch1 클래스(func_ksi_eq·func_U_j) 그대로, **(i) 전이 파라미터(GRAPHITE_STAGING_LIT→LCO_STAGING_LIT: §4 표) 교체 + (ii) 전자 엔트로피 항 $\Delta S_e(x,T)$ plug-in** 만으로 LCO 적용. ∂U/∂T←$\partial U_j^0/\partial T=\Delta S_{\rxn,j}/F$ 동일 경로. 구조 변경 0(파라미터+1항).

## 6. 도핑 보정 (우리 시료)
Al³⁺/Mg²⁺ **비-redox**[doping A] → Co redox·전자 엔트로피 항 *보존*(전자항 그대로). 상전이(order–disorder·MIT·O3↔H1-3) **억제** → logistic **폭 $w$ 넓힘·peak smear**·U_j 미세 shift. high-entropy 도핑 site → config 엔트로피 약간 추가. ⇒ pure-LCO §4 값=초기값, 폭·shift 는 우리 데이터 피팅(G4).

## 7. 갭 → 피팅 위임 (round-trip)
- G1 ΔS(x) 연속표·G2 g(E_F)(x)·G3 MSMR LCO 파라미터·G4 도핑 shift = **우리 코인 하프셀 데이터 round-trip 피팅**으로 식별(초기값=§4·§2). G5 ΔH_f 절대값 = OCV plateau(3.9V 등)로 anchor 대체. 전부 Ch1 철학(문헌 초기값+데이터 피팅) 내.

## Gate (A.3)
전자 엔트로피 닫힌식·MIT 게이트 모델 가정·ΔS 분해·LCO 전이표·코드 일반화·도핑 보정·갭 위임 확정. 이중계산 금지(B) 반영. → AUTHOR_BRIEF LCO 칸 채움 → Phase B 9종 빌드.
