# REVIEW1 — v7-03.tex 적대 검수 (검수 sub, v7-03)

> 대상 `Claude/results/v7-03/v7-03.tex` (873행, 전문 정독 head→tail).
> 판정 기준: `v7-00_spine/Anode_Fit_v11_final.py`(706행 전문)·`v11_flowchart.md`·`AUTHOR_BRIEF.md`.
> 본 문서는 리뷰 전용 — 어떤 파일도 수정·커밋하지 않음.

---

## 1. 척추 N0→N9 순서·노드 커버 (적대 검산)

절 순서 = §1(N0) §2(N1) §3(N2) §4(N3) §5(N4,N5) §6(N6) §7(N7) §8(N8) §9(N9) + §10 부호종합 + §11 G-usable.

- 노드 커버: N0–N9 전부 등장, 누락 없음. ✔
- ★**spine 순서 위반(구조 결함)**: flowchart 및 AUTHOR_BRIEF §3 권장 골격은 **N2 → (N3) → N4,N5 → N6** 순(히스 분기 N3 가 폭·점유 앞). v7-03 은 §3=N2 → §4=**N3** → §5=N4,N5 → §6=N6 으로 **N3 을 N4 앞에** 둠. flowchart 본문 박스 순서(L27 N2 → L30 N3 → L37 N4 → L39 N5 → L41 N6)와는 **일치**한다. 그러나 AUTHOR_BRIEF §3 의 *권장 절 골격*은 항목4(폭·점유)→항목5(평형 peak)→**항목6(히스 N3)** 으로 히스를 peak 뒤로 미룬다("방전 메인·히스는 분기 위상"). v7-03 은 flowchart 코드 진행을 택해 BRIEF 권장 골격과 어긋난다. → **두 통제문서 충돌**: flowchart(코드 진행 1:1)를 우선한 것은 v7 의 1순위 목표("코드 진행을 절 순서로")와 정합하므로 **방어 가능**하나, BRIEF §3 권장과의 불일치는 NOTE 에 결정근거 명시가 있어야 함. 심각도 LOW(정합성 설명 부재).

## 2. ★부호 8항 v11 대조 (refute mandate — 각 항 코드 라인 직접 대조)

| # | 조건 | tex 식·행 | v11 코드 | 판정 |
|---|---|---|---|---|
| 1 | U_j=(−ΔH+TΔS)/F, ΔH<0→U>0 | eq:Uj L245 | func_U_j L69 `(-dH_rxn+T*dS_rxn)/F` | **PASS** 부호·식 일치 |
| 2 | ξ_eq=logistic[σ_d(V_n−U)/w], 방전 V↑→ξ↑ | eq:ksi L413 | func_ksi_eq L86 `z=s*(V_n-U)/w` | **PASS** |
| 3 | dξ/dV=σ_d·ξ(1−ξ)/w, peak 양수 | eq:dxidV L480-482 | L468 `ksi_eq*(1-ksi_eq)/w` (σ_d 無) | **PASS** tex L485-487·검산box·§10-3 이 σ_d 부재 이유(N8 격자역전)를 정확 설명 |
| 4 | ΔU_hys≥0, Ω≤2RT→0; 분기 ±½σ_d | eq:dU L309·eq:branch L324 | func_dU_hys L127-130·func_U_branch L138 | **PASS** |
| 5 | χ_d 방전 χ/충전 1−χ; ΔH_a^eff=ΔH_a−χ_dΩ | eq:chid L547·eq:dHeff L542 | func_chi_d L160·func_dH_a_eff L152 | **PASS** |
| 6 | ∂lnL_q/∂V<0 | §10-6 L805-806 | func_L_q L96 `-x*A/(RT)`, A∝(V−U)↑ | **PASS** ∂lnL_q/∂A=−χ_d/RT<0 정확 |
| 7 | 충전 격자 역전 ξ[::-1]…[::-1] | §8 L639-644 | L474-477 동일 | **PASS** verbatim 일치 |
| 8 | V_n=V_app−σ_d|I|R_n | eq:vn L179 | dqdv L412 `V_in-sigma_d*I_abs*Rn` | **PASS** |

**부호 8항: 8/8 PASS, FAIL 0.** 모든 식별자·부호·라인 인용이 코드와 1:1. (단 §8-6 검산 L806 은 `A∝σ_d F(V_n−U_j^d)`로 쓰나 코드 A=`min(z_cut·n·RT, A_cap·RT)`는 σ_d·F 를 안 곱한 크기量 — 부호 결론은 옳지만 A 의 tex 본문 정의 eq:Acut L560 과 §8-6 의 A 표기가 미세 불일치. 심각도 LOW, 결론 무영향.)

## 3. 확정 결함 (심각도·행·틀림·옳은 형)

| # | 심각도 | 행 | 틀림 | 옳은 형 |
|---|---|---|---|---|
| D1 | **HIGH** | 349, 364-365 | fig:hys spinodal 점 좌표 **x=0.2959/0.7041** 로 플롯(주석 "0.5±√(1/6)≈0.2041"도 틀림: √(1/6)=0.408). Ω=3RT 의 참 spinodal 은 ξ_s=0.5±0.5√(1/3)=**0.2113/0.7887**. y=−0.0157 는 참 spinodal 의 g/RT 값이라, 점이 곡선에서 떨어져 그려짐(0.2959 의 실제 g/RT=+0.0177). | x→0.2113/0.7887, 주석 "0.5±0.5√(1/3)≈0.289" |
| D2 | MEDIUM | 430-432, 435-437 | fig:logistic 데이터 z-스케일 혼용: 끝점 ±0.5 는 logistic(2z)(=0.2689/0.7311), 중간 ±0.3/0 은 logistic(z)(=0.4256/0.5744/0.5). 종 파선 ±0.5=0.3932 도 어느 매핑과도 불일치. 곡선이 매끈하나 정량 부정확. | 한 매핑으로 통일(logistic(z): −0.5→0.3775, 0.5→0.6225; 종 2.5·ξ(1−ξ): ±0.5→0.5875) |
| D3 | LOW | 322 | "이 중심에서 ±½γ_jΔU_hys 만큼 갈라진다" — 식 eq:branch 는 ½σ_d…(방·충 **합쳐** 총 분리는 σ_d 두 부호로 ±½씩) 이므로 방·충 **간격**은 γΔU_hys(½ 아님). "±½" 표현이 간격을 절반으로 오인케 함. | "방·충전이 각각 ±½γ_jΔU_hys, 둘 사이 간격 γ_jΔU_hys" |
| D4 | LOW | 806 | §8-6 의 `A∝σ_d F(V_n−U_j^d)` 표기가 본문 eq:Acut(L560) A 정의(σ_d·F 없는 크기量)와 불일치 | A=min(z_cut·nRT, A_cap·RT) 표기로 통일 |
| D5 | LOW | 487 | "N8 에서 격자를 역전한 뒤 peak_shape 를 구성하므로 부호가 자동 양수" — 평형 peak(N6, L468)는 **격자역전과 무관**하게 이미 ξ(1−ξ)≥0 으로 양수. 충전 시 L468 도 σ_d 없이 양수(N8 미경유 가능). 역전은 N8 꼬리에만 관여. 인과 설명 과결합. | "L468 평형 peak 는 ξ(1−ξ)≥0 자체로 양수; N8 꼬리는 격자역전으로 양수 유지" |

CRIT 0 · HIGH 1 (D1) · MEDIUM 1 (D2) · LOW 3.

## 4. 강점 3 · 약점 3

**강점**
1. 부호 사슬 8항 전건이 코드 라인까지 verbatim 정합(8/8) — 핵심 결함 클래스 0.
2. G-usable §11 우수: S1–S4 한 줄 평가 순서 + 피팅 순서 + 검증조건이 닫혀, 이 절만으로 dqdv() 재현 가능. STAGING 표(L739-742)도 코드 GRAPHITE_STAGING_LIT(L535-563)와 값 일치.
3. 보편식 먼저(eq:gxi 일반 자유에너지 → spinodal·임계는 코너) — BRIEF §4 "보편식 먼저" 준수. equilibrium() L354 인용 정확.

**약점**
1. **(가장 약한 1곳)** fig:hys spinodal 점 오좌표(D1, HIGH) — 그림이 "이해를 돕는다"는 BRIEF §5 기준 위반: spinodal 변곡점이 곡선 밖에 찍혀 독자가 spinodal=변곡점을 오인. 신규 그림이 도리어 오정보.
2. fig:logistic 정량 데이터 z-혼용(D2) — 시각 검수(렌즈⑥) 미수렴 흔적.
3. 절 다리 일부 약함: §6(N6)→§7(N7) 전환은 매끄러우나, §4(N3) 도입이 "N3 는 방전·분기 동시 처리"로 시작해 앞 절(N2)에서 받은 U_j 를 명시 인계하는 다리가 짧음(BRIEF §3 "도입=앞 절에서 받은 것" 의무 경계).

## 5. 완결성 (orphan) · 그림 규약

- 모든 figure 가 \label + 본문 \ref 보유: fig:polar(L190), fig:hys(L342), fig:logistic(L422), fig:tail(L660), fig:full(L749) — orphan **0**. ✔
- 그림 내부 텍스트 영어 ASCII 전용(한글 0) 확인: 모든 node/축/범례 영어. ✔ 캡션 prose 한글 — 규약 합치.
- TikZ 신규 작성(v5/v6 그림 미재사용). ✔
- 단, D1·D2 로 fig:hys·fig:logistic 의 "이해 도움" 실패 — 그림 효과 렌즈에서 감점.
- 식 참조 \eqref orphan 점검: eq:peakfull(L715)·eq:mu(L291) 등 도입 후 사용/종결 — dangling 식 라벨 없음. ✔

## 6. 차원 점수 (6항 × 5점 = /30)

| 차원 | 점수 | 근거 |
|---|---|---|
| 척추 정합(N0–N9) | 5 | 노드 전수 커버, 코드 진행 1:1. BRIEF 권장골격 충돌은 코드우선으로 방어가능(−0 유지). |
| 부호 사슬(코드 대조) | 5 | 8/8 PASS, verbatim. 핵심 결함 클래스 무결함. |
| G-follow | 4 | 유도 단계적·비유 의존 X. D3/D5 의 미세 인과 과결합으로 −1. |
| G-usable(재현) | 5 | §11 닫힘, STAGING 값 코드 일치, S1–S4 완결. |
| 완결성·형식 | 4 | orphan 0, 수식주도·전보체 회피 양호. §4 도입 다리 약함 −1. |
| 그림 효과·시각 | 2 | fig:hys 오좌표(HIGH)·fig:logistic z혼용(MED)로 2개 그림 오정보. −3. |

**합계 = 25 / 30.**

## 7. 부호 8항 최종 (PASS/FAIL + 근거)

1 PASS(func_U_j L69) · 2 PASS(func_ksi_eq L86) · 3 PASS(L468 σ_d 부재 설명 정확) · 4 PASS(func_dU_hys/U_branch) · 5 PASS(func_chi_d/dH_a_eff) · 6 PASS(∂lnL_q/∂A=−χ_d/RT<0) · 7 PASS(L474-477 verbatim) · 8 PASS(dqdv L412). **FAIL 없음.**

---
*검수 sub 완료. 수정·커밋 없음. 산출 = 본 REVIEW1.md 1건.*
