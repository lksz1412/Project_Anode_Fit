# V1.0.10 P5 최종점검 — 감사 드래프트 O2 (B조: code↔Ch2 상호충실도)

> 역할: Anode_Fit v1.0.10 P5 최종 동시 점검 9종 감사 드래프트 **O2** (조: **B조 = code↔Ch2 발열 상호충실도**).
> ★감사 의견만 — 코드/문건 수정 절대 X(정정·그래프는 master). 독립 작성. 추정 시 tier 명시.
> 정독 커버리지(head→tail 전영역): 코드 `docs/v1.0.10/Anode_Fit_v1.0.10.py`(1-850 전체) · Ch2 `graphite_ica_ch2_v1.0.10.tex`(1-751 전체) · Ch1 `graphite_ica_ch1_v1.0.10.tex`(LCO/전자엔트로피/eq:U1T2/eq:ggate 절 정독) · 앵커 P1·P3·P4 RESULT.md(P4 이월 4항 정독).
> 4-tier: **[확정]** 코드 줄·tex 식 이중근거 / **[근거미발견]** 문헌·boxed 부재 / **[추정]** / **[미검증]**.

---

## 0. B조 초점 요약 (한눈)

Ch2 발열 3식(eq:qrev·eq:weighted·eq:hys_rev)과 코드 3메서드(`entropy_coefficient`·`reversible_heat`·`irreversible_heat`) + seam(`_effective_dS_rxn`)의 **양방향 1:1**을 재검산했다. 결론: **B조 발열 코어는 물리·부호·차원·이중계산 직교가 모두 확정 정합**이며, 코드→Ch2 역방향에도 boxed-식 없는 미구현 주장이 없다(비가역 3분해가 대표 검증 포인트 — 아래 B-1). 확정 갭 = **0건(CRITICAL/HIGH)**, 문서정합·라벨 관찰 = **4건(전부 MEDIUM 이하, P4 이월과 동일 클래스)**.

---

## 1. Ch2→코드 방향 매핑 (문건 각 발열 식이 코드에 1:1 있나)

| Ch2 식 (tex 줄·라벨) | Ch2 내용 | 코드 심볼 (py 줄) | 판정 |
|---|---|---|---|
| eq:qrev (L642-646) `Q̇_rev=−I·T·∂U_oc/∂T=−(I·T/F)ΔS` | 가역 발열, T 한 번 | `reversible_heat` (L578-586) `−float(I)*T*entropy_coefficient(V_n,T)` | **[확정] 정합** |
| eq:qrev 첫 항 (L643·648) `Q̇_irr=I(U_oc−V)≥0` lumped | 과전압 소산 | `irreversible_heat` (L588-596) `I*(U_oc−V)` | **[확정] 정합** |
| eq:weighted 완전식 (use-this box L672-674) `∂U/∂T=Σ Q_j g_j[ΔS⁰_j/F+(R/F)ln(ξ_j/(1−ξ_j))]/Σ Q_j g_j`, `g_j=ξ_j(1−ξ_j)/w_j` | 겹침 가중 + 봉우리 내부 config | `entropy_coefficient` (L544-576) | **[확정] 정합** |
| eq:gj (L453-455) `g_j=ξ_j(1−ξ_j)/w_j` | 국소 dQ/dV 비중 | `g = xi*(1-xi)/w` (L569) | **[확정] 정합** |
| eq:single_config (L527-530) config 항 `+(R/F)ln[ξ_j/(1−ξ_j)]` | 봉우리 내부 분포 항 | `config=(R/F)*np.log(xi_c/(1-xi_c))` (L571) | **[확정] 정합** (부호·인자 동일) |
| 파생 B warnbox (L293-309) 이중계산 금지: dqdv 무가산 / q_rev 가산 | 직교 비대칭 | `dqdv` peak_shape=`ksi_eq*(1-ksi_eq)/w` (L486,497 — config 無) vs `entropy_coefficient` +config (L571,573) | **[확정] 정합** |
| eq:hys_rev (L581-584) `∂U_rev/∂T=½(∂U_ch/∂T+∂U_dis/∂T)` | 가역열 = 분기 평균 | `entropy_coefficient` 이 평형중심 U_j 사용(hys shift 無, L562·568) = 분기평균 등가 | **[근거미발견/암묵적]** 아래 B-2 |
| eq:qrev 부호규약 (srcbox L650-654) `ΔS=+F ∂U_oc/∂T`, 방전 ΔS>0→흡열 | 흡·발열 부호 | `reversible_heat` docstring L583 규약 동일 | **[확정] 정합** |
| Ch1 eq:dSegate 전자항(발열 경로 진입) `ΔS_e=−(π²/3)R(kBT/e_V)(g_max/dx)σ(1−σ)` | MIT 전자 엔트로피 | `func_dSe_molar` (L170-185) | **[확정] 정합** (B조 경계상 Ch1 식이나 q_rev 경로 필수 — 아래 B-3) |

### 재검산 근거 (핵심 3식)

**(1) T 한 번 [확정].** `entropy_coefficient`(L575)가 `dUdT = num/den` 로 `∂U/∂T` [V/K]를 반환하고, `reversible_heat`(L586)이 `−I·T·(∂U/∂T)` 로 **T를 정확히 한 번** 곱한다. eq:qrev(L644-645)와 차원 일치: [A]·[K]·[V/K]=[W]. **T² 없음** 확정(코드에 `T*T`·`T**2` 부재, `entropy_coefficient` 내부는 `dS_eff/F`(V/K)와 `config`(V/K)만 — T 명시 곱 없음). P4 adversarial 항목7(factor-2)이 여기 아니라 **LCO override의 dSe(T) 온도스케일**에서 발생했고, master가 T_ref=298.15 동결로 해소함(`_effective_dS_rxn` L659-664 라벨) — B조 재확인: 동결 후 dS_eff가 T-무관 → `func_U_j(T)=(−ΔH+T·dS_eff)/F` T-선형 → `∂U/∂T=dS_eff/F` 가 세 경로(equilibrium/dqdv/entropy_coefficient) 일관. **factor-2 재발 없음 [확정]**.

**(2) 이중계산 직교 [확정].** Ch2 파생 B(L293-309)의 핵심 = "dqdv 곡선은 config 항을 넣지 않는다(폭 w가 이미 담음) / q_rev 경로만 명시 가산". 코드 재검산:
- `dqdv`(L486,497): peak_shape = `ksi_eq*(1-ksi_eq)/w` (평형 종) 또는 `(ksi_eq−occ_lagged)/lag_len_V` (지연) — **config log 항 無**.
- `entropy_coefficient`(L571-573): `num += Qg*(dS_eff/F + config)` — **config 명시 가산**.
두 경로가 같은 `func_ksi_eq`·같은 seam(`_effective_dS_rxn`)을 공유하되 config만 비대칭. Ch2 warnbox(L299) "config를 ΔS⁰_j에 또 더하면 이중계산" 을 코드가 정확히 회피. **직교 확정** — dict 원본(`tr['dS_rxn']`)은 seam base가 `return tr['dS_rxn']`(L542)로 미오염(P4 항목1-6 삼각검증 재확인).

**(3) 부호·차원 [확정].** eq:qrev srcbox(L650-654): `ΔS=−∂(ΔG)/∂T=+F·∂U_oc/∂T`, `Q̇_rev=−IT·∂U/∂T`. 코드 `reversible_heat` docstring(L583) "방전 I>0: ΔS>0(∂U/∂T>0)→q_rev<0 흡열 / ΔS<0→발열" — Ch2 L658-660 서술과 부호 완전일치. `irreversible_heat`(L596) `I*(U_oc−V)` 은 eq:qrev(L643) `I(U_oc−V)≥0` 과 부호·형태 일치.

---

## 2. 코드→Ch2 방향 매핑 (각 발열 메서드가 Ch2 식 근거 있나)

| 코드 메서드 (py 줄) | 근거 Ch2 식 | 판정 |
|---|---|---|
| `_effective_dS_rxn` base (L533-542) seam 항등 `return tr['dS_rxn']` | Ch2 use-this box 입력 ΔS⁰_j (L676-677) | **[확정]** seam은 아키텍처 장치(3경로 공유), 물리 불변 |
| `entropy_coefficient` (L544-576) | eq:weighted 완전식 (L672-674) | **[확정]** 1:1 |
| `reversible_heat` (L578-586) | eq:qrev (L645) | **[확정]** 1:1 |
| `irreversible_heat` (L588-596) lumped만 | eq:qrev 첫 항 lumped (L643·648) | **[확정]** — **Ch2에 3분해 boxed 부재 재확인(grep 0)**, 코드 주석 L590-594 정확 |
| `LCOCathodeDQDV._effective_dS_rxn` (L655-671) 전자항 T_ref 동결 가산 | Ch1 eq:dSegate(전자)·eq:U1T2(T² 곡률) | **[확정/이월]** 동결근사, 다온도 T² 미구현 라벨(P4 이월) |
| `func_dSe_molar` (L170-185) | Ch1 eq:dSegate | **[확정]** (Ch1 식이나 q_rev 경로 물리) |

**코드없는Ch2주장·Ch2없는코드기능 = 0 [확정].** 발열 코어에서 코드가 Ch2에 없는 발열 물리를 추가하지 않았고(예: 임의 T² 곡률·3분해 하드코딩 부재), Ch2가 요구하는 발열 식(eq:qrev·eq:weighted·eq:hys_rev·eq:qrev-irr)은 전부 code-backed. 유일한 "부분" = eq:hys_rev의 명시적 2분기 계산(B-2)과 다온도 T² 곡률(B-4) — 둘 다 미구현이 아니라 **암묵적 등가/의도적 이월**이며 Ch2·P4가 범위밖·이월로 명시.

---

## 3. 확정 갭·관찰 (위치·무엇이·맞는 형태)

### B-1. [확정·정합확인 / 갭 아님] 비가역 3분해 — 코드 lumped ↔ Ch2 boxed 부재 일치
- **위치**: 코드 `irreversible_heat` L588-596(lumped `I(U_oc−V)`, 주석 L590-594) ↔ Ch2 `graphite_ica_ch2_v1.0.10.tex` eq:qrev L643·L648(lumped "과전압 소산").
- **검산**: Ch2 전문 grep(`η_ct|η_diff|I²R|3분해|과전압 분해`) = **0 매치**. 최종 Ch2 v1.0.10에 3분해 boxed 식이 **없음** 확정. 코드가 lumped만 둔 것은 최종 문건과 **정합**.
- **판정**: **갭 아님(정합)**. 단, **P3 RESULT.md 트레일 주의** — P3 result(L23·L54)는 O1의 "비가역 3분해(I²R+Iη_ct+Iη_diff)"를 체리픽 vN-10에 넣었다고 기록하나, finalizer 편입표(P3 result L31-41 byte보존)는 이를 최종 tex에 넣지 않았다(최종 tex grep 0). 즉 **3분해는 v10 map의 stale 중간산물이며 최종 Ch2에 미반영** — 코드 주석 L590-594 "Ch2에 boxed 식 없다"가 최종본 기준 정확. **정정 불필요**(코드·최종문건 모두 정합). *master 참고: P4 이월 "비가역 3분해"(P4 result L57)는 "율의존 피팅 과제"로 올바르게 분류됨.*

### B-2. [근거미발견/암묵적] eq:hys_rev 분기평균 — 코드는 평형중심으로 등가 달성(명시 2분기 계산 부재)
- **위치**: Ch2 eq:hys_rev L581-584 `∂U_rev/∂T=½(∂U_ch/∂T+∂U_dis/∂T)` ↔ 코드 `entropy_coefficient` L559-568(평형중심 `U_j` 사용, `func_ksi_eq` default s=+1, **hys shift 無**).
- **분석**: `entropy_coefficient`는 `func_U_branch`/`hys_shift`(L469)를 호출하지 않고 순수 평형중심 `U_j`(L562)로 ξ를 평가한다. 히스 분기 ±½ΔU_hys는 방·충 대칭이라 **평형중심 = 두 분기의 평균중심**이므로, 코드는 eq:hys_rev의 "분기 평균" 결과를 **평형중심 사용으로 암묵 달성**한다(별도 2분기 계산·½평균 코드 없음).
- **판정**: **물리적으로 정합하나 명시성 부재**. 대칭 히스(γ 단일값·h_η 대칭)에서는 정확 등가. **비대칭 분기**(예: 방·충 γ 다름, chi_split 커스텀)일 때만 평형중심≠½평균이 되어 어긋날 수 있으나, 현재 모델은 γ가 전이당 단일값(L464)이라 항상 대칭 → 실사용 무결.
- **맞는 형태(옵션, master 판단)**: 코드 정정 불필요. 다만 `reversible_heat`/`entropy_coefficient` docstring에 "히스 분기평균(eq:hys_rev)은 평형중심 사용으로 자동 달성 — γ 대칭 전제" **1줄 라벨** 추가하면 code↔Ch2 추적성 완결(현재는 독자가 등가를 추론해야 함). tier: 문서정합 MEDIUM.

### B-3. [확정/이월] LCO x_MIT 문서 불일치 (P4 이월 재확인)
- **위치**: 코드 `LCO_MSMR_LIT` L632 `'x_MIT': 0.50, 'x_center': 0.50` ↔ Ch1 eq:ggate L1070 `x_MIT≈0.85`(2상역 x≈0.75-0.94, L1098-1099).
- **분석**: 발열 경로(`func_dSe_molar`→seam→`entropy_coefficient`→`reversible_heat`)가 `x_MIT`를 소비하므로 **B조(발열) 경계 내**. 코드 값 0.50은 Ch1 anchor 0.85와 0.35 어긋남. 단, 코드는 L619-620에서 **"tier-C 시연 기본값 — round-trip 피팅 前 placeholder(실측 신뢰값 아님)"** 명시 라벨 보유 → **내부적으로 정직**. `dH_rxn`(L630)도 `x_center=0.50` 기준 재보정된 정합값이라 코드 내부는 self-consistent.
- **판정**: **P4 이월(P4 result L54)과 동일 확정 항목**. CRITICAL 아님(placeholder 라벨로 방어). round-trip 피팅 단계에서 물리값(0.85 계열) 정정 + 문서 정합이 정답.
- **맞는 형태(master)**: 코드 `x_MIT`/`x_center`를 0.85 계열로 갱신하거나(그러면 `dH_rxn` 재보정 필요), 또는 L619-620 라벨에 "Ch1 eq:ggate anchor x_MIT≈0.85와 시연 편의상 상이(피팅서 정정)" **명시 cross-ref 1줄** 추가. 현 시점 정정은 round-trip 피팅 과제로 이월 유지가 합리적(P4 판단 계승).

### B-4. [확정/이월] 다온도 T² 곡률 미구현 — 라벨 정합 확인
- **위치**: 코드 `LCOCathodeDQDV._effective_dS_rxn` L659-664(T_ref=298.15 동결 상수 오프셋, "단일-기준 근사") ↔ Ch1 eq:U1T2 L1056-1060(전자항 T² 계수 `a_e/(2F)`, ½ 인자).
- **분석**: eq:U1T2는 전자항 `ΔS_{e,j}∝T`(Ch1 L1154)라 `∂U/∂T`가 T-선형이고 U-이동은 ∝T²(Ch1 L1210-1211). 코드는 dSe를 T_ref에서 동결해 T² 곡률을 **의도적으로 배제**(L662-664 라벨: "Sommerfeld T-스케일·eq:U1T2 center-T_ref 별도적분(½=a_e/2F)은 다온도 round-trip 피팅 단계 과제로 분리(P4 미구현)"). **라벨이 Ch1 식·P4 이월과 정확 대응**.
- **판정**: **미구현이 명시·라벨됨 = 정직 갭(P4 result L55 이월과 동일)**. 단일온도 발열 산출은 무결(factor-2 해소). **정정 불필요**, 이월 유지.
- **맞는 형태(master)**: 다온도 round-trip 피팅 구현 시 `_effective_dS_rxn`에 T-의존 dSe(Sommerfeld ∝T) 복원 + `func_U_j`의 center-T_ref 별도적분(½ 인자). 현재는 라벨로 충분.

---

## 4. 공통 산출 — 3대 무결 최종 확인

| 무결 축 | 판정 | 근거 |
|---|---|---|
| **물리 배경 정확** | **[확정] PASS** | eq:qrev/eq:weighted/eq:qrev-irr ↔ 코드 부호·차원·T-count·이중계산직교 재검산 무결. 가역열=−(IT/F)ΔS(x), 흡·발열 부호교대 Ch2 L658-663 정합. |
| **코드 정확** | **[확정] PASS** | `reversible_heat`(T 한 번)·`entropy_coefficient`(완전식 Σ Q_j g_j[ΔS/F+config])·`irreversible_heat`(lumped)·seam 3경로 공유. 흑연 0-diff(P4 검증 13/13 bit일치, seam base `is tr['dS_rxn']`). |
| **사용자 의도 반영** | **[확정] PASS** | tier-C placeholder·미구현 항목 전부 inline 라벨(x_MIT L619·T² L662·3분해 L592) — "문헌값=초기값, 피팅으로 정정" 철학 계승. 식별자·정수코드·死코드(func_U_j_hys) 보존. |

**P4 이월 4항 문서정합·라벨 확인** (P4 result L53-58):
- x_MIT=0.50 tier-C → **B-3 [확정]** 라벨 有, round-trip 이월 유지 타당.
- 다온도 T² 곡률 → **B-4 [확정]** 라벨 有(eq:U1T2 대응), 이월 유지 타당.
- LCO 시연 파라미터 tier-C → 코드 L619-620·L675 라벨 有, round-trip 이월 타당.
- 비가역 3분해 → **B-1 [확정 정합]** Ch2 boxed 부재와 코드 lumped 일치, 율의존 피팅 이월 타당.
→ **4항 전부 라벨 정합·이월 분류 정확. 신규 확정 CRITICAL/HIGH 갭 0.**

---

## 5. 5줄 요약

1. **조**: B조 = code↔Ch2 발열 상호충실도. 코드(1-850)·Ch2(1-751)·Ch1(발열/LCO 절)·P1·P3·P4 전영역 정독.
2. **확정 갭 수**: CRITICAL/HIGH **0건**. 관찰 4건(B-1 정합확인 / B-2 암묵등가 / B-3·B-4 P4이월 재확인) — 전부 MEDIUM 이하·정정불필요 또는 이월.
3. **최중대 갭(관찰)**: B-2 — eq:hys_rev(분기평균) 명시 2분기 계산 부재, 평형중심 사용으로 **암묵 등가 달성**(γ 대칭 전제 무결, 비대칭 시만 이론적 어긋남). 물리 무결, 추적성만 라벨 권고.
4. **정정 목록(master, 전부 옵션·저위험)**: (B-2) `entropy_coefficient`/`reversible_heat` docstring에 "히스 분기평균=평형중심 자동달성(γ대칭)" 1줄 · (B-3) `LCO_MSMR_LIT` L619-620 라벨에 "Ch1 x_MIT≈0.85와 상이(피팅정정)" cross-ref 1줄. **코드 로직 정정 0 · CRITICAL 정정 0.**
5. **리스크**: 낮음. 발열 코어 T-count/부호/차원/이중계산직교 삼각확정. 잔여 = round-trip 피팅 단계 물리값화(x_MIT·다온도 T²·LCO tier-C·비가역 3분해) — 전부 코드에 정직 라벨·P4 이월과 동일 클래스, P5에서 신규 결함 아님.
