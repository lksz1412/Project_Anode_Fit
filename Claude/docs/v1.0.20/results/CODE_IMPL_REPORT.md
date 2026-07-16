# CODE_IMPL_REPORT — Anode_Fit v1.0.20 코드 실구현 (스트림 2)

- 원칙: **doc-leads** — 문건(v1.0.20 Ch1/Ch2)이 권위, 코드가 문건을 따른다.
- 베이스: `Claude/docs/v1.0.19/Anode_Fit_v1.0.19.py` (1151줄 전문 정독 완료)
- 산출물 A: `Claude/docs/v1.0.20/Anode_Fit_v1.0.20.py` — **완료**
- 산출물 B: 본 보고서 — **완료** (조기 저장 후 단계 append, 최종 갱신 2026-07-16)
- 게이트 하네스: `Claude/docs/v1.0.20/test_gates_v1020.py` (G1/G2/G3 + n(T) 부록, 재실행 가능)
- 실행 환경: Python 3.11.15 · numpy 2.4.6 (기설치 — pip 불필요) · Linux 컨테이너

## 최종 판정: **G1 PASS · G2 PASS · G3 PASS** (+ n(T) 전파 증빙 PASS)

---

## 0. 입력 정독 확인 (전문 정독 의무)

| # | 파일 | 상태 | 핵심 확인 |
|---|---|---|---|
| 1 | `docs/v1.0.19/Anode_Fit_v1.0.19.py` (1151줄) | 전문 정독 완료 | x̄ 진입점 3종(`solve_U_oc`·`entropy_coefficient_x`·`reversible_heat_x`)·vib Einstein(`_vib_theta/_S_vib/_vib_dU/_vib_dS`)·n(T) 선형 잔여(`_n_factor`/`_dwdT`)가 **이미 v1.0.19 에 구현되어 있음** |
| 2 | `docs/v1.0.20/_sections/ch1_appB_codemap.tex` (157줄) | 전문 정독 완료 | 기호↔식별자 대응표·`n_T1/n_T_ref` 폭 다중도 선형 잔여(부재=상수 n bit-exact, 발효 시 폭·config 동반 전파)·x̄ 진입점 노드행 |
| 3 | `docs/v1.0.20/_sections/ch2_appB_codemap.tex` (69줄) | 전문 정독 완료 | B.1 진입점 명명·B.2 회귀 기준값 표·B.3 θ_E 하위호환(bit-exact)·B.4 입력 규약(s=+1·평형 중심·두-상 자유 폭) |
| 4 | `docs/v1.0.20/_sections/ch2_sec08_synthesis.tex` (144줄) | 전문 정독 완료 | eq:complete 완전식·계산 예제 (a)~(e) 수치·tab:worked·tab:qrev 5점 |
| 5 | `docs/v1.0.20/_sections/ch2_sec05_mixing.tex` (240줄) | 전문 정독 완료 | eq:implicit·eq:implicit_diff·eq:gj·eq:dxidT·eq:dwdT-nT·파생 A srcbox(175점·T1=292.15/T2=298.15·경계 3곳 연속·스팬 의존 명시) |
| 6 | `docs/v1.0.20/_sections/ch2_sec04_einstein.tex` (115줄) | 전문 정독 완료 | eq:Svib-einstein·eq:dSvib·eq:dUvib·C-62 수치(−3.74/0/+3.70/+9.14 µV/K @ θ_E=700K) |
| 7 | `docs/v1.0.19/FITTING_GUIDE.md` (135줄) | 전문 정독 완료 | §1.5 폭 4단 사다리·§1.6 θ_E 규약·§6 흑연 회귀 0-diff 게이트·§7 검증 세트 |
| 보조 | `docs/v1.0.19/test_regression_v1019.py` · `results/research/CH2v4/42_numerical_verification.md` · `_sections/ch1_sec10_sum.tex(tab:staging)` · `results/RESULT_P0_setup.md` | 정독 완료 | 골든 하네스 케이스 구성·파생 A 원 검증 규약(x̄∈[0.05,0.95]·FD T1=292.15/T2=298.15·해석식 295.15 K 평가·경계 midpoint ~0.455/0.645/0.815)·staging 초기값 문건 대조·환경 잡음 P0=4.33e-15 |

## 1. 문건 요구 ↔ v1.0.19 베이스 대조 (구현 갭 진단)

| 요구 (문건) | v1.0.19 베이스 상태 | v1.0.20 조치 |
|---|---|---|
| B.1 `solve_U_oc(x̄,T)` = eq:implicit 유일근 솔버 | 구현됨 (이분법·단조 좌변·자동 괄호·tol 1e-13) | 승계 (무변경) |
| B.1 `entropy_coefficient_x(x̄,T)` = 근에서의 eq:complete | 구현됨 (`return_terms` 로 완전식/단순식/config 분리 포함) | 승계 (무변경) |
| B.1 `reversible_heat_x(x̄,T,I)` = eq:qrev 출구 | 구현됨 (−I·T·∂U/∂T, T 한 번) | 승계 (무변경) |
| B.1 기존 `entropy_coefficient(V_n,T)` 유지 (하위호환) | 유지됨 | 승계 (무변경) |
| B.3 θ_E Einstein 보정 — 선택적, 미지정 시 두 가산(ΔU_vib·ΔS_vib) 항등 0 = bit-exact | 구현됨 (`theta_E`/`theta_E_Tref`) — 식형 대조: `_S_vib`=eq:Svib-einstein, `_vib_dS`=eq:dSvib, `_vib_dU`=eq:dUvib(ΔF_vib=RT·ln(1−e^{−θ/T}) 경유·∂ΔU_vib/∂T=ΔS_vib/F round-trip) **일치** | 승계 + G3 수치 증빙 |
| ch1_appB n_j(T)=n_j+n_T1(T−T_ref) — 부재 시 상수 n bit-exact, 발효 시 ∂w/∂T=(R/F)(n(T)+T·dn/dT) 동반 전파 | 구현됨 (`_n_factor`·`_dwdT`) — 식형 대조: eq:dwdT-nT **일치** | 승계 + 부록 수치 증빙 |
| B.4 평형 ξ_j = s=+1·평형 중심(분기 shift 無) | 준수 (`solve_U_oc`/`equilibrium`/`entropy_coefficient` 모두 `func_ksi_eq` 기본 s=+1·`func_U_branch` 미적용) | 승계 (무변경) |
| B.4 두-상 폭 자유 입력 (강제 nRT/F 금지) | 준수 (`w`\|`n` 자유 키; 'w'-단독은 T-동결 → config 자동 소거 `_dwdT=0` = 단순식, ch2 파생 C 정합) | 승계 (무변경) |
| staging 파라미터 = v1.0.19 기존 값 그대로 (문건 tab:staging 대조 확인만) | `GRAPHITE_STAGING_LIT` = tab:staging 전 항목 일치 확인: U 0.210/0.140/0.120/0.085 V · ΔH −11700/−13500/−13100/−13000 · ΔS +29/0/−5/−16 · Q 0.10/0.12/0.25/0.50 · Ω 6000/8000/10000/13000 · ΔH_a 48000/46000/44000/40000 · dVdq 0.30 · n=1 · w 폴백 0.020/0.016/0.014/0.012 · ΔS_a=0 | 승계 (무변경) |

**진단 결론**: 문건 v1.0.20 부록 B 요구명세를 v1.0.19 구현이 전건 충족 → v1.0.20 = **버전 문자열·헤더 주석만 갱신한 정합 이월**(물리·수치 경로 0 변경, 함수 본문 0 변경). 이 결정이 G1/G3 을 구조적으로 보장하며, 아래와 같이 전건 수치 실행으로 증빙했다.

## 2. 구현 항목표 (최종)

| 항목 | 상태 |
|---|---|
| A. `Anode_Fit_v1.0.20.py` 생성 (헤더 v1.0.20·계보 1.0.19→1.0.20 추가·근거 문건 포인터 v1.0.20) | **완료** |
| 게이트 스크립트 `test_gates_v1020.py` (G1/G2/G3 + n(T) 부록, 전건 수치 실행) | **완료** |
| G1 실행·증빙 | **PASS** |
| G2 실행·증빙 (B.2 전건 + tab:worked + tab:qrev 전 열 + 파생 A 175점 + 경계 3곳) | **PASS** |
| G3 실행·증빙 (θ_E bit-exact + 발효 + C-62) | **PASS** |
| n(T) 전파 증빙 (부록) | **PASS** |
| 모듈 자체 `__main__` 검증 (v1.0.19 계승 self-test) | **PASS** (`>>> overall OK: True`) |

## 3. v1.0.19 대비 변경 목록

**변경 함수: 없음 (0건).** 전 함수·클래스·데이터셋·`__main__` 본문 바이트 동일. 변경은 파일 상단 주석 4곳뿐:

| 위치(라인) | 변경 내용 |
|---|---|
| 3 | `release 버전 = 1.0.19` → `= 1.0.20` (문건 Ch1/Ch2 1.0.20 matched) |
| 4 | 구현 계보에 `→ 1.0.20` 추가 |
| 6–7 | 1.0.20 항목 신설: 문건 v1.0.20 부록 B 정합 이월 — B.1/B.3/n(T) 전부 v1.0.19 승계·물리 무변경·게이트 재증빙 명시 |
| 9 | 구현 표제 `— 1.0.19 (2026-07-08)` → `— 1.0.20 (2026-07-16)` |
| 40 | 근거 문건 포인터 `graphite_ica_ch1_v1.0.19.tex(+ch2)` → `v1.0.20` |

`diff` 전문이 위 6줄(3,4,6→6-7,8→9,39→40)로 닫힘을 확인. 모델명·AI 식별자 미포함(헤더 검수 완료).

## 4. G1 — 하위호환 (PASS)

신기능(θ_E·n_T1) 전부 미지정 상태, 동일 입력 그리드에서 v1.0.19 모듈 vs v1.0.20 모듈 직접 대조:

- **비교 배열 30종** (흑연: equilibrium·dqdv 충/방전×3 C-rate·온도 3종·비등온 T(V)·curve facade·스칼라 V·`entropy_coefficient` 스칼라/배열 T·`return_terms` 3항·`reversible_heat`·`solve_U_oc`·`entropy_coefficient_x` 4항·`reversible_heat_x`·`seed_L_V` + LCO: equilibrium·curve 충/방전·entropy_coefficient)
- 결과: **전건 `np.array_equal` bit-exact, max|Δ| = 0.000e+00** (게이트 ≤1e-12 충족, 여유 무한대)
- 보조(골든): v1.0.19 골든 `golden_graphite_ref.npz`(원 캡처 머신 기준) 대비 회귀 하네스 동일 13 케이스 — **max|Δ| = 4.330e-15 ≤ 1e-12 PASS** (본 컨테이너 환경 잡음 기준 P0 = 4.33e-15 와 정확히 일치 — 머신 간 부동소수 잡음, v1.0.19 자신도 이 컨테이너에선 동일 편차)

## 5. G2 — 회귀 기준값 (ch2_appB B.2, 표시 정밀도 일치) (PASS)

전건 **표시 정밀도 문자열 일치**(display == doc)로 판정. 298.15 K·4-전이 staging·w=RT/F(`'n':1` 우선).

### 5.1 계산 예제 x̄=0.25 (§2.8 (a)~(e))

| 항목 | 산출값(전 자리) | 표시 | 문건 | 판정 |
|---|---|---|---|---|
| U_oc | +74.351141 mV | 74.4 | 74.4 | OK |
| ∂U_oc/∂T 완전식 | −0.203946 mV/K | −0.204 | −0.204 | OK |
| 단순식 | −0.133958 mV/K | −0.134 | −0.134 | OK |
| config | −0.069988 mV/K | −0.070 | −0.070 | OK |
| ΔS = F·∂U/∂T | −19.677727 J/mol/K | −19.7 | −19.7 | OK |
| Q̇_rev/I = −T·∂U/∂T | +60.806492 mV | +60.8 | +60.8 | OK |
| round-trip [U(T+3)−U(T−3)]/6K | −0.203946 mV/K | −0.204 | −0.204 | OK |
| \|round-trip FD − 해석 완전식\| | **1.139e-05 µV/K** | — | <0.001 µV/K | OK |

### 5.2 tab:worked 전이별 중간값 (전건 표시 일치)

Σ Q_j g_j = 6.1771 /V → 표시 6.18 (문건 6.18) OK. 전이별 ξ_j/g_j/비중/ΔS⁰_j/F/config = 0.005/0.19/0.003/+0.301/−0.458 · 0.072/2.61/0.051/0.000/−0.220 · 0.143/4.77/0.193/−0.052/−0.154 · 0.395/9.30/0.753/−0.166/−0.037 — **4전이 × 5열 전건 OK**.

### 5.3 tab:qrev 5점 (전 열: U_oc·∂U/∂T·ΔS·Q̇_rev/I)

| x̄ | U_oc [mV] | ∂U/∂T [mV/K] | ΔS [J/mol/K] | Q̇_rev/I [mV] | 판정 |
|---|---|---|---|---|---|
| 0.10 | 43.5 (43.5) | −0.307 (−0.307) | −29.6 (−29.6) | +91.5 (+91.5) | OK |
| 0.25 | 74.4 (74.4) | −0.204 (−0.204) | −19.7 (−19.7) | +60.8 (+60.8) | OK |
| 0.50 | 109.0 (109.0) | −0.089 (−0.089) | −8.6 (−8.6) | +26.6 (+26.6) | OK |
| 0.75 | 148.8 (148.8) | +0.044 (+0.044) | +4.3 (+4.3) | −13.2 (−13.2) | OK |
| 0.90 | 195.2 (195.2) | +0.218 (+0.218) | +21.0 (+21.0) | −64.9 (−64.9) | OK |

발열→흡열 부호 교대(저-x̄ 발열/고-x̄ 흡열) 재현.

### 5.4 파생 A — 175점 전 범위 + 내부 경계 3곳 연속

원 검증(42_numerical_verification.md) 규약 승계: FD = [U_oc(x̄,298.15)−U_oc(x̄,292.15)]/6 K, 해석식은 중점 295.15 K 평가. 그리드 = **x̄∈[0.05,0.95] 균일 175점**(문건 인용 스팬 전 범위·양끝 포함 — 원 검증의 181점−제외 6점보다 엄격한 전수 판정).

- **완전식 vs FD: max = 2.948e-07 mV/K, mean = 4.290e-08 mV/K** — 게이트 ≲1e-2 mV/K 를 4자릿수 여유로 충족(문건 "절대오차 ≈0·잔차 수 µV/K 급 이하" 정합; 원 검증의 보간 역산 대신 솔버 직해라 잔차가 더 작음)
- 내부 경계 3곳 연속 블렌드(모두 OK):
  - 경계 1 (2→1 ↔ 2L→2): x̄_mid=0.453, ∂U/∂T=−0.1100 mV/K ∈ (−0.166, −0.052) ✓ · 국소 최대 스텝 2.3 µV/K (<25) ✓
  - 경계 2 (2L→2 ↔ 3→2L): x̄_mid=0.643, −0.0207 mV/K ∈ (−0.052, 0.000) ✓ · 2.9 µV/K ✓
  - 경계 3 (3→2L ↔ 4→3): x̄_mid=0.817, +0.1018 mV/K ∈ (0.000, +0.301) ✓ · 6.2 µV/K ✓
  - (원 검증 §8 의 midpoint 0.455/0.645/0.815·FD_mid −0.1091/−0.0196/+0.0996 과 정합 — 본 판은 295.15 K 자가산출 봉우리 중점)
- 전 곡선 스텝당 최대 변화 13.5 µV/K (원 검증 181점 기준 13 µV/K/step 과 동급) — 계단 부재
- [참고·게이트 외] 단순식 vs FD max = 0.2273 mV/K, config 스팬 = [−0.227, +0.139] mV/K — 문건 값(0.18 그리드 실측/해석 상한 0.21·[−0.21,+0.14])과의 차이는 문건 스스로 명시한 **그리드 x̄ 스팬 의존**(srcbox: "그리드 양끝에서 계속 커지는 스팬-의존 양"·"그리드 실측 최대값 0.18 은 극값을 정확히 샘플하지 않은 결과, 해석 상한 0.21") 범위 내 — 본 판은 양끝(0.05·0.95)을 실제 샘플하므로 더 큼. 게이트 항목 아님·문건 불일치 아님.

## 6. G3 — θ_E 미지정 경로 bit-exact (PASS)

- **직접 증빙**: vib 가산 4곳(` + self._vib_dU(tr, T)` ×3 [equilibrium·entropy_coefficient·solve_U_oc]·` + self._vib_dU(tr, T_prog)` ×1 [dqdv]·`dS0 + self._vib_dS(tr, T)` ×1 [entropy_coefficient])을 소스에서 제거한 **'보정 도입 이전' 변형 모듈**을 즉석 생성(패턴 발생 횟수 고정 검증 — 소스 드리프트 시 즉시 FAIL), θ_E 미지정 v1.0.20 과 30개 배열 전건 대조 → **전건 `np.array_equal` bit-exact, max|Δ| = 0.000e+00**
- 발효 확인: tr[3] 에 θ_E=700 K 부여 → T_ref=298.15 K 출력 **불변**(ΔU_vib(T_ref)=0 자동) · T=318.15 K max|Δ|=2.374e-03 (>0, 보정 실발효)
- C-62 수치(∂ΔU_vib/∂T = ΔS_vib(T)/F, θ_E=700 K·T_ref=298.15): −3.7382/+0.0000/+3.7000/+9.1378 µV/K @ 278.15/298.15/318.15/348.15 K → 표시 −3.74/0/+3.70/+9.14 — **문건 4점 전건 일치**

## 7. 부록 — n(T) 선형 잔여 전파 증빙 (ch1_appB) (PASS)

- `n_T1=0.0` 명시 부여 vs 부재: equilibrium·dqdv·entropy_coefficient·solve_U_oc 전건 값 bit-exact (`np.array_equal` True)
- `n_T1=5e-4` 발효: ∂w/∂T 해석식 `_dwdT`=(R/F)(n(T)+T·n_T1)=9.901445354e-05 V/K vs `_width` 중심차분 — 상대차 2.67e-14 (w(T) 2차식이라 중심차분 이론상 정확 일치, 확인됨)
- `n_T1=5e-4` round-trip(x̄=0.25): FD −0.214379 vs 해석 완전식 −0.214379 mV/K, |Δ| = 1.670e-05 µV/K — **일반화 config 계수가 폭(솔버)과 가역열(완전식)에 자기정합 전파**(eq:dwdT-nT) 실증

## 8. 관찰 사항 (보고만 — 수정 없음, doc-leads)

1. **ch1_appB_codemap.tex 5행의 구현 파일명이 `Anode_Fit_v1.0.19.py`** 로 남아 있음(v1.0.20 문건 내). 본 과제 산출물명은 지시대로 `Anode_Fit_v1.0.20.py` — 문건 쪽 포인터 갱신 여부는 master 판단 사항 (tex 수정 금지 준수, 미수정).
2. θ_E·(ΔH_rxn,ΔS_rxn) 서식 결합: vib 보정은 `dH_rxn/dS_rxn` 서식 전이에서만 발효하며 `'U'`-단독 서식 전이에 θ_E 를 얹으면 silent 무시(v1.0.19 거동 그대로 승계 — FITTING_GUIDE 의 dS_rxn silent 규정과 같은 계열). 거동 변경은 하지 않음(하위호환 우선), 추가 후보로만 기록: `'U'`+`theta_E` 조합 fail-fast 가드.
3. 파생 A 참고치(단순식 max·config 스팬)의 그리드 의존은 §5.4 에 기록 — 문건 자체가 스팬-의존을 명시하므로 불일치 아님.
4. v1.0.19 폴더는 읽기 전용 사용(게이트 하네스 `sys.dont_write_bytecode` — pyc 미생성, 기존 `__pycache__` 는 본 작업 전 17:40 생성분 그대로).

## 9. 재현 명령

```
cd Claude/docs/v1.0.20
PYTHONIOENCODING=utf-8 python test_gates_v1020.py      # G1/G2/G3 + n(T) 전건
PYTHONIOENCODING=utf-8 python Anode_Fit_v1.0.20.py     # 모듈 자체 self-test (overall OK: True)
```
