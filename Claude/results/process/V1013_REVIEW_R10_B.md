# V1013 P5 검수 R10 — 검수자 B (자유 사냥 통독 + R9 수정분 재검)

- 대상: `graphite_ica_ch2_v1.0.13.tex` 전문 · `Anode_Fit_v1.0.13.py` 전문 · `FITTING_GUIDE.md` · `demo_lco_heat.py` · `plot_dqdv.py` · `test_regression_graphite.py` · `sample_test_v1013.py` 전문 + `git show df0bbb2` (R9) 대상 hunk 전수.
- 청크 스킴: 자유 사냥 통독(물리 논리 1급 > 논리 비약 > 수식-주도) + R9 hunk 재검(⑧) + 수치 실증 스크립트(scratchpad, 산출물 무변경).
- 역할 준수: 검수 의견만 — 산출물 수정 0건. 모든 지적에 줄 번호·원문 인용·재현 근거.

---

## A. 확정 결함 (CRIT / HIGH / MED)

### F2 [HIGH] 스칼라 V + 동역학 꼬리 `dqdv()` — 그리드-의존 분기 뒤집힘으로 침묵 오차 −6.9% (실측 재현)
- 위치: `Anode_Fit_v1.0.13.py` L439–444 (`v_span = max(v_hi - v_lo, self.v_span_floor)`, `v_span_floor=1e-6` 기본 L258) + L491 분기 (`lag_len_V < self.min_lag_grid_steps * grid_step`). API 는 스칼라를 명시 지원: L407 "`V_app : 인가 전위 격자 [V] (스칼라 또는 배열)`" — 스칼라+동역학 조합의 경고 없음.
- 무엇이: 스칼라 입력이면 작업 격자 스팬이 인위적 바닥 1e-6 V 로 잡혀 `grid_step≈6.4e-10 V` — 배열 호출에서는 꼬리 OFF(평형 분기)인 전이가 전부 꼬리 ON 으로 뒤집히고, 창 길이가 L_V 의 수 배(tr0: 창 1.3e-6 / L_V 4.9e-7 ≈ 2.6배)라 인과 필터가 창 안에서 수렴하지 못해 봉우리를 과소평가한다.
- 근거(수치 재현, 출하 데이터셋 그대로): `GRAPHITE_STAGING_LIT`, x=0.5, Rn=0.01, Cbg=0.05, T=298.15, I=1.0, s=+1 —
  - 배열 `dqdv` @V=0.12 → **7.2017** ; 물리 참값 `equilibrium(V_n=0.11)` = **7.2014** (L_V≈1e-7 V 급이라 꼬리 기여는 무시 수준 — 배열이 정답).
  - 스칼라 `dqdv(0.12, ...)` → **6.7040** (−6.9%).
  - 분기 경계: 스칼라 ν·Δ=1.27e-9 vs 전이별 L_V = 4.9e-7/1.5e-7/4.4e-8/4.8e-9 (전부 꼬리 ON) ; 배열 ν·Δ=3.9e-4 (전부 꼬리 OFF).
- 판정: 문서화된 입력형(스칼라)에서 침묵으로 틀린 수가 나온다. `curve()` facade 도 스칼라를 그대로 전달하므로 동일 노출. R9 이전부터의 잠복(신규 발견)이며 출하 그림·회귀·self-test 는 전부 배열이라 오염 없음.
- 수정안: (i) 퇴화 스팬(스칼라·초협소) + 동역학 키 존재 시 작업 창을 `max(v_span, k·max_j L_V)` 이상으로 확장하거나, (ii) 스칼라 입력에서는 평형 분기를 강제하고 docstring 에 "스칼라 호출은 꼬리 미적용(스윕 이력 부재)" 을 명시. 어느 쪽이든 흑연 회귀(배열 경로)는 불변.

### F1 [MED] `entropy_coefficient()` — `'w'`-단독(T-동결 폭) 전이에 config 항 오가산 (코드 자신의 폭 모델·Ch2 srcbox 전제와 모순, 실측 재현)
- 위치: `Anode_Fit_v1.0.13.py` L587 `config = (n_j * R / F) * np.log(xi_c / (1.0 - xi_c))` + docstring L561–562 "★config 항 계수 = ∂w_j/∂T = n_j·R/F". 대조: Ch2 tex L513–514 "이 서식은 `'n'` 키 보유 전이에 적용되며 … `'w'`-단독 전이는 $T$-동결 폭이다", L517–518 "만일 실측 $w_j$ 가 $T$-동결에 가깝다면 단순식/완전식의 우열이 뒤집히는 ~0.3 mV/K 급 차이".
- 무엇이: `_n_factor`(L301–307)는 `'w'`-단독이면 `n=w·F/(RT)` 를 현재 T 로 역산 → `_width`=w 상수(T-동결, 실측 `width(292.15)=width(298.15)=0.020` 확인). 이때 ∂w/∂T=0 이므로 완전식의 config 조각(eq:dxidT 둘째 항)은 0 이어야 하는데, 코드는 `n_j·R/F = w/T ≠ 0` 을 가산한다 — docstring 의 항등 주장("계수 = ∂w_j/∂T")이 `'w'`-단독에서 거짓.
- 근거(수치 재현): 단일 전이 `{'w':0.020,'Q':1,'dH_rxn':-13000,'dS_rxn':-16}`(`'n'` 無), ξ=0.7 고정 FD(코드 자신의 폭 모델 하 ∂U_oc/∂T|ξ) = **−0.1658 mV/K** (=ΔS/F 정확) vs `entropy_coefficient` = **−0.1090 mV/K** — 차 **+0.0568 mV/K** = (w/T)·ln[ξ/(1−ξ)] 예측치와 일치. 대조군 `'n':1.0` 전이는 FD=EC=−0.0928 mV/K (차 1.2e-15) — `'n'` 경로는 무결.
- 판정: 잠복 — 출하 데이터셋(`GRAPHITE_STAGING_LIT`·`LCO_MSMR_LIT`)은 전부 `'n'` 보유라 현 산출물 무오염. 단 py 헤더 L11 이 "피팅 핸들=n(또는 `'n'` 제거 시 `'w'`)" 로 `'w'`-단독 사용을 승인하므로 문서화된 경로다. 크기는 봉우리 가장자리에서 config 항 자체(~0.2 mV/K)의 수십 % 급.
- 수정안: config 항을 `'n'` 보유 전이에만 가산(`tr.get('n') is not None` 게이트)하거나, docstring·가이드에 "`entropy_coefficient` 의 완전식은 폭의 열적 서식 w=nRT/F 전제 — `'w'`-단독(T-동결) 전이는 단순식이 옳음(Ch2 파생 A srcbox)" 을 명시. 게이트 도입 시 흑연 회귀는 불변(회귀 13종에 entropy_coefficient 미포함 + 전 전이 `'n'` 보유).

### F3 [MED] `reversible_heat` 의 "방전 I>0" — 같은 클래스 `curve('discharge')` 와 반대 화학 방향인데 코드·데모에 라벨 층위 경고 미이월 (Ch2 는 경고 완비)
- 위치: `Anode_Fit_v1.0.13.py` L599 "`방전 I>0: ΔS>0(∂U/∂T>0) → q_rev<0 흡열 … (Ch2 부호규약)`" vs 같은 클래스 L246–247 "`탈리튬화에 대응하는 셀 라벨 … 음극(흑연) = 방전`". Ch2 tex L680–683 은 정확히 이 충돌을 경고한다: "Chapter 1 의 방향 라벨(흑연 하프셀 방전 $=$ 탈리튬화, $\sigma_d{=}+1$)과 같은 단어가 \emph{반대 화학 방향}을 가리키므로, 본 절의 부호는 라벨이 아니라 전류 부호 $I$ 로 읽는다".
- 무엇이: Bernardi 관례의 I>0 = 셀 방전 = 흑연 하프셀 **리튬화**. 흑연 `curve(direction="discharge")` = σ_d=+1 = **탈리튬화**. 곧 한 코드 파일 안에서 "방전"이 두 반대 방향을 가리키는데, `reversible_heat` docstring 은 "(Ch2 부호규약)" 포인터만 있고 충돌 경고 문장이 없다. 파생 노출: `demo_lco_heat.py` L49 "`방전 I>0, dU/dT>0(ΔS>0)→흡열 q<0`" 주석과 (c) 패널(L63–67), `sample_test_v1013.py` (c) 패널(L75–88) 모두 I=+1 로 q_rev 를 그리면서 방향 라벨이 없다 — (a)"discharge"·(b)"charge" 곡선 패널과 병치되어, 독자가 (a)/(b) 방향의 열로 오독하면 q_rev 부호 이야기가 뒤집힌다(흑연: (a) 탈리튬화 vs (c) I>0=리튬화).
- 근거: 위 인용 3곳 + Ch2 L680–683. 수식·수치는 전부 옳다(자기일관) — 결함은 R9 가 guide §5 에서 승격해 다룬 바로 그 "방향 라벨 함정" 계열의 코드·스크립트 쪽 잔여.
- 수정안: `reversible_heat` docstring 에 1줄 — "★이 '방전(I>0)'은 Bernardi 셀 방전(흑연 하프셀=리튬화)이다 — `curve()` 의 direction='discharge'(탈리튬화)와 반대 화학 방향; 탈리튬화 구간의 가역열은 I<0 으로 넣는다(Ch2 라벨 층위 주의)". demo·sample (c) 제목 또는 범례에 "I>0 = cell discharge (graphite: lithiation)" 병기.

## B. LOW

### F4 [LOW] 회귀 하네스 docstring 잔여 구명 — R9 가 L2 만 정정하고 L3 미정정
- 위치: `test_regression_graphite.py` L2–3: "`사용: python test_regression_graphite.py capture (편입 前)` / "`python p4_regression.py verify (편입 後, np.array_equal bit 일치)`".
- 무엇이·근거: R9(df0bbb2)가 capture 행의 옛 파일명 `p4_regression.py` 를 정정했으나 바로 아래 verify 행은 옛 이름 그대로다(diff 원문 확인). 수정안: L3 도 `test_regression_graphite.py verify` 로.

### F5 [LOW] 회귀 하네스 미지 mode 침묵 통과 (exit 0)
- 위치: `test_regression_graphite.py` L55–80 `main()`: `mode` 가 `capture`/`verify` 아니면 아무 분기도 타지 않고 출력 없이 종료(else 부재) — `python … veryfy` 오타 시 검증 없이 exit 0 → CI/게이트에서 PASS 로 오인. 기본값 verify 전환(R9)의 부작용은 아니고 기존 잠복(무인자 실행은 verify 13/13 PASS·exit 0 정상 동작 실측). 수정안: `else: print(...); sys.exit(2)`.

### F6 [LOW] 가이드 §7 그래프 suite 목록에서 V8 누락 — suite 에 실존하는 패널
- 위치: `FITTING_GUIDE.md` L90–98 (V1–V7, V9 만 열거). 실물: `Claude/docs/v1.0.10/graph_suite_p5.py` L95–98 — "`# V8 자리 — q_rev LCO(전자 서명)`" / "`V8  LCO q_rev (전자전이 서명)`" 패널 실존(suite docstring 도 "V1-V9 핵심 패널").
- 무엇이·근거: 선별 기준 명시 없이 V9 는 넣고 V8 만 빠져 결번으로 보인다 — 열거 누락. 수정안: V8 행 추가("V8 LCO q_rev 전자전이 서명 — eq:dSegate 골의 발열 흔적") 또는 선별임을 명시.

### F7 [LOW] `demo_lco_heat.py` L41 (R9 신설 문구) — "분해하려면 w 축소" 가 inert 핸들을 지시
- 위치: `demo_lco_heat.py` L41 "`(전이 U=3.880·3.930·4.050 — 폭 겹침으로 병합 피크, 분해하려면 w 축소)`".
- 무엇이·근거: `LCO_MSMR_LIT` 세 dict 전부 `'n':1.0` 보유 → `_n_factor` 는 `'n'` 우선이라 `'w'` 키(0.030 등)는 inert — py 헤더 L10–11 이 스스로 경고하는 함정("`'w' 폴백 … 'n' 존재 시 inert. 피팅 핸들=n`")을 R9 신설 문구가 재생산. 실폭은 RT/F≈25.7 mV. 수정안: "분해하려면 n 축소(또는 `'n'` 제거 후 w)".

## C. NOTE

- N1 [NOTE] Ch2 경계값 표기 불일치: L171 keybox "단상 전이($\Omega_j\le2RT$)" vs L214 "$\Omega<2RT$ 면 등온선이 단조" · L568 "단상($\Omega<2RT$, 균질 고용체)". 물리 measure-zero(임계점 귀속 문제)이나 ≤/< 를 한쪽으로 통일 권고.
- N2 [NOTE] 가이드 §7 이 `graph_suite_p5.py` 를 v1.0.13 suite 로 서술하나 파일은 `docs/v1.0.10/` 에만 존재하고 내부 CODE 경로도 v1.0.10 을 가리킴 — 이식은 P6.1 이월로 ledger 확정된 사항(재논의 아님). 가이드 문면에 "(이식 전 — v1.0.10 폴더)" 표기만 권고.

---

## D. R9 수정분 재검(⑧) — `git show df0bbb2` 대상 hunk 전수 판정

| hunk | 판정 | 근거 |
|---|---|---|
| py L48 L_q 주석 `−TΔS_a` 추가 | 정합 | `func_L_q`(L103–110) 재유도: dG_a=dH−T·dS, T_attempt/T=\|I\|h/(Q k_B T) — 주석식과 일치 |
| py L312 "1.0.10에서 제거" | 정합 | 헤더 L8 "[1.0.10 변경] use_w_eff 경로 제거" 와 일치 |
| py L633–635 LCO 데이터셋 평형 경로 한정어 | 정합 | 클래스 docstring L668–677 과 동일 논리, eq:lco-sigmaslot 실존(ch1 L1922) |
| guide §0 헤딩 참조 교체(sec:lco-direction, eq:lco-sigmaslot) | 정합 | 두 라벨 ch1 L1913·L1922 실존(grep) |
| guide §1 ν≳10 닫힌꼴 | 정합 | 1−(1/ν)/(e^{1/ν}−1): ν=2→22.93%, 8→6.12%, 10→4.92% 독립 재계산 일치 |
| guide §2 Phase C ν≳10 / Phase D "재정렬 완료" | 정합 | py T1 dict `x_MIT:0.85`(L650)·§1 표 행과 일치 |
| guide §5 direction 처방 교체문 | **정합(실행 실증)** | LCO `curve('charge')==dqdv(s=+1)` bit-exact True; `curve(direction=+1)==dqdv(s=−1)` True — 금지 사유 성립. §0 본문(라벨 그대로·손 반전 금지)과 무모순 |
| guide §7 V6 문구 | 정합 | sample_test (d) L92–96 라벨과 일치 |
| demo §3 제목·병합 피크 문구 | 제목 정합 / 신설 문구 1건 결함 | 제목 "충전=탈리튬화, s=+1" 정합; "w 축소" = F7 |
| demo (b) dis→chg 라벨 | 정합 / (c) 잔여 | (b) 는 s=+1=탈리튬화=충전과 정합. (c) q_rev 는 I=+1(Bernardi 방전) 경로로 (b)와 반대 방향인데 방향 표기 침묵 = F3 에 포함 |
| plot_dqdv suptitle 1.0.13·radius 행 삭제 | 정합 | 잔여 없음 |
| 회귀 하네스 L2 파일명·기본 capture→verify | 정합 / 잔여 1 | 무인자 실행 = verify 13/13 PASS·exit 0 실측; guide §6 "verify = 13/13" 서술 정합; 골든 덮어쓰기 위험 제거 유효. 잔여 = F4(L3 옛 파일명) |
| ch2 tex | 해당 없음 | R9 tex hunk 는 ch1 전용(diff stat 확인) — ch2 는 R9 무변경 |

## E. 물리 불변 확인 (자유 사냥 통독 결과)

- Ch2 전 수식 사슬 재유도 — eq:Z1→occ→muV→logistic→Vxi→BW→Veq_BW→slope_BW(임계 Ω=2RT)→Sconfig→dSconfig→dVdT_config→Svib_mode→Se→implicit_diff→gj→dxidT→weighted→single_config→hys_branch→hys_rev→qrev — 부호·차원·극한(표 tab:limits 6코너) 이상 없음. eq:dxidT 둘째 조각(∂w/∂T=n_jR/F)→종합식 config 계수 n_jR/F 사슬 자기일관.
- 코드 대조: `entropy_coefficient`(L556–592) = Ch2 §2.6 keybox 종합식과 항등(`'n'` 전이 한정 — F1 참조); `reversible_heat` = −I·T·∂U/∂T (T 한 번, eq:qrev); `func_U_branch` σ_d=+1 위 가지 = Ch2 파생 D "dis 가 +½"; z_cut=4.357 = ξ(1−ξ) 정점 5% 컷 독립 재해(u/(1+u)²=0.0125→z=4.357).
- 수치 역산 일치: LCO U(298) = 3.930/3.880/4.050 (dict ΔH·ΔS_eff 역산, F=96485.0); ΔS_e 골 −45.68 (문서 −45.7/−46 정합); 흑연 U(298)=0.211/0.140/0.120/0.085; ΔH(stage 2→1)=−FU+TΔS=−13.0 kJ/mol (Ch2 L362 표값 일치); 2RT@298.15=4957.6 (guide "≈4958"); tab:ds ΔS⁰ 열 = py dict 값 1:1.
- 참조 무결: py·guide·Ch2 가 참조하는 Ch1 라벨 29종 전부 실존(grep, ch1 L840–2670); 회귀 verify 13/13 bit-exact PASS(exit 0) 재실행 확인.

## F. 말미 선언

- **가장 약한 1곳**: 폭 파라미터의 이중 입력형(`'n'` vs `'w'`)이 만드는 잠복 분기 — 그 정점이 F1(`entropy_coefficient` 의 config 항이 `'w'`-단독 전이에서 코드 자신의 T-동결 폭·Ch2 srcbox 전제와 모순, +0.0568 mV/K 실측). 문건은 이 지점을 정직하게 조건부화했지만(파생 A srcbox) 코드는 게이트가 없다.
- **확정 결함 집계**: CRIT 0 · **HIGH 1**(F2) · **MED 2**(F1·F3) → CRIT/HIGH/MED 합계 **3**. LOW 4(F4–F7) · NOTE 2(N1·N2).
- **Coverage 선언**: ch2 tex 전문(1–457·458–777, missing 0) · py 전문(1–725·726–884, missing 0) · guide/demo/plot/회귀/sample 전문(각 98·73·135·84·125행 단위 전량) · R9 diff 대상 hunk 전수 · Ch1 은 라벨 존재 grep + 참조 절 스팟(전문 정독은 본 라운드 범위 외) · 수치 실증 4건(스크립트 실행, 산출물 무변경).
- **빈 통과 아님**: 신규 확정 결함 3건(전부 수치 또는 원문 인용 재현 첨부).

### 5줄 요약 (오적발 자기표시)
1. [HIGH·재현] 스칼라 V+동역학 `dqdv` 가 그리드-의존 분기 뒤집힘으로 −6.9% 침묵 오차(6.704 vs 7.201) — 출하 그림·회귀는 배열이라 무오염, 오적발 아님(수치 재현).
2. [MED·재현] `'w'`-단독 전이에서 `entropy_coefficient` config 오가산 +0.0568 mV/K — FD 대조·`'n'` 대조군 무결로 확정, 오적발 아님.
3. [MED·판단여지] "방전 I>0"(Bernardi=리튬화) vs `curve('discharge')`(탈리튬화) 라벨 층위 코드·데모 미표기 — 수치는 전부 옳아 등급(MED vs LOW)에 이견 여지 있음.
4. [LOW×4] 회귀 docstring 옛 파일명 잔여·미지 mode 침묵 exit 0·guide §7 V8 누락(suite 에 실존)·demo "w 축소"(inert 핸들) — F6 은 의도적 선별일 가능성 낮으나 0 아님(자기표시).
5. R9 hunk 전수 재검 = 전부 올바르게 적용(guide §5 처방·회귀 verify 전환 bit-exact 실증), ch2 는 R9 무변경 · Ch2 물리 사슬·Ch1 라벨 29종·수치 역산 전부 무결.
