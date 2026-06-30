# ORIGIN_VERDICT — "델타가 종모양이 되는 진짜 원인은 무엇인가" (Round 2 종합 답변)

> Round 1(`RADIUS_VERDICT.md`)은 *열역학적* 반경→U_j 가설을 부정했다. Round 2는 사용자 재질문("그럼 종모양은 뭐냐? 동일 C-rate 크기별 SOC 차이인가? U_j 분포 원인 미상")에 답한다.
> 근거: 축 E(`31`)·F(`32`)·G(`33`) 카드 master 직접 정독·삼각검증 + `30_scope_origin.md`. R1 문건 보존(addendum).
> 4-tier: 확정 / 근거미발견 / 추정 / 미검증. 작성 2026-06-30.

---

## 1. 세 줄 답
1. **"U_j 분포인 것은 확실"은 사실이 아니다.** 종모양은 *입자간 분포 없이도* 생긴다(내재 폭·단일입자 율속·순차충전). 그리고 분포가 있더라도 그것은 평형 `U_j` 분포가 아니라 **apparent-U = U_j + η(과전압) 분포**다 — GITT는 평형 `U_j`를 입자 무관 상수로 측정한다.
2. **"동일 C-rate에서 크기별로 차오르는 SOC가 달라 생기는 퍼짐"은 맞다 [확정·강한 지지].** 이것이 핵심 기작 중 하나이고(τ∝r² 동역학 분산), 앞서 부정된 *열역학* 반경 효과와 전혀 다른 *동역학* 채널이다.
3. ∴ 실측 치우친 종모양 = **(단일입자 유한율속 비대칭 꼬리) + (입자 크기 kinetic 분산) + (내재 RT/F 폭)** 의 합성. 참 평형 `U_j` 분포의 몫은 ≈0.

---

## 2. "델타가 종모양이 되는 것은 뭐냐?" — 계층별 답

### (A) 애초에 델타가 아닌 전이가 있다 — 내재 평형 폭 [확정]
"단일 입자 = 델타"는 **강한 1차 전이(Ω≥2RT, Frumkin g≥4)에만** 참이다. 그렇지 않으면 단일 입자 평형 dQ/dV는 등온선 기울기 `dx/dE`로서 **애초에 폭 ~nRT/F의 종**(Frumkin/정규용액; Levi & Aurbach, *Electrochim. Acta* 1999, 10.1016/S0013-4686(99)00202-9). ★흑연은 전이별로 갈린다:
- **dilute→stage4, 4L↔3L = 연속(solid-solution)·plateau 없음** → 단일 입자가 *이미 종*. 분포·broadening 불요. (RSC 10.1039/D0TA12607A: "plateau … except for 4L–3L")
- **2L→2(LiC₁₂), 2→1(LiC₆) = two-phase plateau(강한 1차)** → 평형 단일 입자는 델타에 가까움 → **이 전이들에서만** 종모양이 추가 기작을 요구.

→ 즉 사용자의 "델타여야 하는데 종"이라는 출발은 **LiC₁₂·LiC₆ 전이에만 해당**하고, 나머지는 원래 종이다.

### (B) 강한 1차 전이(LiC₁₂·LiC₆)의 델타를 종으로 푸는 것들
세 기작이 합성된다. **셋 다 입자간 평형 U_j 분포가 아니다.**

**(B-i) 단일입자 유한율속 비대칭 꼬리 [확정] — "치우침(skew)"의 주범.**
입자 *하나*라도 유한 전류면 표면 SOC가 평형을 앞서/뒤처져 과전압 `η(SOC)`가 변하며 peak을 한쪽으로 밀고 꼬리를 늘인다 = 모델의 `(ξ_eq−ξ_lag)/L_V`(N7/N8). C-rate↑일수록 심화, 평형(C→0)서 소멸. (Fly·Schaltz·Stroe, *J. Energy Storage* 2020, 10.1016/j.est.2019.101329: C-rate↑→peak 고전위 이동·둔화, resistance correction으로 C/6 peak 위치를 C/48 대비 0.59% 내 예측 → kinetic 성분이 저항으로 환원됨)

**(B-ii) ★입자 크기 kinetic 분산 [확정·강한 지지] — 사용자 신가설 = "broadening"의 주범.**
고정 셀 전류 하 **확산 timescale τ = r²/D**가 크기 제곱으로 벌어져, 작은 입자는 먼저(낮은 η)·큰 입자는 늦게(높은 η) 차오른다 → 같은 인가 전위에서 입자군이 서로 다른 국소 SOC → 거시 전이가 전압 구간에 퍼짐. **흑연 operando로 직접 입증**: Yang et al. 2023, *Nat. Commun.* (10.1038/s41467-023-40574-6) — "고상확산 시간상수가 반경의 제곱", 전환 직경 ~7 µm(작은 입자=intercalation-wave 빠름/큰 입자=shrinking-core 지연), **0.05C 균질 / 전류 2배 → 뚜렷한 SOC 이질**. PSD→전압 feature 분산·분할은 Kirk et al. 2022(10.1137/20M1344305, bimodal PSD→double-plateau "전적으로 bimodality 때문"), 흑연 직접은 Röder 2016(10.1002/ente.201600232, PSD→국소 전류밀도·과전압 분산).
- 지배 무차원수 **τ/t_dis = (r²/D)·C-rate** (Damköhler/Biot 류): **C-rate→0이면 분산→0(저율 소멸)**, PSD 폭 (d90/d10)²가 배율. D≈1×10⁻¹⁰ cm²/s로 직경 10 µm 입자 τ≈42 min, 20 µm 입자 τ≈2.8 h(**직경 2배=τ 4배**). apparent-U 분산 **~수~수십 mV [추정]**(절대 mV 실측표 미발견).

**(B-iii) 내재 RT/F 폭 [확정] — floor.** 평탄역 양끝 단상 꼬리·staging 정렬 폭이 ~nRT/F(≈26 mV) 하한을 깐다.

### (C) 그 외 heterogeneity (부차적, 코인 박전극·저율서 작음)
접촉저항/전류분포 이질(iv), 두께방향 SOC 구배(v, 박전극서 소), 조성·배향 이질(vi), 온도(vii). 모두 apparent-η 분포에 더해지나 코인 박전극·상온·저율에선 (B)보다 작다.

---

## 3. "U_j 분포의 원인을 모르겠다" — 재해석 [핵심 교정]
사용자가 확신한 "U_j 분포"는 **평형 U_j 분포가 아니다.** 관측 peak 전위 `V_peak = U_j + η`에서 **분포하는 것은 η(과전압)**이고, 평형 `U_j`는 GITT QOCP상 입자 무관 thermodynamic 상수(0.22/0.12/0.08 V, Park 2021 10.3390/ma14164683)다. 즉:
- **apparent-U 분포 = η 분포** ← 지배: (B-ii) 크기 kinetic 분산 + (B-i) 단일입자 율속 + (C) 전극 heterogeneity.
- **참 평형 U_j 분포 ≈ 0** (Round 1: 마이크론 흑연 반경→U_j ~0.01 mV; 조성 이질만 약간).

원인 순위(코인 하프셀 5–20 µm, 상온, C/10~1C):
**(B-i) 단일입자 율속 꼬리 > (B-ii) PSD kinetic 분산 > (B-iii) 내재 RT/F > 접촉/전류분포 > 조성·배향 > 두께구배 > 온도 > 참 U 분포(≈0).**

---

## 4. 어떻게 확정하나 — 실측 분해 처방
| lever | 사라지면/줄면 → | 남으면 → |
|---|---|---|
| **C-rate sweep (C/48→1C)** ★1급 분리기 | (B-i)(B-ii)(C) kinetic 전부 | (B-iii)+조성+참U = 평형/내재 |
| **GITT 근평형 잔여 dV/dQ 폭** | — | 잔여폭 = 평형 이질성 **상한**(작으면 종모양≈전부 kinetic) |
| **온도 sweep** | 폭↓(승온) → 확산지배(B-i,B-ii) | 폭↑(RT/F 추종) → 내재(B-iii) |
| **단일입자 vs 다입자 + DRT** | 단입자서 폭↓ → (B-ii)+전극 heterogeneity | 단입자서도 잔존 → (B-i)(B-iii) |

★사용자 신가설(B-ii) 직접 검증: **C-rate를 낮추면 종 폭이 좁아지며 내재 RT/F로 수렴해야** 한다. 그러고도 남는 폭이 평형 이질성(참 U·조성)의 상한이다. (B-ii)와 *순수 입자내* 확산(PSD 무관 B-i)의 분리는 **단일입자 측정**이 키.

---

## 5. 모델 함의 (단일 유효입자 + L_V 구조 확장)
현재 `v11_final.py`는 **단일 유효입자 + kinetic lag L_V(∝I)** — 즉 (B-i)는 이미 있으나 (B-ii) PSD 분산은 없다. 사용자 신가설을 모델에 넣으려면:
- **경로 B(권장·최소확장)**: 단일입자 응답 `f(V; r)`를 **입자 크기 분포 g(r) 위로 합성곱** `dQ/dV = ∫ g(r) f(V; r) dr` + 입자별 charge-transfer/diffusion lag. 작은 r→좌, 큰 r→우 → 자연스러운 비대칭·broadening. (B-i)는 각 f의 L_V로, (B-iii)는 U_j의 RT/F 기울기로 자동 포함. (Röder 2016·Kirk 2022의 MPM 구조)
- ★이렇게 하면 사용자의 원래 발상("peak에서 입자 분포 추산")이 *열역학*이 아니라 *동역학(PSD)* 경로로 부활한다 — 단 추출되는 것은 평형 U 분포가 아니라 **PSD(혹은 그와 얽힌 kinetic 분산 분포)**이고, C-rate·D·형태학과 결합돼 있어 단독 dQ/dV로는 여전히 비유일(Round 1 ill-posedness 유효 → C-rate sweep·독립 PSD 대조로 구속 필요).

---

## 6. 핵심 근거 DOI
- 내재 평형 폭·Frumkin: Levi & Aurbach 1999, **10.1016/S0013-4686(99)00202-9**.
- 흑연 전이별 1차/연속: RSC 2021, **10.1039/D0TA12607A**; IOP 10.1149/2.1251802jes.
- 순차충전(분포 비필수): Dreyer et al. 2010, **10.1038/nmat2730**; Katrašnik·Gaberšček arXiv:2201.04940.
- ★크기 kinetic 분산(흑연 operando): Yang et al. 2023, **10.1038/s41467-023-40574-6**; PSD→feature Kirk 2022, **10.1137/20M1344305**; 흑연 PSD Röder 2016, **10.1002/ente.201600232**; 저율순차/고율병렬 Farkhondeh 2017, 10.1149/2.0211706jes.
- C-rate 분리기: Fly·Schaltz·Stroe 2020, **10.1016/j.est.2019.101329**.
- 평형 U_j 상수(GITT): Park 2021, **10.3390/ma14164683**; D(GITT) PMC8397968.

> abstract/snippet-only(Wiley 402·ScienceDirect 403·arXiv PDF 디코드 실패)는 각 카드에 tier 강등 표기. 핵심 정량(τ∝r²·~7µm·C-rate 의존 = Yang 본문; double-plateau←bimodality = Kirk abstract; τ 계산 = 직접 산정)은 검증됨. apparent-U 절대 mV는 [추정](직접 실측표 미발견 = 열린 문제).
