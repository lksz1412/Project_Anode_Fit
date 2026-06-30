# Anode_Fit v1.0.10 — P1 분석 경쟁 드래프트 **O1**

- **대상**: `Claude/docs/v1.0.10/Anode_Fit_v1.0.10.py` (695줄, 흑연 음극 dQ/dV forward 모델)
- **역할**: P1 작업 sub (분석 전용 — 코드 수정·commit·범위 밖 추가 X). 독립 작성.
- **정독 범위**: line 1 → line 703 전문 (head→tail). 모든 module 함수·class 메서드·데이터셋·`__main__` self-test 커버.
- **근거 표기**: 줄 번호 명시 = 확정 / "추정" = 물리 해석 추론 / "근거 미발견" = 줄로 못 짚음.

---

## 0. 전역 상수·타입 (line 61–70)

| 기호 | 값 | 줄 | 의미 |
|---|---|---|---|
| `R` | 8.314 | 65 | 기체상수 [J/mol/K] |
| `F` | 96485.0 | 66 | 패러데이 상수 [C/mol] |
| `kB` | 1.380649e-23 | 67 | 볼츠만 상수 [J/K] |
| `h` | 6.62607015e-34 | 68 | 플랑크 상수 [J·s] |
| `ScalarOrArray` | `Union[float, np.ndarray]` | 70 | 스칼라/배열 공용 타입 |

차원 점검: `kB`·`h`는 동역학 attempt frequency( `func_L_q`의 `T_attempt = (I/Q_cell)·h/kB` )에만 등장 → §2 적대 검산에서 차원 검증.

---

## 1. ★ 플로우차트 맵 (전 함수 + 물리식 + 줄 번호 + 데이터 흐름)

### 1.0 최상위 데이터 흐름

```
[입력]
  ├─ transitions: List[dict]  (GRAPHITE_STAGING_LIT, line 531–560)
  │     키: U|(dH_rxn,dS_rxn) · w|n · Q · Omega,gamma · dH_a,dS_a · dVdq_qa · h_eta · L_V
  ├─ 생성자 스칼라: x, Rn, Cbg, chi, chi_split, use_dH_eff, z_cut, A_cap_RT,
  │     grid_pad_lo/hi, n_work_min, min_lag_grid_steps, v_span_floor, seed_T/I/Q_cell
  │
  ▼  __init__ (221–259)  ── 가드(_finite*) → 스칼라 확정 → seed_L_V 계산
  │
  ├──▶ equilibrium(V_n, T)         (350–367)   |I|→0 기준선 (방향 불변)
  │       └ func_U_j → _n_factor → _width → func_ksi_eq → Q·ξ(1−ξ)/w
  │
  └──▶ dqdv(V_app, T, I_abs, Q_cell, s)  (370–480)   관측 곡선 (eq:hysmaster)
          ├ 분극 V_n = V_app − σ_d|I|R_n                         (408)
          ├ 작업격자 V_work·T_work 구성                           (410–425)
          ├ 전이 루프:
          │    ├ 평형중심 U_j(T) = func_U_j or tr['U']            (433–436)
          │    ├ 분기중심 center = U_j + func_U_branch(...)        (444–450)  ← 히스
          │    │     └ func_U_branch → func_dU_hys                (133–148)
          │    ├ ξ_eq = func_ksi_eq(center, σ_d)                  (455)
          │    ├ 지연길이 L_V = _resolve_lag_length(σ_d)          (459–460)
          │    │     └ _chi_and_dH_eff → _chi_d(chi_split) + func_dH_a_eff
          │    │       → func_L_q → ×|dVdq_qa|                    (303–347)
          │    └ peak_shape:
          │         · L_V<문턱 → 평형 peak ξ(1−ξ)/w               (462–464)
          │         · else    → (ξ_eq − _causal_lowpass)/L_V      (465–475)  ← 동역학 꼬리
          └ np.interp(V_n←V_work) → 출력                          (479–480)

  curve(...) facade (483–508)  ── 실험조건(방향문자열·C-rate) → dqdv 재사용 (새 물리 X)
          └ _direction_to_sigma (510–524)
```

### 1.1 모듈 레벨 순수 함수

#### `func_w(T, n=1.0)` — 전이 폭 (line 74–75)
- **식**: `w = n·R·T/F` [V]. eq:weff의 기본형(`w = nRT/F`).
- **유도 관점**: logistic 점유 ξ_eq의 특성 폭. n=1·298K → RT/F ≈ 25.69 mV (열전압). `n`은 다중도/현상학적 폭 핸들.
- **흐름**: `func_ksi_eq`(96)·`_width`(284)·`_n_factor` 역산(277)에서 호출. **확정**.

#### `func_U_j(T, dH_rxn, dS_rxn)` — 평형 중심 (line 78–79)
- **식**: `U_j(T) = (−ΔH_rxn + T·ΔS_rxn)/F` [V] (eq:vapp 평형중심). = −ΔG_rxn/F, Nernst/열역학 환산.
- **유도 관점**: 반응 Gibbs energy → OCV. ΔS_rxn>0 → U가 T에 선형 증가(엔트로피 항). 흑연 staging의 각 plateau 중심 전위.
- **흐름**: `equilibrium`(360)·`dqdv`(434, 배열 T 대응)·`__main__` U(298) 검증(583)에서 호출. **확정**.

#### `func_U_j_hys(T, U_j, Omega, gamma, s, last_eta, last_rest)` — 히스 분기중심 (원형) (line 82–91)
- **식**: `u = √(1−2RT/Ω)`; `ΔU_hys = (2/F)(Ω·u − 2RT·artanh u)`; 반환 `U_j + ½·s·partial_hys·γ·ΔU_hys`. `Ω≤2RT → ΔU=0`.
- **유도 관점**: 정규용액(regular solution) spinodal 상한에서의 히스테리시스 gap. 2RT는 spinodal 임계(Ω=2RT에서 상분리 발생 경계) — 그 아래는 단상이라 gap=0.
- **★死코드 확정**: 이 함수는 **클래스 어디서도 호출되지 않음** (grep line 82 정의 외 호출 0). line 35 "사용자 원형 보존" 라벨로 보존되나, 실제 분기중심 산출은 `func_U_branch`(148)가 담당. `last_eta`·`last_rest` 인자는 시그니처에만 있고 본체 미사용(**死인자**). 내부 `partial_hys = 1.0`(90)도 **死지역변수**(항상 ×1). → §2 audit 死코드 항목.
- **흐름**: 미호출. **확정(死)**.

#### `func_ksi_eq(T, V_n, U, n=1.0, s=1)` — 평형 점유 (line 94–97)
- **식**: `z = s·(V_n−U)/w`, `w=func_w(T,n)`; `ξ_eq = logistic(z)` (수치 안정 분기: z≥0이면 `1/(1+e^{−z})`, z<0이면 `e^z/(1+e^z)`).
- **유도 관점**: 단일 전이의 평형 SOC 점유율. logistic = 2-state Fermi 분포/평균장 등온선. s=σ_d가 부호를 줘 충·방전 방향 logistic 기울기 반전.
- **물리 타당성**: 수치 안정 분기(line 97)로 큰 |z|에서 overflow/underflow 회피 — ✓. ξ∈(0,1) 보장.
- **흐름**: `equilibrium`(365)·`dqdv`(455)에서 호출. **확정**.

#### `func_L_q(T, I, Q_cell, dH_a, dS_a, x, A)` — 지연 길이(전하축) (line 100–107)
- **식**: `if I≤0: return −inf`; `T_attempt=(I/Q_cell)·h/kB`; `ΔG_a=ΔH_a−T·ΔS_a`;
  `ln L_q = ln(T_attempt/T) − ln(1+e^{−A/RT}) + ΔG_a/RT − x·A/RT`; `L_q=e^{ln L_q}` (eq:lnLq).
- **유도 관점**: 인과 지연(과전위 완화의 메모리 길이)을 전하 단위로. Arrhenius 장벽(ΔG_a/RT) + 전이상태 affinity 보정(−xA/RT, x=χ_d=전이상태 분율 위치) + attempt frequency 비. `(1+e^{−A/RT})` 분모 = 정·역방향 합 정규화.
- **물리 타당성**: `I≤0 → −inf`는 의도적 sentinel(꼬리 없음 신호); 호출측 `_resolve_lag_length`(343)·`_causal_lowpass`(113)가 비유한 → 평형종으로 catch. **가드가 의도 흐름 차단 X** (§2 검증). `x` 인자에 방향별 χ_d 주입(342) → 충·방전 꼬리 길이 갈림.
- **흐름**: `_resolve_lag_length`(342)에서 호출. **확정**.

#### `_causal_lowpass(source_signal, grid_step, lag_length)` — 인과 저역통과 (line 110–128)
- **식**: `decay = e^{−grid_step/lag}`; 1차 IIR `y[i] = decay·y[i−1] + (1−decay)·x[i]` (eq:memory 인과 합성곱의 이산형). scipy `lfilter` 우선, 예외 시 순수 파이썬 루프 폴백(동일식).
- **유도 관점**: 지수기억 커널 `e^{−Δq/L}`와의 합성곱 = 단극 IIR. 인과(과거만 참조) → 진행 방향의 이력 반영.
- **물리 타당성**: `lag≤0 or 비유한 → source.copy()`(113–114) = 지연 0(꼬리 없음). 초기상태 `zi`로 transient 억제(118). DC 이득 = 1(∑계수=1) → **면적 보존**(§2). **확정**.

#### `func_dU_hys(T, Omega)` — 분기 gap (보완) (line 133–140)
- **식**: `func_U_j_hys` 내부와 동일. `Ω≤2RT → 0`; else `u=√(1−2RT/Ω)`, `(2/F)(Ω·u−2RT·artanh u)` (eq:hysdU).
- **유도 관점**: 히스테리시스 전압 gap의 spinodal 상한 닫힌형. Ω↑ → gap↑(상호작용 강할수록 히스 넓음).
- **흐름**: `func_U_branch`(148)·`__main__` 검증(644,659). **확정**. (func_U_j_hys 식 중복 — §2 死코드 관련.)

#### `func_U_branch(T, U_j, Omega, gamma, sigma_d, h_eta=1.0)` — 분기중심 (보완) (line 143–148)
- **식**: `U_j^d = U_j + ½·σ_d·h_η·γ·ΔU_hys` (eq:hyscenter), `ΔU_hys=func_dU_hys(T,Ω)`.
- **유도 관점**: 평형중심 U_j를 σ_d 방향으로 ±½γΔU_hys 이동 → 방전peak·충전peak 분리. `partial_hys` 하드코딩(1.0)을 `h_eta`(부분 cycle 인자)로 노출.
- **물리 타당성**: σ_d=±1로 대칭 분기 → dis/chg peak 간 거리 = γ·ΔU_hys (★`__main__` 645–646 self-test가 이를 실증: `d(dis−chg) ≈ +γ·dU_hys`).
- **흐름**: `dqdv`(447, `U_j=0`으로 호출해 shift만 추출 후 배열 center에 가산). **확정**.

#### `func_dH_a_eff(dH_a, Omega, chi_d)` — 유효 활성화엔탈피 (보완) (line 152–155)
- **식**: `ΔH_a^eff = ΔH_a − χ_d·Ω` (eq:dHeff).
- **유도 관점**: 깊은 꼬리에서 정규용액 상호작용 상수 몫이 장벽에 흡수. χ_d(방향별)로 충·방전 비대칭 장벽.
- **흐름**: `_chi_and_dH_eff`(299), `use_dH_eff=True`일 때만. **확정**.

#### `func_chi_d(chi, sigma_d)` — 방향별 전달계수 (보완·기본 규칙) (line 158–163)
- **식**: `σ_d≥0(방전) → χ_d=χ`; `σ_d<0(충전) → χ_d=1−χ` (eq:chisum 합-1).
- **유도 관점**: 꼬리 깊은 쪽 거울 대칭(방전 ξ→1 / 충전 ξ→0)으로 역방향 장벽 상수몫이 갈림. 생성자 `chi_split`로 교체 가능(line 161–162; ★`__main__` 628–635 custom rule self-test).
- **흐름**: `_chi_d`(290) → `_chi_and_dH_eff`(297). **확정**.

#### 가드 헬퍼 `_finite` / `_finite_pos` / `_finite_nonneg` (line 167–188)
- `_finite`: NaN/±inf → ValueError. `_finite_pos`: 추가 `>0` 검사(폭·용량·온도 분모용). `_finite_nonneg`: `≥0`(|I|·저항용). 전부 fail-fast 입력 가드. **확정**.

### 1.2 클래스 `GraphiteAnodeDischargeDQDV`

#### `__init__` (line 221–259)
- 스칼라 인자 유한·범위 가드(234–248) → `seed_L_V` 계산(256–259).
- `chi = x`(chi 미지정 시, 237). `chi_split` callable 검사(238–239).
- **데이터**: transitions 원본 참조 저장(232, 사본화 X — `__main__` 690은 호출측이 `dict(t)`로 복제). **확정**.

#### `_build_seed_L_V(T, I, Q_cell)` (line 262–269)
- 전이별 방전(σ_d=+1) 기준 L_V seed 리스트. **진단·초기값 전용**(line 255 주석 명시; `dqdv`는 실제 (T,I,Q_cell)로 재산출). `__main__` 577에서만 출력. **확정(진단)**.

#### `_n_factor(tr, T)` (line 272–278)
- `'n'` 직접 → 반환; 없으면 `'w'`에서 `n = w·F/(RT)` 역산(277); 둘 다 없으면 1.0.
- ★**키 우선순위 함정**: `'n'`이 있으면 `'w'`는 inert(line 9–10 헤더 경고). GRAPHITE_STAGING_LIT는 모든 전이에 `'n':1.0` 보유 → `'w':0.012~0.020`는 **무시됨**(死데이터). 폭 = RT/F 고정. → §2·§3.

#### `_width(tr, T)` (line 281–284)
- `func_w(T, _n_factor(tr,T))`. use_w_eff 경로는 v1.0.10에서 제거(면적보존 버그, line 7·283). **확정**.

#### `_chi_d(sigma_d)` (line 287–290)
- `self.chi_split(self.chi, sigma_d)`. **확정**.

#### `_chi_and_dH_eff(dH_a, Omega, sigma_d, use_dH_eff)` (line 293–300)
- `(χ_d, ΔH_a^eff)` 동시 산출. per-tr override(None=전역). `use_dH_eff=False` → ΔH_a^eff=ΔH_a. **확정**.

#### `_resolve_lag_length(transition, T, I, Q_cell, n_j, sigma_d=+1)` (line 303–347)
- 우선순위: ① `'L_V'` 직접 지정(피팅·테스트 우회, 313–318) → ② `I≤0 or 'dH_a' 부재 → 0`(319–320, 평형종) → ③ 동역학 산출.
- 동역학: `A = min(z_cut·|n|·RT, A_cap_RT·RT)`(331) → `_chi_and_dH_eff`(338) → `func_L_q`(342) → 비유한이면 0(343–344) → `×|dVdq_qa|`(347).
- **★원본 버그 정정 주석**(322–327): 원본 `min(s·F·(OCV−U), 4RT)`에서 s를 min 밖으로 빼 충전 시 음수 상한 버그를 정정. s(방향)는 크기에 안 들어가고 χ_d/ΔH_eff가 받음. **확정**.

#### `equilibrium(V_n, T=298.15)` (line 350–367)
- **식**: `dQ/dV = C_bg + Σ_j Q_j·ξ_eq(1−ξ_eq)/w` (eq:eqpeak, 방향 불변, |I|→0).
- U_j: `dH_rxn`&`dS_rxn` 있으면 func_U_j, 없으면 `tr['U']`(359–362). **히스·동역학 없음** (순수 평형). **확정**.

#### `dqdv(V_app, T, I_abs, Q_cell, s=+1)` (line 370–480)
- 핵심 forward. 분극(408) → 작업격자(415, 저전위쪽 pad로 꼬리 수용) → 비등온 T(V) interp(418–422) → 전이 루프(431–477) → `np.interp` 복원(479).
- 평형/지연 분기: `lag_len_V < min_lag_grid_steps·grid_step` → 평형 peak(462–464); else 인과 꼬리(465–475). 충전(σ_d<0)은 격자 뒤집어 필터 후 되돌림(473) = 방향 반전 인과기억.
- **식**: `peak_shape = (ξ_eq − r̄)/L_V` (eq:closed, 평형−지연의 미분 이산형, 475). **확정**.

#### `curve(...)` facade (line 483–508)
- 실험조건(방향문자열·C-rate·Q_cell·T) → `|I| = c_rate·Q_cell`(505, I_abs 미지정 시) → `dqdv` 재사용. **새 물리 X**(line 490; ★`__main__` 613–615가 curve==dqdv 일치 실증). **확정**.

#### `_direction_to_sigma(direction)` staticmethod (line 510–524)
- 문자열/정수 → σ_d. 미지원 문자열 → ValueError(521). **확정**.

---

## 2. ★ 조건 audit (명령 + 증거)

### 2.A "BDD 음극 dQ/dV 물리수식 기반 피팅 함수" 충족도

| 요구 | 충족 | 증거(줄) |
|---|---|---|
| 흑연 음극 staging dQ/dV forward | ✓ | `GRAPHITE_STAGING_LIT` 4-stage(531–560), `dqdv`(370) |
| 물리수식 기반(현상 fit 아님) | ✓ | func_U_j 열역학(78)·func_L_q Arrhenius(100)·정규용액 히스(133) |
| 충·방전 방향(σ_d) | ✓ | 분극(408)·분기중심(447)·꼬리반전(470–473)·χ_d(287) |
| 온도 의존(스칼라·T(V)) | ✓ | `T_work` interp(418–422), func_U_j 배열 T(434) |
| C-rate 의존 | ✓ | `curve` `\|I\|=c_rate·Q_cell`(505), func_L_q ∝ I(104) |
| 피팅 핸들 전부 노출 | 대체로 ✓ | per-tr dict + 생성자 override (line 196 "내부 하드코딩 없음") |
| **면적 보존** | ✓ | _causal_lowpass DC이득=1(∑=1), eq:closed 미분형(475); 헤더 line 11 plot_dqdv.py 실증 주장 |

### 2.B ★흑연 음극 전용 확정 (LCO·발열·전자엔트로피 부재)

**명령**: `grep "q_rev|dS_e|LCO|LiCoO|cathode|entropic|electron entropy"` → **No matches**(전 파일).
- **q_rev(가역 발열)**: 부재. 열 생성 항 없음 — 등온/T(V) 입력만, 자기발열 모델 X. **확정**.
- **dS_e(전자 엔트로피)**: 부재. 엔트로피는 `dS_rxn`(반응, func_U_j)·`dS_a`(활성화, func_L_q)뿐 — 전자 엔트로피 항 없음. **확정**.
- **LCO/양극**: 부재. `GraphiteAnodeDischargeDQDV` 클래스명·`GRAPHITE_STAGING_LIT` stage 4→3→2L→2→1(흑연 intercalation staging 전용). **확정 — 흑연 음극 전용 모델**.

### 2.C 결함 (None/0 가드 의도차단 · 死코드 · 시그널/호출체인)

| # | 분류 | 증거(줄) | 판정 |
|---|---|---|---|
| C1 | **死코드(함수)** | `func_U_j_hys`(82–91) 클래스 미호출(grep 호출 0). 보존 라벨(35)로 남으나 기능 vestigial; 식은 func_dU_hys(133)가 중복 보유 | **결함(死)** — 면적·정확성 무영향이나 유지보수 리스크. 원형보존 정책상 의도적. |
| C2 | **死인자/死지역** | func_U_j_hys `last_eta`·`last_rest` 시그니처만(본체 미사용); `partial_hys=1.0`(90) 死지역(항상 ×1) | **결함(死)** — 미호출이라 무해. |
| C3 | **死데이터** | GRAPHITE_STAGING_LIT 각 전이 `'w'`(533,540,547,554)가 `'n':1.0` 존재로 inert(_n_factor 274 우선순위) | **결함(혼란성)** — 헤더 line 9–10에 경고 명시. 폭 핸들=n. |
| C4 | None/0 가드 의도차단 점검 | `func_L_q I≤0→−inf`(102) → `_resolve_lag_length`이 I≤0을 **먼저** 0으로 차단(319) → func_L_q엔 I>0만 도달; 비유한 L_q도 catch(343) | **무결함** — 가드가 정상 흐름 차단 안 함. 평형종(꼬리 0)으로 정확히 분기. |
| C5 | None 가드 점검 | `'dH_a' is None → 0`(319), `tr.get('Omega',0.0)`(335,441) 등 dict.get 기본값 | **무결함** — 키 부재 시 합리적 기본(꼬리/히스 off). |
| C6 | 시그널/호출체인 정합 | `dqdv`→`_resolve_lag_length`(sigma_d 전달, 460)→`_chi_and_dH_eff`(338)→`func_L_q(x=chi_d)`(342). 방향 σ_d가 χ_d/ΔH_eff/꼬리반전까지 일관 전파 | **무결함** — 방향 신호 끊김 없음. |
| C7 | 면적보존(_causal_lowpass) | 계수 `[1−decay]/[1,−decay]` ∑=1 → DC이득 1; `lag≤0→copy`(113) | **무결함** — ξ_eq 적분 보존, peak=(ξ−r̄)/L_V 형태로 면적 중립. |
| C8 | transitions 사본화 X | `__init__` line 232 원본 참조 저장 — 호출측이 같은 dict 재사용 시 공유. `__main__` 690은 `dict(t)`로 회피 | **경미** — 입력 mutate 안 하므로 실해 없음(추정). |

### 2.D ★물리 타당성 적대 검산 (부호·차원·극한)

| 검산 | 결과 | 증거 |
|---|---|---|
| **차원 `func_w`** | [n]·[J/mol/K]·[K]/[C/mol] = J/C = V ✓ | 75 |
| **차원 `func_U_j`** | [J/mol]/[C/mol]=V ✓; TΔS도 J/mol ✓ | 79 |
| **차원 `func_L_q`** | `T_attempt=(I/Q_cell)·h/kB`: [A]/[C]·[J·s]/[J/K] = [1/s]·[s·K]=[K] ✓ → `ln(T_attempt/T)` 무차원 ✓. ΔG/RT 무차원 ✓ | 104–106 |
| **차원 `func_dU_hys`** | (1/F)·(Ω) = [J/mol]/[C/mol]=V ✓; artanh 무차원 ✓ | 140 |
| **부호 ΔS_rxn>0 → ∂U/∂T>0** | func_U_j `+T·dS_rxn/F` ✓ (열역학 정합) | 79 |
| **부호 분기 σ_d** | 방전 +½γΔU / 충전 −½γΔU → dis peak가 chg보다 고전위(흑연 lithiation 히스 정성 일치, 추정) | 148, `__main__` 645 |
| **극한 Ω≤2RT → gap 0** | spinodal 미달 단상 → 히스 0 ✓ (물리 정확: 상분리 임계) | 137, `__main__` 659 검증 |
| **극한 \|I\|→0 → dis=chg** | γ=0 전이서 일치(가역 평형) | `__main__` 663–665 검증 |
| **극한 γ=0 → 분기 0** | center=U_j(449) ✓ | 444 |
| **artanh 정의역** | `u=√(1−2RT/Ω)∈[0,1)` (Ω>2RT 보장) → artanh 유한 ✓ | 88,139 |
| **음수 dQ/dV** | 꼬리에서 `(ξ−r̄)/L_V`가 국소 음수 가능 — `__main__` 653 `neg` 플래그로 모니터(물리적으로 꼬리 undershoot 허용; 평형종은 ξ(1−ξ)≥0) | 475, 654–655 |

**적대 결론**: 부호·차원·극한 모두 정합. 유일 주의 = 꼬리 undershoot 음수 영역(C-rate 高·L_V 大에서 (ξ−r̄)<0)은 인과 메모리 모델의 자연 결과(死코드/버그 아님). spinodal·면적보존·방향전파 모두 물리 일관. **확정**.

---

## 3. ★ 피팅 파라미터 인벤토리

곡선 지배영역 = peak **위치**(중심전위) / **폭** / **높이**(면적·peak amplitude) / **꼬리**(저율 deviation) / **히스 분기**(dis-chg split).

| 파라미터 | 키/위치 | 역할 (식) | 지배영역 | 초기값(LIT) | 자유/고정 권고 | 민감도 직관 |
|---|---|---|---|---|---|---|
| **n_j** | `'n'` (534…) / `func_w` | 폭 다중도, w=nRT/F | **폭** | 1.0 (전 전이) | **자유** (폭 핸들) | w∝n 선형; n↑ → peak 넓고 낮아짐(면적 일정). 高감도. |
| **U_j** | `'U'` 또는 (`dH_rxn`,`dS_rxn`) | 평형중심 (func_U_j) | **peak 위치** | 0.210/0.140/0.120/0.085 V | **자유**(또는 열역학 고정) | 직접 peak 전위. dH_rxn 1kJ ≈ 10mV shift. 最高감도. |
| ΔH_rxn | `'dH_rxn'`(534…) | U_j=(−ΔH+TΔS)/F | **peak 위치** | −11700~−13000 J/mol | 자유 or 고정 | ∂U/∂(ΔH)=−1/F → −10.4 mV/kJ. 高감도. |
| ΔS_rxn | `'dS_rxn'`(534…) | U_j의 T기울기 | peak 위치 **T의존** | +29/0/−5/−16 J/mol/K | 자유(또는 0) | ∂U/∂T=ΔS/F; T범위 좁으면 低감도. |
| **Ω_j** | `'Omega'`(533…) | 정규용액 상호작용 (히스 gap·ΔH_eff) | **히스 분기 + 꼬리** | 6000~13000 J/mol | 자유 | Ω>2RT(=4955@298K)부터 gap 발생; 임계 근방 高비선형 감도. ΔH_eff에도 −χ_dΩ. |
| **γ (gamma)** | `'gamma'` | 분기 축소 인자 (func_U_branch) | **히스 분기** | 미지정(0) | 자유 (히스 데이터 있을 때) | dis-chg split = γ·ΔU_hys 선형. γ=0이면 히스 off. |
| **ΔH_a** | `'dH_a'`(536…) | 활성화 장벽 (func_L_q Arrhenius) | **꼬리** (L_V) | 40000~48000 J/mol | 자유 | L_q∝e^{ΔH_a/RT}: 지수 감도 → 꼬리 길이 매우 민감(1kJ≈40% @298K). 最高 꼬리감도. |
| ΔS_a | `'dS_a'`(536…) | ΔG_a=ΔH_a−TΔS_a | 꼬리 T의존 | 0.0 (전 전이) | 고정(0) 권고 | 초기 0; T스윕 fit시만 풀기. |
| **χ (chi)** | 생성자 `chi`/`x` | 전이상태 분율 → χ_d (func_chi_d) | **꼬리 비대칭**(dis vs chg L_V) | x=0.5 → chi=0.5 | 자유(0~1) | dis χ_d=χ / chg=1−χ. χ=0.5면 대칭; ≠0.5면 충·방전 꼬리 길이 갈림. 中감도. |
| **L_V** | `'L_V'` (선택) | 지연 길이 직접지정(동역학 우회) | **꼬리** | 미지정 | 고정(테스트) or 자유(현상 fit) | 주면 ΔH_a/dVdq_qa 등 동역학 전부 우회. 직접 꼬리 폭. |
| z_cut | 생성자/`'z_cut'` | 컷 affinity A=z_cut·nRT (꼬리 컷점) | 꼬리(약) | 4.357(=ξ_eq 5%) | **고정** 권고 | A→func_L_q의 −xA/RT·정규화. 물리적 컷 정의값, 보통 고정. 低감도. |
| A_cap_RT | 생성자/`'A_cap_RT'` | A 상한 = A_cap·RT | 꼬리(가드) | 4.0 | **고정** | 상한 클램프; 거의 비활성. 極低감도. |
| **dVdq_qa** | `'dVdq_qa'`(536…) | L_V=\|dV/dq\|·L_q 환산 | **꼬리 높이/폭** | 0.30 V (전 전이) | 자유 | L_V 선형 스케일. 꼬리 V-폭 직접. 中감도. |
| Q_j | `'Q'`(533…) | 전이 용량 가중 | **peak 높이/면적** | 0.10/0.12/0.25/0.50 | 자유 | dQ/dV ∝ Q 선형. 면적 = Q. 高감도(정규화). |
| h_eta | `'h_eta'` | 부분 cycle 인자 (func_U_branch) | 히스 분기(스케일) | 1.0 | 고정(1.0) 권고 | 분기 shift ×h_eta. full cycle=1. |
| Rn | 생성자 `Rn` | 분극 V_n=V−σ_d\|I\|Rn | **전체 V-shift**(IR) | 0.0(LIT)/0.01(__main__) | 자유 | 곡선 통째 ±\|I\|Rn 평행이동. C-rate 의존. 中감도. |
| Cbg | 생성자 `Cbg` | 배경 dQ/dV | baseline 오프셋 | 0.0/0.05 | 자유(상수/V함수) | 전체 수직 오프셋. |

**고정 권고 요약**: z_cut·A_cap_RT·dS_a·h_eta = 물리/구조 상수(고정). 자유 핵심 = U_j(또는 dH_rxn)·n·Q·dH_a·dVdq_qa·Ω·γ·χ·Rn. 꼬리 최고감도 = **ΔH_a(지수)**, 위치 최고감도 = **U_j/dH_rxn**.

> ★ **死데이터 경고(C3)**: GRAPHITE_STAGING_LIT의 `'w'`(0.012~0.020)는 `'n':1.0` 존재로 **피팅에 안 들어감**. 폭을 'w'로 풀려면 'n' 키를 제거해야 함(_n_factor line 274 우선순위).

---

## 4. 불확실·근거 미발견

- 헤더 line 11 "plot_dqdv.py 실증"·line 38 "graphite_ica_ch1_Opus_v6.tex" = 외부 파일 참조 — 본 파일 내 코드로는 검증 불가(**근거 미발견**, 외부 문건 P1 범위 밖). eq:label은 코드 주석 inline으로만 확인.
- C8 transitions 공유 참조의 실해 = mutate 코드 없어 무해로 **추정**(전수 추적은 했으나 호출 패턴 무한대 아님).
- 분기 부호(dis>chg 고전위)의 흑연 lithiation 히스 정성 부합은 **추정**(self-test는 부호 일관만 실증).

---

## 5. 정독·커버리지 자기검수

- **Read coverage**: line 1–703 전문 1회 정독 + grep 3회 교차(q_rev류 부재 / partial_hys·h_eta / func 호출처). 누락 함수 0.
- **함수 커버**: module 11개(func_w·U_j·U_j_hys·ksi_eq·L_q·_causal_lowpass·dU_hys·U_branch·dH_a_eff·chi_d·가드3) + 메서드 11개(__init__·_build_seed_L_V·_n_factor·_width·_chi_d·_chi_and_dH_eff·_resolve_lag_length·equilibrium·dqdv·curve·_direction_to_sigma) **전부 §1 맵에 줄 근거와 함께 등재**.
- 적대 검산(§2.D) 11항·인벤토리(§3) 17파라미터 지배영역 확정.
