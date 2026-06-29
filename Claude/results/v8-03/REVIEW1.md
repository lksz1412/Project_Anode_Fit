# REVIEW1 — v8-03.tex 적대 검수 (검수 sub, v8-03 단일 대상)

> 방법: 3 병렬 Agent(G-derive / D-PEAK+부호 / 그림+G-follow) refute mandate + master 삼각검증(손 검산·수치 재현·ref/cite 자동검증). 대상 전문 정독(1072행) + 기준 v11_final.py·v11_flowchart.md·AUTHOR_BRIEF_v8.md·KNOWN_DEFECTS.md 전수 점검.

---

## 1. 확정 결함 (라인 + 명 + 라벨 + 심각도)

| # | 라인 | 결함 | 라벨 | 심각도 | 근거(삼각검증) |
|---|------|------|------|--------|----------------|
| C1 | **867-868** | **D-PEAK 미수정 잔존.** "L_V 작으면 ξ_lag→1칸 뒤처진 ξ_eq → (ξ_eq−ξ_lag)/L_V가 dξ_eq/dV 종으로 환원" — KNOWN_DEFECTS ★최우선·v7-11 상속 결함이 거의 verbatim 잔존. | D-PEAK | **CRITICAL** | master 수치 재현: ρ=e^{−Δgrid/L_V}, L_V→0 ⇒ ρ→0 ⇒ ξ_lag→ξ_eq(같은 칸) ⇒ peak_shape max→0 (참 종 12.5 미접근). 환원은 반대 극한 L_V≫Δgrid(ρ→1). eq:branch(872) 스위치와 정면 모순. |
| C2 | **1053-1054** | D-PEAK 동일 오류 전파(부호 self-test R3). "|I|→0에서 peak가 평형 종으로 떨어진다"를 연속 환원으로 서술 — 실제론 eq:branch 스위치가 가로챔. | D-PEAK | HIGH | 위와 동일 메커니즘. C1 수정 시 동반 수정 필요. |
| H1 | 791-795 | **D-DHEFF.** eq:dHeff `ΔH_a^eff=ΔH_a−χ_dΩ`가 χ_d 계수 중간식 없이 점프("+Ω 흡수" 손짓만). `r⁺=k₀exp[−(ΔH_a−TΔS_a−χ_dA)/RT]`류 중간식 부재. | D-DHEFF | HIGH | 보유O/해결X. |
| H2 | 427-431 | **D-VEQ.** eq:Veq의 다리 `sF(V_eq−U)=g'(ξ)`가 inline 정당화 0 — V_eq 유도가 §4(eq:eqcond, 573-575)에 있어 forward-defer(순환). | D-VEQ | HIGH | 보유O/해결X. |
| H3 | 577-592 | **D-WEFF.** eq:weff `(RT/F)(1−Ω/2RT)` 중심기울기 중간식 누락 + 본문 μ 부호(L573 −Ω·θ규약)와 eq:eqcond(574)가 박스로 매끄럽게 연결 안 됨(부호 비정합). 보조서 `d/dV[…]=RT/[ξ(1−ξ)]`는 d/dξ 오표기, "logistic 중심기울기 sF/4"는 sF/4RT 오기. | D-WEFF | HIGH | **★박스값 자체는 정확**(master 검산: 물리상 Ω=2RT서 w_eff→0, spinodal 문턱 일치; v11 func_w_eff L144와 1:1). 결함은 *유도 다리*이지 박스 아님 — G-derive 에이전트의 "박스 부호 반대=CRITICAL" 주장은 과대평가, master 하향 조정. |
| H4 | 686, 919 | 그림 2개 orphan(본문 \ref 0): fig:logistic·fig:reversal. 브리프 §5 "orphan 0" 위반. | — | HIGH | master ref 자동검증으로 확인(never-referenced 목록). |
| M1 | 451-575 | §3·§4 내부 μ/eqcond 부호 비정합(H3 상류). L573 `−Ω(1−2ξ)` + L574 `−sF(V−U)` ⟹ L575는 `+sF(V−U)+Ω` 이어야 정합인데 부호 추적 흐림. | — | MED | master 손 검산. |
| L1 | 109, caption | fig:spine 캡션에 "v7-11 유래/신규" 표기 누락(8개 중 유일). | — | LOW | — |
| L2 | 1064-1066 | bazant2013·dreyer2010 bibitem 미인용. | — | LOW | master cite 자동검증. KNOWN_DEFECTS LOW 잔존. |

---

## 2. KNOWN_DEFECTS 보유표 (전수)

| 라벨 | 상태 | 라인 |
|------|------|------|
| **D-PEAK** ★ | **보유 O / 해결 X (CRITICAL)** | 867-868 (+전파 1053-54) |
| **D-VEQ** | 보유 O / 해결 X | 427-431 |
| **D-DHEFF** | 보유 O / 해결 X | 791-795 |
| **D-WEFF** | 보유 O / 해결 X (유도 다리; 박스값은 정확) | 577-592 |
| **D-UBR** | **완화 O / 잔존 LOW** — "실측 분기 중심을 방향별 한 자유도로 적으면"으로 현상학적 매개변수화 명시(유도 가장 아님). KNOWN_DEFECTS 권고 충족. | 475-477 |
| D-VN(minor) | 자명 이항(허용) | 250-255 |
| fig:overshoot(식번호 오기/라벨 뒤바뀜/중복) | **해결 O** — \eqref 사용으로 번호 오기 불가, fig:hysloop 분기 라벨 물리 정합(극대=ξ_s−/극소=ξ_s+), 가짜 데이터 중복 없음 | 493-514 |

요지: **5개 핵심 결함(D-PEAK·D-VEQ·D-DHEFF·D-WEFF·D-UBR) 중 D-UBR만 해결, 나머지 4개 미수정.** ★최우선 D-PEAK가 verbatim 잔존 — "검토1서 ★D-PEAK 상속 전수 확인" 지시에 직접 저촉.

---

## 3. 강점 3 · 약점 3

**강점**
1. spinodal·artanh ΔU_hys·detailed balance/logistic·L_q 4항 로그 — 4개 유도 사슬이 모범적 (a)→(d) 단계 + 코드 1:1. master 손 검산: ΔU_hys(Ω=12000)=86.69 mV(self-test 86.7 일치), ln[(1+u)/(1-u)]=2artanh u 항등 검증, eq:Lqfull↔func_L_q L96 4항 1:1, U(298)=0.0853 V(목표 0.085) 정합.
2. 부호 8항(S1–S8) 전건 v11 코드와 1:1 — 부호 결함 0. 분극 서술이 flowchart 2026-06-29 정정(방전 V_app>V_n)과 정합.
3. 그림 8개 TikZ 전부 ASCII-clean(한글 0, 렌더 안전) · dangling ref 0(39 ref / 74 label 전부 해소) · cite 5건 bib 존재.

**약점 (가장 약한 1곳 = ★)**
1. ★ **L867-868 D-PEAK 거짓 극한 정당화** — KNOWN_DEFECTS 최우선 ★결함 미수정. 거짓 정당화를 따라 코드 짜면 작은 L_V 곡선이 0으로 무너져 **G-follow/재현가능성 직접 파괴**. eq:branch(872)와 모순·R3(1053-54)로 전파. 수정안: "L_V 작으면 종 환원" 삭제 → (a) 연속 정당화 r/L_V=dξ_eq/dV는 L_V≳Δgrid에서만, (b) 작은 L_V 평형 회복은 eq:branch 스위치로 명시.
2. 유도 3개(D-DHEFF·D-VEQ·D-WEFF)가 "한줄 점프·forward-defer·중간식 누락"을 그대로 보유 — v8의 존재 이유(유도 복원) 미달.
3. 그림 2개(fig:logistic·fig:reversal) 본문 \ref 부재 orphan.

---

## 4. 차원 점수 (합 / 35)

| 차원 | 점수 | 비고 |
|------|------|------|
| G-derive(유도 완결성) | 2.5 / 5 | 4사슬 모범 vs 3박스(D-DHEFF/D-VEQ/D-WEFF) 한줄점프·순환·부호다리 결함 |
| 배치 보존(v7-11) | 5 / 5 | 절순서 N0–N9·결과박스·식별자·표 보존 |
| 부호 8항(v11 1:1) | 5 / 5 | S1–S8 전건 PASS |
| **D-PEAK 처리** | **1 / 5** | ★최우선 결함 verbatim 잔존 + eq:branch 모순 + R3 전파 |
| G-follow | 3 / 5 | D-PEAK 거짓 정당화로 작은-L_V 재현 오도 |
| G-usable / 완결성 | 4 / 5 | keybox 6단계·nodemap 완결·식참조 정합; orphan 2 감점 |
| 그림 | 3.5 / 5 | ASCII 완벽·dangling 0·라벨 물리 정합; orphan 2 + 유래표기 1 누락 |
| **합계** | **24 / 35** | |

---

## 5. 부호 8항 (AUTHOR_BRIEF §7, v11 코드 대조)

| 항 | 명제 | 판정 | 근거(라인/코드) |
|----|------|------|-----------------|
| S1 | U_j=(−ΔH+TΔS)/F, ΔG=−sFU | PASS | eq:Uj(327) ↔ func_U_j L69 |
| S2 | ξ_eq=logistic[σ_d(V−U)/w], 방전 V↑→ξ↑ | PASS | eq:xieq(657) ↔ func_ksi_eq L86 z=s(V−U)/w |
| S3 | dξ/dV peak 양수·방향불변 | PASS | eq:eqpeak(713) ↔ L468 ksi(1−ksi)/w |
| S4 | ΔU_hys≥0 / Ω≤2RT→0 / 분기 ±½σ_d | PASS | eq:dUhys(465)·eq:Ubranch(477) ↔ func_U_branch L138 |
| S5 | χ_d 충전 1−χ / ΔH_a^eff=ΔH_a−χ_dΩ | PASS | eq:chid(788)·eq:dHeff(794) ↔ func_chi_d L160·func_dH_a_eff L152 |
| S6 | ∂lnL_q/∂V: 컷상수→운영 0(부등식=동기) | PASS | 815-818·S6(1036) 자기모순 0 |
| S7 | 꼬리 충전 격자역전 / dQ/dV 방전 거울(양수) | PASS | eq:reversal(887) ↔ L474-477 ξ[::-1]…[::-1] |
| S8 | 분극 V_n=V_app−σ_d|I|R_n(방전 측정>내부) | PASS | eq:vn(250) ↔ L412; flowchart 6-29 정정 정합 |

부호 결함 0/8. (단 부호 *유도 다리*의 비정합은 H3/M1로 별도 — 박스 부호 자체는 전건 정확.)

---

## 6. master 삼각검증 노트 (G-derive 에이전트 과대평가 정정)
- G-derive 에이전트가 eq:weff를 "박스 부호 반대(1−↔1+) = CRITICAL"로 보고했으나, master 직접 손 검산 결과 **박스값(1−Ω/2RT)이 물리·코드(func_w_eff L144) 모두 정확**(Ω=2RT서 w_eff→0, spinodal 문턱 일치). 실제 결함은 본문 μ 부호 규약(θ vs ξ)이 박스로 매끄럽게 연결 안 되는 *유도 다리*이므로 **HIGH(유도)로 하향**. 박스 변경 금지(v11 1:1 유지) — 수정은 유도 다리 부호 정합 + 중심기울기 중간식 추가로.
- D-PEAK는 3개 에이전트 중 2개(D-PEAK 전담·그림 전담)가 독립 적발 + master 수치 재현 = 삼각 일치 → 확정 CRITICAL.
