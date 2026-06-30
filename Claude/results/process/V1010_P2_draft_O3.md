# V1010 P2 Ch1 정련 supplement — 경쟁 드래프트 O3 (객관·물리 무결 골격)

> **역할**: Anode_Fit v1.0.10 **P2 챕터1 9종 경쟁 드래프트 O3**(작업 sub). 드래프트만 — 본 supplement 는 Ch1 본문(`graphite_ica_ch1_v1.0.10.tex`)을 *수정하지 않는다*. 정련 방향과 누락 보완 식을 **식→식 유도**로 제시하는 제안서다.
> **대상 (ground truth)**: ① 이론 문건 `Claude/docs/v1.0.10/graphite_ica_ch1_v1.0.10.tex`(1867줄) ② 코드 검증 앵커 `Claude/results/process/V1010_P1_code-audit_RESULT.md`(코드 = `Anode_Fit_v1.0.10.py` 703줄; tex 본문은 동일 모델 `Anode_Fit_v11_final.py` 706줄을 인용하나 헤더 L3·L100 에서 1.0.10 라벨 matched 선언) ③ broadening·w 설계명세 `Claude/results/research/broadening_w_design.md` ④ 종모양 기원 verdict `Claude/results/research/radius/ORIGIN_VERDICT.md`.
> **표기 (4-tier)**: [확정]=tex 식·코드 줄 직접 근거 / [근거 미발견]=문건·코드로 못 짚음 / [추정]=설계 의도·교재 표준에서 추론 / [미검증]=수치 round-trip 미실시.
> **부호·차원 규약**: 모든 보완 식은 부호(삽입 기준)·차원([J/mol/K] 등)·극한($|I|\to0$, $\Omega\to2RT^+$, $\rho\to\delta$)을 적대 검산해 제시. 독자 평가·메타 발언 0.

---

## §0. supplement 의 위치 — 무엇을 정련하나 (작성 전 사전 점검)

P2 작업지시문은 Ch1 을 "코드 플로우차트 충실 물리화학 교과서"로 정련하되 (LCO 코드는 P4 예고, P2 는 이론) supplement 를 산출하라고 명한다. 본격 작성 전, **현 v1.0.10 이 이미 가진 것**과 **정련 여지**를 가른다(과잉 보완·중복 제안 차단).

| 영역 | 현 v1.0.10 보유 [확정] | P2 정련 여지 |
|---|---|---|
| 코드 spine 매핑 | N0--N9 + `tab:nodemap`(노드↔식↔코드 식별자) | **P1 audit 의 코드 거동(死코드·조건부 inert·해상도 의존)이 tex 서술과 어긋나는지** 교차 — §1 |
| broadening | `sec:broadening` 3출처(①②③) + `eq:ensavg` + `fig:broadening` | ③ 앙상블 통계역학이 **코드의 단일 유효입자 구조와 정합**한지, ρ(U_app) 가 w_j 에 흡수되는 경로가 코드 거동과 일치하는지 — §1-C |
| w 이중지위 | `sec:width` 단상=평형 예측 / 두-상=현상학적 — `eq:wbase` 한 식 | 코드가 **'n':1.0 고정으로 두-상도 RT/F 평가**하는 사실이 이중지위 서술과 모순 없는지 — §1-B |
| 누락 유도 다리 | Gibbs→μ→평형, spinodal, logistic(detailed balance), L_q, 인과꼬리 전부 (a)→(d) 단계 | **9 드래프트·tex 가 비운 다리**(grand-canonical↔logistic 의 화학퍼텐셜 부호, Sommerfeld 적분의 중간 단계) — §2 |
| LCO 이론 | `sec:lco-electronic` Sommerfeld 유도 + `eq:dSe`·`eq:dSegate` + 단위다리 + 분해 `eq:lco-decomp` | **Sommerfeld 적분 중간식 명시·전자 비열→엔트로피 적분의 교재급 완결·물리 무결(축퇴 극한·Mott 보정 한계)** — §3 (중점) |

→ 결론: v1.0.10 은 **골격이 거의 완비**. supplement 의 실질 = ① P1 코드 거동 vs tex 서술 정합 매트릭스(누락·과잉 적발), ② 비어 있는 *중간 유도 식*(특히 Sommerfeld 적분·grand-canonical 부호 다리)을 교재급으로 채움, ③ LCO 전자 엔트로피의 물리 무결성 강화. **모델 확장 0**(broadening 설계명세 D3·forward-only 준수).

---

## §1. ★ Ch1 ↔ 코드 coverage 매트릭스 (P1 맵 step ↔ Ch1 식, 누락·과잉)

P1 audit(`V1010_P1_code-audit_RESULT.md` §1·§2)이 코드를 24심볼·12 closed-form·플로우차트로 앵커했다. 그 코드 거동을 Ch1 의 식·서술과 1:1 대조한다. 기준 = **코드가 실제로 하는 일** vs **tex 가 그렇다고 적은 것**.

### 1-A. 노드별 정합표 (N0--N9, LCO 추가분 포함)

| 노드 | 코드 거동 (P1 §1, 줄근거) | Ch1 식 (tex) | 정합 |
|---|---|---|---|
| N0 | `curve`→`_direction_to_sigma`, $\lvert I\rvert$=c_rate·Q_cell (L505) | `eq:n0map`(L197) | ✔ [확정] |
| N1 | $V_n=V_\app-\sigma_d\lvert I\rvert R_n$ (L408) | `eq:vn`(L368) | ✔ [확정] |
| N1' 격자 | $n_\work=\max(2048, 2\lvert V_n\rvert)$ (L412), pad 0.15 | `eq:vwork`(L380) | ✔ 식 일치, **단 해상도 의존 경고 누락**(→ 1-D #3) |
| N2 | `func_U_j`=$(-\Delta H_\rxn+T\Delta S_\rxn)/F$ (L79), 배열 $T$ 대응 (L434) | `eq:Uj`(L448) | ✔ [확정] |
| N3 | `func_U_branch`(L148) 호출 (L447); **death: `func_U_j_hys`(L82) 미호출** | `eq:Ubranch`(L630)·`eq:center`(L642) | ✔ 식 일치, **死코드 명시 없음**(→ 1-D #1) |
| N4 | `func_w`=$nRT/F$ (L75); **`_n_factor` 'n':1.0 우선 → 'w' 폴백 inert** (L274) | `eq:wbase`(L714) + 이중지위 | ✔ tex 가 L1195-97 에서 명시 흡수(→ 1-B) |
| N5 | `func_ksi_eq` logistic, overflow-safe 분기 (L96-97) | `eq:xieq`(L770) | ✔ [확정] |
| N6 | `equilibrium`=$C_\bg+\sum Q_j\xi_\eq(1-\xi_\eq)/w$ (L366) | `eq:eqpeak`(L1130) | ✔ 면적=Q 검산 정합 [확정] |
| N7 | $\mathcal A=\min(z_\cut nRT, A_\cap RT)$ (L331)→`func_L_q`(L106)→×$\lvert$dVdq_qa$\rvert$(L347) | `eq:Acut`(L1372)--`eq:LV`(L1424) | ✔ [확정], **z_cut 조건부 inert 명시 없음**(→ 1-D #2) |
| N8 | `_causal_lowpass`(L110-128) DC gain=1; 충전 격자역전 (L473) | `eq:lowpass`(L1471)·`eq:reversal`(L1539) | ✔ [확정] |
| N9 | `dqdv_work += Q*peak_shape`→`np.interp` (L477·L479) | `eq:sum`(L1594) | ✔ [확정] |
| 분기 스위치 | $L_V<\nu\Delta_\mathrm{grid}$→평형종 (L462) | `eq:branch`(L1521), 진폭 불연속 명시 (L1529) | ✔ [확정], tex 가 D-PEAK2 로 정직 기술 |
| **LCO N5+** | **코드 부재** (P1 §2-E `grep "LCO\|dS_e"`→No matches) | `eq:dSegate`(L1036) plug-in 예고 | **과잉(미구현)** → P4 예고 — tex L1686 명시 [확정] |

→ **closed-form 12식 + N0--N9 + LCO 추가 4행(N0'/N2'/N5+/N9')** 전부 코드 식 또는 P4 예고와 1:1. **물리식 누락 0, 모델 과잉 0**(LCO 는 의도적 P4 예고).

### 1-B. ★ w 이중지위가 코드 거동과 정합하는가 [확정 + 추정]

**설계명세 요구**(`broadening_w_design.md` §2): 단상($\Omega<2RT$) $w=nRT/F$=평형 예측 / 두-상($\Omega>2RT$) $w$=현상학적 자유 피팅 폭. 명시 문장 1개로 구분.

**코드 사실**(P1 §1.2 `_n_factor`·§2 D 항): `GRAPHITE_STAGING_LIT` 의 4 전이는 **모두 `'n':1.0` 보유** → `'w':0.012~0.020` 폴백은 *死데이터*(inert). 따라서 코드의 실제 평가 폭은 *전이 무관* $w=RT/F\approx25.7$ mV [확정, P1 §1.2 L274].

**정합 판정**: tex 는 이 함정을 **정확히 짚었다** — `sec:width`(L731) "전부 두-상은 *초기값 상태*일 뿐", L1195-97 "현재 코드의 staging 출발값은 $n_j=1$ 고정이라 실제 평가 폭은 $RT/F\approx25.7$ mV 이고, 0.012/0.014 V 등 `'w'` 폴백은 `'n'` 을 제거해야 활성화된다". → **코드 거동(폴백 inert)과 tex 서술이 정합** [확정]. 이중지위는 *피팅 후 $\Omega_j$ 값이 갈린다*는 물리적 진술이고, *현재 출발 상태*는 전부 $n=1$ 평가라는 코드 사실을 tex 가 분리해 적었다.

**정련 제안 (모순 없음, 명료화만)** [추정]: 이중지위 절(L723-738)이 "*값*은 한 줄, *지위*는 $\Omega$ 가 가른다"를 잘 적으나, **"지위 분기는 코드 분기가 아니다"**라는 한 문장을 더 명시하면 오독이 줄어든다 — 코드는 $\Omega>2RT$ 여부로 `_width` 를 갈라 평가하지 *않고*(항상 `func_w` 한 식), 분기는 *해석 층*에서만 일어난다. tex L729 가 이미 "코드 분기가 아니라 그 전이의 $\Omega_j$ 값이 가른다"로 적었으므로 **추가 불요, 현 서술 유지가 정확**.

### 1-C. ★ broadening(집합 통계역학)이 코드 거동과 정합하는가 [확정 + 추정]

**설계명세 요구**(`broadening_w_design.md` §1(b)·§4): 세 출처 ①유한율속 비대칭 꼬리 ②내재 RT/F ③집합 다입자 통계역학(앙상블 ρ(U_j)). **forward 통계평균만(역산 X)**, 다입자/PSD 모델 0, 사이즈 효과 배제. **단일 유효입자 구조 유지**.

**코드 사실**(P1 §1.3·§5, `ORIGIN_VERDICT.md` §5): 코드는 **단일 유효입자 + kinetic lag $L_V(\propto\lvert I\rvert)$**. 즉 출처 ①은 `(ξ_eq−ξ_lag)/L_V`(N8, eq:peakshape)로 *모델에 실재*하고, ②는 $w=RT/F$ 의 floor 로 *암묵 실재*하나, ③(앙상블 ρ)은 **코드에 명시 항이 없다** — `dqdv`는 입자 1개의 응답만 계산한다 [확정, ORIGIN §5 "v11_final.py 는 단일 유효입자… (B-ii) PSD 분산은 없다"].

**정합 판정**: tex `sec:broadening`(L1158-1292)이 ③을 다루는 방식이 코드와 정합하는 핵심 = **③은 *모델 항*이 아니라 *현상학적 $w_j$ 에 흡수되는 설명*으로만 들어온다**. tex 가 이를 세 곳에서 못박는다:
1. `eq:ensavg`(L1222) 의 forward 적분 $\langle dQ/dV\rangle_\mathrm{ens}=\int\rho(U_\app)(dQ/dV)^\mathrm{single}_{U_\app}dU_\app$ 는 **설명용 forward 만**, 역산 금지 (L1236, L1266 (ii)).
2. L1274 (iii) "입자 크기 분포 위로 합성곱하는 다입자 *기계장치*는 모델에 넣지 않는다… 모델 차원은 늘지 않고, 늘어난 것은 ③의 *비-크기* 통계평균 *설명*뿐이다".
3. L1276 "코드의 forward 모델은 *단일 유효입자 + 동역학 지연 $L_V$*(N7·N8) 구조를 유지한다. 곧 앙상블 무질서는 현상학적 $w_j$ 한 파라미터로 흡수".

→ **코드(단일 유효입자)와 tex(③=설명·흡수, 모델 0)가 완전 정합** [확정]. 설계명세 D3(다입자/PSD 모델 X)·forward-only 가 tex 에 정확히 baked. **모델 과잉 0**.

**적대 검산 — ρ(U_app) vs ρ(U_j) 의 정합** [확정]: ORIGIN_VERDICT 의 핵심 교정("분포하는 것은 평형 $U_j$ 가 아니라 apparent-U $=U_j+\eta$ 의 $\eta$")이 tex `eq:ensavg`(L1225) 의 적분변수 $U_\app=U_j+\eta,\ U_j=$const 와 일치. v10-11 supersede 기록(tex L24·L1215-1221)이 ρ(U_j)→ρ(U_app) 정정을 명시 — **중심 상수 ↔ 폭(η) 분포 모순이 해소됨** [확정]. → broadening 절은 코드·verdict·설계명세 3자 정합. **정련 제안: 없음(현 서술이 물리 무결·코드 정합).**

**미세 정련 여지 (선택)** [추정]: `eq:ensavg`(L1231-1233) 가 "①(비대칭 skew)은 대칭 합성곱으로 표현 안 됨 → 적분 피적분 항 아님, $w_j$ 에 따로 흡수"라고 적어 $w_j\supset(②\otimes③)+①$ 로 묶는다. 이 분해가 정밀하나, **①(한 입자 시간변화 $\eta(t)$) vs ③(입자간 $\eta$ 산포)의 "같은 과전압의 다른 평균"**(L1327)이라는 통찰은 그림 캡션에만 있다. 본문 (b)-③ 마무리에 한 문장 승격 가능 — 단 *현 위치로도 완결*이라 강제 불요.

### 1-D. P1 audit 이 적발한 코드 거동 중 tex 가 *명시하지 않은* 3건 (누락 — 본문 무결성 무관, 부기 권고)

tex 는 *물리식*을 다루므로 아래는 본문 결함이 아니다. 다만 "코드 플로우차트 충실"을 표방하므로, P4(코드개정) 예고로 *각주 1줄* 부기하면 코드↔문건 추적성이 완결된다 [추정].

1. **死코드 `func_U_j_hys`(L82-91)** — tex `tab:nodemap` N3 은 `func_dU_hys`·`func_U_branch`만 적고 `func_U_j_hys` 는 언급 0. 실제 분기중심은 `func_U_branch`(L447)가 담당. tex 가 *正코드만* 인용한 것은 정확하나, P1 §2-D 가 死코드로 적발했으므로 "원형 보존 死함수 1건" 부기 가능 [확정, P1].
2. **z_cut 조건부 inert (L331)** — $\mathcal A=\min(z_\cut nRT, A_\cap RT)$ 에서 *기본 데이터셋(n=1, z_cut=4.357≥4.0)*은 $A=4RT$ 로 capped → z_cut inert. tex `eq:Acut`(L1372) 은 min 식을 정확히 적었으나, **"기본값에선 z_cut 이 binding 하지 않음"**은 미명시. P1 §2-D D4 가 self-test L691 z_cut=2.0 으로 binding 경로 실증. 부기 가능 [확정, P1].
3. **꼬리 활성/비활성의 해상도 의존 (L412)** — $n_\work=\max(2048, 2\lvert V_n\rvert)$ → 분기 스위치 임계 $L_V<\nu\Delta_\mathrm{grid}$($\Delta_\mathrm{grid}=v_\mathrm{span}/n_\work$)가 *사용자 V 점수에 종속*. 같은 물리 $L_V$ 라도 입력 해상도에 따라 평형종/꼬리종 분기. tex `eq:branch`(L1521)·`eq:vwork`(L380) 은 식을 적으나 *해상도 종속성*은 미명시. P1 §1.3 보완3 [확정, P1].

→ 3건 모두 **물리 무결성 무관**(死코드·조건부 inert·수치 해상도). tex 의 *물리 교과서* 성격엔 영향 0. 코드 추적성 완결을 원하면 `sec:sum` 또는 각 노드 codebox 에 1줄 각주.

---

## §2. ★ 누락 유도·다리 보완 (물리화학 교재·식→식) + v3~v9 통합

v1.0.10 은 (a)출발→(b)연산→(c)중간식→(d)박스 4단계 유도를 *거의 모든* 박스에 갖춰 v3~v9 의 압축 다리를 이미 복원했다(헤더 L42-49). 여기서는 **그 4단계에서도 *중간 한 칸*이 빠진** 두 자리를 교재급으로 채운다 — supplement 는 이 식들을 *제안*하고, 본문 편입은 P3 author 가 결정한다.

### 2-A. grand-canonical 점유 ↔ logistic 의 화학퍼텐셜 부호 다리 (sec:dist 보강) [추정·교재]

**현 tex 다리**(L875-879): "$\Delta\mu=-sF(V-U_j)$ … 지수 $\beta\Delta\mu=-s(V-U_j)/w_j$ … 따라서 `eq:fermifn` 은 $\langle n\rangle=1/(1+e^{-s(V-U_j)/w_j})$ 곧 $\xi_\eq$ 와 같은 식". → 부호 환산은 맞으나, **왜 $\Delta\mu\equiv\varepsilon_\mathrm{occ}-\mu_\mathrm{Li}=-sF(V-U_j)$ 인가**의 한 칸이 압축돼 있다.

**보완 다리 (식→식)**:
출발 — grand-canonical 점유의 자유에너지 비용은 자리 점유 에너지에서 입자 저장소(reservoir)의 화학퍼텐셜을 뺀 것:
$$\Delta\mu \equiv \varepsilon_\mathrm{occ}-\mu_\mathrm{Li}. \tag{2.1}$$
연산 — 평형 조건 `eq:eqcond`(tex L429)가 저장소 화학퍼텐셜을 전위로 환산한다: $\mu_\mathrm{Li}(\theta_\eq)=\mu^0-sF(V-U)$. 자리 점유 에너지를 기준 $\varepsilon_\mathrm{occ}\equiv\mu^0$(점유 자리의 표준 자유에너지)로 두면
$$\Delta\mu = \mu^0-\big[\mu^0-sF(V-U_j)\big] = -sF(V-U_j). \tag{2.2}$$
중간식 — 몰당↔자리당 환산($\beta\Delta\mu=\Delta\mu/(RT)$, $F\leftrightarrow$ 자리당 $e$, $R\leftrightarrow k_B$):
$$\beta\Delta\mu = \frac{-sF(V-U_j)}{RT} = -\frac{s(V-U_j)}{w_j},\quad w_j\equiv\frac{RT}{F}. \tag{2.3}$$
박스 (tex `eq:fermifn` 에 대입):
$$\boxed{\ \langle n\rangle=\frac{1}{1+e^{+\beta\Delta\mu}}=\frac{1}{1+e^{-s(V-U_j)/w_j}}=\xi_\eq.\ } \tag{2.4}$$

**부호 검산** [확정]: $V\uparrow$(방전 $s=+1$) → $\Delta\mu=-sF(V-U_j)\downarrow$(더 음) → 점유 자리가 저장소 대비 *비싸짐* → $\langle n\rangle\downarrow$? — 아니다. $\beta\Delta\mu\downarrow$(더 음) → $e^{+\beta\Delta\mu}\downarrow$ → $\langle n\rangle\uparrow$. 그런데 $\langle n\rangle$=리튬 *자리 점유*=$\theta$, 진행률 $\xi=1-\theta$. tex 가 $\xi_\eq$ 로 적은 것은 **부호 한 번 차이**(L207-208 $\theta=1-\xi$). → 식 (2.4)의 $\langle n\rangle$ 은 *점유 $\theta$* 인데 tex `eq:fermifn`→`eq:xieq` 가 $\xi_\eq$ 로 직결한다. **검증 필요점** [추정]: tex L876 의 "단일 자리 점유에 적용"에서 $\langle n\rangle$ 을 $\theta$ 가 아니라 *진행률 점유*로 재라벨했는지 — 부호 자기일관성은 유지되나(둘 다 logistic, $s$ 가 흡수), **라벨 명시**가 한 칸 더 친절하다. → P3 에서 "$\langle n\rangle$=리튬 자리 점유 $\theta_\eq$, $\xi_\eq=$ logistic 형 동일(부호 규약 흡수)" 한 줄 권고.

→ 이 다리가 **흑연 리튬-자리 분포 ↔ LCO 전자-준위 분포(Fermi-Dirac)의 동형**(tex `keybox` L890-895)을 떠받친다 — §3 의 출발점.

### 2-B. spinodal Taylor 소멸의 임계지수 한 칸 (sec:hys 보강) [확정·이미 있음, 강화 선택]

tex `eq:dUhys` 직후(L617-618)가 $\Delta U_\hys\to\frac{8RT}{3F}u_j^3\to0$, $u_j^3\propto(T_c-T)^{3/2}$ 를 적어 **임계지수 3/2 까지 이미 유도**. v3~v9 보다 강하다 [확정]. → **보완 불요**. 단 supplement 가 *교재 연결*을 더하면: 이 $3/2$ 는 mean-field 정규용액의 *order parameter* $u\propto(T_c-T)^{1/2}$(β=1/2 임계지수)에서 gap$\propto u^3$ 으로 따라나온 것 — Landau 이론의 mean-field β. tex 가 수식은 닫았으므로 *연결 한 줄*만 선택적. [추정]

### 2-C. v3~v9 통합 점검 — 이미 통합 완료 [확정]

설계명세 `broadening_w_design.md` §4(D1: v9→v10 통합·전부 때려박기)와 tex 헤더(L36-41) 대조: v9 흑연 forward + LCO 전자엔트로피 + ξ_eq 분포 + 통계역학 **보존** + broadening 절·w 이중지위·w_eff 제거 **추가**. tex L1858 의 broadening 참고문헌(leviaurbach1999·fly2020·dahn1995·dreyer2010·park2021·rsc2021) + cogswell2012 *드롭*(사이즈 배제) 이 설계명세와 1:1 [확정]. → **v3~v9 통합 누락 0**. supplement 가 새로 *가져올* 유도 원천 없음(ver.3/ver.5 포팅 금지 — 메모리 `feedback_anode_fit_chapter_dependency_tree` 준수).

---

## §3. ★ LCO 이론 정련 (중점) — 전자 엔트로피 Sommerfeld 교재급·물리 무결

P2 작업지시문이 LCO 이론 정련을 *중점*으로 명한다. 코드는 P4 예고(현 흑연 전용). 본 절은 **물리식 중심으로 LCO 양극 dQ/dV·전자엔트로피 Sommerfeld 를 교재급으로 닫고, 부호·차원·극한을 적대 검산**한다. 현 `sec:lco-electronic`(L924-1105)이 이미 강건하므로, supplement 는 **비어 있는 *중간 적분 단계*를 명시**하고 **물리 무결 경계(축퇴 극한·Mott 항·이중계산)**를 못박는다.

### 3-A. LCO dQ/dV 세 봉우리 — 흑연 식의 전극-불문 적용 [확정]

평형 peak `eq:eqpeak` $Q_j\xi_\eq(1-\xi_\eq)/w_j$ 는 전극 가정이 없으므로(tex `sec:lco-center` L466 "유도에 전극 가정 없음") LCO 양극에 그대로 [확정]:
- T1 (MIT) $\sim$3.90 V, T2 $\sim$4.05 V, T3 $\sim$4.17-4.20 V (tex `tab:lco-staging`).
- 세 전이 모두 $\Omega>2RT$ 두-상 → 폭은 *이중지위 두-상 측*(현상학적 피팅 폭, broadening 정함) [확정, tex L1149-1151].
- order-disorder 큰 $\Omega$ → spinodal gap 키워 T2·T3 좁은 한 쌍 peak.

**정련 제안 (물리 무결)**: 흑연과의 *유일한 구조 차이* = T1 의 전자 엔트로피 항. 이것이 §3-B--D 의 중점. **LCO peak 식 자체는 흑연과 byte-identical** — supplement 가 더할 식 없음.

### 3-B. ★ Fermi-Dirac → 전자 비열 $C_e$ → 전자 엔트로피 $S_e$ — Sommerfeld 적분 *중간 단계* 명시 (교재급)

현 tex `sec:lco-Se`(L944-969)가 (a)Fermi-Dirac→(b)정보엔트로피→(c)Sommerfeld→$S_e$→(d)박스를 닫는다. 그러나 **(c) 의 핵심 적분이 한 줄로 압축**돼 있다 — "표준 Sommerfeld 적분 $\int(-\partial f/\partial E)(E-E_F)^2 dE=\frac{\pi^2}{3}(k_BT)^2$ 가 전자 비열을 닫는다"(L959-961). 교재급으로 그 *중간 식*을 채운다.

**보완 유도 (식→식, Ashcroft-Mermin / Kittel 표준)**:

(a) 출발 — 전자기체 내부에너지. 상태밀도 $g(E)$(자리당, 스핀 포함), Fermi-Dirac $f(E)=[1+e^{(E-E_F)/k_BT}]^{-1}$:
$$U_e(T)=\int_{-\infty}^{\infty} E\,g(E)\,f(E)\,dE. \tag{3.1}$$

(b) 연산 — Sommerfeld 전개. 임의 매끈한 $H(E)$ 에 대해 축퇴 극한 $k_BT\ll E_F$ 에서
$$\int_{-\infty}^{\infty} H(E) f(E)\, dE = \int_{-\infty}^{E_F} H(E)\,dE + \frac{\pi^2}{6}(k_BT)^2 H'(E_F) + \mathcal{O}\!\Big[\big(\tfrac{k_BT}{E_F}\big)^4\Big]. \tag{3.2}$$
이 전개는 $-\partial f/\partial E$ 가 $E_F$ 근방 폭 $\sim k_BT$ 의 우함수형 첨두라는 데서 온다(짝수 모멘트만 생존).

(c) 중간식 — 비열로. $C_e=\partial U_e/\partial T$ 에 (3.2)를 $H=Eg$ 로 적용하면, $T$-독립 항(첫 적분)은 미분에서 죽고 둘째 항만 남는다. 표준 처방대로 $g(E)$ 를 $E_F$ 근방 상수 $g(E_F)$ 로 동결(tex L956-959 의 동결 정당화)하면 둘째 항의 모멘트 적분이
$$\int_{-\infty}^{\infty}\Big(-\frac{\partial f}{\partial E}\Big)(E-E_F)^2\,dE=\frac{\pi^2}{3}(k_BT)^2 \tag{3.3}$$
로 닫혀(표준 Sommerfeld 2차 모멘트), 비열이
$$\boxed{\ C_e=\frac{\partial U_e}{\partial T}=\frac{\pi^2}{3}k_B^2\,T\,g(E_F)\equiv\gamma_S T\ } \tag{3.4}$$
($T$-선형 전자 비열, Sommerfeld 계수 $\gamma_S=\frac{\pi^2}{3}k_B^2 g(E_F)$).

(d) 박스 — 엔트로피로. 3법칙 $S_e(0)=0$ 에서
$$S_e(T)=\int_0^T\frac{C_e(T')}{T'}\,dT'=\int_0^T \gamma_S\,dT'=\gamma_S T=\frac{\pi^2}{3}k_B^2\,T\,g(E_F). \tag{3.5}$$
$C_e/T'=\gamma_S$=상수라 적분이 곧바로 닫혀 **$S_e=C_e$**(전자기체의 특수성: 저온 $S_e=\gamma_S T=C_e$) — tex `eq:Se`(L967)와 일치 [확정].

**차원 검산** [확정]: $[\gamma_S]=[k_B^2][g(E_F)]=(\mathrm{J/K})^2\cdot(1/\mathrm{J})\cdot(\text{자리당})=\mathrm{J/K^2}$/자리 → $[\gamma_S T]=\mathrm{J/K}$/자리=$k_B$ 차원 ✔. $g$ 가 e/eV 단위면 eV→J ($1.602\times10^{-19}$) 환산 필요(tex L1000 명시) ✔.

**극한 검산** [확정]: $g(E_F)\to0$(절연체, $x\to1$) → $S_e\to0$(전자 엔트로피 꺼짐) ✔. $T\to0$ → $S_e\to0$(3법칙) ✔. $k_BT\not\ll E_F$(비축퇴) → (3.2) 전개 깨짐 → §3-D 경계.

→ 이 4단계가 tex 의 압축된 (c) 를 *교재 완결*로 편다. **편입 권고**: tex L959-963 의 한 문장을 식 (3.1)-(3.5) 로 확장(P3 author 결정).

### 3-C. ★ 전이당(삽입당) 전자 엔트로피 $\Delta S_{e,j}$ 와 단위 다리 — 부호 무결 [확정]

tex `eq:dSe`(L986)·`eq:dSemolar`(L995)·`eq:dSegate`(L1036)이 자리당→몰당 환산·MIT-logistic 게이트·부호를 닫았다. supplement 가 **부호 사슬을 독립 재검산**(P2 작업지시문 "부호·차원 적대검산"):

삽입 기준($x\uparrow$ 당) 전자 엔트로피:
$$\Delta S_{e,j}(x,T)=\frac{\partial S_e}{\partial x}\Big|_T=\frac{\pi^2}{3}k_B^2 T\,\frac{\partial g(E_F,x)}{\partial x}. \tag{3.6}$$
게이트 `eq:ggate` $g=g_\mathrm{max}[1-\sigma(\frac{x-x_\mathrm{MIT}}{\Delta x_\mathrm{MIT}})]$ → $\frac{\partial g}{\partial x}=-\frac{g_\mathrm{max}}{\Delta x_\mathrm{MIT}}\sigma(1-\sigma)<0$. 대입:
$$\boxed{\ \Delta S_{e,j}=-\frac{\pi^2}{3}k_B^2 T\,\frac{g_\mathrm{max}}{\Delta x_\mathrm{MIT}}\,\sigma(1-\sigma)<0\ }\quad(\text{삽입 기준}). \tag{3.7}$$

**부호 적대 검산** [확정] — *삽입($x\uparrow$)*: 금속→절연체, $g(E_F)$ 가 $g_\mathrm{max}\to0$ *감소* → $\partial g/\partial x<0$ → $\Delta S_{e,j}<0$. 물리: 전자 자유도가 *닫혀* 엔트로피 감소(삽입 시 음의 기여). *탈리튬화($x\downarrow$, 본 문건 LCO 충전 주진행)*: 절연체→금속, $g$ 켜짐 → $\lvert\Delta S_{e,j}\rvert=-\partial S_e/\partial x>0$ 방출($\sim0.18 k_B$/atom). → **흑연 삽입 $\Delta S_\rxn=-16$ J/mol/K 슬롯과 부호 일관**(둘 다 삽입 음) [확정, tex L1002-1009]. ✔

**단위 다리 적대 검산** [확정]: 자리당 (3.6)은 $[k_B^2]$ 차원(원자 1개당). forward 슬롯 $\Delta S_{\rxn,j}$ 는 몰당 J/(mol·K). $N_A$ 곱: $N_A k_B^2 = R k_B$ (자리당 $k_B$ 한 몫이 몰당 $R$ 로 승격):
$$\Delta S_{e,j}^\mathrm{mol}=N_A\frac{\partial S_e}{\partial x}=\frac{\pi^2}{3}R\,k_B\,T\,\frac{\partial g}{\partial x}\quad[\mathrm{J/(mol\,K)}]. \tag{3.8}$$
$N_A$ 누락 시 $\sim10^{23}$ 배 과소(tex L1689 경고) — **차원 함정 명시됨** ✔. 부호는 $N_A>0$ 불변 ✔.

**크기 검산** [확정]: 완전 metal 자리당 $S_e/k_B=\frac{\pi^2}{3}(k_BT)g(E_F)=3.29\times0.0259\,\mathrm{eV}\times13/\mathrm{eV}\approx1.1\,k_B$/atom($T$=300K). O3 부분몰 차 $\approx0.18 k_B$/atom — 같은 자릿수 ✔ (tex L1066). config(>½ 지배)보다 작으나 MIT 게이트로 필수.

→ **부호·차원·크기 3중 검산 통과**. tex 의 LCO 전자항 부호 사슬은 무결 [확정]. supplement 의 정련 = 위 독립 재검산을 *부호 회귀 self-test* 형식으로 `sec:signcheck` 의 R-항에 추가 권고(현 R1-R5 는 흑연 전용 — LCO 전자항 R6 추가 가능) [추정].

### 3-D. ★ 물리 무결 경계 — Sommerfeld 가정의 한계 명시 (교재급 정직성)

tex 가 함수형 tier A·anchor tier A·연속곡선 부재(G2)를 *3등급 분리*(L970-979)로 정직하게 적었다 [확정]. supplement 가 **물리 무결을 더 못박는** 세 경계를 명시(교재가 마땅히 적을 한계):

1. **축퇴 극한 $k_BT\ll E_F$ 의 정당성** [추정·교재]: Sommerfeld (3.2)는 이 극한에서만 성립. LCO 금속상 $E_F\sim$ eV 급, $k_BT\approx0.026$ eV(300K) → $k_BT/E_F\sim0.03\ll1$ → 전개 유효, 보정항 $\mathcal O[(k_BT/E_F)^4]\sim10^{-6}$ 무시 가능 ✔. **단 MIT *천이 중*($g(E_F)$ 가 0 에서 켜지는 구간)에는 $E_F$ 근방 상태밀도가 급변** → 동결 $g\approx g(E_F)$ 가 *천이 폭 내에서* 약화. tex 가 이를 게이트 폭 $\Delta x_\mathrm{MIT}$ 로 흡수(결함 분산)하나, **"천이 구간 자체의 Sommerfeld 유효성은 끝점(완전 metal)에서 가장 강하고 천이 중심에서 가장 약하다"**는 한계 한 줄 권고. forward 모델은 게이트로 보간하므로 실용상 무해(피팅 흡수).

2. **Mott 항(상태밀도 에너지 의존)의 무시** [추정·교재]: (3.2) 둘째 항의 정확형은 $\frac{\pi^2}{3}k_B^2 T\,g(E_F)$ 가 아니라 $g$ 의 에너지 미분 $g'(E_F)$ 보정을 포함($C_e=\frac{\pi^2}{3}k_B^2T[g(E_F)+\frac{\pi^2}{6}(k_BT)^2(g''-\frac{g'^2}{g})+\cdots]$). 표준 동결은 $g'(E_F)$ 항을 버린다(tex L956-959 의 "선도 차수"). LCO 금속상 $g(E)$ 가 $E_F$ 근방 완만하면 무해 — **이 무시가 선도 차수 근사임을 (이미 tex 가 적은) 명시 유지로 충분**. 추가 식 불요.

3. **이중계산 방지(config↔elec 직교)의 물리 한계** [확정·이미 있음]: tex `sec:lco-decomp`(L1647-1655)이 (가)가산성=$Z=Z_\mathrm{config}\cdot Z_\mathrm{elec}$ 인수분해(직교)·(나)무이중계산=슬롯 분리 규칙으로 갈라 못박았다. **MIT 부근 리튬정렬↔전자밴드 결합**(잔차 교차항)은 (가)에서 "선도 차수 직교, 결합 몫은 (나) 슬롯 분리로 통제"로 인정 [확정]. → 물리 무결. supplement 추가 불요.

→ **물리 무결 판정**: LCO 전자 엔트로피 절은 (i)Sommerfeld 함수형 tier A, (ii)부호 삽입-기준 무결, (iii)단위 다리 $N_A k_B^2=Rk_B$ 정확, (iv)이중계산 직교+슬롯분리, (v)축퇴 극한 유효 — **물리적으로 견고**. 정련 = 위 3-B 의 *중간 적분 단계 식 (3.1)-(3.5) 편입* + 3-D #1 *천이 구간 Sommerfeld 유효성 한 줄* 이 실질. 나머지는 현 서술이 이미 교재급.

### 3-E. ★ 전자항의 $T$-선형 식별 신호 — 다온도 피팅 무결 [확정]

tex L1010-1015 가 "$\Delta S_{e,j}\propto T$ → $\partial U_1/\partial T\rvert_e=\Delta S_{e,j}/F\propto T$ → *기울기 자체가 $T$-선형* → $U_1$ 이동 $\propto T^2$"를 닫았다. **식별 신호는 'peak 위치가 $T$-선형'이 아니라 '$\partial U/\partial T$ 가 $T$-선형'** — config·vib(상수 $\Delta S$)와 *결정적으로* 구분 [확정]. supplement 가 이를 *교재 검산*으로 확인:
$$U_1(T)=U_1(0)+\frac{1}{F}\int_0^T \Delta S_{\rxn,1}^\mathrm{cat}(T')\,dT';\quad \Delta S^\mathrm{cat}=\underbrace{\Delta S^0}_{\text{const}}+\underbrace{\gamma_S' T}_{\text{elec},\propto T} \tag{3.9}$$
($\gamma_S'\equiv N_A\frac{\pi^2}{3}k_B^2\partial g/\partial x$, 부호 음). 적분:
$$U_1(T)=U_1(0)+\frac{\Delta S^0}{F}T+\frac{\gamma_S'}{2F}T^2. \tag{3.10}$$
→ config·vib 는 $T$-선형 항($\frac{\Delta S^0}{F}T$), 전자항은 $T^2$ 항($\frac{\gamma_S'}{2F}T^2$). **다온도 dQ/dV 에서 $U_1(T)$ 의 *2차 곡률*이 전자항의 fingerprint** [확정, tex 와 정합]. 부호: $\gamma_S'<0$ → $T^2$ 항 음 → 고온서 $U_1$ 이 선형 외삽보다 *낮음*. 차원 ✔($[\gamma_S'/F]=$ V/K²). → **Ch2 가역 발열로 확장 시 이 $T$-의존이 핵심**(tex L1014). supplement 식 (3.9)-(3.10)은 *식별 신호의 명시 적분형* — 편입 선택.

---

## §4. 정련 제안 요약 (★ supplement 결론 — 본문 수정 X, P3 편입 후보)

| # | 위치 (tex) | 정련 종류 | 근거 | tier |
|---|---|---|---|---|
| P1 | `sec:dist` L959-963 | **중간 유도 식 편입** — grand-canonical $\Delta\mu=-sF(V-U)$ 다리 (§2-A 식 2.1-2.4) | 한 칸 압축 | [추정] |
| P2 | `sec:lco-Se` L959-963 | ★**Sommerfeld 적분 중간식 편입** (§3-B 식 3.1-3.5) — $U_e\to C_e\to S_e$ 교재 완결 | (c) 압축 | [확정·교재] |
| P3 | `sec:lco-electronic` L1010 | **전자항 $T$-식별 적분형 편입** (§3-E 식 3.9-3.10) — $U_1\propto T^2$ 곡률 fingerprint | 신호 명시 | [확정] |
| P4 | `sec:signcheck` R-항 | **LCO 전자항 부호 회귀 R6 추가** (§3-C 식 3.7 삽입-음 검산) | 흑연 전용 R1-5 보완 | [추정] |
| P5 | `sec:lco-Se` L979 후 | **천이구간 Sommerfeld 유효성 한 줄** (§3-D #1) — 끝점 최강·중심 최약 | 교재 정직 | [추정] |
| (부기) | 각 codebox 각주 | 코드 추적성 — 死코드·z_cut inert·해상도 의존 (§1-D 3건) | P1 audit | [확정] |

**비-정련(현 서술 유지 확정)**: ① w 이중지위(코드 폴백 inert 와 정합, §1-B) ② broadening ③ 앙상블(코드 단일유효입자·forward-only·모델 0 정합, §1-C) ③ spinodal Taylor 3/2(이미 유도, §2-B) ④ v3~v9 통합(누락 0, §2-C) ⑤ 이중계산 직교(이미 못박음, §3-D #3) ⑥ LCO peak 식(흑연 byte-identical, §3-A).

**물리 무결 종합 판정** [확정]: Ch1 v1.0.10 은 코드 플로우차트 충실·물리화학 유도 완결·LCO 전자엔트로피 Sommerfeld 견고. supplement 의 실질 = **비어 있던 *중간 적분 단계 식*(Sommerfeld $U_e\to C_e\to S_e$, grand-canonical 부호 다리, 전자항 $T^2$ 식별형)을 교재급으로 채우고, 부호·차원·극한을 독립 적대 검산해 무결을 재확인**. 모델 확장 0(설계명세 D3·forward-only 준수). **누락 유도 5건 보완·과잉 0·코드 정합 매트릭스 PASS.**

---

*작성: 2026-07-01 | P2 Ch1 경쟁 드래프트 O3(작업 sub, 드래프트 전용·본문 수정 X) | 입력: tex 1867줄·P1 result·broadening 설계명세·ORIGIN_VERDICT 전문 정독 | 산출: V1010_P2_draft_O3.md*
