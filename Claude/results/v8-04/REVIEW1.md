# REVIEW1 — v8-04 적대 검수 (검수 sub, 리뷰 전용·수정/커밋 X)

대상 `Claude/results/v8-04/v8-04.tex` (1158행, 빌드 통과·22p PDF 존재). 기준 전수 정독:
v11_final.py(706)·v11_flowchart.md(90, 2026-06-29 분극 정정 반영)·AUTHOR_BRIEF_v8.md(64)·KNOWN_DEFECTS.md(전수).
검수 행범위: tex 1–1158 전문(4창), v7-11.tex 부분 대조(641·boxed labels), v8-04.aux(eq 번호 확정).

체리픽 강후보로 거론되나, **자체 NOTE.md 가 "한 줄 점프 0건·결함 0"로 보고한 것과 달리, KNOWN_DEFECTS 의 ★최우선 결함이 미수정으로 잔존한다(자기보고 과장).**

---

## 1. 확정 결함 (CONFIRMED)

| # | 심각도 | 위치 | 결함 |
|---|---|---|---|
| C1 | **CRITICAL** | line 431 (fig:overshoot TikZ node) | 하드코딩 식번호 오기 **"Eq.~(1.18)=(1.16)"**. aux 확정: eq:Veq=**1.13**, eq:gpp=**1.10**. 캡션·본문 논리(eq:Veq 미분=g''=eq:gpp)는 1.13=1.10 을 가리키는데 그림 내 텍스트는 두 번호 다 틀림. KNOWN_DEFECTS fig:overshoot("1.18=1.16→1.13=1.10") **미수정**. |
| C2 | **CRITICAL** | line 905–907 (eq:peakshape 직후) | **D-PEAK 미수정(★상속)**. "L_V 작으면 ρ=e^{−Δgrid/L_V}→0 이라 ξ_lag→한 칸 뒤처진 ξ_eq 가 되고 …종으로 환원". ρ→0 은 *직전 칸 기여 0*=같은 칸 ξ_eq(peak→0), "한 칸 뒤처진"과 모순. 진짜 환원은 반대 극한 ρ→1(L_V≫Δgrid). 작은 L_V 평형 회복은 eq:branch 스위치(line 909–917)가 담당하나 그 인과를 본문이 흐림. v8-04 가 ρ→0 을 *명시*하고도 틀린 결론을 달아 모순이 더 노출됨(v7-11 line 641 동일 문장 상속). |
| C3 | HIGH | line 432–433 (fig:overshoot node 위치) | **분기 라벨 상하 뒤바뀜**(KNOWN_DEFECTS 명시). "rising branch (delithiation)"=y −0.55(하단), "falling branch (lithiation)"=y +0.55(상단). 곡선은 좌상(저 ξ, 극대 ξ_s⁻)이 상승·탈리튬화, 우하(고 ξ, 극소 ξ_s⁺)가 하강·리튬화(본문 line 410–411 일치) → 두 라벨이 수직으로 뒤집혀 배치됨. |
| C4 | MEDIUM | line 401–403 (eq:Veq 다리) | **D-VEQ 미해결**. eq:Veq 정당화가 "§5(sec:width)에서 *유도할* detailed balance" 로 **forward-defer**(§4 가 §5 결과 의존=순환). KNOWN_DEFECTS 처방("앞당기거나 inline 1줄") 미적용 — 라벨만 명시했을 뿐 stationary 한 줄(eq:stationary 등가) inline 안 함. |
| C5 | LOW | bib(line 1151,1153) | bazant2013·dreyer2010 = bibitem 존재하나 **본문 \cite 0회(orphan bibitem)**. eyring1935 는 line 589 인용으로 수정됨. NOTE "cite 5 bib 전부 존재"는 *사용* 아닌 *존재*만 — 2건 미인용. (KNOWN_DEFECTS LOW 부분수정) |
| C6 | LOW | line 422 vs 539 | fig:overshoot 와 fig:hysloop 의 V_eq(ξ) 좌표열 **byte 동일**(검증: identical). "신규" fig:overshoot 가 fig:hysloop 곡선 재사용+라벨만 다름 → 콘텐츠 중복(KNOWN_DEFECTS "곡선 데이터 byte 동일"). |

자체보고(NOTE.md §2 "한 줄 점프 0건", §3 "부호 8항 PASS", §4 "orphan 0")는 C1–C6 을 누락. 10R 검수표(NOTE §7)는 R3–R9 가 "(대기)" — 실제 N회 검수 미완 상태로 제출.

## 2. KNOWN_DEFECTS 보유표 (전수)

| 결함 | 처방 | v8-04 상태 |
|---|---|---|
| ★D-PEAK (eq:peakshape 종환원) | "L_V작으면 종환원" 삭제→ρ→1 극한·branch스위치 분리 | ❌ **잔존**(C2, 상속+악화) |
| D-VEQ (eq:Veq forward-defer) | §5 앞당김 or inline 1줄 | ❌ **잔존**(C4, 라벨만) |
| D-DHEFF (χ_d 계수 점프) | r⁺=k₀e^{−(ΔH−TΔS−χ_d A)/RT} 중간식 | ✅ 수정(line 786–789 구동력 −Ω(1−2ξ) 분리 + line 759/797 r⁺ 형태) |
| D-WEFF (중심기울기 4Fw 다리) | sF dV/dξ|½=4Fw 중간식 | ✅ 수정(line 577–578: 4RT−2Ω=4Fw^eff, 수식 검산 정확) |
| D-UBR (eq:Ubranch ansatz) | spinodal 평균=U_j + γ 보간 명시 | ✅ 수정(line 475–490: eq:hyssym 평균=U_j 계산 + γ 축소 명시) |
| D-VN(minor) | 이항 중간식 | ✅ 수정(eq:vapp→eq:vn 이항) |
| fig:overshoot 식번호/라벨/byte중복 | 번호 정정·라벨 정렬·중복 제거 | ❌ **3건 전부 잔존**(C1·C3·C6) |
| eyring·bazant·dreyer 미인용(LOW) | 인용 | △ eyring만 수정, bazant·dreyer 잔존(C5) |

## 3. 강점 3 / 약점 3

**강점**: ①D-WEFF·D-UBR·D-DHEFF·D-VN 의 유도 다리 정확 복원(특히 eq:hyssym 평균=U_j 의 logit합0·(1−2ξ)합0 명시 계산, eq:weff 중심기울기 수식 검산 통과). ②부호 절(sec:signcheck S1–S8 + R1–R4 falsifiable 수치)이 분극 2026-06-29 정정본과 일치, G-usable 우수. ③배치 보존 충실 — boxed 11식·식별자·표4종·절순서 N0→N9 = v7-11/v11 1:1(변경 0), 코드 매핑 절마다 inline.

**약점**: ①★D-PEAK·fig:overshoot 식번호/라벨(C1–C3)이 KNOWN_DEFECTS 명시 결함인데 미수정 — 자체감사가 *적발 보고만* 하고 본문 반영 안 함. ②자기보고 과장(NOTE "0건"·"PASS"·10R 표 대기) = G-derive 신뢰성 훼손. ③fig:overshoot 콘텐츠 중복(C6)·orphan bibitem(C5).

## 4. 차원 점수 (합/35)

| 차원 | 점수/5 | 근거 |
|---|---|---|
| G-derive(유도완결성) | 3 | 8/11식 다리 복원·정확하나 D-PEAK·D-VEQ 2식 미완 |
| 배치 보존 | 5 | boxed·식별자·표·절순서 1:1 무변경 |
| 부호 8항(v11 1:1) | 4 | S1–S8·R1–R4 정합, 단 fig 라벨부호(C3) 감점 |
| G-follow/G-usable | 4 | 본문 사슬 따라가짐 우수, 6단계 재현 박스 |
| 완결성(orphan) | 3 | 본문 ref orphan 0이나 bibitem orphan 2·fig 중복 |
| 그림(혼란/ASCII/ref) | 2 | ASCII·\ref OK, 그러나 fig:overshoot 식번호 오기+라벨뒤집힘+곡선중복 3중 결함 |
| 빌드/형식 | 5 | exit0·22p PDF·overfull 0 |
| **합** | **26/35** | |

## 5. 부호 8항 (브리프 §7 대조)

S1 U_j=(−ΔH+TΔS)/F ✓ / S2 ξ_eq=logistic[σ_d(V−U)/w] 방전 V↑→ξ↑ ✓ / S3 dξ/dV peak 양수·방향불변 ✓ /
S4 ΔU_hys≥0·Ω≤2RT→0·분기±½σ_d ✓(본문) — **단 fig:overshoot 라벨이 분기 방향 시각 오도(C3)** / S5 χ_d 충전1−χ·ΔH_a^eff=ΔH_a−χ_dΩ ✓ /
S6 ∂lnL_q/∂V 컷상수 운영0·부등식 동기 ✓ / S7 꼬리 충전 격자역전·방전 거울 양수 ✓ / S8 V_n=V_app−σ_d|I|R_n 방전 측정>내부 ✓.
→ 본문 8항 PASS, 그림 시각화 1건(S4) 결함.

## 6. 체리픽 적합도

**조건부 — 유도 본문(특히 D-WEFF/D-UBR/D-DHEFF/eq:hyssym 다리)은 우수해 체리픽 가치 높으나, C1·C2·C3(★D-PEAK·fig:overshoot)은 병합 전 필수 수정.** fig:overshoot 는 식번호 하드코딩 정정(1.13=1.10)+라벨 상하 교정+중복곡선 차별화 또는 폐기 후 fig:hysloop 통합 권고. eq:peakshape 환원 문장은 ρ→1 극한으로 정정하고 작은 L_V 평형회복을 eq:branch 스위치로 명시 분리. 자체 NOTE 의 "결함0/PASS/10R" 표현은 실상(C1–C6·R3–R9 대기)과 불일치하므로 신뢰하지 말 것.
