# V1010 P2 드래프트 S2 — Ch1 ↔ 코드 coverage 매트릭스 + 누락 유도 보완 + LCO 이론 정련

> **작업 sub 산출**: P2 9종 경쟁 드래프트 S2 (독립 서브 역할)  
> **입력 정독 근거**: `graphite_ica_ch1_v1.0.10.tex`(34p 전문·1867줄) · `V1010_P1_code-audit_RESULT.md` · `broadening_w_design.md` · `ORIGIN_VERDICT.md` 전문 정독 완료.  
> **날짜**: 2026-07-01  
> **범위**: 드래프트 문건 산출 전용 — 코드·tex·기존 결과 수정 0.

---

## ★ 산출물 1 — Ch1 ↔ 코드 coverage 매트릭스

### 1-A. 노드별 Ch1 절 ↔ 코드 step 전면 매핑

아래 표는 P1 맵(§1)의 24심볼·코드 step을 Ch1의 절·식 번호로 대응시키고, 누락(Ch1에 있으나 코드 미반영)과 과잉(코드에 있으나 Ch1 미설명)을 명시한다.

| 코드 노드 | 코드 식별자 (줄) | Ch1 절 | Ch1 식 번호 | 커버리지 | 비고 |
|---|---|---|---|---|---|
| **N0** | `curve`, `_direction_to_sigma` (L483-524) | §1 (N0) | eq:n0map | ✔ 완전 | 방향 부호 σ_d · |I|=c_rate·Q_cell |
| **N1** | `dqdv` L408 (V_n = V_app − σ_d|I|R_n) | §2 (N1) | eq:vn | ✔ 완전 | 유도 (a)→(d) + 작업격자 eq:vwork 포함 |
| **N1 작업격자** | L410-425 V_work linspace · T_work interp | §2.2 | eq:vwork | ✔ 완전 | padding p=0.15·n_work_min=2048 |
| **N2** | `func_U_j` (L78-79) · `dqdv` L434 | §3, §3.1, §3.2 | eq:Uj, eq:gibbsdef, eq:mudef, eq:eqcond | ✔ 완전 | Gibbs→μ→전기화학 평형→U_j(T) 전 유도 |
| **N2-LCO** | 동일 `func_U_j` | §3.3 (LCO center) | eq:lco-dUdT | ✔ 완전 | ∂U/∂T=ΔS_cat/F 부호 검산 포함 |
| **N3 gap** | `func_dU_hys` (L133-140) | §4.1, §4.2 | eq:mu, eq:gxi, eq:gpp, eq:spinodal, eq:hyssub, eq:hysdiff, eq:dUhys | ✔ 완전 | 격자기체→μ(θ)→g''=0→spinodal→ΔU_hys 전 유도 |
| **N3 branch** | `func_U_branch` (L143-148), `dqdv` L447 | §4.3 | eq:hyssym, eq:Ubranch, eq:center | ✔ 완전 | 대칭(식:hyssym) + 분기 중심 박스 |
| **N3 LCO** | 동일 func_U_branch | §4.4 (LCO hys) | eq:dUhys, eq:Ubranch (재사용) | ✔ 완전 | order-disorder T2·T3 + MIT T1 구조 설명 |
| **N4** | `_n_factor` (L272-278) · `_width` (L281-284) · `func_w` (L74-75) | §5.1 | eq:wbase | ✔ 완전 | n:1→w:폴백 inert 함정 명시('n' 우선순위·P1 F1) |
| **N4 이중지위** | 동일 (w 값은 공통 eq:wbase) | §5.1 (★폭 이중지위) | eq:wbase | ✔ 완전 | 단상=평형예측 / 두-상=현상학적 피팅 폭 분리 |
| **N5 logistic** | `func_ksi_eq` (L94-97) | §5.2 | eq:bv, eq:db, eq:logisticsolve, eq:xieq | ✔ 완전 | Eyring→detailed balance→logistic 전 유도 |
| **N5+ 분포관점** | (코드 항 없음, 통계역학 설명) | §5.3 (sec:dist) | eq:partfn, eq:fermifn | ✔ 보조 | grand-canonical 단일 자리 = ξ_eq 정체 규명 |
| **N5+ LCO 전자엔트로피** | (코드 P4 예고, 현재 미구현) | §6 (sec:lco-electronic) | eq:fd, eq:Se, eq:dSe, eq:dSemolar, eq:ggate, eq:dSegate | ★ **누락** (코드 미구현) | Fermi-Dirac→Sommerfeld→MIT-logistic 게이트. P4 plug-in 예고 |
| **N6** | `equilibrium` (L350-367) · `dqdv` L462-464 inline | §7 (sec:eqpeak) | eq:belliden, eq:eqpeak | ✔ 완전 | 보존식 미분→종 항등식→peak 박스 |
| **N6 LCO peak** | 동일 `equilibrium` 구조 | §7.1 (sec:lco-peak) | eq:eqpeak (재사용) | ✔ 완전 | 양극 영역 3봉우리 T1·T2·T3 |
| **N6 broadening** | (코드 항 없음, 설명만) | §7.2 (sec:broadening) | eq:ensavg | ✔ 완전 | 세 출처 ①동역학 ②내재폭 ③앙상블 η 분포; 역산 금지 |
| **N7 컷** | `_resolve_lag_length` L331 (A=min) | §8.2 (sec:lag) | eq:Acut | ✔ 완전 | z_cut=4.357 미분5%컷 + A_cap 상한 + 방향부호 분리 |
| **N7 χ_d** | `func_chi_d` (L158-163) · `_chi_and_dH_eff` (L293-300) | §8.3 | eq:chid | ✔ 완전 | 합-1 제약 유도 |
| **N7 ΔH_eff** | `func_dH_a_eff` (L152-155) | §8.3 | eq:dHeff | ✔ 완전 | 깊은 꼬리 Ω 흡수 |
| **N7 L_q** | `func_L_q` (L100-107) | §8.4 | eq:kuniv, eq:Lq, eq:Lqmid2, eq:Lqfull | ✔ 완전 | 운동방정식→L_q→T_* 묶기 전 유도 |
| **N7 L_V** | `_resolve_lag_length` L347 | §8.4 | eq:LV | ✔ 완전 | |dV/dq|_qa 환산 + 운영미분=0 설명 |
| **N8 저역통과** | `_causal_lowpass` (L110-128) | §9.1 | eq:intfactor, eq:memory, eq:lowpass | ✔ 완전 | 적분인자 ODE 해→지수기억→IIR 이산형 |
| **N8 peak shape** | `dqdv` L475 peak_shape=(ξ_eq−ξ_lag)/L_V | §9.2 | eq:peakshape, eq:branch | ✔ 완전 | 0/0 극한 논증 + 분기 스위치 D-PEAK2 포함 |
| **N8 충전 역전** | `dqdv` L473 ([::-1]...[::-1]) | §9.3 | eq:reversal | ✔ 완전 | 인과 방향 증명·방전 거울 |
| **N9** | `dqdv` L477 dqdv_work += Q·peak_shape · np.interp | §10 (sec:sum) | eq:sum | ✔ 완전 | 선형 합산 + 역보간 |
| **초기값 표** | `GRAPHITE_STAGING_LIT` (L531-560) | §10.1 + tab:staging | (표) | ✔ 완전 | 4전이 초기값·의미 |
| **LCO ΔS 분해** | (코드 P4 plug-in 예고) | §10.2 (sec:lco-decomp) | eq:lco-decomp | ★ **누락** (코드 미구현) | config+vib+elec 3성분 가산성 직교성 증명·이중계산금지 |
| **LCO 코드 일반화** | (코드 P4 예고) | §10.3 (sec:lco-code) | eq:msmr (MSMR 동형) | ★ **누락** (코드 미구현) | MSMR 동형·방향인자 f=−σ_d 대응·전이dict 교체 |
| **부호 검산** | (코드 self-test L567-703) | §11 (sec:signcheck) | S1~S8 + R1~R5 | ✔ 완전 | 8항 정성 + 5항 수치 회귀 |

### 1-B. 누락(Ch1 기술·코드 미구현) 항목

| 항목 | Ch1 위치 | 코드 상태 | 중요도 |
|---|---|---|---|
| **LCO 전자 엔트로피 ΔS_e** | §6 전체 (eq:Se·eq:dSe·eq:dSemolar·eq:ggate·eq:dSegate) | 미구현 (P4 예고) | HIGH — MIT T1 재현 필수 |
| **LCO ΔS 분해 plug-in** | §10.2 eq:lco-decomp | 미구현 (P4) | HIGH |
| **MSMR 동형 코드 일반화** | §10.3 eq:msmr | 미구현 (P4) | HIGH |
| **`equilibrium`의 배열 T(V) 미지원** | §2.2 (V_work 설계) | [확정] T 스칼라 전용 (P1 보완2) | MEDIUM — 비등온 기준선 |
| **n_work 해상도 의존 꼬리 분기** | §9.2 eq:branch | [확정] (P1 보완3) | LOW — 피팅 시 주의 |
| **면적=Q assert 부재** | §7 eq:eqpeak (면적=Q 이론 확정) | self-test assert 없음 (P1 보완4) | LOW |

### 1-C. 과잉(코드에 있으나 Ch1 미서술/경고) 항목

| 항목 | 코드 위치 | Ch1 서술 | 비고 |
|---|---|---|---|
| **死코드 `func_U_j_hys`** | L82-91 | §4 에 역할 언급 없음 (P1 §2-D) | 호출 0·면적 무영향·원형보존 동결 |
| **`dVdq_qa` 누락 silent off** | L346-347 | §8.4 각주 수준 언급 없음 | P1 F2: 동역학 전이 schema 필수 경고 |
| **'n' 우선순위 → 'w' 폴백 inert** | L272-278 | §5.1 이중지위에서 암묵 언급만 | P1 §2-D `_n_factor` 함정 |
| **`chi_split` custom rule** | L161-162 | §8.3 eq:chid 서술에서 언급 없음 | self-test L628-635로만 실증 |

---

## ★ 산출물 2 — 누락 유도·다리 보완

### 2-A. 코드 노드 사슬에서 미완성이었던 다리들과 현재 Ch1 상태

아래 보완은 v3~v9가 덜어냈거나 단계가 뛰어진 세 곳의 식→식 다리를 v1.0.10 Ch1이 이미 완성한 방식을 확인·정리하고, 추가 보완이 필요한 gap을 명시한다.

#### 2-A-1. g(ξ) 이중웰 → spinodal → ΔU_hys 닫힌식 (N3 유도 체인)

**이전 버전 gap**: v3~v7은 spinodal 조건을 결과식으로만 주었고 g''(ξ)=0의 근의 공식 경로가 없었다.

**v1.0.10 Ch1 완성 상태** (§4.1-4.2, eq:gxi→eq:gpp→eq:spinodal→eq:hyssub→eq:hysdiff→eq:dUhys):

1. **출발**: 격자기체 자리당 자유에너지  
   g_j(ξ) = g_j^0 + RT[ξ ln ξ + (1−ξ)ln(1−ξ)] + Ω_j ξ(1−ξ)

2. **1계·2계 미분**:  
   g_j'(ξ) = RT ln[ξ/(1−ξ)] + Ω_j(1−2ξ)  
   g_j''(ξ) = RT/[ξ(1−ξ)] − 2Ω_j

3. **spinodal 조건 g''=0**:  
   ξ^2 − ξ + RT/(2Ω_j) = 0  
   ξ_s^± = ½(1 ± u_j),  u_j = √(1 − 2RT/Ω_j)  [Ω_j > 2RT]

4. **두 spinodal 전위 차** (eq:hyssub → eq:hysdiff):  
   logit 인자: ξ_s^±에서 ξ/(1−ξ) = (1±u)/(1∓u) → 두 끝 역수  
   (1−2ξ) 인자: ±u  
   ΔU_hys = V_eq(ξ_s^−) − V_eq(ξ_s^+)  
            = (RT/F)[ln((1−u)/(1+u)) − ln((1+u)/(1−u))] + (Ω/F)[u−(−u)]  
            = −(4RT/F)·artanh u + (2Ω/F)·u

5. **박스** (eq:dUhys):  
   ΔU_j^hys = (2/F)[Ω_j·u_j − 2RT·artanh u_j],  u_j = √(1−2RT/Ω_j)

6. **연속성 검산**: Ω→2RT^+에서 u→0, Taylor artanh u ≈ u+u³/3+…  
   → ΔU_hys → (8RT/3F)u_j^3 → 0  (임계온도에서 매끄럽게 소멸)

**평가**: 유도 완비. 추가 보완 불요.

---

#### 2-A-2. Eyring 속도식 → detailed balance → logistic → ξ_eq 유도 (N5 체인)

**이전 버전 gap**: v5 이전은 logistic을 결과식으로만 제시했고 detailed balance에서 유도하는 경로가 없었다.

**v1.0.10 Ch1 완성 상태** (§5.2, eq:bv→eq:db→eq:logisticsolve→eq:xieq):

1. **출발** (Eyring, eq:bv):  
   정방향 장벽 ΔG_a − χ A_j, 역방향 ΔG_a + (1−χ)A_j  
   r^+ = k_0 exp[−(ΔG_a − χ A_j)/RT]  
   r^− = k_0 exp[−(ΔG_a + (1−χ)A_j)/RT]

2. **비를 취하면** (eq:db):  
   r^+/r^− = exp[χ A_j/RT + (1−χ)A_j/RT] = exp[A_j/RT]  
   — χ+(1−χ)=1 합-1이 χ를 소거 → Boltzmann비 = detailed balance

3. **운동방정식 정지점** (eq:logisticsolve):  
   r^+(1−ξ_eq) = r^−ξ_eq  
   → ξ_eq/(1−ξ_eq) = r^+/r^− = exp[sF(V_n−U_j)/RT]  
   → ξ_eq = 1/(1+exp[−sF(V_n−U_j)/RT])

4. **폭 다중도·방향 부호 일반화** (eq:xieq):  
   w_j = n_j RT/F 로 묶고 U_j^d(분기 중심)로 일반화  
   ξ_eq,j(V,T) = 1/(1+exp[−σ_d(V−U_j^d)/w_j])

**grand-canonical 다리** (§5.3, eq:partfn→eq:fermifn): 단일 자리 분배함수 Z=1+exp(−βΔμ) → 평균 점유 <n> = 1/(1+exp(+βΔμ))가 ξ_eq와 동일식 — 흑연 Li 자리 점유 분포 = Fermi-Dirac형.

**평가**: 유도 완비. v9 보완 결과 그대로 유지됨.

---

#### 2-A-3. 운동방정식 → L_q → L_V 체인 (N7 완전 유도)

**이전 버전 gap**: v3~v6은 L_V를 현상학적 파라미터로만 두었고 Arrhenius 장벽에서 유도하는 경로가 없었다.

**v1.0.10 Ch1 완성 상태** (§8.1-8.4, eq:Lq→eq:kuniv→eq:Lqmid2→eq:Lqfull→eq:LV):

1. **출발** — 운동방정식을 용량축으로 (eq:Lq):  
   dξ_j/dt = k_j(ξ_eq,j − ξ_j), 정전류 dq/dt=|I|/Q_cell로 나누면  
   dr_j/dq = dξ_eq,j/dq − r_j/L_q,j,  **L_q,j = |I|/(Q_cell·k_j)**

2. **k_j 전개** (eq:kuniv):  
   k_j = r^+(1+exp[−A_j/RT]),  r^+ ≈ k_0 exp[−(ΔG_a^eff−χ_d A)/RT]

3. **T_* 묶기** (eq:Lqfull):  
   L_q,j = (T_*/T) · exp[(ΔH_a^eff − T ΔS_a)/RT] / (1+exp[−A/RT]) · exp[−χ_d A/RT]  
   T_* ≡ |I|h/(Q_cell k_B)

4. **전압축 환산** (eq:LV):  
   L_V,j = |dV/dq|_{q_a} · L_q,j

**컷 affinity 동결 논리** (§8.4 말미): A = min(z_cut·n_j·RT, A_cap·RT)가 전이당 상수 → 운영상 ∂ln L_q/∂V = 0 (한 스칼라). 부등식 ∂ln L_q/∂V < 0은 국소 구동력으로 두면 V↑→A↑→유효장벽↓→L_q↓라는 컷 규칙의 *물리적 동기*로만 성립(운영 미분과 물리 단조성이 일관, 자기모순 0).

**평가**: 유도 완비. v8에서 도입된 D-PEAK/D-PEAK2·D-WEFF 4핵심이 모두 반영됨.

---

#### 2-A-4. 인과 기억 ODE → 이산 저역통과 → peak shape (N8 체인)

**이전 버전 gap**: v3~v5는 IIR 점화식을 근거 없이 직접 제시했고 연속해에서 이산화하는 경로가 없었다.

**v1.0.10 Ch1 완성 상태** (§9.1-9.3, eq:intfactor→eq:memory→eq:lowpass→eq:peakshape→eq:reversal):

1. **적분인자법** (eq:intfactor→eq:memory):  
   1계 선형 ODE에 적분인자 exp(q/L_q) 적용 →  
   r_j(q) = r_j(q_0)exp[−(q−q_0)/L_q] + ∫_{q_0}^q exp[−(q−q')/L_q]·(dξ_eq/dq') dq'

2. **이산 격자** (eq:lowpass):  
   감쇠 ρ = exp(−Δ_grid/L_V) → 점화식  
   ξ_lag,i = ρ·ξ_lag,i−1 + (1−ρ)·ξ_eq,i  
   (DC gain = [1−ρ]/[1,−ρ]: 계수합 = 1 → 면적 보존)

3. **peak shape** (eq:peakshape):  
   peak_shape = (ξ_eq − ξ_lag)/L_V

4. **분기 스위치 D-PEAK2** (eq:branch):  
   L_V < ν·Δ_grid → 평형 종 eq:eqpeak 직접 (0/0 극한 회피)

5. **충전 격자 역전** (eq:reversal):  
   충전(σ_d<0): ξ_lag = lowpass(ξ_eq[::-1])[::-1]

**평가**: 유도 완비.

---

#### 2-A-5. ★ 남은 Gap — LCO 전자 엔트로피 유도 (Ch1에 있으나 코드 미구현·P4 예고)

이 gap은 "Ch1에 유도가 완비"되었으나 "코드에 아직 없다"는 점에서 나머지와 성격이 다르다. coverage 매트릭스(1-B)에서 HIGH 누락으로 표시된 항목이며, 아래 2-A-5는 그 유도가 Ch1에서 어떻게 닫혔는지를 확인·정리하는 것이다 (코드 구현은 P4).

**Ch1 §6 완성 상태 요약** (eq:fd→eq:Se→eq:dSe→eq:dSemolar→eq:ggate→eq:dSegate):

1. Fermi-Dirac → Sommerfeld 전개 → 전자 비열 C_e = (π²/3)k_B²T·g(E_F)  
2. S_e 적분: C_e/T가 T'무관 → **S_e(T,x) = (π²/3)k_B²T·g(E_F,x)**  
3. 삽입 기준 전이 엔트로피: ΔS_e,j = ∂S_e/∂x|_T = (π²/3)k_B²T·∂g/∂x  
4. 몰당 환산 (N_A 곱하기): ΔS_e,j^mol = (π²/3)R·k_B·T·∂g/∂x  [J/(mol·K)]  
5. MIT-logistic 게이트: g(E_F,x) ≈ g_max[1−σ((x−x_MIT)/Δx_MIT)]  
6. 닫힌식: ΔS_e,j(x,T) = −(π²/3)k_B²T·(g_max/Δx_MIT)·σ(1−σ) < 0

**신뢰 등급 분리**:
- 함수형 S_e = (π²/3)k_B²T·g(E_F): tier A (Sommerfeld 표준)
- anchor g_max ≈ 13 e/eV/atom (CoO₂, x=0): tier A 단일점 [Motohashi 2009]
- 연속 곡선 g(E_F,x): 1차 문헌 부재(갭 G2) → logistic 게이트로 모델 가정·피팅 위임

**코드 plug-in 명세** (P4용):
- 위치: T1 전이 dict의 ΔS_rxn 평가 시 ΔS_e,j^mol을 더하는 한 줄
- 단위 주의: 자리당 식eq:dSe (k_B² 차원) → 몰당 식eq:dSemolar (R·k_B 차원, N_A 배)
- 피팅 인자: (g_max, x_MIT, Δx_MIT) 3개, 초기값 (13 e/eV, 0.85, 0.05)

---

### 2-B. v3~v9 교과서 요소 통합 확인

| v3~v9 요소 | v1.0.10 Ch1 포함 여부 | 위치 |
|---|---|---|
| 격자기체 자유에너지 g(ξ)·Stirling 근사 | ✔ | §4.1 eq:gxi |
| spinodal 이중웰 그림 | ✔ | fig:doublewell |
| detailed balance χ+(1-χ)=1 | ✔ | §5.2 eq:db |
| grand-canonical 분포 관점 (Fermi-함수형 ξ_eq) | ✔ | §5.3 eq:partfn·eq:fermifn |
| 인과 기억 일반해 (적분인자법) | ✔ | §9.1 eq:memory |
| DC gain=1 면적보존 (IIR 계수 합) | ✔ | §9.1 eq:lowpass + P1 §0 |
| broadening 세 출처 (동역학·내재·앙상블 η) | ✔ | §7.2 sec:broadening |
| LCO Fermi-Dirac→Sommerfeld 유도 | ✔ | §6 전체 |
| MSMR 동형 (f=−σ_d 대응) | ✔ | §10.3 eq:msmr |
| 부호 S1~S8 전수 검산 + 수치 R1~R5 | ✔ | §11 |

---

## ★ 산출물 3 — LCO 이론 정련

### 3-A. v9 LCO 타당성 — 코드 정합·교재급 검토

#### 3-A-1. LCO 전이 초기값 타당성 (tab:lco-staging)

| 전이 | U_j [V] | 성격 | Ω_j 상태 | ΔS_rxn^cat 초기값 | 문헌 tier |
|---|---|---|---|---|---|
| T1 (MIT) | ~3.90 | 절연체→금속, 2상역 x≈0.75–0.94 | >2RT (두-상) | config+ΔS_e 게이트 ON | A (Menetrier 1999, Reimers 1992) |
| T2 (order-disorder a) | ~4.05 | hex→monoclinic, x≈0.55 | >2RT (두-상) | config 주도 ≈+0.47 J/(K·mol) | A (Motohashi 2009) |
| T3 (order-disorder b) | ~4.17–4.20 | monoclinic→hex, x≈0.48 | >2RT (두-상) | config ≈+1.49 J/(K·mol) | A (Motohashi 2009) |

**3개 전이 모두 Ω_j>2RT (두-상)**: §5.1 이중지위에서 세 전이의 폭 w_j도 "현상학적 자유 피팅 폭"으로 읽혀야 한다. 흑연 2L→2·2→1 두 전이와 동일한 논리 적용.

**도핑 보정 (Al³⁺/Mg²⁺)**: §4.4(sec:lco-hys)에서 Ω_j를 2RT 쪽으로 낮춰 spinodal gap·히스가 줄고 broadening이 커진다고 명시 — 코드에서는 Ω_j 초기값을 낮게 두거나 γ_j를 줄여 구현.

#### 3-A-2. ΔS_rxn 부호·크기 교재급 검산

**대표 단전극 엔트로피 계수** ∂φ/∂T ≈ +0.83 mV/K (Swiderska-Mocek 2019, LCO 단전극 vs Li, tier B):

ΔS_rxn^cat = F · ∂U/∂T = 96485 C/mol × 0.83×10⁻³ V/K ≈ **+80 J/(mol·K)**  

이 값은 삽입 기준(x↑) 전체 엔트로피 계수의 대표 스케일이다.

**전자항과의 공존 (T1)**:
- 전자항: |ΔS_e,j| ≈ 0.18 k_B/atom × N_A ≈ 1.5 J/(mol·K) (작지만 음, MIT 국소)
- 전체 합: +80 + (−1.5) ≈ +78.5 J/(mol·K) > 0 → 총 부호 불변
- 결론: 전자항은 음의 소수 보정이며 총 엔트로피 계수 부호를 바꾸지 않는다

**구성 성분 층위 주의**: config 항(표 tab:lco-staging의 ≈+0.47 J/(K·mol))은 전이별 "부분몰 성분"이고, +80은 "단전극 전체 계수"의 대표 스케일 — 서로 다른 층위의 양이다. 전이별 정밀값 ≠ 전체 계수 스케일.

#### 3-A-3. 코드 정합 확인 (N2 · N5 · N5+)

- N2 `func_U_j(T, dH_rxn, dS_rxn)`: LCO도 흑연과 동일 식 (−ΔH_rxn+T·ΔS_rxn)/F — 단 값만 양극 영역으로 교체. **정합 ✔**
- N5 `func_ksi_eq`: 방향 부호 σ_d 규약 — LCO에서 방전(σ_d=+1)은 리튬화(x↑), 충전(σ_d=−1)은 탈리튬화(x↓). 흑연과 σ_d 규약 1:1 대칭. **정합 ✔**
- N5+ 전자 엔트로피 항: **현재 미구현** (P4). forward 슬롯 ΔS_rxn,j에 ΔS_e,j^mol을 더하는 한 줄만 필요.

---

### 3-B. LCO 양극 dQ/dV 분석 — 교재급 서술

#### 3-B-1. 흑연과 LCO 비교 요약표

| 항목 | 흑연 음극 | LCO 양극 |
|---|---|---|
| 전위 범위 | ~0.085–0.21 V vs Li/Li⁺ | ~3.90–4.20 V vs Li/Li⁺ |
| 전이 개수 | 4 (staging 4→3·3→2L·2L→2·2→1) | 3 (T1 MIT + T2·T3 order-disorder) |
| 삽입 방향 | 방전 = 탈리튬화 (ξ: 0→1) | 방전 = 리튬화 (x↑), 충전 = 탈리튬화 |
| 두-상 전이 | 2L→2(LiC₁₂)·2→1(LiC₆) 2개만 | T1·T2·T3 전부 (Ω>2RT) |
| 전자 엔트로피 | 무시 (ΔS_e≈0, 전도성 변화 미미) | T1 MIT에서 필수 (g(E_F): 0→13 e/eV) |
| ΔS_rxn 성분 | config+vib | config+vib+electronic (T1만) |
| ΔS_rxn 부호·크기 | 전이별 +29/0/−5/−16 J/(mol·K) | 대표 스케일 ≈+80 J/(mol·K) (단전극) |
| 폭 w_j 지위 | 2개=두-상(현상학적), 2개=단상(평형예측) | 3개 전부=두-상(현상학적) |
| 도핑 보정 | 해당 없음 | Al³⁺/Mg²⁺: Ω↓ → spinodal gap 감소·broadening 증가 |

#### 3-B-2. dQ/dV 곡선 특징 (교재급 분석)

**T1 (MIT, ~3.90 V)**:
- 2상 plateau → spinodal gap에 의한 히스테리시스 분기 (eq:dUhys·eq:Ubranch)
- 전자 엔트로피 기여: ΔS_e,j ∝ T → ∂U_1/∂T의 기울기 자체가 T에 비례 → 위치 이동은 ∝T²
- 관측 신호: "다온도 dQ/dV에서 T1 봉우리의 온도 이동률이 T에 선형으로 증가"가 전자항의 식별 신호

**T2·T3 (order-disorder, ~4.05·~4.17 V)**:
- monoclinic 초격자 정렬: Ω>2RT의 상분리 → 좁은 한 쌍 peak
- T2와 T3는 hex↔monoclinic의 전방·역방향이라 거의 같은 조성(x≈0.55)에 2개 peak
- ΔS config 주도: 정렬(order) 엔트로피 변화가 U_j(T) 온도 이동을 결정

**도핑 LCO (우리 시료 Al/Mg 치환)**:
- Ω↓ → spinodal gap·히스 감소 → peak smear + U_j 미세 shift
- 피팅 관점: pure-LCO Ω_j가 초기값, 도핑 폭·shift는 데이터 피팅으로 정함

#### 3-B-3. Sommerfeld 전자 엔트로피 — 교재급 유도 요약

**물리 전제**: LiCoO₂(x=1)에서 Co³⁺(t₂g⁶ low-spin, 닫힌껍질) → 전기 절연체 (g(E_F)≈0).  
x↓로 Co⁴⁺ 정공 → t₂g 띠 전도 전자 → 금속 (g(E_F)→유한).  
MIT 범위: x≈0.75–0.94 [Menetrier 1999, Reimers 1992], tier A.

**단계별 유도 (§6)**:

1. 전도 전자 Fermi-Dirac 분포: f(E) = 1/(1+exp[(E−E_F)/k_BT])  
   — §5.3의 ξ_eq(리튬 자리 점유)와 수학적으로 동형: "입자 0/1 배타 점유"

2. Sommerfeld 근사 (g(E)≈g(E_F) in ±k_BT창):  
   C_e = ∂U_e/∂T = (π²/3)k_B²T·g(E_F)  [T-선형 전자 비열]

3. S_e = ∫₀ᵀ (C_e/T')dT' = (π²/3)k_B²T·g(E_F)  [T-선형]

4. 삽입 기준 전이당: ΔS_e,j = ∂S_e/∂x|_T = (π²/3)k_B²T·∂g/∂x

5. 몰당 (N_A 환산): ΔS_e,j^mol = (π²/3)R·k_B·T·∂g/∂x  [J/(mol·K)]

6. MIT-logistic 게이트 (모델 가정, 이유 4가지):  
   g(E_F,x) ≈ g_max[1−σ((x−x_MIT)/Δx_MIT)]  
   — σ'=σ(1−σ) 항등식(eq:belliden과 동일)으로 미분 닫힘:  
   ΔS_e,j = −(π²/3)k_B²T·(g_max/Δx_MIT)·σ(1−σ) < 0

**T-의존성 비교**:
- config·vib ΔS_rxn: T에 독립 (상수)
- 전자항 ΔS_e ∝ T: ∂U_j/∂T|_e = ΔS_e/F ∝ T  
  → ∂U_j/∂T가 T에 선형 → U_j 이동 ∝ T² (선형 아님)
- 피팅 식별: 다온도 데이터에서 전자항만 이 T-의존성을 보임

**크기 검산**:
- 완전 금속 한계: S_e/k_B = (π²/3)(k_BT)·g(E_F) = 3.29×0.026 eV × 13 eV⁻¹ ≈ 1.1 k_B/atom (T=300K)
- O3 영역 부분몰 차: ≈0.18 k_B/atom [Reynier 2004, tier B]
- 결론: config의 O3 ΔS(>½ 지배)보다 작으나, MIT 구간에만 켜지는 게이트라 config 단독으로 MIT 재현 불가 [ml2024, tier A]

#### 3-B-4. MSMR 동형 — LCO 코드 일반화 정당화

MSMR (multiphase species reaction) 모델 [Paul et al. 2024]:  
x_j = X_j / (1+exp[f(U−U_j^0)/ω_j])

Ch1 식eq:xieq와 1:1 대응:
- 용량 가중: X_j ↔ Q_j
- 중심: U_j^0 ↔ U_j^d
- 폭: ω_j ↔ w_j
- **방향 인자**: f ↔ −σ_d  (MSMR의 지수 +f(U−U^0) = Ch1의 지수 −σ_d(V−U^d))

이 동형이 "같은 forward 코드가 구조 변경 0으로 LCO에 적용된다"는 근거다. 바뀌는 것은:
1. 전이 파라미터 교체: GRAPHITE_STAGING_LIT → LCO_STAGING_LIT
2. T1 전이 ΔS_rxn에 ΔS_e,j^mol 한 줄 추가 (P4)

---

### 3-C. 코드 ↔ 이론 정합 추가 확인 항목

| 검증 항목 | 이론 결과 | 코드 구현 | 정합 |
|---|---|---|---|
| U_j(T) 온도선형 | ∂U_j/∂T = ΔS_rxn/F (eq:lco-dUdT) | func_U_j: (−dH_rxn+T·dS_rxn)/F | ✔ |
| 전자항 T-의존 | ΔS_e ∝ T → ∂U_1/∂T ∝ T | 미구현 (P4) | ★ 누락 |
| 양극 히스 분기 | 동일 eq:dUhys·eq:Ubranch | func_dU_hys·func_U_branch | ✔ (값만 교체) |
| 두-상 폭 지위 | T1·T2·T3 전부 현상학적 피팅 폭 | w_j = n_j·RT/F (동일 식, 초기값만 교체) | ✔ |
| 전셀 합성 배제 | "하프셀 범위, 단전극 부호만" (§1.1) | 코드도 단전극 (no full-cell) | ✔ |
| N_A 단위 환산 | ΔS_e,j^mol = N_A·ΔS_e,j | P4 plug-in 시 ×N_A 필수 | ★ 주의 (누락 시 10²³배 과소) |

---

## 부록 — 주요 식 색인 (S2 참조용)

| 식 번호 | 내용 | 코드 식별자 |
|---|---|---|
| eq:n0map | σ_d, |I|=c_rate·Q_cell | curve, _direction_to_sigma |
| eq:vn | V_n = V_app − σ_d|I|R_n | dqdv L408 |
| eq:vwork | V_work linspace·패딩 | dqdv L415 |
| eq:gibbsdef·eq:mudef | G=H−TS, μ=∂G/∂n | (이론 기반) |
| eq:eqcond | ΔG_j=−sFU_j | (이론 기반) |
| eq:Uj | U_j(T)=(−ΔH_rxn+T·ΔS_rxn)/F | func_U_j L79 |
| eq:lco-dUdT | ∂U_j/∂T=ΔS_rxn^cat/F | func_U_j (동일, 값만 교체) |
| eq:gxi·eq:gpp | g_j(ξ) 격자기체 자유에너지·2계 미분 | (이론 기반) |
| eq:spinodal | ξ_s^± = ½(1±u_j), u_j=√(1−2RT/Ω_j) | func_dU_hys L137·L138 |
| eq:dUhys | ΔU_j^hys = (2/F)[Ω_j·u_j−2RT·artanh u_j] | func_dU_hys L140 |
| eq:Ubranch | U_j^d = U_j + ½σ_d h_η γ_j ΔU_j^hys | func_U_branch L148 |
| eq:wbase | w_j = n_j RT/F | func_w L75 |
| eq:bv·eq:db | Eyring→detailed balance r^+/r^− = exp[A/RT] | (이론 기반) |
| eq:xieq | ξ_eq = 1/(1+exp[−σ_d(V−U^d)/w]) | func_ksi_eq L96-97 |
| eq:partfn·eq:fermifn | grand-canonical Z, <n>=Fermi함수 | (이론·ξ_eq 정체) |
| eq:fd·eq:Se·eq:dSe | Fermi-Dirac→Sommerfeld→ΔS_e | (Ch1 §6, 코드 P4) |
| eq:dSemolar·eq:ggate·eq:dSegate | 몰당 환산·MIT게이트·닫힌식 | (Ch1 §6, 코드 P4) |
| eq:belliden | dξ_eq/dz = ξ_eq(1−ξ_eq) (종 항등식) | dqdv L464 |
| eq:eqpeak | (dQ/dV)^eq_j = Q_j·ξ_eq(1−ξ_eq)/w_j | equilibrium L366·dqdv L464 |
| eq:ensavg | 앙상블 forward 평균 (eq:ensavg) | (설명, 모델 항 0) |
| eq:Acut | A = min(z_cut·n_j·RT, A_cap·RT) | _resolve_lag_length L331 |
| eq:chid | χ_d: 방전 χ / 충전 1−χ | func_chi_d L163 |
| eq:dHeff | ΔH_a^eff = ΔH_a − χ_d·Ω_j | func_dH_a_eff L155 |
| eq:Lq·eq:Lqfull | L_q=|I|/(Q_cell·k_j)·Arrhenius 전개 | func_L_q L100-107 |
| eq:LV | L_V = |dV/dq|_{q_a}·L_q | _resolve_lag_length L347 |
| eq:memory·eq:lowpass | ODE 적분인자해·IIR 점화식 | _causal_lowpass L110-128 |
| eq:peakshape·eq:branch | (ξ_eq−ξ_lag)/L_V · 분기 스위치 | dqdv L462-475 |
| eq:reversal | 충전 격자 역전 [::-1]…[::-1] | dqdv L473 |
| eq:sum | dQ/dV = C_bg + Σ Q_j[peak_shape_j] | dqdv L477·np.interp L479 |
| eq:lco-decomp | ΔS_rxn^cat = config+vib+electronic | (Ch1 §10.2, 코드 P4) |
| eq:msmr | MSMR 동형·f=−σ_d 대응 | func_ksi_eq (구조 동일) |

---

*작성: 2026-07-01 | S2 드래프트 | 범위: Ch1 coverage 매트릭스·누락 유도·LCO 이론 정련 | 코드·tex 수정 0*
