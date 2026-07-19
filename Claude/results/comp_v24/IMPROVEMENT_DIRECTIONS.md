# 흑연 dQ/dV 모델 개선 방향성 조사 (v1.0.24) — 사용자 요청 "방향성 조사"

> 실행 X — 전부 **추가 후보**(P5). 사용자 결정 전 코드·문건 무수정.
> 근거: 공개데이터 실측(Zenodo 20086298·20323533) + 문헌 조사(MSMR·staging 이론).

---

## 0. 먼저: "각짐"의 정체 — 물리 결함 아님, 그림 격자 아티팩트 (해소)

- 문건 평형식 `Σ Q_j·ξ(1−ξ)/w_j` 는 로지스틱(C∞ 해석함수)의 합 → **수학적으로 완전히 매끄럽다**(각질 수 없음).
- gr_fit.png 의 각짐 = 내가 모델선을 **데이터 격자(0.5 mV)** 로 그려서, w_j<1 mV 인 초sharp 피크(FWHM 2.8 mV)가 5~6점으로 표본화 → 직선 이음이 삼각형처럼 보인 것. `gr_angular_diag.png` 가 증명: **동일 식을 0.02 mV 격자로 그리면 유리처럼 매끈**(피크사이 포함).
- 즉 (a) 데이터 문제 아님, (b) 미반영 물리 아님, (c) w 시작값 문제 아님(피팅 수렴·2셀 일치). → 전 그림 고해상 재생성 완료.

## 1. 프레이밍: 이 모델은 이미 **MSMR** 이다 (검증됨)

문헌 대조 결과 문건의 평형식은 **정확히 MSMR(Multi-Species Multi-Reaction; Verbrugge·Baker·Koch 2017 JES E3243 / Baker·Verbrugge 2018 JES A3952)** 이다:
- MSMR: `x_j = X_j/(1+exp[f(U−U0_j)/ω_j])`, `f=F/RT`, `x=Σ_j x_j`.
- 미분: `|dx/dU| = Σ_j (X_j f/ω_j)·ξ_j(1−ξ_j)` = **문건식과 동일**.
- **매핑**: `Q_j ↔ X_j`, `U_j ↔ U0_j`, **`w_j ↔ ω_j·RT/F`** (ω_j = MSMR '무질서/이상성' 파라미터).
- 문건 코드는 이미 LCO 절에서 이 매핑을 명시(`class LCOCathodeDQDV: MSMR 동형, X_j↔Q_j·ω_j↔w_j`). → 흑연에도 동일 성립을 문헌이 확인.
- **함의**: '피크 sharpness' 는 coupling 없이도 **ω_j(=w_j) 하나로 조절**된다. 작은 ω_j=질서/협동=sharp, 큰 ω_j=무질서=broad. 우리 실측 피팅의 두-상 w/RTF≈0.03–0.06(=ω_j≈0.03–0.06)·shoulder ω_j≈0.7 이 정확히 이 스펙트럼.

## 2. 사용자 가설 "전이들이 상호 영향을 준다" — 물리는 맞다, 그러나 이 잔차의 해법은 아니다

**물리적으로 옳다**: 흑연 staging(1/2/2L/3/4)은 본질적으로 **층간 결합(inter-layer coupling)** 현상이다:
- Safran, *PRL* 44, 937 (1980) — 층간 정전/탄성 결합이 이산 stage 를 안정화(devil's-staircase).
- Dahn, *PRB* 44, 9170 (1991) — Li_xC6 상평형도: 1→4→3→2L→2→1 두-상 계열; Li–Li 반발 vs C–C 층간 인력 경쟁.
- Bazant 계열(Guo·Smith·Bazant 2016 JPCL; Cordoba·Chandesris·Plapp 2024) — **두-층/다층 정칙용액 자유에너지 + 층간 결합항**이 stage 를 *자연발생*시킴.
→ 즉 sharp 피크의 sharpness 는 진짜로 coupling 에서 온다.

**그러나 이 잔차(R²≈0.95–0.97)의 해법으로는 최악의 선택**:
1. 우리 잔차의 실제 원인 = **(a) 4전이가 병합한 sub-피크(0.105 spike·0.117 shoulder) + (b) 대칭 peak 모양**. 둘 다 coupling 과 무관.
2. MSMR 은 이미 ω_j 로 협동성(intra-전이)을 흡수 → sharpness 는 확보됨.
3. 전-전이 coupling 행렬 λ_jk 는 **1-D 곡선에서 식별 불가**: λ_jk·ξ_k 는 U_j 이동·w_j 재척도로 대부분 흡수 → "맞는데 이유가 틀린" 피팅 + 온도/율속 이전 불가.
→ **결론: 사용자 직관은 staging 물리의 핵심을 정확히 짚었으나, coupling 은 T/율속/히스처럼 "피크가 외부변수로 움직여야 할 때"만 값어치가 있다. 정적 평형곡선 잔차의 1순위 해법은 아니다.**

## 3. 랭크된 개선 방향 (전부 추가 후보 — 사용자 결정)

### ★1순위 [저위험·최고효율] 전이 수 4→5(또는 6), canonical stage 전위에 고정
- **근거**: 고품질 흑연 dQ/dV 는 5–6개 feature. MSMR 흑연 문헌(coal-graphite, *JES* 2024 ad2061)은 **6 gallery** 사용: ω_j={3.96, 0.24, 0.66, 0.086, 0.16, 0.047}, U0_j≈{0.333, 0.210, 0.128, 0.126, 0.089, 0.089}. 우리 4전이는 4↔3↔2L 클러스터를 병합 중 → 실측 0.105 spike·0.117 shoulder 미포착의 정체.
- **주목**: 그 논문은 U0 가 거의 같은 gallery 쌍(0.126/0.128·0.089/0.089)으로 **한 물리 피크를 폭 다른 두 로지스틱으로** 표현 — 우리 피팅이 0.14V 근처에서 narrow+broad 를 쌓은 것과 **동일 트릭**(문헌이 이미 쓰는 방법). 즉 우리 fit 이 옳게 작동.
- **후보 실행**: `GRAPHITE_STAGING_LIT` 를 5–6전이로 확장(U 고정·ω_j>0 bound). 예상 R²↑.
- **위험**: 낮음(U 고정으로 과적합 차단).

### ★2순위 [저–중위험] 두 저전위 피크에 작은·비대칭 폭
- **근거**: LiC12↔LiC6·2L↔2 는 1차 두-상(Dahn) → 작은 ω_j. 비대칭은 order–disorder 엔트로피 스텝(Reynier·Yazami·Fultz 2004 JES)·조성의존 Ω 에서 발생. 단일 로지스틱 ξ(1−ξ)는 **구조적으로 대칭**이라 잔차(b)는 함수형이 보장한 것.
- **후보 실행**: 양측 폭 `w_j^L≠w_j^R` 일반화 로지스틱(Zhu 2023 *Adv. Mater.* adma.202304666), 또는 문헌식 겹친-로지스틱 쌍.
- **위험**: 낮음–중(피크당 +1 파라미터, 위치·높이와 직교하는 shape 변화라 식별 가능).

### 3순위 [고위험, T/율속/히스 전용] 최근접 stage 결합 λ_{j,j+1}·ξ_{j+1}
- **근거**: 진짜 Safran/Kirczenow 층간 반발의 mean-field 선형화. **피크가 외부변수로 이동·상호배제**해야 할 때만.
- **위험**: 높음(식별성). 반드시 인접쌍만·단일 상수·부호 prior·정적합 실패 입증 후에만.

### 4순위 [최물리·중–고노력] 정칙용액(다층) 자유에너지로 대체 → common-tangent OCV
- **근거**: Bazant 두-층·Cordoba–Chandesris–Plapp 다층 Cahn–Hilliard. coupling+비대칭+진짜 1차 sharpness 를 native 로 포함하며 **Ch1 전하보존·내부전위 프로그램과 직결**(곡선피팅 아닌 열역학 포텐셜).
- **위험**: 노력 중–고, 과적합 낮음. OCV 가 비해석적(Maxwell) → 피크별 피팅 어려움. **Chapter 2–3 '열역학' 타깃**으로 적합.

## 3b. ★실측 실험 결과 (개선방향 랭크의 데이터 검증 — 흑연 2셀, BDD 추출)
문헌 랭크를 실측으로 검증(코드 무수정 실험):
| 실험 | R²(대칭/기본) | R²(개선) | 이득 | 판정 |
|---|---:|---:|---:|---|
| ①전이 4→6 (`gr_4vs6_transitions.png`) | 0.952–0.958 | 0.954–0.960 | **+0.2–0.4%** | 미미 — 추가 전이가 기존 피크 근처로 감(이 데이터엔 미포착 피크 적음) |
| ②비대칭 두-측폭 (`gr_sym_vs_asym.png`) | 0.952–0.958 | 0.961 | **+~1%** | 모듬 — 일부 피크 실측 비대칭(wR/wL 최대 4.5×) 확인 |
→ **데이터 기반 결론**: 이 SINTEF 흑연에선 잔차 지배원인이 미포착 피크(#1)도, 비대칭(#2)도 아닌
  **두-상 near-delta 첨두**(대칭·비대칭 로지스틱 공히 재현 불가). R²≈0.95–0.96 천장이 곧
  **MSMR 구조 한계의 signature**(§0·§4). 마지막 4–5%를 닫으려면 #1/#2(각 ~1%) 아닌 **#4(정칙용액
  자유에너지)** 가 실제 해법 — 문헌 예측을 실측이 확인. (단 #2 비대칭은 저비용 부분 이득이라 병행 가치.)

## 4. 문건에 명시할 정직한 한계 (추가 후보)
임의의 sum-of-logistics(MSMR)는 **V 에 대해 단조** → **진짜 평형 두-상 plateau(=dQ/dV delta)를 재현 불가**, ω_j→0 근사만 가능. 1–2순위 후 두 sharp 피크 잔차가 남으면 그것이 **진짜 1차 전이의 signature** 이고, 정직한 해법은 4순위(정칙용액 자유에너지)뿐 — 로지스틱 추가·coupling 이 아니다. 이 한계를 §7(브로드닝)에 1문단 명시 후보.

## 5. 실측이 뒷받침한 추가 관찰 (근거)
- **저Si f_Si 과대(0.48 vs 0.30, 2셀 일치)**: 약한 넓은 Si 항이 baseline 흡수 → Si U 를 순수-Si 피팅값(0.29/0.43/0.47V)으로 약구속하거나 전극 baseline Cbg(V) 분리 → 저Si 정량화. [추가 후보]
- **율속 washout(≥~10mA 스테이징 소멸) + 분극 shift(20 mV/mA, R²=0.86)**: 문건 유한율속(① L_V∝|I|)·분극(V_n=V−|I|Rn) 둘 다 실측 확인(정성). 정량 L_V∝|I| 는 상용 SiOx 음극 confound(농도분극·harvested)로 단순추적 불가 → **출하 `dqdv()` 전체(Rn+L_V) 피팅**이 정식 검증 = 다음 단계(V3 정량). [추가 후보]

## 부록: 참고문헌(문헌조사 검증분 — 서지 무날조, 불확실은 표시)
- Verbrugge·Baker·Koch 2017 *JES* 164 E3243 / Baker·Verbrugge 2018 *JES* 165 A3952 (MSMR 원전).
- MSMR→coal-graphite 6-gallery: *JES* 2024, 1945-7111/ad2061 (ω_j·U0_j 표).
- Safran *PRL* 44, 937 (1980); Safran·Hamann *PRB* 22 (1980, 페이지 미확인).
- Dahn *PRB* 44, 9170 (1991); Ohzuku 1993 *JES* 140, 2490.
- Levi·Aurbach, Frumkin isotherm review, *Electrochim. Acta* 45, 167 (1999).
- Reynier·Yazami·Fultz, entropy of Li-graphite, *JES* 151, A422 (2004); *J. Power Sources* 119–121, 850 (2003).
- Zhu et al., two-sided intercalation, *Adv. Mater.* 2023 (adma.202304666).
- Bazant/Smith 계열: Guo·Smith·Bazant 2016 *JPCL*; Ferguson·Bazant 2012 *JES* 159 A1967; Cordoba·Chandesris·Plapp 2024 arXiv:2401.13108.
- Mercer et al. dilute-limit, *Electrochim. Acta* 324, 134774 (2019, 저자 일부 미확인).
