# V1010 인계 무결성 대검수 — draft O2 (코드 인계 + 그래프 물리 정합)

> 검수자 ID=**O2** · 초점 ROLE=**코드 인계(v11_final→v1.0.10) + 그래프 물리 정합**. 독립 검수, 코드·문건 수정 0(v1.0.10 동결, 결과는 v1.0.11 핸드오버 갱신용). 모든 판정은 실측(두 코드 직접 실행)·코드 줄·tex 줄·SPEC 기록 줄 근거. 추정 최소화, 문제 발견 우선(union·refute·가장약한1곳·빈통과금지).
>
> **실측 방법**: `Anode_Fit_v11_final.py`(SPEC)·`Anode_Fit_v1.0.10.py`(현행)를 Python 3.12.10 / numpy 2.4.3 / scipy 1.17.1 로 각각 로드해 동일 조건에서 FWHM·면적·peak·병합·byte-diff 를 측정(스크립트 = scratchpad `measure_o2*.py`). 아래 수치는 전부 코드 실제 출력이며 추정이 아니다.

---

## 0. 핵심 실측표 (두 코드 직접 실행 — 추측 아님)

| 케이스 | v11_final | v1.0.10 | 판정 |
|---|---|---|---|
| `_n_factor('w'=0.012 & 'n'=1.0)` | **1.0** ('n' 우선) → `_width`=25.691 mV | **1.0** (동일) | 'w'=12mV 폴백 **inert**(양 파일 동일) |
| 단일 LiC₆ 평형, STAGING as-is (w=0.012 & n=1.0) | FWHM **90.52 mV** · area **0.5000** | FWHM **90.52 mV** · area **0.5000** | **byte 동일** · 면적보존 |
| 단일 LiC₆, 'n' 제거 → 'w'=12mV 활성 | FWHM **42.21 mV** · area 0.5000 | FWHM **42.21 mV** · area 0.5000 | 42mV = 'w' 경로 (6-30 "기본" 행의 실체) |
| 단일 LiC₆, `use_w_eff`=True (w/n 없음) | FWHM **90.52 mV** · area **9.9998** (깨짐) | **경로 없음**(제거됨) | v1.0.10 이 버그 경로 제거 |
| full 4-staging 평형 (default) | local max **1개** · max 7.350 | local max **1개** · max 7.350 (동일) | 4 전이 → 단일 bell 병합 |
| 평형 곡선 v11 vs v1.0.10 (default) | — | — | **max_abs_diff = 0.000e+00** |
| dqdv 방전 v11 vs v1.0.10 (default) | — | — | **max_abs_diff = 0.000e+00** |
| 폭의 Ω 의존 (default `_width`) | — | Ω=0/6000/13000/50000 전부 FWHM 90.47 mV | 폭 **Ω-무관**(상분리 무반영) |

해석식 대조(독립 검산): logistic 미분 종의 FWHM = 3.525·w. w=RT/F=25.69mV → 90.57mV(실측 90.52), w=12mV → 42.31mV(실측 42.21). **완전 일치 — 코드가 eq:wbase(w=nRT/F)·eq:belliden(logistic 종)을 정확히 구현**.

---

## 1. 인계 판정 항목 (등급 · 위치 · 무엇이 인계됐나/문제 · 왜 · 렌즈)

### [PASS·정당] O2-A — `use_w_eff` 제거가 6-30 진단(면적보존 버그)대로 정당히 이행됨
- **위치**: 현행 `Anode_Fit_v1.0.10.py` L4·L7·L305(주석만)·`_width` L303-306 (live 코드 0) / SPEC = `CODE_w_check.md` L9·L14·L20 · `HANDOVER_2026-06-30_*.md` §2(D) L46·L53(과제 D-1) · Ch1 tex L20·L32.
- **무엇이 인계됐나**: 6-30 CODE_w_check 가 `use_w_eff`를 "면적 위반 버그(ξ_eq 폭 ≠ 분모 w)"로 진단(실측 area 9.294, FWHM 90.6). v1.0.10 은 `func_w_eff`·`use_w_eff`·`w_eff_floor_frac` 를 **live 코드에서 완전 제거**(grep 결과 3줄 전부 주석). 실측 재현: v11_final `use_w_eff`=True → **area 9.9998**(내가 직접 재현, 6-30 의 9.294 와 grid 차만) / v1.0.10 → 그 경로 자체 부재.
- **왜 정당**: (축1 논리 무결) 제거가 default 거동을 바꾸지 않음이 실측으로 확정 — 평형·dqdv 곡선 v11 vs v1.0.10 **max_abs_diff=0.000e+00**. 즉 `use_w_eff`는 default(=False)에서 이미 dead-path 였고, 제거는 순수 죽은 경로 적출이라 회귀 0. 물리적으로도 6-30 결론(Ω↑→narrowing 은 방향 반대·two-phase 실측은 종이지 델타 아님)과 정합.
- **렌즈**: 이전 문제(버그)→개선 의도(제거)→실제 개선(live 0·회귀 0)→우수구조 보존(default 거동 byte 동일)→v1.0.10 인계 = **5/5 온전**.

### [PASS·정당] O2-B — w 이중지위가 코드('n' 우선 · 'w' 폴백 inert)와 문건이 정합
- **위치**: 코드 `_n_factor` L294-300 · `_width` L303-306 / Ch1 tex `sec:width` L716-743·L724·L1255-1257 / SPEC 6-30 과제 V8-1 ① L54.
- **무엇이 정합**: 코드 `_n_factor` 는 (1)'n' 직접 (2)'w'→n=w·F/RT 역산 (3)없으면 1 순. STAGING dict 는 'w'와 'n':1.0 **둘 다** 보유 → 'n' 우선 → 폭=RT/F=25.7mV, 'w'=12mV **inert**(실측: `_n_factor`=1.0 반환). tex 는 이를 **은닉 없이 명시** — L1255-1257 "현재 코드의 staging 출발값은 n_j=1 고정이라 실제 평가 폭은 RT/F≈25.7mV이고, 0.012/0.014V 등 'w' 폴백은 'n'을 제거해야 활성화된다". 그림 panel(2) 범례도 "default n=1.0 (w=RT/F): FWHM 84mV / explicit w=12mV (legacy): FWHM 42mV" 로 두 지위 병기.
- **왜 정합(축2 교과서성)**: 단상=평형 예측(w=nRT/F 검증가능) / 두-상=현상학적 자유 피팅 폭 이라는 6-30 과제 V8-1① 이 tex L728-743 에 완전 복원. 코드가 "폭으로 항상 한 식 w=nRT/F 를 쓴다(상호작용 narrowing 항 없음)"(L725-726)와 코드 `_width` 가 일치.
- **렌즈**: G-follow(따라가짐) 1급. 이중지위 물리(broadening 이 두-상 폭을 정한다)가 코드 단일식과 모순 없이 연결됨.

### [PASS·정당] O2-C — ★그래프 bell 은 의도된 apparent-U/η 물리 반영(결함 아님)
- **위치**: 그림 `figs/anode_fit_v1_0_10_dqdv.png`(4패널, 코드 실출력) · `plot_dqdv.py` L84-94·L130-131 / Ch1 broadening 절 L1275-1307 (eq:ensavg L1282-1287) / SPEC 6-30 §2(B)(D)·radius `ORIGIN_VERDICT`·`31_bell_without_distribution.md`.
- **무엇이 확인됐나**: (1) 코드 기본 출력은 **종모양**이며 뾰족이/발산이 아니다 — 단일 LiC₆ FWHM 90.5mV·**면적=Q=0.500 보존**(내 실측). (2) tex 는 이 종을 apparent-U=U_j+η 앙상블 분포(U_j=const·입자무관, η 만 분포·ρ(U_app) forward-only·역산X·사이즈배제; L1275-1312)로 정초 — 6-30 §2(B) 결론과 일치. (3) 그림 자체가 subtitle "use_w_eff removed" + "area = Q = 0.499 (conserved)" 로 종+면적보존을 정상으로 프레이밍.
- **왜 결함 아님**: bell 자체(한 전이의 유한 폭 종)는 물리적으로 정당하고 면적 보존됨. 6-30 이 "뾰족이만 나온다=틀림, 기본은 정상 종" 이라 확정한 것과 실측 일치. **오적발 주의 대상(bell→구조결함)을 나는 결함으로 적발하지 않는다** — 이 부분은 O2 자기표시 오적발 방지 통과.
- **렌즈**: 이전 우수물리(v3/v4/v5 두-broadening·현상학적-w) 보존 → v10 apparent-U 재정초 → v1.0.10 tex 인계 = 온전.

### [HIGH·실결함, 강등 후보] O2-D — 기본 n=1(w=RT/F)이 4 staging 을 분리 못 해 단일 bell 로 병합(default 표시 문제)
- **위치**: `GRAPHITE_STAGING_LIT` L680-709('n':1.0 ×4) · `_width` L303-306 · `_n_factor` L294-300 · 그림 panel(1) / 대조 SPEC = `V1010_PROBLEM_REPORT.md` R1 [CRIT] L11-16 · `HANDOVER_v1.0.11.md` R1.
- **실측**: 4 전이 중심 U=210/140/120/85mV → 간격 **70/20/35mV**. 전이별 기본 FWHM=**90.6mV** > 모든 간격 → 평형 dQ/dV **local max 1개**(V≈0.100). 폭이 **Ω-완전무관**(Ω=0/6000/13000/50000 전부 FWHM 90.47mV) → 상분리(두-상 near-delta)를 열역학으로부터 생성 못 함.
- **무엇이 문제/왜**: (축2 교과서성·default 정직) 이건 **"인계 훼손"이 아니라** — v11_final 도 **완전히 동일**(local max 1개, FWHM 90.5mV; 두 파일 dqdv byte 동일). 즉 v10→v1.0.10 에서 **새로 생긴 결함이 아니라 계승된 default 표시 특성**이다. tex(L1255-1257)와 그림 범례가 "n=1 고정·'w' inert" 를 **명시**하므로 은닉은 아니다(축2 정직성 확보). 다만 release default 그래프가 4 전이 분리를 보여주지 못하는 것은 v1.0.10 자체 저자 검수(R1)가 이미 CRIT 로 지목했고 v1.0.11 개정 대상으로 이월됨.
- **★인계 무결성 관점 판정**: 이 항목은 **인계 결함(v10→v1.0.10 훼손)이 아니라 v1.0.11 로 이월된 기존 설계 한계**다. 2026-07-02 사용자 재framing(bell=의도 물리·진짜 쟁점은 default n=1 미분리)과 정확히 일치 — bell 물리는 정당(O2-C), n=1 미분리는 default 표시 개선 과제(본 항목). 두 층을 섞으면 "bell=구조결함" 오판(6-30 이후 R1 프레이밍)이 재발한다. **등급을 CRIT→HIGH(default 표시/피팅 초기값 문제)로 강등 권고.**
- **렌즈**: G-usable(사용성) — 초기값이 4 전이를 안 보여주면 피팅 착수가 불친절. 단 코드·tex 가 이를 명시하고 'n' 제거로 즉시 분리 가능하므로 물리 무결(G-derive)은 훼손 아님.

### [HIGH·실결함, 계승] O2-E — kinetic 꼬리 default OFF (seed_L_V 전부 0 → dqdv 꼬리 미진입)
- **위치**: 실측 `seed L_V = ['0.0000','0.0000','0.0000','0.0000']` (v1.0.10 self-test 출력) · `_resolve_lag_length` L325-369 · `dqdv` 문턱 분기 L484-497 · 생성자 `seed_I`=0.1 L252 / 대조 = `V1010_PROBLEM_REPORT.md` R2 [HIGH] L18-20.
- **무엇이 문제/왜**: default(dVdq_qa=0.30·seed_I=0.1)에서 L_V ≈ 1e-8 V ≪ 작업격자 문턱(min_lag_grid_steps·grid_step ≈ 4e-4) → dqdv 가 tail 분기(L487-497) 미진입, 평형 peak 분기(L486)로 떨어짐. 실측: 방전/충전 곡선이 default 서 거의 동일(peak@V 이동은 순수 ±I·Rn ohmic; 그림 panel(3)). 문건·graph_suite 가 강조한 **비대칭 finite-rate 꼬리 broadening 이 default 서 비활성**.
- **인계 관점**: v11_final 도 동일 로직(코드 byte 대응) — v1.0.10 신규 결함 아님, **계승**. 축1(논리) 무결(코드가 물리대로 L_V 작으면 평형종으로 환원), 축2(사용성) 저하 = default 그래프가 "C-rate 의존"을 ohmic-shift 로만 보여줌. v1.0.11 R2 이월 대상.
- **렌즈**: G-usable — 기능은 옳으나 default 노출이 오해 소지. (실결함이나 인계 훼손 아님.)

### [MED·문서 정합] O2-F — 회귀 스크립트 "면적=Q assert" 명칭이 실제 gate(golden bit-exact)와 불일치
- **위치**: `test_regression_graphite.py` `area_check` L43-50·L62/L75 · docstring L1 "byte 일치 검증" / 대조 = `V1010_PROBLEM_REPORT.md` R7 L35 · FP 표기 L43.
- **실측**: `AREA check: trapz(eq)=0.908219 Qsum=0.970000 ratio=0.936308`. ratio≠1.000 은 격자 [0.03,0.34] 가 LiC₆ 종(peak 85mV·FWHM 90mV)의 저전위 꼬리를 절단한 **grid-truncation artifact**(wide window 에선 면적=Q=1.000000, 6-30·problem-report 확정). 실제 gate 는 `np.array_equal` golden bit-exact(13/13)이지 면적 assert 가 아님 → 명칭↔gate 불일치.
- **왜(축2)**: 면적보존은 물리적으로 정상(내 단일전이 실측 0.5000)인데 스크립트 출력이 0.936 을 보여줘 오해 유발. **면적 자체는 결함 아님(FP)** — 명칭/출력 라벨만 정합 필요. v1.0.11 R7 이월.
- **렌즈**: G-usable(검증 신뢰) — 코드 무결, 라벨 오해.

### [MED·cross-version 손실] O2-G — v4 단상 narrowing 유도(w_eff=(RT/F)(1−Ω/2RT)) prose 가 tex 에서 소실
- **위치**: v1.0.10 Ch1 tex — `w_eff` prose **흔적 0**(grep: eq:weff·func_w_eff·use_w_eff "자취 0" L20·L32 만 언급) / SPEC = `old/_archive/Opus_v4` (v4 단상 예측) · `V1010_PROBLEM_REPORT.md` R5 [MED] L28-29.
- **무엇이 손실/왜**: v4 는 Ω<2RT 단상에서 `w_eff=(RT/F)(1−Ω/2RT)` 를 **검증가능한 평형 예측**(isoslope 매칭)으로 두었다. v1.0.10 은 코드 `use_w_eff` 제거(정당·O2-A)와 함께 **단상 폭 Ω-narrowing prose 예측까지** 소거하고 "단상 w=nRT/F flat" 으로 단언(tex L729-731). 코드 제거는 옳지만(Ω>2RT 서 음수폭·orthogonal), **단상(Ω<2RT) 한정 narrowing 예측은 물리적으로 유효한 별개 물건**이라 prose 각주로는 보존됐어야.
- **인계 관점**: 정당 컷 vs 손실의 경계 — 6-30 과제 V8-1② 는 "w_eff 절 정정/제거(단상 한정 경고와 함께)" 였는데, v1.0.10 은 제거 쪽만 취하고 단상 예측 복원을 누락. **부분 손실**(코드 미개입 각주 복원이 v1.0.11 R5 과제). 축1 관점 경미(단상은 흑연 staging 에 현재 없음).
- **렌즈**: cross-version 손실 — 정당 컷의 과잉(단상 예측까지 컷).

### [LOW·계약] O2-H — irreversible_heat q_irr 부호 무가드 (U_oc<V·I>0 서 음수 반환 가능)
- **위치**: `irreversible_heat` L590-598 (`I·(U_oc−V)` bare) / Ch2 eq:qrev q_irr≥0 · `V1010_PROBLEM_REPORT.md` R6 [MED] L31-32.
- **무엇/왜**: lumped `I·(U_oc−V)` 에 ≥0 가드 없음 — U_oc<V·I>0 조합서 음수(비발열) 반환. docstring 이 "caller 책임" 을 명시하나 Ch2 는 q_irr≥0 을 boxed(2법칙). 코드-문건 계약 경미 불일치. v11_final 엔 이 메서드 자체가 없음(v1.0.10 P4 확장분) → 신규 도입분의 가드 누락. v1.0.11 R6 이월.
- **렌즈**: G-derive(2법칙 정합) 경미 — 실사용 위험 낮음(정상 조건 U_oc≥V).

---

## 2. 무결 영역 (정독·실행 근거 남김 — 빈통과 방지)

- **전자엔트로피 seam byte-불변**: `_effective_dS_rxn`(흑연 base L533-542 = 항등 반환)·LCO override L657-673. 흑연 경로가 `tr['dS_rxn']` 을 그대로 반환(가산·부동소수 연산 없음) → LCO 편입이 흑연 곡선 byte 0-diff. 실측 회귀 골든 캡처 13 배열 정상(SHA 안정), 평형·dqdv v11 vs v1.0.10 **max_abs_diff=0.0** 로 흑연 무섭동 확인. `func_dSe_molar` L170-185 검산값 골 −45.7 J/mol/K(Ch1 −46 정합) — 코드 상수(π²/3·R·kB/e_V·gate) 물리 정확. **byte-identical 인계 = 6-30 이후 v10 유지 조건 충족.**
- **히스 분기(func_U_branch·func_dU_hys)**: self-test 실측 dU_hys=86.7mV·dis/chg split=+86.9mV(expect +86.7) 정합. Ω≤2RT→0(제곱근 NaN 영역 명시 분기, L137-140). v11_final 과 동일 식.
- **가드·facade·per-tr override**: guards 7/7 fire, curve()==dqdv (max_diff 0.0), per-tr z_cut override 격리(tr[0]만 변화) 실측 PASS — v11_final self-test 와 동형. 회귀 가드 계승 온전.
- **detailed balance 유도(ξ_eq)**: tex L745-765 (Eyring→BV→비→logit) 코드 `func_ksi_eq` L94-97 (logistic, s 부호·overflow-safe np.where 분기)와 일치. χ 상쇄(합-1)로 평형비가 χ-무관 = 코드 `_chi_and_dH_eff` 가 χ_d 를 꼬리에만 주입하고 평형종엔 안 넣는 구조와 정합.
- **충전 꼬리 방향**: 코드 L489-495 (충전 σ_d=−1 → 격자 반전 필터 후 되돌림) 실측 mirror 정상. (단 Ch1 본문 L1609-10 "V 큰 쪽" 문장은 캡션·코드와 반대 = problem-report R3, 이는 O1/문건 검수자 담당이라 본 O2 는 코드측 무결만 확인.)

---

## 3. 가장 약한 1곳 (single weakest spot)

**O2-D 와 O2-C 의 경계 = "bell 병합"의 이중 해석 위험**이 가장 약하다. bell 자체(한 전이 종·면적보존)는 의도된 apparent-U/η 물리(O2-C, PASS)지만, **4 전이가 한 bell 로 병합**되는 default(O2-D)는 저자 검수(R1)가 CRIT "구조 결함"으로, 2026-07-02 사용자는 "default n=1 표시 문제(bell 은 정상)"로 프레이밍 — **동일 현상의 상반된 등급**이다. 실측이 가르는 결론: (1) 병합은 v11_final 도 완전 동일 → **인계 훼손이 아니다**(신규 결함 X). (2) 폭이 Ω-완전무관이라 **두-상 near-delta 를 열역학으로 못 만드는 것은 사실**(R1 물리 근거 유효). (3) 그러나 코드·tex·그림이 "n=1·'w' inert·면적보존" 을 **명시·정직**하게 노출 → 은닉 결함 아님. **따라서 O2 판정: bell=정당 물리(O2-C), 병합=정직하게 노출된 default 초기값/표시 한계(O2-D, HIGH·v1.0.11 이월)이며 "인계 무결성" 축에서는 훼손 0** — "구조 결함(CRIT)" 라벨은 인계 검수 문맥에선 과대(오적발 위험 쪽). 이 경계를 흐리면 6-30 이후의 "bell→구조결함" 오판이 재발한다.

## 4. 버전 전환별 인계 판정 (코드/그래프 축)

| 전환 | 코드·그래프 인계 판정 | 근거(실측) |
|---|---|---|
| v8→v9 | **보존** (흑연 코드 무변, LCO seam 가산) | seam `_effective_dS_rxn` 항등 반환 → 흑연 byte 0-diff |
| v9→v10 | **개선** (broadening 복원·apparent-U 재정초·use_w_eff 제거 결정) | 6-30 진단 이행: w 이중지위·forward-only·사이즈배제 tex 복원 |
| **v10(v11_final)→v1.0.10** | **개선+보존**(신규 훼손 0) | use_w_eff live 제거로 default 거동 **byte 동일**(max_abs_diff 0.0)·회귀 골든 안정·전자엔트로피 byte 불변 |
| — 부분 손실 | O2-G(v4 단상 narrowing prose) 미복원 | tex w_eff prose 흔적 0 (정당 컷의 과잉) |
| — 계승 한계(신규 아님) | O2-D(4-staging 병합)·O2-E(꼬리 default OFF) | 두 파일 동일 → v1.0.11 이월 |

## 5. 5줄 요약

1. **초점**: 코드 인계(v11_final→v1.0.10) + 그래프 물리 정합 — 두 코드 직접 실행 실측 대조.
2. **인계 결함 수**: 코드/그래프 축에서 **신규 인계 훼손 = 0건**(v11 vs v1.0.10 평형·dqdv byte 동일). 실결함 5(O2-D HIGH·O2-E HIGH·O2-F MED·O2-G MED·O2-H LOW)은 전부 **계승 or 문서 정합**이지 v1.0.10 신규 훼손 아님. use_w_eff 제거(O2-A)·w 이중지위(O2-B)·bell 물리(O2-C)는 정당 PASS.
3. **최중대**: O2-D(4-staging 병합 = default n=1·폭 Ω-무관) — 단 **인계 훼손이 아니라 v10 계승 + 정직 노출된 default 표시/초기값 한계**로, "구조 결함 CRIT" 라벨은 인계 문맥에선 HIGH 로 강등 권고.
4. **두 축 유지 판정**: 축1(G-derive 물리 무결) = **유지**(logistic/detailed balance/seam/히스 코드가 tex 식과 실측 일치, FWHM 해석식 완전 정합). 축2(G-follow/G-usable 교과서성) = **대체로 유지**(n=1·'w' inert·면적보존 명시)이나 default 그래프가 4 전이 미분리·꼬리 OFF 로 사용성 저하(v1.0.11 이월).
5. **★오적발 자기표시**: 나는 **bell 종모양을 결함으로 적발하지 않았다**(O2-C 에서 의도 물리로 확인) — 6-30 이후의 "bell=구조결함" 오판을 재생산하지 않음. 또한 회귀 area ratio 0.936 을 **면적 결함으로 적발하지 않았다**(grid-truncation FP 로 실측 확인, O2-F). use_w_eff 제거도 회귀로 오적발하지 않았다(byte 0-diff 로 정당 확인, O2-A). 유일 잠재 과민 위험 = O2-D 등급(CRIT vs HIGH)이며, 실측(v11 동일·정직 노출)에 근거해 HIGH·이월로 판정.
