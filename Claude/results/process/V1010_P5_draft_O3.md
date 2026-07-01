# V1010 P5 감사 드래프트 — O3 (C조: 내용 완성도 + 코드없는내용 0 + 피팅 추천 + 그래프 suite)

> 역할: Anode_Fit v1.0.10 P5 최종 동시 점검 9종 **감사 드래프트 O3** (조 = **C조**). ★감사 의견만 — 코드/문건 수정 X(정정·그래프는 master). 독립 작성. 추정 금지(코드 줄·tex 식 근거). refute 우선·빈 통과 금지·허위적발 금지.
> 작성 2026-07-01. 정독 커버리지 head→tail 전영역: `Anode_Fit_v1.0.10.py`(740줄) · `graphite_ica_ch1_v1.0.10.tex`(1816줄) · `graphite_ica_ch2_v1.0.10.tex`(705줄) · P1~P4 RESULT 4종 + demo_lco_heat.py(65줄)·plot_dqdv.py(115줄).
> 4-tier 표기: **[확정]**=코드 줄·tex 식 직접 근거 / **[근거미발견]**=코드/문건으로 못 짚음 / **[추정]**=설계 의도 추론 / **[미검증]**=실증 대기.

---

## 0. 결론 요약 (먼저)

C조 4초점 전수 점검 결과, **확정 갭 6건**(문서↔코드 라벨/값 4 + 완성도 서술 2), 그 외는 대체로 무결·code-backed. **최중대 갭 = C-G1(LCO 데이터셋 이름 문서=`LCO_STAGING_LIT` vs 코드=`LCO_MSMR_LIT` 불일치, "이 문건만으로 코드 재현" 자기완결성 직접 저해)**. **코드 없는 내용(미구현 주장)은 2건 후보였으나 둘 다 문서가 "P4 미구현·예고"로 self-label → 위반 아님(정직 처리 확인)**. 피팅 추천·그래프 suite는 §3·§4에 설계 제시(현 코드에 fitting wrapper·round-trip·그래프 스크립트 부재 = 확장 과제, 결함 아님).

---

## 1. 초점 (1) 코드 없는 내용 0 — 문건이 코드에 없는 기능·주장을 담는가

**방법**: P4로 LCO·발열·전자엔트로피가 code-backed 되었으므로(P4 RESULT §7·§9), Ch1·Ch2의 각 boxed 식/주장에 대응 코드 심볼이 실재하는지 역매핑. 그 외 "코드가 하는 것처럼 읽히나 실제 미구현"을 refute-우선 색출.

### 1-A. code-backed 확정 (통과 — 빈 통과 아님, 심볼 줄근거 병기)

| 문건 주장 (tex) | 코드 심볼 (줄) | 판정 |
|---|---|---|
| eq:qrev `q_rev=−IT·∂U/∂T=−(IT/F)ΔS` (Ch2 L645) | `reversible_heat` (L578-586) `-float(I)*T*self.entropy_coefficient(...)` | **[확정]** T 한 번 |
| eq:weighted 완전식 `Σ Q_j g_j(ΔS/F+config)/Σ Q_j g_j` (Ch2 L471-474·종합식 L672-674) | `entropy_coefficient` (L544-576) num/den 루프 + `config=(R/F)ln(ξ/(1−ξ))` (L571) | **[확정]** |
| eq:qrev 첫 항 lumped `q_irr=I(U_oc−V)` (Ch2 L643) | `irreversible_heat` (L588-596) | **[확정]** |
| eq:dSegate `ΔS_e=−(π²/3)R(kB T/e_V)(g_max/dx)σ(1−σ)` (Ch1 L1082-1086) | `func_dSe_molar` (L170-185) — 부호<0·÷EV_TO_J·R·kB 몰당 | **[확정]** demo 골깊이 −45.68 재현 |
| eq:gunit `g_J=g_eV/e_V` 나눗셈 (Ch1 L1027) | L185 `(kB*T/EV_TO_J)` 나눗셈 (곱셈 아님) | **[확정]** |
| eq:msmr 동형 `f↔−σ_d, X_j↔Q_j, ω_j↔w_j` (Ch1 L1738-1747) | `LCOCathodeDQDV`(L641) 상속·σ_d 뒤집기 없음 + `func_ksi_eq` 공유 | **[확정]** |
| sec:lco-code 전자항 plug-in "seam 한 줄"(Ch1 L1752-1756) | `_effective_dS_rxn` override (L655-671) 3경로 공유 seam | **[확정]** |
| eq:Sedirect 직접엔트로피 경로 (Ch1 L980-985) | (교차검증용 유도 — 코드 산출 아님, 문서 내 검산) | **[확정]** 코드-무관 정당(아래 1-C) |

→ Ch1·Ch2의 핵심 boxed 식 **전부 코드 심볼 대응 확정**. "코드에만 있고 문서에 없는" 역방향 갭도 없음(P4 seam·q_rev 메서드가 전부 Ch1/Ch2 식 근거).

### 1-B. ★코드-없는-내용 후보 2건 — 둘 다 문서 self-label "P4 미구현" 확인 (위반 아님)

C조 핵심 렌즈 = "문서가 코드에 없는 기능을 있는 것처럼 주장하나". 2건 후보를 refute-우선 정밀 검사:

- **후보①: x↔ξ_eq,1(V) 좌표 매핑** (Ch1 sec:lco-decomp L1724-1729, "★Ch2/P4 코드 구현 예고 (i) 좌표 매핑"). Ch1은 "전자항이 조성 x 함수인데 dqdv는 전압 격자 → x=x(ξ_eq,1(V)) 매핑으로 좌표를 잇는다"고 설계를 서술. **코드 실제**: `LCOCathodeDQDV._effective_dS_rxn`(L655-671)은 x-매핑을 하지 **않고** `tr['x_center']`(상수 0.50)를 `func_dSe_molar`에 넣는다(L669) — V-격자 위 x-의존 평가 미구현. **판정 [확정·위반 아님]**: Ch1 문장이 "★Ch2/**P4 코드 구현 예고**"·"다음 단계"로 명시 라벨(L1724) + P4 RESULT §11이 "다온도 round-trip 피팅서 구현"으로 이월 확정 + P4 review1이 "O3 x↔ξ 역방향"을 설계 단계서 **defer** 처리(P4 RESULT §5·§8 항목7). 곧 문서는 미래 설계로 정직하게 프레이밍했고 "코드가 이미 한다"고 주장하지 않음. **완성도 관점 개선 제언(정정 아님)**: Ch1 L1727의 `x=x(\xi_{\eq,1}(V))` 서술과 코드의 `x_center` 상수 근사 사이 "현 P4 구현은 x_center 단일-기준 동결"임을 sec:lco-decomp에도 1줄 명시하면(현재 이 명시는 코드 docstring L659-664에만 존재) 독자 오독 여지 0. → C-G5(완성도 제언, 아래 §5).

- **후보②: eq:U1T2 T² 곡률** (Ch1 L1054-1056 `U_1(T)=U_1(T_0)+ΔS_0/F(T−T_0)+a_e/2F(T²−T_0²)`). Ch1은 전자항 ∝T → U₁ 이동 ∝T² 이라는 곡률을 boxed. **코드 실제**: `_effective_dS_rxn`(L659-664 docstring)이 "전자항을 T_ref=298.15 동결 상수 오프셋"으로 처리 → dS_eff T-무관 → U_j(T) T-**선형**(곡률 없음). 곧 코드는 eq:U1T2의 T² 항을 **구현하지 않는다**. **판정 [확정·위반 아님]**: Ch1 L1046("Ch2의 가역 발열로 확장할 때 중요")·L664 코드 docstring("Sommerfeld T-스케일·eq:U1T2 center-T_ref 별도적분(½=a_e/2F)은 다온도 round-trip 피팅 단계의 과제로 분리(P4 미구현, 라벨)")이 미구현을 명시 + P4 RESULT §11 "다온도 T² 곡률 … 다온도 round-trip 피팅서 구현" 이월 확정. 문서·코드 docstring·P4 result 3중으로 "단일-기준 동결 근사, T² 미구현" 정직 라벨. **위반 아님**.

→ **초점(1) 결론 [확정]: 코드 없는 내용 = 0**. 두 후보 모두 문서가 "미구현·P4/다온도 피팅 과제"로 self-label → 허위 주장 아님. (P4 adversarial 항목7이 T²를 factor-2 결함으로 잡아 동결 근사로 마감한 이력까지 result에 박혀 있어 추적 가능.)

### 1-C. eq:Sedirect·통계열역학 본체 — 코드 없는 "유도"는 code-없는-내용이 아님 (오적발 방지)

Ch1 eq:Sedirect(L980-985)·Ch2 §sec:partition~§sec:config 전개(분배함수 Z→⟨n⟩→S_config)는 코드에 대응 심볼이 없다. **그러나 이는 "코드가 해야 할 기능"이 아니라 "코드가 쓰는 식(logistic·func_U_j)의 통계역학적 유도·기원"이다** — 교과서의 정당한 유도 몫이며 코드-없는-내용(미구현 기능 허위주장)과 범주가 다르다. Ch2 서(L89-96)가 "분포를 결론으로 인용하지 않고 본체로 전개"를 명시 목적으로 선언 → 오적발 회피. **판정 [확정·정상]**.

---

## 2. 초점 (2) 교재 자기완결 — 타 전공 석박사 비약 0·독자평가 0·식→식 유도 완결

### 2-A. 식→식 유도 완결성 (통과 — 표본 3식 (a)→(d) 추적)

- **eq:dUhys**(Ch1 L610-614): (a) 비단조 V_eq → (b) spinodal 대입 eq:hyssub → (c) 극대−극소 차 eq:hysdiff(artanh 항등식 명시) → (d) 박스. **[확정]** 중간 항등식(`ln[(1−u)/(1+u)]−ln[(1+u)/(1−u)]=−4artanh u`) 본문 노출(L607).
- **eq:xieq**(Ch1 L770): (a) Eyring+비대칭장벽 eq:bv → (b) 비→detailed balance eq:db → (c) 정지점 logit eq:logisticsolve → (d) 폭·방향 일반화 박스. **[확정]** χ 상쇄(`χA+(1−χ)A=A`) 명시(L751).
- **eq:weighted**(Ch2 L471-474): eq:implicit → 음함수 미분 eq:implicit_diff → eq:gj·eq:dxidT → 박스. **[확정]** 단순식/완전식 두 단계 분리·config 항 출처(w의 T-의존, L457-463) 명시.

식→식 다리 비약 표본 3식 전수 완결. eq:Se 두 경로(비열 eq:Se + 직접 eq:Sedirect) 교차검증까지 완비(Ch1 L974-987).

### 2-B. 독자수준 평가 표현·타전공 비약 (통과 — refute 색출)

- P2 RESULT §6·§8이 "독자 수준 평가 표현 0(편입 7건 전수 확인)"·"완결 문장·안정 객관"을 gate로 확정. 본 감사 재확인: Ch1·Ch2 boxed·keybox·warnbox에서 "쉽게", "당연히", "독자라면" 류 평가 표현 색출 결과 **미발견**. **[확정]**
- Sommerfeld 전개(Ch1 sec:lco-Se L948-987)는 축퇴 극한·Mott 보정 경계까지 자기전개(외부 "표준결과 인용" 아님) — 타전공(고체물리) 비약 없이 Fermi-Dirac→비열→적분 3단계 노출. **[확정]**

### 2-C. ★자기완결 저해 실물 갭 (아래 §6 3대무결에서 상술) — C-G1 라벨 불일치

"이 문건만으로 같은 곡선 재현 코드를 짤 수 있다"(Ch1 서 L138·keybox L1806)가 Ch1의 자기완결 선언인데, LCO 데이터셋 이름을 **`LCO_STAGING_LIT`**(Ch1 L311·L312·L1750)로 지목하나 실제 코드 심볼은 **`LCO_MSMR_LIT`**(코드 L621). 독자가 문서대로 `LCO_STAGING_LIT`을 찾으면 코드에 없음 → 재현 직접 저해. **[확정] = C-G1(최중대).**

---

## 3. 초점 (3) 피팅 추천 — 모델↔데이터 round-trip 워크플로 설계

**현 상태 [확정]**: 코드에 fitting wrapper·Optuna·round-trip 루틴 **부재**(P1 RESULT §2-C "fitting wrapper 권고, 코드 범위 밖"·Ch1 sec:inputs L1763 "Optuna로 피팅하는 것" = 사용자 과제 선언). 결함 아님 — 설계 제안이 C조 산출.

### 3-A. 파라미터 인벤토리 + tier (P1 §3 인벤토리 + Ch1 tab:inputs + LCO/발열 확장)

**Tier 1 (peak 골격 — 저율/평형 데이터서 직접 식별, 먼저 자유화)**
| 파라미터 | 코드 키 | 지배영역 | 초기값 | 경계·주의 |
|---|---|---|---|---|
| U_j 또는 (ΔH_rxn, ΔS_rxn) | `U`/`dH_rxn,dS_rxn` | peak 위치(V축) | 흑연 0.085~0.210 / LCO 3.88~4.05 | 열역학 환산 우선. 단온도서 ΔH·U 중복→하나 고정 |
| n_j (폭) | `n`(또는 `w` 역산) | peak 폭 | 1.0 | **n>0 필수**(F1: n≤0→NaN/음수폭, P1 §2-C) |
| Q_j | `Q` | peak 면적·높이 | 흑연 0.10/0.12/0.25/0.50 | ΣQ 정규화 제약 권고 |
| C_bg | `Cbg` | baseline | 0 | callable이면 유한성 검증(F4) |

**Tier 2 (히스·비대칭 — 충/방전 pair 데이터 필요)**
| Ω_j | `Omega` | 히스 gap·ΔH_eff | 6000~13000 J/mol | Ω>2RT(≈4958@298K)부터 gap. **γ와 결합** → 하나 고정 후 타 fit |
| γ_j | `gamma` | dis-chg split(=γ·ΔU_hys) | 0(off) | Ω↔γ 식별성 붕괴 회피 |
| χ (chi) | `chi`/`x` | 꼬리 충방전 비대칭 | 0.5 | **[0,1] bound**(F3). χ=0.5면 비대칭 0(D5) |
| R_n | `Rn` | 전체 IR shift | 0 | rate-series서 자유 |

**Tier 3 (동역학 꼬리 — rate-series 필요, 지수 감도)**
| ΔH_a | `dH_a` | 꼬리 길이 L_V(exp 지수) | 40000~48000 J/mol | 최고감도. rate-series 필수 |
| dVdq_qa | `dVdq_qa` | 꼬리 V-스케일 | 0.30 | **누락=silent 꼬리off**(F2) — schema서 필수 |
| L_V (직접) | `L_V` | 꼬리 길이 우회 | 미지정 | 초벌 자유 안정, 물리 fit서 제거. 지정 시 dH_a/Ω/χ/z_cut 전부 우회(과식별 주의) |

**Tier 4 (다온도 전용 — 단온도서 과적합)**
| ΔS_rxn | `dS_rxn` | ∂U/∂T=ΔS/F | +29/0/−5/−16 | 다온도 데이터 전 고정 |
| ΔS_a | `dS_a` | 꼬리 T의존 | 0 | 다온도서 조건부 |

**LCO 전용 확장(전자항 — MIT 게이트 3파라미터)** [Ch1 eq:ggate L1069-1070, 코드 dict 키 L632]
| g_max_eV | `g_max_eV` | 게이트 높이 | 13.0 (Motohashi anchor, tier A 단일점) | 초기값 고정, 도핑 시 소폭 |
| x_MIT | `x_MIT` | 게이트 중심 | 코드 0.50 / **Ch1 0.85**(★C-G2 불일치) | round-trip서 물리값 정정 |
| dx_MIT | `dx_MIT` | 게이트 폭 | 0.05 | 결함 농도 의존, 데이터 피팅 |

### 3-B. round-trip 절차 (Ch2 procedurebox L699-716 + Ch1 sec:lco-decomp round-trip 가드 기반 설계)

1. **저율/평형 다온도 dQ/dV 측정** (T_k 여럿, 저율로 동역학 lag 폭 부풀림 회피 — Ch2 L703).
2. **분극 선제거**: V_n=V_app−σ_d|I|R_n (Ch1 eq:vn) — 평형 U_oc의 T-의존만 남김 (Ch2 L705).
3. **Tier 1 자유화 동시피팅**: 각 온도의 U_j(T_k)·w_j(T_k) 허용, `equilibrium()`(단, T 스칼라 전용 — P1 §1.3 보완2) 또는 저율 `dqdv()`로 forward 종 fit. (MSMR 절차 대응, Ch2 L707-709)
4. **round-trip 검증(핵심)**: 회귀한 U_j(T)의 중심 기울기 → ΔS⁰_j=F·dU_j/dT (Ch2 L710) → GRAPHITE_STAGING_LIT의 dS_rxn(+29/0/−5/−16) 복원 확인. 흑연은 `__main__` U(298) 검산(코드 L730-731)이 이미 U↔(ΔH,ΔS) round-trip 예시.
5. **Tier 2→3→4 순차 개방** (P1 §2-F 4단계): 충/방전 pair(Ω·γ) → rate tail(dH_a·dVdq_qa, 먼저 L_V 직접 fit로 관측가능성 확인) → 다온도(dS_rxn·dS_a).
6. **LCO 전자항 self-test 가드**(Ch1 L1729-1733): T1 위치 U_1(298)≈3.90V + ∂U_1/∂T 부호·기울기(다온도 이동률)로 게이트 3파라미터 검증 후 신뢰값 승격.

### 3-C. 초기값·경계 (fail-fast 가드 활용)
- 코드 가드(`_finite_pos`·`_finite_nonneg`, L189-210)가 T>0·Q_cell>0·|I|≥0·z_cut>0 등 fail-fast → 피팅 bounds 위반 시 즉시 ValueError. **[확정]** 그러나 **n>0·χ∈[0,1]·dVdq_qa>0는 미가드**(P1 §2-C F1/F3/F2) → fitting wrapper 스키마에서 별도 bound 필수. **[확정·설계 제언]**

---

## 4. 초점 (4) 그래프 suite 설계 — 종합 그래프 목록·각 검증 목적

**현 상태 [확정]**: 코드 저장소에 그래프 스크립트 2종 존재 — `plot_dqdv.py`(흑연 4패널)·`demo_lco_heat.py`(LCO+발열 3패널) + 산출 png 2종(figs/). round-trip·온도의존·전자항 곡률 전용 그래프는 부재 → C조 설계 제안.

### 4-A. 기존 그래프 (실재 확인)
| 파일 | 패널 | 검증 목적 | 상태 |
|---|---|---|---|
| plot_dqdv.py | (1)흑연 4전이 평형 (2)단일 LiC6 종+면적보존 (3)방/충 히스 (4)온도 vs FWHM | use_w_eff 제거 후 정상 종·면적=Q 실증 | **[확정]** figs/anode_fit_v1_0_10_dqdv.png |
| demo_lco_heat.py | (a)흑연 dQ/dV (b)LCO dQ/dV(MSMR) (c)q_rev(흑연+LCO) | LCO 3봉·q_rev 부호·전자항 발열 서명 | **[확정]** figs/P4_lco_heat_validation.png |

### 4-B. ★제안 그래프 suite (round-trip·온도의존·검증 목적별)

| # | 그래프 | 축·내용 | 검증 목적 (어느 물리/식) |
|---|---|---|---|
| G1 | 흑연+LCO dQ/dV 나란히 | V(0.05~0.25 / 3.85~4.20) vs dQ/dV, 방·충 | 한 프레임 두 전극(Ch1 통합 교육가치), MSMR 동형 |
| G2 | **round-trip 복원** | 입력 ΔS_rxn(+29/0/−5/−16) → forward U_j(T) → 회귀 → ΔŜ 산점도 (y=x 대각) | eq:Uj·ΔS 식별성(Ch2 L710 절차4). **핵심 신뢰 가드** |
| G3 | q_rev(V) 흡·발열 교대 | V vs q_rev, ΔS 부호 전환대 음영 | eq:qrev 부호규약(저-x 흡열/고-x 발열, Ch2 L661-664) |
| G4 | ∂U_oc/∂T(x) 완전식 vs FD | x vs mV/K, 완전식·단순식·유한차분 3선 | 파생A 수치검증(Ch2 srcbox L484-495, 완전식≈0 오차·단순식 최대 0.18) |
| G5 | 온도의존 peak 이동 | T(258~318K) vs peak@V·FWHM | U_j(T)=ΔS/F 이동·폭 RT/F(Ch1 sec:center, plot_dqdv 패널4 확장) |
| G6 | 전자항 골 ΔS_e(x) | x vs ΔS_e[J/mol/K], MIT 중심 골 −46 | eq:dSegate 게이트(Ch1 fig:lco-electronic 대응, 코드 func_dSe_molar) |
| G7 | **다온도 이동률(T² 곡률)** | T vs ∂U_1/∂T (전자항 T-선형) / U_1 vs T(곡률) | eq:U1T2 곡률 식별 신호(**단, 현 코드 동결근사=선형 → 다온도 피팅 구현 후 유효**, §1-B②) |
| G8 | 히스 분기 split | V vs 방/충 peak, gap=γ·ΔU_hys | eq:Ubranch(코드 __main__ L784-793 self-test 그래프화) |
| G9 | 면적보존 회귀 | 전이별 ∫dQ/dV dV vs Q_j | eq:eqpeak 면적=Q(P1 §0 면적 1.000, self-test assert 부재 보완) |

주의: **G7은 T² 곡률 그래프이나 현 코드는 T_ref 동결로 U_j(T) 선형** → G7은 "다온도 round-trip 피팅 T² 구현 후" 유효(§1-B② 라벨과 일관). 현 시점 G7은 "선형 기준선 + eq:U1T2 예상 곡률 오버레이"로만 그려야 오도 없음. **[확정·설계 주의]**

---

## 5. 완성도 제언 (정정 아님 — master 판단용)

- **C-G5 [완성도 제언]**: Ch1 sec:lco-decomp (i)(L1727 `x=x(ξ_eq,1(V))`)는 "P4 예고"지만, 실제 P4 코드는 `x_center` 단일 상수 동결(코드 L659-664 docstring). 독자가 sec:lco-decomp만 읽으면 "코드가 V-격자 x-매핑을 한다"고 오독할 여지. → sec:lco-decomp에 "현 P4 구현은 x_center 단일-기준 동결 근사(코드 docstring 참조)" 1줄 브리지 추가 제언(현재 이 명시는 코드 docstring·`_effective_dS_rxn`에만 존재, Ch1 본문엔 부재).
- **C-G6 [완성도 제언·경미]**: Ch2 procedurebox(L699-716)는 흑연 round-trip 절차만 제시. LCO 전자항 3파라미터(g_max·x_MIT·dx_MIT)의 round-trip 가드는 Ch1 sec:lco-decomp L1729-1733에 있으나 Ch2 발열 챕터엔 없음 → 발열 산출 시 LCO 전자항 검증 절차 cross-ref 1줄 제언(inline 참조).

---

## 6. 공통 산출 — 3대 무결 최종 확인 + P4 이월 정합·라벨

### 6-A. 3대 무결
- **물리 배경 정확 [확정]**: eq:qrev T 한 번(차원 [W])·부호 흡발열 교대·이중계산 직교(config 중심/분포 분리)·전자항 부호<0(삽입기준)·÷e_V 단위 — Ch1/Ch2 유도 완결, P3 review1 7건 확정과 정합. 물리 오류 미발견.
- **코드 정확 [확정]**: P4 흑연 0-diff(P4 §9 13/13 array_equal)·seam 3경로 일관·q_rev/dSe/이중계산 삼각검증(P4 §8). C조 재확인: `_effective_dS_rxn` base가 `tr['dS_rxn']` 항등(L542) → 흑연 byte 불변, LCO override만 전자항 가산(L666-671). 정합.
- **사용자 의도 반영 [확정]**: "BDD 양·음극 dQ/dV 피팅 함수 확장"(P4 §1) = 흑연+LCO+발열 code-backed 완료. MSMR 동형·면적보존 DC=1·식별자/정수코드/死코드 보존(P4 §10 gate PASS).

### 6-B. ★확정 갭 6건 (위치·무엇이·맞는 형태 — master 정정용)

| ID | 등급 | 위치 | 무엇이 | 맞는 형태 |
|---|---|---|---|---|
| **C-G1** | HIGH | Ch1.tex **L311·L312·L1750** (`LCO_STAGING_LIT`) | 문서가 지목한 LCO 데이터셋 이름이 코드 심볼 `LCO_MSMR_LIT`(코드 L621)와 불일치 → 자기완결("문건만으로 재현") 저해 | Ch1 3곳을 `LCO_MSMR_LIT`로 통일(또는 코드 심볼명을 문서에 맞춤 — master 택1). demo_lco_heat.py L27-31·코드 L621은 `LCO_MSMR_LIT`로 일관하므로 **문서 측 정정이 최소변경** |
| **C-G2** | MEDIUM | Ch1.tex eq:ggate **L1070** (`x_MIT≈0.85`) vs 코드 L631-632 (`x_MIT:0.50, x_center:0.50`) | 전자 게이트 중심 조성 문서 0.85 / 코드 0.50 불일치 (MIT 2상역 x≈0.75-0.94, Ch1 L691·L944와도 코드 0.50이 어긋남) | P4 RESULT §11 이월 확정 항목. round-trip 피팅서 물리값(0.85급) 정정. 현 코드 0.50은 tier-C placeholder(코드 L619-620 라벨) → **문서에 "코드 시연값 x_MIT=0.50은 placeholder, eq:ggate anchor 0.85와 별개" 각주** 또는 코드 정정(피팅 단계). 지금은 라벨 정합만 |
| **C-G3** | MEDIUM | Ch1 tab:lco-staging **L330-332** (T1~3.90/T2~4.05/T3~4.17-4.20 V) vs 코드 LCO_MSMR_LIT (3.930/3.880/4.050 V, L622·L630·L635) + demo L41 "목표 3.880·3.930·4.050" | LCO 세 전이 전위·전자항 위치 불일치: 문서 T1(MIT/전자항)=3.90V 최저, 코드 전자항 전이=3.880V(둘째 dict) & 주평탄역=3.930V. 문서는 T2·T3를 order-disorder 쌍(4.05/4.17)으로, 코드는 4.050 단일 곁가지 | tier-C 시연값 정합. 문서 tab:lco-staging와 코드 LCO_MSMR_LIT 전위·전자항 배정 일치화(전자항이 문서=최저 T1 / 코드=중간 3.880) → master가 한쪽 기준 택해 정합. round-trip 피팅 전 placeholder라 **라벨·주석 정합이 우선**(값 자체는 피팅 override 전제) |
| **C-G4** | LOW | Ch1.tex **L133-134** (서론 `dqdv` 호출 구현명 `Anode_Fit_v11_final.py`) + Ch1 L38·L46 헤더 주석 (`graphite_ica_ch1_Opus_v6.tex`) | 본문 구현 파일명이 구버전 `v11_final`(현 `Anode_Fit_v1.0.10.py`), 근거문건이 `Opus_v6`(현 v1.0.10). P3서 Ch2는 v11→v1.0.10 정정했으나 Ch1 본문 L133·헤더 잔존 | Ch1 L133 `Anode_Fit_v11_final.py`→`Anode_Fit_v1.0.10.py`, L38 근거문건명 현행화. (P2 RESULT는 신규 편입만 다뤄 이 기존 본문 잔존 미정정 — 파일명 라벨 일관성) |
| **C-G5** | LOW(제언) | Ch1 sec:lco-decomp **L1727** | x↔ξ 매핑 "예고"만 있고 현 코드=x_center 동결 근사임이 Ch1 본문 미명시(docstring에만) | sec:lco-decomp에 "현 P4=x_center 단일-기준 동결" 1줄 브리지 (§5) |
| **C-G6** | LOW(제언) | Ch2 procedurebox **L699-716** | LCO 전자항 round-trip 가드 cross-ref 부재 | Ch2에 Ch1 L1729-1733 전자항 self-test 참조 1줄 (§5) |

### 6-C. P4 이월 4항목 문서 정합·라벨 확인 [확정]
- **x_MIT tier-C**: → C-G2로 실물 갭 확정(문서 0.85 vs 코드 0.50). P4 §11 이월과 일치. 코드 L619-620·L631 "tier-C 시연 placeholder" 라벨 실재 확인.
- **다온도 T² 곡률**: 코드 미구현(동결 근사) — 코드 L659-664 docstring·Ch1 L664·L1046·P4 §11 3중 라벨 확정. **문서 정합 OK**(§1-B②). 그래프 G7 유효성 주의(§4-B).
- **시연 파라미터 tier-C**: LCO_MSMR_LIT(코드 L619-638)·GRAPHITE_STAGING_LIT(L675-707) 모두 "초기값·신뢰값 아님·피팅 override 전제" 라벨 실재. Ch1 tab:staging(L1665)·tab:lco-staging(L322) "출발점, 피팅으로 override" 정합. **[확정]**
- **비가역 3분해**: 코드 lumped만(`irreversible_heat` L588-596)·3분해 옵션 라벨(L590-594 docstring "Ch2 boxed 부재→lumped만"). Ch2 eq:qrev(L643) lumped만 boxed 확인 → **문서·코드 정합**(3분해는 Ch2에 boxed 식 없음이 근거). **[확정]**

---

## 7. 5줄 요약

1. **조 = C조(O3)**: 내용 완성도 + 코드없는내용 0 + 피팅 추천 + 그래프 suite. 코드 740줄·Ch1 1816줄·Ch2 705줄·P1~P4 result 전문 head→tail 정독.
2. **확정 갭 6건**: C-G1(LCO 데이터셋명 문서 LCO_STAGING_LIT↔코드 LCO_MSMR_LIT, HIGH)·C-G2(x_MIT 0.85↔0.50)·C-G3(LCO 3전위/전자항 배정 불일치)·C-G4(본문 v11_final 파일명 잔존)·C-G5/G6(완성도 제언 2).
3. **최중대 갭 = C-G1**: 문서가 지목한 `LCO_STAGING_LIT`이 코드에 없음(코드=`LCO_MSMR_LIT`, demo도 MSMR) → "문건만으로 재현" 자기완결 직접 저해. 문서 3곳(Ch1 L311·L312·L1750) 정정이 최소변경.
4. **정정 목록**(master용): Ch1 L311/L312/L1750 데이터셋명 통일 · x_MIT 0.85↔0.50 라벨 각주 · LCO 3전위/전자항 배정 정합 · L133 구현파일명 v1.0.10 현행화 · sec:lco-decomp·Ch2 procedurebox cross-ref 1줄. **코드 수정 X — 라벨·문서 정합 위주**(값은 tier-C placeholder라 피팅 override 전제).
5. **리스크**: 코드없는내용=0 확정(x↔ξ 매핑·T² 곡률 2후보 모두 문서 self-label "P4 미구현" → 위반 아님). 피팅 워크플로·그래프 G2/G7/G4는 설계 제안(현 코드 fitting wrapper·round-trip 스크립트 부재는 확장 과제이지 결함 아님). G7(T² 곡률) 그래프는 다온도 피팅 구현 전엔 선형 기준선+예상곡률 오버레이로만 유효.

---

*V1010 P5 감사 드래프트 O3 (C조) | 2026-07-01 | 코드·문건 수정 없음(감사 의견만) | 정정·그래프 실행은 master*
