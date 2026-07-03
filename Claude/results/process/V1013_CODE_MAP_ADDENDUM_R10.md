# V1013 CODE_MAP — 현행화 Addendum R10 (P6.1)

> **본 문건은 `V1013_CODE_MAP.md`(P1 산출)의 현행화 Addendum 이다(기준 커밋 292f10e — "v1.0.13 P5 R10 최종").**
> 원본은 결과 문건 보호 규칙에 따라 무수정 보존하며, 본 Addendum 이 R9 검수(`V1013_REVIEW_R9_B.md` §6 M1~M8)가
> 지적한 stale 항목의 처분과 **현행 전체 매핑표(A~E절 완전판)** 를 담는다 — **이 문건 단독으로 사용 가능**하다.
>
> 입력 전문 정독(P6.1 작업 sub, head→tail 생략 없음): `V1013_CODE_MAP.md`(117줄) · `V1013_REVIEW_R9_B.md`(210줄) ·
> `Anode_Fit_v1.0.13.py`(1-899) · `graphite_ica_ch1_v1.0.13.tex`(1-2934) · `graphite_ica_ch2_v1.0.13.tex`(1-776).
> 줄번호는 전부 292f10e 작업본 재실측(Read/Grep, cat -n 기준) — 원본 CODE_MAP·R9_B 수치의 재인용 아님.
>
> **현행 실측 헤더(원본 헤더 L3-8 대체값)**: py **899줄** · ch1 **2934줄** · ch2 **776줄**.
> **boxed 총 38개 = Ch1 31 + Ch2 7** (grep `\boxed` 전수: ch1 31행·ch2 7행 매치).

---

## 0. 원본 대비 변경 항목표 (R9_B M1~M8 처분)

| # | R9_B 지적 | 처분(본 Addendum 반영) | 비고 |
|---|---|---|---|
| M1 | boxed 30→38 (Ch1 23→31); 신규 8건 A절 부재 | **A절에 8행 신설**(§A-신설: 사슬 box·eq:sm-gc·eq:fermifn·eq:sm-muideal·eq:sm-thresh·eq:sm-logistic·eq:sm-nernst·eq:lco-sigmaslot) + 요약 전면 재계산(§4) | 신규 8건 실측 재확인 — R9_B 목록과 집합 일치. R10 에서 boxed 추가 변동 없음(38 유지) |
| M2 | eq:Lq 행 오매핑(구판 tex 라벨 배치 잔재) | **eq:Lq 행 재작성** — 현행 eq:Lq(box ch1 L1542, label L1543) = 용량축 길이 정의식 L_q=\|I\|/(Q_cell·k_j) ↔ `func_L_q`(L103-110)·`_resolve_lag_length` 의 `L_q = func_L_q(...)`(L371). min(...) 컷은 별도 식 eq:Acut(label L1565, C절 행) | 원본의 "min(z_cut·n·RT, A_cap·RT)" 대응은 eq:Acut 소관으로 이동 |
| M3 | D절 "LCO_MSMR_LIT 전자항 x_MIT=0.50 중간 T2-dict" orphan 행 stale | **해당 행 삭제** — loop B 재정렬 완료: 코드 T1 dict `'x_MIT': 0.85`(L666, 주석 L659-660 "재정렬"), tex tab:lco-staging 캡션 L1887-1888 "x_MIT=0.85 물리 anchor 로 배정 — v1.0.13 재정렬 완료". orphan(a) 7건→**6건**, 핵심 발견 연동 수정(§4) | 진단 근거("코드 L630-637 과 대조")가 더 이상 사실 아님 |
| M4 | 헤더 실측치 stale(원본: py 860·ch1 2230·ch2 731) | **재실측 갱신**: py **899** · ch1 **2934** · ch2 **776** (cat -n 기준). R9_B 자신의 수치(883·2768·730)도 현행과 다름 — py 는 R10 정정 커밋(퇴화 스팬 가드·'w'-단독 config 게이트 신설)으로 +16줄, tex 는 R9_B 산정 방식 차이(비어있지 않은 줄 수 계열)로 판단(현행 grep 라벨 위치가 R9_B 실측 대비 +0~+1 이동에 불과) | 본 Addendum 전 표가 292f10e 기준 |
| M5 | 코드 줄번호 전면 stale | **전면 재실측** — 아래 A~E절 완전판의 모든 py 줄번호가 처분. R9_B M5 의 대표값 대비로도 R10 에서 +0~+17 추가 이동(예: eq:vn 분극 437→**438**, LCO_MSMR_LIT 638-659→**655-676**, `_effective_dS_rxn`(LCO) 688-704→**705-721**, `__main__` 747-883→**764-899**) | R10 신설 코드 2건: 퇴화 스팬 가드(L441-446·L497)·config 게이트(L595-600) |
| M6 | tex 줄번호 전면 stale | **전면 재실측** — 아래 표의 모든 tex 줄번호가 처분(예: tab:inputs → **L2758-2795(label 2763)**, eq:lco-plugin box → **L2738-2743(label 2744)**, Ch2 use-this box → **L703-705**) | Ch2 boxed 7건 집합 불변(정합) |
| M7 | `_delith_is_discharge`/`curve()` 환산 미등재 | **A절 신설 행**(M1-⑧ eq:lco-sigmaslot 행)으로 처분 — orphan(b) 아님(tex 가 tab:inputs L2792·sec:facade L2812-2819·boxed eq:lco-sigmaslot 로 문서화 완료) | |
| M8 | dSegate 실측값 온도 명기 | **명기**: 골 깊이 −45.655 J/(mol·K) @T=298 K / **−45.678 @T_ref=298.15 K**(코드 docstring L182 는 "T=298 → ≈ −45.7" 계열, LCO seam 실평가는 T_ref=298.15 → −45.678) | 두 값 모두 재현 검증 완료(R9_B 물리 불변 확인 3 참조) |

**원본 헤더 문구의 현행 정정 2건(추가)**: ① "v1.0.13 실측 boxed 총 30개" → **38개**. ② "tab:inputs(ch1 L2193-2226)" → **ch1 L2758-2795**. 원본 핵심 발견 1(생성자 인자 전수 문서화로 orphan(b) 후보 제외)의 결론 자체는 현행 tab:inputs 에서 그대로 유효(L2783-2786 에 grid_pad·n_work_min·min_lag_grid_steps·v_span_floor·seed_* 전부 실림).

---

## 1. A절 — Ch1 결과박스(boxed) 31개: 문건→코드 (완전판)

줄번호 표기: tex 는 `box 시작-끝(label)`, py 는 현행 실측. "지위" 분류는 원본 체계 유지(1:1 구현 / 구조구현·데이터비활성 / 동결 근사 / 유도 전용 / 부분 구현 / 미구현 / 개념도).

### A-1. 원본 승계 23행 (줄번호·내용 현행화)

| 문건 항목(라벨·현행 줄) | 코드 대응(현행 줄) | 방향 | 지위 | 처분·비고 |
|---|---|---|---|---|
| eq:vn (box L839, label L840) | `dqdv` 분극: `V_n = V_in - sigma_d*I_abs*self.Rn` (L438) | 문건→코드 | 1:1 구현 | 내용 불변, 줄번호만 현행화 |
| eq:Uj (box L922, label L923) | `func_U_j` (L79-80) `(-dH_rxn+T*dS_rxn)/F` | 문건→코드 | 1:1 구현 | codebox(ch1 L932-939)가 seam `_effective_dS_rxn` 경유까지 명시 |
| eq:lco-dUdT (box L2048-2052, label L2053) | `func_U_j` 재사용(LCO 는 `LCOCathodeDQDV._effective_dS_rxn` L705-721 seam 경유 `dS_rxn` 만 치환) | 문건→코드 | 1:1 구현(파라미터 치환) | "같은 함수, 값만 cat" 주장 코드 확인 유지(새 함수 無) |
| eq:dUhys (box L1036-1038, label L1039) | `func_dU_hys` (L136-143) | 문건→코드 | 1:1 구현 | Ω≤2RT→0 분기 포함 |
| eq:Ubranch (box L1056, label L1057) | `func_U_branch` (L146-151) | 문건→코드 | 1:1 구현 | h_eta 인자화 확인 |
| eq:lco-dUhys (box L2164-2171, label L2172) | `func_dU_hys` 재사용(LCO 전이에 호출 경로 개방) | 문건→코드 | **1:1 구현(구조)·비활성(데이터)** | `LCO_MSMR_LIT`(L655-676) 3건 모두 `'Omega'`·`'gamma'` 키 미배정 → 분기 비활성. tex 도 명시(ch1 L2122-2126: "미배정 시 구현은 Ω=0 폴백으로 히스 분기를 비활성") — 문건·코드 양측 선언 일치 |
| eq:lco-Ubranch (box L2175-2177, label L2178) | `func_U_branch` 재사용 | 문건→코드 | 1:1 구현(구조)·비활성(데이터) | 상동 |
| eq:lco-mit (box L2228-2231, label L2232) | 구조적 분리 자체: `func_dU_hys`(L136-143, Ω만 인자)와 `_effective_dS_rxn`(L705-721, 전자항·Ω 무관)가 코드상 별개 함수/경로 | 문건→코드 | 1:1 구현(구조 분리 검증) | "두 몫이 다른 슬롯" = Ω 와 ΔS_e 가 다른 인자·다른 함수로 실증 — 유지 |
| eq:xieq (box L1173, label L1174) | `func_ksi_eq` (L97-100), z≥0/z<0 오버플로 분기 | 문건→코드 | 1:1 구현 | `np.where` 분기 수학적 동치 — tex L1178-1179 가 분기식까지 인용 |
| eq:dSe (box L2330-2331, label L2332) | `func_dSe_molar` 내부(자리당→몰당 전 단계) | 문건→코드 | 유도 중간식 | 코드는 몰당 최종형(eq:dSegate)만 직접 평가 — 유지 |
| eq:U1T2 (box L2377, label L2378) | **미대응** — `_effective_dS_rxn`(L705-721)은 T_ref 동결 상수 오프셋만 사용 | 문건→코드 | **미구현 과제** | 코드 docstring L708-714("P4 미구현, 다온도 round-trip 과제")·tex L2727-2731("동결 구현 → 선형 U(T)") 양측 명시. ½=a_e/2F 인자 tex L2380-2381 확인 |
| eq:ggate (box L2391-2392, label L2393) | `func_dSe_molar` 내부 σ(1−σ) 게이트(L185-187, folded) | 문건→코드 | 1:1 구현(folded) | g(E_F,x) 자체는 별도 반환 없이 dSegate 닫힌식에 흡수 — 유지 |
| eq:dSegate (box L2405-2408, label L2409) | `func_dSe_molar` (L173-188) 전체 | 문건→코드 | 1:1 구현 | 3중 단위가드(leading −·÷e_V(`EV_TO_J` L170)·몰당 R·k_B) 일치. 실측 골: **−45.655 @298 K / −45.678 @298.15 K**(M8 온도 명기) vs 문건 −45.7~−46 |
| eq:eqpeak (box L1340-1342, label L1343) | `equilibrium` 합산 (L395) / `dqdv` 평형분기 (L497 조건, L499 `ksi_eq*(1-ksi_eq)/w`) | 문건→코드 | 1:1 구현 | R10 신설: 평형분기 조건에 `degenerate_span`(스칼라·단일점 퇴화 스팬 가드) 추가 — tex 도 문서화(ch1 L857-858), 아래 C-신설 행 참조 |
| eq:lco-eqpeak (box L2525-2528, label L2529) | `equilibrium`/`dqdv` 동일 코드, `LCO_MSMR_LIT` 3전이(L655-676) 통과 | 문건→코드 | 1:1 구현(코드 일반화로 자동 충족) | 새 함수 불요 — MSMR 동형 주장(sec:lco-code L2630-)이 "구조 변경 0" 실증 — 유지 |
| eq:Lq (box L1542, label L1543) | **[M2 재작성]** 용량축 지연 길이 정의식 L_{q,j}=\|I\|/(Q_cell·k_j) ↔ `func_L_q`(L103-110, Eyring 평가형 eq:Lqfull 의 로그 구현)·`_resolve_lag_length` 의 `L_q = func_L_q(T, I, Q_cell, dH_a_use, dS_a, chi_d, A)`(L371) | 문건→코드 | 1:1 구현 | 원본의 `min(z_cut*n_safe*R*T, A_cap*R*T)` 대응은 **eq:Acut**(label L1565; 코드 L357-360) 소관 — C절 행 참조. 구판 tex 배치 잔재 해소 |
| eq:dHeff (box L1589, label L1590) | `func_dH_a_eff` (L155-158) | 문건→코드 | 1:1 구현 | `use_dH_eff` 토글 on/off (L270, `_chi_and_dH_eff` 분기 L327-328) |
| eq:LV (box L1619, label L1620) | `_resolve_lag_length` 반환 (L376) `abs(dVdq_qa)*L_q` | 문건→코드 | 1:1 구현 | |
| eq:peakshape (box L1704, label L1705) | `dqdv` (L510) `(ksi_eq - occ_lagged)/lag_len_V` | 문건→코드 | 1:1 구현 | |
| eq:sum (box L1792-1794, label L1795) | `dqdv` 누적(L512) + `np.interp`(L514) | 문건→코드 | 1:1 구현 | |
| eq:lco-decomp (box L2593-2595, label L2596) | `LCOCathodeDQDV._effective_dS_rxn` (L705-721) | 문건→코드 | 1:1 구현(부분 folded) | config+vib 는 `LCO_MSMR_LIT` 의 `dS_rxn` 리터럴에 합산(3항 분리 변수 없음) — elec 항만 명시 가산(`func_dSe_molar` 호출 L719-720) — 유지 |
| eq:lco-msmrpeak (box L2683-2686, label L2687) | — (등가성 증명, 별도 코드 불요) | 문건→코드 | 유도 전용(등가성 증명) | MSMR θ(1−θ)/ω ≡ Ch1 ξ(1−ξ)/w — 유지 |
| eq:lco-plugin (box L2738-2743, label L2744) | **부분 구현**: 뒤 3단(`func_U_branch`→`func_ksi_eq`→`equilibrium`/`dqdv`)은 실행 경로, 앞 2단(x 좌표매핑 eq:lco-xmap → V-종속 ΔS_e eq:lco-SeV)은 `tr['x_center']` 고정 스칼라(L719)로 대체 | 문건→코드 | 부분 구현 | tex 자신이 동결 근사를 명문화(L2727-2731 "조성도 x=x_center 로 동결해 V-무관 상수") — 유지 |

### A-2. 신설 8행 (M1·M7 처분 — R9 재구조화分)

| 문건 항목(라벨·현행 줄) | 코드 대응(현행 줄) | 방향 | 지위 | 처분·비고 |
|---|---|---|---|---|
| Part 0 유도 사슬 box (비라벨, box L322-325, sec:sm-found L316) | `func_ksi_eq`→`equilibrium`/`dqdv` 평형 사슬 전체 | 문건→코드 | 개념도(코드 대응 불요) | "미시상태→Ξ→θ→lattice gas→μ(θ;Ω)→ξ_eq→Nernst" — 도착점들이 아래 개별 boxed 로 코드에 닿음 |
| eq:sm-gc (box L386-388, label L389) | — | 문건→코드 | 유도 전용 | 대정준 분배함수 Ξ·Gibbs 인자 — 통계역학 기초, 코드 평가식 아님 |
| eq:fermifn (box L439, label L440) | — (기원식) | 문건→코드 | 유도 전용(`func_ksi_eq` 의 기원) | 단일 자리 점유 θ — 몰당 옷을 입은 최종형이 eq:sm-logistic/eq:xieq 로 코드 도달 |
| eq:sm-muideal (box L494, label L495) | — | 문건→코드 | 유도 전용 | 이상 lattice gas μ(θ) — eq:sm-nernst·eq:mu 의 디딤돌 |
| eq:sm-thresh (box L552-556, label L557) | `func_dU_hys` 의 `if Omega <= two_RT: return 0.0` 분기 (L139-141; 원형 `func_U_j_hys` L87-89 동일 분기) | 문건→코드 | 1:1 구현(판별 분기 대응) | Ω≤2RT ⇔ 단상(gap 0) / Ω>2RT ⇔ 이중웰 — 문턱 판별식이 코드의 명시 분기와 1:1 |
| eq:sm-logistic (box L680-682, label L683) | `func_ksi_eq` (L97-100) | 문건→코드 | 1:1 구현(중복 확인) | Ch1 eq:xieq 와 같은 함수 공유(s=+1 고정·Ω=0 특수형) — Ch2 eq:logistic 과 삼중 재확인 관계 |
| eq:sm-nernst (box L794-798, label L799) | — | 문건→코드 | 유도 전용(이상 극한) | V_eq(ξ)=U+RT/(sF)·ln[ξ/(1−ξ)] — 코드는 이 역함수형을 직접 평가하지 않음(logistic 정방향만) |
| **eq:lco-sigmaslot** (box L1918-1921, label L1922) | `_delith_is_discharge` 클래스 속성(흑연 True L248 / LCO False L703) + `curve()` 전극 인지 환산 분기 `if not self._delith_is_discharge: sigma_d = -sigma_d` (L536-541) | 문건→코드 | **1:1 구현(loop B 구현물)** | σ_d=+1 ⇔ 탈리튬화; 흑연 하프셀 방전↦+1·LCO 하프셀 충전↦+1. 저수준 `dqdv(s=...)` 는 환산 없이 물리 부호 직접(tex sec:facade L2812-2819·tab:inputs L2792 도 문서화) — M7 동시 처분 |

---

## 2. B절 — Ch2 결과박스(boxed) 7개: 문건→코드 (완전판)

| 문건 항목(라벨·현행 줄) | 코드 대응(현행 줄) | 방향 | 지위 | 처분·비고 |
|---|---|---|---|---|
| 서두 사슬 박스 (비라벨, L99) `Z→⟨n⟩→S→∂U/∂T→q_rev` | `func_ksi_eq`→`entropy_coefficient`→`reversible_heat` 파이프라인 | 문건→코드 | 개념도(코드 대응 불요) | 화살표들이 아래 개별 항목에 대응 — 유지 |
| eq:logistic (box L158-159, label L160) | `func_ksi_eq` (L97-100, 동일 함수 — Ch1 eq:xieq 재확인) | 문건→코드 | 1:1 구현(중복 확인) | Ch2 는 통계역학 기원 재유도, 코드는 Ch1 과 공유 — 유지. 각주(L150-152)가 s=+1 유도 전용 부호와 σ_d 혼동 가드 명시 |
| eq:Sconfig (box L224-225, label L226) | **미대응(직접)** — 절댓값 S_config 자체는 코드에 없음 | 문건→코드 | 유도 중간식 | 도함수형(eq:dSconfig L239, 비boxed)만 `entropy_coefficient` 의 config 항으로 구현(L597) — 유지 |
| eq:weighted "단순식" (box L483-485, label L486) | **조건부 대응(R10 갱신)** — `'n'` 키 전이는 코드가 완전식(config 항 포함)으로 평가하나, **`'w'`-단독 전이는 config=0 게이트(L599-600)로 정확히 이 단순식과 일치** | 문건→코드 | 유도 중간식 → **부분 1:1(‘w’-단독 전이 한정)** | R10 신설 config 게이트가 지위를 바꿈: tex 파생 A "전제 명시" srcbox(ch2 L512-520 — "'w'-단독 전이는 T-동결 폭"·"단순식이 옳음")와 코드 분기(L595-600)가 정합. 원본의 "중심값-only 근사 디딤돌" 서술은 'n' 전이에 한해 유지 |
| use-this 완전식 (비labeled box, L703-705) | `entropy_coefficient` (L562-605) 전체, 특히 num/den 합산 L592-603 | 문건→코드 | 1:1 구현 | config 계수 **n_j·R/F**(L597 — v1.0.13 R2 정정 반영: 구판 R/F 는 n_j=1 특수형) + `'w'`-단독 게이트(L595-600). 독립 재구현 대조 실측 diff 1.08e-19(과거 감사) 유효 |
| eq:hys_rev (box L608-609, label L610) | `entropy_coefficient` 가 평형 중심 U_j(히스 shift 無) 사용 (L586) | 문건→코드 | **동결 근사(자동)** | 분기별 평균을 직접 계산하지 않고 평형 중심으로 근사 — docstring(L574-576) "γ 대칭 전제, 비대칭 분기별 ∂U/∂T 미구현" 명시. tex 도 선형화 근사 한정 명시(ch2 L612-615) — 유지 |
| eq:qrev (box L675, label L676) | `reversible_heat` (L607-618) `-I*T*entropy_coefficient(...)` (L618) | 문건→코드 | 1:1 구현 | T 한 번(T² 아님) 확인. R9 정정 반영: 라벨 층위 주의(Bernardi 셀-수지 '방전 I>0' = 흑연 하프셀 리튬화)가 코드 docstring L612-615·tex L680-683 양측에 명문화 |

---

## 3. C절 — 비-boxed 이지만 명시적 코드 대응 식 (완전판)

문건이 `\boxed{}` 없이 본문 `\code{...}` 로 코드 식별자를 직접 지목하는 식들 — orphan 판정 제외.

### C-1. 원본 승계 10행 (현행화)

| 문건 항목(현행 줄) | 코드 대응(현행 줄) | 지위 |
|---|---|---|
| eq:vwork (L850-854) 작업격자 | `dqdv` L450 `V_work=np.linspace(...)`; `grid_pad_lo/hi`·`n_work_min`(생성자 L256-257, 가드 L273-275) | 1:1 구현 — tab:inputs L2783 재확인 |
| eq:branch (L1715-1721) 꼬리/평형 전환 | `dqdv` L497 `if degenerate_span or ... lag_len_V < self.min_lag_grid_steps*grid_step` | 1:1 구현 — ν=2(tab:inputs L2784). ν 문턱 점프 닫힌식·ν≳10 권고는 ch1 L1726-1730(각주 포함) |
| eq:reversal (L1737-1743) 충전 격자역전 | `dqdv` L505-508 `ksi_arr[::-1]` 필터 후 재역전 | 1:1 구현 |
| eq:center (L1066-1072) 분기중심 선택 | `dqdv` L479-485 `if gamma!=0 and Omega>0: center=U_j+hys_shift(L482-483) else U_j` | 1:1 구현 |
| eq:lowpass (L1663-1665) 이산 저역통과 | `_causal_lowpass` (L113-131; lfilter 우선·점화식 폴백) | 1:1 구현 |
| eq:Acut (L1562-1565) 컷 affinity 상한 | `_resolve_lag_length` L357-360 `A = min(z_cut*n_safe*R*T, A_cap*R*T)`; per-tr override `z_cut`/`A_cap_RT`(L358-359) | 1:1 구현 — **M2 재배정의 수용처**(원본 eq:Lq 행의 min-컷 대응이 이 행 소관) |
| eq:chid (L1575-1578) 방향별 전달계수 | `func_chi_d` (L161-166) + `chi_split` 주입(기본값 L253, callable 가드 L267-269, `_chi_d` L316-319) | 1:1 구현 |
| eq:lco-xmap (L2700-2702) x=x(ξ_eq,1(V)) | **미구현** — `_effective_dS_rxn` 은 `tr['x_center']` 고정 스칼라 사용(L719) | 미구현 과제(문건·코드 양측 tier-C 명시: tex L2704 "단순 선형보간(tier C)·함수형 확정은 round-trip 피팅 몫") |
| eq:lco-SeV (L2708-2713) ΔS_e(V,T) | **미구현(V-종속형)** — 코드는 `func_dSe_molar(x_center, T_ref=298.15, ...)` 1회 평가 후 상수 오프셋(L717-720) | 동결 근사 — V-격자 실시간 평가 아님 |
| eq:lco-U1V (L2719-2725) U_1(V,T) 적분형의 동결 근사 | `_effective_dS_rxn`(L705-721) 전체 로직 | 1:1 구현(동결 근사형) — 코드가 실제 쓰는 식은 eq:U1T2 완전형이 아니라 이 동결형(tex L2727-2731 자체 명문화) |

### C-2. 신설 4행 (R10 신설 가드 2건 + 명시 대응 보강 2건)

| 문건 항목(현행 줄) | 코드 대응(현행 줄) | 지위 |
|---|---|---|
| 퇴화 스팬 가드 서술 (ch1 L857-858: "스팬 Δv 는 하한 v_span_floor=10⁻⁶ V 로 바닥진다(단일점·스칼라 입력의 격자 퇴화 가드)") | `dqdv` L441-446 `degenerate_span = (v_hi-v_lo) < self.v_span_floor` + 분기 조건 합류 L497 — **R10 신설(스칼라 입력 평형 분기 강제)** | 1:1 구현 — 배열 스윕 경로 불변(흑연 회귀 bit-exact 유지, 주석 L441-444) |
| 'w'-단독 config 게이트 서술 (ch2 L512-520 파생 A 전제 명시 srcbox; config 계수 n_j·R/F 는 eq:dxidT L469-477·eq:single_config L553) | `entropy_coefficient` L595-600 `if tr.get('n') is not None: config=(n_j*R/F)*log(...) else: config=0.0` — **R10 신설** | 1:1 구현 — 'w'-단독 = T-동결 폭 → 단순식(eq:weighted)과 일치(B절 eq:weighted 행 참조) |
| eq:n0map (L206-210) 실험조건 매핑 | `curve` (L518-548) + `_direction_to_sigma` (L630-644) + `I_use = c*Q_cell`(L545) | 1:1 구현 — tab:nodemap N0 행(L2830)이 직접 지목 |
| eq:wbase (L1116-1118) 폭 w=nRT/F | `func_w` (L75-76) + `_width` (L310-313) + `_n_factor` 'w'→n 역산 (L301-307) | 1:1 구현 — tab:nodemap N4 행(L2834) 직접 지목 |

---

## 4. D절 — Orphan (a): 문건O·코드X (완전판 — M3 반영 **6건**)

| 문건 항목(현행 줄) | 지위 | 근거 |
|---|---|---|
| eq:U1T2 (box L2377) 전자항 T² 곡률 | **미구현 과제** — 동결 근사(eq:lco-U1V)로 대체 | 코드 docstring L708-714, tex L2727-2731 양측 명시 |
| eq:lco-xmap (L2702) 좌표매핑 x=x(ξ_eq,1(V)) | **동결 근사(tier-C)** — `x_center` 고정 스칼라(L719) | tex L2704(선형보간 tier C)·L2622-2624(★Ch2/P4 코드 구현 예고 (i)) 명시 |
| eq:hys_branch (ch2 L603, label) 분기별 ∂U/∂T | **동결 근사(자동)** — 평형 중심 U_j 사용으로 근사 | 코드 docstring L574-576 "Ch2 범위 밖 선언, 후속 과제" |
| eq:ensavg (ch1 L1425-1429) 앙상블 ρ(U_app) 합성곱 broadening | **미구현 과제(forward-only 명시 배제)** — 단일 유효입자+L_V 구조 유지 | tex L1459-1468 (ii)(iii): "역산 ill-posed·forward-only"·"다입자 기계장치는 모델에 넣지 않는다" |
| procedurebox (ch2 L725-742) ΔS⁰_j 다온도 round-trip 식별 절차(1-5단계) | **미구현(스코프 밖)** — Optuna 등 외부 피팅 스크립트 영역 | `Anode_Fit_v1.0.13.py` 는 forward 모델만(피팅 루프 없음, 파일 전체 재확인 1-899) |
| eq:lco-dUhys/eq:lco-Ubranch (Ch1) | **구조 구현·수치 비활성** — A절 해당 행 참조 | `LCO_MSMR_LIT` 3-dict 전수 재확인(L655-676): `'Omega'`·`'gamma'`·`'dH_a'` 키 전부 없음 → 분기·꼬리 비활성(실질 방향 의존 = 분극뿐, tex L2122-2126·코드 주석 L688-689 정합) |

**[M3 삭제 행]** ~~"LCO_MSMR_LIT 전자항 배정(x_MIT=0.50, 중간 T2-dict) — 물리 anchor 불일치"~~ → loop B 재정렬 **완료**로 orphan 아님: 코드 T1 dict `'x_MIT': 0.85`(L666)·`'x_center': 0.85`(L665), tex tab:lco-staging 캡션 L1887-1888 "v1.0.13 재정렬 완료".

**q_irr 3분해(I²R+Iη_ct+Iη_diff)** — 원본 D절 마지막 행의 지위 유지: boxed 식 자체가 Ch2 에 없어 orphan 아닌 "정직한 부재". 코드 docstring L622-626(lumped-only 선언)·tex ch2 L716-723 한계 (1)~(5) 정합. (본 완전판에서는 D절 표 밖 메모로 유지 — 문건O·코드X 요건 자체를 충족하지 않으므로.)

---

## 5. E절 — Orphan (b): 코드O·문건X (완전판 — 6건, M7 은 A절로 이관)

| 코드 항목 | 위치(현행) | 지위·비고 |
|---|---|---|
| `_finite`/`_finite_pos`/`_finite_nonneg` 가드 3종 + 전 호출부 `ValueError` fail-fast | L192-213, 생성자(L262-277)·`dqdv`(L420-435)·`_resolve_lag_length` 전역 | **코드 전용** — 입력 검증 메커니즘은 물리식이 아니라 엔지니어링 관행(정상). tab:inputs 는 인자 기본값·역할만 표로 제공 |
| `_build_seed_L_V` 내부 메커니즘(대표 방전조건 1회 선호출) | L291-298(유래 주석 L279-284) | **코드 전용** — `seed_T/I/Q_cell` 파라미터는 tab:inputs L2786 에 있으나 "원본 List 문자열 키 대입 TypeError 우회" 유래는 유지보수 이력 |
| `curve()` 방향 문자열 별칭 전수(`"dis"`,`"d"`,`"+"`,`"+1"`,`"1"`,`"sigma+"` / `"chg"`,`"c"`,`"-"`,`"-1"`,`"sigma-"`) | `_direction_to_sigma` L630-644(별칭 튜플 L637-639) | **코드 전용(경미)** — 문건은 대표 예만(ch1 L2813-2814·L528 docstring 계열), 코드 별칭이 더 많음. 물리 무관 문서화 갭 |
| `__main__` self-test 스위트(가드 7종·chi_split A/B·히스 분기·꼬리 역전·극한 reduction·per-tr override 격리) | L764-899 | **코드 전용(검증 인프라)** — boxed 식(S1-S8·R1-R5 부호사슬)을 실행 검증하는 유일 코드 경로. tex sec:signcheck(L2853-2906)의 R1-R3 이 "코드 __main__ self-test 와 같은 양의 수기 재산출"로 상호 참조하므로 완전한 orphan 은 아님 |
| `func_U_j_hys` (원형 보존) | L83-94 | **부분 orphan — 미사용 원형(dead code)** — R10 에서 docstring L85-86 이 "현 활성 경로 미호출(동등 물리, CODE_MAP orphan(b))" 를 **코드 자체에 명문화**(신규). 활성 경로는 분리형 `func_dU_hys`+`func_U_branch` |
| `LCOCathodeDQDV` 가 상속만으로 6개 메서드(`equilibrium`/`dqdv`/`curve`/`entropy_coefficient`/`reversible_heat`/`irreversible_heat`)를 재정의 없이 물려받는 사실 | L679-721(클래스 전체 — 재정의는 `_effective_dS_rxn`·`_delith_is_discharge` 뿐) | **코드 전용(구조적 사실)** — "구조 변경 0" 주장(sec:lco-code)의 실증. 실질은 orphan 아닌 근거 보강 |

**[M7 이관]** `_delith_is_discharge`·`curve()` 환산 분기는 E절이 아니라 **A절 신설 eq:lco-sigmaslot 행**이 정위치(문건이 boxed+표+절로 3중 문서화).

---

## 6. 요약 (전면 재계산 — 원본 §요약 대체)

- **문건→코드 boxed 매핑**: Ch1 31 + Ch2 7 = **38건**, 전부 대응 확인.
  - Ch1 31 = 1:1 구현 **19**(vn·Uj·lco-dUdT·dUhys·Ubranch·xieq·dSegate·ggate[folded]·eqpeak·lco-eqpeak·Lq·dHeff·LV·peakshape·sum·lco-decomp[부분 folded]·sm-thresh[분기 대응]·sm-logistic[중복 확인]·**lco-sigmaslot[신설]**) / 구조구현·데이터비활성 **2**(lco-dUhys·lco-Ubranch) / 구조 분리 검증 **1**(lco-mit) / 유도 전용 **6**(sm-gc·fermifn·sm-muideal·sm-nernst·dSe·lco-msmrpeak) / 개념도 **1**(Part 0 사슬 box) / 부분 구현 **1**(lco-plugin) / 미구현 **1**(U1T2).
  - Ch2 7 = 개념도 1(서두 사슬) / 1:1 구현 2(use-this 완전식·qrev) / 1:1 중복 확인 1(logistic) / 유도 중간식 1(Sconfig) / 유도 중간식→부분 1:1 1(weighted — R10 'w'-단독 게이트로 승격) / 동결 근사 1(hys_rev).
- **Orphan (a) 문건-만**: **6건**(M3 로 1건 삭제) — eq:U1T2·eq:lco-xmap·eq:hys_branch·eq:ensavg·procedurebox·eq:lco-dUhys/Ubranch(데이터 비활성). 전부 문건·코드 양측 명시 선언(미서술 누락 0).
- **Orphan (b) 코드-만**: **6건** — 가드 3종·seed_L_V 메커니즘·방향별칭 전수·self-test 스위트·`func_U_j_hys`(미사용 원형 — R10 에서 코드 자체가 지위 명문화)·LCO 상속 사실. 근거 없는 창작(진짜 orphan) **0건**.

### 핵심 발견 현행판 (원본 5건의 상태 갱신 + 신규 2건)

1. [유지] tab:inputs(현행 L2758-2795)의 생성자 인자 전수 문서화 — v1.0.11 "코드-only 후보"들의 orphan(b) 제외 유효(L2783-2786).
2. [유지] LCO 히스테리시스 박스는 구조 완비·수치 비활성(`LCO_MSMR_LIT` 에 Omega/gamma/dH_a 없음) — "구현됨"과 "발현됨"의 분리 사례.
3. [유지] eq:lco-plugin 5단 사슬은 부분 구현(앞 2단 = x_center 동결 스칼라).
4. [갱신] `func_U_j_hys` dead code — R10 에서 **docstring 이 미호출·orphan(b) 지위를 코드 자체에 명문화**(L85-86). 정리 후보 지위는 유지하되 "문서화 갭"은 해소.
5. [유지] 근거 없는 창작 0건.
6. [신규] **R10 신설 가드 2건이 양측 문서화로 완결** — 퇴화 스팬 가드(코드 L441-446·L497 ↔ ch1 L857-858)·'w'-단독 config 게이트(코드 L595-600 ↔ ch2 L512-520). 코드-문건 동기화가 R10 침묵 오차 정정에서도 유지됨.
7. [신규] loop B(전극 인지 환산 + 전자항 T1 재정렬)가 **boxed 신설(eq:lco-sigmaslot)·표(tab:lco-staging·tab:inputs L2792)·코드(_delith_is_discharge·x_MIT=0.85)** 3자 정합으로 닫힘 — R9_B M1-⑧/M3/M7 의 뿌리가 전부 이 한 쌍의 구현·문서화.

---

*P6.1 작업 sub 산출 — 원본 `V1013_CODE_MAP.md`·검수 `V1013_REVIEW_R9_B.md` 무수정. 기준 커밋 292f10e.*
