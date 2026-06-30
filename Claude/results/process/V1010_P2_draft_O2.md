# V1010 P2 — Ch1 정련 supplement (드래프트 O2)

> **역할**: P2 챕터1 9종 경쟁 드래프트 중 O2(작업 sub). 드래프트 전용 — 본문 tex 수정 X·범위 밖 자의 X. 독립 작성.
> **목표**: Ch1(`graphite_ica_ch1_v1.0.10.tex`, 1866줄)을 *코드 플로우차트에 충실한 물리화학 교과서*로 정련하기 위한 supplement. LCO 코드는 P4 예고(이론만 P2).
> **입력 정독 완료**: ① Ch1 tex 전문(1866줄, N0–N9 + LCO 절 + 부호 검산 + thebibliography 24건) ② `V1010_P1_code-audit_RESULT.md`(맵·audit·인벤토리, 24심볼·12식·정정4) ③ `broadening_w_design.md`(broadening 3기작·w 이중지위·w_eff 제거·D1~D3) ④ `radius/ORIGIN_VERDICT.md`(델타→종 계층·apparent-U=U_j+η·forward-only).
> **표기 4-tier**: [확정]=코드·식 직접 줄근거 / [근거미발견]=문건·코드로 못 짚음 / [추정]=설계 의도 추론 / [미검증].
> **부호·차원·극한 적대검산** = 각 항 말미 별도 검산.

---

## §A. ★ Ch1 ↔ 코드 coverage 매트릭스 (P1 맵 step ↔ Ch1 식, 누락·과잉)

### A-0. 매트릭스 읽는 법
P1 result §1(24심볼·12 closed-form)·§2-A(물리식 충족도 12행)를 ground-truth 앵커로 삼아, Ch1 tex 의 박스식·\code{} 식별자·\label 을 그 위에 1:1 사상한다. 세 판정 열 —
- **Code→Ch1**: P1 의 코드 줄/식이 Ch1 에 박스식으로 전개되어 있는가(코드가 있는데 본문에 없는 = G-follow 결손 후보).
- **Ch1→Code**: Ch1 박스식이 코드 식별자로 닫히는가(본문이 코드 없는 식을 끌어왔으면 과잉 후보).
- **G-follow/G-usable**: 따라가짐(유도 다리 완결) / 사용성(이 식만으로 코드 짤 수 있나).

### A-1. 코어 forward 노드 N0–N9 (흑연) — 12 closed-form 전수 [확정]

| 노드 | P1 코드 식 (줄) | Ch1 박스식 (\label) | 코드 식별자 | Code→Ch1 | Ch1→Code | 비고 |
|---|---|---|---|---|---|---|
| N0 | σ_d, \|I\|=c_rate·Q_cell (curve L505) | eq:n0map | `curve`,`_direction_to_sigma` | ✔ | ✔ | 매핑 §1.0 |
| N1 | V_n=V_app−σ_d\|I\|R_n (L408) | eq:vn | `dqdv` L408 | ✔ | ✔ | (a)(b)(c) 3-다리 |
| N2 | U_j=(−ΔH+TΔS)/F (func_U_j L79) | eq:Uj | `func_U_j` | ✔ | ✔ | G→μ→평형조건 유도 완비 |
| N3 | ΔU_hys(artanh) (func_dU_hys L140) | eq:dUhys | `func_dU_hys` | ✔ | ✔ | spinodal→gap 유도 완비 |
| N3 | U^d=U+½σ_d h_η γ ΔU_hys (func_U_branch L148) | eq:Ubranch / eq:center | `func_U_branch` | ✔ | ✔ | 死코드 func_U_j_hys 는 본문에 *적절히 미등장* |
| N4 | w=nRT/F (func_w L75) | eq:wbase | `func_w`,`_width` | ✔ | ✔ | 이중지위 절 보유 |
| N5 | ξ_eq=logistic[s(V−U)/w] (func_ksi_eq L96-97) | eq:xieq | `func_ksi_eq` | ✔ | ✔ | Eyring→detailed balance 유도 |
| N6 | Q·ξ(1−ξ)/w (L366·L464) | eq:eqpeak | `equilibrium`,인라인 | ✔ | ✔ | 종 항등식 eq:belliden |
| N7 | A=min(z_cut·n·RT, A_cap·RT) (L331) | eq:Acut | `_resolve_lag_length` | ✔ | ✔ | |
| N7 | χ_d (func_chi_d L163) | eq:chid | `func_chi_d` | ✔ | ✔ | |
| N7 | ΔH_a^eff=ΔH_a−χ_d·Ω (func_dH_a_eff L155) | eq:dHeff | `func_dH_a_eff` | ✔ | ✔ | use_dH_eff 토글 명시 |
| N7 | L_q (func_L_q L106) | eq:Lqfull | `func_L_q` | ✔ | ✔ | T_*≡\|I\|h/(Q_cell k_B) 묶음 |
| N7 | L_V=\|dVdq_qa\|·L_q (L347) | eq:LV | `_resolve_lag_length` L347 | ✔ | ✔ | |
| N8 | ξ_lag 점화식 (_causal_lowpass L110-128) | eq:lowpass / eq:memory | `_causal_lowpass` | ✔ | ✔ | 적분인자→일반해→이산 IIR |
| N8 | peak_shape=(ξ_eq−ξ_lag)/L_V (L475) | eq:peakshape | 인라인 | ✔ | ✔ | |
| N8 | 분기 스위치 L_V<ν·Δ_grid (L462-475) | eq:branch | `min_lag_grid_steps` | ✔ | ✔ | 이산 모드 스위치 정직 기술 |
| N8 | 충전 격자 역전 ξ[::-1]…[::-1] (L473) | eq:reversal | `_causal_lowpass` 호출 | ✔ | ✔ | ★가장 미묘한 부호 |
| N9 | C_bg+Σ Q_j[·] (L477·L427) | eq:sum | `dqdv_work`,`np.interp` | ✔ | ✔ | 보존식 직접 미분 |

→ **12 closed-form + 보조식(eq:center·eq:branch·eq:reversal·eq:lowpass) 전부 양방향 cover [확정].** P1 §2-A 의 12식이 Ch1 박스에 0누락.

### A-2. ★ 누락·과잉·비대칭 cover 진단 (G-follow·G-usable 1급 렌즈)

코드↔식 1:1 은 위처럼 0누락이나, *교과서 충실성*(따라가짐·자기완결)의 관점에서 다음 비대칭이 남는다. 각 항은 §B(다리 보완)에서 메운다.

| # | 종류 | 위치 | 진단 | tier | 보완 |
|---|---|---|---|---|---|
| **M1** | 코드 동작↔본문 비대칭 | eq:center / dqdv L447 | 코드는 `func_U_branch(T_rep, 0, …)`로 *U_j=0 넣어 shift만 추출*해 배열 center 에 더한다(P1 §1.2). Ch1 §1.4 식(638-639줄)에 이 "0 넣기" 한 줄은 있으나, *왜 0 을 넣는가*(배열 U_j 와 스칼라 shift 분리)의 물리/수치 동기가 본문 prose 로는 한 박자 빠르게 지나간다. G-usable 경계. | [확정] | §B-1 |
| **M2** | 해상도 의존 미서술 | eq:branch / dqdv L412 | P1 보완3[확정]: `n_work=max(2048, V_n.size·2)` → 분기 문턱 `L_V<ν·grid_step`(grid_step=v_span/n_work)이 *사용자 V 점수에 종속*. Ch1 eq:branch 절은 ν·Δ_grid 문턱·진폭 불연속은 정직히 적으나 *Δ_grid 자체가 입력 해상도 함수*라는 점은 본문에 없음 — 재현코드 작성자가 같은 물리 L_V 로 다른 분기를 얻을 수 있음(G-usable 결손). | [확정] | §B-2 |
| **M3** | T 스칼라 전용 미명시 | eq:eqpeak / equilibrium L352 | P1 보완2[확정]: `equilibrium`은 `_finite_pos("T",T)`라 *T 스칼라 전용*(배열 T(V) 미지원), dqdv 는 L402-424 분기로 지원. Ch1 §sec:eqpeak·tab:nodemap 은 equilibrium 을 "|I|→0 기준선"으로만 적고 이 입력 제약은 없음. | [확정] | §B-3 |
| **M4** | 死코드 부호 함정 미언급(설계상 정당) | func_U_j_hys L82-91 | P1 보완1[확정]: 死함수 인자 `s:int=1` vs 대체 `func_U_branch`의 `sigma_d`. *死코드라 본문 미등장이 옳다*(교과서가 死코드를 끌어오면 오히려 노이즈). → **과잉 아님·미보완이 정답.** 단 P4 코드개정서가 死코드 제거 시 본문 영향 0 임을 부기로만 남길 가치. | [확정] | §B-4(부기) |
| **M5** | z_cut docstring 부정확(코드측) | A=min(z_cut·n·RT,…) L217 docstring | P1 정정2[확정]: 코드 docstring "ξ_eq 5%" 부정확(실제=정규화 미분 ξ(1−ξ)/0.25 의 5%). **Ch1 eq:Acut 절(1368-1370줄)은 "미분 5% 컷·점유 자체 아님"으로 정확** — 본문은 옳고 코드 docstring 만 틀림. 교과서 정련 사안 아님(P4 코드 docstring 수정 후보). | [확정] | 보완 불요(본문 정확) |

→ **과잉(Ch1 이 코드 없는 식을 끌어옴) = 0건 [확정].** 모든 박스식이 코드 식별자로 닫힘. 비대칭은 전부 *코드 동작의 미묘한 디테일이 본문 prose 에서 한 박자 압축된* G-usable 결손(M1-M3)이며, M4-M5 는 보완 불요(설계상 정당/본문 정확).

**[적대검산 — 매트릭스]** 12 closed-form 을 P1 §2-A 와 1:1 대조, 누락 행 0. 과잉을 찾기 위해 Ch1 박스식 전수(eq:vn·Uj·dUhys·Ubranch·wbase·xieq·eqpeak·Acut·chid·dHeff·Lqfull·LV·peakshape·sum 14개 + eq:center·branch·reversal·lowpass·belliden·db·logisticsolve)를 코드 식별자로 역사상 → 모두 닫힘. LCO 박스(eq:lco-dUdT·Se·dSe·dSemolar·ggate·dSegate·lco-decomp·msmr)는 *코드 미구현*이나 §sec:lco-code 가 "P4 plug-in 예고"로 명시 = 과잉 아님(예고된 미래 코드). **누락=0(코드↔식)·과잉=0·G-usable 결손 3건(M1-M3).**

---

## §B. ★ 누락 유도·다리 보완 (물리화학 교재·식→식·v3~v9 통합)

§A 의 M1-M3 다리 + Ch1 본문에서 *식→식 유도가 한 단계 점프*한 자리를 물리화학 교재 깊이로 메운다. 모든 보완은 *본문에 더할 prose/식의 초안*이며 결과식·부호·코드는 불변.

### B-1. [M1] 분기 shift 의 "U_j=0 넣기" — 배열·스칼라 분리의 정당화

**현 본문(638-648줄)**: eq:Ubranch 의 U_j 자리에 0 을 넣어 hys_shift 를 얻고 배열 U_j 에 더한다(eq:center).

**보완 다리(식→식)**: eq:Ubranch 는 $U_j^{\,d}(T)=U_j(T)+\tfrac12\sigma_d h_\eta\gamma\,\Delta U_j^\hys(T)$ 다. 여기서 두 항의 *T 의존 구조*가 다르다 —
- 첫째 항 $U_j(T)$ 는 비등온이면 $T_\work$ 배열을 통해 *격자별 배열*(eq:Uj, dqdv L434 배열 T 대응).
- 둘째 항 $\tfrac12\sigma_d h_\eta\gamma\Delta U_j^\hys$ 는 $\Delta U_j^\hys=\text{func\_dU\_hys}(T_\rep,\Omega)$ 가 *대표 온도 $T_\rep=\overline{T_\work}$ 의 스칼라*다(P1 §2-D 시그널체인: "분기 shift 는 T_rep 스칼라 근사", 의도적 단순화).

따라서 둘을 한 함수 호출로 합치면 *배열 U_j 가 스칼라 분기 함수 안으로 들어가 차원이 어긋난다*. 코드는 선형성 $U_j^{\,d}=U_j+(U_j^{\,d}-U_j)$ 를 이용해 *분기 증분만* 따로 뽑는다 —
$$\text{hys\_shift}\equiv U_j^{\,d}\big|_{U_j\to0}=\tfrac12\sigma_d h_\eta\gamma\,\Delta U_j^\hys(T_\rep),\qquad \text{center}=U_j(T_\work)+\text{hys\_shift}.$$
곧 "U_j=0 넣기"는 *eq:Ubranch 가 U_j 에 대해 affine(1차)*이라 상수항(U_j)과 증분항(shift)이 분리 가능함을 쓴 것이며, 배열(U_j)·스칼라(shift) 차원을 맞추는 표준 broadcasting 처방이다. 이 한 줄로 "왜 0 인가"가 닫힌다(M1 G-usable 회복).

**[적대검산]** 차원: hys_shift [V](ΔU_hys [V]×무차원), center=배열[V]+스칼라[V]=배열[V] ✔. 극한: γ→0 ⇒ hys_shift→0 ⇒ center=U_j(eq:center 둘째 분기 일치) ✔. 부호: σ_d=+1 방전 ⇒ shift>0(ΔU_hys≥0) ⇒ center↑(eq:Ubranch (d) 부호 일치) ✔.

### B-2. [M2] 분기 문턱의 해상도 의존 — Δ_grid=v_span/n_work 명시

**현 본문(eq:branch, 1520-1533줄)**: $L_V<\nu\Delta_\mathrm{grid}$ 면 평형 종, 아니면 꼬리. ν=2.

**보완 다리**: $\Delta_\mathrm{grid}$ 가 *고정 상수가 아니라 입력 해상도의 함수*임을 한 줄로 못박는다 — eq:vwork 에서
$$\Delta_\mathrm{grid}=\frac{V_{\work,n}-V_{\work,1}}{n_\work-1}=\frac{(1+p_\mathrm{lo}+p_\mathrm{hi})\,\Delta v}{n_\work-1},\qquad n_\work=\max(n_{\work,\min},\,2|V_n|),$$
($\Delta v=\max V_n-\min V_n$, $p_\mathrm{lo}=p_\mathrm{hi}=0.15$, $n_{\work,\min}=2048$). 따라서 사용자 입력 격자 점수 $|V_n|$ 가 $1024$ 를 넘으면 $n_\work=2|V_n|$ 로 커져 $\Delta_\mathrm{grid}$ 가 *작아지고*, 분기 문턱 $\nu\Delta_\mathrm{grid}$ 도 함께 내려간다. 곧 *같은 물리 $L_V$ 라도 입력 V 점수가 촘촘하면 꼬리종, 성기면 평형종*으로 갈릴 수 있다(P1 보완3[확정]). 이는 sub-grid 지연의 수치 불안정을 피하는 분기의 *불가피한 부작용*이며, 재현코드 작성자는 $L_V$ 와 $|V_n|$ 를 함께 보고해야 분기 거동이 재현된다(G-usable 회복). 권고: rate-tail 을 관측하려면 $|V_n|\gtrsim n_{\work,\min}/2=1024$ 또는 ν 를 키워 문턱을 깊은 꼬리로 민다.

**[적대검산]** 차원: Δ_grid [V/점]·ν[무차원]→문턱 [V], L_V [V] 비교 동차 ✔. 극한: |V_n|→대 ⇒ n_work→대 ⇒ Δ_grid→0 ⇒ 문턱→0 ⇒ 더 많은 전이가 꼬리종(단조) ✔. 부호: 모든 양 양수 ✔.

### B-3. [M3] equilibrium 의 T 스칼라 전용 — 한 문장 부기

**현 본문(§sec:eqpeak·facade 절·tab:nodemap)**: equilibrium = |I|→0 기준선.

**보완 다리(한 문장)**: equilibrium 은 `T=_finite_pos("T",T)`(L352)라 *등온 스칼라 T 전용*이며, 비등온 $T(V)$ 곡선은 dqdv(eq:vwork 의 $T_\work$ 보간, L402-424)에서만 지원된다. 곧 기준선(equilibrium)과 관측(dqdv)은 *온도 입력 차원이 다르다* — 다온도 ICA 를 equilibrium 으로 그리려면 온도마다 따로 호출해 합성해야 한다. (교과서 사용성: 독자가 equilibrium 에 배열 T 를 넣어 ValueError 를 만나는 함정 차단.)

**[적대검산]** 이 보완은 *제약 명시*라 식 무관. P1 §1.3·§1.4 7축표("T 스칼라 전용" vs "배열 T 지원")와 1:1 정합 ✔.

### B-4. [M4] 死코드 부기 — 본문 영향 0 명시 (보완 아닌 가드)

func_U_j_hys(L82-91)는 死코드이고 분기중심은 func_U_branch 가 담당(P1 §1.2·§2-D). *교과서가 死코드를 끌어오지 않은 것은 옳다*. 단 P4 코드개정서가 死코드를 제거할 때 *Ch1 본문은 1바이트도 영향받지 않음*(본문은 eq:Ubranch=func_U_branch 만 인용)을 P4 핸드오버에 부기. 이것은 §B 다리 보완이 아니라 *미래 코드 변경의 본문 불변 보증*이다.

### B-5. ★ v3~v9 통합 — Ch1 이 이미 흡수했거나 *의도적으로 덜어낸* 축의 처리

broadening_w_design §0·§4 와 헤더 주석(11-21줄)에 따르면 v3/v4/v5 가 가졌고 v8/v9 가 0 으로 만든 축이 v10-10/11 에서 *설명으로만* 복원됐다. 현 v1.0.10 본문이 그 통합을 어떻게 닫는지 확인·정련한다(과잉 재유입 금지).

| v3~v9 축 | v1.0.10 처리 | 정련 판정 |
|---|---|---|
| 평형 델타 vs 실측 종 (v3/v4/v5 보유, v8/v9 0건) | §sec:broadening (b) 3기작·fig:broadening 로 *설명* 복원 [확정] | ✔ 올바른 물리로 복원(다입자 기계장치 0) |
| w_eff(Ω) "종을 좁힘→델타" 절 (v3~) | 본문 자취 0(헤더 20·32줄 "w_eff 제거"), 코드 use_w_eff 제거(L7) | ✔ narrowing 반대방향 — 제거가 정답. 본문 §sec:width 가 "별도 좁힘 항 두지 않는다"(720-721줄)로 못박음 |
| 다입자/ρ_G 모델 기계장치 (v4/v5) | §sec:broadening (c)(iii) "PSD convolution 모델 도입 안 함" 3중 금지 [확정] | ✔ forward-only·ill-posed 차단 |
| 사이즈(반경)→U_j (v4/v5 일부) | §sec:broadening (c)(i) 전면 배제(τ∝r²·Gibbs-Thomson·PSD) [확정] | ✔ ORIGIN_VERDICT §2(A)·§3 정합(반경→U ~0.01mV) |
| 앙상블 통계역학 (v10 신규 요구) | (iii-a) Dreyer 평형 plateau + (iii-b) apparent-U=U_j+η broadening 2층 분리 [확정] | ✔ "중심 상수↔폭 분포" 모순 해소(eq:ensavg) |

→ **v3~v9 통합 = 이미 v1.0.10 에 *올바르게* 닫혀 있음.** O2 의 정련 기여는 *재유입 금지의 재확인*과, 아래 B-6 의 **(iii-a)/(iii-b) 분리가 식으로 더 단단해질 자리** 한 곳뿐이다(과잉 추가 X).

### B-6. ★ (iii-a) Dreyer 평형층 ↔ (iii-b) broadening 층 — 식으로 분리 강화 [추정 정련]

**현 본문(1207-1238줄)**: (iii-a) Dreyer 순차전환이 plateau(평형 델타)를 만들고, (iii-b) 그 델타를 apparent-U=U_j+η 의 앙상블 분포 ρ(U_app)(eq:ensavg)가 종으로 편다. 두 층을 섞으면 "중심이 분포한다"는 오류로 미끄러진다고 경고.

**정련(식→식, 본문 강화 초안)**: 두 층의 *수학적 지위 차*를 한 식으로 못박을 수 있다. (iii-a) 평형층은 단일입자 비단조 $V_\eq(\xi)$(eq:Veq, $\Omega>2RT$)를 *Maxwell 공통접선*으로 한 전위 $U_j$ 에 모으는 연산 —
$$\big(\tfrac{\dd Q}{\dd V}\big)^\mathrm{single}_\mathrm{eq}\;\xrightarrow{\ N\text{-입자 순차전환}\ }\;\delta(V-U_j)\quad(\text{plateau, }\eta=0\text{ 극한}),$$
곧 *적분변수 없는 결정론적 사상*(델타 생성)이다. (iii-b) broadening 층은 그 위에 *적분변수 U_app 을 도입*한 합성곱(eq:ensavg) —
$$\big\langle\tfrac{\dd Q}{\dd V}\big\rangle_\mathrm{ens}=\int\rho(U_\app)\,\big(\tfrac{\dd Q}{\dd V}\big)^\mathrm{single}_{U_\app}\,\dd U_\app,\qquad U_\app=U_j+\eta,\ U_j=\text{const}.$$
*핵심 구분*: (iii-a)의 적분변수는 없고(델타로 모임), (iii-b)의 적분변수는 *η(과전압)이지 U_j 가 아니다*. 같은 ρ→δ 극한에서 (iii-b)는 *(iii-a)가 만든 단일 델타로* 환원된다(eq:ensavg 의 ρ→δ(U_app−U_j)). 곧 두 층은 *합성 순서가 고정*(평형 델타 생성 → η 산포 합성)이며 가환이 아니다 — 먼저 η 를 분포시키고 평형을 따지면 "U_j 분포" 오류가 된다. 이 순서 비가환성이 본문 경고("둘을 섞으면 미끄러진다")의 *형식적 내용*이다.

또한 본문(1231-1233줄)이 정확히 적은 *①(skew)은 eq:ensavg 의 피적분 항이 아니다*를 식으로 보강 —
$$w_j\ \supset\ \underbrace{(\text{②}\otimes\text{③})}_{\text{eq:ensavg, 대칭 합성곱}}\ +\ \underbrace{\text{①}}_{\text{비대칭 skew, }L_V\text{ 가 따로}}.$$
대칭 합성곱(②⊗③)은 중심을 옮기지 않고 *폭만* 키우는 반면, ①(유한율속 꼬리, eq:peakshape)은 *치우침*(peak 를 한쪽으로 밂)이라 합성곱 커널로 표현 불가 — 그래서 ①은 eq:ensavg 밖, 동역학 $L_V$ 가 담는다. 이 분해가 "현상학적 $w_j$ = ②⊗③ 흡수, ① = $L_V$ 분리"의 *역할 분담*을 식으로 닫는다.

**[적대검산 — B-6]** 차원: eq:ensavg 적분 ∫ρ(U_app)[C/V] dU_app[V]=[C/V]·([V]^{-1}·[V])=[C/V] ✔(ρ 는 [1/V] 밀도). 극한: ρ→δ ⇒ ⟨dQ/dV⟩→단일입자 응답@U_j(③ 소멸) ✔(본문 1234-1236줄 일치). 부호: ρ≥0·단일입자 응답≥0 ⇒ 앙상블 평균≥0 ✔. 순서 비가환: η 먼저 분포→평형 따지면 U_j 가 흔들리는 *비물리*(GITT 입자무관 상수 park2021 위배) ⇒ 순서 고정이 물리 정합 ✔. ①≠합성곱: skew 는 홀수 모멘트(3차) 도입, 대칭 커널은 홀수 모멘트 0 ⇒ ① 표현 불가 [확정] ✔.

---

## §C. ★ LCO 이론 정련 (중점) — dQ/dV·전자엔트로피 Sommerfeld 교재급 갈고닦기·물리 무결

P2 의 중점. Ch1 §sec:lco-* 절(전자 엔트로피·MIT 게이트·decomp·MSMR 동형)을 *Sommerfeld 전개·Fermi-Dirac 통계역학 교과서 깊이*로 갈고닦되, 코드 무영향(P4 예고)·부호·차원·극한·단위 다리 전수 적대검산. 본문 결과식·tier·게이트 초기값은 불변.

### C-0. LCO 절 구조 한눈에 — 흑연 forward 틀 위의 *추가 1항*

| LCO 절 | 박스식 (\label) | 흑연 대비 추가/공유 | tier |
|---|---|---|---|
| §sec:lco-map | tab:lco-staging (T1-T3) | 파라미터 교체(같은 키 구조) | 초기값(Xia·Reynier·Motohashi) |
| §sec:lco-center | eq:lco-dUdT ∂U/∂T=ΔS^cat/F | *식·부호 흑연과 1:1*(전극 불문) | 함수형 tier A·값 x의존 |
| §sec:lco-electronic | eq:Se·eq:dSe·eq:dSemolar·eq:ggate·eq:dSegate | ★흑연엔 0인 전자항(MIT 고유) | 함수형 A·anchor A 단일점·곡선 부재(G2) |
| §sec:lco-decomp | eq:lco-decomp config+vib+elec | 3성분 분해(흑연=config+vib) | config>½ A·elec 게이트 |
| §sec:lco-code | eq:msmr 동형 | 구조 변경 0·파라미터+1항 | MSMR tier A |

### C-1. ★ Sommerfeld 전자 엔트로피 유도 — 교과서 무결 점검·갈고닦기

**현 본문(944-969줄, §sec:lco-Se (a)→(c))**: Fermi-Dirac f(E)→정보 엔트로피 합→축퇴 극한 Sommerfeld 전개→$C_e=\tfrac{\pi^2}{3}k_B^2 T g(E_F)$→$S_e=\int_0^T(C_e/T')\dd T'=\tfrac{\pi^2}{3}k_B^2 T g(E_F)$ (eq:Se).

**교과서 무결 점검** — 본문 유도 사슬의 각 단계를 표준 고체물리(Ashcroft-Mermin Ch.2 Sommerfeld 전개)와 대조, *물리 무결* 확인 + *압축된 다리* 보강:

**(점검 1) 정보 엔트로피 → Sommerfeld 의 다리 [확정·본문 정확, 다리 보강 가치].**
본문(952-955줄)은 "정보 엔트로피 $-k_B\sum[f\ln f+(1-f)\ln(1-f)]$ 가 축퇴 극한서 Fermi 준위 근방 좁은 열폭에만 살아 Sommerfeld 로 닫힌다"고 적고, *비열 경로*($U_e$ 미분→$C_e$→$S_e=\int C_e/T'$)로 우회한다. 이 우회는 *옳고 표준적*이나, 독자가 "정보 엔트로피 식과 $\tfrac{\pi^2}{3}k_B^2 T g(E_F)$ 가 같은가"를 직접 잇지 못한다. *직접 다리*(교재 식→식)를 보강:

엔트로피를 직접 Sommerfeld 전개하면 — 자유전자 엔트로피는 $S_e=-k_B\!\int g(E)[f\ln f+(1-f)\ln(1-f)]\,\dd E$. 치환 $\beta(E-E_F)\equiv\zeta$, $f=1/(1+e^\zeta)$ 에서 *피적분의 엔트로피 핵* $s(\zeta)\equiv-[f\ln f+(1-f)\ln(1-f)]$ 는 $\zeta=0$ 대칭의 종(폭~몇 $k_BT$)이며 $\int_{-\infty}^\infty s(\zeta)\,\zeta\,\dd\zeta=0$(홀짝), $\int_{-\infty}^\infty s(\zeta)\,\dd\zeta=\tfrac{\pi^2}{3}$ (표준 적분, Fermi 적분 항등식). $g(E)\approx g(E_F)$ 동결(아래 점검 2) 하에
$$S_e=-k_B\,g(E_F)\!\int s(\zeta)\,k_BT\,\dd\zeta=k_B\,g(E_F)\,k_BT\cdot\tfrac{\pi^2}{3}=\tfrac{\pi^2}{3}k_B^2\,T\,g(E_F),$$
곧 비열 경로 없이 *엔트로피 정의에서 직접* eq:Se 가 닫힌다($\int s(\zeta)\dd\zeta=\pi^2/3$ 한 항등식으로). 이 직접 다리가 비열 우회와 *같은 결과*임을 보여 정보 엔트로피↔Sommerfeld 의 G-follow 를 완결한다. (비열 경로도 보존 — 두 경로 일치가 교차검증.)

**(점검 2) $g(E)\approx g(E_F)$ 동결의 정당성 [확정·본문 명시적].**
본문(955-959줄)이 *명시 가정*으로 못박음 — 적분 기여 띠 폭 ~$k_BT$, 축퇴 $k_BT\ll E_F$ 서 그 창 안 $g(E)$ 에너지 의존 선도차수 무시. *교과서 무결* ✔. 보강 다리: 1차 보정은 Sommerfeld 전개 둘째 항 $\propto g''(E_F)(k_BT)^2$ 라 $S_e$ 에 $O((k_BT/E_F)^2)$ 상대보정 — LCO metal $E_F\sim$ eV, $k_BT@300K\approx0.026$ eV ⇒ 보정 ~$10^{-3}$ 무시 가능[추정, 자릿수]. 곧 anchor $g_{\max}=13$ e/eV 단일점 동결이 선도차수서 충분.

**(점검 3) anchor 크기 검산 재현 [확정].**
본문 1065-1067줄: $S_e/k_B=\tfrac{\pi^2}{3}(k_BT)g(E_F)=3.29\times0.0259\,\mathrm{eV}\times13/\mathrm{eV}\approx1.1\,k_B$/atom. *독립 재산출*: $\pi^2/3=3.2899$, $k_BT@300K=0.02585$ eV, ×13/eV=0.3361, ×3.2899=**1.106** $k_B$/atom ✔(본문 1.1 일치). O3 부분몰 차 ~0.18 $k_B$/atom(reynier2004, tier B)과 같은 자릿수 ✔.

**[적대검산 — C-1]**
- 차원: eq:Se $[k_B^2][K][1/E]=[J/K]^2[K][1/J]=[J/K]$ ✔(엔트로피). $g$ [상태/E/atom], 자리당 [J/K/atom].
- 부호: $s(\zeta)\ge0$(정보 엔트로피 음 아님)·$g(E_F)\ge0$·$T\ge0$ ⇒ $S_e\ge0$ ✔.
- 극한: $T\to0$ ⇒ $S_e\to0$(3법칙 정합, $C_e=\gamma T\to0$) ✔. $g(E_F)\to0$(절연체) ⇒ $S_e\to0$(전자 자유도 닫힘) ✔.
- 적분 항등식: $\int_{-\infty}^\infty s(\zeta)\dd\zeta=\pi^2/3$ — 표준(Wilson/Sommerfeld), 본문 둘째 모멘트 $\int(-\partial f/\partial E)(E-E_F)^2\dd E=\tfrac{\pi^2}{3}(k_BT)^2$ 와 *같은 $\pi^2/3$ 상수*에서 옴(비열-엔트로피 일관) ✔.

### C-2. ★ 자리당→몰당 단위 다리 ($k_B$→$R$) — 교재급 갈고닦기 [확정]

**현 본문(990-1001줄, eq:dSe→eq:dSemolar)**: 자리당 $\Delta S_{e,j}=\tfrac{\pi^2}{3}k_B^2 T\,\partial g/\partial x$ [$k_B^2$ 차원]를 forward 슬롯 $\Delta S_{\rxn,j}$[J/(mol·K)]에 넣으려면 $N_A$ 배 → $\Delta S_{e,j}^\mathrm{mol}=N_A\partial S_e/\partial x=\tfrac{\pi^2}{3}R k_B T\,\partial g/\partial x$ (eq:dSemolar), $N_A k_B^2=R k_B$.

**갈고닦기(단위 다리 명시·교재)**: 환산 핵심은 $N_A k_B=R$(기체상수 정의)와 $N_A k_B^2=(N_A k_B)k_B=R k_B$. 곧 자리당 양($k_B^2$)에 $N_A$ 한 번 곱하면 *$k_B$ 한 몫만 $R$ 로 승격*하고 나머지 $k_B$ 는 남는다 — 이것이 본문 "자리당 $k_B$ 한 몫이 몰당 $R$ 로 올라간다"(992-993줄)의 정확한 차원 내용. 결과 $\tfrac{\pi^2}{3}R k_B T\,\partial g/\partial x$ 는 *$R$(몰당)·$k_B$(여전히 자리당 에너지 척도) 혼합 차원*이 의도된 것 — $g$ 가 e/eV 단위면 eV→J 환산 $1.602\times10^{-19}$ 도 함께(본문 1000줄). **★실수 가드(본문 1687-1689줄과 정합)**: $N_A$ 누락 시 전자항 ~$10^{23}$ 배 과소 ⇒ forward 에서 전자항이 *완전 무력화*(config+vib 만 남음). 이 가드는 P4 코드 plug-in 의 *1순위 단위 검산*이다.

**[적대검산 — C-2]** 차원: eq:dSemolar $[R][k_B][K][\partial g/\partial x]$. $\partial g/\partial x$ [상태/eV/atom](x 무차원당). eV→J 후 $[J/(mol\,K)][J/K][K][1/J/atom]$… *자리당→몰당 환산이 $\partial/\partial x$(Li 1몰 삽입당)와 결합*해 최종 [J/(mol·K)] ✔(forward 슬롯 동차). 자릿수: $\tfrac{\pi^2}{3}R k_B T\cdot(g_{\max}/\Delta x_\mathrm{MIT})$ 의 골 깊이 ~ 본문 0.18 $k_B$/atom×$N_A$≈1.5 J/(mol·K)(499줄·1660줄 일치) ✔. 부호: $N_A>0$ ⇒ 환산 부호 불변(eq:dSe<0 → eq:dSemolar<0) ✔.

### C-3. ★ MIT-logistic 게이트 부호 무결 — $\Delta S_e<0$(삽입 기준) 전수 [확정·중점]

**현 본문(eq:dSe·eq:dSegate, 985-1045줄 + 1002-1009줄 부호 규약)**: 삽입($x\uparrow$)으로 금속→절연체 ⇒ $g(E_F)$ $g_{\max}\to0$ 감소 ⇒ $\partial g/\partial x<0$ ⇒ $\Delta S_{e,j}=\partial S_e/\partial x<0$(삽입 기준 음). 닫힌식 eq:dSegate 가 leading $-$ 부호로 $\Delta S_{e,j}<0$ 을 식 자체에 못박음. 탈리튬화 시 $|\Delta S_e|>0$ 방출.

**부호 무결 전수(교과서 갈고닦기, 식→식)**:
1. 게이트 eq:ggate: $g(E_F,x)=g_{\max}[1-\sigma(\tfrac{x-x_\mathrm{MIT}}{\Delta x_\mathrm{MIT}})]$. $x\downarrow$(탈리튬화)로 $\sigma\downarrow$ ⇒ $[1-\sigma]\uparrow$ ⇒ $g\uparrow$(0→$g_{\max}$) ✔(절연체 $x\approx1$ ⇒ $g\approx0$, metal $x\to0$ ⇒ $g\to g_{\max}$).
2. $\partial g/\partial x$: 연쇄율 $\partial\sigma/\partial x=\sigma'(z)/\Delta x_\mathrm{MIT}=\sigma(1-\sigma)/\Delta x_\mathrm{MIT}>0$, 따라서 $\partial g/\partial x=-g_{\max}\partial\sigma/\partial x=-\tfrac{g_{\max}}{\Delta x_\mathrm{MIT}}\sigma(1-\sigma)<0$ ✔.
3. eq:dSegate: $\Delta S_{e,j}=\tfrac{\pi^2}{3}k_B^2 T\,\partial g/\partial x=-\tfrac{\pi^2}{3}k_B^2 T\tfrac{g_{\max}}{\Delta x_\mathrm{MIT}}\sigma(1-\sigma)<0$. leading $-$·모든 인자 양 ⇒ *식 자체가 음 못박음* ✔.
4. 흑연 일관: 흑연 $2\to1$ 삽입 $\Delta S_\rxn=-16$ J/(mol·K)<0(tab:staging)과 *같은 삽입-기준 음부호* ⇒ 슬롯 부호 규약 일관 ✔(본문 1002-1009줄·1659-1660줄).

**★부호 공존 무결(오독 방지, 본문 496-503줄 갈고닦기)**: 전체 $\Delta S_\rxn^\mathrm{cat}\approx+80$ J/(mol·K)>0(단전극 대표 스케일, swiderska2019)과 T1 전자항 $\Delta S_{e,1}<0$ 이 *모순 아님* — 전자항은 ~1.5 J/(mol·K)(0.18 $k_B$/atom×$N_A$) 규모의 *소수 음 보정*이라 ~+80 의 양의 합에 얹혀도 총 부호 불변. 두 양은 *서로 다른 종류*(±80=전체 계수 대표 스케일, config/vib/elec 합 / 전자항=한 성분의 골). 이 "층위 다름"이 무결의 핵심 — 같은 종류로 착각해 "+80 vs −1.5 모순"으로 읽으면 오류.

**[적대검산 — C-3]**
- 부호 사슬: $x\downarrow⇒\sigma\downarrow⇒g\uparrow$ / $\partial g/\partial x<0$ / $\Delta S_{e}<0$(삽입) / $|\Delta S_e|>0$(탈리튬 방출) — 4단 일관 ✔.
- 극한: $x=x_\mathrm{MIT}$ ⇒ $\sigma(1-\sigma)=\tfrac14$ 최대 ⇒ 골 최심(fig:lco-electronic 봉우리 중심) ✔. $|x-x_\mathrm{MIT}|\gg\Delta x_\mathrm{MIT}$ ⇒ $\sigma(1-\sigma)\to0$ ⇒ $\Delta S_e\to0$(T1 외 소멸·국소화) ✔.
- 차원: eq:dSegate $[k_B^2][K][상태/eV/atom]/[무차원]$ → 자리당, ×$N_A$=몰당(C-2) ✔.
- T 의존: $\Delta S_e\propto T$ (eq:Se 의 $T$) ⇒ $\partial U_1/\partial T|_e=\Delta S_e/F\propto T$ *T-선형*, U-이동 $\propto T^2$ ✔(본문 1010-1014줄·1099줄 — "위치가 아니라 *이동률*이 T-선형"이 식별 신호, 다른 항=상수 ΔS 와 구분).

### C-4. ★ LCO dQ/dV 세 봉우리 — 평형 peak 식의 양극 적용 무결 [확정]

**현 본문(§sec:lco-peak, 1144-1156줄)**: 평형 peak eq:eqpeak $Q_j\xi_\eq(1-\xi_\eq)/w_j$ 는 전극 불문 ⇒ LCO 하프셀 세 봉우리(T1~3.90/T2~4.05/T3~4.17-4.20 V). 폭 $w_j=n_jRT/F$, 세 전이 모두 $\Omega>2RT$ 두-상 ⇒ §sec:width 이중지위의 *두-상 측*(현상학적 피팅 폭). order-disorder 큰 Ω 가 spinodal gap 키워 T2·T3 좁은 한 쌍.

**정련 점검(무결)**: LCO 세 전이가 *모두 두-상(Ω>2RT)*이라는 진술이 흑연(초기값 4개 전부 Ω>2RT, 738줄)과 *동일 구조*임을 확인 — 둘 다 "초기값 거친 추정, 피팅 후 갈림"(733-738줄). 단 LCO 는 흑연과 달리 *solid-solution 전이가 표에 없음*(T1-T3 전부 상전이) ⇒ LCO 는 흑연의 "dilute→stage4·4L-3L 단상" 대응이 없다. 이 비대칭은 *물리적*(LCO 0.5≤x≤1 영역은 order-disorder·MIT 가 지배)이며 본문 tab:lco-staging 와 정합. broadening(iii) 앙상블 통계역학은 *흑연 두-상에 국한*(1199-1205줄), LCO 는 *일반 η 분포만*(흑연-특정 turbostratic 무질서 근거 미이식, tier C 동형 가정) — 이 scope 분리가 무결(LCO GITT 입자무관 OCP 확정 시 tier 갱신 명시).

**[적대검산 — C-4]** eq:eqpeak 전극 불문: 유도(보존식 미분→종 항등식 eq:belliden)에 전극 가정 0 ⇒ LCO 적용 무결 ✔. 위치=중심 $U_j^d$·순높이=$Q_j/(4w_j)$·면적=$Q_j$ 세 양 전극 불문 ✔. T1 위치 온도이동 $\partial U_1/\partial T$ 가 전자항 $\Delta S_{e,1}\propto T$ 로 *T-선형 이동률*(C-3) ⇒ 관측 신호 ✔.

### C-5. ★ config+vib+elec 분해 무결 — 가산성·무이중계산 분리 [확정·정련]

**현 본문(eq:lco-decomp, 1630-1667줄)**: $\Delta S_\rxn^\mathrm{cat}=\Delta S^\mathrm{config}+\Delta S^\mathrm{vib}+\Delta S_e^\mathrm{mol}$. (가) 가산성=config(Li 자리 점유 배열)·elec(전자 밴드 점유) *직교 자유도* ⇒ $Z=Z_\mathrm{config}Z_\mathrm{elec}$ 인수분해 ⇒ $S=S_\mathrm{config}+S_\mathrm{elec}$. (나) 무이중계산=★이중계산 금지(B) 규칙(config 슬롯=봉우리 중심 표준값만, logistic 이 내부 조성의존 담음 / elec 슬롯=MIT 게이트 골만).

**교과서 무결 점검(정련)**: 본문이 *가산성(더해도 되나)*과 *무초과(과대계상 없나)*를 명확히 분리(1647-1655줄)한 것은 통계역학적으로 정확 —
- 가산성: 독립 부분계 분배함수 곱 ⇒ 엔트로피 합($S=k_B\ln Z=k_B\ln Z_\mathrm{config}+k_B\ln Z_\mathrm{elec}$). MIT 부근 Li 정렬-전자 밴드채움 결합은 *교차항(잔차)*이나 선도차수서 0, 결합 몫은 (나) 슬롯 분리로 따로 통제 ⇒ *분해 자체 가산성은 선도차수 성립* ✔.
- 무이중계산: config 봉우리 *내부* 조성의존 $R\ln[(1-\xi)/\xi]$ 는 logistic(§sec:dist 점유분포)이 *자동 생성* ⇒ config 슬롯엔 *중심 표준값 $\Delta S_j^0$ 만* ⇒ 같은 엔트로피 두 번 안 셈 ✔. (config 값 = tab:lco-staging 의 중심 표준값으로 읽음, 1646줄.)

→ "직교성=더해도 되는가 / 이중계산 금지=과대 없는가" 이원 보증이 *교과서 무결*. O2 정련 기여: 이 분리가 §sec:dist 의 *점유분포 다리*(흑연 Li 자리 ↔ LCO 전자 준위, 같은 Fermi-함수형)와 *한 언어*임을 재확인 — config 의 logistic 자동생성과 elec 의 Fermi-Dirac 가 *같은 grand-canonical 점유 통계*(eq:fermifn↔eq:fd)라, 가산성이 "두 점유 분포의 독립 곱"으로 자연 귀결(890-895줄 keybox 다리).

**[적대검산 — C-5]** 가산성: $Z=Z_cZ_e ⇒ \ln Z=\ln Z_c+\ln Z_e ⇒ S$ 합 ✔(독립 극한). 무초과: config 중심값+elec 골, 각 자유도 몫만 ⇒ 측정 ΔS 초과 X ✔. 부호: config(O3 영역 >½ 양 지배, reynier2004)·vib(음 baseline)·elec(삽입 음 골) 합 ⇒ 대표 +80(C-3 공존 무결) ✔. 직교 가정 한계: MIT 부근 결합 = 교차항, 본문이 *근사 직교*·*선도차수*로 정직히 한정(tier 병기) ✔.

### C-6. ★ MSMR 동형 — 방향인자 $f=-\sigma_d$ 무결 [확정]

**현 본문(§sec:lco-code, eq:msmr, 1669-1694줄)**: MSMR $x_j=X_j/(1+\exp[f(U-U_j^0)/\omega_j])$ ↔ Ch1 $\xi_\eq=1/(1+\exp[-\sigma_d(V-U_j^d)/w_j])$. 대응: $X_j\leftrightarrow Q_j$, $U_j^0\leftrightarrow U_j^d$, $\omega_j\leftrightarrow w_j$, $f\leftrightarrow-\sigma_d$. 지수 $+f(U-U_j^0)$ vs $-\sigma_d(V-U_j^d)$ ⇒ $f=-\sigma_d$.

**무결 점검**: 방향인자 대응 $f=-\sigma_d$ 가 *지수 자리 비교*에서 강제됨을 식으로 재확인 — 두 logistic 이 같은 점유(0→1)를 같은 방향으로 그리려면 지수 부호가 일치해야 하고, MSMR $+f$·Ch1 $-\sigma_d$ 가 같은 자리 ⇒ $f=-\sigma_d$ 必. 이로써 탈리튬화/리튬화 진행 방향이 두 모델 일관(본문 1678-1681줄). 결론: Ch1 곡선 클래스(func_ksi_eq·func_U_j·eq:sum)는 *구조 변경 0*으로 LCO 적용, 바뀌는 것은 ①파라미터 교체 ②전자항 plug-in 1줄(P4).

**[적대검산 — C-6]** 부호: MSMR $f=+1$ 종 ↔ Ch1 $\sigma_d=-1$(즉 $f=-\sigma_d$) 같은 진행 ✔. 차원: 지수 $f(U-U_j^0)/\omega_j$ 무차원 ↔ $-\sigma_d(V-U_j^d)/w_j$ 무차원 ✔. 구조: 합산 $\sum_j X_j$(MSMR)↔$\sum_j Q_j$(eq:sum) 동형 ✔. plug-in: 전자항은 eq:dSemolar(몰당, $N_A$ 가드 C-2)만 T1 ΔS 에 가산 ⇒ 구조 불변 ✔.

---

## §D. 종합 — O2 정련 기여 요약 (드래프트)

1. **§A 매트릭스 [확정]**: 12 closed-form + 보조식 N0-N9 양방향 cover *누락=0·과잉=0*. G-usable 결손 3건(M1 분기 0-넣기·M2 해상도 의존·M3 T 스칼라)만 다리 필요. M4(死코드)·M5(z_cut docstring) 보완 불요(설계 정당/본문 정확).
2. **§B 다리 [확정+추정]**: M1-M3 식→식 보완(B-1 affine 분리·B-2 Δ_grid=v_span/n_work·B-3 T 스칼라 부기). v3~v9 통합은 *이미 올바르게 닫힘*(B-5, 재유입 금지 재확인). B-6 = (iii-a 평형층 델타생성 / iii-b broadening η-합성) *순서 비가환·①≠대칭커널* 식 강화(정련).
3. **§C LCO 중점 [확정]**: Sommerfeld 전자엔트로피 *직접 엔트로피 경로*($\int s(\zeta)\dd\zeta=\pi^2/3$)로 정보엔트로피↔eq:Se G-follow 완결(C-1). 단위 다리 $N_A k_B^2=R k_B$·$10^{23}$ 가드(C-2). MIT 게이트 부호 4단 사슬·+80↔−1.5 공존 무결(C-3). 세 봉우리 전극불문·scope 분리(C-4). config+vib+elec 가산성↔무이중계산 이원 보증·점유분포 한 언어(C-5). MSMR $f=-\sigma_d$ 무결(C-6).
4. **물리 무결**: 부호 8/8(§sec:signcheck S1-S8)·전자항 부호 4단·차원 전수·극한($T\to0$·$g\to0$·$\rho\to\delta$·$|I|\to0$)·단위 다리 — 적대검산 통과, *코드 무영향(LCO=P4 예고)·결과식/tier/게이트 초기값 불변*.

> **본 supplement 는 드래프트(O2)** — 본문 tex·코드 미수정. 마스터가 9종 경쟁 중 채택·통합한다. 모든 식→식 보완은 *본문에 더할 초안*이며 결과식·부호·코드·tier 불변. 입력 4건 전문 정독 근거.
