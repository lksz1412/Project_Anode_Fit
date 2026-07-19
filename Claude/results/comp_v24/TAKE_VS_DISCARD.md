# 가져갈 것 vs 버릴 것 — 실검증 최종 판정 (v1.0.24, C·A·B 완료)

> 사용자 요구: "진짜로 가져갈것, 버릴것 제대로 분간." 문헌 방향성(LIT_ADVANCE_SYNTHESIS)을 우리
> 데이터로 실검증(C 일관성·A LCO데이터·B 상성격)한 뒤의 **확정 판정**. 문건·코드 무수정(반영은 사용자 "가자").
> 근거 산출물: `regsol2`·`consistency2`·`regsol_si`·`lco_phase`(.py/.png/.json)·`lit_raw/`·`lco_data/`.

---

## 0. 한 줄 판정
| 후보 | 판정 | 근거(실검증) |
|---|---|---|
| 흑연 두-상 = 정칙용액 Ω>2RT(sharp) 시드 | **★가져갈것** | regsol2: Ω_j/RT=[4.06,2.02,3.55,4.07] 전부>2RT·Cordoba DFT 2.5RT 정합 |
| 단일 물리셋(전역/제약 피팅) 일관성 | **★가져갈것** | consistency2: 단일셋 R² 페널티 ~2%·부트스트랩 sharp피크 ±0.07mV |
| 실측 U_j·ΔS_j 시드(Paul2024 등) | **★가져갈것** | 5-6 gallery 실측 U_j·ω_j·dU/dT 확보 |
| Si = 고용체(broad, 소수 gallery) | **★가져갈것** | regsol_si: Si 폭/(RT/F)=[1.45,2.74,1.09]≳1 |
| LCO 3-feature 3-물리(두-상+order-disorder) | **★가져갈것** | lco_phase: 실측 O2 3.70V 두-상(0.34·RT/F)+order-disorder |
| near-delta = 정칙용액+Maxwell⊗kinetic | **◐조건부** | regsol2: R² +0.5%만(물리성↑·R²는 미미) |
| Si에 sharp 두-상/near-delta 강요 | **✗버릴것** | Si 전 feature 폭≳RT/F=고용체(두-상 아님) |
| 흑연 전이 6+ 증설 | **✗버릴것** | XRD 미지원 curve-fitting |
| DFT 결합E(0.41eV)를 Ω로 대입 | **✗버릴것** | 면내 bare=반발(ordering), 상분리 아님 |
| LCO ΔS_e 전자항 크게 | **✗버릴것** | Reynier2004: 전자엔트로피 작음(config 지배) |
| 해석 O3-LCO를 실측처럼 신뢰 | **✗버릴것** | lco_phase: O3 2소스 폭 10× 불일치(위치만 정합) |

---

## 1. ★ 가져갈 것 (TAKE — 실검증 완료)

### T1. 흑연 두-상 = 정칙용액 Ω>2RT sharp 시드 — 파라미터 물리성·일관성 때문
- **검증(regsol2)**: 출하 흑연 dQ/dV 4전이를 정칙용액(Ω>2RT+Maxwell⊗kinetic)으로 피팅 → **Ω_j/RT=[4.06, 2.02, 3.55, 4.07] 전부 >2RT(두-상 확증)**, Cordoba 2024 DFT 앵커(Ω_a≈2.5RT) 정합. 0.140V 전이만 Ω=2.02(임계 바로 위=최대 고용체성) = **Dahn 4↔3 고용체 예외와 독립 일치**.
- **왜 가져가나**: 사용자 핵심요구=파라미터의 물리적 의미·일관성. 정칙용액은 폭이 다른 피크들을 **단일 해석가능 Ω**로 통일; 로지스틱은 w=37mV(비물리)~1.3mV로 뒤섞여 해석불가·0.227V 피크 놓침.
- **반영형태**: 폭 시드를 Ω>2RT 기준으로(두-상 sharp), 실측 U_j·ω_j(Paul2024)로 초기화. **near-delta 자체의 R² 극적개선은 기대 X**(T5 참조).

### T2. 단일 물리셋 일관성(전역/제약 피팅) — 산업 방어력의 핵심 해답
- **검증(consistency2)**: 동일소재 2셀에 U_j·w_j 공유 전역피팅 → R²=0.917/0.924(자유 0.938/0.936 대비 **페널티 ~2%**). **하나의 물리셋으로 전 셀 설명** = 조건마다 재피팅 불요 = 산업사용.
- **비일관의 정체 = 피팅 규율**: 규율(seed+bound+일관추출) 프로토콜서 셀간 w 산포 **3–10%**(무규율 런의 178% 아님). → 사용자가 걱정한 비일관은 **모델 결함 아닌 절차 문제**, 문헌 프로토콜(Hu-Schwartz·PyBOP)로 해결.
- **부트스트랩 UQ**: sharp 두-상 피크(0.142/0.105V) **±0.07mV·CV 3–5%**(매우 신뢰), broad dilute(0.181V) 축퇴(±3.2mV·CV 19%). → **믿을 파라미터=sharp 두-상**.
- **반영형태**: 소재당 단일 물리셋 + 신뢰구간 보고 + stoich 정렬 선행(Lu-Trimboli).

### T3. 실측 U_j·ΔS_j 시드
- **확보**: Paul2024 MCMB/상용 5-6 gallery U_j·ω_j·dU_j/dT; Cordoba Ω; Reynier/Koch ΔS(x). 흑연 U_j 화학불변(consistency2 P3: 0.143V σ=1.6mV).
- **반영형태**: 문건 GRAPHITE_STAGING_LIT 시드를 실측값으로 교체·검증(범위 시드로, MCMB≠임의흑연 주의).

### T4. Si = 고용체(broad, 소수 gallery) + LCO 3-feature 3-물리
- **Si(regsol_si)**: 폭/(RT/F)=[1.45,2.74,1.09] 전부≳1 = 고용체. 흑연 두-상(≪0.12)과 20-50× 분리. → Si-host는 소수 broad gallery(연속 고용체).
- **LCO(lco_phase)**: 실측 O2 3.70V 두-상 sharp(0.34·RT/F)+4.15V order-disorder(0.68·RT/F). LCO는 흑연·Si 사이 혼재 → **feature별 다른 물리**(두-상 sharp / order-disorder broad) 필요.

## 2. ✗ 버릴 것 (DISCARD — 실검증으로 기각)

### D1. Si에 sharp 두-상/near-delta 형태 강요 → 물리 오모델
- **근거(regsol_si)**: Si 전 feature 폭≳RT/F(고용체). δ 물리캡시 Ω 바닥(0.2RT)까지 = "더 broad 원함". a-Si=단일상(Chevrier-Dahn·Artrith). → Si를 sharp 두-상으로 모델하면 존재않는 staging 피크 주입.

### D2. 흑연 전이 6+ 증설 → curve-fitting
- **근거**: XRD(Dahn1991)=두-상 4개만. 6+는 물리 위반(기존 판정 유지·GRAPHITE_STAGING_XRD).

### D3. DFT 쌍결합E(0.41eV)를 정칙용액 Ω로 직접 대입
- **근거**: Pande-Viswanathan 면내 bare 상호작용=**반발**(ordering/초격자), 상분리 아님. 유효 상분리 Ω는 창발(탄성+staging)≈2.5RT(Cordoba). 0.41eV 대입은 물리 오류.

### D4. LCO ΔS_e(전자항) 크게 가중
- **근거**: Reynier2004 — LCO 엔트로피는 config 지배·phonon 큼·**전자 작음**. ΔS_e 크게 넣으면 config+phonon 이중계상. → 작은 bound 보정으로만.

### D5. 해석 O3-LCO를 실측처럼 신뢰
- **근거(lco_phase)**: O3 해석 2소스(Marquis·Ramadass) 위치는 정합(3.909/3.891V)이나 **폭 10× 불일치**(near-delta vs broad). 해석fit은 phase-character(폭) 판정 불가.

### D6. 비대칭 peak 커널 창시 후 "문헌근거" 주장 / Bazant PDE를 생성기로
- **근거**: 흑연 비대칭 폐형 커널 미발표(창시=우리 몫, 문헌 아님). Bazant/Dreyer=PDE(회피대상)·물리 정당화로만 인용.

## 3. ◐ 조건부 / 선검증 (CONDITIONAL)

### C1. near-delta = 정칙용액+Maxwell⊗kinetic
- **검증(regsol2)**: R² 0.938→0.943(+0.5%, **미미**). near-delta 천장은 실재하나 자유폭 로지스틱이 이미 커널로 대부분 맞춤.
- **판정**: **R² 위해선 채용 불필요**(비용>편익). **파라미터 물리성(Ω) 위해선 T1로 채용**. 즉 "near-delta 닫기"가 목적이면 조건부(값싼 개선 아님), "Ω 물리성"이 목적이면 T1.

### C2. Si 히스테리시스 분리 U_j branch / c-Li₁₅Si₄ 1차항 / LCO R_n(x)
- **선검증 필요**: 히스테리시스 branch(Köbbing)는 GITT 이력 데이터로, Li₁₅Si₄는 1차 심리튬 데이터로, R_n(x)는 >4.4V 율데이터로 각각 검증 후.

## 4. 데이터 현실 (정직 — A 결과)
- **흑연/Si**: 실측 확보·검증완료(SINTEF Zenodo 20086298).
- **LCO 실측 O3 numeric = 공개 부재**(LiionDB DNS死·Zenodo/CAMP LCO 결여·SINTEF셋 LCO 없음·Reynier2004/Hudak2014 그림전용). 가용=실측 O2(Carlier2002, 폴리타입 상이)+해석 O3(Marquis·Ramadass·Moura). → **실 O3 검증 유일경로=Reynier/Hudak 그림 WebPlotDigitizer 디지타이즈**(조작 금지 하 정당). 보존: `lco_data/`.

## 5. 반영 우선순위 (사용자 "가자" 시)
1. **T2 일관성**(산업 방어력 최대) — 소재당 단일 물리셋 + UQ 프로토콜.
2. **T1·T3 흑연 Ω>2RT 물리 시드** — 실측 U_j·ΔS·Ω 반영(파라미터 해석성).
3. **T4 Si/LCO 물리 분리** — Si=고용체·LCO=feature별.
4. **C 조건부** — GITT/율 데이터 확보 후 히스테리시스·R_n(x).
5. **LCO 실 O3** — 그림 디지타이즈(별도 승인).
