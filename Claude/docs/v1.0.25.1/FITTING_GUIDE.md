# Anode_Fit v1.0.20 — 피팅 추천 가이드 (모델 ↔ 데이터)

> **v1.0.20**: 문건(Ch1 66p·Ch2 25p) 검수·보강 정합판. 코드는 v1.0.19 와 물리·수치 동일(게이트 G1 bit-exact — `test_gates_v1020.py`)·헤더만 갱신. 본 가이드의 절차·초기값·회귀 기준은 그대로 유효하며, 회귀 기준값의 U_j 평가 규약은 Ch2 부록 B.4(환산값 (−ΔH+TΔS)/F — 표시 반올림 입력 금지)를 따른다.

> `Anode_Fit_v1.0.20.py`(흑연 음극 + LCO 양극 MSMR + 가역 발열)를 실측 dQ/dV·엔트로피 계수에 피팅하는 워크플로. **v1.0.19 = Ch1+Ch2 전면 재작성 정합 + x̄→U_oc 솔버·x̄ 진입점(`solve_U_oc`·`entropy_coefficient_x`·`reversible_heat_x`) 추가(가역발열을 조성 x̄에서 직접 산출).** 파라미터 tier·round-trip 절차·초기값/경계·수렴 판정 + **역방향 식별 사슬(S0–S5)·가정 울타리·잔차 진단표**. 이론 근거 = Ch1(dQ/dV·LCO)·Ch2(발열). ★흑연 회귀 0-diff 는 피팅 전 과정 불변(LCO 편입이 흑연 경로 무섭동). **v1.0.15 = 이산 전압 격자 완전 퇴출→점별 연속 메모리 적분(아래 §1 점별 주). v1.0.16 = 폭을 n 으로 fit·폭 T-의존 4단 사다리·선택적 n(T)(§1.5).**

## 0. 방향 규약 (★LCO 데이터 걸기 전 필독 — Ch1 sec:lco-direction, eq:lco-sigmaslot)

- 모델의 방향 인자 σ_d 의 물리 내용은 셀 라벨이 아니라 **탈리튬화(산화) 진행 = +1** 이다(Ch1 eq:lco-sigmaslot). 흑연 음극 하프셀은 방전=탈리튬화라 라벨=물리가 겹치지만, **LCO 하프셀은 충전이 탈리튬화**다.
  - ★**v1.0.14 전극 인지 환산 구현**: `LCOCathodeDQDV.curve()` 는 셀 라벨을 그대로 받는다 — **LCO 충전 곡선 ↦ `direction="charge"`** 로 주면 내부에서 자동으로 σ_d=+1(탈리튬화)로 환산된다(`_delith_is_discharge=False`). 라벨을 손으로 뒤집어 넣지 말 것. 저수준 `dqdv(s=...)` 는 환산 없이 물리 부호(탈리튬화=+1)를 직접 받는다.
  - 이 규약으로 분극(V_app>V_n)·히스 분기(탈리튬화 봉우리가 위)·꼬리 인과(시간=전위 오름차순) 세 작용처가 흑연과 1:1 유지된다. 평형 종 자체는 ξ↔1−ξ 대칭이라 어느 읽기로도 같은 봉우리(잠복형 — 봉우리가 맞아 보여도 방향 의존 3작용처가 틀어진다).
  - 현재 `LCO_MSMR_LIT` 는 Omega·dH_a 미배정 → 분기·꼬리 비활성이라 실질 방향 의존은 분극뿐.
- MSMR 대응은 f=+σ_d(진행률↔진행률 pairing, 원계열 f=F/RT>0 의 재모수화 — Ch1 eq:lco-msmrmap).

## 1. 파라미터 tier 표

| tier | parameter | scope | 초기값 | 하한 | 상한 | 제약 | 필요 데이터 | release |
|---|---|---|---|---|---|---|---|---|
| 1 (peak 골격) | U_j **또는** (ΔH_rxn, ΔS_rxn) | 전극 공통 | 표 초기값 | — | — | U_j 순서보존 | 저율 등온 dQ/dV | 확정 |
| 1 | n_j (폭 w=n·RT/F; **폭은 n 으로 fit**) | 공통 | 1.0 | >0 | ~4 | n>0; 폭 T-의존은 §1.5(상수 n→상수 w→n(T)) | 봉우리 폭(각 실측 T) | 확정 |
| 1 | Q_j | 공통 | 표 | >0 | — | ΣQ_j ≈ Q_total(면적보존 게이트 ±5% — §6) | 용량 | 확정 |
| 1 | Cbg | 공통 | 0 | — | — | — | baseline | 확정 |
| 2 (히스·비대칭) | Ω | 공통 | 표(흑연)·**LCO 미배정** | ≥0 | — | ★하한 금지 — 히스 분기는 Ω>2RT(≈4958@298K) 전이에서만 발효(gap=0 연속), 단상 전이는 Ω<2RT 피팅 기대(Ch1 §width·Ch2 파생 C); Ω 는 dH_a_eff(=dH_a−χ_d·Ω)로 문턱 무관 발효하므로 lb 를 걸면 꼬리 물리가 오염 | 충·방전 pair | 피팅 |
| 2 | γ | 공통 | 0 | 0 | 1 | γ∈[0,1] | 충·방전 gap | 피팅 |
| 2 | Rn | 공통 | 0 | ≥0 | — | — | 분극 이동 | 피팅 |
| 3 (동역학 꼬리) | dH_a | 공통 | 표(흑연)·**LCO 미배정** | >0 | — | — | rate-series(ΔH_a^eff 의 다온도 확정은 S4) | 피팅 |
| 3 | dVdq_qa | 공통 | 0.30 | >0 | — | ★누락=silent 꼬리 off | rate-series | 피팅 |
| 3 | χ | 공통 | 0.5 | 0 | 1 | χ∈[0,1] — 식별 신호는 꼬리 기울기(S3, 방향별 전달계수) | 등온 다전위 꼬리(rate-series) | 피팅 |
| 4 (다온도) | dS_rxn, dS_a | 공통 | 표 | — | — | 부호 문헌일치; ★dS_rxn 은 (ΔH_rxn,ΔS_rxn) 서식 전이에서만 발효 — 'U' 서식에 dS_rxn 만 얹으면 **silent 무시**(dS_eff=0). 다온도 진입 전 모든 전이를 (ΔH,ΔS) 서식으로 전환 | 다온도 | 피팅 |
| — | g_max_eV, x_MIT, dx_MIT | **LCO 전자항** | 13/**0.85**/0.05(v1.0.14 — T1 물리 anchor 로 재정렬 완료) | — | | ΔS_e 골≈−46 J/mol·K | 엔트로피 계수 | 시연 정렬 완료·피팅 갱신 |

- ★**LCO Ω_j 지위**: `LCO_MSMR_LIT` 세 dict 전부 `'Omega'` 키 미배정 → 코드는 `Ω=0` 폴백으로 **히스 분기 비활성**. Ch1 §lco-hys 의 spinodal·gap 식은 Ω_j^cat 이 round-trip 으로 배정될 때를 위한 구조식이고, 두-상 거동은 **Ω_j^cat>2RT 로 피팅되는 전이에 한해** 발효된다. LCO 충·방전 pair 를 확보하기 전에는 tier-2 를 LCO 에 열지 말 것.
  - **LCO tier-2/3 초기값 출발점(갭 명시)**: LCO 전용 Ω_j^cat·dH_a^cat 의 문헌 anchor 는 **근거 미발견(갭)** — pair/rate 데이터 확보 후 개방 시 출발점은 흑연과 같은 정규용액·활성화 스케일(Ω: 수천~1.3만 J/mol, 발효 문턱 2RT≈4958 J/mol@298K 대조; dH_a: 계면 활성화 문헌 범위 25–59 kJ/mol — Ch1 tab:staging 하단과 같은 '경향 anchor' 지위)에서 잡되, 이는 초기값일 뿐 신뢰값이 아니다(피팅 override 전제). 이 갭 때문에 LCO 피팅이 tier-1(골격)에서 멈추는 것은 정상 경로다.
- 가드: 코드 `_finite_pos`/`_finite_nonneg` 가 T·I·Q_cell·dict 값의 유한·부호를 fail-fast. bound(n>0·χ∈[0,1]·dVdq_qa>0·dx_MIT>0)는 fitting wrapper 스키마에서 별도 강제.
- ★**점별 아키텍처(v1.0.15~)**: 균일 작업 전압 격자·1차 저역통과 점화식·역보간·ν(min_lag_grid_steps) 분기 스위치가 **아키텍처에서 제거**됐다. 꼬리는 연속 메모리 적분 $\xi_\mathrm{lag}(V)=\frac1{L_V}\int_{-\infty}^{V}\xi_\eq(u)e^{-(V-u)/L_V}du$ 의 **점별 평가**이고(Ch1 §1.9), 평형 종은 그 $L_V\to0$ 해석적 극한이다(eq:tail-limit) — 구판의 격자 문턱(`L_V<ν·Δ_grid` 시 꼬리 off)이 만들던 ~23% 이산 점프가 원천 사라졌다. 제거된 생성자 파라미터: `min_lag_grid_steps`·`grid_pad_lo/hi`·`n_work_min`·`v_span_floor`(잔존 입력 = 무시). 회귀 골든은 점별 코드로 재정초(v1.0.15).

## 1.5 폭 피팅 규약 — fit n·실측 T·폭 T-의존 4단 사다리 (v1.0.16, 근거 CLOSING_v1.0.15 Part 4)

봉우리 폭은 **w 맨값이 아니라 다중도 n 으로 fit** 한다(w=n·RT/F, RT/F 는 물리 앵커). n 은 무차원 비이상·분산 인자(n=1 이상 단전자 Nernstian / n<1 협폭 / n>1 광폭)라 해석 가능하고, **같은 n 이 봉우리 폭과 가역열 config 항을 동시에 정해 자기정합**(완전식)이다. 고정 T 에서 n·w fit 은 전단사 동치라(n=wF/RT), 둘의 실질 차이는 **다온도 거동**에서만 난다.

**실측 T 투입**: `dqdv(V_app, T, …)`·`entropy_coefficient(V_n, T)` 는 각 측정점의 실제 온도를 받는다 — 등온 = 스칼라, 비등온 = V_app 길이 배열 T(V). 폭 w=n·RT/F 가 그 점의 실측 T 를 반영한다(가정 아닌 실측 조건).

**폭 T-의존 4단 사다리 (선험 가정 아닌 데이터 확정)**:
1. **기본 = 상수 n**(열적 w∝T). 단상 전이는 물리 정당(lattice-gas 등온선 기울기 RT/F).
2. **다온도 per-T 진단**: 여러 실측 T 에서 전이별 n 을 각각 fit(n(T_k)) → T-독립이면 열적 스케일 확증(상수 n 확정).
3. **n 이 T 로 드리프트** → 그 전이를 **상수 w(T-동결)** 로 전환(전이 dict 에서 `'n'` 제거·`'w'` 지정; 대개 두-상 broadening). config 항 자동 소거(단순식, `_dwdT`=0).
4. **그래도 안 맞으면 최소 n(T)**: 전이 dict 에 `'n_T1'`([1/K])·`'n_T_ref'`([K], 기본 298.15) → n(T)=n+n_T1·(T−n_T_ref) 선형 잔여만. 전 자유 n(T)·불충분 다온도 데이터는 과적합(identifiability 붕괴).

**★n(T) → 가역열 config 동반(자동)**: n(T) 채택 시 $\partial w/\partial T=(R/F)(n(T)+T\,n_{T1})$ 이라 `entropy_coefficient` 의 config 항이 자동 정합 전파된다(코드 `_dwdT`). 폭 fit 과 발열이 **한 n(T) 로 묶여** 산출되므로, 두-상 폭의 실제 T-의존이 비열적이면 폭 다온도 fit 과 발열 예측 양쪽에서 함께 드러난다(진단 하나로 검출). **상수 n(n_T1 부재)은 v1.0.15 와 bit-exact**(additive).

**참고 — w 이중지위**(Ch1 §width·Ch2 파생 C): 단상(Ω≤2RT)=평형 예측 폭 / 두-상(Ω>2RT; LiC₁₂[2L→2]·LiC₆[2→1] 둘만)=현상학적 자유 피팅 폭 — 어느 지위인지는 **Ω 가 가르지 폭 키가 아니다.** 두-상에 열적 서식 config 적용은 '물리 유도 아닌 **모델 선택**'(Ch2 srcbox 헤지: 실측 T-동결이면 단순/완전식 우열 ~0.3 mV/K 뒤집힘). ★staging 표의 좁은 폭(`'w'` 폴백 0.012–0.020 V)은 **거친 초기값**이고 `'n':1` 이 눌러 실폭=RT/F=25.7 mV(FWHM 90.5 mV) — 좁은 폭을 실제로 쓰려면 `'n'` 제거는 **피팅 선택**(골든 영향)이지 버그 정정 아님(Ch1 §width 명시).

## 1.6 vib 엔트로피 θ_E 피팅 규약 — Einstein 양자 보정 (v1.0.18.2, 제안 1)

vibrational 엔트로피는 기본이 **T_ref(298.15 K) 동결 상수**(ΔS⁰_j 에 흡수, 고전극한 kBT≫ℏω)다. 준양자 모드(kBT~ℏω, 예 LiCoO₂ 광학 포논 50–80 meV → θ_E≈580–930 K)는 작은 잔여 T-의존을 남겨 다온도 피팅에서 **electronic 항(∝T)에 섞일 수 있다**. 분리하려면 전이 dict 에 **`'theta_E'`([K], Einstein 온도)**(+선택 `'theta_E_Tref'`, 기본 298.15)를 주어 명시 T-의존을 회복한다:

- **S_vib(T;θ_E)=R[−ln(1−e^{−u})+u/(e^u−1)], u=θ_E/T** (단일모드 Einstein = Ch2 eq:Svib_mode 특수화). 고온극한 → R[1+ln(T/θ_E)](현 동결과 정합), 저온 →0.
- **additive**: θ_E 부재 = 현 동결과 **bit-exact**(골든 불변). 부여 시 중심 U_j += ΔU_vib(Helmholtz 자유에너지 편차)·가역열 ΔS_eff += [S_vib(T)−S_vib(T_ref)] **짝으로**(round-trip ∂ΔU_vib/∂T=ΔS_vib/F; 코드 `_vib_dU`/`_vib_dS`). ΔC_p 상쇄로 ∂U/∂T=ΔS(T)/F 는 T-의존 ΔS 에도 성립.
- **θ_E 출처 3경로**: (i) 실측 포논(Raman/INS) 환산, (ii) 제일원리 포논 DOS 적분, (iii) 다온도 곡률 직접 회귀[**데이터-주도 1순위**]. 위 50–80 meV 는 환산 **예시일 뿐** — 대상 호스트 실측으로 교체.
- **★식별 조건(과적합 회피)**: 분리에는 **준양자 창(kBT~ℏω)을 걸치는 실측 T 점 3개 이상** 필요. 2-온도(유한차분)는 곡률과 선형을 합으로만 보아 **축퇴**(θ_E·electronic 계수 분리 불가) — 데이터 2점뿐이면 θ_E 개방 금지.
- **경계**: vib(T-축)·config(x-축, §1.5)·electronic(∝T)은 ΔS_eff 에 독립 가산. 셋을 가르는 기준은 함수형(로그 vs Einstein 곡률 vs 선형). Phase D(다온도)에서 tier-4 와 함께 개방.

## 2. Round-trip 절차 (5-Phase, 과식별 회피 = tier 단계 개방)

- **Phase A — peak 골격**(저율 등온): tier-1(U_j 또는 ΔH/ΔS·n·Q·Cbg)만 개방. `equilibrium()` 또는 저율 `dqdv()`로 봉우리 위치·폭·면적 맞춤. 게이트: ΣQ_j∈[0.95,1.05]Q_total·U_j 순서. (= 식별 사슬 S1)
- **Phase B — 히스·비대칭**(충·방전 pair — S5 는 다율·각 T 의 gap, S2 는 전류 차단 도약 데이터 요구): tier-2(Ω·γ·Rn) 개방, tier-1 고정. 충전/방전 곡선 gap·분극 이동. (= S2+S5; χ 는 이 데이터로 식별 불가 — Phase C 로 이월. LCO 는 §1 의 Ω 지위 주의 — pair 데이터 확보 전 개방 금지)
- **Phase C — 동역학 꼬리**(rate-series): tier-3(dH_a·dVdq_qa·χ) 개방. **L_V 직접 fit 과 물리 dH_a/dVdq_qa/χ fit 동시개방 금지**(과식별) — 물리 경로 우선, L_V 직접은 초벌 우회만. (= S3) ★수치 지형 주의: k₀=k_BT/h·ΔS_a=0 전제에서 꼬리가 peak 폭 w 에 견줄 만큼(가시적) 자라는 dH_a ≈ **80 kJ/mol 급**(298 K·C/10·χ=0.5·dVdq_qa=0.30 표 초기값 기준, Ω_j 클수록 상승) — 표 초기값(40–48)은 꼬리가 무시할 만큼 작은 영역(대표 L_V~10⁻⁸ V)이라 그 사이 dH_a gradient 가 낮다. **점별 아키텍처(v1.0.15~)라 구판의 격자 문턱 점프(~23%)는 없고 꼬리가 매끈하다(L_V→0=평형 종, eq:tail-limit)** — 다만 초기값에서 꼬리 감도가 낮으니 dH_a 를 80 급에서 출발시키거나 L_V 초벌 우회로 스케일을 먼저 잡을 것(Ch1 tab:staging 하단 실현 크기 고지 참조). ★식별 주의: 등온 rate-series 에서 dVdq_qa 와 dH_a 는 L_V 의 곱으로만 진입하는 공선형 쌍이다 — dVdq_qa 는 피팅 폐쇄 대상이 아니라 S1 산출(또는 실측) OCV 의 컷점 기울기에서 유도해 **동결**하고 dH_a 만 개방할 것.
- **Phase D — 다온도·LCO 전자항**: tier-4(dS_rxn·dS_a) + LCO 전자항(g_max·x_MIT·dx) 개방. `entropy_coefficient()`·`reversible_heat()`(또는 SOC 축 실측이면 x̄ 진입점 — 아래 항)를 다온도 엔트로피 계수에 맞춤(S4 의 다온도 Arrhenius 로 ΔH_a^eff 확정도 이 단계 데이터 소관). 전자항 dict 는 T1=MIT(x_MIT=0.85 물리 anchor)로 **재정렬 완료(v1.0.14 루프 B)** — Ch1 tab:lco-staging. ★**scope 정직(다온도 LCO 전자항)**: 전자항의 T-복원 — `func_dSe_molar` 에 실측 T 전달로 Sommerfeld ∝T 스케일 복원 + eq:U1T2 의 center-T_ref 별도적분(½=a_e/2F) — 은 **현 v1.0.19 코드에 미구현**이다. 현행은 T_ref 동결 상수 근사(조성도 x_center 동결, Ch1 §17 동결 근사와 동일 — U_1(T) 선형). 다온도 LCO 데이터로 이 단계를 실제 돌리려면 T-복원은 **사용자 구현 또는 차기 버전** 몫이며, 흑연 다온도 경로(dS_rxn·θ_E·n(T))는 현 코드로 완결이다. (= S4; 고정점 1회 갱신은 초기 근사 — 수렴은 이 단계서 수치 확인, Ch1 §lco-code)
- **Phase E — 검증**(holdout): 미사용 T·C-rate 에서 예측 vs 실측. **흑연 0-diff 회귀 assert**(LCO 편입 후에도 흑연 불변).
- **★x̄ 진입점 사용 시점 (v1.0.19)**: 실측이 전위축이 아니라 **SOC(조성 x̄) 축**으로 주어질 때 — Phase D 의 엔트로피 계수 ∂U_oc/∂T(x̄) 대조, Phase E 의 SOC-격자 holdout, 가역열 q_rev(x̄) 산출 — 는 `solve_U_oc(x_bar, T)`(Ch2 eq:implicit 전하 보존 음함수의 유일근 → U_oc) → `entropy_coefficient_x(x_bar, T)`(그 근에서의 완전식 ∂U_oc/∂T) → `reversible_heat_x(x_bar, T, I)`(eq:qrev 출구) 사슬을 쓴다. dQ/dV 피팅(Phase A~C)은 기존 V_n 경로 그대로다(x̄ 진입점은 additive — 기존 경로·골든 무섭동). `entropy_coefficient`/`entropy_coefficient_x` 에 **`return_terms=True`** 를 주면 완전식/단순식/config 항이 분리된 dict(`{'complete','simple','config'}`, x̄ 판은 `'U_oc'` 포함)로 반환된다(기본 False 의 반환·수치 불변) — §1.5 의 두-상 폭 T-동결 진단(완전식 vs 단순식 우열)에 이 분리를 쓴다.

## 3. 역방향 식별 사슬 S0–S5 (비순환)

각 단계 출력은 다음 단계의 **동결 기지값**으로 쓰여 단계마다 미지수가 한 겹씩만 남는다. 화살표를 거슬러 자유화하면 공선형이 되살아난다. §2 의 Phase A–E 는 이 사슬의 순방향 개방 스케줄이다.

| 단계 | 데이터 | 절차 | 닫는 파라미터 |
|---|---|---|---|
| S0 | GITT 완화 transient | √t 형/지수형 각각 회귀 후 AIC 낮은 쪽 채택 | 활성화 지배 확인(수송 진단) |
| S1 | 저율 OCV·dQ/dV (각 T) | 검출 직독 + 다-peak 동시 국소 회귀 | {U_j, w_j(n_j), Q_j}, C_bg |
| S2 | 전류 차단 도약 | ΔV = σ_d·\|I\|·R_n 직독(첫 샘플 간격 내 순간 도약만) | R_n |
| S3 | 등온 다전위 꼬리 | ln L_q vs V_drive 기울기 −χsF/RT (S0 통과 전제; dVdq_qa 는 S1 OCV 컷점 기울기의 파생량 — 여기서 피팅하지 않음) | χ (+부산물 r_a — 컷점 잔여 지연 r(q_a)=ξ_eq−ξ_lag, 꼬리로 이월되는 진행 몫) |
| S4 | 다온도 꼬리 | Arrhenius: y(T) vs 1/T | ΔH_a^eff, 절편 |
| S5 | 다율 충방전 gap (각 T) | 절편·기울기 분해 + 절편 T-형 비선형 회귀 | γ_j, Ω_j |

보충 규정(선별):
- **S1 직독+회귀 필수** — 직독만으로는 봉우리 겹침이 면적·중심에 계통 오염(검출 초기값으로 다-peak 평형식 동시 최소제곱).
- 히스 전이의 S1 출력은 방향별 측정 중심 {U_j^dis, U_j^chg}(중점 U_j 와 측정 gap). 충·방 저율 **공동** 최소제곱으로, U_j^dis/U_j^chg 는 분리 자유도·w_j·Q_j 는 방향 공유 강제 — S5 선참조 없이 비순환 유지, S5 의 (γ_j,Ω_j)는 그 측정 gap 을 재현하는 정합 조건.
- S1 "준평형" 자격은 자기 모델로 점검 — 역산한 0.05C 잔류 지연과 kinetic 이동이 보고 불확도보다 작아야. 크면 GITT 휴지로 대체.
- **dVdq_qa 산출 절차(S3 진입 전 동결값)**: ① S1 이 확정한 OCV(또는 저율 준평형 곡선)에서 전이별 꼬리 **컷점 q_a** 를 찾는다 — 컷 affinity A(eq:Acut)가 정의하는 좌표로, 원천 dξ_eq/dq 가 정점의 약 5%로 떨어지는 용량점(기본 n=1 은 상한 A_cap=4.0RT 가 걸려 실효 z=4.0, 정점의 약 7%). ② 그 q_a 에서 OCV 접선 기울기 |dV/dq| 를 국소 수치 미분(잡음 억제용 국소 다항 fit 권장)으로 읽어 `dVdq_qa` 로 **동결**한다. ③ 이 값은 L_V=|dV/dq|_{q_a}·L_q (eq:LV) 로만 곡선에 진입하므로, dH_a 와 동시 개방하면 곱-공선형(§2 Phase C 식별 주의)이다.
- S5 절편의 상대 온도 기울기가 불확도보다 작으면 **깊은 2상측 퇴화**로 판정, lumped gap Δ_j≡γ_j·ΔU_j^hys 한 개(온도 상수)로 강등.
- 코드 검증 = round-trip: 알려진 θ* 로 합성 곡선 + 측정 수준 잡음 → 전 파이프라인이 θ* 를 회복하는지(동결 사슬이 공선형을 끊는지, 평활 창이 w 편향을 넣지 않는지). 실행 예제 = §7 `fit_roundtrip_demo.py`.

## 4. 가정의 울타리 (유효범위 조건)

① 활성화 지배(아니면 S0 수송 진단 선행) ② 좁은 장벽 분포(꼬리가 반로그 현 아래로 휘면 분포 확장 필요 — 현 코드 미구현·후속) ③ prefactor·활동도 T-안정(Arrhenius 절편 분리의 전제) ④ 꼬리 컷 공통 고정 ⑤ 분기 중심의 ξ=½ 대칭(eq:hyssym) ⑥ γ_j 전류·온도 무관(저~중율) ⑦ 분극 선형·lumped R_n ⑧ 전이 간 독립 가산 ⑨ C_bg 를 S1 에서 동결 ⑩ 반쪽전지 환산 선행 ⑪ 전이당 상수-L 동결(위반 지문 = 꼬리 후미 가속) ⑫ V_drive=V_n lumped ⑬ 운전 중 전해질 조성 불변(저온·고율 농도 분극에서 먼저 깨짐) ⑭ 분기 전이 꼬리 파라미터(χ·ΔH_a)는 mosaic 전선을 한 완화로 뭉친 유효값 ⑮ 무부반응(쿨롱 효율≈1; 위반 지문 = 충방전 면적 불일치) ⑯ χ 전이 공통(위반 시 전이별 세분).

## 5. 잔차 진단표 (증상 → 의심 원인 → 처방)

| 증상 | 의심 원인 | 처방 |
|---|---|---|
| 꼬리가 반로그 현 아래로 처짐 | 장벽 분포 넓음(울타리 ②) | 분포 적분 확장(후속 과제) |
| 꼬리 후미가 현 위로 부풂(가속) | 상수-L 가정 위반(울타리 ⑪) | sub-window 국소 L_V 처리 확인 |
| gap–\|I\| 기울기가 점점 줆(로그형) | η_ct∝ln\|I\| 우세(울타리 ⑦ 분극 선형 위반) | 저율 한정·R_ct 분리 |
| gap–\|I\| 기울기가 점점 커짐 | 확산 한계·γ_j(\|I\|)(울타리 ⑥ 위반) | 율 하향·수송 진단(S0 재진단) |
| Arrhenius 비선형 | 공율속·경쟁 꼬리원 | S0 재진단 |
| 충방전 면적 불일치 | 용량 미평형·부반응(울타리 ⑮) 또는 (1−r_a) 회계 누락 | 전처리·cycle 안정화·회계 점검 |
| 절편 T-의존 < 불확도 | 깊은 2상측 퇴화 | lumped Δ_j 강등(S5 규정) |
| 전이별 gap 기울기 상이 | lumped R_n 위배(울타리 ⑦) | R_{n,j} 세분 |
| S0 완화가 혼합형(두 모형 다 잔차) | 다공 전극의 확산·반응 혼재 | 판정 보류·EIS 병행 |
| LCO 봉우리는 맞는데 rate/히스 거동이 반대 | **방향 규약 오적용(§0)** — 셀 라벨로 σ_d 부여 | LCO 충전 곡선 ↦ `curve(direction='charge')`(자동 σ_d=+1 환산) 또는 저수준 `dqdv(s=+1)` 재확인 — `curve(direction=+1)` 은 전극 인지 반전을 거쳐 σ_d=−1 이 되므로 금지 |

## 6. 수렴·물리제약 판정

- 잔차 ΣΔ²/N < 1e-4 (정규화 dQ/dV). **정규화 정의(게이트 확인 가능형)**: 측정 조건(곡선)별로 |dQ/dV| 의 **peak 최대값을 1 로 스케일**한 뒤, 그 스케일에서의 점별 잔차 Δ 의 제곱평균 ΣΔ²/N 을 취한다(무차원) — √(1e-4)=1e-2 이므로 이 게이트는 "peak 높이 대비 RMS 잔차 1% 미만"과 동치다.
- ΣQ_j ∈ [0.95, 1.05]·Q_total (면적보존).
- U_j 순서 보존 · 다온도 ΔS 부호 문헌 일치.
- **흑연 회귀 0-diff**: `test_regression_v1019.py`(본 폴더 동봉, `Anode_Fit_v1.0.19` import) = `golden_graphite_ref.npz`(본 폴더 동봉) 대비 **13/13 np.array_equal PASS** (피팅·LCO 편입이 흑연 경로 불변). ※코드 알고리즘의 의도적 수치 변경 시에는 ledger 기록 후 골든 재베이스라인(v1.0.15 점별 재아키텍처가 그 예 — 검증 후 재캡처).

## 7. 검증 스크립트·그래프 suite (v1.0.19 동봉)

본 폴더(`docs/v1.0.19/`)의 검증 세트는 다음과 같다(구버전 스크립트 `plot_dqdv.py`·`demo_lco_heat.py`·`sample_test_v1016.py`·`graph_suite_v1016.py`·`test_regression_graphite.py` 는 구버전 폴더 소재 — 본 폴더 미동봉, v1.0.19 판으로 대체):

- **`fit_roundtrip_demo.py` — 피팅 round-trip 실증(역방향)**: 알려진 θ* 로 합성 dQ/dV 를 생성하고(측정 수준 잡음 주입), §6 정규화 잔차를 손실함수로 tier 단계 개방(§2 스케줄)에 따라 피팅해 θ* 회복오차·수렴을 출력한다 — §3 말미 "코드 검증 = round-trip" 규정의 실행 예제(forward 자기일관성 검증과 별개의 **역방향** 실증).
- **`test_regression_v1019.py` — 흑연 회귀 골든**: `golden_graphite_ref.npz` 대비 13/13 np.array_equal(§6 게이트).
- **`graph_suite_v1019.py` — validation 그래프 suite**(`Anode_Fit_v1.0.19` import, 산출 png 는 `figs/`): 아래 V1~V9.
- **`samples/` — x̄ 진입점 산출 예시**: `fig_Uoc_x.png`(x̄→U_oc 솔버)·`fig_dUdT_x.png`(∂U_oc/∂T(x̄) 완전식/단순식)·`fig_qrev_x.png`(q_rev(x̄) 부호 교대)·`fig_dqdv_graphite/lco/temperature.png`·`fig_vib_einstein.png`(θ_E 보정 곡선)과 `continuity_scan_report.txt`(x̄ 격자에서 U_oc·∂U_oc/∂T 의 연속성·블렌드 스캔 리포트).

V1~V9 (graph_suite):
- **V1** 흑연+LCO dQ/dV 나란히 — MSMR 동형, 두 전극 한 프레임.
- **V2** round-trip 복원 parity(입력 ΔS → forward U_j(T) → 회귀 ΔŜ, y=x) — ★FD round-trip 수치 무결 가드(ΔS↔∂U/∂T 정의 정합; 잡음 데이터 통계적 식별성 증명 아님 — 통계적 식별성은 §3 round-trip 잡음 주입이 담당).
- **V3** q_rev(V) 흡·발열 교대(ΔS 부호전환 음영) — eq:qrev 부호규약.
- **V4** ∂U/∂T 완전식 vs 단순식 vs FD — 파생 A 수치검증(config 항·완전식≈FD; 전제 = w=nRT/F 서식, Ch2 파생A srcbox 조건부).
- **V5** 온도의존 peak 이동(258–318K) — U_j(T)=ΔS/F 이동.
- **V6** 전자항 골 ΔS_e(x) (x_MIT=0.50 vs 0.85 오버레이) — eq:dSegate·구판 시연(0.50) 대비 물리 anchor(0.85) 참조 오버레이.
- **V7** 다온도 T² 곡률(선형 기준선 + eq:U1T2 예상곡률) — ★현 동결근사=선형, 다온도 피팅 구현 후 유효(오도 방지 주의).
- **V8** LCO q_rev 전자전이 서명 — eq:dSegate 골의 발열 흔적.
- **V9** 면적보존 회귀(∫dQdV dV vs Q_j) — eq:eqpeak 면적=Q.
