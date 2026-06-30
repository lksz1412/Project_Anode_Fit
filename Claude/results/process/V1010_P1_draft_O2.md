# Anode_Fit v1.0.10 — P1 분석 경쟁 드래프트 O2

> 대상: `Claude/docs/v1.0.10/Anode_Fit_v1.0.10.py` (695줄, 흑연 음극 dQ/dV 물리 구현)
> 작성: P1 분석 sub (작업 sub, 분석 전용 — 코드 수정·commit 없음). 전 함수·메서드 커버, 줄 근거 명시.
> 검증 방식: 전문 정독 + 부호/차원/극한 적대 검산. 불확실은 '추정'/'근거 미발견' 라벨.

---

## 0. 모듈 골격 한눈에 (커버리지 체크)

| # | 심볼 | 줄 | 역할 | 비고 |
|---|------|-----|------|------|
| 1 | `func_w` | 74-75 | 전이 폭 w=nRT/F | 원형 보존 |
| 2 | `func_U_j` | 78-79 | 평형 중심 U_j=(−ΔH+TΔS)/F | 원형 보존 |
| 3 | `func_U_j_hys` | 82-91 | 히스 분기 중심(spinodal gap) | 원형 보존, **死코드(미호출)** |
| 4 | `func_ksi_eq` | 94-97 | 평형 점유 ξ_eq=logistic[s(V−U)/w] | 원형 보존, overflow-safe |
| 5 | `func_L_q` | 100-107 | 지연 길이 L_q(Arrhenius·attempt) | 원형 보존 |
| 6 | `_causal_lowpass` | 110-128 | 인과 1차 저역통과(지수기억) | 원형 보존 |
| 7 | `func_dU_hys` | 133-140 | spinodal gap ΔU_hys(보완 헬퍼) | func_U_j_hys 내부와 동일식 |
| 8 | `func_U_branch` | 143-148 | 분기 중심 U^d=U+½σ_d h_η γ ΔU_hys | h_eta 인자화 |
| 9 | `func_dH_a_eff` | 152-155 | ΔH_a^eff=ΔH_a−χ_d·Ω | 유효장벽 |
| 10 | `func_chi_d` | 158-163 | 방향별 χ_d(방전 χ / 충전 1−χ) | 주입 교체 기본값 |
| 11 | `_finite`/`_finite_pos`/`_finite_nonneg` | 167-188 | 입력 가드 헬퍼 | fail-fast |
| 12 | `__init__` | 221-259 | 생성자·가드·seed_L_V 채움 | |
| 13 | `_build_seed_L_V` | 262-269 | 전이별 L_V seed(진단/초기값) | |
| 14 | `_n_factor` | 272-278 | 폭 다중도 n('n'→'w'역산→1) | |
| 15 | `_width` | 281-284 | 폭 w=func_w(T,n) | use_w_eff 제거됨 |
| 16 | `_chi_d` | 287-290 | χ_d=chi_split(χ,σ_d) | |
| 17 | `_chi_and_dH_eff` | 293-300 | (χ_d, ΔH_a^eff) 응집 | per-tr override |
| 18 | `_resolve_lag_length` | 303-347 | 전이 1개 L_V 산출 | 핵심 동역학 |
| 19 | `equilibrium` | 350-367 | |I|→0 평형 dQ/dV | |
| 20 | `dqdv` | 370-480 | 관측 dQ/dV(분극·분기·꼬리) | 메인 합산 |
| 21 | `curve` | 483-508 | 실험조건 facade | dqdv 재사용 |
| 22 | `_direction_to_sigma` | 510-524 | 방향 문자열/정수→σ_d | |
| 23 | `GRAPHITE_STAGING_LIT` | 531-560 | 4-전이 초기값 데이터셋 | 원형 보존 |
| 24 | `__main__` self-test | 567-703 | 알파 작동 검증 | |

전 24개 심볼 커버 완료.

---

## 1. ★ 플로우차트 맵 (입력 → equilibrium / dqdv → curve)

### 1.1 입력 단 (생성자 + 데이터셋)

```
GRAPHITE_STAGING_LIT (531-560)              생성자 스칼라 인자 (221-231)
  4개 전이 dict:                              x, Rn, Cbg, chi, chi_split,
   U/dH_rxn,dS_rxn  → 평형 중심                use_dH_eff, z_cut, A_cap_RT,
   w/n              → 폭                       grid_pad_lo/hi, n_work_min,
   Q                → 전이 가중                 min_lag_grid_steps, v_span_floor,
   Omega, gamma     → 히스                      seed_T/I/Q_cell
   dH_a, dS_a       → 동역학 꼬리
   dVdq_qa          → L_q→L_V 환산
   (옵션) L_V, h_eta, z_cut/A_cap_RT/use_dH_eff override
        │
        ▼
   __init__ (221) ─ 가드(234-248) ─→ _build_seed_L_V (256, 262)
        │                                  │ 방전 기준 σ_d=+1, seed 대표조건
        │                                  ▼ 진단/초기값(곡선에 직접 안 들어감)
        │                              seed_L_V[ ] 리스트
        ▼
   self.transitions, self.* 파라미터 확정
```

물리식 연결:
- **평형 중심** `func_U_j` (78): U_j(T) = (−ΔH_rxn + T·ΔS_rxn)/F. 'U' 키 있으면 직접 사용(equilibrium 361, dqdv 436).
- **폭** `func_w` (75): w = n·RT/F. `_n_factor` (272): n 키 직접 → w 키서 n=w·F/(RT) 역산 → 없으면 n=1. `_width` (284) 가 호출.

### 1.2 equilibrium (|I|→0 기준선, 350-367)

```
V_n (스칼라/배열), T
   │ T 가드 _finite_pos (352)
   ▼
baseline = Cbg(V) or Cbg 상수 (354-356)
   │
   for tr in transitions (358):
   │   U_j = func_U_j(T,dH_rxn,dS_rxn) [359-360]  또는  tr['U'] [362]
   │   n_j = _n_factor (363) ;  w = _width (364)
   │   ksi_eq = func_ksi_eq(T, V, U_j, n_j)  [365]   ← s 기본 +1
   │   dqdv += tr['Q'] · ξ_eq(1−ξ_eq)/w      [366]  ← eq:eqpeak
   ▼
dqdv 반환 (방향 불변; 꼬리 없음 = 순수 평형 peak)
```

**dQ/dV 개형 기여 (평형 peak)**: 각 전이는 중심 U_j 에서 폭 w 의 **종 모양(bell) 피크**를 만든다. 정점값 = Q/(4w) (ξ=½에서 ξ(1−ξ)=¼). 폭이 좁을수록(w↓, 즉 n↓·T↓) 피크가 높고 날카로워진다. 4개 전이가 서로 다른 U(0.085~0.210 V)에 놓여 흑연 특유의 다중 staging 피크열을 만든다.

### 1.3 dqdv (관측 곡선, 370-480) — 핵심 신호 체인

```
입력: V_app, T(scalar/array), I_abs, Q_cell, s
   │ σ_d = +1 if s≥0 else −1 (388)
   │ 가드: I_abs≥0(391), Q_cell>0(392), V 유한·비어있지않음(394-400), T 유한·>0(404)
   ▼
[분극]  V_n = V_app − σ_d·|I|·R_n   (408)            ← eq:hysmaster
   │       └ 방전(+1): V_n 하향 / 충전(−1): V_n 상향 (IR 시프트)
   ▼
[작업격자] v_span(411) → V_work = linspace(v_lo−pad·span, v_hi+pad·span, n_work) (415)
   │       grid_step (416);  n_work = max(n_work_min, 2·V_n.size) (412)
   │       T_work = interp(T(V)) (422) 또는 등온 상수 (424); T_rep=mean (426)
   ▼
dqdv_work = Cbg(V_work) baseline (427-429)
   │
   for tr (431):
   │  U_j = func_U_j(T_work,...) [434]  또는 tr['U'] [436]
   │  [분기중심] gamma≠0 & Omega>0 →
   │       hys_shift = func_U_branch(T_rep, U_j=0, Ω, γ, σ_d, h_η) (447)  ← eq:hyscenter
   │       center = U_j + hys_shift (448)         else center = U_j (450)
   │  n_j = _n_factor(T_work) (452) ; w = _width(T_work) (453)
   │  [평형점유] ksi_eq = func_ksi_eq(T_work, V_work, center, n_j, σ_d) (455)
   │  [지연길이] n_rep (458) → lag_len_V = _resolve_lag_length(tr,T_rep,|I|,Q_cell,n_rep,σ_d) (459)
   │
   │  if lag_len_V < min_lag_grid_steps·grid_step  (462):
   │       peak_shape = ξ_eq(1−ξ_eq)/w               (464)  ← 평형 종(꼬리 무시)
   │  else:
   │       방전: occ_lagged = _causal_lowpass(ξ, step, L_V)       (471)
   │       충전: occ_lagged = lowpass(ξ[::-1])[::-1]              (473) ← 방향 반전
   │       peak_shape = (ξ_eq − occ_lagged)/L_V                   (475)  ← eq:closed
   │
   │  dqdv_work += tr['Q']·peak_shape (477)
   ▼
dqdv_out = interp(V_n, V_work, dqdv_work) (479)  → 원래 격자로 되돌림
반환 (스칼라면 [0])
```

각 식의 **dQ/dV 개형 기여**:
- **분극 V_n (408)**: 곡선 전체를 σ_d·|I|·R_n 만큼 V축 평행이동. 방·충 피크를 IR 만큼 벌린다(히스와 별개의 외인성 split). |I|→0 또는 R_n=0 이면 무영향.
- **분기 중심 (447-448)**: 평형 종의 **중심을 σ_d 방향으로 ±½γΔU_hys 이동**. 방전 피크는 +, 충전 피크는 − 로 갈려 내재적 히스 split 생성. peak shape 자체(높이·폭)는 불변, 위치만 이동. γ=0 → 0.
- **평형 점유 ξ_eq (455)**: 0→1 로 가는 logistic. 그 미분형 ξ(1−ξ)/w 가 피크.
- **지연 꼬리 (471-475)**: 평형 ξ 와 지연된 occ_lagged 의 차를 L_V 로 나눠 **피크를 진행방향 뒤쪽으로 끌고 비대칭화**. 고율(|I|↑) → L_V↑ → 피크 낮아지고 꼬리가 길어짐(분극에 의한 피크 broadening·tailing). 방·충은 진행방향이 반대라 꼬리도 반대쪽으로 (471 vs 473).

### 1.4 curve (facade, 483-508)

```
V_app, direction(str/int), c_rate, Q_cell, T, I_abs?
   │ σ_d = _direction_to_sigma(direction) (501, 510)
   │ Q_cell 가드 (502)
   │ I_use = c_rate·Q_cell (505)  또는  I_abs override (507)
   ▼
return self.dqdv(V_app, T, I_use, Q_cell, s=σ_d) (508)   ← 새 물리 없음, 환산만
```

### 1.5 _resolve_lag_length (동역학 꼬리 길이, 303-347) — 상세

```
transition, T, I, Q_cell, n_j, σ_d
   │ 'L_V' override 있으면 → 유한·≥0 가드 후 그대로 (313-318)  [동역학 우회]
   │ I≤0 또는 'dH_a' 없음 → 0 (319-320)  [평형 종, 꼬리 없음]
   ▼
[컷 affinity]  A = min(z_cut·n_safe·R·T, A_cap·R·T)   (328-331)
   │            ← ξ_eq 가 정점 ~5% 로 떨어지는 컷점(z_cut=4.357), 상한 A_cap·RT
   │ dH_a(333), dS_a(334), Omega(335) 가드
   │ (χ_d, ΔH_a^eff) = _chi_and_dH_eff(dH_a, Ω, σ_d, override) (338)  ← eq:chisum·eq:dHeff
   ▼
[L_q]  L_q = func_L_q(T, I, Q_cell, ΔH_a^eff, dS_a, x=χ_d, A) (342)
   │     ← T_attempt=(I/Q_cell)·h/kB ; ln L_q = ln(T_att/T) − ln(1+e^{−A/RT})
   │       + ΔG_a^eff/RT − χ_d·A/RT
   │ 비유한 → 0 (343-344)
   ▼
[L_V]  return |dVdq_qa| · L_q (347)   ← eq:tail: L_V=|dV/dq|_qa·L_q
```

**개형 기여**: L_V 가 dqdv 의 꼬리 비대칭·broadening 을 결정하는 단일 스칼라(전이당 1회 산출, 격자 전체 공용). χ_d·ΔH_a^eff 의 σ_d 의존 때문에 방·충 꼬리 길이가 다르게 나온다.

---

## 2. ★ 조건 audit (음극 dQ/dV 물리수식 충족도·결함·흑연 전용성)

### 2.1 물리수식 피팅 함수 충족도 — 부호/차원/극한 적대 검산

| 항목 | 식·줄 | 검산 | 판정 |
|------|-------|------|------|
| **차원: w** | nRT/F (75) | [J/mol/K·K]/[C/mol]=J/C=V. n 무차원 | ✅ |
| **차원: U_j** | (−ΔH+TΔS)/F (79) | [J/mol]/[C/mol]=V | ✅ |
| **차원: ξ_eq** | logistic[s(V−U)/w] (96-97) | (V−V)/V=무차원 → ξ∈(0,1) | ✅ |
| **차원: peak** | Q·ξ(1−ξ)/w (366) | [C]/[V]=C/V (dQ/dV) | ✅ |
| **차원: L_q** | 무차원(아래) | T_attempt=(I/Q)·h/kB, [A/C·J·s/(J/K)]=[1/s·s·K]=K → ln(K/K) 무차원 ✓; ΔG/RT 무차원 ✓ | ✅ L_q 무차원 |
| **차원: L_V** | |dVdq_qa|·L_q (347) | [V]·무차원=V. peak=(ξ−occ)/L_V → 무차원/V=1/V, ×Q[C] → C/V ✓ | ✅ |
| **부호: 분극** | V_n=V−σ_d|I|R_n (408) | 방전 σ_d=+1: 음극 전위 하강(과전압) 일관. 충전 −1: 상승 | ✅ 물리 일관 |
| **부호: 분기** | +½σ_d γ ΔU_hys (148/447) | 방전 중심 ↑(+), 충전 중심 ↓(−). 흑연 히스: 방전(리튬화) OCV가 충전보다 낮음이 통상 — **부호 관례는 문건 eq:hyscenter 정의 따름(추정: 코드는 σ_d·ΔU_hys 부호를 문건에 위임)** | ⚠ 부호 관례 문건 의존 |
| **극한: Ω≤2RT** | dU=0 (85/137) | spinodal 미형성 영역, √(음수) 회피 명시 분기 | ✅ |
| **극한: |I|→0** | L_q→0(T_attempt→0, ln→−∞, exp→0) (104,107) | 꼬리 소멸 → 평형 peak 로 환원. self-test 663-665 max diff~0 확인 | ✅ |
| **극한: I≤0** | func_L_q return −inf (102-103) | exp(−inf)=0 등가. _resolve(319)서도 0. 이중 가드 | ✅ |
| **극한: γ=0** | hys_shift 안 탐(444 else) | center=U_j, 방·충 동일 → 히스 없음 | ✅ |

**핵심 적대 검산 — `_causal_lowpass` 면적 보존**:
1차 IIR `(1−a)/(1−a·z⁻¹)`, a=decay_per_step (115-121). DC gain = (1−a)/(1−a) = 1. 즉 저역통과는 **합(적분)을 보존**한다. peak_shape=(ξ−occ_lagged)/L_V 를 V로 적분하면 ∫(ξ−occ)dV/L_V. occ 는 ξ 를 L_V 만큼 지연시킨 것이므로 적분차 ≈ L_V·(경계 ξ 차)/L_V → **전이당 총면적 Q 보존**(ξ: 0→1 단조이면 ∫(ξ−occ)dV = L_V·Δξ_boundary). 초기상태 zi=a·source[0] (118) 가 경계 누출을 막아 면적 보존. **판정: 면적보존 OK** (v1.0.10 변경 핵심 = use_w_eff 제거로 폭·분모 정합 회복, 줄 7·283).

### 2.2 결함 audit (가드·死코드·시그널체인·면적보존)

| 결함 | 위치 | 등급 | 내용 |
|------|------|------|------|
| **死코드: `func_U_j_hys`** | 82-91 | LOW | 원형 보존 함수지만 클래스 어디서도 미호출(분기 중심은 func_U_branch 사용, 447). self-test도 호출 안 함. 보존 목적상 의도적 잔존 — 기능 결함 아님 | 
| **死코드: seed_L_V** | 256, 262-269, 577 | NOTE | 곡선 산출(dqdv)에 안 들어감 — 진단·초기값 전용(주석 254-255 명시). dqdv 가 실제 (T,I,Q_cell)로 재산출. **의도적**, 결함 아님 |
| **분기중심 T_rep 사용** | 447 | LOW | 분기 shift 를 배열 T_work 가 아닌 스칼라 T_rep 로 1회 계산 후 배열 U_j 에 가산. 비등온 T(V)에서 ΔU_hys 의 T의존성이 평균으로 근사됨 — 의도적 단순화(주석 445 "전이당 상수"). 결함이라기보다 근사 |
| **L_V dqdv 미사용 분기** | 462-464 | NOTE | lag_len_V < min_lag_grid_steps·grid_step 이면 평형 종으로 폴백. **과거 v04 peak_ids>0 류 死가드 잔존 없음** 확인 — 이 분기는 정상(저율 꼬리 무시) |
| **Cbg 유한성 미검사** | 236, 354, 427 | NOTE | Cbg callable 출력 유한성은 사용자 책임으로 명시 위임(주석 236). 의도적 |
| **n_safe=abs(n_j)** | 328 | LOW | A 계산서 n 절대값 사용 — 음수 n 입력 시 크기만 취함. 폭 w 는 음수 n 이면 음수 폭(func_w 75)이 되나 별도 가드 없음 — **n<0 입력 방어 없음(추정: 실사용 n>0 전제)** |

**시그널체인 추적 (수정 후 호출체인 정합)**:
- `s` (방향) → σ_d (388) → ① V_n 분극(408) ② 분기중심 σ_d(447) ③ ξ_eq logistic 부호(455) ④ 꼬리 방향반전(470-473) ⑤ χ_d/ΔH_eff(459→338). **5개 경로 모두 σ_d 일관 전파** — 끊김·가드 차단 없음. 
- func_ksi_eq 의 5번째 인자 s=σ_d (455): logistic 부호. 충전(s=−1)이면 z 부호 반전 → ξ 가 V감소 방향으로 0→1. **방향 일관**.
- `func_L_q` 의 x 인자 자리에 χ_d 주입 (342): 원형 func_L_q(x) 의 x 를 전이상태분율이 아닌 방향별 전달계수로 재해석 — 주석 341 명시. **의도적, 시그널 정합**.

### 2.3 흑연 전용성 확정 (LCO·발열·전자엔트로피 부재)

| 점검 | 결과 | 근거 |
|------|------|------|
| **흑연 staging 전용** | ✅ | GRAPHITE_STAGING_LIT(531) = stage 4→3, 3→2L, 2L→2, 2→1 (흑연 LiC_x 상전이). U≈0.085~0.210 V = 흑연 음극 전위대 |
| **LCO(양극) 부재** | ✅ 부재 확정 | LiCoO₂·층상양극·3.x~4.x V 관련 항 전무. 클래스명 GraphiteAnode |
| **발열(thermal)항 부재** | ✅ 부재 확정 | 자기발열·열생성·엔트로피 발열(Q=TΔS 셀 발열)·열폭주 항 없음. T 는 입력 파라미터(등온/T(V) 프로파일)일 뿐 — 발열 ODE 없음 |
| **전자 엔트로피 부재** | ✅ 부재 확정 | ΔS_rxn(534 등)은 반응 엔트로피(열역학 U 보정)일 뿐, 전자 비열·전자 엔트로피(c_e·T, Sommerfeld)항 없음. dS_a 는 활성화 엔트로피 |
| **dQ/dV 단일 물리** | ✅ | 전 코드가 dQ/dV(미분용량) 곡선 합성에만 집중. 적분용량·전압프로파일·SOC-OCV 역변환 없음 |

**판정: 순수 흑연 음극 dQ/dV 평형+동역학 모델**. 양극/발열/전자엔트로피 결합은 의도적으로 배제(Ch1 범위 정합).

### 2.4 미충족·미검증 (4-tier)

- **근거 미발견**: 분기중심 σ_d 부호의 물리 관례(방전 ↑ vs ↓)가 코드만으로는 확정 불가 — 문건 eq:hyscenter 정의에 위임됨. 문건 대조 필요.
- **추정**: GRAPHITE_STAGING_LIT 값들은 "초기값·신뢰값 아님"(주석 528) — 피팅 override 전제. 물리적 타당성은 라벨된 출처(DFT/Thinius 등) 추정 수준.
- **미검증**: n<0 입력 시 음수 폭 거동(별도 가드 없음). 실사용서 n>0 전제로 미테스트.

---

## 3. ★ 피팅 파라미터 인벤토리

| 파라미터 | 식·줄 | 역할 | 곡선 지배영역 | 초기값(GRAPHITE_STAGING_LIT) | 자유/고정 | 민감도(추정) |
|----------|-------|------|--------------|------------------------------|-----------|------|
| **n_j** (폭 다중도) | func_w 75, _n_factor 272 | 폭 w=nRT/F | **피크 폭·높이** 전역. n↓→폭↓→피크 뾰족·고. 정점 Q/(4w)∝1/n | n=1.0 (전 전이) | 자유(또는 w로 역산) | **고**. 폭·높이 직접 결정 |
| **U_j** (평형 중심) | func_U_j 79, 360/434 | 피크 V축 위치 | **피크 위치**. ΔH↑→U↓(흑연 0.085~0.21V) | 'U' 0.085/0.120/0.140/0.210; 또는 ΔH_rxn,ΔS_rxn | 자유(U 직접 또는 열역학환산) | **고**. 위치 = staging 식별 |
| **Q_j** (전이 가중) | tr['Q'] 366/477 | 피크 면적(전하) | **피크 면적**. 곡선 높이 스케일. 면적보존으로 ∫=Q | 0.10/0.12/0.25/0.50 | 자유 | **고**. 상대 면적비 |
| **Ω_j** (상호작용) | Omega, func_dU_hys 140 | 히스 gap·ΔH_a^eff | **히스 split 크기**(Ω>2RT서 ΔU_hys 발생) + 유효장벽 −χ_d·Ω | 6000/8000/10000/13000 J/mol | 자유 | **중**(히스 켤 때 고). Ω≤2RT면 gap 死 |
| **dH_a** (활성화 엔탈피) | dH_a, func_L_q 106 | 꼬리 길이 L_q∝e^{ΔG_a/RT} | **고율 꼬리·broadening**. ΔH_a↑→L_q↑→꼬리↑·피크↓ | 48000/46000/44000/40000 J/mol(저SOC→만충 감소) | 자유 | **고(고율)·저(저율)**. |I|→0서 무영향 |
| **χ** (전달계수) | x/chi 210/237, _chi_d 290 | χ_d 방향분배 → ΔH_a^eff·L_q | **방·충 꼬리 비대칭**. 방전 χ / 충전 1−χ | x=0.5(default), chi=None→x | 자유 | **중**. 방·충 꼬리 차 결정. χ=0.5면 대칭 |
| **L_V** (지연 길이) | 'L_V' override 313, 347 | 꼬리 비대칭·broadening | **직접 지정 시 동역학 우회**. 피크 tailing 폭 | (데이터셋엔 없음; override 전용) | 고정(주면)/자유(동역학산출) | **고**. 꼬리 형상 직접 |
| **z_cut** (컷 affinity) | z_cut 226, 329-331 | 컷점 A=z_cut·n·RT | **L_q 절대 스케일**(A 통해). ξ_eq 5%컷=4.357 | 4.357(=ξ_eq 5%) | 자유(per-tr override 가능) | **중**. A=min(z_cut·nRT, A_cap·RT)서 상한 걸리면 둔감 |
| **dVdq_qa** (OCV 기울기) | dVdq_qa 347 | L_V=|dVdq_qa|·L_q | **꼬리 V스케일**. L_q(무차원)→L_V(V) 환산 | 0.30 V (전 전이) | 자유 | **고**. L_V 선형 비례 |

**보조 파라미터 (인벤토리 외 — 명시 요청 8종 아님, 참고)**:
- γ_j (gamma): 분기 축소 인자, 히스 shift 크기 ½σ_d·γ·ΔU_hys (447). 데이터셋엔 없음(=0 → 히스 off). self-test서 γ=1.0 주입(639).
- dS_rxn (29/0/−5/−16 J/mol/K): U_j 온도의존. dS_a (0): 활성화 엔트로피 → ΔG_a (105).
- h_eta (1.0 기본): 부분 cycle 인자, 분기 shift 스케일(148).
- Rn (0.01 self-test): 외인성 IR 분극, V_n 시프트(408).
- Cbg (0.05 self-test): 배경 dQ/dV 오프셋(427).
- A_cap_RT (4.0): A 상한 캡(331).
- z_cut=4.357 검산: ξ=1/(1+e^{−4.357})≈0.9873, ξ(1−ξ)/0.25≈5.0% — **"ξ_eq 5%" 라벨(218) 정확** ✅.

**지배영역 요약**: 위치=U_j, 폭/높이=n_j(+T), 면적=Q_j, 히스 split=Ω·γ, 고율 꼬리=dH_a·L_V·dVdq_qa·z_cut, 방·충 비대칭=χ.

---

## 4. 종합 판정

- **물리 충족도**: 차원·부호·극한 검산 전 항목 통과(2.1). 면적보존(IIR DC gain=1)·시그널체인 σ_d 5경로 일관 확인.
- **결함**: CRITICAL/HIGH **없음**. 死코드 2건(func_U_j_hys·seed_L_V)은 의도적 보존/진단용. n<0 미방어가 유일한 미검증 코너(LOW).
- **흑연 전용**: 확정 — LCO·발열·전자엔트로피 완전 부재, dQ/dV 단일 책임.
- **v1.0.10 핵심**: use_w_eff 제거(폭·분모 정합 → 면적보존 회복, 줄 7·283). 회귀 가드(per-tr override isolation self-test 686-699) 존재.
