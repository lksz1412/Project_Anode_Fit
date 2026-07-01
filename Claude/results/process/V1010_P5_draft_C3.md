# Anode_Fit v1.0.10 P5 최종점검 감사 드래프트 C3

조: C조(완성도+코드없는내용0+피팅추천+그래프suite)  
역할: 감사 의견만. 코드/문건 수정 없음.  
판정 기준: `확정 / 근거미발견 / 추정 / 미검증` 분리. 허위 attribution 금지. 추정으로 빈칸 보충 금지.

---

## 0. 수행 범위와 읽은 범위

### 직접 정독 범위

- base prompt: `C:/Users/lksz1/AppData/Local/Temp/claude/d--Projects/f45f576c-1efc-4f50-8591-1f84bb7d7f39/scratchpad/p5_audit_base.txt` 전문.
- 프로젝트 지침: `CLAUDE.md` 전문, `Codex/AGENTS.md` 전문. 루트 `AGENTS.md` 없음 확인.
- 코드: `Claude/docs/v1.0.10/Anode_Fit_v1.0.10.py` 1-849행.
  - 1차 출력 중 302-536행 생략 의심 구간 재독 완료.
- Ch1: `Claude/docs/v1.0.10/graphite_ica_ch1_v1.0.10.tex` 1-1932행.
  - 1-500, 501-1000, 1001-1500, 1501-1932 구간 출력.
  - 생략 의심 구간 244-277, 730-788, 1200-1298, 1724-1763 재독 완료.
- Ch2: `Claude/docs/v1.0.10/graphite_ica_ch2_v1.0.10.tex` 1-750행.
  - 1차 출력 중 250-559행 생략 의심 구간 재독 완료.
- 앵커:
  - `Claude/results/process/V1010_P1_code-audit_RESULT.md` 1-445행.
  - `Claude/results/process/V1010_P2_ch1_RESULT.md` 1-83행.
  - `Claude/results/process/V1010_P3_ch2_RESULT.md` 1-83행.
  - `Claude/results/process/V1010_P4_code-revision_RESULT.md` 1-58행.

### 보조 감사 범위

- Ch1 보조 감사: Ch1 1-1932행, 코드 1-849행 read-only.
- Ch2 보조 감사: Ch2 1-750행, 코드 1-849행, `plot_dqdv.py`, `demo_lco_heat.py`, `test_regression_graphite.py` read-only.
- 피팅/그래프 보조 감사: 코드, Ch1, Ch2, P1/P4 관련 산출, 그래프 산출물 read-only.
- 보조 감사는 최종 책임 근거로 단독 채택하지 않고, 직접 확인 범위와 대조해 아래 tier에 통합했다.

---

## 1. 총평

**P5 C조 기준 최종 판정: 조건부 FAIL.**

물리식 핵심 골격 자체는 상당히 정리되어 있다. 특히 q_rev의 `T` 한 번, Ch2 weighted entropy coefficient, 비가역 발열 lumped 구현, Ch1/Ch2의 전자엔트로피 단위 다리, P4의 흑연 회귀 0-diff 라벨은 큰 방향에서 맞다.

그러나 C조의 핵심 조건인 **코드 없는 내용 0**, **피팅 추천**, **그래프 suite**에는 아직 확정 갭이 남는다. 가장 큰 문제는 LCO 전자항/전이표/피팅 단계가 문건에서는 물리 anchor에 가까운 형태로 읽히지만, 실제 코드는 `tier-C placeholder`와 단일 기준온도 동결 근사를 쓰고 있다는 점이다. Ch2도 엄밀한 SOC-grid q_rev 절차와 히스 분기 평균 가역열을 문서화하지만, 현 코드 API는 전압 격자 진단 함수 수준이다.

---

## 2. 확정 갭

### G1. Ch1 LCO 전이표 이름과 전이값이 코드와 맞지 않음

- Tier: **확정**
- 위치:
  - Ch1 `LCO_STAGING_LIT` 명명 및 표: `graphite_ica_ch1_v1.0.10.tex` L311-L317, L322-L335.
  - Ch1 코드 매핑: L1750-L1756, L1843-L1847.
  - 코드 실제: `Anode_Fit_v1.0.10.py` L615-L638.
- 내용:
  - Ch1은 `LCO_STAGING_LIT` 3전이를 T1 MIT `~3.90 V`, T2 `~4.05 V`, T3 `~4.17--4.20 V`로 제시한다.
  - 코드에는 `LCO_STAGING_LIT`가 없고 `LCO_MSMR_LIT`만 있다.
  - 코드 전이값은 `3.930`, `3.880`, `4.050 V`이며, 주석상 `tier-C 시연 기본값 — round-trip 피팅 前 placeholder`다.
- 맞는 형태:
  - 문건은 현 코드 기준이면 `LCO_MSMR_LIT`로 명명하고, `3.930/3.880/4.050 V`가 **시연 placeholder**임을 명시해야 한다.
  - 물리 anchor 표를 유지하려면 코드 구현 표와 문헌 anchor 표를 분리해야 한다.

### G2. LCO MIT 전자항의 조성 anchor가 Ch1과 코드에서 불일치

- Tier: **확정**
- 위치:
  - Ch1 MIT gate: L1063-L1075 (`x_MIT≈0.85`, `dx≈0.05`).
  - Ch1 T1 전자항 plug-in: L1713-L1716, L1752-L1756.
  - 코드 placeholder: `Anode_Fit_v1.0.10.py` L626-L633, L667-L670.
  - P4 이월: `V1010_P4_code-revision_RESULT.md` L53-L56.
- 내용:
  - Ch1은 MIT 중심을 `x_MIT≈0.85`, 2상역 `x≈0.75--0.94`로 둔다.
  - 코드는 전자항 전이에 `x_center=0.50`, `x_MIT=0.50`, `dx_MIT=0.05`를 넣는다.
  - P4 결과도 이를 `x_MIT=0.50 tier-C placeholder`와 Ch1 `x_MIT≈0.85` 불일치로 명시했다.
- 맞는 형태:
  - 현재 코드값은 물리값이 아니라 `tier-C placeholder`로 문건 본문 표와 코드 매핑에 분명히 분리해야 한다.
  - 최종 물리값은 round-trip 피팅 후 `x_MIT≈0.85` anchor와 정합되게 승격해야 한다.

### G3. Ch1의 다온도 T² 전자항은 코드에서 구현되지 않은 과제임

- Tier: **확정**
- 위치:
  - Ch1 `ΔS_e∝T`, `U_1(T)∝T^2`: L1042-L1061, L1208-L1211.
  - 코드 동결 근사: `Anode_Fit_v1.0.10.py` L659-L664, L667-L670.
  - P4 이월: `V1010_P4_code-revision_RESULT.md` L40, L55.
- 내용:
  - Ch1은 전자항의 관측 신호로 `∂U_1/∂T`가 T에 선형, 위치 이동이 `T²`라고 설명한다.
  - 코드는 `T_ref=298.15`에서 `func_dSe_molar(...)`를 평가해 상수 오프셋으로 더한다.
  - 코드 주석도 `Sommerfeld T-scale`과 `eq:U1T2`는 다온도 round-trip 피팅 단계 과제라고 명시한다.
- 맞는 형태:
  - 문건 본문에서 P4 현 코드가 구현한 것은 **단일 기준온도 동결 근사**이고, Ch1 `eq:U1T2`는 **미구현/피팅 과제**임을 같은 위치에서 표시해야 한다.

### G4. Ch1의 LCO 세 전이 `Ω_j>2RT`/두-상 폭 지위는 현 코드에 없음

- Tier: **확정**
- 위치:
  - Ch1 LCO order-disorder/MIT two-phase: L679-L696.
  - Ch1 LCO peak 폭: L1200-L1211.
  - 코드 LCO dict: `Anode_Fit_v1.0.10.py` L621-L638.
  - 코드 Omega 기본 처리: L463-L472.
- 내용:
  - Ch1은 LCO 세 전이가 모두 `Ω_j>2RT`의 두-상 전이이며 폭이 현상학적 피팅 폭이라고 설명한다.
  - 코드 `LCO_MSMR_LIT`에는 `Omega`, `gamma` 키가 없다.
  - 따라서 현 코드에서 LCO 히스 분기/두-상 gap은 켜지지 않고, `Omega=0.0`, `gamma=0.0` 기본 경로다.
- 맞는 형태:
  - 문건은 LCO two-phase/hysteresis 설명을 **이론/피팅 후보**로 두고, 현 P4 코드 시연은 `Omega/gamma` 미지정이라고 분리해야 한다.

### G5. Ch2의 SOC-grid q_rev 절차는 코드 API로 직접 지원되지 않음

- Tier: **확정**
- 위치:
  - Ch2 종합식 절차: `graphite_ica_ch2_v1.0.10.tex` L668-L684.
  - Ch2 방법론 출구: L699-L715.
  - 코드 heat API: `Anode_Fit_v1.0.10.py` L544-L586.
- 내용:
  - Ch2는 주어진 SOC `x`에서 전하보존 음함수 `Σ Q_j ξ_j(U_oc,T)=Qx`를 풀어 `U_oc(x,T)`를 얻고 다시 `ξ_j`에 되먹이라고 한다.
  - 현 코드는 `entropy_coefficient(V_n,T)`와 `reversible_heat(V_n,T,I)`를 제공한다. 입력은 전압 격자이며 SOC→전압 solver가 없다.
- 맞는 형태:
  - 현 코드는 **voltage-grid diagnostic**으로 라벨해야 한다.
  - Ch2식의 엄밀 SOC-grid q_rev를 주장하려면 `U_oc(x,T)` solver와 그 그래프/검증이 필요하다.

### G6. Ch2 히스테리시스 분기 평균 가역열은 문서에는 있으나 코드에는 없음

- Tier: **확정**
- 위치:
  - Ch2 `eq:hys_rev`: L570-L584.
  - 코드 dqdv 분기 중심: `Anode_Fit_v1.0.10.py` L460-L477.
  - 코드 heat 메서드: L544-L586.
- 내용:
  - Ch2는 가역 발열에 들어가는 엔트로피 계수를 충/방전 분기 평균 `1/2(ch+dis)`로 제시한다.
  - 코드 `dqdv()`에는 히스 분기 중심이 있으나, `entropy_coefficient()`와 `reversible_heat()`에는 `direction`, `gamma`, branch-average 인자가 없다.
- 맞는 형태:
  - Ch2 `eq:hys_rev`는 현 코드-backed 항목이 아니라 **이론/후속 구현 후보**로 라벨해야 한다.
  - 코드-backed 발열은 현재 평형 중심 기반 weighted entropy coefficient다.

### G7. Ch2 “175점 FD와 완전식 부동소수점 일치”는 재현 가능한 코드/테스트 근거 미발견

- Tier: **근거미발견**
- 위치:
  - Ch2 수치 검증 claim: L484-L494, L687-L690, L747.
  - 관련 테스트 확인: `test_regression_graphite.py`는 dQ/dV 회귀/면적 중심.
- 내용:
  - Ch2는 내부 수치 검증으로 175점 finite-difference와 완전식의 부동소수점 일치를 주장한다.
  - 읽은 코드/테스트/그래프 suite에서 해당 FD 비교 스크립트나 machine artifact를 찾지 못했다.
- 맞는 형태:
  - claim을 유지하려면 재현 스크립트/결과 경로를 명시해야 한다.
  - 없으면 “내부 검증 결과”가 아니라 “유도상 예상/미검증”으로 내려야 한다.

### G8. `w_j` 자유 피팅 폭과 config 항 계수의 연결 설명이 부족함

- Tier: **확정**
- 위치:
  - Ch2 `∂w/∂T=R/F` 유도: L457-L464.
  - Ch2 두-상 `w_j` 현상학적 자유 피팅 폭: L539-L560, L676-L680.
  - 코드 `n/w` 처리: `Anode_Fit_v1.0.10.py` L293-L306.
  - 코드 config 항: L566-L573.
- 내용:
  - Ch2의 config 항 유도는 `w=RT/F`의 명시적 온도 의존에서 `(R/F)ln(...)`를 얻는다.
  - 같은 문서는 흑연 두-상 `w_j`를 다온도 피팅으로 얻는 현상학적 자유 폭이라고 둔다.
  - 코드도 `n` 또는 `w` override를 허용하지만, `entropy_coefficient()`의 config 항 계수는 항상 `R/F`다.
- 맞는 형태:
  - `n_j≠1` 또는 `w`가 T-independent 피팅 폭일 때 config 계수가 왜 여전히 `R/F`인지, 또는 어떤 조건에서만 이 식을 쓰는지 명시해야 한다.

### G9. 피팅 추천은 파라미터 목록은 넓지만 numeric bounds/tier/protocol이 부족함

- Tier: **확정**
- 위치:
  - Ch1 입력표/피팅 준비: L1762-L1804.
  - Ch2 다온도 피팅 절차: L699-L715.
  - P1 피팅 결함/인벤토리: `V1010_P1_code-audit_RESULT.md` L324-L367, L371-L404.
- 내용:
  - `{ΔH_rxn, ΔS_rxn, Q, w/n, Ω, γ, χ, kinetics, LCO MSMR, electronic term}` 인벤토리는 대체로 존재한다.
  - 그러나 실제 optimizer용 numeric bounds, shared/fixed/free tier, 전이별 제약, LCO electronic bounds가 닫힌 표로 없다.
  - Ch1도 “어느 것을 고정하고 어느 것을 피팅할지는 사용자가 데이터로 정한다”고 남긴다.
- 맞는 형태:
  - 최소 표: `parameter / tier / initial value / lower / upper / constraint / required data / release status`.
  - 필수 bound 후보: `Q_j>=0`, `ΣQ_j` normalization, `n_j>0`, `0<=γ<=1`, `0<=χ<=1`, `dH_a>0`, `dVdq_qa>=0`, `dx_MIT>0`, `g_max_eV>=0`, `x_MIT` 물리 구간.

### G10. round-trip 피팅 검증 suite가 조각별 절차에 머물고 통합 recovery protocol이 없음

- Tier: **확정**
- 위치:
  - Ch2 다온도 dQ/dV 절차: L699-L715.
  - P1 초벌 피팅 순서: `V1010_P1_code-audit_RESULT.md` L358-L367.
  - P4 이월: `V1010_P4_code-revision_RESULT.md` L54-L58.
- 내용:
  - 문건에는 다온도 중심 기울기 추정과 단계적 피팅 순서가 있다.
  - 그러나 synthetic true parameter 생성, noise/multistart, recovered-vs-true, holdout T/C-rate, residual/parity plot까지 닫힌 round-trip protocol은 없다.
- 맞는 형태:
  - graphite와 LCO를 분리해 true/recovered table, parity plot, residual plot, holdout temperature/rate 검증을 요구해야 한다.

### G11. graph suite는 현재 demo/시각화 수준이며 P5 요구 suite에는 부족함

- Tier: **확정**
- 위치:
  - P4 그래프 PASS: `V1010_P4_code-revision_RESULT.md` L48-L51.
  - `plot_dqdv.py`는 dQ/dV 시각화/면적 중심.
  - `demo_lco_heat.py`는 graphite/LCO dQ/dV와 q_rev range/figure 저장 중심.
- 내용:
  - 현재 그래프는 흑연 dQ/dV, LCO dQ/dV, q_rev 시연에는 유효하다.
  - 그러나 요청된 graph suite 중 round-trip parameter recovery, bounds sensitivity, multi-temperature T1 shift, SOC-grid q_rev 검증, electronic on/off 비교는 확인되지 않는다.
- 맞는 형태:
  - `demo PASS`와 `final validation suite 미완`을 분리해야 한다.
  - 필요한 그래프: `roundtrip_recovery_graphite`, `roundtrip_recovery_lco`, `bounds_sensitivity`, `temperature_holdout`, `T1 electronic on/off`, `SOC-grid q_rev`.

### G12. “내부 하드코딩 상수 없음” 문장은 LCO 전자항 현 구현에는 맞지 않음

- Tier: **확정**
- 위치:
  - Ch1 피팅 준비: L1762-L1765.
  - 코드 LCO 전자항: `Anode_Fit_v1.0.10.py` L667-L670.
- 내용:
  - Ch1은 곡선식의 모든 기호가 생성자 인자 또는 전이 dict 키이며 내부 하드코딩 상수는 없다고 한다.
  - 코드 `LCOCathodeDQDV._effective_dS_rxn()`은 `T_ref=298.15`를 내부 상수로 둔다.
- 맞는 형태:
  - “현 Ch1 graphite core 기준”으로 제한하거나, LCO 전자항의 `T_ref=298.15`는 단일 기준 근사의 내부 상수임을 예외로 명시해야 한다.

---

## 3. 정합 PASS 또는 보류 항목

### q_rev T 한 번

- Tier: **확정 PASS**
- Ch2 L643-L646과 코드 L578-L586이 정합한다.
- `q_rev=-I*T*∂U/∂T`이며 T² 자동누적은 코드에서 피했다.

### weighted entropy coefficient

- Tier: **확정 PASS, 단 전압 격자 기준**
- Ch2 L669-L684의 weighted formula는 코드 L544-L576에 구현되어 있다.
- 단 G5처럼 SOC-grid 음함수 solver는 별도 미구현이다.

### 비가역 발열 3분해

- Tier: **확정 PASS**
- Ch2 boxed 식은 lumped `I(U_oc-V)`이고, 코드 L588-L596도 lumped only다.
- `I²R_n + Iη_ct + Iη_diff` 개별 분해는 P4 이월 L57 및 코드 docstring에서 후속 피팅 과제로 분리되어 있다.

### P4 이월 라벨

- Tier: **부분 PASS**
- `x_MIT tier-C placeholder`, `다온도 T² 곡률 미구현`, `LCO 시연 파라미터`, `비가역 3분해`는 P4 결과 L53-L57에 이월로 명시되어 있다.
- 다만 Ch1/Ch2 본문에서는 일부 항목이 현 코드-backed처럼 읽힐 여지가 있어 본문 라벨 보강이 필요하다.

---

## 4. 교재 자기완결성 감사

### 확정

- Ch1은 전하/전위/히스/logistic/꼬리/LCO 전자엔트로피 유도를 긴 단계로 제공한다. 큰 흐름은 자기완결성이 높다.
- Ch2도 분배함수→점유 분포→config/vib/electronic→weighted entropy→q_rev 사슬을 제공한다.

### 남은 갭

- LCO 전자항의 `x` 좌표를 코드 전압 격자로 연결하는 `x↔ξ_eq(V)` 매핑은 Ch1 L1724-L1729에서 “다음 단계 / 별도 상태 변수 또는 전이 진행률 매핑”으로 남는다. 현 코드는 `x_center` 상수만 사용한다.
- Ch2의 SOC-grid q_rev 절차는 문서상 닫혀 있으나 코드 API와 그래프 검증이 전압-grid 진단 수준이다.
- Ch2의 “모든 모양”, “측정급 비선형”, “확정했다”류 표현은 L687-L697의 실데이터/히스/Ω(T)/electronic gap과 충돌해 과장으로 읽힐 수 있다. “모델 내부 검증 기준”으로 제한하는 것이 맞다.

---

## 5. 피팅 추천 감사

### 확정된 장점

- 파라미터 인벤토리 폭은 충분하다.
- P1은 주/보조 파라미터와 초벌 피팅 순서를 제시한다.
- Ch2는 다온도 dQ/dV에서 `ΔS^0_j=F dU_j/dT`를 얻는 절차를 제시한다.

### 확정 부족

- numeric bounds가 부족하다.
- LCO `x_MIT`, `dx_MIT`, `g_max_eV`, `x_center`, `T_ref`의 release status가 분리되지 않았다.
- synthetic round-trip recovery가 없다.
- graphite/LCO별 shared/free/fixed parameter strategy가 없다.
- 현재 `LCO_MSMR_LIT` 시연값은 tier-C placeholder인데, 문건 표의 물리 anchor와 나란히 놓이면 신뢰값처럼 읽힌다.

### 정정용 권고

1. 피팅 표 추가:
   - 열: `parameter`, `scope(graphite/LCO/shared)`, `initial`, `lower`, `upper`, `constraint`, `tier`, `required data`, `release status`.
2. 단계 추가:
   - Phase A: 저율 등온 graphite/LCO dQ/dV로 `U_j,Q_j,n_j,Cbg`.
   - Phase B: 충/방전 pair로 `Rn,γ,Ω`.
   - Phase C: rate-series로 `L_V` 직접 fit 후 `dH_a,dS_a,dVdq_qa,χ` 물리 환산.
   - Phase D: 다온도 series로 `ΔS_rxn`, LCO `a_e/x_MIT/dx_MIT/g_max_eV`.
   - Phase E: holdout T/C-rate 검증.
3. `L_V` 직접 fit과 물리 `dH_a,dVdq_qa,χ` fit은 동시에 열지 말고 tier를 분리한다.

---

## 6. 그래프 suite 감사

### 현재 확인

- 흑연 dQ/dV 시연 및 면적/온도/충방전 그림은 존재한다.
- P4 LCO/heat demo는 graphite dQ/dV, LCO dQ/dV, q_rev range를 보여준다.
- P4 결과는 그래프 3종 PASS를 기록한다.

### 부족

- round-trip parameter recovery 그래프 없음.
- LCO `x_MIT=0.50` placeholder와 `x_MIT≈0.85` 물리 anchor 비교 그래프 없음.
- electronic on/off 비교 없음.
- multi-temperature T1 shift / T² curvature 그래프 없음.
- SOC-grid q_rev와 voltage-grid diagnostic q_rev 비교 없음.
- bounds sensitivity, residual, holdout plot 없음.

### 정정용 그래프 목록

1. `graphite_dqdv_equilibrium_rate_temperature.png`
2. `lco_dqdv_msmr_placeholder_vs_anchor.png`
3. `qrev_voltage_grid_diagnostic.png`
4. `qrev_soc_grid_after_solver.png`
5. `lco_electronic_on_off_T1_shift.png`
6. `roundtrip_recovery_graphite_parity_residual.png`
7. `roundtrip_recovery_lco_parity_residual.png`
8. `bounds_sensitivity_identifiability.png`
9. `holdout_temperature_rate_validation.png`

---

## 7. 3대 무결 최종 확인

### 물리 배경 정확

- 핵심 q_rev, weighted entropy, lumped irreversible heat, Sommerfeld 단위 다리는 대체로 정확하다.
- 단 LCO MIT/T²/두-상/전자항은 현 코드 구현과 물리 본문 사이의 release status가 섞여 있어 최종본 기준 정확성 라벨 보강 필요.

### 코드 정확

- 코드 자체는 P4 의도대로 흑연 회귀 보존, LCO placeholder, q_rev diagnostic, lumped irreversible heat를 구현한다.
- 문제는 코드가 구현한 범위보다 문건이 더 강한 claim으로 읽히는 지점들이다.

### 사용자 의도 반영

- 사용자 의도인 “BDD 양·음극 dQ/dV 물리수식 피팅 함수”, “코드 없는 내용 0”, “피팅 추천”, “그래프 suite”에는 아직 미완 항목이 있다.
- P5에서 master 정정 시 문건/코드/그래프 release status를 명확히 분리하면 의도 반영 가능.

---

## 8. master 정정 목록

1. Ch1 `LCO_STAGING_LIT` 표와 코드 매핑을 `LCO_MSMR_LIT` 현 구현표와 문헌 anchor 표로 분리.
2. `x_MIT=0.50`, `x_center=0.50`은 `tier-C placeholder`로 본문에 명시하고, `x_MIT≈0.85`는 물리 anchor/피팅 목표로 분리.
3. `eq:U1T2`와 `Sommerfeld T-scale`은 현 코드 미구현, 단일 기준온도 동결 근사는 구현으로 분리.
4. LCO `Ω_j>2RT`, `γ`, two-phase/hys는 현 코드 LCO dict 미지정이므로 이론/피팅 후보로 라벨.
5. Ch2 SOC-grid q_rev 절차와 코드 voltage-grid diagnostic을 분리.
6. Ch2 `eq:hys_rev` branch-average heat는 후속 구현 후보로 라벨.
7. Ch2 175점 FD 검증은 재현 artifact 경로를 붙이거나 tier를 `근거미발견/미검증`으로 낮춤.
8. `w_j` 자유 피팅 폭과 config coefficient `(R/F)ln(...)`의 적용 조건을 명시.
9. 피팅 bounds/tier/protocol 표 추가.
10. graph suite를 demo와 validation/recovery로 분리하고 recovery/holdout 그래프를 추가.

---

## 9. 추가 후보

- 코드 self-test에서 q_rev T-once와 entropy coefficient finite는 확인되지만, Ch2 FD 175점 검증 및 SOC-grid q_rev solver는 별도 테스트로 분리하는 것이 좋다.
- `T_ref=298.15`는 P4 안정화 선택으로 타당하나, 피팅 API로 노출할지 또는 “internal fixed reference”로 명시할지 결정 필요.
- LCO 전이 `U=3.880`에 electronic flag가 붙은 현 시연 구조는 물리 anchor와 어긋나므로, 그래프 suite에서 placeholder임을 시각적으로 라벨해야 한다.

---

## 10. 5줄 요약

조: C3 / C조(완성도+코드없는내용0+피팅추천+그래프suite).  
확정 갭 수: 11건 확정 + 1건 근거미발견 핵심 claim.  
최중대 갭: Ch1 LCO MIT/전이표/`x_MIT` 물리 anchor와 코드 `LCO_MSMR_LIT` tier-C placeholder가 섞여 코드-backed처럼 읽힘.  
정정 목록: LCO 표 분리, `x_MIT` placeholder 라벨, T² 미구현 라벨, SOC-grid q_rev/branch-average heat 후속 라벨, 피팅 bounds·round-trip·graph suite 추가.  
리스크: 현 상태로 “코드 없는 내용 0” PASS를 선언하면 LCO 전자항·q_rev 엄밀 절차·그래프 recovery에서 과대보고가 된다.
