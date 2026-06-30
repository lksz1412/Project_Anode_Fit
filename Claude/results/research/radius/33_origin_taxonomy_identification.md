# 축 G — apparent-U 분포 원인의 전수 분류 + 식별·분해 방법

> 작성: 학술 조사 sub (4세션 분업). 배정 축 G 한정. 종합·verdict·타 카드는 master 전담.
> 대상 현상: 흑연 음극 dQ/dV staging peak 의 치우친 종모양(broadening + 비대칭).
> 핵심 전제: 관측 peak 전위 `V_peak = U_j(평형 전이전위) + η(과전압)`. 실측에서 분포하는 것은 평형 `U_j` 가 아니라 **apparent-U = U_j + η** 일 개연성. 본 축은 이 apparent-U 분포를 *전부* 분류하고, 실측에서 *분리*하는 처방을 정리한다.
> 기준 셀: 흑연 코인 하프셀, 입자 5–20 µm, 상온, C/10 ~ 1C.
> tier 규약: A = 본문/식 수준 확인, B = abstract/검색 요약 수준, C = 2차 인용·추정. abstract-only 는 명시·강등.

---

## 소절 1 — apparent-U 분포 원인의 전수 목록 · 상대 중요도 순위

흑연 dQ/dV peak 폭(FWHM)·비대칭에 들어가는 기여를 8 종으로 분리. 각 기작이 만드는 폭은 **독립 기여의 합성**(대략 분산의 합)으로 누적되며, peak 위치 `V_peak` 의 분포로 환원해 비교한다.

### (i) 단일입자 내재(열역학) 폭 — `~RT/F` 스케일
- **물리**: 단상 고용체(solid-solution) 구간에서 `dx/dU` 가 유한 → peak 가 무한히 날카롭지 않다. 이상 고용체면 `dQ/dU` 의 1/e 반폭 ~ `RT/F ≈ 26 mV`(상온), 비이상 상호작용(staging 정렬 에너지)으로 더 좁아지거나(2상 유사) 넓어진다. Nernstian intercalation slope 실측 ~54–58 mV/decade 로 단상 거동의 유한 기울기가 확인된다.
- **흑연 특이성**: 흑연은 대부분 1차 상전이(2상 공존: stage 2↔1, LiC12↔LiC6)라 *내재 평형* 폭은 매우 좁다(이상적으론 δ-함수 한계). 따라서 흑연에서 (i)은 평탄역 양끝의 단상 꼬리·stage 정렬 폭에만 기여 → **하한선(floor)** 역할. 규모 ~ 수~수십 mV.
- 근거: Nernstian Li+ intercalation slope 54–58 mV/dec (PMC8179004); staging 전이 전위차 ~90 mV 보고(1L-4L-3L-2L). tier B.

### (ii) 단일입자 유한율속 꼬리 (고상확산 + charge-transfer)
- **물리**: 유한 전류에서 입자 표면 SOC 가 평균보다 앞서감 → 표면 과전압 `η_ct + η_diff` 가 SOC 따라 변하며 peak 를 **고전위(충전)/저전위(방전) 쪽으로 밀고 비대칭 꼬리**를 만든다. 확산 한정이면 꼬리가 전류·`√(L²/D)` 로 늘어난다.
- **흑연 특이성**: 흑연 D_Li 가 stage 별로 크게 변(2상 경계 이동 = "shrinking annuli"), staging 마다 율속 다름 → stage 3 은 충전 고율서 억제. 비대칭의 주원인 후보.
- 근거: shrinking annuli & stage-dependent rate (arXiv 1211.0027); 고율서 peak 고전위 이동·둔화(Fly/Schaltz/Stroe 2020, 아래). tier A/B 혼합.

### (iii) 입자 크기 kinetic 분산 (PSD-유발 SOC 분산)
- **물리**: 정전류 하 작은 입자가 먼저 차고/빠지며, 큰 입자는 늦음 → 입자군 사이 SOC(따라서 국소 `η`) 가 벌어진다. dQ/dV 는 입자군별 응답의 **합** → peak 가 PSD 폭만큼 broadening·비대칭.
- **정량/모델**: Röder et al. 2016 (Energy Technol. 4(12):1588) — 연속 PSD 를 유한 입자군으로 근사한 다입자(MPM) 전극모델. 방전 말 작은 입자→큰 입자로 전류밀도 이동. 좁은·소형 PSD 가 균질. Heterogeneity → 불균일 표면 과전압·반응속도.
- 근거: DOI 10.1002/ente.201600232 (tier B, abstract+요약). arXiv 2006.12208 (unimodal/bimodal PSD heterogeneity 모델, tier B).

### (iv) 접촉저항/전류분포 이질 (CBD·calendering)
- **물리**: carbon-binder domain(CBD) 분포·calendering 으로 전자/이온 전도도가 입자·위치별로 불균일 → 국소 `iR`/`η` 분산 → peak 폭에 더해짐. 접촉저항은 입자크기 의존.
- **흑연 특이성**: 코인셀 박전극에서도 reaction extent heterogeneity 가 실시간 측정으로 확인됨(전류 유입 비대칭).
- 근거: reaction extent heterogeneity 실시간 모니터(oaepublish energymater.2024.271); CBD inhomogeneity 모델(PMC11304268). tier B.

### (v) 두께방향 SOC 구배 (porous-electrode 반응 분포)
- **물리**: 전해질 이온 수송 한정으로 separator 측이 먼저 반응 → through-plane SOC 구배 → 전극을 가로지른 국소 `η` 분포 → peak broadening. 두꺼운/고로딩 전극·고율서 심화.
- **흑연 특이성**: synchrotron XRD 로 graphite through-plane lithiation gradient 직접 관측(고율 충/방전).
- 근거: heterogeneous lithiation of graphite (arXiv 2005.04983, Wiley/J.Electrochem 계열); in-plane heterogeneous & inverted response (PMC11935889). tier B. **코인셀 박전극·저율(C/10)에선 (v) 기여 작음** → 상대 순위 낮춤.

### (vi) 조성·형태·배향 이질 (intrinsic 물질 분산)
- **물리**: 흑연화도·결정자 크기·edge/basal 노출·배향(AB/ABC stacking) 차이로 입자별 *참 전이전위* 와 staking 안정도가 미세하게 다름 → 평형 수준에서도 약간의 U 분산. Voltage hysteresis 가 meta-stable carbon stacking 과 연결.
- 근거: voltage hysteresis & meta-stable carbon stackings (RSC DOI 10.1039/D0TA10403E, open html); intercalation in single microcrystals (PMC5719043). tier B.

### (vii) 온도
- **물리**: `RT/F` 항(↑T → 내재 폭↑) + 확산계수 활성화(↑T → kinetic 꼬리↓)로 **상반** 작용. 온도 의존이 (i) vs (ii)의 분리 신호가 됨(아래 소절 2).
- 근거: entropy/enthalpy of Li intercalation (DOI S0378775303002854). tier B.

### (viii) 참 열역학 U 분포 (평형 이질성)
- **물리**: 위 (i)~(vii) 를 모두 제거(완전 평형·균질)해도 남는, 활물질 자체의 평형 전이전위 분포. 본 프로젝트 사용자가 "정확한 원인 모름" 이라 한 항목. **거의 0 에 수렴할 것**이 본 축의 잠정 결론 — 흑연 1차 상전이는 평형서 매우 좁아야 하므로, 실측 폭의 대부분은 (ii)~(v) kinetic·heterogeneity 로 흡수됨.

### 순위 (코인 하프셀 5–20 µm, 상온, C/10~1C)
1. **(ii) 단일입자 유한율속 꼬리** — 비대칭의 1차 원인, C-rate 로 직접 제어됨.
2. **(iii) PSD kinetic 분산** — broadening 의 1차 원인, 율 의존.
3. **(i) 내재 RT/F 폭** — floor(하한). 평형서도 남는 ~RT/F.
4. **(iv) 접촉/전류분포 이질** — 중간. 박전극서도 비0.
5. **(vi) 조성·배향 이질** — 평형 잔여 폭에 기여.
6. **(v) 두께 SOC 구배** — 코인 박전극·저율서 작음(고로딩서 급상승).
7. **(vii) 온도** — 폭의 분리 변수(원인이자 진단 lever).
8. **(viii) 참 U 분포** — 잠정 ~0 (가장 약한 후보).

---

## 소절 2 — ★ 식별·분해 방법 (어느 lever 가 어느 원인을 집어내는가)

목표: 위 8 원인을 실측에서 *분리*해 "이 셀 종모양의 지배 원인" 을 확정.

| 분리 lever | 변화시키는 것 | 사라지면/줄면 → 지목 원인 | 변치 않으면 → 지목 원인 |
|---|---|---|---|
| **C-rate sweep** (C/48→1C) | 과전압·확산 꼬리 | (ii)(iii)(iv)(v) **kinetic 전부** | (i)(vi)(viii) **평형/내재** |
| **GITT / 근평형 잔여폭** | 모든 `η`→0 | — (잔여폭 = 평형 이질성 **상한**) | 잔여폭 = (i)+(vi)+(viii) 합 |
| **온도 sweep** | RT/F 항 ↑ & D 활성화 | 폭↓(승온) → (ii)(iii) 확산지배 | 폭↑(승온)·RT/F 추종 → (i) 내재 |
| **전극 두께/로딩** | through-plane 구배 | 폭↓(박막화) → (v) | (v) 비기여 |
| **단일입자 vs 다입자** | PSD·전극 이질 제거 | 단입자서 폭↓ → (iii)(iv)(v) | 단입자서도 폭 잔존 → (i)(ii)(vi) |
| **DRT (EIS)** | 시간상수 분해 | charge-transfer/diffusion/contact peak 분리 → (ii)(iv) 정량 | — |

### 핵심 식별 논리
- **C-rate 의존성 = 1급 분리기**: 저율(C/48 근방)서 사라지는 폭 = kinetic((ii)~(v)). 남는 폭 = 평형/내재((i)(vi)(viii)). Fly/Schaltz/Stroe 2020: C-rate↑ → peak 고전위 이동·둔화, C/6 이상서 식별 peak 수 감소; **resistance correction** 으로 C/6 peak 위치를 C/48 대비 0.59% 내 예측(보정 없으면 1.90%) → kinetic 성분이 저항으로 환원 가능함을 입증.
- **GITT 근평형 잔여 폭 = 평형 이질성의 *상한***: 펄스 후 완전 이완 OCV 로 그린 dV/dQ 의 잔여 폭이 (i)+(vi)+(viii) 합의 측정 상한. 이것이 작으면 → 실측 종모양은 거의 전부 kinetic.
- **온도 = (i) vs (ii) 분리**: 승온 시 RT/F 폭은 *넓어지고* 확산 꼬리는 *좁아진다*(상반). 폭의 온도 부호가 지배 항을 지목.
- **단일입자 측정**(미소전극/단결정) = (iii)(iv)(v) 제거 → 남는 폭이 진짜 단입자 내재((i)(ii)(vi)). intercalation in single microcrystals (PMC5719043)·thin-layer graphite (1211.0027) 가 이 대조의 근거.
- **DRT** = `η` 의 *종류* 분해: charge-transfer / 고상확산 / 입자-입자·접촉 저항 peak 를 시간상수로 분리 → (ii)와 (iv)를 정량 구분.

---

## 소절 3 — 모델 매핑 (단일 유효입자 + kinetic lag `L_V` 구조에 apparent-U 분포 넣기)

사용자 forward 모델 = **단일 유효입자 + kinetic lag `L_V`(∝ 전류)**. 이 구조에 위 분포를 넣는 3 경로:

### 경로 A — 과전압 분포 항 (가장 단순)
- SPM 의 평형 `U_j(x)` 에 전류 비례 lag `L_V = R_eff · I`(이미 모델에 존재) + **분포 폭 항** `σ_app(I,T)` 를 추가: `V_peak = U_j + L_V(I) ± (폭 합성)`. 폭 합성 = √(σ_i² + σ_ii²(I) + σ_iii²(PSD) + …).
- 장점: 단일입자 골격 유지. 단점: 비대칭(꼬리)을 대칭 `σ` 로 근사 → (ii) 비대칭 손실.

### 경로 B — 입자 크기 분포 위 합성곱 (SPM→MPM)
- 단일 유효입자 응답 `f(V; r)` 를 PSD `g(r)` 로 **합성곱**: `dQ/dV|관측 = ∫ g(r) · f(V; r) dr`. 작은 r → peak 좌측, 큰 r → 우측 → 자연스러운 비대칭·broadening. Röder 2016·arXiv 2006.12208 의 다입자군(MPM) 근사가 이 구조의 문헌적 토대(연속 PSD → 유한 입자군 합).
- (iii) PSD kinetic 분산을 *직접* 재현. (ii) 단입자 꼬리는 각 `f(V;r)` 에 charge-transfer/diffusion 모델로 내장.

### 경로 C — 완전 P2D/MPET (참조 상한)
- through-plane (v) + 전류분포 (iv) 까지 필요하면 porous-electrode(P2D) 또는 MPET 로 확장. 코인 박전극·저율에선 과잉 → 본 forward 모델 목적엔 경로 B 가 비용-정확도 최적.

### 처방
- **최소 확장 = 경로 B(PSD 합성곱) + 각 입자에 (ii) charge-transfer/diffusion lag**. 이로써 지배 2 원인((ii)(iii))을 물리적으로 재현하고, (i)은 `U_j` 의 RT/F 유한기울기로 자동 포함. (iv)(v)는 잔차로 남겨 두께/로딩 실험으로 사후 보정.

---

## 원인 순위 매트릭스

| 원인 | 식별 신호(주 lever) | 흑연 mV 규모(코인 박전극) | C-rate 의존 | 대표 문헌 (DOI/URL) | 분리법 |
|---|---|---|---|---|---|
| (ii) 유한율속 꼬리 | C-rate↑서 비대칭↑ | 수십~100+ mV (고율) | **강** | Fly/Schaltz/Stroe J.Energy Storage 2020 29:101329, 10.1016/j.est.2019.101329; 1211.0027 | C-rate sweep, DRT |
| (iii) PSD 분산 | 단입자 대조서 폭↓ | 수십 mV (PSD폭 비례) | 강 | Röder 2016 10.1002/ente.201600232; arXiv 2006.12208 | 단입자 vs MPM, PSD 측정 |
| (i) 내재 RT/F | 온도 따라 폭↑ | ~26 mV (RT/F) + staging | 약(평형 floor) | Nernstian: PMC8179004; staging 90 mV | 온도 sweep, GITT |
| (iv) 접촉/전류분포 | DRT contact peak | 수~수십 mV | 중 | energymater.2024.271; PMC11304268 | DRT, calendering 대조 |
| (vi) 조성·배향 이질 | 평형 잔여폭 | 수~수십 mV | 약 | RSC 10.1039/D0TA10403E; PMC5719043 | GITT, 단결정 |
| (v) 두께 SOC 구배 | 두께↓서 폭↓ | 박전극 작음(고로딩 ↑) | 강(고로딩) | arXiv 2005.04983; PMC11935889 | 두께/로딩 변화 |
| (vii) 온도 | 폭의 T-부호 | (분리 lever) | — | 10.1016/S0378-7753(03)00285-4 | 온도 sweep |
| (viii) 참 U 분포 | GITT 잔여(잠정~0) | ~0 (추정) | 없음 | (귀무 후보) | GITT 상한 |

> mV 규모는 문헌 정성+RT/F 스케일에서 추정한 order-of-magnitude (tier B/C). 정밀값은 master 통합 시 셀별 재산정 필요.

---

## 이 축 요약: 흑연 종모양의 지배 원인 순위 · 분해 처방 · 열린 문제

**지배 원인 순위 (코인 하프셀 5–20 µm, 상온, C/10~1C)**
1. **유한율속 꼬리(ii)** — 비대칭의 주범, C-rate 직접 제어.
2. **PSD kinetic 분산(iii)** — broadening 의 주범, 단입자 대조로 분리.
3. **내재 RT/F 폭(i)** — 평형 floor(~26 mV + staging).
4~ 접촉/전류분포(iv) > 조성·배향(vi) > 두께 구배(v, 박전극서 소) > 온도(vii, lever) > **참 U 분포(viii) ≈ 0 (가장 약한 후보)**.
→ **결론: 실측 종모양의 대부분은 평형 U_j 분포가 아니라 kinetic + heterogeneity 가 만든 apparent-η 분포.** 사용자의 "U_j 분포 원인 미상" 은 대체로 (viii)이 작고 (ii)(iii)이 큰 것으로 재해석됨.

**실측 분해 처방 (확정 가능 조건)**
- **C-rate sweep (C/48→1C)**: 저율서 사라지는 폭 = kinetic, 남는 폭 = 평형/내재. (1급 분리기)
- **GITT 근평형 잔여 dV/dQ 폭**: 평형 이질성((i)+(vi)+(viii))의 **상한** 측정.
- **온도 sweep**: 폭의 부호로 (i) RT/F vs (ii) 확산 분리.
- **단입자 vs 다입자 + DRT**: (iii)(iv)(v) 제거·`η` 종류 분해.
- **모델**: 경로 B = **단일 유효입자 응답을 PSD `g(r)` 위로 합성곱** + 각 입자 charge-transfer/diffusion lag → 지배 2 원인 직접 재현, (i)은 `U_j` RT/F 기울기로 자동 포함.

**가장 강한 DOI**
- **Fly, Schaltz, Stroe, J. Energy Storage 2020, 29:101329 — `10.1016/j.est.2019.101329`** (rate dependency of ICA; C-rate→peak 이동·둔화 정량, resistance correction). C-rate 분리기의 1차 근거.
- 보강: **Röder et al., Energy Technol. 2016, 4(12):1588 — `10.1002/ente.201600232`** (PSD→전극 응답 MPM 모델).

**열린 문제 (master 종합용)**
- (viii) 참 U 분포 = 0 가정의 검증: GITT 잔여폭이 실제로 RT/F floor 까지 내려가는지 본 셀에서 미확인.
- mV 규모표는 tier B/C 추정 — 셀별 정량 재산정 필요.
- 경로 B 합성곱에서 (ii) 비대칭을 입자별 모델로 충분히 잡는지 vs (iv)(v) 잔차로 남는지 분해 미확정.
- abstract-only 강등 항목: Röder 2016, arXiv PSD/heterogeneity, DRT 적용 사례는 본문 식 수준 미확인(tier B).
