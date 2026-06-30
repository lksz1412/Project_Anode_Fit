# V1010 P2 Supplement Draft S1
# Ch1 ↔ 코드 Coverage 매트릭스 + 누락 보완 초안 + LCO 이론 정련안

> 역할: 작업 sub (S1 독립 드래프트). 통합·커밋은 master.
> 대상: `graphite_ica_ch1_v1.0.10.tex` (34 p, v1.0.10) + `V1010_P1_code-audit_RESULT.md` (24심볼·파라미터 앵커)
> 이론 자료: `broadening_w_design.md` + `ORIGIN_VERDICT.md`
> 작성 2026-07-01

---

## 1. Ch1 ↔ 코드 1:1 Coverage 매트릭스

### 1.1 매트릭스 작성 규약

- **코드 step**: P1 맵(§1.1 / §1.2 / §1.3) 기준 N0–N9 + 모듈 함수
- **Ch1 절·식 번호**: tex 실제 `\section`·`\label` 기준 (`sec:*`, `eq:*`)
- **커버 판정**: ✅ = 절+식 유도 있음 / ⚠ = 절 있으나 유도 미완 / ❌ = 문건 유도 없음(누락) / ➖ = 코드엔 없음(문건 과잉)
- 식 번호는 `.tex`의 `\label{eq:…}` 값 사용

### 1.2 매트릭스 본표

| # | 코드 step / 심볼 | 코드 줄 | 핵심 식 | Ch1 절 | Ch1 식 번호 | 커버 | 비고 |
|---|---|---|---|---|---|---|---|
| **N0** | `curve` → `_direction_to_sigma`, `sigma_d`, `I_abs` | L483–524 | σ_d = ±1, \|I\| = c_rate·Q_cell | sec:notation | eq:n0map | ✅ | 매핑 절 완전 |
| **N1** | `dqdv` 분극 `V_n = V_app − σ_d·I_abs·Rn` | L408 | V_n = V_app − σ_d\|I\|R_n | sec:pol | eq:vn (eq:vapppol→eq:vnmid→eq:vn) | ✅ | (a)→(b)→(c) 3단 유도 완전 |
| N1-보조 | 작업 격자 `V_work`, 패딩 | L415 | eq:vwork | sec:pol §subsec 작업격자 | eq:vwork | ✅ | 패딩값 p=0.15 명시 |
| **N2** | `func_U_j`: U_j = (−ΔH + TΔS)/F | L78–79 | eq:Uj | sec:center | eq:gibbsdef → eq:mudef → eq:eqbalance → eq:eqcond → eq:Ujmid → eq:Uj | ✅ | G→μ→전기화학평형 6단계 유도 완전 |
| **N3** | `func_dU_hys`: ΔU_hys(Ω, T) | L133–140 | eq:dUhys | sec:hys §gap닫힌꼴 | eq:mu → eq:gxi → eq:gpp → eq:spinodal → eq:hyssub → eq:hysdiff → eq:dUhys | ✅ | 격자기체→spinodal→gap 7단 유도 완전 |
| N3-a | `func_U_branch`: U^d = U_j + ½σ_d·h_η·γ·ΔU_hys | L143–148 | eq:Ubranch | sec:hys §방향별분기중심 | eq:hyssym → eq:Ubranch | ✅ | 대칭→한 자유도 환원 |
| N3-b | `dqdv` 히스 분기 중심 계산 (L444–450) 게이트 `gamma != 0.0 and Omega > 0.0` | L444 | eq:center | sec:hys 끝 para | eq:center | ✅ | 코드 조건부 분기 명시됨 |
| N3-c | **`func_U_j_hys` 死코드** | L82–91 | (동일식) | 없음 | 없음 | ➖ | 死코드라 Ch1 서술 대상 아님·`func_U_branch`가 대체; 각주 언급 가능 |
| **N4** | `func_w`: w = nRT/F | L74–75 | eq:wbase | sec:width §폭w | eq:wbase | ✅ | 이상 극한·이중지위 서술 완전 |
| N4-b | **`_n_factor`: 'n' 우선 / 'w' 역산 / default 1** | L272–278 | — | ❌ 없음 | ❌ 없음 | ❌ | **누락 GAP-A**: 'n'↔'w' 우선순위·'w' 폴백 inert 물리 미서술 |
| **N5** | `func_ksi_eq`: ξ_eq = logistic[σ_d(V−U)/w] | L94–97 | eq:xieq | sec:width §평형점유유도 | eq:bv → eq:db → eq:logisticsolve → eq:xieq | ✅ | Eyring→detailed balance→logistic 4단 유도 완전 |
| N5-보조 | grand-canonical 분포 관점 (Fermi-함수 동형) | L94–97 | eq:fermifn | sec:dist | eq:partfn → eq:fermifn | ✅ | 통계역학 다리 절 완전 |
| N5-b | **overflow-safe 수치 분기** `z≥0 → 1/(1+e^{−z})`, `z<0 → e^z/(1+e^z)` | L97 | — | ❌ 없음 | ❌ 없음 | ❌ | **누락 GAP-B**: 수치 안정 분기 식 미서술 |
| **N5+** | LCO 전자 엔트로피 ΔS_e (MIT-logistic 게이트) | — | eq:dSegate, eq:ggate | sec:lco-electronic | eq:Se → eq:dSe → eq:dSemolar → eq:ggate → eq:dSegate | ✅ | Fermi-Dirac → Sommerfeld → 게이트 유도 완전; 코드 구현은 P4 예고 필요 |
| **N6** | `equilibrium`: Q_j·ξ_eq(1−ξ_eq)/w | L350–367 | eq:eqpeak | sec:eqpeak | eq:belliden → eq:eqpeak | ✅ | logistic 미분 종 항등식 유도 완전 |
| N6-b | **두-상 broadening·현상학적 w — ③ 앙상블 전이** | L462–464 | eq:ensavg | sec:broadening | eq:ensavg | ✅ | forward 통계평균·③(iii-b) apparent-U 분포 서술 완전 |
| N6-c | `equilibrium` **T 스칼라 전용 제약** (배열 T 미지원) | L352 | — | ❌ 없음 | ❌ 없음 | ❌ | **누락 GAP-C**: equilibrium vs dqdv의 T 배열 지원 차이 미서술 |
| **N7-A** | `_resolve_lag_length` 컷 affinity A = min(z_cut·n·RT, A_cap·RT) | L331 | eq:Acut | sec:lag §컷affinity | eq:Acut | ✅ | z_cut = 미분 5% 컷 선택값 명시 |
| **N7-B** | `func_chi_d`: χ_d (방전 χ / 충전 1−χ) | L158–163 | eq:chid | sec:lag §방향별전달계수 | eq:chid | ✅ | 합-1 제약 유도 완전 |
| **N7-C** | `func_dH_a_eff`: ΔH_a^eff = ΔH_a − χ_d·Ω | L152–155 | eq:dHeff | sec:lag §방향별전달계수 | eq:dHeff | ✅ | 깊은 꼬리 상호작용 흡수 유도 완전 |
| **N7-D** | `func_L_q`: ln L_q = ln(T*/T) − ln(1+e^{−A/RT}) + ΔG_a/RT − χ_d·A/RT | L100–107 | eq:Lqfull (eq:Lq → eq:kuniv → eq:Lqmid2 → eq:Lqfull) | sec:lag §L_q평가 | eq:Lqmid → eq:Lq → eq:kuniv → eq:Lqmid2 → eq:Lqfull | ✅ | 운동방정식→용량축→k_j→닫힌식 완전 |
| **N7-E** | `_resolve_lag_length` → `L_V = |dVdq_qa|·L_q` | L347 | eq:LV | sec:lag §L_V환산 | eq:LV | ✅ | 전압축 환산 완전 |
| N7-F | **`dH_a` 부재 시 L_V=0 (꼬리 off)** | L319–320 | — | ⚠ 부분 | sec:lag 끝 para | — | ⚠ | **보완 GAP-D**: 'L_V' 직접 지정이 dH_a/chi/Omega/z_cut 전부 우회 (`dqdv` silent-off)는 표~tab:inputs 각주로 경고만, 본문 유도 없음 |
| **N8-A** | `_causal_lowpass`: ρ = exp(−Δ/L_V), ξ_lag[i] = ρ·ξ_lag[i−1] + (1−ρ)·ξ_eq[i] | L110–128 | eq:lowpass | sec:tail §지수기억 | eq:intfactor → eq:memory → eq:lowpass | ✅ | 1계 ODE→적분인자→이산 저역통과 3단 완전 |
| N8-A2 | **DC 이득 = 1 (면적 보존)** (`_causal_lowpass` 계수 [1−ρ]/[1,−ρ]) | L110–128 | — | ❌ 없음 | ❌ 없음 | ❌ | **누락 GAP-E**: DC gain=1이 면적 보존의 물리적 이유·검산 미서술 |
| **N8-B** | `peak_shape = (ξ_eq − ξ_lag)/L_V` | L475 | eq:peakshape | sec:tail §peak모양 | eq:peakshape | ✅ | 완전 |
| **N8-C** | 분기 스위치: L_V < ν·Δ_grid → 평형 종 직접 | L462–464 | eq:branch | sec:tail §L_V소멸 | eq:branch | ✅ | 0/0 불연속·이산 모드 스위치 명시 |
| **N8-D** | 충전 격자 역전 `ξ[::-1]…[::-1]` | L473 | eq:reversal | sec:tail §충전역전 | eq:reversal | ✅ | 인과 방향 완전 |
| **N9** | `dqdv_work += Q_j * peak_shape`, `np.interp(V_n, V_work, dqdv_work)` | L477, L479 | eq:sum | sec:sum | eq:sum | ✅ | 선형 합산·역보간 완전 |
| **파라미터: U_j** | `'U'` 또는 `(dH_rxn, dS_rxn)` | L78, L360 | eq:Uj | sec:center | eq:Uj | ✅ | 피팅 인자 완전 설명 |
| **파라미터: n_j** | `'n'`(또는 `'w'` 역산; default 1.0) | L272–278 | eq:wbase | sec:width | eq:wbase | ⚠ | 'n' 우선/'w' inert 명시 없음 → GAP-A 참조 |
| **파라미터: Ω_j** | `'Omega'` | L441 | eq:dUhys, eq:dHeff | sec:hys, sec:lag | eq:dUhys, eq:dHeff | ✅ | 히스+꼬리 이중 역할 완전 |
| **파라미터: γ_j** | `'gamma'` | L442 | eq:Ubranch | sec:hys | eq:Ubranch | ✅ | 분기 축소 완전 |
| **파라미터: ΔH_a** | `'dH_a'` | L333 | eq:Lqfull | sec:lag | eq:Lqfull | ✅ | 활성화 엔탈피 완전 |
| **파라미터: ΔS_a** | `'dS_a'` | L334 | eq:Lqfull (ΔG_a=ΔH_a−TΔS_a) | sec:lag | eq:Lqfull | ✅ | 온도 의존 엔트로피 완전 |
| **파라미터: χ** | `'x'` / 생성자 `chi` | L237 | eq:chid | sec:lag | eq:chid | ✅ | 전달 계수 완전 |
| **파라미터: dVdq_qa** | `'dVdq_qa'` | L347 | eq:LV | sec:lag | eq:LV | ⚠ | silent-off 경고 GAP-D 참조 |
| **파라미터: Rn** | 생성자 `Rn` | L235, L408 | eq:vn | sec:pol | eq:vn | ✅ | IR 분극 완전 |
| **파라미터: Cbg** | 생성자 `Cbg` | L236, L427 | eq:sum | sec:sum | eq:sum | ⚠ | 유한성 미검 경고(F4) — 문건 각주 수준 경고만 |
| **파라미터: z_cut** | 생성자 / per-tr override | L217, L329 | eq:Acut | sec:lag | eq:Acut | ⚠ | **docstring 부정확(L217)**; tex 본문은 "미분 5% 컷" 정확; §1.2 sec:lag 절엔 올바른 설명 ✅ |
| **파라미터: A_cap_RT** | 생성자 | L226, L330 | eq:Acut | sec:lag | eq:Acut | ✅ | A 상한 완전 |
| **파라미터: ΔS_rxn** | `'dS_rxn'` | L78, L534 | eq:Uj | sec:center | eq:Uj | ✅ | 온도 기울기 완전 |
| **파라미터: h_eta** | `'h_eta'` | L443 | eq:Ubranch | sec:hys | eq:Ubranch | ✅ | 부분 cycle 인자 완전 |
| **LCO 파라미터** | `LCO_STAGING_LIT`(3전이) | — | — | sec:lco-map, sec:lco-hys, sec:lco-electronic, sec:lco-decomp | 다수 | ✅ | 전이 구조·부호·전자항 모두 완전 |

### 1.3 누락(GAP) 및 과잉(➖) 요약

| ID | 유형 | 코드 자리 | Ch1 현황 | 핵심 내용 |
|---|---|---|---|---|
| **GAP-A** | ❌ 누락 | `_n_factor` L272–278 | 절 없음 | 'n' 우선 / 'w' 역산 / default 1.0 우선순위 물리; `GRAPHITE_STAGING_LIT`의 `'n':1.0` 때문에 `'w'` 폴백값(0.012–0.020 V)이 실제로 비활성(inert)인 사실 |
| **GAP-B** | ❌ 누락 | `func_ksi_eq` L97 | 절 없음 | overflow-safe 이중 분기: z≥0 → 1/(1+e^{−z}), z<0 → e^z/(1+e^z) — 수학적 동일이나 수치적으로 필요한 이유 |
| **GAP-C** | ❌ 누락 | `equilibrium` L352 | 절 없음 | `equilibrium`은 T 스칼라 전용(`_finite_pos` 검사); `dqdv`와 달리 배열 T(V) 비등온 미지원; 실용 함정 |
| **GAP-D** | ⚠ 보완 | `_resolve_lag_length` L313–320 | 부분 | 'L_V' 직접 지정 시 dH_a/chi/Omega/z_cut/dVdq_qa 전부 우회; dH_a 부재 → silent L_V=0 (꼬리 off); 과식별 주의 |
| **GAP-E** | ❌ 누락 | `_causal_lowpass` L110–128 | 절 없음 | DC 이득 = 1 (계수 [1−ρ]/[1,−ρ], ∑=1) → 면적 보존의 수학적 증명; 이것이 1.0.10 use_w_eff 제거와 연결되는 물리 |
| **➖ 과잉** | ➖ 코드 없음 | — | sec:lco-electronic § 전자항 plug-in (sec:lco-code) | 전자항 코드 구현(`ΔS_e` 슬롯 plug-in)은 **P4** 예정 — 현재 `Anode_Fit_v1.0.10.py` 코드에 미구현(§2-E 흑연 전용 확인). 문건은 완전한 이론 서술이나 코드 대응이 없음 → **P4 구현 예고 문장 필요** |

---

## 2. 누락 유도·다리 보완 초안

### 2.1 GAP-A: `_n_factor` 우선순위 — 폭 척도의 세 경로

**삽입 위치**: `sec:width` §폭w 말미, `\textbf{★폭 $w_j$의 이중지위}` 아래 codebox.

**보완 초안** (교과서 형식):

---

**★코드의 폭 입력 우선순위 — 왜 `'w'` 폴백이 비활성이 되는가.**

코드 `_n_factor`(L272–278)는 전이 dict에서 폭 척도를 세 경로로 읽는다.

$$
n_j = \begin{cases}
\text{tr}['\text{n}'] & \text{`'n'` 키 존재 (최우선)}\\
\dfrac{\text{tr}['\text{w}'] \cdot F}{RT} & \text{`'n'` 없고 `'w'` 존재 (역산)}\\
1.0 & \text{둘 다 없을 때 (default)}
\end{cases}
\label{eq:nfactor}
$$

세 경로 모두 동일한 $w_j = n_j RT/F$(식~\ref{eq:wbase})로 합쳐진다 — **폭을 계산하는 식은 하나**, 입력 형식만 셋이다. 우선순위의 물리적 귀결이 하나 있다: `GRAPHITE_STAGING_LIT`는 모든 전이에 `'n': 1.0`을 명시 보유한다(첫째 경로). 따라서 같은 dict의 `'w': 0.012`–`0.020` 폴백값은 **실제로 읽히지 않는다**(비활성 — Dead data). 현재 코드 상태에서 폭은 $w_j = 1.0 \times RT/F \approx 25.7\,\text{mV}$ (298 K)로 고정된다. 피팅에서 폭을 자유 파라미터로 노출하려면 `'n'` 키 값을 직접 조정하거나(단조 방향 식별), `'n'` 키를 제거하고 `'w'`를 쓰는 것(역산 경로)이 동치다. 단상(solid-solution) 전이의 경우 폭이 평형 예측 $RT/F$에서 멀어지면 물리 근거를 잃으므로, 피팅 bound를 $n_j > 0$으로 강제하는 것(§2-C F1의 피팅 가드)이 실용상 권고된다.

---

### 2.2 GAP-B: logistic overflow-safe 분기의 수치 정당화

**삽입 위치**: `sec:width` §평형점유유도, `\begin{signbox}` 바로 앞.

**보완 초안**:

---

**★수치 안정 분기 — logistic 의 두 동치 표현.**

식~\ref{eq:xieq}의 $\xi_\eq = 1/(1+e^{-z})$는 $z \gg 0$에서 수치적으로 안전하나, $z \gg 0$이면 $e^{-z} \approx 0$이라 부동소수점 1/(1+0) = 1 (정상), $z \ll 0$이면 $e^{-z} \to \infty$라 분모 overflow → NaN이다. 분자·분모를 $e^{-z}$로 나눈 동치 표현

$$
\xi_\eq = \frac{e^z}{1 + e^z} \qquad (z < 0 \text{ 에서 수치 안정})
\label{eq:ksisafe}
$$

은 $z \ll 0$에서 $e^z \approx 0$이라 0/(1+0) = 0으로 안전하다. 코드 `func_ksi_eq`(L97)는 이 두 표현을 $z \ge 0$과 $z < 0$으로 나눠 평가한다:

$$
\xi_\eq = \begin{cases}
\dfrac{1}{1+e^{-z}} & z \ge 0\\[6pt]
\dfrac{e^z}{1+e^z} & z < 0
\end{cases}
\qquad (z \equiv \sigma_d(V-U_j^{\,d})/w_j)
\label{eq:ksibranch}
$$

두 표현은 $z = 0$에서 $\xi_\eq = 1/2$로 연속이며 수학적으로 동일하다. 이 분기는 새 물리를 도입하는 것이 아니라 식~\ref{eq:xieq}의 **수치 실현**이다 — $\xi_\eq \in (0,1)$ 보장과 대 $|z|$에서의 계산 안정성을 동시에 얻는다.

---

### 2.3 GAP-C: `equilibrium` T 스칼라 전용 제약 — `dqdv`와의 분기

**삽입 위치**: `sec:eqpeak` § equilibrium 코드박스 뒤, 또는 `sec:notation` §서론 맥락 각주.

**보완 초안**:

---

**★`equilibrium` vs `dqdv` — 온도 처리의 분기.** 두 메서드는 같은 물리식(식~\ref{eq:eqpeak})을 평가하지만 온도 처리가 다르다. `equilibrium`(L350–367)은 진입부에서 `T = _finite_pos("T", T)`(L352)를 수행한다 — 이 가드는 스칼라 양수를 요구하므로 **배열 T(V) 비등온 입력을 거부**한다. 반면 `dqdv`(L370–480)는 `T_is_array` 분기(L402–424)로 비등온 프로파일 $T(V)$를 완전히 지원한다(같은 격자 위로 보간, 대표 온도 $T_\rep = \overline{T_\text{work}}$). 이 차이는 두 메서드의 목적에서 온다 — `equilibrium`은 $|I| \to 0$ 기준선(등온 단순 계산)이고, `dqdv`는 실측 비등온 실험조건을 모두 받는 전면 forward 계산이다. 따라서 **다온도 비등온 데이터에 기준선이 필요할 때는 `dqdv`를 $|I| = 0$ 대신 $|I| \to 0$으로 근사**($L_V \to 0$이 되어 평형 종으로 환원)하거나, `equilibrium`을 반복 호출해야 한다.

---

### 2.4 GAP-D: 동역학 꼬리의 세 off-스위치 — silent 꼬리 소거 방지

**삽입 위치**: `sec:lag` § $L_q$ 평가 끝 codebox 뒤 새 소절.

**보완 초안**:

---

**★동역학 꼬리의 세 off-스위치 — silent 소거 방지.** `_resolve_lag_length`(L303–347)는 $L_V$를 산출하기 전에 세 분기로 꼬리를 꺼버리는 경로가 있다. 세 경로를 명시한다.

**(i) 직접 지정 'L_V' 우회(L313–318):** 전이 dict에 `'L_V'` 키가 있으면 그 값을 직접 반환하고 이후의 $\mathcal{A} \to \chi_d \to \Delta H_a^\eff \to L_q$ 사슬을 **전부 건너뛴다**. 이는 피팅 초벌 단계나 단위 테스트에 유용하나, `'L_V'`와 `dH_a`·`chi`·`Omega`·`z_cut`·`dVdq_qa`를 동시에 dict에 넣으면 후자들이 꼬리에 **반영되지 않는다** — 과-식별(over-specification) 위험.

**(ii) $I \le 0$ 또는 `dH_a` 부재 → $L_V = 0$(L319–320):** 전류 크기 $|I| = 0$이거나 전이 dict에 `'dH_a'` 키가 없으면 $L_V = 0$이 되어 평형 종 분기(식~\ref{eq:branch})로 떨어진다. `dH_a` 부재는 코드가 경고나 오류 없이 조용히 꼬리를 끄는 **silent off**이므로, 동역학 전이에는 반드시 `dH_a`를 dict에 포함해야 한다.

**(iii) `dVdq_qa` = 0 또는 누락 → $L_V = 0$(L346–347):** `dVdq_qa`가 dict에 없으면 `transition.get('dVdq_qa', 0.0)`이 0.0을 반환하고(L346), $L_V = |0.0| \times L_q = 0$이 된다. `dH_a`가 완전히 있어도 이 한 누락으로 꼬리가 사라진다 — 역시 silent off. `dVdq_qa` 값은 LIT 데이터셋에서는 0.30 V로 설정돼 있으므로 초기값 그대로 두면 문제없으나, 커스텀 전이 dict를 만들 때 간과하기 쉽다.

$$
L_V = 0 \;\text{(꼬리 off)} \iff
\begin{cases}
\text{'L\_V'}\in\text{tr} & \text{(직접 지정, 사슬 우회)} \\
|I| \le 0 \;\text{또는}\; \text{'dH\_a'}\notin\text{tr} & \text{(silent, ①②)} \\
|\text{dVdq\_qa}| = 0 & \text{(silent, ③)}
\end{cases}
\label{eq:tailoff}
$$

이 세 경로 중 ①은 의도적 선택이고, ②③은 dict 누락에 의한 비의도적 소거다 — 피팅 wrapper에서 schema 검증(`dH_a > 0`, `dVdq_qa > 0`)이 권고된다(§2-C F2).

---

### 2.5 GAP-E: DC 이득 = 1 → 면적 보존의 수학적 증명

**삽입 위치**: `sec:tail` §지수기억 ¶ 이산 저역통과 직후 새 verifybox.

**보완 초안**:

---

**★DC 이득 = 1과 면적 보존.** `_causal_lowpass`(L110–128)의 IIR 필터는 분자 계수 $[1-\rho]$, 분모 계수 $[1, -\rho]$이다($\rho = e^{-\Delta_\text{grid}/L_V}$). 이 필터의 DC 전달 이득 — 즉 $z = 1$ (DC 성분)에서의 전달함수 — 은

$$
H(1) = \frac{1-\rho}{1-\rho} = 1
\label{eq:dcgain}
$$

로 정확히 1이다. 이것이 **면적 보존의 수학적 근거**다: 입력 신호 $\xi_\eq(V)$의 전압 적분 $\int \xi_\eq \, dV$와 출력 $\xi_\text{lag}(V)$의 전압 적분이 같으므로($H(1) = 1$이 그 조건), peak shape $= (\xi_\eq - \xi_\text{lag})/L_V$의 전압 적분은

$$
\int \frac{\xi_\eq - \xi_\text{lag}}{L_V} \, dV = \frac{1}{L_V}\int(\xi_\eq - \xi_\text{lag})\, dV = \frac{1-H(1)}{L_V}\int \xi_\eq\, dV = 0
\label{eq:tailarea}
$$

이 아니라, $Q_j \cdot \text{peak shape}$의 전압 적분 $= Q_j$ 라는 면적 보존은 — 더 정확히는 — 꼬리 분기의 전압 적분이 평형 분기와 같은 $Q_j$로 수렴한다는 것을 **전체 $V$ 구간이 충분히 커서 경계 손실이 없을 때** 보장한다. $L_V$가 크면 격자 가장자리에서 $\xi_\text{lag}$가 $\xi_\eq$를 충분히 따라잡지 못해 경계 손실이 생기므로(§0 §2-C, 큰 $L_V$에서 면적 0.9997), `grid_pad`·전압창을 충분히 크게 잡는 것이 실용상 권고된다. v1.0.10의 `use_w_eff` 제거(L7)는 ξ_eq 폭과 분모 w의 불일치를 바로잡아 이 면적 보존이 깨지는 버그를 제거한 것이며, DC 이득 = 1이 그 수학적 지지다(독립 적분 검산: 전이별 면적 비율 = 1.000000, §0).

---

## 3. LCO 이론 정련안

### 3.1 v9 LCO 검토분 타당성 평가

v9(= v1.0.10의 LCO 절들)이 담은 LCO 이론 내용을 P1 맵 §2-E·코드 상태와 대조해 타당성을 평가한다.

| 항목 | v9/v1.0.10 서술 | 타당성 | 비고 |
|---|---|---|---|
| LCO 양극 부호 규약 (sec:lco-map) | σ_d=+1 방전=LCO 리튬화, 충전=탈리튬화; 흑연과 1:1 대칭 | ✅ 타당 | 부호 규약 대칭 정확 |
| U_j(T) 식 동일 적용 (sec:lco-center) | 식~eq:Uj 전극 무관; LCO는 입력값만 바뀜 | ✅ 타당 | 유도에 전극 가정 없음 확인 |
| ∂U_j/∂T = ΔS_rxn/F (eq:lco-dUdT) | 같은 T 미분 | ✅ 타당 | |
| LCO order-disorder ↔ 정규용액 Ω (sec:lco-hys) | T2·T3: Ω>2RT 상분리; T1: MIT 2상역 | ✅ 타당 | |
| MIT 전자 엔트로피 S_e = (π²/3)k_B²T·g(E_F) (sec:lco-Se) | Sommerfeld 표준 결과 tier A | ✅ 타당·완전 | 함수형·anchor·연속 곡선 3층 신뢰등급 분리 정확 |
| MIT-logistic 게이트 g(E_F,x) ≈ g_max·[1−σ((x−x_MIT)/Δx)] (sec:lco-gate) | 물리 정당화 4 근거 (anchor·중심·폭·자기일관) | ✅ 타당 | 모델 가정임을 명시; tier 병기 |
| ΔS_e 부호: 삽입 기준 < 0 (eq:dSe) | 삽입(x↑)→금속→절연체 → ∂g/∂x < 0 → ΔS_e < 0 | ✅ 타당 | 부호 유도 완전 |
| 몰당 환산 N_A·∂S_e/∂x (eq:dSemolar) | N_A k_B² = R k_B 환산 | ✅ 타당 | 단위 다리 명시 |
| ΔS_e ∝ T — ∂U_j/∂T의 T-선형성 (sec:lco-Se 끝) | C_e = (π²/3)k_B²T·g(E_F) → S_e = C_e적분 → T-선형 | ✅ 타당 | U 이동은 ∝T² (비선형 식별 신호) |
| 닫힌식 eq:dSegate: ΔS_e = −(π²/3)k_B²T·(g_max/Δx)·σ(1−σ) < 0 | logistic 미분 항등식으로 닫힘 | ✅ 타당·완전 | 식 형식·부호 모두 정확 |
| **∆S_rxn config+vib+elec 분해 (eq:lco-decomp)** | config 이중계산 금지·직교성 가산 | ✅ 타당 | 가산성 정당화(직교)·무이중계산(슬롯 분리) 양면 완전 |
| **전자항 코드 plug-in (sec:lco-code)** | `ΔS_e^mol = N_A·∂S_e/∂x`를 ΔS_rxn 슬롯에 더하는 1줄 | ⚠ 미구현 | **P4 구현 예고 필요**: 현 v1.0.10 코드에 전자항 없음(§2-E 확인); 문건 이론은 완전하나 코드 대응 없음 |
| MSMR 동형 (eq:msmr) | x_j = X_j/(1+exp[f(U−U^0)/ω])과 eq:xieq의 1:1 대응 | ✅ 타당 | f = −σ_d 대응 명시 |

### 3.2 LCO dQ/dV·전자 엔트로피 이론 교재급 정련

#### 3.2.1 현황 진단

v1.0.10 sec:lco-electronic 절은 이미 상당한 교재급 수준이다. 그러나 다음 부분에서 **미완성 또는 보강 가능** 위치가 있다.

**(A) Sommerfeld 전개의 중간 유도 단계 — 상세화 여지**

현재 (b)에서 "축퇴 전자기체에서 Sommerfeld 전개로 닫힌다"고 기술하고 $C_e$ → $S_e$ 적분이 곧바로 eq:Se로 닫히는데, **그 Sommerfeld 적분의 닫힘 자체** — 즉 $\int(-\partial f/\partial E)(E-E_F)^2 dE = (\pi^2/3)(k_BT)^2$의 유도 — 가 생략되어 있다.

**(B) ΔS_e 부호 논리의 단계화 — 현재 단락이 길어 사슬이 흐림**

삽입 기준 부호의 논리 사슬이 단락 안에서 다소 흘러가 있다. 이를 명시적 (a)→(b)→(c)→(d) 단계로 분리하면 교재 형식에 부합한다.

**(C) ΔS_e ∝ T의 관측 신호 — 다온도 피팅에서의 식별 방법**

현재 "∂U_1/∂T의 기울기 자체가 T에 비례"라고 서술하는데, 이것이 왜 config·vib와 구분되는지 — 즉 **다온도 dQ/dV peak 위치의 T 의존**에서 어떻게 전자항을 식별하는지 — 의 실험적 처방이 없다.

#### 3.2.2 정련 초안

**[보완 A] Sommerfeld 적분 닫힘 — 중간 유도**

sec:lco-Se (c) 중간식 단계에 아래를 삽입한다.

---

Sommerfeld 적분이 닫히는 핵심은 $-\partial f/\partial E$의 국소성이다. 분포 $f(E) = 1/(1+e^{(E-E_F)/k_BT})$를 미분하면

$$
-\frac{\partial f}{\partial E} = \frac{1}{k_BT} \frac{e^{(E-E_F)/k_BT}}{(1+e^{(E-E_F)/k_BT})^2}
= \frac{1}{4k_BT}\operatorname{sech}^2\!\left(\frac{E-E_F}{2k_BT}\right)
\label{eq:dfde}
$$

이 함수는 $E = E_F$ 에서 높이 $1/(4k_BT)$의 **폭 $\sim k_BT$의 대칭 봉우리**다($k_BT \ll E_F$ 금속 극한에서 델타에 근접). $g(E) \approx g(E_F)$ 동결 아래 내부에너지 변화는

$$
\delta U_e = \int_{-\infty}^{+\infty} (E - E_F) \left(-\frac{\partial f}{\partial E}\right) g(E_F) \, dE
= g(E_F) \int_{-\infty}^{+\infty} \varepsilon \cdot \frac{e^{\varepsilon/k_BT}}{(e^{\varepsilon/k_BT}+1)^2} \frac{d\varepsilon}{k_BT}
\label{eq:duemid}
$$

($\varepsilon \equiv E - E_F$, 치환). 피적분 함수의 기함수 성질과 표준 Sommerfeld 적분 $I_2 \equiv \int_0^\infty \varepsilon^2 \frac{e^\varepsilon}{(e^\varepsilon+1)^2} d\varepsilon / (k_BT)^2 = \pi^2/6$을 이용하면 (기함수 부분은 대칭으로 0, 우함수 $\varepsilon^2$ 몫만 남음)

$$
\delta U_e = g(E_F)(k_BT)^2 \cdot 2I_2 = g(E_F) \frac{\pi^2}{3} (k_BT)^2
\label{eq:duefinal}
$$

이므로 $C_e = \partial\delta U_e/\partial T = \frac{\pi^2}{3}k_B^2 T g(E_F)$가 T-선형으로 닫힌다. 이를 $S_e = \int_0^T C_e/T' dT'$로 적분하면 $C_e/T' = (\pi^2/3)k_B^2 g(E_F)$가 $T'$ 무관상수라 적분이 곧바로 $S_e = (\pi^2/3)k_B^2 T g(E_F)$ (식~\ref{eq:Se})로 닫힌다.

---

**[보완 B] ΔS_e 부호 논리 — (a)→(b)→(c)→(d) 명시적 단계화**

sec:lco-Se (d) 박스 앞의 부호 단락을 아래 4단계로 재구성한다.

---

**(a) 출발 — 삽입 기준.** forward 모델의 $\Delta S_{\rxn,j}$ 슬롯은 **삽입 방향** ($x \uparrow$, Li 주입 당)의 엔트로피 변화다 — 흑연의 $\Delta S_\rxn = -16$ J/(mol·K) < 0 (stage 2→1 삽입 시 엔트로피 감소)와 같은 부호 규약.

**(b) 연산 — g(E_F)의 조성 의존.** MIT 삽입($x \uparrow$)은 금속 → 절연체 방향이므로 $g(E_F)$가 감소한다: $g_{\max} \to 0$. 따라서 $\partial g / \partial x < 0$.

**(c) 중간식 — ΔS_e 부호 결정.** 식~\ref{eq:dSe}에 (b)를 대입:

$$
\Delta S_{e,j} = \frac{\pi^2}{3} k_B^2 T \underbrace{\frac{\partial g}{\partial x}}_{<\,0 \;\text{(삽입=금속→절연체)}} < 0
\label{eq:dSesgn}
$$

**(d) 박스 — 삽입 기준 음의 값; 탈리튬화 방출.** 삽입($x \uparrow$)에서 전자 엔트로피가 감소($\Delta S_{e,j} < 0$)하는 것은 전도 전자가 줄어들어 열용량이 감소하는 것과 일관된다. 역으로 탈리튬화($x \downarrow$, 본 문건 LCO 충전 주 진행)에서 방출되는 전자 엔트로피 $|\Delta S_{e,j}| = -\partial S_e/\partial x > 0$이 T1 부근에서 국소 봉우리를 이룬다.

---

**[보완 C] ΔS_e ∝ T 식별 처방 — 다온도 peak 위치 T 의존**

sec:lco-Se 끝에 다음 단락을 추가한다.

---

**★다온도 피팅에서 전자항 식별 처방.** config·vib 성분의 $\partial U_j/\partial T = \Delta S_\rxn^\mathrm{const}/F$는 온도에 **무관한 상수**이므로 peak 위치가 $T$에 **선형**으로 이동한다. 반면 전자항은 $\Delta S_{e,j} \propto T$(식~\ref{eq:Se})이므로 그 기여 $\partial U_1/\partial T|_e = \Delta S_{e,j}/F \propto T$도 온도에 **선형**으로 증가한다 — 즉 $\partial U_1/\partial T$의 기울기 자체가 $T$에 비례하며, 이를 적분한 T1 위치의 전자항 기여는 $\propto T^2$이다.

실험적으로 이 두 기여를 분리하는 처방은 다온도 dQ/dV 데이터에서 T1 peak 위치 $V_{\text{peak,1}}(T)$를 추적하는 것이다. Config·vib만 있다면 $V_\text{peak,1}$는 $T$에 선형이고 그 기울기는 $\Delta S_\rxn^\mathrm{const}/F$로 일정하다. 전자항이 있으면 **기울기 자체가 $T$에 비례**하므로 $V_\text{peak,1}$는 $T$에 대해 2차 포물선을 따른다:

$$
V_\text{peak,1}(T) \approx U_1^{(0)} + \frac{\Delta S^\mathrm{const}}{F} T + \frac{1}{F}\frac{\pi^2}{3}k_B^2 \frac{\partial g}{\partial x}\bigg|_{x=x_\mathrm{MIT}} \cdot T^2
\label{eq:Tquad}
$$

($U_1^{(0)}$ = 기준 온도 외삽). 두 항의 계수($\Delta S^\mathrm{const}/F$와 T² 계수)를 독립적으로 피팅하면 config·vib 몫과 전자항 몫을 분리 식별할 수 있다. 단, 이 분리에는 30 K 이상의 온도 구간이 필요하다(30 K 창에서 전자항 기여 $\Delta U \approx |(\partial g/\partial x)\cdot\pi^2 k_B^2 T / F| \cdot \Delta T \sim$ 수 mV 규모 [추정] — 정밀 정량은 실측으로 결정).

**코드 구현 예고 (P4).** 식~\ref{eq:dSegate}의 전자 엔트로피 항 — $\Delta S_{e,j}^{\,\mathrm{mol}}(x, T)$를 `ΔS_rxn` 슬롯에 더하는 한 줄 — 은 **P4**에서 구현될 예정이다. 현재 `Anode_Fit_v1.0.10.py`는 흑연 음극 전용(§2-E)이며 LCO 전자항 코드가 없다. P4 구현 시 단위 주의 사항(자리당 $k_B^2$ → 몰당 $N_A k_B^2 = Rk_B$, 식~\ref{eq:dSemolar})과 `g(E_F, x)` 연속 곡선(식~\ref{eq:ggate}의 logistic 게이트, 초기값 3개 피팅)을 반드시 포함해야 한다.

---

### 3.3 v3~v9 교과서 요소 통합 권고

v3~v9에서 있었다가 v8~v9에서 삭제된 요소 중 broadening_w_design.md가 복원을 명시한 항목을 점검한다.

| 요소 | v3~v5 상태 | v8~v9 상태 | v1.0.10 상태 | 통합 권고 |
|---|---|---|---|---|
| broadening 절 (전이별 고용체 vs 2상) | 있음 | 삭제 | ✅ 완전 복원 (sec:broadening) | 완료 — 추가 작업 불필요 |
| w 이중지위 (평형 예측 vs 현상학적 피팅 폭) | 있음 | 삭제 | ✅ 완전 복원 (sec:width §이중지위) | 완료 |
| w_eff 제거 이유 | w_eff 있음 | 삭제 이유 불명 | ✅ 명시 제거 + 이유 서술 | 완료 |
| Dreyer 다입자 순차전환 (평형 plateau 기원) | 있음 | 삭제 | ✅ 복원 (sec:broadening (iii-a)) | 완료 |
| apparent-U = U_j + η (분포는 η) | 일부 | 삭제 | ✅ 복원 (sec:broadening (iii-b)) | 완료 |
| dQ/dV → ρ(U_app) 역산 금지 | 일부 | 없음 | ✅ 명시 (sec:broadening (c)) | 완료 |
| LCO 전자 엔트로피 (sec:lco-electronic) | v5 초안 수준 | v9에서 발전 | ✅ 완전 유도 (v1.0.10) | 완료 — 본 §3.2 정련으로 추가 보강 |

**결론**: v3~v9의 복원 대상 교과서 요소는 v1.0.10에서 이미 모두 복원되었다. 잔여 보강은 §3.2의 세 정련 항목(Sommerfeld 중간 유도·부호 4단계·다온도 식별 처방)이다.

---

## 4. 통합 요약

### 4.1 Coverage 결과

- **완전 커버(✅)**: 코드의 12 closed-form 식 전부 + 24심볼 중 19개 심볼·파라미터가 Ch1 절·식으로 완전히 유도됨
- **누락(GAP A–E)**: 5건 — `_n_factor` 우선순위(A), overflow-safe 분기(B), equilibrium T 제약(C), silent tail-off 스위치(D), DC gain=1 면적보존(E)
- **코드 없는 이론 문건 과잉(➖)**: LCO 전자항 코드 구현 — P4에서 구현 예고 문장으로 정렬 필요

### 4.2 보완 우선순위

| 우선 | GAP | 중요성 | 삽입 위치 |
|---|---|---|---|
| 1 | GAP-D (silent tail-off) | 피팅 실용 — 눈에 안 띄는 결함 | sec:lag 끝 |
| 2 | GAP-A (_n_factor 우선순위) | 폭 파라미터 해석 핵심 | sec:width 끝 |
| 3 | GAP-E (DC gain=1) | 면적 보존 이론 완결 | sec:tail 지수기억 뒤 |
| 4 | GAP-B (overflow-safe) | 수치 구현 투명성 | sec:width logistic 뒤 |
| 5 | GAP-C (equilibrium T제약) | 실용 함정 경고 | sec:eqpeak codebox 뒤 |

### 4.3 LCO 정련 완성도

- 이론 서술: **대부분 완전** (v1.0.10이 이미 교재급 수준)
- 보강 대상: 3건 — Sommerfeld 중간 유도, ΔS_e 부호 4단계, 다온도 식별 처방
- 코드 구현: **P4 예고 필요** (현재 흑연 전용·전자항 미구현)
- P4 구현 핵심 주의: N_A 환산($k_B^2$ → $Rk_B$) + logistic 게이트 3파라미터 피팅

---

*산출: 2026-07-01 | V1010 P2 Draft S1 | 범위: supplement 단독 (Ch1 tex 미수정, 코드 미수정) | 통합·커밋은 master 전담*
