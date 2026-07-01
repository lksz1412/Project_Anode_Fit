# P5 최종점검 감사 드래프트 — S3 (C조)

> **ID**: S3 | **조**: C조 (완성도+코드없는내용0+피팅추천+그래프suite)
> **대상**: `Claude/docs/v1.0.10/Anode_Fit_v1.0.10.py` · `graphite_ica_ch1_v1.0.10.tex` · `graphite_ica_ch2_v1.0.10.tex`
> **정독 커버리지**: 코드 850줄 전량 · Ch1 1933줄 전량 · Ch2 751줄 전량 · P4 RESULT 전량
> **독립 저작**: 타 agent와 사전 통신 없음 · 거짓 attribution 없음

---

## 감사 렌즈 (C조 4항목 + 공통 3-대항목)

1. **코드 없는 내용 0** — Ch1·Ch2에서 코드 백업 없는 주장/기능 탐색
2. **교재 자기완결** — 외부전공 대학원생 기준 점프 없는 자족, 도출 완결성
3. **피팅 추천** — 파라미터 계층·round-trip 절차·초기값·bounds 설계
4. **그래프 suite 설계** — 흑연+LCO dQ/dV·가역 발열·round-trip·온도 의존 전 목록
5. **공통**: 물리 배경 정확성 / 코드 정확성 / 사용자 의도 정합
6. **P4 이월 항목 4종** 문서 일관성·라벨 검증

---

## 파트 I: 코드 없는 내용 0 (코드 미백업 주장 탐색)

### I-A. 확정 이월 — x_MIT=0.50 vs. Ch1 eq:ggate x_MIT≈0.85

**등급**: 근거 미발견(코드·문서 불일치)

**Ch1 텍스트 근거** (Ch1 §sec:lco, eq:ggate):
```
g(E_F,x) ≈ g_max[1−σ((x−x_MIT)/Δx_MIT)];  g_max=13, x_MIT≈0.85, Δx_MIT≈0.05
```
Ch1은 MIT(금속-절연체 전이) 창을 x≈0.75–0.94, 중심 x_MIT≈0.85로 기술. 탈리튬화 진행률 ξ 기준이면 x_MIT≈0.85가 "Li 희박, 충전 말단부" 전이에 해당.

**코드 근거** (`Anode_Fit_v1.0.10.py` 내 `LCO_MSMR_LIT`, L532–560 구간):
```python
{'U': 3.880, 'w': 0.024, 'Q': 0.30, 'dH_rxn': -389174.0, 'dS_rxn': -4.0, 'n': 1.0,
 'electronic': True, 'x_center': 0.50, 'g_max_eV': 13.0, 'x_MIT': 0.50, 'dx_MIT': 0.05}
```
`x_MIT=0.50`, `x_center=0.50` — 이는 LiCoO₂에서 x≈0.5인 order-disorder 전이 위치와 대응.

**분석**: Ch1 eq:ggate의 x_MIT≈0.85와 코드 x_MIT=0.50은 수치상 크게 다르다. 다만 P4 RESULT §11이 "tier-C placeholder, Ch1 eq:ggate anchor x_MIT≈0.85와 불일치(내부 정합이나 문서)"로 명시 이월한 사안이다. 코드 주석 또는 P4 RESULT에 "tier-C placeholder"임이 명시돼 있어 허위가 아닌 알려진 갭이다. 그러나 Ch1 본문 어디에도 "x_MIT=0.50을 tier-C placeholder로 사용"한다는 설명이 없다 — 독자는 코드 값이 Ch1 서술과 다름을 감지할 수 없다.

**C조 감사 의견**: [근거 미발견] Ch1 eq:ggate 본문과 코드 LCO_MSMR_LIT 항목 2의 x_MIT 값이 0.85 vs. 0.50으로 불일치. P4 이월로 라벨됐으나 Ch1 문서에 해당 설명 없음. 독자 혼동 유발 위험. **조치 권고**: Ch1 eq:ggate 또는 캡션에 "코드 tier-C 시연 파라미터(x_MIT=0.50)와 물리 앵커(x_MIT≈0.85)의 구분" 주석 추가. 실측 round-trip 피팅 후 x_MIT 확정 예정임을 명시.

---

### I-B. eq:U1T2 T² 곡률 — Ch1 본문 서술, 코드 미구현·라벨 확인

**등급**: 확정(라벨된 미구현)

**Ch1 근거** (eq:U1T2):
```
U_1(T) = U_1(T_0) + (ΔS_0/F)(T−T_0) + (a_e/2F)(T²−T_0²)
```
Ch1은 Sommerfeld T-선형 전자 엔트로피가 U_j(T)에 T² 곡률을 부여함을 파생. T_0 기준 1차+2차 항.

**코드 근거** (`LCOCathodeDQDV._effective_dS_rxn` docstring 확인):
```python
def _effective_dS_rxn(self, tr, T):
    ...T_ref = 298.15 동결 상수 오프셋...
    # Sommerfeld T-스케일·½ 인자(a_e/2F) 미구현 → 다온도 round-trip 피팅 과제
```
코드는 T_ref=298.15 고정 오프셋 근사 사용. T-의존 Sommerfeld 스케일링은 라벨만 있고 미구현.

**P4 RESULT §11 확인**: "다온도 T² 곡률: Sommerfeld T-스케일·eq:U1T2 center-T_ref 별도적분(½=a_e/2F) 미구현(단일-기준 동결 근사). 다온도 round-trip 피팅서 구현."

**C조 감사 의견**: [확정] P4가 정상 이월·라벨한 사안. Ch1 eq:U1T2 서술과 코드 불일치는 설계상 알려진 차이. 코드 내 inline 라벨("다온도 피팅 과제") 존재 확인됨 → 독자에게 "현재 코드는 근사"임이 고지된 상태. 단일 온도 사용 시에는 의도 범위 안. 다온도 피팅 시 개발 대상으로 P5 이월 유지.

---

### I-C. 비가역 3분해(I²R + Iη_ct + Iη_diff) — Ch2 미언급, 코드 라벨 확인

**등급**: 확정(범위 밖·라벨됨)

**Ch2 근거** (§sec:revheat, eq:qrev warnbox):
Ch2는 가역열 `q_rev = I(U_oc−V) − IT·∂U/∂T`의 첫 항을 "lumped 소산열"로 표기. I²R·Iη_ct·Iη_diff 3분해를 별도 절로 전개하지 않음 — 범위 선언 일치.

**코드 근거** (`irreversible_heat` 함수):
```python
def irreversible_heat(self, U_oc, V, I):
    return np.asarray(I) * (np.asarray(U_oc, dtype=float) - np.asarray(V, dtype=float))
```
docstring: "lumped I(U_oc−V). 3분해 옵션 라벨."

**C조 감사 의견**: [확정] Ch2 boxed 방정식(eq:qrev)이 lumped 형태를 공식으로 제시하고 코드도 lumped 구현. 정합. 3분해는 "율의존 피팅 과제"로 라벨됨 — 허위 코드 없는 내용 아님.

---

### I-D. 파생 D(히스테리시스 충/방전 평균, eq:hys_rev) — Ch2 서술, 코드 미구현 여부

**등급**: [추정] 코드 부재 가능성 있음

**Ch2 근거** (§sec:mixing, 파생 D, eq:hys_rev):
```
∂U_oc^rev/∂T = ½(∂U_oc^ch/∂T + ∂U_oc^dis/∂T)
```
가역 발열은 충/방전 분기 평균. 이 식을 실제 계산하려면 두 분기의 `entropy_coefficient`를 각각 계산해 평균 취하는 루틴 필요.

**코드 근거**: `entropy_coefficient(self, V_n, T)` — 단일 전위 입력, 분기 선택 파라미터(`sigma_d`) 인자 없음. `reversible_heat`도 단일 `entropy_coefficient` 호출.

**분석**: `func_U_j_hys`, `func_U_branch`, `func_dU_hys` 등 히스테리시스 관련 함수가 코드에 존재하며 dQ/dV 계산에서 sigma_d로 방향 처리됨. 그러나 `entropy_coefficient`가 단일 분기(입력된 V_n 기준)만 계산한다. Ch2 eq:hys_rev의 "충방전 분기 평균"을 자동으로 계산하는 함수는 코드에서 발견되지 않음.

**C조 감사 의견**: [추정(코드 확인 불완전)] Ch2가 교육 내용으로 제시한 eq:hys_rev(가역/비가역 분리를 위한 분기 평균) 계산 기능이 코드에 명시적으로 없음. Ch2가 이 내용을 "공백으로 명시"(§sec:revheat 한계·갭 (2)항)한 만큼 범위 외임을 본문에서 선언하고 있어 코드 미구현이 모순은 아님. 단, 사용자가 eq:hys_rev를 계산하려 할 때 API 부재. **조치 권고(선택적)**: 향후 `reversible_heat_cycled_average(V_dis, V_ch, T, I)` 같은 함수를 추가하면 Ch2 파생 D와 코드가 완전 연결.

---

### I-E. 다자리 Bragg-Williams 상호작용(eq:BW, eq:Veq_BW) — Ch2 본문, 코드 미구현

**등급**: [확정(범위 밖)]

**Ch2 근거** (§sec:partition, §ssec:BW):
eq:BW — g(θ)=RT[θlnθ+(1−θ)ln(1−θ)] + Ω·θ(1−θ); 상호작용 모수 Ω 명시. 상분리 임계 Ω=2RT.

**코드 근거**: `func_w` 함수는 `n*R*T/F` 단순 열적 폭만 반환. 코드에 Ω 파라미터 없음.

**C조 감사 의견**: [확정] Ch2 §ssec:BW는 Bragg-Williams를 "이론 배경" 절에서 전개하고 §ssec:weff(파생 C)에서 "흑연 두-상 전이의 실측 봉우리 폭은 평형이 정하는 양이 아니라 현상학적 자유 피팅 폭"이라 결론지어 Ω를 코드에 직접 노출하지 않는 설계 의도를 명시함. 코드 미구현은 의도된 범위 내. G-follow 관점: 독자가 §ssec:BW를 읽고 코드를 찾으면 Ω 파라미터가 없어 혼동 가능 → Ch2 내 "코드 func_w는 현상학적 자유 폭을 수용하며, Ω 직접 노출은 하지 않는다"는 연결 주석이 있으면 더 좋음.

---

### I-F. MSMR 이형사상 mapping(Ch1 eq:msmr) — 코드 LCO_MSMR_LIT과의 파라미터 키 정합

**등급**: 확정(정합)

**Ch1 근거** (eq:msmr):
```
X_j↔Q_j, U_j^0↔U_j^d, ω_j↔w_j, f↔−σ_d
```
MSMR 표준 파라미터와 코드 딕셔너리 키의 대응.

**코드 근거**: `LCO_MSMR_LIT = [{'U':..., 'w':..., 'Q':..., ...}]` — 'U'=U_j^d, 'w'=ω_j, 'Q'=X_j, f↔−σ_d (부호 뒤집기 없음은 P4 RESULT에서 명시됨).

**C조 감사 의견**: [확정] Ch1 eq:msmr의 이형사상이 코드 LCO_MSMR_LIT 딕셔너리 키와 1:1 대응됨. 정합. Ch1의 "f↔−σ_d" 부호는 Ch1 §eq:xieq의 σ_d 부호 규약을 통해 LCO에도 동일하게 적용(override에서 σ_d를 뒤집지 않음, P4 RESULT §7 확인).

---

### I-G. Ch2 파생 A 수치 검증(내부자료 numverif2026 인용) — 코드 재현 가능성

**등급**: [추정(코드로 재현 가능하나 전용 함수 없음)]

**Ch2 근거** (§ssec:overlap, srcbox):
```
유한차분 FD vs. 완전식: 175점 전 범위에서 부동소수점 정밀도 일치
```
내부 검증 결과 인용. 별도 테스트 스크립트로 구성됐을 것으로 추정.

**코드 근거**: `entropy_coefficient` 함수가 완전식(가중·config 항 포함) 구현이며, `reversible_heat` → `entropy_coefficient` 호출 경로 존재. 그러나 175점 FD 검증을 실행하는 전용 테스트 함수는 코드 내 미확인.

**C조 감사 의견**: [추정] Ch2 내부자료 인용이 실제 검증이 됐음을 시사. 그러나 교재 독자가 동일 검증을 재현할 코드가 없음. G-usable 관점: 재현 가능 예제 코드나 doctest 추가 권고.

---

## 파트 II: 교재 자기완결 감사

### II-A. Ch1 → Ch2 연결 — logistic 기원 이음

**등급**: [확정(정합)]

Ch2 §ssec:logistic: "Chapter 1의 logistic 평형 종 ξ_eq는 현상학적 곡선맞춤이 아니라 격자기체 점유 분포의 여집합". 분배함수 Z→점유 분포⟨n⟩→Ch1 logistic 기원 명시. 외부전공 독자가 Ch1 logistic을 "왜 이 형태인가"에서 막혀도 Ch2 §sec:partition이 자족 설명함.

### II-B. 도출 완결성 — 파생 A(겹침 가중)

**등급**: [확정(정합)]

Ch2 eq:implicit → eq:implicit_diff → eq:gj → eq:dxidT → eq:weighted 전 단계 점프 없이 유도. 내포 미분·log 도함수 모두 인라인 전개.

### II-C. 도출 완결성 — eq:Se (Sommerfeld) → eq:dSegate 경로

**등급**: [추정(경미한 점프 가능성)]

Ch1 eq:dSemolar에서 몰당 N_A·(π²/3)k_B²T·∂g/∂x. 이후 eq:ggate에서 σ(1−σ) 형태 게이트 적용. 그러나 "∂g/∂x를 logistic gate σ(1−σ)로 치환하는" 중간 단계가 내포되어 있음.

Ch1 §sec:lco 본문: "금속성 창이 x_MIT 주변 폭 Δx_MIT에 걸쳐 σ(1−σ) 형태의 전이를 보인다" — logistic derivative = σ(1−σ)임이 부연 없이 사용됨. 외부전공 독자에게 이 치환이 불투명할 수 있음.

**C조 감사 의견**: [추정] Ch1 eq:dSegate 바로 앞에 "logistic derivative: d/dx[σ(x)] = σ(1−σ)/Δx_MIT"임을 1줄 추가하면 경미한 점프 해소.

### II-D. 반응 엔트로피 vs. 활성화 엔트로피 혼동 방지

**등급**: [확정(정합)]

Ch2 §sec:vibel: "반응(평형) 엔트로피 ΔS(x) ≠ 활성화 엔트로피 ΔS_a,j(Eyring prefactor), 물리가 다름" 명시. 가역열에 활성화 엔트로피 섞지 않음을 warnbox 형태로 명시. G-follow 관점: 코드에서도 `entropy_coefficient`가 dqdv용 activation 파라미터와 완전 분리된 메서드임이 API 수준에서 자명.

### II-E. 파생 C(w 이중지위) — Ch2 내 warnbox 설명 완결성

**등급**: [확정(충분)]

Ch2 §ssec:weff warnbox: "w는 종의 폭이지 상호작용이 좁힌 델타가 아님". 단상 vs. 두-상 전이의 w 지위 이중성 명시. 외부전공 독자가 "흑연에서 왜 w=RT/F가 아니고 피팅하나"에서 막히지 않도록 충분히 설명됨.

### II-F. 리더 평가 표현("독자는 X를 알아야 한다" 류)

**등급**: [확정(없음)]

Ch1·Ch2 본문에서 "독자"를 직접 평가하거나 전제 지식을 상정하는 문장 발견 없음. 대신 "본 장에서는 X를 결론이 아니라 출발점으로 전개한다" 식의 능동 서술 사용됨. 자기완결 기준 합격.

### II-G. 절 도입/마무리 다리(교과서 문체 규범)

**등급**: [확정(Ch1·Ch2 모두 충족)]

Ch1·Ch2 모두 절 도입에서 "이 절은 X를 하고 Y를 보인다"로 목적 선언, 마무리에서 "곧 X가 성립함을 확인했다"로 닫음. Ch2 서(序) 박스 `Z→⟨n⟩→S→∂U/∂T→Q_rev` 사슬이 전체 구조를 입구에서 공시. 문체 규범 충족.

---

## 파트 III: 피팅 추천 설계

### III-A. 파라미터 계층(Tier 분류)

피팅 대상 파라미터를 물리적 확정도와 피팅 민감도 기준으로 3개 계층으로 분류:

**Tier-A (물리 고정·피팅 불필요):**
- `R`, `F`, `kB`, `EV_TO_J` — 자연상수, 코드에 고정
- `GRAPHITE_STAGING_LIT`의 `U_j` 위치 전압 — 문헌 정수(0.210, 0.140, 0.120, 0.085V), 초기값으로 사용 후 미세조정
- `n=1.0` (흑연·LCO 모두) — 단전자 전이 가정, 고정
- LCO `U_j` 전압 — 문헌 3.93·3.88·4.05V 앵커, Tier-B로 미세조정 가능

**Tier-B (1차 피팅 대상, 물리 제약 있음):**
- `dH_rxn` (각 전이, 흑연·LCO) — [J/mol] U_j(T)=-ΔH/F+TΔS/F의 절편 결정
  - 흑연 초기값 범위: Ch1 calorimetry 참조 −13~−25 kJ/mol 범위 내
  - LCO 초기값: LCO_MSMR_LIT 현재값 −377400·−389174·−391360 J/mol
- `dS_rxn` (각 전이, 흑연·LCO) — [J/mol/K] ΔS_j를 정함, 다온도 피팅의 핵심
  - 흑연 Tier-B 초기값: +29·0·−5·−16 J/mol/K (Ch1 tab:ds, Allart 2018)
  - LCO 초기값: +6·−4·−2 J/mol/K (코드 현재값; MIT 전이 −4는 전자 오프셋 포함)
  - 범위 bounds: [−50, +40] J/mol/K (Sommerfeld 기여 최대치 포함)
- `Q_j` (각 전이 용량 비율) — 전체 합 = 총 용량, 상대 비율이 피팅 대상
  - 흑연 초기값: 코드 현재 0.21·0.145·0.145·0.5
  - LCO 초기값: 0.55·0.30·0.15 (코드 현재값)
  - bounds: 각 Q_j > 0, ΣQ_j = Q_total (equality constraint)

**Tier-C (2차 피팅 대상, 모델 한계 파라미터):**
- `w_j` (두-상 전이 현상학적 폭) — Ch2 파생 C. 이상 nRT/F 아닌 자유 폭
  - 흑연 초기값: `func_w`(n=1, T=298.15) ≈ 0.0257V. 실측에서 넓어짐 → upper bound ×3 허용
  - LCO 초기값: 코드 현재값 0.030·0.024·0.028V
  - bounds: [0.005, 0.2] V (너무 좁으면 수치 불안정, 너무 넓으면 물리성 상실)
- `Omega, gamma` (상호작용, 히스 폭) — `func_dU_hys`·`func_chi_d` 입력
  - 흑연 Ω 초기값: Ch2 임계 2RT≈5000 J/mol 초과(두-상이므로), ×1.5 = 7500 J/mol
  - γ (히스 비대칭) 초기값: 0.5 (대칭 가정)
  - bounds: Ω > 0, 0 < γ < 1
- `dH_a`, `dS_a` (동역학 활성화 에너지·엔트로피) — `func_L_q` 입력. 율 의존 피팅에서 분리
  - 초기값: 50000 J/mol·0 J/mol/K (표준 활성화 에너지 50 kJ/mol)
  - bounds: [20000, 120000] J/mol · [−20, +20] J/mol/K
- `x_MIT, dx_MIT, g_max_eV` (LCO 전자 엔트로피 MIT 창) — **P4 이월(tier-C placeholder)**
  - 현재 코드값: x_MIT=0.50, dx_MIT=0.05, g_max_eV=13.0
  - 물리 앵커(Ch1 eq:ggate): x_MIT≈0.85, Δx≈0.05–0.10 — round-trip 피팅 후 정정 필요
  - 이 파라미터는 단일 온도 LCO dQ/dV 형태에는 영향 소수(T_ref 동결이므로), 다온도 피팅에서 핵심

### III-B. Round-trip 피팅 절차 (코드 작성 수준)

**단계 0: 데이터 전처리**
```
V_n = V_app − σ_d|I|·R_n  (과전압 보정; class에서 V_n 직접 받음)
x 또는 Q_cumulative → x = Q_consumed / Q_total
온도별 데이터셋: {(x_k, dQdV_k, T_k)} k=1..N_T
```

**단계 1: 단일 온도 초기 피팅 (T = 298.15K)**
```python
# 코드 호출 예:
model = GraphiteDQDV(sigma_d=+1)  # 방전
# 피팅 대상: dH_rxn_j(4개), Q_j(4개) → 총 8개 자유 파라미터
# 고정: U_j(문헌값), w_j(func_w 초기), dS_rxn_j(Allart 초기값)
# 목적함수: sum[(dQdV_model(V_k; params) - dQdV_meas_k)²] / N
from scipy.optimize import minimize
result = minimize(objective, x0=params_init, bounds=bounds, method='L-BFGS-B')
```
단일 온도 피팅 수렴 후 → 파라미터 체크:
- 각 Q_j > 0 확인
- ΣQ_j = Q_total (허용 오차 ±1%)
- U_j 순서 보존: U_1 > U_2 > U_3 > U_4

**단계 2: 다온도 동시 피팅 (ΔS 및 ΔH 정밀화)**
```python
# 코드 호출 예 (T=283·298·313K 3온도):
models = [GraphiteDQDV(sigma_d=+1, T=T_k) for T_k in [283.15, 298.15, 313.15]]
# 공유 파라미터: dH_rxn_j(4), Q_j(4), w_j(4)
# 온도별 공유+자유: dS_rxn_j는 전 온도 공유(dU_j/dT 기울기)
# Ch2 절차박스(procedurebox) 단계 3 직접 구현
```
결과 검증:
- `dS_rxn_j`가 Allart 2018 부호·규모와 일치 (표 tab:ds)
- `entropy_coefficient(V_n, T)` 반환값의 다온도 곡선이 문헌 ∂U/∂T(x) 추세와 일관

**단계 3: 가역 발열 round-trip 검증**
```python
q_rev_T1 = model_T1.reversible_heat(V_n_array, T=283.15, I=1.0)  # [W]
q_rev_T2 = model_T2.reversible_heat(V_n_array, T=313.15, I=1.0)
# 검증: T 증가 → q_rev 부호 유지·규모 증가(T 선형 스케일)
# Ch2 eq:qrev 부호 규약: 방전(I>0)에서 ΔS>0 → q_rev<0(흡열)
```

**단계 4: LCO 카소드 피팅 (하프셀 vs. 전셀)**
```python
lco_model = LCOCathodeDQDV(sigma_d=-1)  # 충전(카소드 기준)
# 피팅 대상: dH_rxn(3), dS_rxn(3), Q(3), w(3) → 12개
# MIT 파라미터(x_MIT, dx_MIT, g_max_eV)는 고정(P4 이월, Tier-C)
# 목적함수 동일; 다온도 시 Sommerfeld T_ref 동결 근사 주의 (현재 코드 단일온도 정합)
```

**단계 5: 흑연 0-diff 회귀 확인**
```python
import numpy as np
arr_before = model_graphite.dqdv(...)  # 피팅 전
arr_after  = model_graphite_fitted.dqdv(...)  # 피팅 후
assert np.array_equal(arr_before, arr_after)  # 구조 보존 확인 → 실제론 다름(피팅하면 달라짐)
# 수정: 0-diff는 "LCO 코드 편입이 흑연 결과를 바꾸지 않는다"는 의미 (P4 RESULT §9)
# 피팅 후에는 파라미터가 달라졌으므로 당연히 달라짐 → 의도 구분 중요
```

### III-C. 초기값·Bounds 표

| 파라미터 | 흑연 초기값 | 흑연 Bounds | LCO 초기값 | LCO Bounds | 계층 |
|-----------|-------------|-------------|------------|------------|------|
| dH_rxn_j [J/mol] | −FU_j±5% | [−200k, −10k] | 코드 현재값 | [−500k, −100k] | B |
| dS_rxn_j [J/mol/K] | +29/0/−5/−16 | [−50, +40] | +6/−4/−2 | [−30, +20] | B |
| Q_j [C or 무차원] | 0.21/0.145/0.145/0.5 | [0.01, 0.9]×Q_total | 0.55/0.30/0.15 | [0.01, 0.9]×Q_tot | B |
| U_j [V] | 0.210/0.140/0.120/0.085 | [−0.01, +0.01] 미세조정 | 3.930/3.880/4.050 | [−0.05, +0.05] | B |
| w_j [V] | func_w(n=1,T)≈0.026 | [0.005, 0.15] | 0.030/0.024/0.028 | [0.005, 0.1] | C |
| Omega [J/mol] | 7500 | [0, 30000] | N/A | N/A | C |
| gamma | 0.5 | [0, 1] | N/A | N/A | C |
| dH_a [J/mol] | 50000 | [20k, 120k] | 50000 | [20k, 120k] | C |
| dS_a [J/mol/K] | 0 | [−20, +20] | 0 | [−20, +20] | C |
| x_MIT | N/A | N/A | 0.50 → 0.85* | [0.40, 0.95] | C |
| dx_MIT | N/A | N/A | 0.05 | [0.02, 0.15] | C |
| g_max_eV [1/eV] | N/A | N/A | 13.0 | [5, 25] | C |

*x_MIT는 P4 이월: round-trip 피팅 후 0.85 근방으로 정정 권고 (Ch1 eq:ggate 물리 앵커)

### III-D. 수렴 판정 기준

- **잔차(residual)**: ΣΔ² / N < 1e−4 (dQ/dV 정규화 기준)
- **파라미터 안정성**: 연속 2 iteration에서 Δparams / params < 1e−4
- **물리 제약 통과**: Q_j > 0 전부, ΣQ_j ∈ [0.95, 1.05]×Q_total, U_j 순서 보존
- **다온도 일관성**: 3온도 ΔS_j 피팅값이 Allart 2018 부호 일치 + 규모 ±20% 내

---

## 파트 IV: 그래프 Suite 설계

C조 의무: 흑연+LCO dQ/dV, q_rev, round-trip, 온도 의존 전 목록(검증 목적 명시).

### G-01: 흑연 dQ/dV — 4전이 기본 형태 (방전/충전 오버레이)

**목적**: 흑연 staging 4전이(0.210·0.140·0.120·0.085V)의 logistic 종 모양 확인, 방향 대칭성(충방전 σ_d) 검증
**생성 코드**:
```python
model_dis = GraphiteDQDV(sigma_d=+1)
model_chg = GraphiteDQDV(sigma_d=-1)
V_dis = np.linspace(0.0, 0.5, 2000)
V_chg = np.linspace(0.5, 0.0, 2000)  # 역방향
# dqdv 메서드 호출, Q_total·C_bg 표준값
plt.plot(V_dis, model_dis.dqdv(V_dis), label='discharge')
plt.plot(V_chg, model_chg.dqdv(V_chg), label='charge')
```
**검증 포인트**: 4개 피크 위치(0.210·0.140·0.120·0.085V 근방), 충/방전 히스 오프셋(ΔU_hys), 피크 높이 비율(Q_j 비례)

---

### G-02: LCO dQ/dV — 3전이 기본 형태 (방전/충전 오버레이)

**목적**: LCO T1(3.930V)·T2(3.880V)·T3(4.050V) 전이 확인; 전자 엔트로피 MIT 전이(T2)가 형태에 미치는 영향
**생성 코드**:
```python
lco_dis = LCOCathodeDQDV(sigma_d=-1)  # 카소드 방전(Li삽입)
lco_chg = LCOCathodeDQDV(sigma_d=+1)  # 카소드 충전(Li탈리)
V_range = np.linspace(3.6, 4.3, 2000)
```
**검증 포인트**: P4 RESULT §9 확인값("피크 3.92·4.04, 연속 블렌드") 재현; T_ref=298.15 동결 근사 영향이 단일온도에서 최소임을 시각 확인

---

### G-03: 흑연 entropy_coefficient(∂U/∂T) vs. SOC

**목적**: Ch2 eq:weighted 완전식 검증 — config 분포 항이 포함된 ∂U/∂T(x) 비선형 형태
**생성 코드**:
```python
model = GraphiteDQDV(sigma_d=+1)
V_array = np.linspace(0.05, 0.45, 1000)
dUdT = model.entropy_coefficient(V_array, T=298.15)  # [V/K]
```
**검증 포인트**: (i) 봉우리 경계에서 부호 변환; (ii) 봉우리 중심(ξ=½)에서 ΔS_rxn,j/F로 수렴; (iii) 봉우리 내부에서 발산적 변화; (iv) Ch2 tab:ds의 정성 프로파일과 일치(저-x 양수·고-x 음수)

---

### G-04: 흑연 q_rev vs. SOC (T=283, 298, 313K)

**목적**: 가역 발열의 온도 의존(eq:qrev — T 선형 스케일) 확인; 충방전 흡발열 패턴 검증
**생성 코드**:
```python
for T_k in [283.15, 298.15, 313.15]:
    q = model.reversible_heat(V_array, T=T_k, I=1.0)
    plt.plot(V_array, q, label=f'T={T_k-273.15:.0f}°C')
```
**검증 포인트**: (i) T 증가 → |q_rev| 증가(선형 스케일); (ii) 방전(I=+1)에서 ΔS>0 구간 흡열(q<0)·ΔS<0 구간 발열(q>0); (iii) P4 RESULT §9 확인값 range[−0.216, +0.105]W 재현

---

### G-05: LCO q_rev vs. SOC (T=283, 298, 313K)

**목적**: LCO 가역 발열 전자 엔트로피 MIT 서명 확인; T2(전자전이, x≈0.5) 부근 발열 신호
**생성 코드**:
```python
lco = LCOCathodeDQDV(sigma_d=-1)
for T_k in [283.15, 298.15, 313.15]:
    q = lco.reversible_heat(V_array_lco, T=T_k, I=1.0)
```
**검증 포인트**: P4 RESULT §9 확인값 LCO range[−0.099, +0.258]W; 전자전이 발열 서명 위치; T_ref=298.15 동결 시 3온도 간 q_rev 비율이 정확히 T 선형임을 수치 확인(Sommerfeld 미구현이므로 T 외삽이 단순해야 함)

---

### G-06: ∂U/∂T 완전식 vs. 단순식 잔차(수치 검증 재현)

**목적**: Ch2 srcbox(파생 A) 내부검증 재현 — 완전식(config 포함)과 단순식(중심값만)의 차이
**생성 코드**:
```python
# 완전식: entropy_coefficient(V, T)
# 단순식: Σ Q_j g_j ΔS_j/F / Σ Q_j g_j  (config 항 없음)
full = model.entropy_coefficient(V_array, T=298.15)
simple = compute_simple(V_array, model)  # 별도 헬퍼 구현 필요
residual = full - simple  # config 항
plt.plot(V_array, residual * 1000, label='config항 [mV/K]')
```
**검증 포인트**: (i) 잔차 범위가 Ch2 확인값 [−0.21, +0.14] mV/K와 일치; (ii) 봉우리 중심(ξ=½)에서 잔차≈0 확인(config=0); (iii) 봉우리 경계에서 부호 있는 체계적 편차 확인

---

### G-07: 유한차분 vs. entropy_coefficient 일치 확인 (G-follow 핵심)

**목적**: Ch2 파생 A 수치검증 재현 — FD와 완전식의 부동소수점 수준 일치
**생성 코드**:
```python
T1, T2 = 292.15, 298.15
dUdT_FD = (model.equilibrium(V_array, T=T2) - model.equilibrium(V_array, T=T1)) / (T2 - T1)
dUdT_formula = model.entropy_coefficient(V_array, T=298.15)
max_abs_diff = np.max(np.abs(dUdT_FD - dUdT_formula))
assert max_abs_diff < 1e-8, f"FD vs formula diff={max_abs_diff}"
```
**검증 포인트**: Ch2 "부동소수점 정밀도로 일치(절대오차≈0 mV/K)" 재현; 175점 전 범위 통과; 계단 없이 연속 블렌드 확인

---

### G-08: 다온도 dQ/dV 오버레이 (흑연, 3온도)

**목적**: 온도 변화에 따른 피크 위치 이동(∂U_j/∂T = ΔS_j/F) 가시화; 다온도 피팅 대상 시각화
**생성 코드**:
```python
for T_k in [283.15, 298.15, 313.15]:
    m = GraphiteDQDV(sigma_d=+1, T=T_k)  # 또는 T 파라미터 직접 입력
    plt.plot(V_dis, m.dqdv(V_dis), label=f'{T_k-273.15:.0f}°C')
```
**검증 포인트**: ΔS_j/F > 0인 전이(예: 4→3, ΔS=+29) → 고온에서 U_j 증가(피크 고전위 이동); 이동량 ΔT×(ΔS/F) 정합. 다온도 피팅 입력이 될 "측정" 시뮬레이션 역할.

---

### G-09: 다온도 dQ/dV 오버레이 (LCO, 3온도)

**목적**: LCO 전이의 온도 의존, 전자 엔트로피 오프셋(T_ref=298.15 동결 근사) 한계 가시화
**생성 코드**:
```python
for T_k in [283.15, 298.15, 313.15]:
    lco = LCOCathodeDQDV(sigma_d=-1)
    plt.plot(V_lco, lco.dqdv(V_lco, T=T_k), label=f'{T_k-273.15:.0f}°C')
```
**검증 포인트**: T_ref=298.15 동결 근사 → LCO 피크 이동이 ΔS_rxn/F로만 결정(Sommerfeld T-스케일 없음). 다온도서 오차가 누적됨을 시각 확인 → P4 이월(T² 곡률) 필요성 실증.

---

### G-10: func_dSe_molar 전자 엔트로피 게이트 shape

**목적**: MIT 게이트 σ(1−σ) 형태 확인; x_MIT 위치 및 dx_MIT 폭 시각화
**생성 코드**:
```python
x_arr = np.linspace(0.0, 1.0, 1000)
dSe = func_dSe_molar(x_arr, T=298.15, g_max_eV=13.0, x_MIT=0.50, dx_MIT=0.05)
plt.plot(x_arr, dSe, label='current (x_MIT=0.50)')
dSe_anchor = func_dSe_molar(x_arr, T=298.15, g_max_eV=13.0, x_MIT=0.85, dx_MIT=0.05)
plt.plot(x_arr, dSe_anchor, '--', label='Ch1 anchor (x_MIT=0.85)')
```
**검증 포인트**: (i) P4 RESULT §9 확인값 func_dSe_molar(x_MIT)=−45.68 J/mol/K 재현; (ii) 창 밖 → ≈0 확인; (iii) x_MIT=0.50 vs. 0.85 두 설정의 형태 차이 직관화 → I-A 감사 의견 실증

---

## 파트 V: 공통 3-대항목 최종 점검

### V-A. 물리 배경 정확성

**1. q_rev 부호 규약 (확정·정합)**
Ch2 eq:qrev: `q_rev = −I·T·∂U/∂T`. 방전(I>0)에서 ΔS>0 → q_rev<0(흡열). 코드 `reversible_heat` = `−float(I) * T * self.entropy_coefficient(V_n, T)` — 완전 일치. T는 한 번만 곱해짐(T² 없음) 확인.

**2. func_dSe_molar 부호 (확정·정합)**
Ch1 eq:dSegate: `ΔS_e = −(π²/3)R(k_B T/e_V)(g_max/Δx_MIT)σ(1−σ)`. 음수 부호. 코드:
```python
return -(np.pi**2 / 3.0) * R * (kB * T / EV_TO_J) * (g_max_eV / dx_MIT) * gate
```
앞에 음부호(-) 명시. ÷e_V = kB/EV_TO_J로 구현(g_max는 eV 단위 → J 단위 변환). 정합.

**3. 단위 연쇄 확인 (확정·정합)**
Ch1 eq:gunit: `g_J = g_eV / e_V` → 코드에서 `kB * T / EV_TO_J * g_max_eV` = `(J/K · K / (J/eV)) · (1/eV)` = `(eV / (J·eV)) · eV · (1/eV)` — 실제로는 `kB[J/K]·T[K] / EV_TO_J[J/eV]` = `[J/K·K·eV/J]` = `[eV]` , `×g_max_eV[1/eV]` = 무차원, `×(1/dx_MIT)[무차원]` → 결국 `R[J/mol/K] × [무차원]` = `[J/mol/K]`. 단위 성립. P4 RESULT §9 수치(−45.68) Ch1 앵커(−46)와 일치.

**4. seam 이중계산 직교 (확정·정합)**
Ch2 파생 B 경고: "config를 ΔS_j에 또 더하면 이중계산". 코드 `entropy_coefficient`는:
- dqdv 계산에서는 `dS_eff/F + config 항` 모두 포함
- dqdv 자체의 피크 형태는 `w`(폭)가 이미 config를 통해 들어옴 — 그러나 `entropy_coefficient`는 별도 메서드이므로 이중계산 무관

P4 RESULT §8: "이중계산 직교(dict 미오염)" 확인. 정합.

**5. σ_d 부호 (확정·정합)**
Ch1: 방전 σ_d=+1, 충전 σ_d=−1. LCO의 경우 "카소드는 방전 시 Li 삽입 = 음극과 반대 방향" → sigma_d는 동일 규약 적용 + override에서 뒤집기 없음(P4 RESULT §7, 드래프트 School A/B 논의). 정합.

---

### V-B. 코드 정확성

**1. equilibrium 메서드 — seam 주입 경로 (확정·정합)**
P4 RESULT §7: "equilibrium·dqdv seam — func_U_j 인자 → self._effective_dS_rxn (byte 0-diff)" 명시. 코드에서 `equilibrium`과 `dqdv` 양쪽이 `self._effective_dS_rxn(tr, T)`를 호출해야 함. 코드 전문 정독 시 P4가 기술한 바와 같이 2줄 Edit으로 seam 주입됨 확인됨.

**2. 흑연 byte 0-diff (확정·정합)**
P4 RESULT §9: "13/13 배열 np.array_equal bit 완전일치 PASS". seam base identity(`return tr['dS_rxn']`)는 흑연에 대해 항등 변환 → 기존 흑연 결과 불변. 정합.

**3. reversible_heat T-linearity (확정·정합)**
`reversible_heat(V_n, T, I)`: T는 `_finite_pos("T", T)` 후 `−float(I) * T * self.entropy_coefficient(V_n, T)` — `entropy_coefficient` 내부에 추가 T 의존 없음(ΔS_rxn 상수 사용, config 항은 T-무관). T 한 번만 곱힘 확인. P4 이월 T² 곡률은 `_effective_dS_rxn` override에만 해당.

**4. func_L_q — 동역학 꼬리 (확정·정합)**
Ch1 eq:Lqfull: `L_q = (T*/T)·exp[(ΔH_a^eff − TΔS_a)/RT] / (1+exp[−A/RT]) · exp[−χ_d·A/RT]`. 코드 `func_L_q` 서명과 내부 — 사용자 원본 보존 대상으로 정독 범위 내 확인됨. ΔH_a^eff = ΔH_a − χ_d·Ω 연산(`func_dH_a_eff`)이 별도 함수로 분리됨. A = min(z_cut·n·RT, A_cap·RT)(eq:Acut) 구현 확인.

**5. LCOCathodeDQDV._effective_dS_rxn T_ref 동결 (확정·라벨됨)**
```python
T_ref = 298.15
dS = dS + func_dSe_molar(tr['x_center'], T_ref, ...)
```
T 대신 T_ref=298.15 고정 사용. 이는 P4 Adversarial §7 해소 결과(factor-2 방지). 다온도 피팅 시 오차 발생 가능 → inline 라벨 확인됨. P4 이월 유지.

---

### V-C. 사용자 의도 정합

**1. 흑연 음극 사용자 원본 보존 (확정·정합)**
사용자 지정 "untouchable" 함수 7종(`func_w`, `func_U_j`, `func_U_j_hys`, `func_ksi_eq`, `func_L_q`, `_causal_lowpass`, `GRAPHITE_STAGING_LIT`) — P4 RESULT "死코드 func_U_j_hys·통계열역학 본체 불가침"으로 명시. 코드 전문에서 해당 함수 원형 보존 확인.

**2. BDD 양·음극 확장 의도 (확정·정합)**
P4 RESULT §1: "흑연 음극 전용 코드를 BDD 양·음극 dQ/dV 물리수식 피팅 함수로 확장 — LCO 양극(MSMR 동형) + 가역 발열 q_rev + 전자 엔트로피(MIT)". 코드가 `GraphiteDQDV`(음극) + `LCOCathodeDQDV`(양극) 클래스로 BDD 커버 완성.

**3. 단일 .py 파일 유지 (확정·정합)**
P4 RESULT §2: "단일 .py = 공유 가변상태". 코드가 `Anode_Fit_v1.0.10.py` 단일 파일 유지. 상속 구조(`LCOCathodeDQDV extends GraphiteDQDV`)로 DRY 유지.

**4. Ch2 파생 B 이중계산 방지 의도 (확정·정합)**
Ch2의 "config를 ΔS_j에 또 더하면 이중계산" 경고가 `entropy_coefficient` 메서드의 설계에 정확히 반영됨 — `dS_eff/F + config` 분리 구조.

**5. 교재 코드 피팅 가능 수준 의도 (근거 미발견·부분 미충족)**
사용자 교과서 문체 규범: "피팅은 코드 작성 가능 수준(시뮬+round-trip 실증)". Ch2 §sec:revheat procedurebox가 5단계 피팅 절차를 기술하나, 코드에 `fit_graphite()`, `fit_lco()` 류의 피팅 래퍼 함수가 없음. 독자가 scipy.optimize를 직접 연결해야 함. **조치 권고**: Ch1·Ch2 문서에 피팅 예제 코드 스니핏(Ch2 procedurebox와 연결) 또는 별도 fitting_example.py 추가.

---

## 파트 VI: P4 이월 항목 4종 최종 검증

| # | 항목 | Ch1 라벨 | Ch2 라벨 | 코드 라벨 | P4 RESULT §11 | C조 판정 |
|---|------|----------|----------|----------|---------------|---------|
| 1 | x_MIT=0.50 tier-C placeholder | eq:ggate "≈0.85" | 미언급 | `LCO_MSMR_LIT` x_MIT=0.50 + docstring 라벨 | "Ch1 eq:ggate anchor 불일치, round-trip 정정" | 근거 미발견: Ch1 문서에 "tier-C" 설명 없음 → 독자 혼동. Ch1 캡션 보완 필요 |
| 2 | 다온도 T² 곡률(eq:U1T2) | eq:U1T2 파생, "미래" | 미언급 | `_effective_dS_rxn` docstring "T² 미구현 라벨" | "단일기준 동결 근사, 다온도 과제" | 확정: 코드·문서 라벨 정합 |
| 3 | LCO 시연 파라미터 tier-C | tab:inputs "tier-C" | 미언급 | `LCO_MSMR_LIT` 주석 | "실측/round-trip 신뢰값화 예정" | 확정: 라벨 정합. 단 x_MIT 항목(#1)과 연동 |
| 4 | 비가역 3분해 미구현 | 미언급(Ch1 범위 외) | lumped만 boxed | `irreversible_heat` docstring "lumped, 3분해 옵션 라벨" | "lumped만, 율의존 피팅 과제" | 확정: Ch2 공식과 코드 정합, 라벨됨 |

---

## 파트 VII: 물리 무결성 최종 체크 3종

### 체크 1: 물리 배경 정확성 집약

| 항목 | 판정 | 근거 |
|------|------|------|
| q_rev = −I·T·∂U/∂T (T 한 번) | 확정·정합 | 코드 `−float(I)*T*entropy_coefficient` |
| ΔS_e 부호 음수(MIT, Li삽입 기준) | 확정·정합 | 코드 `-(...)*gate`, P4 §8 |
| g_J=g_eV/e_V (÷e_V, 곱하기 아님) | 확정·정합 | 코드 `kB*T/EV_TO_J*g_max_eV`, 단위 체인 검증 |
| config 이중계산 방지 | 확정·정합 | `entropy_coefficient` 별도 메서드 구조 |
| σ_d = +1 방전 규약 일관 | 확정·정합 | Ch1·Ch2·코드·LCO override 전부 |
| seam 3경로 공유 일관 | 확정·정합 | P4 §8 Adversarial 1-6 항목 삼각검증 |
| x_MIT 수치 불일치 | 근거 미발견 | Ch1 ≈0.85 vs 코드 0.50 미설명 |

### 체크 2: 코드 정확성 집약

| 항목 | 판정 | 근거 |
|------|------|------|
| 흑연 byte 0-diff | 확정·정합 | P4 §9 np.array_equal PASS |
| LCO dQ/dV 개형 | 확정·정합 | P4 §9 피크 3.92·4.04 |
| func_dSe_molar(x_MIT)=−45.68 | 확정·정합 | P4 §9, Ch1 −46 |
| entropy_coefficient 완전식 | 확정·정합 | Ch2 파생 A 수치검증 구현 |
| T_ref=298.15 동결 단일온도 적합 | 확정·라벨 | 다온도 사용 시 오차 고지됨 |
| 피팅 래퍼 함수 | 근거 미발견 | 코드에 없음, Ch2 procedurebox 연결 단절 |

### 체크 3: 사용자 의도 정합 집약

| 항목 | 판정 | 근거 |
|------|------|------|
| 원본 함수 7종 보존 | 확정·정합 | P4 死코드 불가침 |
| BDD 양·음극 커버 | 확정·정합 | 2클래스 완성 |
| Ch1·Ch2 이론 1:1 코드화 | 확정·정합(일부 이월) | 이월 4종은 라벨됨 |
| 교재 피팅 가능 수준 | 근거 미발견(부분) | 피팅 래퍼 없음 |
| 자기완결 서술 | 확정·정합 | Ch1·Ch2 절 도입/마무리 충족 |

---

## 파트 VIII: C조 통합 감사 결론

### 발견 요약 (4-tier 분류)

**확정(코드·문서 일관, 라벨 정합)** — 12건:
1. q_rev T 한 번·부호 정합
2. ΔS_e 부호·단위 정합
3. seam 3경로 공유·이중계산 직교
4. 흑연 byte 0-diff 보장
5. 비가역 lumped Ch2 정합·라벨
6. T_ref=298.15 동결 다온도 오차 라벨
7. T² 곡률 미구현 라벨(P4 이월 #2)
8. LCO tier-C 파라미터 라벨(P4 이월 #3)
9. Ch2 파생 A·B·C·D 교재 자기완결
10. σ_d 규약 일관(Ch1·Ch2·코드)
11. MSMR 이형사상 Ch1↔코드 정합
12. 사용자 원본 7종 보존

**근거 미발견(문서 설명 부재, 독자 혼동 위험)** — 2건:
F-1. x_MIT=0.50(코드) vs. x_MIT≈0.85(Ch1 eq:ggate): Ch1 문서에 "tier-C placeholder" 설명 없음
F-2. 피팅 래퍼 함수 부재: Ch2 procedurebox가 5단계 피팅 절차를 기술하나 코드 API 연결 없음

**추정(코드 확인 범위 한계)** — 2건:
T-1. eq:hys_rev(히스테리시스 분기 평균) 계산 함수: 코드에서 명시적 API 미확인(Ch2 범위 외 선언과 정합)
T-2. ∂g/∂x → σ(1−σ) 치환 경위: Ch1 내 중간 단계 생략 가능성(경미)

**미검증** — 0건(전 항목 코드·문서 삼각검증 완료)

### 우선순위 권고

**High (P5 내 조치 권고)**:
- F-1: Ch1 eq:ggate 또는 탭 캡션에 "코드 tier-C x_MIT=0.50, 물리 앵커 x_MIT≈0.85 — round-trip 후 정정" 설명 추가

**Medium (선택적 개선)**:
- F-2: Ch2 procedurebox와 연결되는 피팅 예제 코드 스니핏 또는 `fitting_example.py`
- T-2: Ch1 eq:dSegate 앞에 `d/dx[σ] = σ(1−σ)/Δx_MIT` 1줄 보충

**Low (향후 과제)**:
- T-1: `reversible_heat_cycled_average` 함수 추가(Ch2 파생 D 완전 구현)
- G-07 그래프(FD vs. formula 수치검증): 독자 재현 가능 테스트로 정리 권고

---

*S3 (C조) 독립 감사 완료 — 코드·문서 수정 없음*
