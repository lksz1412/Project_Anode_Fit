# 흑연 staging 상(phase) — XRD 근거 확정 (전이 개수 물리 판정)

> 사용자 요구: 전이 개수 변경은 **XRD 실측 관측**에 근거해야 타당. 본 문건 = 그 XRD 근거 확정.
> 결론 선요약: **전이를 6개로 늘리는 건 물리적으로 틀림(curve-fitting).** XRD 확정 = **두-상 4개 + 4↔3 고용체 1개.**

## 1. XRD 확정 staging 서열 (Dahn 1991, in-situ XRD)
**J. R. Dahn, "Phase diagram of Li_xC6," *Phys. Rev. B* 44, 9170 (1991)** — 정본 in-situ XRD (0<x<1, 0–70℃).
서열(리튬화 증가): **dilute 1′ → stage 4 → stage 3 → stage 2L(liquid-like) → stage 2(LiC₁₂) → stage 1(LiC₆).**

Dahn 초록 verbatim: 모든 전이가 공존(coexistence, 1차 두-상)인데 **"stage 4→3 전이만 예외"**(연속/고용체).

| # | 전이 | ~전압(리튬화) | XRD 성격 | dQ/dV |
|---|---|---|---|---|
| 1 | dilute 1′ ↔ 4 | ~0.20–0.22 V | **두-상**(x≈0.04부터, 약함) | sharp 약함 |
| — | **stage 4 ↔ 3** | ~0.14–0.20 V(경사역) | **두-상 아님 = 고용체(연속)** | **broad shoulder** |
| 2 | stage 3 ↔ 2L | ~0.12–0.14 V | **두-상** | sharp |
| 3 | stage 2L ↔ 2 | ~0.11–0.12 V | **두-상** | sharp |
| 4 | stage 2 ↔ 1 (LiC₁₂↔LiC₆) | ~0.085–0.09 V | **두-상**(최강·최sharp) | 최sharp, near-delta |

→ **XRD 확정 두-상 전이 = 4개**(1′↔4·3↔2L·2L↔2·2↔1). **4↔3 은 고용체**(공존역 없음).
(교차확인: Ohzuku·Iwakoshi·Sawai *JES* 140, 2490 (1993); Woo et al. *PRB* 27, 7831 (1983).)

## 2. "추가 피크 = 진짜 상 vs Ω-shoulder" 판정 (핵심)
정칙용액 μ(x)=μ°+RT·ln[x/(1−x)]+Ω(1−2x), dμ/dx|_{x=½}=4RT−2Ω:
- **Ω<2RT**: μ 단조 → **단일 고용체** → V(x) 경사 → dQ/dV **유한 broad peak**. **큰(subcritical) Ω 는 변곡/shoulder 를
  만들어 피크 분리처럼 보이나 새 상 아님** = 사용자가 의심한 "Ω-shoulder".
- **Ω=2RT**: 임계점, dQ/dV 발산.
- **Ω>2RT**: μ 비단조 → Maxwell 공통접선 → **평탄 plateau = miscibility gap = 두 공존상** → XRD 고정 d-spacing
  2개 → dQ/dV **near-delta**.

**판정자 = XRD(고정 d-spacing 2개 vs 연속 이동), dQ/dV 폭 아님.** 폭만으론 두-상/고용체 구분 불가(유한폭은 입도·계면·kinetics).
→ **2↔1·2L↔2·3↔2L 은 XRD 공존 확인 = 진짜 두-상**(피크 정당). **4↔3 은 XRD 공존 없음 = 고용체 shoulder**(별도 상 아님).
→ **0.14–0.22 V 경사에서 별도 5번째 "상"을 뽑는 건 고용체 shoulder 를 curve-fitting 하는 것**(XRD 미지원). 6+ = 끼워맞추기.

## 3. Ω 정량값 (Bazant 2-sublattice 정칙용액 fit)
Ferguson·Bazant *Electrochim. Acta* 146, 89 (2014); Guo·Smith·Bazant·Brus *JPCL* 7, 2151 (2016):
- **Ω_a = 3.4 k_BT (>2 k_BT)** = 면내(in-plane) 인력 → **진짜 면내 상분리**(LiC₆/LiC₁₂ 응축 sharp 의 정량 기원).
- Ω_b = 1.4 k_BT (<2 k_BT) 층간 반발(단독으론 상분리 안함).
- Ω_c = 30 k_BT 대형 = staging(Daumas–Hérold 교대충전) 강제. **staging 은 단일 Ω 아닌 다층 ordering.**
- **함의: 단일 Ω 아닌 2-sublattice(2-layer) 정칙용액이 물리적으로 옳음**(단일 Ω 는 면내 sharpness 만 포착, staging 못담음).
- DFT 확증: Persson·Van der Ven·Ceder *PRB* 82, 125416 (2010) cluster expansion+MC 가 stage 1/2 두-상 재현(3/4 는 제외).

## 4. 조건 의존 (회사 관측 "조건 따라 피크 잡힘"의 물리)
- **1차 plateau(2↔1)은 견고·T-무관**(Reynier·Yazami·Fultz *JPS* 119–121, 850 (2003); *JES* 151, A422 (2004) — 2↔1 plateau ∂/∂T≈0 = 진짜 두-상 열역학 signature).
- **고용체·order-disorder(dilute/4/3)는 fragile**: 고율·상온서 병합, 저율·저온·고분해능(synchrotron)·엔트로피profiling서 분리·sharpen.
- → 회사서 "조건 따라 안 잡히던 피크 잡힘"은 **고용체/order-disorder feature 에 대해 물리적으로 실재**. 단 그 분리가
  **두 진짜 상인지 한 고용체 shoulder 인지는 XRD 가 결정**(그 측정이 우연히 분해했다는 사실이 아니라).

## 5. 모델링 함의 (문건 반영은 사용자 최종 결정 — 여기선 물리 확정만)
1. **전이 개수는 4개가 XRD 정당**(두-상 4). 6개는 물리 위반(curve-fitting) — **폐기**.
2. **4↔3(0.14–0.20 V)은 고용체 shoulder**로 모델(broad, Ω<2RT), 별도 sharp 두-상 아님. 현 모델의 "shoulder 잔차"의 정체.
3. **폭 시드 = Ω>2RT 기준**(사용자 제안 타당): 두-상 4개는 sharp seed(Ω>2RT), 4↔3 는 broad seed(Ω<2RT). w=RT/F 일괄은 물리 위반.
4. 엄밀히는 **2-sublattice 정칙용액**(면내 Ω_a + staging Ω_c)이 정본; 단일 Ω/로지스틱은 근사.
5. **판정 기준 문건 명기 후보**: "Ω>2RT ⇒ 두-상(XRD 공존)·sharp / RT≲Ω<2RT ⇒ 고용체·shoulder(새 상 아님)".

## 서지 (전부 실재·검증가능)
Dahn *PRB* 44, 9170 (1991) · Ohzuku·Iwakoshi·Sawai *JES* 140, 2490 (1993) · Woo et al. *PRB* 27, 7831 (1983) ·
Reynier·Yazami·Fultz *JPS* 119–121, 850 (2003) & *JES* 151, A422 (2004) · Persson·Hinuma·Meng·Van der Ven·Ceder
*PRB* 82, 125416 (2010) · Ferguson·Bazant *Electrochim. Acta* 146, 89 (2014) · Guo·Smith·Bazant·Brus *JPCL* 7, 2151 (2016)
· "Stage 4→3 transition" *J. Solid State Electrochem.* (2003).
정직 단서: plateau 전압은 히스/율 의존(리튬화 근사값); Bazant Ω 는 OCV-fit(직접 XRD 측정 아님); Persson DFT 는 stage 1/2 신뢰(3/4 제외); dQ/dV 폭 단독으론 두-상/고용체 구분 불가(XRD 가 판정자).
