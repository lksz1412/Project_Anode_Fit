# V1013 P5 검수 — Round 9 / 검수자 B (부속 문서·스크립트 단위 청크)

> 청크 스킴(R9): **부속 문서·스크립트 파일 단위** — 파일 하나씩 [전문 정독 → 본문 tex(`graphite_ica_ch1/ch2_v1.0.13.tex`)·코드 최종본(`Anode_Fit_v1.0.13.py`, 883줄 전문 정독)과 3자 대조 + read-only 실행 검증].
> 대상 6파일: `FITTING_GUIDE.md` · `test_regression_graphite.py` · `plot_dqdv.py` · `demo_lco_heat.py` · `sample_test_v1013.py` · `V1013_CODE_MAP.md`.
> 역할 규율: 검수 의견만(파일 무수정), 모든 지적에 줄번호·원문 인용, refute mandate 수행. 실행 검증은 프로젝트 파일을 쓰지 않는 경로만(회귀 하네스 verify·본체 self-test·scratchpad 재현 스크립트).

---

## 1. FITTING_GUIDE.md (98줄 전문 정독)

### G1 [HIGH] L32 — ν 권고 수치가 tex 최종본(R3 정정)과 불일치 (기지 이월 확정)
- 원문: "실측 rate-series 피팅 시 **ν≈8–10 권장** — 꼬리 활성 문턱(...)의 이산 점프(~23% 급 L_V 불연속)를 완화한다."
- tex 최종본(ch1 L1727): "$\nu{=}8$: $6.1\%$, $\nu{=}10$: $4.9\%$, 곧 $5\%$ 이내로 낮추려면 $\nu\!\gtrsim\!10$ 이 필요하다."
- 닫힌식 $1-(1/\nu)/(e^{1/\nu}-1)$ 재검산(실행): ν=2→22.9%, ν=8→6.1%, ν=10→4.9% — tex 수치 정확. ν=8 은 5% 문턱을 넘으므로 "8–10" 권고는 정정 전 서술.
- 수정안: "ν≳10 권장(ν=8 은 점프 6.1% 로 5% 초과; ν=10 에서 4.9%)". ~23% 표현은 기본값 ν=2 의 점프이므로 존치 가능.

### G2 [HIGH] L38 — 같은 ν 수치 재등장
- 원문(Phase C): "(= S3; **ν≈8–10** 권고 적용 지점)".
- 수정안: G1 과 동일하게 "ν≳10" 으로.

### G3 [HIGH] L79 (§5 잔차 진단표 마지막 행) — 처방이 v1.0.13 전극 인지 환산과 모순 (따르면 오히려 오적용 재생산)
- 원문: "| LCO 봉우리는 맞는데 rate/히스 거동이 반대 | **방향 규약 오적용(§0)** — 셀 라벨로 σ_d 부여 | **LCO 충전 곡선 ↦ direction=+1 재확인** |"
- 검증: `LCOCathodeDQDV.curve(direction=+1)` 은 `_direction_to_sigma(+1)=+1` 후 `_delith_is_discharge=False` 반전으로 **σ_d=−1(리튬화)** 슬롯에 간다(코드 L530-535, L614-628). 실행 확인: `curve('charge')==dqdv(s=+1)` maxdiff **0.0** / `curve('discharge')==dqdv(s=−1)` maxdiff **0.0**. 곧 이 처방을 curve() 에 그대로 따르면 §0 L8 의 "라벨을 손으로 뒤집어 넣지 말 것"과 정반대 결과.
- 수정안: "LCO 충전 곡선 ↦ `curve(direction='charge')` (자동 σ_d=+1 환산) 또는 저수준 `dqdv(s=+1)` 재확인".

### G4 [MEDIUM] L39 (Phase D) — 전자항 dict 재정렬 지시가 이미 완료된 작업(자기모순 + 코드·tex 모순)
- 원문: "★전자항 dict 를 T1=MIT(최고 x·최저 V) 로 재정렬(Ch1 tab:lco-staging, **현 시연은 중간 dict**)."
- 코드 L642-649: "[v1.0.13 루프 B] 전자항을 물리 anchor(T1=MIT, x_MIT≈0.85 ...) dict 로 **재정렬**(구판은 중간 dict x_MIT=0.50 ...)" — T1 dict 에 `'x_MIT': 0.85` 배정 완료. tex(ch1 L1886-1888): "전자항은 T1$=$MIT dict 에 $x_\mathrm{MIT}{=}0.85$ 물리 anchor 로 배정 — **v1.0.13 재정렬 완료**". 가이드 자신의 L28 도 "재정렬 완료"라 명기 — L39 만 구판 서술.
- 수정안: L39 의 해당 ★문장을 "재정렬 완료(v1.0.13)" 확인 문구로 교체하거나 삭제(뒤의 Sommerfeld T-스케일·eq:U1T2 ½=a_e/2F 과제는 유효 — tex L2376-2382 로 확인 정합).

### G5 [MEDIUM] L5 (§0 heading) — tex 라벨 참조 오기
- 원문: "## 0. 방향 규약 (★LCO 데이터 걸기 전 필독 — Ch1 **sec:lco-peak** 방향 슬롯 한정)".
- tex 실측: 방향 규약 절 = `sec:lco-direction`(ch1 L1912, "$\sigma_d$ 입력 슬롯의 물리 내용은 탈리튬화 여부다") + boxed `eq:lco-sigmaslot`(L1917-1921). `sec:lco-peak`(L2487)은 "LCO dQ/dV peak — 양극 영역의 세 봉우리"로 방향 규약 절이 아님.
- 수정안: "Ch1 sec:lco-direction(eq:lco-sigmaslot)" 로 교체.

### G6 [MEDIUM] L90 (§7) — `graph_suite_p5.py` 가 v1.0.13 폴더에 없고 구버전 코드를 import
- 원문: "신규 validation suite `graph_suite_p5.py`:"
- 실측: 파일은 `Claude\docs\v1.0.10\graph_suite_p5.py` 에만 존재하며 내부 `CODE = ...\v1.0.10\Anode_Fit_v1.0.10.py`(L14)·출력도 v1.0.10\figs 로 고정 — v1.0.13 코드의 검증 suite 가 아님.
- 수정안(P6.1 결정 사항): v1.0.13 으로 이식(import 경로·V6 라벨 현행화 포함) 또는 가이드에 소재·버전 한정을 명기.

### G7 [LOW] L90-98 (§7) — V8 누락
- 가이드 목록은 V1–V7·V9(8개)이나 실물 스크립트에는 **V8(LCO q_rev 전자전이 서명, ax[2,2])** 패널 존재(v1.0.10 suite L95-98). 수정안: V8 행 추가.

### G8 [LOW] L96 (§7 V6) — "x_MIT 불일치 실증" 문구 stale
- 원문: "V6 전자항 골 ΔS_e(x) (x_MIT=0.50 vs 0.85 오버레이) — eq:dSegate·**x_MIT 불일치 실증**".
- 재정렬 완료 후 0.50 은 "구판(pre-v1.0.13) 참조"의 지위(sample_test (d) 라벨과 동일). "불일치 실증"→"구판 시연 대비 물리 anchor 참조 오버레이"로 현행화.

### G9 [INFO] L21 — 온도 표기 미세 불일치
- "Ω>2RT(≈4958**@298K**)": 4957.6 J/mol 은 T=298.15K 값(298K 면 4955.1). 표기 통일 권고 수준.

### 정합 확인(결함 아님, 대조 완료 항목)
- §0 L8 전극 인지 환산 서술 = 수치 실증(diff 0.0, 위 G3 검증). §0 L10 "Omega·dH_a 미배정 → 분극뿐" = 코드 `LCO_MSMR_LIT`(L638-659) 키 부재 확인 + dis/chg maxdiff 0.090(0.5 mV 분극 이동만).
- §1 초기값·기본값: g_max/x_MIT/dx = 13/0.85/0.05(L28) = 코드 L648-649 = tex tab:inputs L2789 = eq:ggate L2390-2391. dVdq_qa 0.30 = 데이터셋 값(tab:inputs 기본 0 은 dict 부재 시 silent off — L26 의 ★경고와 정합). z_cut 4.357·A_cap 4.0·ν 기본 2.0 = 코드 L255-257 = tab:inputs L2775·L2782.
- §6 "test_regression_graphite.py verify = 13/13" = 실행 결과 13/13 OK·PASS.
- 참조 라벨 실재: eq:hyssym(1051)·eq:lco-msmrmap(2669)·tab:lco-staging(1892)·sec:lco-hys(2094)·sec:lco-code(2628)·eq:U1T2(2377, ½=a_e/2F 인자 tex L2379 확인)·Ch2 파생 A(ch2 L446 srcbox L497-521)·파생 B(L549).

---

## 2. test_regression_graphite.py (83줄 전문 정독 + verify 실행)

### T1 [LOW] L2-3 — docstring 사용법의 파일명 구명칭
- 원문: "사용: python **p4_regression.py** capture / verify" — 실제 파일명은 `test_regression_graphite.py`. 수정안: 파일명 갱신.

### T2 [LOW] L47·L56 — area_check "assert" 과장 + 무인자 기본 mode=capture 위험
- L47 docstring "면적=Q **assert**" 이나 함수는 출력만 하고 assert/게이트 없음. verify 실행 실측 ratio=0.936 — 이는 창 [0.03,0.34] 절단 효과(wide-grid 재적분 0.9699998/0.97, 물리 정상)라 gate 를 걸려면 wide-grid 로 걸어야 함.
- L56 `mode = sys.argv[1] if len(sys.argv) > 1 else "capture"` — 인자 없이 실행하면 **골든을 덮어씀**. 기본을 verify 로 바꾸거나 인자 필수화 권고.

### 정합 확인
- import 경로 = v1.0.13 코드(L14-16, env override 포함). 골든 13 배열 구성 = 가이드 §6 "13/13" 일치. **verify 실행: 13/13 OK, `GRAPHITE 0-DIFF: PASS`** — LCO 편입·R2~R8 정정 후에도 흑연 경로 bit-exact 불변 실증.

---

## 3. plot_dqdv.py (135줄 전문 정독)

### P1 [MEDIUM] L54 — 그림 suptitle 버전 문자열 stale
- 원문: `"Anode_Fit 1.0.10 (use_w_eff removed) - dQ/dV bell shapes (code actual output)"` — v1.0.13 산출 그림(파일명도 `anode_fit_v1_0_13_dqdv.png`, L121)에 구버전 표기. 수정안: "Anode_Fit 1.0.13".

### P2 [LOW] L4 — docstring 비문 잔재
- 원문: "radius `fig_bell_vs_spike.png` 식으로 4패널 생성·저장." — "radius" 가 문맥 없이 남은 잔재(이전 프로젝트 그림 명칭 참조로 추정). 문구 정리 권고.

### 정합 확인
- import = `Anode_Fit_v1.0.13.py`(L48). 패널 (2) 의 'n' pop → 'w'=0.012 폴백 시험은 `_n_factor` 우선순위(코드 L301-307)와 정합. 면적보존 재현: 단일 LiC6 wide-grid ∫=0.49938/Q=0.5 — 스크립트 판정 로직(L131, 허용 0.02) 통과 확인.

---

## 4. demo_lco_heat.py (72줄 전문 정독 + scratchpad 재현 실행)

### D1 [HIGH] L36-41·L60-62 — LCO 방향 라벨이 boxed 규약(eq:lco-sigmaslot)과 정반대
- 원문: L36 `print("=== 3. LCO dQ/dV 개형 (방전 σ_d=+1) ===")`, L38 `lco.dqdv(Vc, ..., s=+1)`, L61 라벨 `"dis {lab}"`, L62 제목 `"(b) LCO cathode dQ/dV (discharge, MSMR)"`.
- tex(ch1 L1917-1921 boxed eq:lco-sigmaslot): "σ_d=+1 ⇔ 탈리튬화 ... **LCO 하프셀 — 충전** ↦ +1". 저수준 `dqdv(s=...)` 는 물리 부호 직접(코드 L676: "탈리튬화=+1") — 곧 이 시연 곡선의 물리는 **LCO 충전(탈리튬화)** 인데 라벨은 전부 "방전/discharge". 가이드 §5 마지막 행이 경고하는 "방향 규약 오적용(셀 라벨로 σ_d 부여)" 그 자체를 v1.0.13 동봉 데모가 시연 중. 수치 영향은 현 데이터셋에서 분극뿐(±0.5 mV; dis/chg maxdiff 0.090)이나 라벨-물리 불일치는 규약 위반.
- 수정안: 라벨을 "charge (delithiation, s=+1)" 로 고치거나, 방전 시연이 목적이면 `s=-1`(또는 `lco.curve(direction="discharge")`) 로 호출. sample_test_v1013.py 의 (b) 패널 방식(curve+셀 라벨)이 모범.
- (참고, 범위 밖 메모) 본체 `Anode_Fit_v1.0.13.py` L633-634 의 데이터셋 주석 "방전 σ_d=+1(LCO 리튬화)" 도 같은 계열의 혼동 소지 표현 — 코드 본체 담당 검수 라운드에서 문구 확인 권고.

### D2 [MEDIUM] L39-41 — "국소 피크 ≈ 전이 U" 기대가 실출력과 불일치
- 원문: `print(f"  국소 피크 전위(≈전이 U): ... (목표 3.880·3.930·4.050)")`.
- 동일 코드·격자·문턱(>0.5)으로 재현 실행: 국소 피크 **2개 = [3.919, 4.038]** — 3개 목표 어느 것과도 폭(24-30 mV) 이내로 안 맞음. 원인: U 간격 50 mV vs 봉우리 FWHM ≈ 3.5w ≈ 85-106 mV 로 T1(3.930)·T2(3.880) 봉우리가 병합. "≈전이 U" 서술이 현행 시연 파라미터에서 성립하지 않음.
- 수정안: "(겹침으로 병합 피크 — 분해하려면 w 축소)" 명시 또는 목표 문구를 병합 기대값으로 조정.

### 정합 확인
- dSe 검산 재현: func_dSe_molar(0.85, 298.15)=−45.678(기대 문구 "~ −45.7" 정합, 창 밖 ~0). seam 3경로: 흑연 항등 +29.0 / LCO 전자전이 dS_eff=−39.678(=+6.0−45.678) / 비전자 −4.0 — L26-34 출력 주장 전부 재현 일치. L28 "T1=MIT — v1.0.13 루프 B 재정렬" 주석 현행. L49 q_rev 부호 주석 = Ch2 eq:qrev(L675-676)·코드 L594-602 정합. import v1.0.13 ✓.

---

## 5. sample_test_v1013.py (124줄 전문 정독 + scratchpad 재현)

### S1 [INFO] 등급성 결함 미발견 — 방향 규약·재정렬 반영의 모범 사례
- (b) 패널: `lco.curve(Vc, direction="discharge", ...)`(L67) — 전극 인지 환산 경유 σ_d=−1(리튬화) = 올바른 LCO 방전. (d) 패널: `x_MIT` 를 `LCO_MSMR_LIT[0]` 에서 동적 취득(L92, "T1 realigned to physical anchor 0.85")·0.50 은 "pre-v1.0.13 tier-C demo, reference"(L96) 로 정확히 라벨. dSe 출력(−45.68, target ~−46) 재현 일치. 버전 문자열·import 전부 v1.0.13.
- [LOW·빈 통과 방지 최약점] (b)의 "discharge"(=σ_d=−1, 리튬화)와 demo_lco_heat (b)의 "discharge"(실은 s=+1, 탈리튬화)가 **서로 다른 물리 곡선에 같은 라벨** — 두 그림을 나란히 볼 사용자 혼동 소지. 근본 원인은 D1 이므로 D1 수정으로 해소됨.

---

## 6. V1013_CODE_MAP.md (117줄 전문 정독) — R2~R8·P2.1 재구조화 미반영 다수

### M1 [HIGH] boxed 총계 30 → 현행 38 (Ch1 23→31)
- 원문(L8): "v1.0.13 실측 boxed 총 30개 = Ch1 23개... + Ch2 7개(불변)".
- 현행 grep 실측: **Ch1 31 + Ch2 7 = 38**. Ch1 신규 8건(맵 A절 부재):
  1. 사슬 box(L322, 비라벨 — Part 0 유도 사슬, 개념도)
  2. eq:sm-gc(box L386) — 유도 전용
  3. eq:fermifn(L439) — 유도 전용(func_ksi_eq 의 기원식)
  4. eq:sm-muideal(L494) — 유도 전용
  5. eq:sm-thresh(L552) — Ω≤2RT 단상 판별 ↔ `func_dU_hys` 의 `Omega <= two_RT` 분기(코드 L140-141) 대응 지정 가능
  6. eq:sm-logistic(L680) — ↔ `func_ksi_eq`(L97-100) 재확인(Ch1 eq:xieq 와 공유)
  7. eq:sm-nernst(L794) — 유도 전용(이상 극한)
  8. **eq:lco-sigmaslot(L1917)** — ↔ `_delith_is_discharge`(L248, L686) + `curve()` 환산 분기(L530-535): **loop B 구현물과 1:1 — A절 신설 행 필수**
- 처분: A절에 8행 신설 + 요약 "30건"·"Ch1 23개" 전면 재계산.

### M2 [HIGH] A절 eq:Lq 행 — 현행 tex 기준 오매핑
- 원문(A절): "eq:Lq (box L1688...) | `_resolve_lag_length` 내 A 산출 (L354) | ... `min(z_cut*n_safe*R*T, A_cap*R*T)`".
- 현행 tex: eq:Lq(box L1542) = **L_{q,j}=|I|/(Q_cell·k_j) 용량축 길이 정의식**이고, min(...) 컷은 별도 boxed 아닌 eq:Acut(L1565; C절에 이미 행 존재). 현행 기준 eq:Lq 의 코드 대응 = `func_L_q`(L103-110) 및 `_resolve_lag_length` 의 `L_q = func_L_q(...)`(L371).
- 처분: eq:Lq 행 재작성(구판 tex 라벨 배치 기준의 잔재로 판단).

### M3 [MEDIUM] D절 orphan "LCO_MSMR_LIT 전자항 배정 (x_MIT=0.50, 중간 T2-dict)" 행 stale
- loop B 로 T1 dict·x_MIT=0.85 재정렬 **완료**(코드 L642-649, tex L1886-1888 "v1.0.13 재정렬 완료"). "물리 anchor 와 불일치" 진단·근거("코드 L630-637 데이터와 정확히 대조")가 더 이상 사실 아님. orphan(a) "7건" 요약과 핵심 발견 도입부도 연동 수정 필요.

### M4 [MEDIUM] 헤더 입력 실측치 3종 stale (L3-4)
- "py 860줄"→**883**, "ch1 2230줄"→**2768**, "ch2 731줄"→**730**.

### M5 [MEDIUM] 코드 줄번호 전면 stale (계통 이동 +2~+22)
- 예: eq:vn `V_n=...` L431→**437** / func_ksi_eq L95-98→**97-100** / func_dU_hys L134-141→**136-143** / func_U_branch L144-149→**146-151** / func_dSe_molar L171-186→**173-188** / LCO_MSMR_LIT L625-642→**638-659** / LCO `_effective_dS_rxn` L666-682→**688-704** / equilibrium 합산 L388→**395** / dqdv 평형분기 L487→**493** / peakshape L498→**504** / 합산·interp L500·502→**506·508** / entropy_coefficient L545-579→**556-592** / reversible_heat L581-589→**594-602** / `_direction_to_sigma` L606-613→**614-628** / 가드 L190-211→**192-213** / `__main__` L725-861→**747-883**. P6.1 에서 일괄 재실측 필요.

### M6 [MEDIUM] tex 줄번호 전면 stale
- 예: eq:vn box L379→**839** / eq:Uj L459→**922** / eq:xieq L983→**1173** / eq:dSegate L1297-1300→**2404-2408** / tab:inputs L2193-2226→**2756-2793**(핵심 발견 1 의 참조 포함 2곳) / eq:lco-plugin L2175-2178→**2736-2742** / Ch2 eq:logistic L152-153→**158** / eq:qrev L672→**675** / use-this box L699-701→**703-705**. Ch2 boxed 7건의 집합 자체는 불변(정합).

### M7 [LOW] E절 — loop B 신규 코드 요소 미등재
- `_delith_is_discharge` 속성·`curve()` 반전 분기가 E절(코드O·문건X)에도 A/C절에도 없음. 단 tex 가 이미 문서화(tab:inputs L2790·sec:facade L2812-2814·eq:lco-sigmaslot)했으므로 orphan(b)가 아니라 **A절 매핑 행 신설**(M1-⑧)이 올바른 처분.

### M8 [INFO] eq:dSegate 행 "실측 −45.655" — T=298 값(T=298.15 면 −45.678)
- 재검산으로 두 값 모두 재현. 온도 명기만 권고(코드 docstring 검산 문구는 −45.678/T_ref=298.15 계열).

### 정합 확인(현행 코드에서 여전히 유효한 맵 내용)
- 발견 2(LCO Ω 미배정 → 히스 구조 구현·수치 비활성) ✓ / 발견 3(eq:lco-plugin 부분 구현 — `x_center` 고정 스칼라, 코드 L702) ✓ / 발견 4(`func_U_j_hys` dead code — 정의 L83-94, 활성 경로 미호출) ✓ / q_irr lumped-only(코드 L604-612, Ch2 boxed 부재) ✓ / eq:U1T2 미구현·동결 근사(eq:lco-U1V) 구도 ✓.

---

## [가이드 수정 필요] 통합 목록 (P6.1 일괄 반영용)
| # | 위치 | 내용 | 등급 |
|---|---|---|---|
| G1 | L32 | ν≈8–10 → **ν≳10**(ν=8 은 6.1%) | HIGH |
| G2 | L38 | 동일 ν 수치 정정 | HIGH |
| G3 | L79 | 처방 "direction=+1" → "`curve(direction='charge')` 또는 저수준 `dqdv(s=+1)`" | HIGH |
| G4 | L39 | "현 시연은 중간 dict" 삭제 — 재정렬 완료(L28 과 자기모순 해소) | MEDIUM |
| G5 | L5 | sec:lco-peak → **sec:lco-direction**(eq:lco-sigmaslot) | MEDIUM |
| G6 | L90 | graph_suite_p5.py 소재·버전(v1.0.10 import) — 이식 또는 한정 명기 | MEDIUM |
| G7 | L90-98 | V8(LCO q_rev 전자 서명) 행 누락 보충 | LOW |
| G8 | L96 | V6 "불일치 실증" → 구판 참조 오버레이로 현행화 | LOW |
| G9 | L21 | 2RT 온도 표기(298 vs 298.15) 통일 | INFO |

## [CODE_MAP 현행화 필요] 통합 목록 (P6.1 현행화 자료)
| # | 내용 | 등급 |
|---|---|---|
| M1 | boxed 30→38(Ch1 23→31); 신규 8건(7 SM boxed + eq:lco-sigmaslot) A절 행 신설·요약 재계산 | HIGH |
| M2 | eq:Lq 행 오매핑 — 현행 eq:Lq(L1542)=L_q 정의식 ↔ func_L_q/L371; min 컷은 eq:Acut(C절 기존 행) | HIGH |
| M3 | D절 x_MIT=0.50 orphan 행·요약 7건·관련 서술 — loop B 재정렬 완료 반영 | MEDIUM |
| M4 | 헤더 실측치: py 883줄·ch1 2768줄·ch2 730줄 | MEDIUM |
| M5 | 코드 줄번호 전면 재실측(+2~+22 이동, 대표 20여 곳 위 §6 M5) | MEDIUM |
| M6 | tex 줄번호 전면 재실측(tab:inputs 2756-2793 등) | MEDIUM |
| M7 | `_delith_is_discharge`/curve() 환산 = A절 신설(M1-⑧와 동일 건) | LOW |
| M8 | dSegate 실측값 온도 명기(−45.655@298 / −45.678@298.15) | INFO |

## 스크립트 수정 필요(참고 — 가이드·맵 외)
- D1 [HIGH] demo_lco_heat.py 방향 라벨(방전↔s=+1) — eq:lco-sigmaslot 위반.
- D2 [MEDIUM] demo_lco_heat.py 피크 기대문("≈전이 U", 목표 3값)이 실출력(병합 2피크 3.919·4.038)과 불일치.
- P1 [MEDIUM] plot_dqdv.py suptitle "1.0.10" → 1.0.13.
- T1/T2/P2 [LOW] 하네스 docstring 구명칭·capture 기본값·area assert 과장·plot docstring 비문.

---

## 가장 약한 1곳 (필수 지목)
**FITTING_GUIDE.md L79 (G3)** — 잔차 진단표에서 "방향 규약 오적용"을 교정하라고 만든 행의 처방("LCO 충전 곡선 ↦ direction=+1")을 v1.0.13 `LCOCathodeDQDV.curve()` 에 그대로 따르면 전극 인지 환산이 σ_d=−1 로 뒤집어 **정확히 그 오적용을 재생산**한다(실행 검증: curve('charge')=dqdv(s=+1) bit-exact, curve(+1)=dqdv(s=−1)). 진단표는 피팅 실무자가 문자 그대로 따라 하는 표라 G-follow·G-usable 1급 결함이며, 같은 뿌리의 라벨 혼동이 동봉 데모(demo_lco_heat, D1)에서도 실제 발생해 있다.

## 물리 불변 확인 (실행 근거)
1. 흑연 회귀 0-diff: `test_regression_graphite.py verify` **13/13 np.array_equal PASS** — LCO 편입·R2~R8 정정 후 흑연 경로 bit-exact 불변.
2. 면적보존: wide-grid ∫dQdV = 0.49938/Q=0.5(단일 LiC6)·0.9699998/ΣQ=0.97(4전이) — 보존(하네스의 ratio 0.936 은 창 절단 효과, 물리 위반 아님).
3. LCO U(298.15) 순전파(R3 재역산 dH −391016.1/−375554.4/−391360.0): 3.930000/3.880000/4.049994 V — 목표 정합(seam 전자항 −45.678 포함).
4. ν 문턱 점프 닫힌식 재검산 = 22.9%/6.1%/4.9%(ν=2/8/10) — tex 수치 일치.
5. 방향 환산 항등: curve↔dqdv 대응 maxdiff 0.0(bit-exact), dis/chg 차이 = 분극 이동뿐(LCO 현 데이터셋).
6. 본체 self-test: guards 7/7·per-tr override 격리·Ω=2RT→gap 0·γ=0/|I|→0 dis=chg — overall OK True.

## Coverage 선언
- 검수 대상 6파일 **전문 정독**: FITTING_GUIDE.md 98줄 · test_regression_graphite.py 83줄 · plot_dqdv.py 135줄 · demo_lco_heat.py 72줄 · sample_test_v1013.py 124줄 · V1013_CODE_MAP.md 117줄 (계 629줄, head→tail 생략 없음).
- 대조 기준: `Anode_Fit_v1.0.13.py` **883줄 전문 정독**(1-727 + 728-883). tex 는 대조 기준 자료로서 라벨(\label)·boxed 전수 grep(ch1 165 라벨·31 boxed / ch2 32 라벨·7 boxed) + 쟁점 구간 직독(ch1 L1530-1569·1706-1760·1880-1995·2355-2414·2487-2496·2745-2814, ch2 L690-714, 계 약 330줄) — tex 자체의 전문 검수는 본 라운드 청크 스킴의 범위 밖(타 검수자 담당).
- 실행 검증 4종(회귀 verify·본체 self-test·scratchpad 수치 재현 2회) 전부 프로젝트 파일 무수정 경로.

## 5줄 요약 (오적발 자기표시)
1. 가이드 3건 HIGH: ν≈8–10(기지 이월, tex ν≳10 확정)·§5 처방 direction=+1(따르면 σ_d=−1 오적용 재생산, 실행 실증)·Phase D "현 시연은 중간 dict"(재정렬 완료와 모순).
2. CODE_MAP 은 boxed 30→38(신규 8: SM 7 + eq:lco-sigmaslot)·eq:Lq 행 오매핑·x_MIT orphan stale·줄번호 전면 stale — P6.1 전면 현행화 필요.
3. demo_lco_heat 는 LCO s=+1 을 "방전"으로 라벨(eq:lco-sigmaslot 정반대) + 피크 기대문이 실출력(병합 2피크)과 불일치; sample_test 는 규약 준수 모범.
4. 물리 불변 전부 확인: 회귀 13/13 bit-exact·면적보존·U(298) 순전파·ν 점프 닫힌식·방향 환산 항등.
5. [오적발 가능성 자기표시] G5(sec:lco-peak — 의도적 축약 참조였을 가능성, 다만 라벨 실물과 불일치는 사실)·D2(데모가 "보고용 출력"이라 주장할 여지, 다만 "≈전이 U" 문구는 객관적으로 불성립)·G9/M8/T2 는 INFO~LOW 경계 — 등급 하향 여지 인정.
