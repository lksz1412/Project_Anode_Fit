# REVIEW1 — v7-08.tex 적대 검수 (검수 sub, 리뷰 전용)

> 대상 `v7-08.tex` (597행) 전문 정독 / 판정기준 `Anode_Fit_v11_final.py`·`v11_flowchart.md`·`AUTHOR_BRIEF.md` 정독.
> 본 파일은 리뷰 산출물 1개 — 어떤 코드/문건도 수정·커밋하지 않음.

---

## 1. 확정 결함 {심각도 · 행 · 틀림 · 옳은 형}

### CRIT-1 — eq:dqdvwork 의 `+` 누락 (선형 합산이 곱으로 변질)
- **행**: 533–537 (식 N9 첫 누적식)
- **틀림**:
  ```
  dqdv_work(V_work) = C_bg(V_work)  Σ_j Q_j peak_shape_j(V_work)
  ```
  `C_bg(V_work)` 와 `Σ` 사이에 연산자가 없어 **`C_bg × Σ` (병치 곱)** 으로 읽힌다.
- **옳은 형**: `dqdv_work = C_bg(V_work) + Σ_j Q_j·peak_shape_j`.
- **근거**: v11 코드 L431 `dqdv_work = C_bg` 초기화 → L481 `dqdv_work = dqdv_work + tr['Q']*peak_shape` (가산 누적). 바로 다음 식 eq:masterv11(L543)은 `C_bg + Σ` 로 `+` 보유 → **인접식·코드와 직접 모순**. 본문 L532 "선형 합산" 표현과도 충돌. N9는 곡선 도착점 — 누적 부호 오류는 1급.

### HIGH-1 — eq:equilibrium 의 ξ_eq 가 분기중심 U_j^d 로 묶임 (equilibrium()은 U_j 사용)
- **행**: 372–376 (eq:equilibrium), 기호 정의는 326–330(eq:xieq, center=U_j^d)
- **틀림**: eq:equilibrium 의 `ξ_eq,j` 는 eq:xieq 에서 **center=U_j^d (분기 적용)** 로 정의됨. 그러나 코드 `equilibrium()` L369 는 `func_ksi_eq(T,V,U_j,n_j)` 로 **분기 미적용 U_j·s=+1** 사용(flowchart L65 "히스 미반영" 명시).
- **옳은 형**: equilibrium 의 ξ_eq 는 `U_j`(비분기) 기준임을 식/기호 수준에서 분리해야. 현재 boxed 식이 U_j^d-묶인 기호를 그대로 사용.
- **완화**: 본문 L377 prose 가 "분기를 쓰지 않는 한계"로 일부 보강 — 그러나 boxed 식 자체는 여전히 모호. (확정 결함, 심각도 HIGH 하향 불가 — 박스식이 코드와 불일치.)

### HIGH-2 — ΔU_hys 유도의 핵심 중간식(OCV–ξ 관계) 누락 (G-follow 단절)
- **행**: 209–225 (spinodal ξ_s^± → eq:dUhys)
- **틀림**: 본문은 "두 spinodal **전위**의 차"라 하나, 조성 ξ_s^±=(1±u)/2 를 전위로 환산하는 사상
  `V(ξ) = U − (RT/F)ln[ξ/(1−ξ)] − (Ω/F)(1−2ξ)` 를 **한 번도 적지 않음**. 학부생이 eq:spinodal→eq:dUhys 를 따라갈 수 없음.
- **옳은 형**: V(ξ) 정규용액 OCV 식을 명시 중간식으로 승격 후 ξ_s^± 대입(검산: 대입하면 정확히 (2/F)[Ωu−2RT·artanh u] 산출 — 결과식 자체는 코드 func_dU_hys L130 과 일치, **유도만 생략**).
- **부수 증거**: fig:hysbranch(247)가 V(ξ) S-curve 를 그림으로 보이지만 본문에 그 식이 없어 그림이 미정의 관계를 가리킨다.

### MED-1 — eq:weffraw "중심 기울기 일치에서" 무유도 단정
- **행**: 286–290
- **틀림**: w^eff=(RT/F)(1−Ω/2RT) 를 "중심 기울기 일치"라는 한 마디로 던짐(유도 0). G-follow 미달.
- **옳은 형**: ξ=1/2 에서 dV/dξ 를 정규용액에서 미분해 RT/F·(1−Ω/2RT) 산출하는 1–2줄 중간식 필요.

### MED-2 — eq:dlnLdV 에서 (1+e^{−A/RT}) 항의 A-의존 무시
- **행**: 444–450
- **틀림**: ∂lnL_q/∂V = −(χ_d/RT)·∂A/∂V 로 적었으나 코드 ln_Lq(L96)의 `−ln(1+e^{−A/RT})` 항도 A-의존(+). 또한 코드 A 는 `min(z_cut·n·RT, A_cap·RT)` 로 V-무관 상수 → ∂A/∂V 프레이밍 자체가 휴리스틱.
- **옳은 형**: "활성화 지배 + A 단조증가 가정" 명시하거나 (1+e^{−A/RT}) 항 부호 기여를 병기. 결론 부호(<0)는 유지되나 식이 부분적.

---

## 2. 강점 3 · 약점 3 (가장 약한 1)

**강점**
1. 부호 사슬 8항 중 7항이 v11 코드와 **글자 단위 정합**(func_U_j·func_ksi_eq·func_dU_hys·func_U_branch·func_chi_d·func_dH_a_eff·충전역전 L474-477·분극 L412). keybox(586)가 4식으로 닫음.
2. spine N0→N9 순서가 flowchart(권위)와 정확히 일치 — 브리프 §3 제안순(w/ξ_eq 선행)과 충돌 시 **flowchart 우선** 올바른 판단(N3 분기를 N4 앞에 배치).
3. staging 표(569-572)·defaults(579)가 GRAPHITE_STAGING_LIT·__init__ 와 전수 일치 — G-usable 초기값 닫힘.

**약점**
1. **(가장 약한 1) CRIT-1 eq:dqdvwork `+` 누락** — 도착 노드의 누적식이 곱으로 변질, 인접 master 식·코드와 직접 모순. 재현 코드를 식대로 짜면 곡선이 틀어짐(G-usable 직접 파괴).
2. 두 핵심 유도(ΔU_hys, w^eff)가 결과식만 제시·중간식 생략(HIGH-2·MED-1) — "수식 주도·보편식 먼저" 규범 미달, 가장 짧은 문건 후보다운 유도 압축.
3. equilibrium() 기호 정합 미세 균열(HIGH-1) — 박스식 ξ_eq 가 분기중심에 묶임.

---

## 3. 차원 점수 (6 × 5 = /30)

| 차원 | 점수 | 근거 |
|---|---|---|
| 척추 정합(N0–N9) | 5/5 | flowchart 순서·노드 전수 커버, 권위 우선 판단 정확 |
| 부호 정합(8항 대조) | 4/5 | 7/8 글자단위 PASS, 1건(CRIT-1 N9 누적)에서 `+` 누락 |
| G-follow(유도) | 2/5 | ΔU_hys·w^eff 핵심 중간식 누락, V(ξ) 미정의 |
| G-usable(재현·STAGING) | 3/5 | 표·defaults 닫힘이나 CRIT-1 이 재현식 깨뜨림 |
| 완결성(orphan/그림) | 5/5 | 4그림 전부 신규·ASCII·\ref·orphan 0, 절 다리 의무 충족 |
| 형식(수식주도·전보체·다리) | 4/5 | 전보체 거의 없음·절 도입/마무리 양호, 단 유도 압축이 수식주도 규범 일부 침해 |
| **합** | **23/30** | |

---

## 4. 부호 8항 PASS/FAIL + 근거

| # | 항목 | 판정 | 근거 |
|---|---|---|---|
| 1 | U_j=(−ΔH+TΔS)/F | **PASS** | eq:UjT(180) = code func_U_j L69 |
| 2 | ξ_eq=logistic[σ_d(V−U)/w], 방전 V↑→ξ↑ | **PASS** | eq:xieq(326) z=σ_d(V−U^d)/w = code L86 |
| 3 | dξ/dV=σ_d·ξ(1−ξ)/w, peak 양수 | **PASS** | eq:dxidVsig(361)·eq:eqpeakshape(366) |
| 4 | ΔU_hys≥0, Ω≤2RT→0, 분기 ±½σ_d | **PASS** | eq:dUhys(218)·eq:Ubranch(228) = code func_dU_hys/func_U_branch L130/138; 검산 V(ξ_s^±) 차 정확 |
| 5 | χ_d=χ/1−χ, ΔH_a^eff=ΔH_a−χ_dΩ | **PASS** | eq:chidHeff(421) = code func_chi_d L160·func_dH_a_eff L152 |
| 6 | ∂lnL_q/∂V<0 | **PARTIAL** | eq:dlnLdV(446) 부호 결론 맞으나 (1+e^{−A/RT}) 항·A 상수성 무시(MED-2). FAIL 아님(결론 정합)·식 불완전 |
| 7 | 충전 격자 역전 ξ[::-1]…[::-1], 충전=방전 거울 | **PASS** | eq:chargelowpass(483) = code L474-477 |
| 8 | V_n=V_app−σ_d|I|R_n | **PASS** | eq:polarization(131)·eq:interpout(558) = code L412 |

추가: **eq:Lq(N7 L_q) 전수 검산 PASS** — eq:Lqdef(L_q=|I|/Q_cell·k_j) + eq:kuniv 대입 → eq:Lq, code func_L_q L96 ln_Lq 와 정확 일치(부호·k_BT/h·1/(1+e^{−A/RT}) 모두 정합).

**부호 FAIL 항: 없음(8항 중 7 PASS, 6번 PARTIAL).** 단 N9 누적식 자체의 연산자 결함(CRIT-1)은 부호체크리스트 8항 밖의 별도 1급 결함.
