# REVIEW2 — v7-08b.tex 검토2 (검수 sub, 리뷰 전용)

> 대상 `v7-08b.tex` (646행) 전문 정독 · 식/부호사슬 단위 청크.
> 판정기준 `Anode_Fit_v11_final.py`(706행)·`v11_flowchart.md`(분극 정정본)·`AUTHOR_BRIEF.md`.
> diff `v7-08.tex`↔`v7-08b.tex` 로 보완 5건 외 무변경 확인(surgical edit, 회귀면 최소화).
> 본 파일은 리뷰 산출물 1개 — 어떤 코드/문건도 수정·커밋하지 않음.

---

## 1. REVIEW1 보완 5건 반영 검증 {보완 → 판정 → 근거}

| # | REVIEW1 결함 | 보완 위치(v7-08b) | 판정 | 근거(코드/재유도) |
|---|---|---:|---|---|
| CRIT-1 | eq:dqdvwork `+` 누락(곱 변질) | 584 `\;+\;` | **해소** | `dqdv_work=Cbg`(L431-433) → `+= Q*peak_shape`(L481) 가산. 인접 eq:masterv11(593)·본문 "선형 누적"(578)과 정합. |
| HIGH-1 | eq:equilibrium ξ_eq 가 분기중심 U_j^d 에 묶임 | 379-386 prose + eq:Veqbaseline(382)·eq:VappVeqxieq(384) | **부분 해소(prose만)** | 코드 `equilibrium()` L364-369 = `func_ksi_eq(T,V,U_j,n_j)` 비분기 U_j·s=+1. 새 prose(386)가 "U_j^d 고정 branch 아니라 V_eq 에서 결정" 명문화 → 의미는 확정. 단 **boxed eq:equilibrium(406)·eq:eqpeakshape(399) 가 여전히 동일 글리프 ξ_eq 사용**(eq:xieq L351 가 ξ_eq≡U_j^d·z_j=σ_d(V−U_j^d)/w 로 전역 결박). 잔존 표기 충돌(아래 §2 R-1). |
| HIGH-2 | ΔU_hys 유도 V(ξ) 중간식 누락 | 296-309 eq:ocvregular·eq:hysocvstep + 210-217 spinodalstep1/2/3 | **해소** | spinodal 3단계(2Ω 이항→역수→완전제곱) 전수 검산 PASS → ξ_s^±=½±½u, u=√(1−2RT/Ω). eq:dUhys = code func_dU_hys L130 글자정합. |
| MED-1 | eq:weffraw "기울기 일치" 무유도 | 304-307 eq:weffbridge | **해소** | dV/dξ=(RT/F)(1/ξ+1/(1−ξ))−2Ω/F, ξ=½ 대입 bracket=4 → (4RT−2Ω)/F, ×¼ = (RT/F)(1−Ω/2RT). **분모 2RT 정확(4RT off-by 없음)**, code func_w_eff L144 정합. |
| MED-2 | eq:dlnLdV (1+e^{−A/RT}) A-의존 무시 | 443-451 eq:Lqfromk·eq:lnLqintermediate + 488-494 활성화지배 명시 | **해소(보강)** | ln L_q 중간식이 −ln(1+e^{−A/RT}) 항 명시 → code func_L_q L96 term-by-term 정합. eq:dlnLdV(490) 는 "활성화 지배" 가정 하 부호결론 유지(완전식 아니나 결론 PASS). |
| (추가) | N1 분극 prose 부호 오류("관측 V 평형보다 낮다") | 134, keybox 643 | **해소** | flowchart 2026-06-29 정정(DQ-b1: 방전=탈리튬화·산화 → V_app>V_n, 양의 anodic η)과 일치. 구 v7-08 L134 의 superseded 문구를 정정 문구로 교체. keybox 에 `V_app>V_n, η>0` 1줄 추가. |

**소결**: 5건(+분극 prose) 중 4건 완전 해소, HIGH-1 은 prose 의미확정·boxed 표기 미경화로 **부분 해소**.

---

## 2. 신규 회귀 적발 (Codex 보완·CRIT 수정 대상 → 엄격 적용)

diff 는 ① 중간식 align 삽입(spinodal·weff·lnLq) ② 절 도입 prose 6개 ③ N9 `+` ④ equilibrium baseline 블록 ⑤ 분극/keybox prose — 5종. 신규 label 9개(spinodalstep1/2/3·ocvregular·hysocvstep·weffbridge·Veqbaseline·VappVeqxieq·Lqfromk·lnLqintermediate).

- **R-1 [신규-경미 LOW~MED · §1 HIGH-1 잔존] boxed eq:equilibrium ξ_eq 표기 미경화.**
  eq:xieq(351) 가 ξ_{eq,j} 를 분기중심 U_j^d·z=σ_d(V−U_j^d)/w 로 **전역·권위 정의**. 그러나 보완이 추가한 prose(386)는 equilibrium() 의 ξ_eq 가 U_j(비분기)·s=+1 기준임을 말로만 분리하고, **boxed eq:equilibrium(406)·eq:eqpeakshape(399)·eq:masterv11(595) 첫 분기는 동일 글리프 ξ_eq 를 무표식 사용**. boxed 식만 따르는 독자는 U_j^d-결박 ξ_eq 를 equilibrium() 에 대입하는 바로 그 혼동에 노출. **단 수치 무해**(커널 ξ(1−ξ)/w 는 z 우함수 + γ=0 에서 U_j^d=U_j). v7-08 에 이미 동일 boxed 존재 → 보완은 prose 만 덧대 半폐쇄. 깔끔한 해법 = 평형 분기 기호에 ξ_eq^0 또는 `(U_j,s=+1)` 인자 명시.
- **R-2 [OK · 회귀 아님] eq:ocvregular(+Ω(1−2ξ)) vs eq:Veqbaseline(Ω 생략).** 의도적·정합. 전자=w_eff 유도용 정규용액 OCV 전식, 후자=code func_ksi_eq 순수 logistic 의 해석적 역(코드는 Ω 를 logit 이 아니라 폭 w_eff 로만 접음). prefactor w_j(=_width, RT/F 아님) 도 코드 정합. 모순 아님.
- **R-3 [OK · 회귀 아님] eq:hysocvstep(|V_chg−V_dis|) vs eq:dUhys(spinodal 폐형).** 동일 비음수량 2경로. prose 309 가 func_dU_hys 로 화해. 단 두 정의(branch 차 vs spinodal 폭)의 등가성은 *유도 없이 단정*(대칭 spinodal 모델 가정) — **pre-existing 모델 가정**이지 신규 결함 아님(§3 약점).
- **R-4 [OK] orphan 0.** 신규 label 9 중 eqref 되는 것은 Veqbaseline(386)·hysocvstep(309) 2개. 나머지 7은 모두 visible align 내 중간단계로 referenced/boxed 결과식(spinodal·weffraw·Lq·N6 baseline)으로 흐름 → 규약상 true orphan 아님. VappVeqxieq 가 가장 약하나(consumer="이를 풀면" prose) 의미상 소비됨.
- **R-5 [OK · 경미] 절 도입 prose 중복.** N6 마무리(416 "L_V sub-grid 클 때 뒤로 끌림")와 N7 도입(421 "순간 평형 못 따라감")이 동일 착상 재진술 — 무해. 기존 절 다리(573 "마지막 절은…" 등) 미파손.
- **빌드 회귀 0**: log error 0, undefined ref/citation 0, overfull ≥30pt 0, PDF 10p(NOTEb 보고와 일치).

**신규 회귀 = R-1 1건(LOW~MED, 수치 무해·표기), 사실상 HIGH-1 半폐쇄 잔존. CRIT/HIGH 신규 = 0.**

---

## 3. 재점수 (6 × 5 = /30)

| 차원 | v7-08 | v7-08b | 근거 |
|---|:---:|:---:|---|
| 척추 정합(N0–N9) | 5 | **5** | flowchart 순서·노드 전수 커버 불변. |
| 부호 정합(8항) | 4 | **5** | CRIT-1 `+` 복원으로 N9 누적식 코드 정합 + 분극 prose 정정(flowchart DQ-b1 일치). 8항 PASS(6번 결론 PASS). |
| G-follow(유도) | 2 | **4** | spinodal 3단계·weff bridge·lnLq 중간식 삽입으로 핵심 유도 단절 해소. R-1 표기 충돌로 5점 보류. |
| G-usable(재현·STAGING) | 3 | **5** | CRIT-1 해소로 재현식 정상화. 표·defaults·equilibrium baseline 닫힘. |
| 완결성(orphan/그림) | 5 | **5** | 신규 label 7 align-chain 소비, orphan 0. 4그림 불변. |
| 형식(수식주도·전보체·다리) | 4 | **5** | 무유도 단정 제거, 절 도입/마무리 prose 보강. 전보체 0. |
| **합** | **23** | **29/30** | R-1(equilibrium ξ_eq 표기 미경화) 1점 차감. |

---

## 4. 부호 8항 PASS/FAIL

| # | 항목 | 판정 | 근거 |
|---|---|:---:|---|
| 1 | U_j=(−ΔH+TΔS)/F | **PASS** | eq:UjT(180)=func_U_j L69. |
| 2 | ξ_eq=logistic[σ_d(V−U)/w], 방전 V↑→ξ↑ | **PASS** | eq:xieq(351) z=σ_d(V−U^d)/w = code L86. |
| 3 | dξ/dV=σ_d·ξ(1−ξ)/w, peak 양수 | **PASS** | eq:dxidVsig(392)·eq:eqpeakshape(400). |
| 4 | ΔU_hys≥0, Ω≤2RT→0, 분기 ±½σ_d | **PASS** | spinodalstep1-3 검산 + eq:dUhys(229)=func_dU_hys L130; Ω→2RT(u→0)→0 한계 확인; 방전 σ_d=+1 중심↑·충전↓(prose 309 정합). |
| 5 | χ_d=χ/1−χ, ΔH_a^eff=ΔH_a−χ_dΩ | **PASS** | eq:chidHeff(465)=func_chi_d L160·func_dH_a_eff L152. |
| 6 | ∂lnL_q/∂V<0 | **PARTIAL** | eq:dlnLdV(490) 결론 부호 PASS, "활성화 지배" 가정 하; (1+e^{−A/RT})·A 상수성은 여전히 부분(보강됐으나 완전식 아님). FAIL 아님. |
| 7 | 충전 격자역전 ξ[::-1]…[::-1], 충전=방전 거울 | **PASS** | eq:chargelowpass(529)=code L474-477. |
| 8 | V_n=V_app−σ_d|I|R_n | **PASS** | eq:polarization(131)·eq:interpout(607)=code L412; 방전 V_app>V_n·η>0 prose(134·643) flowchart 정합. |

**부호 FAIL = 0(7 PASS, 6번 PARTIAL). N9 누적식 `+` 결함(구 CRIT-1) 해소 확인. 추가 검산: eq:Lq 전수(eq:Lqfromk+eq:lnLqintermediate→boxed) code func_L_q L96 term-by-term PASS.**
