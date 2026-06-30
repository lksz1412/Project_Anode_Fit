# V1010 P3 — 챕터2(발열) 경쟁 드래프트 O2 (supplement)

> **역할**: P3 Ch2(가역 발열·엔트로피 통계열역학) 9종 경쟁 드래프트 중 **O2**(작업 sub). 본 문서 = Ch2 이론을 코드(`Anode_Fit_v1.0.10.py`)·Ch1과 정합시키는 **물리화학 교과서 정련 supplement**. 발열 *코드*는 P4 범위(코드에 q_rev/ΔS_e 부재 — P1 §2-E 확정), 본 P3는 발열 *이론*을 식→식 유도 깊이로 갈고닦는다.
> **입력 정독**: `docs/v1.0.10/graphite_ica_ch2_v1.0.10.tex`(751줄 전문) · `results/process/V1010_P1_code-audit_RESULT.md`(전문) · `docs/v1.0.10/graphite_ica_ch1_v1.0.10.tex`(1933줄 — N0~N9 골격·∂U/∂T=ΔS/F(eq:Uj)·Sommerfeld 전자엔트로피(sec:lco-Se)·config+vib+elec 분해(eq:lco-decomp)·broadening(sec:broadening)·staging 표 정독, 전자엔트로피·중심·분해 절 중점).
> **표기 등급**: [확정]=식·코드·Ch1 직접 줄근거 / [추정]=물리 추론(근거 명시) / [근거 미발견]=세 입력으로 못 짚음.
> **범위 보존**: 드래프트 *제안*만. tex/코드 수정 X. Ch2 범위(코인 하프셀 단독, 전셀 합성 범위 밖) 준수. 허위 attribution X.

---

## §0. 핵심 한 줄 (supplement 결론)

Ch2의 발열 사슬 `Z → ⟨n⟩ → S=−R∑p ln p → ∂U_oc/∂T = ΔS/F → Q̇_rev = −I·T·∂U_oc/∂T`는 부호·차원·극한 적대검산을 **전부 통과**하며, Ch1의 `∂U_j/∂T=ΔS_rxn,j/F`(eq:Uj 미분)·Sommerfeld 전자엔트로피(eq:Se)·config+vib+elec 분해(eq:lco-decomp)와 **모순 0**으로 맞물린다. 다만 (i) Ch2 서두 식 `Q̇_rev=−T·I·∂U/∂T·T·ΔS`로 적힌 *과제 지시문의 곱*은 차원이 깨지며 — 올바른 닫힌 사슬은 `−I·T·∂U/∂T = −(I·T/F)·ΔS`(T 한 번), Ch2 본문 eq:qrev은 이미 올바르다 — , (ii) Ch2의 ΔS↔Bernardi entropic coefficient 정합은 `ΔS_rxn,j ↔ F·∂U_j/∂T`로 1:1이되 *부호 규약 통일*(ΔS=+F·∂U_oc/∂T)을 srcbox가 명시적으로 못박아야 round-trip이 닫힌다. 아래 §1~§3이 식→식으로 전개한다.

---

## §1. ★ Ch2 ↔ 코드 / Ch1 정합 매트릭스

### 1-1. 통계열역학·가역발열 ↔ 엔트로피항·Ch1 (정합 축)

| Ch2 양 (절·식) | Ch1 대응 (줄·식) | 코드 대응 (P1 줄근거) | 정합 판정 |
|---|---|---|---|
| 점유 분포 `⟨n⟩=1/(1+e^{β(ε₀−μ)})` (eq:occ, §2.1) | `ξ_eq=logistic[σ_d(V−U)/w]` (sec:dist, eq:fermifn; Ch1 L881·L949 "Fermi-함수형") | `func_ksi_eq` (L94-97, overflow-safe) | **[확정]** 동형. Ch2 eq:occ = Ch1 ξ_eq의 통계역학적 기원(단일자리 2-상태 Z₁) |
| logistic 폭 `w=RT/F` (eq:logistic, §2.2) | `w=n_jRT/F` (eq:Uj 표기·sec:width) | `func_w` (L74-75); 코드 `n_j=1` 고정 → 실폭 RT/F≈25.7 mV (P1 §1.2·D4) | **[확정]** Ch2 `w=RT/F`는 n=1 한정. Ch2가 "n=1" 명시 안 함 → §1-3 결함 D-C1 |
| `∂U_oc/∂T = ΔS(x)/F` (서·eq:qrev) | `∂U_j/∂T = ΔS_rxn,j/F` (eq:Uj 미분, L453·L474) | `func_U_j=(−ΔH+TΔS)/F` (L78-79) | **[확정]** 동일 관계식. Ch2가 부분몰 config 항으로 x-의존 확장(eq:dVdT_config) |
| 부분몰 config `∂S_config/∂θ=−R ln[θ/(1−θ)]` (eq:dSconfig) | Nernst 로그항 `V(ξ)=U_j+(RT/F)ln[ξ/(1−ξ)]` (Ch1 sec:dist) | 코드엔 명시 분해 없음(평형 peak ξ(1−ξ)/w만, L366) | **[확정]** Ch2가 Ch1 w의 T-의존이 담은 config를 *분리*해 드러냄(파생 B) |
| 겹침 가중식 `∂U_oc/∂T=Σ Q_j g_j ΔS⁰_j/F / Σ Q_j g_j` (eq:weighted) | 합산식 `dQ/dV=C_bg+Σ Q_j ξ(1−ξ)/w` (eq:sum) | `equilibrium`/`dqdv` 합산 (L366·L477); `g_j=ξ(1−ξ)/w` = 평형 peak 핵 | **[확정]** g_j가 곧 국소 dQ/dV 봉우리 = 코드 peak 핵. 음함수 미분 닫힘 |
| vibrational `S_vib,k=k_B[(1+n)ln(1+n)−n ln n]` (eq:Svib_mode) | 고-x 음 baseline(staging 표 ΔS_rxn=−5,−16) | 코드: ΔS_rxn 슬롯에 흡수(L78, 별도 vib 항 X) | **[확정]** Ch2 vib = Ch1 음 baseline의 BE-분포 기원. 코드는 중심값 흡수 |
| electronic `S_e=(π²/3)k_B²T g(E_F)` (eq:Se) | **동일 식** Ch1 eq:Se (L971) | 코드: ΔS_e/Sommerfeld 부재(P1 §2-E [확정]) | **[확정]** Ch2 eq:Se ≡ Ch1 eq:Se byte-수준 동형. 코드 미구현 = P4 |
| 가역 발열 `Q̇_rev=−I·T·∂U_oc/∂T` (eq:qrev) | Ch1 범위 밖(서론·sec:lco-Se L1046 "Ch2의 가역 발열로 확장") | 코드: q_rev/TΔS/dT 부재(P1 §2-E [확정]) | **[확정]** Bernardi 출구는 Ch2 고유. Ch1이 명시적으로 Ch2에 위임 |

### 1-2. ΔS_rxn,j ↔ Bernardi entropic coefficient 정합 (요청 핵심)

Bernardi-Pawlikowski-Newman 에너지 수지(eq:qrev, bernardi1985)의 가역항은 셀 전위의 온도계수 `∂U_oc/∂T`로 닫힌다. 이를 *반응 엔트로피*로 환산하는 다리가 정합의 핵심이다 — Ch2 srcbox(L650-654)와 Ch1 eq:Uj 미분이 **같은 항등식의 두 끝**이다.

- **Ch1 (전위→엔트로피)**: 평형 중심 `U_j(T)=(−ΔH_rxn+TΔS_rxn)/F`(eq:Uj, L448)를 T로 미분 → `∂U_j/∂T = ΔS_rxn,j/F`(L453). 이는 Gibbs-Helmholtz `∂(ΔG)/∂T=−ΔS`와 `ΔG=−FU`(eq:eqcond)를 잇는다. **[확정]**
- **Ch2 (엔트로피→발열)**: 같은 관계를 부호 규약으로 통일 — `ΔS=−∂(ΔG)/∂T=+F·∂U_oc/∂T`(srcbox L651-653) → `Q̇_rev=−IT·∂U/∂T=−(IT/F)ΔS`(eq:qrev). **[확정]**
- **1:1 매핑 (entropic coefficient)**: 측정 Bernardi entropic coefficient `α≡∂U_oc/∂T [V/K]`와 반응 엔트로피는 `ΔS_rxn,j = F·α_j`(α를 봉우리 중심 ξ=½에서 읽으면 중심 표준값 ΔS⁰_j). Ch2 표 tab:ds의 `ΔS⁰_j=+29/0/−5/−16 J mol⁻¹K⁻¹`(L330-333)가 곧 `F×(∂U_j/∂T)|_center` = Ch1 staging 표(tab:staging L1673-1676)와 **동일 4값**. **[확정]** 두 표가 같은 양의 두 이름임.

> **★정합 단언 [확정]**: Ch2의 ΔS(x) 분해 `ΔS(x)=ΔS⁰_j + R ln[ξ/(1−ξ)] + δS_vib/e(x)`(warnbox L302-304)에서 첫 항 ΔS⁰_j가 정확히 Bernardi entropic coefficient의 *봉우리 중심값* F·α_j이고, 둘째 항이 봉우리 *내부* x-의존(α의 SOC 변화)이다. 곧 측정 α(x)의 비선형 = Ch2 세 분포가 자동 생성. Ch1 eq:lco-decomp(`ΔS_rxn,j^cat=ΔS^config+ΔS^vib+ΔS_e^mol`)의 세 성분이 Ch2의 세 분포(config 격자기체 / vib BE / elec FD)와 **1:1 동일 분류**(아래 §1-4 교차표).

### 1-3. ★ 누락·과잉·중복/모순

**(A) 코드 대비 — 과잉 아님, 의도적 develop (발열=P4)**

| Ch2 항목 | 코드 상태 (P1 근거) | 분류 |
|---|---|---|
| q_rev=−IT·∂U/∂T (eq:qrev) | **부재** (P1 §2-E [확정]: T 외생 입력, 발열항·dT/dt 결합 0) | **누락 아님 — 발열은 P4 코드개정 범위**. Ch2가 이론 선행 |
| ΔS_e Sommerfeld (eq:Se) | **부재** (P1 §2-E [확정]: ΔS_rxn·ΔS_a만, 전자 상태밀도 항 X) | 흑연 하프셀선 소수(Ch2 §3.2 "보정항") → 코드 정당 배제. LCO만 P4 plug-in |
| 부분몰 config 분리 R ln[ξ/(1−ξ)] | **암묵** (코드 ξ(1−ξ)/w가 w의 T-의존으로 자동 포함, 명시 분리 X) | 모순 아님 — Ch2가 코드의 *내재* 항을 해석적으로 드러냄(파생 A 수치검증, FD 일치) |
| 겹침 가중 음함수식 (eq:implicit, eq:weighted) | **암묵** (코드 합산 Σ Q_j ξ(1−ξ)/w가 음함수 해의 forward; 코드는 U_oc 직접 안 풂) | 정합 — Ch2가 코드 합산의 ∂/∂T를 해석적으로 닫음 |

**(B) Ch2 내부 — 정련 후보 (드래프트 제안, 본문 수정은 master)**

- **D-C1 [확정]**: Ch2 eq:logistic의 `w=RT/F`(L155)는 **n_j=1 한정**. Ch1 sec:width·코드 `func_w=n_jRT/F`(L74)는 n_j 일반. 코드 데이터셋이 n=1이라 *실값은* RT/F가 맞으나(P1 D4), Ch2가 "w=RT/F"를 무조건으로 적으면 다중도 n_j≠1 전이에서 오독. **제안**: Ch2 eq:logistic에 "n_j=1 기준; 일반은 w=n_jRT/F(Ch1)" 1줄. (Ch2 §4.1 종합식 g_j=ξ(1−ξ)/w_j는 이미 w_j로 일반표기 — 서두 eq:logistic만 RT/F 고정.)
- **D-C2 [확정]**: Ch2 서두(L84) `Q̇_rev=−I·T·∂U_oc/∂T=−(I·T/F)·ΔS(x)` 본문식은 **올바름**(T 한 번). 그러나 *과제 지시문*의 `q_rev=−T·I·∂U/∂T·T·ΔS`는 T가 두 번 곱해져 차원 깨짐 — 이는 지시문 축약 오타이지 Ch2 본문 결함 아님([근거 미발견]: tex 본문엔 그 곱 없음). **§2-3에서 식→식으로 검산해 본문이 옳음을 확정.**
- **D-C3 [추정]**: Ch2 eq:Svib_mode(`S_vib,k=k_B[(1+n)ln(1+n)−n ln n]`)는 *절대* vib 엔트로피. 발열에 들어가는 건 부분몰 ΔS_vib=∂S_vib/∂x(L370-372)인데 닫힌식 미제시(부호만: 고-x 음). **제안**: Ch2가 ΔS_vib 부분몰을 ∂n_k/∂x·∂S_vib/∂n_k로 한 줄 더 전개하면 config(닫힌식 보유)와 대칭. 근거: Ch1도 vib는 음 baseline 정성서술만(L1711) → 두 챕터 공통 공백, 정직 기술됨.

**(C) 모순 — 0건 [확정]**: 부호 규약(ΔS=+F·∂U_oc/∂T)·차원(아래 §2)·극한(§2-4) 전 축에서 Ch2↔Ch1↔코드 충돌 없음. Ch1 sec:lco-Se L1046이 "Ch2의 가역 발열로 확장"을 *명시 예고*하고 Ch2 bernardi1985 출구가 이를 받음 → 챕터 경계 정합 [확정].

### 1-4. 세 분포 ↔ Ch1 eq:lco-decomp 교차표 [확정]

| 자유도 | Ch2 분포 (절) | Ch2 엔트로피식 | Ch1 분해 성분 (eq:lco-decomp) | 발열 기여 부호 |
|---|---|---|---|---|
| Li 배열 | 격자기체 (§2,§3.1) | S_config=−R[θlnθ+(1−θ)ln(1−θ)] (eq:Sconfig) | ΔS^config (logistic w가 담음) | config 양 발산(저-x) → 흡열(방전) |
| 격자 진동 | Bose-Einstein (§4.1) | S_vib,k=k_B[(1+n)ln(1+n)−n ln n] (eq:Svib_mode) | ΔS^vib (음 baseline) | 고-x 음 → 발열(방전) |
| 전도 전자 | Fermi-Dirac (§4.2) | S_e=(π²/3)k_B²T g(E_F) (eq:Se) | ΔS_e^mol (MIT 게이트, ∝T) | 흑연 ≈0; LCO MIT만 |

> 세 분포가 Ch2(통계역학 기원)와 Ch1(분해 슬롯)에서 **동일 3분류**. 가역 발열 = 이 세 분포를 재배열하는 열(Ch2 eq:qrev 후속 서술 L656-657). [확정]

---

## §2. ★ 발열 이론 갈고닦기 (중점) — 식→식 유도와 적대검산

### 2-1. q_rev 유도 — Bernardi 수지에서 −I·T·∂U/∂T 까지 (식→식, 유도 깊이)

**(a) 출발 — 전지 셀 에너지 수지.** 등압 전지의 발열률은 전기 일과 엔탈피 변화의 차로 닫힌다. 단일 활물질 하프셀에서 Bernardi-Pawlikowski-Newman 일반 수지(bernardi1985)는

```
Q̇ = I(U_oc − V) − I·T·(∂U_oc/∂T)          (eq:qrev 좌변, Ch2 L643)
     └─ Q̇_irr ≥ 0 ──┘   └──── Q̇_rev ────┘
```

여기서 `I(U_oc−V)`는 과전압 소산(2법칙상 항상 발열; Ch1 동역학 꼬리·분극이 만드는 entropy production), 둘째 항이 가역열이다.

**(b) 연산 — 가역항을 반응 엔트로피로.** 평형 전위와 반응 Gibbs 에너지가 `ΔG=−FU_oc`(Ch1 eq:eqcond)로 묶이므로, Gibbs-Helmholtz 항등식 `ΔS=−∂(ΔG)/∂T`에 대입하면

```
ΔS = −∂(ΔG)/∂T = −∂(−FU_oc)/∂T = +F·(∂U_oc/∂T)        (★부호 규약 통일, Ch2 srcbox L651)
```

**(c) 중간식 — Q̇_rev에 역대입.** `∂U_oc/∂T = ΔS/F`를 가역항에 넣으면

```
Q̇_rev = −I·T·(∂U_oc/∂T) = −I·T·(ΔS/F) = −(I·T/F)·ΔS(x)    (T 정확히 한 번)
```

**(d) 박스 — 닫힌 발열식.**

```
┌─────────────────────────────────────────────────────────┐
│  Q̇_rev = −I·T·(∂U_oc/∂T) = −(I·T/F)·ΔS(x)               │   (Ch2 eq:qrev, L645)
└─────────────────────────────────────────────────────────┘
```

> **★유도 깊이 단언 [확정]**: 화살표 `Bernardi 수지 → ΔG=−FU → Gibbs-Helmholtz → ΔS=+F∂U/∂T → Q̇_rev=−(IT/F)ΔS` 4단계 모두 점프 없음. 각 단계가 Ch1 eq:eqcond·eq:Uj와 1:1. **지시문의 `−T·I·∂U/∂T·T·ΔS`(T 두 번)는 이 사슬 어디에도 없다** — (c)에서 ∂U/∂T를 ΔS/F로 *치환*하는 것이지 *곱하는* 게 아니다. T를 한 번만 곱한 본문 eq:qrev이 옳다(§2-2 차원검산이 확정).

### 2-2. 부호·차원 적대검산 (11행)

| # | 항/식 | 차원 검산 | 부호 검산 | 판정 |
|---|---|---|---|---|
| 1 | ∂U_oc/∂T | [V/K] = [V]/[K] | ΔS>0 → ∂U/∂T>0 (eq:Uj L453 정합) | ✅ |
| 2 | ΔS=F·∂U_oc/∂T | [C/mol]·[V/K]=[J/(mol·K)] | ✅ 엔트로피 차원 | ✅ |
| 3 | Q̇_rev=−I·T·∂U/∂T | [A]·[K]·[V/K]=[A·V]=[W] | 부호: 아래 4행 | ✅ 일률(W) |
| 4 | Q̇_rev=−(IT/F)ΔS | [A]·[K]·[J/(mol·K)]/[C/mol]=[A·J/C]=[A·V]=[W] | 두 형 차원 일치 | ✅ |
| 5 | **★지시문 곱 −T·I·∂U/∂T·T·ΔS** | [K]·[A]·[V/K]·[K]·[J/(mol·K)]=[W·K·J/(mol·K)] **≠[W]** | — | ❌ **차원 깨짐** → 지시문 오타 확정([근거 미발견] in tex) |
| 6 | 방전 I>0, ΔS>0 (저-x config) | — | Q̇_rev=−(IT/F)ΔS<0 → **흡열**(셀 열 흡수, Ch2 L659) | ✅ |
| 7 | 방전 I>0, ΔS<0 (고-x vib, 2→1) | — | Q̇_rev>0 → **발열**(Ch2 L662-663) | ✅ |
| 8 | S_config=−R[θlnθ+(1−θ)ln(1−θ)] | [J/(mol·K)] (R 차원) | θ∈(0,1)→ log<0→ −R·(음)>0 → S≥0 | ✅ S_config≥0 |
| 9 | ∂S_config/∂θ=−R ln[θ/(1−θ)] (eq:dSconfig) | [J/(mol·K)] | θ→0: ln→−∞ → +∞; θ→1: −∞ | ✅ 양끝 발산 |
| 10 | S_e=(π²/3)k_B²T g(E_F) (eq:Se) | k_B²·T·g = [J²/K²]·[K]·[1/J]=[J/K] 자리당; ×N_A→[J/(mol·K)] | g≥0, T≥0 → S_e≥0 | ✅ (Ch1 L987 동일) |
| 11 | Q̇_rev 충방전 대칭(가역) | — | I→−I (충↔방)서 Q̇_rev 부호반전 = 가역(한 사이클 상쇄) | ✅ eq:hys_rev 정합 |

> **적대 결론 [확정]**: 차원·부호 11행 전부 정합. **유일 결함은 지시문의 T-이중곱(#5)** — Ch2 본문 eq:qrev은 T 한 번으로 옳다. 흡/발열 교대(#6·#7)는 ΔS(x) 부호전환(저-x 양→고-x 음)이 직접 만들며 calorimetry 가역 발열 관측(standardised2024)과 정합.

### 2-3. ΔS ↔ q_rev 양방향 닫힘 (round-trip)

발열 산출의 실전 닫힘은 *측정 α(x)→ΔS→q_rev* 와 *분포→ΔS→α(x)* 두 방향이 일치해야 한다.

- **순방향 (분포→발열)**: 세 분포 합 `ΔS(x)=ΔS⁰_j+R ln[ξ/(1−ξ)]+δS_vib/e(x)` → `Q̇_rev=−(IT/F)ΔS(x)`. config 항이 봉우리 내부 x-의존을 자동 채움(Ch2 procedurebox step 5, L712). [확정]
- **역방향 (측정→ΔS)**: 다온도 dQ/dV 동시 피팅 → `U_j(T_k)` 회귀 → `ΔS⁰_j=F·dU_j/dT`(Ch2 procedurebox step 4, L710) → Allart tab:ds 대조. [확정]
- **닫힘 조건 [확정]**: 두 방향이 만나려면 부호 규약 `ΔS=+F·∂U_oc/∂T` *단일 채택*이 필수(Ch2 L653 "통일"). Ch1 eq:Uj 미분(`∂U_j/∂T=ΔS_rxn/F`)과 동부호 → round-trip 닫힘. **제안(드래프트)**: Ch2 procedurebox에 "step 4의 dU_j/dT 부호 = eq:qrev srcbox 규약과 동일" 한 줄 cross-ref 추가하면 역방향-순방향 부호 정합이 독자에게 자명. (현재도 모순 없음 — 명시성만 보강.)

### 2-4. 극한·코너 적대검산 (발열 초점)

| 극한 | ΔS·Q̇_rev 거동 | 물리 검증 | 판정 |
|---|---|---|---|
| ξ→1 (희박, Li-poor) | config→+∞ → ΔS→+∞ → Q̇_rev→−∞(흡열) | 삽입 자리 선택지 폭증; 저-x 큰 양 ΔS(+29) (Ch2 tab:limits L610) | ✅ |
| ξ→0 (만충, Li-rich) | config→−∞ → ΔS→−∞ → Q̇_rev→+∞(발열) | 배열 선택지 소멸 (Ch2 L611) | ✅ |
| ξ=½ (중심) | config=0 → ΔS=ΔS⁰_j → Q̇_rev=−(IT/F)ΔS⁰_j | 중심 표준값 정확 회수(파생 B 일관) | ✅ |
| I→0 | Q̇_rev=−(IT/F)ΔS→0 | 전류 0 → 가역 발열 0 (소산·가역 둘 다 사라짐) | ✅ |
| T→0 | S_e→0(∝T), Q̇_rev→0(∝T) | 3법칙 정합; 전자항 T-선형 소멸(Ch1 L987) | ✅ |
| 고온(k_BT~E_F) | electronic ∝T 우세화 | FD Sommerfeld; S_e 선형 증가(Ch2 tab:limits L615) | ✅ |
| Ω→2RT⁺ | 상분리 임계; 실측 폭=현상학적 피팅(broadening) | Ch1 sec:broadening; Ch2 파생 C. 발열식 g_j=ξ(1−ξ)/w_j의 w_j는 피팅 폭 | ✅ |

> **극한 결론 [확정]**: 발열 7코너 전부 옳은 물리로 환원. 특히 I→0·T→0이 Q̇_rev→0(가역열 소멸)을 정확히 주고, ξ 양끝 발산이 흡/발열 극값을 만든다 — 분포식이 자기일관.

### 2-5. 비가역 옵션 (가역/비가역 분리)

발열 정련의 마지막 매듭 = 가역(Q̇_rev)과 비가역(Q̇_irr) 분리. Ch2 eq:qrev이 둘을 명시 분해하나, *히스테리시스* 경로의 비가역 옵션이 추가 갈래다.

- **소산 비가역 [확정]**: `Q̇_irr=I(U_oc−V)≥0`(eq:qrev 첫 항). 과전압 η=U_oc−V가 Ch1 동역학 꼬리·분극(V_n=V_app−σ_d|I|R_n)에서 옴. 항상 발열(2법칙). ∂/∂T와 무관.
- **히스 비가역 옵션 [확정]**: 가역 발열은 두 분기 *평균* `∂U_oc^rev/∂T=½(∂U^ch/∂T+∂U^dis/∂T)`(eq:hys_rev L582-583). 히스 gap ΔU^hys 자체는 비가역 — 한 사이클당 `∝I·ΔU^hys`의 entropy production(eq:hys_branch 후 L586). 이는 ∂/∂T와 *별개* — 가역열에 안 섞임.
- **★분리 단언 [확정]**: `Q̇_rev`(분포 재배열 가역 엔트로피) ⊥ `ΔU^hys`(경로 비가역 소산). 하나의 ∂U/∂T로 뭉치면 둘 섞임(Ch2 keybox L589-592). 코드 정합: 코드 `func_U_branch`(L143-148)가 ±½σ_d γΔU_hys로 분기중심 갈라 — Ch2 eq:hys_branch의 `g_j^(d)`와 1:1(P1 §1.2 func_U_branch). 가역 평균은 두 분기 ∂/∂T의 산술평균으로 코드 후처리 가능(현 코드 미구현 = P4).

> **비가역 옵션 정합 [확정]**: Ch2가 (i) 소산 Q̇_irr (ii) 히스 ΔU^hys 두 비가역을 가역 Q̇_rev에서 분리. 경로의존 측정 불확실도 *정량*은 Ch2 범위 밖(L592·L693, 정직 공백 명시) — 틀이 제시됨.

### 2-6. ΔS_rxn ↔ Bernardi entropic coefficient 정합 (요청 명시, 식 정밀)

Bernardi 출구의 entropic coefficient `α≡∂U_oc/∂T`와 Ch2 ΔS(x)의 정합을 **식 수준**으로 못박는다.

```
[측정] α(x) ≡ ∂U_oc/∂T [V/K]   ← potentiometric 다온도 회귀 (Ch2 procedurebox)
[Ch1]  α_j(center) = ΔS_rxn,j/F  (eq:Uj 미분, ξ=½ 봉우리 중심)
[Ch2]  α(x) = (1/F)·[ΔS⁰_j + R ln(ξ/(1−ξ)) ]   (단일전이 지배, eq:single_config L528)
       = (1/F)·[ Σ_j Q_j g_j (ΔS⁰_j + R ln(ξ_j/(1−ξ_j))) / Σ_j Q_j g_j ]  (겹침, 종합식 L673)
```

- **중심 회수 [확정]**: ξ=½서 ln1=0 → `α=ΔS⁰_j/F`. 곧 측정 entropic coefficient의 *봉우리 중심값* = Ch1 staging 표 ΔS_rxn,j/F. tab:ds(Ch2)와 tab:staging(Ch1)이 같은 4값(+29/0/−5/−16). **[확정]**
- **내부 x-의존 [확정]**: 봉우리 내부 α(x) 비선형은 config 항 `R ln(ξ/(1−ξ))/F`가 자동 — 새 입력 없이(Ch2 파생 A 수치검증 FD 일치, L489 "부동소수점 정밀도"). 곧 측정 entropic coefficient의 SOC 곡선 = 분포가 생성. **[확정]**
- **부호 일관 [확정]**: Ch1 LCO verifybox(L488 `ΔS=F·dU/dT=+80 J/(mol·K)` @ +0.83 mV/K)와 동일 환산 부호. 흑연 staging도 동부호 규약 → entropic coefficient ↔ ΔS_rxn 1:1.

> **★요청 핵심 답 [확정]**: ΔS_rxn,j ↔ Bernardi entropic coefficient는 `ΔS_rxn,j = F·(∂U_oc/∂T)|_center` 단일 식으로 정합. *봉우리 중심* = 표준값(상수), *봉우리 내부* = config 분포 x-의존, *합산* = 겹침 가중. 세 층이 Ch2 종합식 한 식(L673)에 모두 담기며 Bernardi 출구 `Q̇_rev=−IT·α`로 닫힌다. Ch1·Ch2·코드 부호 모순 0.

---

## §3. ★ v5 + v3 survey 통합

Ch2 tex는 헤더(L1-15)에서 자신이 **v5** 빌드(코인 하프셀 엔트로피·가역발열 통계열역학, v4-11 기반, w_eff 절 제거 정정본)임을 명시한다. v5의 정정 핵심과, Ch1이 참조하는 v3 계열(ver.3/ver.5 포팅 금지 메모리 정합)을 발열 관점에서 통합 survey한다.

### 3-1. v5 정정 — 발열 관련 (tex 헤더 L8-13 근거)

| 항목 | v4 (구) | v5 (현, Ch2 본문) | 발열 영향 |
|---|---|---|---|
| 파생 C (w_eff) | `w_eff(Ω)=w(1−Ω/2RT)` "상호작용이 종을 좁힘" | **완전 제거** — two-phase 실측은 종이지 델타 아님(narrowing 반대) | g_j=ξ(1−ξ)/w_j의 w_j가 *현상학적 피팅 폭*으로 재정의 → 발열 종합식 입력이 평형 예측 아닌 피팅값(L678-680) [확정] |
| 통계열역학 본체 | (보존) | A·B·D + Z→⟨n⟩→S_config·vib·elec 보존 | 발열 ΔS=세 분포 합 골격 불변 [확정] |
| broadening 기원 | (Ch2 내 혼재) | Ch1 broadening 절로 *위임*(L554) | 발열식 w_j의 기원 추적은 Ch1, Ch2는 지위만 못박음 [확정] |

> **v5 발열 정합 [확정]**: w_eff 제거가 발열 종합식(L673)의 `w_j` 지위를 명확화 — 단상 Ω<2RT는 평형 예측 nRT/F, 흑연 two-phase Ω>2RT는 다온도 dQ/dV 피팅 폭. 발열 산출 시 w_j를 평형값으로 *오입력*하면 봉우리 폭 틀림 → ΔS(x) 내부 항 `R ln(ξ/(1−ξ))` 평가 오류. v5가 이 함정을 파생 C·warnbox(L561-568)로 차단.

### 3-2. v3 survey — 포팅 금지·Ch1 기반 정합 (메모리 chapter_dependency_tree 정합)

- **메모리 정합 [확정]**: `feedback_anode_fit_chapter_dependency_tree` = ver.3/ver.5 포팅 금지(박사님 것 아님). 본 supplement는 ver.3/ver.5 *코드*를 포팅하지 않고, **현 Ch1(v1.0.10)·Ch2(v5)·코드(v1.0.10) 세 입력만**으로 발열 이론 정합. v3 survey = "Ch2가 Ch1의 어느 v3-유래 식을 *재유도 없이 인계*받는가"의 추적.
- **Ch1→Ch2 인계 식 (재유도 금지, 인계만) [확정]**:
  - `ξ_eq=logistic` (Ch1 sec:dist) → Ch2 eq:occ가 통계역학 기원으로 *재해석*(Z₁에서). Ch2가 Ch1을 베끼지 않고 분배함수에서 독립 유도 → 동형 확인. [확정]
  - `∂U_j/∂T=ΔS_rxn/F` (Ch1 eq:Uj 미분) → Ch2 발열식 첫 항으로 *직접 인계*(재유도 X). [확정]
  - Sommerfeld S_e (Ch1 eq:Se, L971) → Ch2 eq:Se가 "Ch1 v9 전자 엔트로피 절에서 상술, 본 장은 분포 언어로 확장해 받음"(L395-396) *명시 인계*. [확정]
  - broadening 3기작·w_j 이중지위 (Ch1 sec:broadening) → Ch2 파생 C가 결과만 받아 지위 못박음(L554). [확정]
- **v3 발열 공백 [추정·정직]**: Ch1·Ch2 어디에도 ver.3 *발열 코드*는 없음(코드 q_rev 부재 P1 §2-E). 발열은 Ch2 이론(P3)→코드(P4) 신규 develop. v3에서 포팅할 발열 자산 0 → 메모리 "포팅 금지"와 *충돌 없음*(애초 포팅 대상 부재).

### 3-3. 통합 survey 결론 [확정]

v5 Ch2 발열 이론은 (i) w_eff 제거로 종합식 w_j 지위 명확화, (ii) Ch1 v9 인계 식(ξ_eq·∂U/∂T·S_e·broadening) 4종을 재유도 없이 받되 통계역학 기원은 독립 전개, (iii) v3 포팅 0(발열 신규 develop)으로 메모리 의존트리·포팅금지와 정합. 발열 사슬은 세 입력만으로 자기완결.

---

## §4. 발열 이론 정련 제안 종합 (드래프트 — master 통합 위임)

> 본문 수정 X, *제안*만. 우선순위·채택은 검수/검토 sub·master.

| ID | 제안 | 근거 | 등급 |
|---|---|---|---|
| P-1 | eq:logistic(L155)에 "n_j=1 기준, 일반 w=n_jRT/F" 1줄 | D-C1: 코드 n_j 일반(L74) vs Ch2 RT/F 고정 | MEDIUM(오독 차단) |
| P-2 | procedurebox(L700~)에 step4 dU_j/dT 부호 = eq:qrev srcbox 규약 cross-ref | D-C2·§2-3 round-trip 부호 명시성 | LOW(현 모순 0, 명시 보강) |
| P-3 | eq:Svib_mode 뒤 부분몰 ΔS_vib=∂S_vib/∂x 한 줄 전개 | D-C3: config는 닫힌식, vib는 정성서술만(대칭 결손) | LOW(두 챕터 공통 공백, 정직 기술됨) |
| P-4 | (확정 권고 아님) 지시문 T-이중곱은 본문에 없음 — 본문 eq:qrev 불변 | §2-1·§2-2 #5: tex 본문 옳음, 지시문 오타 | NOTE(수정 불요) |

**자기완결성 (타전공 독자)**: 본 supplement는 식→식 유도(§2-1 4단계)·차원/부호 11행(§2-2)·극한 7코너(§2-4)로 발열 사슬을 자립 검산. 화학식·물리식 중심, 독자 평가·주관 0. 추정은 근거 병기([추정] 라벨).

---

## §5. Read Coverage / 정직 한계

- **Ch2 tex**: 751줄 전문 정독(서~맺음·thebibliography). 발열 절(sec:revheat L636-716)·세 분포(§2-4)·파생 A-D·warnbox·keybox·tab:ds·tab:limits 전수.
- **P1 result**: 전문 정독. 발열 정합 근거 = §2-E(q_rev/ΔS_e 부재 [확정])·§1.2(func_U_j·func_U_branch·func_ksi_eq)·D4(z_cut/n=1).
- **Ch1 tex**: 1933줄 중 발열-load-bearing 절 집중 정독 — N0~N3 골격(L1-516)·eq:Uj 미분(L437-508)·Sommerfeld 전자엔트로피 전유도(sec:lco-Se L948-1077)·config+vib+elec 분해(eq:lco-decomp L1685-1733)·staging 표(L1658-1683)·broadening 지위(grep L1205-1385). 절 헤더 전수 grep 확인.
- **정직 한계 [근거 미발견]**: (i) 지시문의 `q_rev=−T·I·∂U/∂T·T·ΔS` 곱은 tex 본문에 부재 → 지시문 축약/오타로 판정(본문 eq:qrev은 T 한 번, 옳음). (ii) Ch1 1933줄 중 히스·꼬리·합산 중간절(516-1657 일부)은 발열 직접 무관으로 grep 헤더·핵심식만 확인(전문 라인 정독은 발열 절 한정) — 발열 정합 결론에 영향 없음(중심·전자·분해·broadening 절은 전문 정독).

---

*드래프트 O2 | 2026-07-01 | P3 Ch2 발열 supplement(경쟁 드래프트) | 입력 3종(Ch2 v5 tex·P1 result·Ch1 v1.0.10 tex) 정독 기반 | 본문/코드 수정 0 · 제안만 · 허위 attribution 0*
