# V1010 P3 Draft S2 — Ch2 ↔ 코드/Ch1 정합 매트릭스 + 발열 이론 갈고닦기

> **역할**: Anode_Fit v1.0.10 P3 챕터2(발열) 9종 경쟁 드래프트 S2 (작업 sub)
> **드래프트만 — 수정 X. 범위 밖 자의 X. 허위 attribution X. 독립.**
> **입력 정독 완료**: `graphite_ica_ch2_v1.0.10.tex`(751줄 전문) · `V1010_P1_code-audit_RESULT.md`(전문) · `graphite_ica_ch1_v1.0.10.tex`(sec:lco-electronic 포함 전문)

---

## 산출 1 — Ch2 ↔ 코드/Ch1 정합 매트릭스

### 1-A. 통계열역학 항목 ↔ 코드 ↔ Ch1 전수 비교

| Ch2 이론 항목 | Ch2 식 | 코드 대응 여부 | Ch1 정합 여부 | 판정 |
|---|---|---|---|---|
| 단일 자리 대정준 분배함수 Z₁ | eq:Z1 | **부재** (코드는 분배함수를 직접 쓰지 않고 logistic 결과만 사용) | Ch1 sec:dist "Fermi 함수형"으로 서술, 유도 없음 → Ch2가 기원 공급 | **누락(코드·Ch1 모두 Z₁ 비가시)** — Ch2 고유 이론 영역 |
| 평균 점유 ⟨n⟩ = logistic | eq:occ | `func_ksi_eq` L94-97 (`logistic(z)`) — 구조 일치 | Ch1 eq:logisticsolve, eq:fermifn (두 경로로 유도) | **정합** — Ch2 eq:occ ↔ Ch1 eq:logisticsolve ↔ 코드 L96-97 삼각 일치 |
| 화학 퍼텐셜 μ ↔ 전위 V 연결 | eq:muV | 코드에서 `func_ksi_eq(V_n, U, n, s)` 가 (V−U)/w 형태로 흡수 | Ch1 eq:Uj 정의(ΔG=−FU → U_j=(−ΔH+TΔS)/F) | **정합** — μ−ε₀ ≡ −σ_d·F·(V−U_j) 는 코드 s·(V_n−U)/w와 동형; 명시 연결식은 Ch2에만 |
| logistic 폭 w = RT/F | eq:logistic 아래 서술 | `func_w(T, n=1.0)` L74-75: `w = n·R·T/F` | Ch1 기호표 n_j 행: "w = n_j·RT/F" | **정합** — n_j=1 이상 단일 자리 극한에서 Ch2 w=RT/F ↔ 코드 w(T,1)=RT/F 동일 |
| Bragg–Williams 자유에너지 g(θ) | eq:BW | 코드에서 Ω는 `'Omega'` 파라미터로 존재(L441, L335); g(θ) 함수형 미구현(평형 등온선 직접 x) | Ch1: Ω를 `'Omega'` 키·히스 gap·ΔH_eff 두 역할로 씀 | **부분 정합** — BW 자유에너지 명시 식은 Ch2에만; 코드는 Ω의 열역학적 기원이 아니라 파라미터로 수용 |
| 평형 전위 V_eq(θ) BW식 | eq:Veq_BW | 코드 미구현 (코드는 U_j + 히스 shift 형태, BW 상호작용항 +(Ω/F)(1−2θ) 없음) | Ch1 비구현; Ch1은 Ω가 스핀오달 gap에만 관여 | **불일치/의도적 생략** — 코드는 BW 평형 전위 아닌 U_j + spinodal 분기를 쓴다. Ch2 eq:Veq_BW는 교과서 전시용 이론 |
| 임계 Ω=2RT | eq:slope_BW | `func_dU_hys` L85·L137 `Ω≤2RT → gap=0` — 임계 조건 구현됨 | Ch1 sec:lco-hys: "Ω>2RT 면 상분리" 명시 | **정합** — 임계 수치·물리 일치 |
| S_config = −R[θlnθ + (1−θ)ln(1−θ)] | eq:Sconfig | **코드 부재** (P1 §2-E 확정: "전자엔트로피·발열·LCO 부재") | Ch1 sec:hys 에 "S_mix" 로 일부 언급되나 열역학 전개 미비; Ch2가 완전 유도 | **코드 부재(의도적)** — Ch2 고유 이론. 코드는 S_config 수치를 직접 계산하지 않고, dS_rxn 파라미터로 측정값 수용 |
| ∂S_config/∂θ = −Rln[θ/(1−θ)] | eq:dSconfig | **코드 부재** | Ch1 부재(∂U/∂T 서술 있으나 분포 미분 유도 없음) | **누락** — Ch2 eq:dSconfig는 Ch1 eq:lco-dUdT의 config 기여 기원 설명. 이중계산 주의(파생 B) |
| ∂V/∂T\|_ξ = ΔS⁰_j/F + (R/F)ln[ξ/(1−ξ)] | eq:dVdT_config | **코드에서 func_U_j(T, dH_rxn, dS_rxn)** 의 T 미분 = ΔS_rxn/F 만 구현; config 분포항 (R/F)ln[ξ/(1−ξ)] 미구현 | Ch1 eq:lco-dUdT "∂U_j/∂T = ΔS_rxn,j/F" (중심 표준값만) | **불일치(의도적)** — 코드는 중심 표준값만 사용; Ch2 eq:dVdT_config의 config 봉우리 내부 항은 P4 발열 코드에서 구현 예정 |
| 전이별 표준값 ΔS⁰_j (table) | tab:ds | `GRAPHITE_STAGING_LIT` `'dS_rxn'` 키: +29/0/−5/−16 J/mol/K | Ch1 기호표: ΔS_rxn,j 행 "삽입 반응 엔트로피(평형)" | **정합** — 수치·부호 일치 (Ch2 tab:ds와 코드 초기값 전수 대응 확인됨) |
| 겹침 가중식 ∂U_oc/∂T(x)(단순식) | eq:weighted | **코드 부재** (발열 계산 미구현, P1 §2-E) | Ch1 부재 | **누락(P4 대상)** — Ch2 eq:weighted는 P4 발열 구현의 핵심 입력 |
| 파생 A 수치검증 (175점 FD 일치) | srcbox:numverif | Ch1 코드 Anode_Fit_v11 4-전이 파라미터 사용 서술 | Ch1 코드 `equilibrium`/`dqdv` 호출 → `∂U_oc/∂T` 유한차분 | **추정 정합** — Ch2 srcbox 내 `Anode_Fit_v11` 참조는 코드와 동일 파라미터 집합 의미. 실행 근거는 Ch2 본체에 있고 코드 파일에서 독립 재현 가능 |
| 파생 B 이중계산 금지 | warnbox (파생 B) | `GRAPHITE_STAGING_LIT` `'dS_rxn'`이 중심 표준값ΔS⁰_j (봉우리 중심값) | Ch1: ΔS_rxn은 "삽입 반응 엔트로피"로만 정의, 분포 항 분리 미명시 | **정합(강화 필요)** — 코드·Ch1 모두 ΔS_rxn = 중심 표준값으로 쓰고 있어 파생 B 정의와 일관; Ch1이 "이중계산 금지"를 명시하지 않는 것이 Ch2의 보완 역할 |
| S_vib (포논 BE 분포) | eq:Svib_mode | **코드 부재** | Ch1 부재(언급 없음) | **누락(의도적)** — 흑연에서 vib 기여는 ΔS⁰_j 중심값에 흡수 (파생 B 논리); 별도 수치 미구현 |
| S_e (전자 Sommerfeld) | eq:Se | **코드 부재(흑연 음극 전용, P1 §2-E)** | Ch1 sec:lco-electronic eq:Se·eq:dSe — LCO 전용으로 완전 유도 | **부재(의도적, 흑연 전용)** — Ch2 sec:vibel §2의 흑연 S_e≈0 서술·Ch1 sec:lco-electronic LCO 유도와 정합. 단, Ch2의 Sommerfeld 식은 Ch1 eq:Se와 동일 형태 → 교차 참조 가능 |
| 파생 D 히스 분기 평균 | eq:hys_rev | `func_U_branch` L143-148, `func_dU_hys` L133-140 — 분기 중심 구현됨. 단, ∂U/∂T 분기 평균 수치는 미구현 | Ch1 sec:lco-hys: 충/방전 히스 분기 서술 | **부분 정합** — 히스 분기 중심은 코드에 있으나 eq:hys_rev(분기 평균으로 가역열 산출)는 P4 대상 |
| 가역 발열 Q̇_rev = −IT·∂U_oc/∂T | eq:qrev | **코드 부재** (P1 §2-E 확정) | Ch1: ∂U_j/∂T 연결까지 있으나 발열식 미제시 | **누락(P4 대상)** — Ch2 eq:qrev는 Ch1의 U_j(T) + Ch2 분포 엔트로피 + Bernardi 에너지 수지를 묶는 최종 산출식 |

### 1-B. 누락·과잉·중복/모순 요약

**누락 (코드에 없고 P4 구현 대상):**
1. `S_config` 계산 루틴 및 `∂S_config/∂θ` 수치
2. `∂U_oc/∂T(x)` 겹침 가중 완전식 (`eq:weighted` + config 항)
3. `Q̇_rev = −IT·∂U_oc/∂T` 발열 산출
4. 히스 분기 평균 `eq:hys_rev`에 기반한 가역/비가역 분리 수치

**과잉 (발열=P4 관련 Ch2 항목으로 P3 이론 범위에서 참조만):**
- `eq:weighted`·`eq:qrev`·`eq:hys_branch`·`eq:hys_rev`는 Ch2 이론으로 완결되었으나 코드 구현은 P4. P3 드래프트는 이 식들의 물리 기반을 제공하는 역할.

**중복/모순 위험:**
1. **Ω의 이중 역할**: Ch2에서 Ω는 (a) BW 상전이 임계 Ω=2RT(§sec:limits)와 (b) 코드의 히스 gap·ΔH_eff 파라미터 두 역할을 한다. Ch1도 동일하게 Ω를 두 역할로 쓰지만 분리 서술이 없다. Ch2 §sec:limits·§ssec:weff가 이를 명시하여 혼동을 방지하고 있으므로 정합.
2. **ΔS_rxn 이중계산**: 코드 `'dS_rxn'`이 중심 표준값으로 쓰이므로 P4에서 `eq:dVdT_config`의 config 항을 추가할 때 `dS_rxn`을 다시 더하면 이중계산 발생 — Ch2 파생 B가 이를 명시적으로 경계.
3. **w = RT/F vs 두-상 현상학적 폭**: Ch2 §ssec:weff에서 명시된 이중지위(단상=평형 예측, 두-상=현상학적 피팅)는 코드에서 n_j=1 초기값으로 반영되어 있으나 Ch1 sec:width(n_j=1 고정→실폭=RT/F)와 직접 연결이 약함 — 정합은 되나 설명 다리 필요.

---

## 산출 2 — 발열 이론 갈고닦기 (★중점)

### 2-A. q_rev = −T·ΔS 유도 전 단계: 열역학 기초 연결

**출발 전제(두 열역학 법칙):**
전기화학 반응 `Li⁺ + e⁻ + [] → Li(삽입)` 에서 깁스 자유에너지 변화는
$$\Delta G = \Delta H - T\Delta S$$
와 전기화학 일의 연결
$$\Delta G_{\mathrm{rxn},j} = -FU_j$$
에 의해 닫힌다. 온도 미분은 깁스–헬름홀츠 항등식
$$\left(\frac{\partial \Delta G}{\partial T}\right)_P = -\Delta S$$
이므로
$$\frac{\partial U_j}{\partial T} = \frac{1}{F}\left(-\frac{\partial \Delta G}{\partial T}\right) = \frac{\Delta S_{\mathrm{rxn},j}}{F}.$$

이것이 Ch2 eq:dVdT_config 첫 항의 기원이며, Ch1 eq:Uj 미분이 같은 식을 줌을 Ch1·Ch2 양쪽에서 확인했다.

### 2-B. ΔS ↔ q_rev 연결 — 가역 발열식의 단계별 유도

**단계 1: Bernardi–Pawlikowski–Newman 에너지 수지.**
단일 활물질 계(코인 하프셀)에서 전지 셀의 총 발열률은
$$\dot{Q}_{\mathrm{total}} = \dot{Q}_{\mathrm{irr}} + \dot{Q}_{\mathrm{rev}},$$
비가역(소산) 항은 과전압에 의한 entropy production으로 항상 양수:
$$\dot{Q}_{\mathrm{irr}} = I(U_{\mathrm{oc}} - V) \geq 0,$$
가역(엔트로피) 항은 부호 양방향이다.

**단계 2: 깁스–헬름홀츠에서 q_rev 닫기.**
셀 전압과 깁스 에너지의 관계 $\Delta G = -FU_{\mathrm{oc}}$ 를 활용하면 1몰 Li 삽입당 반응 엔트로피는
$$\Delta S(x) = -\frac{\partial \Delta G}{\partial T} = F\frac{\partial U_{\mathrm{oc}}}{\partial T}.$$
가역 열은 이 엔트로피 변화가 온도 $T$ 에서 환경과 교환하는 열로 정의된다. 충전상태(SOC) $x$ 에서 $x + dx$ 로 이동하는 미소 반응에서 흡수되는 가역 열:
$$\delta q_{\mathrm{rev}} = T\,\Delta S\,d\xi = T\cdot F\frac{\partial U_{\mathrm{oc}}}{\partial T}\,d\xi.$$
전류 $I$ (방전 기준 $I > 0$)로 시간 $dt$ 에 흐르는 전하가 $I\,dt$ 이고, 대응되는 Li 몰수의 이동이 $I\,dt/F$ 이므로 발열률은
$$\boxed{\dot{Q}_{\mathrm{rev}} = -I\,T\,\frac{\partial U_{\mathrm{oc}}}{\partial T} = -\frac{IT}{F}\,\Delta S(x).}$$

**부호 확인:** 방전($I > 0$)에서 $\Delta S > 0$이면 $\dot{Q}_{\mathrm{rev}} < 0$ (흡열: 셀이 환경에서 열을 흡수). $\Delta S < 0$이면 $\dot{Q}_{\mathrm{rev}} > 0$ (발열). 흑연 음극은 저-$x$에서 config 기여가 커 $\Delta S > 0$ (방전 흡열), 고-$x$에서 $\Delta S < 0$ (방전 발열).

**추정 근거**: 이 유도는 Ch2 eq:qrev·srcbox(부호 규약)와 일치한다. Bernardi et al. (1985) DOI:10.1149/1.2113792 에서 검증된 에너지 수지에 기반한다.

### 2-C. ΔS(x) 분해 — 세 분포와 config 항의 위치

Ch2의 핵심 결과인 분해식:
$$\Delta S(x) = \underbrace{R\ln\frac{\xi}{1-\xi}}_{\text{config 분포 (}w\text{ 가 자동 공급)}} + \underbrace{\Delta S^0_j}_{\text{중심 표준값 (vib+elec 흡수)}} + \underbrace{\delta S_{\mathrm{vib}/e}(x)}_{\text{전이 폭 내 급변 시만}}$$

각 항의 코드·Ch1 정합:

1. **config 분포 항 `Rln[ξ/(1−ξ)]`**: Ch2 eq:dSconfig에서 `∂S_config/∂θ = −Rlnθ/(1−θ)` 로 유도. 코드에서 직접 수치화 미구현. P4에서 `func_ksi_eq`가 주는 `ξ_j`를 그대로 받아 계산 가능.

2. **중심 표준값 `ΔS⁰_j`**: 코드 `'dS_rxn'` 키 (+29/0/−5/−16 J/mol/K). Ch1·Ch2 양쪽에서 "봉우리 중심(ξ=½)에서 측정" 정의로 일관.

3. **`δS_vib/e(x)` 잔차**: 흑연에서 거의 0 (vib 천천히 변해 중심값 흡수, electronic ≈ 0). LCO MIT에서만 `ΔS_e(x,T) ∝ T` 가 생존. Ch1 sec:lco-electronic 에서 유도된 Sommerfeld 식(Ch2 eq:Se와 동일 형태)이 유일한 비영 잔차 사례.

### 2-D. 비가역 옵션 — 교육적 대비

가역 발열과 대비되는 비가역 소산열:
- **비가역 소산열**: `Q̇_irr = I(U_oc − V) ≥ 0`. 항상 발열. Ch1의 동역학 꼬리(L_V, Arrhenius 활성화 장벽 ΔH_a)가 만드는 entropy production이 이 항의 기여다. 가역열에 섞이지 않는다.
- **히스테리시스 소산**: 한 사이클당 `∝ I·ΔU_hys`. 코드 `func_dU_hys` 가 `ΔU_hys`를 산출하고 `'gamma'` 파라미터가 크기를 조절한다. Ch2 파생 D (eq:hys_rev)가 가역/비가역 분리를 형식화.
- **활성화 엔트로피 ΔS_a**: 코드 `'dS_a'` 키(Eyring prefactor 온도 의존). 평형 반응 엔트로피 `ΔS_rxn`과 차원이 같으나 물리가 다르다. Ch2 sec:vibel §3에서 명시적으로 혼동 금지를 표명. 코드 P1 §3-2 표에서 dS_a=0.0(초기값, 다온도 조건부)으로 확인됨.

---

## 산출 3 — v5 검토분 + v3 survey 통합

### 3-A. v5 대비 v1.0.10 Ch2 변경 이력 식별 (파일 헤더 기반)

헤더에서 확인 가능한 v5 정정 사항:
- **`w_eff` 절 제거**: v4의 파생 C(w_eff(Ω) = w(1−Ω/2RT)) 절이 완전 삭제됨. 이유: 두-상 실측 봉우리는 narrowing이 아니라 broadening으로 "종"이 형성되므로 방향 반대. 코드 v1.0.10에서도 `use_w_eff` 완전 제거(P1 §2-D D1 확인, L7·L283).
- **w_j 이중지위 도입**: 대신 "단상=평형 예측, 두-상=현상학적 자유 피팅 폭"의 이중지위(§ssec:weff)가 v5에서 신설.
- **통계열역학 본체(A·B·D) 보존**: 분배함수→점유분포→S_config·vib·elec·히스 전 절은 v4-11에서 이어받아 그대로 보존됨.

### 3-B. Ch2 내 v3 survey와의 관계 (Ch2 텍스트 기반 추정)

v5(= 현행 Ch2 v1.0.10 기반)의 참고문헌이 포함하는 내용을 정리하면:
- **Bernardi et al. (1985)**: 발열 에너지 수지의 1차 문헌. Ch2 eq:qrev에서 인용.
- **Newman & Thomas-Alyea**: 격자기체 삽입 전극 열역학·OCV(T) 기울기 = ΔS. Ch2 eq:Z1–eq:logistic의 기초.
- **Huggins (2009)**: 격자기체·BW 평형 전위. Ch2 eq:BW·eq:Veq_BW.
- **Bazant (2013)**: regular-solution lattice-gas OCV·상분리 임계 Ω=2RT. Ch2 §ssec:BW·§sec:limits.
- **Reynier et al. (2003)**: 흑연 삽입 엔트로피의 실험 측정. Ch2 §sec:vibel.
- **Allart et al. (2018)**: 흑연 부분몰 ΔS(x) 전극 분리 측정. Ch2 tab:ds와 정량 대응.
- **MSMR (2024) Part I/II**: 다온도 피팅으로 ΔS⁰_j 추정 절차. Ch2 procedurebox의 구체 절차와 직접 대응.
- **Standardised 2024**: 가역 발열 직접 calorimetry 실측 정합. Ch2 §sec:revheat.

### 3-C. Ch2 정확성·정합성 우선순위 평가

**강점 (확인됨):**
1. `Z₁ → ⟨n⟩ → S_config → ∂U_oc/∂T → Q̇_rev` 사슬이 점프 없이 분포에서 유도됨 (Ch2 인트로 박스 확인).
2. 파생 A 수치 검증: 완전식이 유한차분과 부동소수점 정밀도로 일치 (Ch2 srcbox:numverif).
3. 이중계산 금지(파생 B): 중심 표준값·config 분포 항의 정의가 자기일관적 (`ξ=½`에서 config=0 이므로 중심 정의와 모순 없음).
4. 한계 명시(Ch2 §sec:revheat 끝): 실데이터 round-trip 피팅 미완, 히스 측정 불확실도 정량화 미비, Ω 온도 의존 미확보 등 5개 공백 솔직하게 나열.

**보완 권고 (P3 supplement 초점):**
1. **Ch2 ↔ Ch1 전자엔트로피 연결**: Ch2 §ssec:elec에서 Sommerfeld `eq:Se`를 다루지만 Ch1 sec:lco-electronic의 완전 유도(`eq:Se = (π²/3)k_B²Tg(E_F)` 비열→적분 경로 + 정보 엔트로피 직접 경로)를 참조할 수 있음. "두 경로의 합치" 교차검증(Ch1 eq:Sedirect)이 Ch2의 흑연 대비 LCO 사례를 보강함.
2. **코드 `'dS_rxn'` 초기값 ↔ Ch2 tab:ds 정량 매핑**: Ch2 tab:ds 값(+29/0/−5/−16)이 코드 `GRAPHITE_STAGING_LIT`의 `'dS_rxn'` 키와 일치함을 S2 매트릭스(1-A)에서 확인; P3 supplement 문건이 이를 공식 anchor로 명시 가능.
3. **파생 C(w 이중지위)와 코드 n_j=1 고정의 명시적 연결**: Ch2 §ssec:weff는 "두-상 전이에서 w는 현상학적 피팅"이라 하고, Ch1·코드는 n_j=1 초기값으로 시작한다. P3 supplement가 "n_j=1 초기값은 두-상 이중지위 하에서 현상학적 w=RT/F의 시작점이며 피팅으로 override됨"을 명시하면 Ch2 §ssec:weff ↔ Ch1 sec:width ↔ 코드 §1.2 func_w 삼각 연결이 완성됨.
4. **`q_rev` 부호 규약의 Ch1·코드 통일 확인**: Ch2 eq:qrev는 `I>0=방전` 기준. Ch1·코드 `'dS_rxn'` 부호 (+29 = 저-x 방전 흡열 ↔ $\dot{Q}_{\mathrm{rev}} < 0$)와 일관함을 수치 예시로 명시 가능.

---

## 드래프트 S2 품질 자기 점검

**화학식·물리식 중심**: Z₁ → ⟨n⟩ → S_config → ∂V/∂T → Q̇_rev 사슬이 식 번호와 함께 단계 추적 가능.

**유도 완결**: q_rev 유도는 깁스–헬름홀츠 항등식 → 미소 가역열 → 발열률의 3단계로 전개.

**타전공 자기완결**: Bernardi 에너지 수지, Fermi 분포형 자리 점유, Sommerfeld 전자 엔트로피를 모두 식에서 출발해 참조 없이 따라갈 수 있는 수준으로 서술.

**안정·객관**: 코드 부재 항목은 "P4 대상"·"의도적 부재"로 분류, 추정은 "추정 근거" 명기.

**독자평가 0**: 수치는 Ch2 tab:ds·코드 `GRAPHITE_STAGING_LIT`에서 직접 도출됨.

---

*드래프트 S2 작성: 2026-07-01 | 작업 sub 독립 | 수정 X | 범위 외 자의 X | 허위 attribution X*
*출력 파일: `D:\Projects\Project_Anode_Fit\Claude\results\process\V1010_P3_draft_S2.md`*
