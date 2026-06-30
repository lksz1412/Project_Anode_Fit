# P1 Result — 코드 검증·플로우차트 앵커 (vN-11)

> **산출물**: Anode_Fit v1.0.10 P1(코드 검증·플로우차트 앵커) 최종 result. 본 문서 = ① 11항목 result 래퍼(머리) + ② §1 맵·§2 audit·§3 인벤토리 본체(adversarial 확정 정정 4건 반영본).
> **단계 체인**: 9 드래프트 → 검토1(체리픽 recipe) → vN-10 통합본 → adversarial 검수 → **vN-11(본 문서, finalizer)**.
> **정정 출처**: master(adversarial 검수) 확정 4건만 반영. 본문 식·줄은 vN-10 유지(추측 정정 X).

## Summary

v1.0.10 코드(`Anode_Fit_v1.0.10.py`, 703줄, 흑연 음극 dQ/dV forward 모델)에 대해 **맵·audit·인벤토리 3산출**을 1통합본으로 조립·검증했다. **맵**(§1)은 24심볼 전수 줄근거 + 데이터흐름 ASCII + equilibrium↔dqdv 7축 비교로 전 함수·물리식·호출체인을 앵커링했고, **audit**(§2)은 closed-form 12식 전부를 코드 줄에 매핑(2-A)·부호/차원/극한 11행 적대검산(2-B)·피팅 실용 결함 4건(2-C)·死코드/면적보존/조건부 inert(2-D)·흑연 전용성(2-E, LCO·발열·전자엔트로피 부재)·초벌 피팅 순서(2-F)로 명령+증거 기반 결함을 확정했으며, **인벤토리**(§3)는 주8/보조10 2계층 파라미터를 지배영역·등급·줄근거로 확정했다. adversarial 검수 결과 물리식 12개·24심볼 coverage·정정 1/3·보완 1~4 substance가 코드와 충돌 0으로 PASS, 인용 정밀도 4건(z_cut docstring 줄 L218→L217, γ=0 극한 보강, seed 인용 외관모순, docstring 판정 의존성)만 finalizer에서 보정했다.

## Step Range

1. 입력 정독 — vN-10 통합본(`V1010_P1_map_v10.md`) 전문 + 코드 필요 줄 확인.
2. adversarial 확정 정정 4건의 코드 근거 재검증(L217 z_cut docstring / L218 A_cap_RT / L444 게이트 `gamma != 0.0 and Omega > 0.0`).
3. 정정 4건을 본문 해당 위치에 반영(본문 식·줄 불변, 인용·서술만 보정).
4. 11항목 result 래퍼로 통합본을 래핑해 최종 산출.

## Inputs

- **코드 (ground truth)**: `Claude/docs/v1.0.10/Anode_Fit_v1.0.10.py` — 703줄. 수정 X(분석/검증 전용).
- **9 드래프트**: O1/O2/O3(객관·골격), C1/C2/C3(피팅 실용·결함·순서), S1/S2/S3(축·호출자·식). 검토1이 골격 recipe 확정.
- **검토1 확정**: §1=O1+S2+O3, §2=O3+O2+C1/C2/C3, §3=O3+C3+S 채택. 흑연 전용·DC gain=1·死코드·'w' inert 확정.
- **adversarial 검수**: vN-10 통합본 대상 적대 검수 → 정정 4건 확정 + 그 외 전부 PASS.

## Read Coverage

- **코드**: `Anode_Fit_v1.0.10.py` 전문(703줄) 정독 — 전역상수(L61-70)·모듈순수함수(L74-188)·클래스 메서드(L221-524)·데이터셋(L531-560)·self-test(L567-703). 24심볼 전수 줄근거 cover.
- **finalizer 직접 재독**: L210-234(생성자 docstring·시그니처, z_cut=L217 / A_cap_RT=L218 확인), L438-453(히스 게이트 L444 `gamma != 0.0 and Omega > 0.0` → else center=U_j 확인).
- **9 드래프트** 전수 + **검토1**(체리픽 recipe) + **adversarial 검수**(정정 4건) 정독.

## Execution Evidence

- **독립 면적적분 = 1.000000** — ∫Q·ξ(1−ξ)/w dV(전이별 0.10/0.12/0.25/0.50 일치), 꼬리 ∫=0.99986(큰 L_V 격자 경계 손실). use_w_eff 제거(L7) 면적보존 목적과 수치 일치. [adversarial 확정]
- **ΔU_hys(Ω=12000, 298K) = 86.69 mV** — self-test L644 "≈86.7 mV" 일치(u=0.766). Ω≤2RT 분기 → gap=0(L85·L137). [adversarial 확정]
- **self-test 7/7 PASS** — guards 7/7 + curve==dqdv 일치 + 히스 split(d(dis−chg)≈+γ·dU_hys) + override isolation(z_cut=2.0 격리). [adversarial 확정]
- **z_cut 검산** — ξ_eq(z=4.357)=98.73%(1−ξ=1.27%), 정규화 미분 ξ(1−ξ)/0.25=5.00% → docstring "ξ_eq 5%"는 정규화 미분의 5%를 가리킴(docstring 부정확, L217). A 컷: z_cut·RT=4.357RT > A_cap·RT=4.0RT → n=1·z_cut≥4.0서 4.0RT capped. [adversarial 확정]

## Validation

- **맵 coverage** — 24심볼 전수(§1.0) + 12 closed-form 식(§2-A) 0누락 매핑. **PASS** (명령: 심볼표 vs 코드 grep / 증거: §1.0 줄근거 24행).
- **audit** — 부호·차원·극한 11행(§2-B)·피팅 결함 4건(§2-C)·死코드/면적/inert(§2-D) 전부 **명령(줄 인용)+증거(독립 계산/grep)+범위(영향·권고)** 충족. 흑연 전용성 `grep "LCO|q_rev|dS_e|cathode|발열"`→No matches(§2-E). **PASS**.
- **인벤토리** — 주8/보조10 파라미터 지배영역·줄근거·등급 확정(§3-1·3-2). 지배영역 = 위치=U_j/폭=n_j/면적=Q_j/히스=Ω·γ/꼬리=dH_a·dVdq_qa·L_V/비대칭=χ/IR=Rn/baseline=Cbg **확정 PASS**.

## Gate

**PASS** — 정정 4건 코드 근거 재검증 완료(L217·L218·L444 직접 확인), 본문 식·줄 불변, 11항목 result 완비. adversarial 그 외 전부 PASS 승계. P2 진입 차단 사유 없음.

## Confirmed Non-Changes

- **코드 불변**: `Anode_Fit_v1.0.10.py` 1바이트도 수정 안 함(분석/검증 전용). 死코드(`func_U_j_hys` L82-91)·docstring 부정확(L217)·면적 self-test 부재(L567-703)는 **보고만** — 코드 개정은 P4 후보.
- **본문 식·줄 불변**: vN-10 물리식 12개·24심볼 coverage·정정 1/3·보완 1~4 substance는 adversarial 확정 PASS → 그대로 유지. finalizer는 인용 줄(L218→L217)·극한 서술·부기 1줄만 보정.
- **§3-2 z_cut 행 L226·L329 인용 불변**: 생성자 기본값(L226)·binding 사용(L329) 줄로 정확 — M1 정정 대상 아님(z_cut **docstring** 인용만 L217로 보정).

## Open Issues

- **P2 전달**: LCO·발열 이론 갈고닦기(Ch1 범위 = 흑연 음극 staging 평형+동역학 꼬리+히스 전용, 양극·열·전자구조는 의도적 배제 — 후속 챕터 develop 대상).
- **P4 코드개정서 처리 후보**: ① 死코드 `func_U_j_hys`(L82-91, last_eta·last_rest·partial_hys 死) ② z_cut docstring 부정확(L217 "ξ_eq 5%" → 정규화 미분 5%로 정정 필요) ③ 면적=Q self-test assert 부재(L567-703, 면적 회귀 가드 결함). 모두 P1에선 보고만, 코드 개정은 P4.
- **피팅 실용 가드**(§2-C F1~F4): n>0·χ∈[0,1] bound·dVdq_qa>0 schema·Cbg 유한성 — fitting wrapper 권고(코드 범위 밖).

## Next

**P2 챕터1 진입** — 본 P1 result(코드 검증·플로우차트 앵커)를 ground-truth 앵커로 삼아 Ch1 이론 본문 develop.

---

---

# Anode_Fit v1.0.10 — P1 통합본 (vN-11, 정정 반영 본체)

> **대상 (ground truth)**: `Claude/docs/v1.0.10/Anode_Fit_v1.0.10.py` (703줄, 흑연 음극 dQ/dV forward 모델)
> **산출**: ① §1 플로우차트 맵 ② §2 조건 audit ③ §3 피팅 파라미터 인벤토리
> **조립 방식**: master(검토1) 확정 recipe대로 9 드래프트의 장점만 체리픽. 모든 식·결함은 **코드 줄 번호 근거**. 코드·드래프트 수정 없음(분석 전용).
> **표기**: [확정]=코드·식 직접 줄근거 / [추정]=설계 의도 추론 / [근거 미발견]=코드로 못 짚음.
>
> **§1 골격 = O1** (24심볼 전수 줄근거 + 데이터흐름 ASCII + 차원검산) + S2 호출자 보강 + O3 §1-G 7축 비교표
> **§2 골격 = O3** (§0 사전 수치검산) + O2 차원검산 11행 + C1/C2 피팅 실용 결함 + C3 초벌 피팅 4단계
> **§3 골격 = O3** (주8/보조10 2계층) + C3 3등급·피팅 순서 + S계열 축 다이어그램

---

## §0. 독립 수치 검산 (작성 전 사전 확인 — 추측 배제용) [O3 §0]

본격 맵 작성 전, "추측 배제"를 위해 코드 주장 식들을 독립 계산으로 대조했다(O3·C1·C2·C3 수치 검산 교차).

| 항목 | 코드/식 주장 (줄) | 독립 계산 | 판정 |
|---|---|---|---|
| **z_cut=4.357 의미** | docstring(L217) "ξ_eq 5%" | ξ_eq(z=4.357)=**98.73%** (1−ξ=1.27%); **정규화 미분** ξ(1−ξ)/0.25=**5.00%** | **★ docstring 부정확** — "5%"는 점유율이 아니라 **정규화 미분 ξ(1−ξ)/0.25의 5%**(→ §2 C1, ★정정 2) |
| **ΔU_hys(Ω=12000, 298K)** | self-test L644 "≈86.7 mV" | u=0.766, ΔU_hys=**86.69 mV** | [확정] 일치 |
| **ΔU_hys(Ω≤2RT)** | L85·L137 분기 0 | Ω=2RT(=4957.6) → u=0, gap=**0** | [확정] 일치 |
| **A 컷(n=1, 기본 데이터셋)** | A=min(z_cut·n·RT, A_cap·RT) (L331) | z_cut·RT=**4.357RT** > A_cap·RT=**4.0RT** → **4.0RT로 capped** | [확정]·**조건부**: n=1 & z_cut≥4.0서만 z_cut inert (→ §2 D4, ★정정 3) |
| **L_q(dH_a=44k, I=0.1, χ=0.5)** | func_L_q (L100-107) | =1.094e-07 → L_V=×0.30=**3.28e-08** | [확정] 유한·양수 |
| **ΔH_a^eff 부호 (χ=0.5)** | dH_a−χ_d·Ω (L155) | χ=0.5 → 방·충 χ_d 동일(0.5) → ΔH_eff 충방전 비대칭 **0** | [확정] (→ §2 D5) |
| **면적보존 (평형)** | ∫Q·ξ(1−ξ)/w dV = Q | 수치적분 = **1.000000** (전이별 0.10/0.12/0.25/0.50 일치, ΣQ=0.97 ↔ 적분 0.96999…) | [확정] area-conserving |
| **면적보존 (꼬리)** | ∫(ξ_eq−ξ_lag)/L_V dV ≈ Q | L_V=0.02 → 0.4997; L_V=0.10 → 0.95~0.97 (격자 경계 손실 증가) | [확정] DC 보존, finite-grid 절단 (→ §2 C2-면적) |

→ §0의 핵심: **z_cut docstring 1건이 부정확**, 나머지는 코드 식 정합. 면적보존은 1.0.10의 use_w_eff 제거(L7) 목적과 수치 일치.

---

## §1. ★ 플로우차트 맵 (전 함수 + 물리식 + 줄 번호 + 데이터 흐름) [골격 = O1]

### 1.0 모듈 골격 한눈에 — 24심볼 전수 커버리지 [O1·O2 교차]

| # | 심볼 | 줄 | 역할 | 비고 |
|---|------|-----|------|------|
| 1 | `func_w` | 74-75 | 전이 폭 w=nRT/F | 원형 보존 |
| 2 | `func_U_j` | 78-79 | 평형 중심 U_j=(−ΔH+TΔS)/F | 원형 보존 |
| 3 | `func_U_j_hys` | 82-91 | 히스 분기중심(spinodal gap) | 원형 보존, **死코드(미호출)** |
| 4 | `func_ksi_eq` | 94-97 | 평형 점유 ξ_eq=logistic[s(V−U)/w] | 원형 보존, overflow-safe |
| 5 | `func_L_q` | 100-107 | 지연 길이 L_q(Arrhenius·attempt) | 원형 보존, I≤0→−inf |
| 6 | `_causal_lowpass` | 110-128 | 인과 1차 저역통과(지수기억) | 원형 보존, DC gain=1 |
| 7 | `func_dU_hys` | 133-140 | spinodal gap ΔU_hys(보완 헬퍼) | func_U_j_hys 내부와 동일식 |
| 8 | `func_U_branch` | 143-148 | 분기중심 U^d=U+½σ_d·h_η·γ·ΔU_hys | h_eta 인자화 (死코드 대체) |
| 9 | `func_dH_a_eff` | 152-155 | ΔH_a^eff=ΔH_a−χ_d·Ω | 유효장벽 |
| 10 | `func_chi_d` | 158-163 | 방향별 χ_d(방전 χ / 충전 1−χ) | 주입 교체 기본값 |
| 11 | `_finite`/`_finite_pos`/`_finite_nonneg` | 167-188 | 입력 가드 헬퍼 | fail-fast |
| 12 | `__init__` | 221-259 | 생성자·가드·seed_L_V 채움 | |
| 13 | `_build_seed_L_V` | 262-269 | 전이별 L_V seed(진단/초기값) | dqdv 미사용 |
| 14 | `_n_factor` | 272-278 | 폭 다중도 n('n'→'w'역산→1) | 'n' 우선 |
| 15 | `_width` | 281-284 | 폭 w=func_w(T,n) | use_w_eff 제거됨 |
| 16 | `_chi_d` | 287-290 | χ_d=chi_split(χ,σ_d) | |
| 17 | `_chi_and_dH_eff` | 293-300 | (χ_d, ΔH_a^eff) 응집 | per-tr override |
| 18 | `_resolve_lag_length` | 303-347 | 전이 1개 L_V 산출 | 핵심 동역학 |
| 19 | `equilibrium` | 350-367 | |I|→0 평형 dQ/dV | 방향 불변 |
| 20 | `dqdv` | 370-480 | 관측 dQ/dV(분극·분기·꼬리) | 메인 합산 |
| 21 | `curve` | 483-508 | 실험조건 facade | dqdv 재사용 |
| 22 | `_direction_to_sigma` | 510-524 | 방향 문자열/정수→σ_d | staticmethod |
| 23 | `GRAPHITE_STAGING_LIT` | 531-560 | 4-전이 초기값 데이터셋 | 원형 보존 |
| 24 | `__main__` self-test | 567-703 | 알파 작동 검증 | **면적=Q assert 부재**(→ §2 보완4) |

**전역 상수** (L61-70): `R`=8.314 J/mol/K, `F`=96485.0 C/mol, `kB`=1.380649e-23 J/K, `h`=6.62607015e-34 J·s. kB·h는 `func_L_q`의 attempt frequency `T_attempt=(I/Q_cell)·h/kB`에만 등장.

### 1.1 최상위 데이터 흐름 [O1 ASCII]

```
[입력]
  ├─ transitions: List[dict]  (GRAPHITE_STAGING_LIT, L531-560)
  │     키: U|(dH_rxn,dS_rxn) · w|n · Q · Omega,gamma · dH_a,dS_a · dVdq_qa · h_eta · L_V
  ├─ 생성자 스칼라: x, Rn, Cbg, chi, chi_split, use_dH_eff, z_cut, A_cap_RT,
  │     grid_pad_lo/hi, n_work_min, min_lag_grid_steps, v_span_floor, seed_T/I/Q_cell
  │
  ▼  __init__ (221-259)  ── 가드(_finite*) → 스칼라 확정 → seed_L_V 계산
  │
  ├──▶ equilibrium(V_n, T)         (350-367)   |I|→0 기준선 (방향 불변, T 스칼라 전용)
  │       └ func_U_j → _n_factor → _width → func_ksi_eq → Q·ξ(1−ξ)/w
  │
  └──▶ dqdv(V_app, T, I_abs, Q_cell, s)  (370-480)   관측 곡선 (eq:hysmaster)
          ├ 분극 V_n = V_app − σ_d|I|R_n                         (408)
          ├ 작업격자 V_work·T_work 구성 (n_work=max(n_work_min, V_n.size·2)) (410-425)
          ├ 전이 루프:
          │    ├ 평형중심 U_j(T) = func_U_j or tr['U']            (433-436)
          │    ├ 분기중심 center = U_j + func_U_branch(...)        (444-450)  ← 히스
          │    │     └ func_U_branch → func_dU_hys                (133-148)
          │    ├ ξ_eq = func_ksi_eq(center, σ_d)                  (455)
          │    ├ 지연길이 L_V = _resolve_lag_length(σ_d)          (459-460)
          │    │     └ _chi_and_dH_eff → _chi_d(chi_split) + func_dH_a_eff
          │    │       → func_L_q → ×|dVdq_qa|                    (303-347)
          │    └ peak_shape:
          │         · L_V<문턱 → 평형 peak ξ(1−ξ)/w               (462-464)
          │         · else    → (ξ_eq − _causal_lowpass)/L_V      (465-475)  ← 동역학 꼬리
          └ np.interp(V_n←V_work) → 출력                          (479-480)

  curve(...) facade (483-508)  ── 실험조건(방향문자열·C-rate) → dqdv 재사용 (새 물리 X)
          └ _direction_to_sigma (510-524)
```

### 1.2 모듈 레벨 순수 함수 (줄근거 + 식 + 호출자) [O1 본문 + S2 호출자 보강]

#### `func_w(T, n=1.0)` — 전이 폭 (L74-75)
- **식**: `w = n·R·T/F` [V]. eq:weff의 기본형.
- **유도**: logistic 점유 ξ_eq의 특성 폭. n=1·298K → RT/F ≈ 25.69 mV (열전압). n=다중도/현상학적 폭 핸들.
- **호출자** [S2]: `_width`(L284), `func_ksi_eq` 내부(L96), `_n_factor` 역산 분기(L277). **[확정]**

#### `func_U_j(T, dH_rxn, dS_rxn)` — 평형 중심 (L78-79)
- **식**: `U_j(T) = (−ΔH_rxn + T·ΔS_rxn)/F` [V] = −ΔG_rxn/F (깁스-헬름홀츠/Nernst 환산).
- **유도**: 반응 Gibbs energy → OCV. ΔS_rxn>0 → U가 T에 선형 증가(엔트로피 항). 흑연 staging 각 plateau 중심 전위.
- **호출자** [S2]: `equilibrium`(L360), `dqdv`(L434, 배열 T 대응), `__main__` U(298) 검증(L583). **[확정]**

#### `func_U_j_hys(T, U_j, Omega, gamma, s=1, last_eta=1.0, last_rest=600)` — 히스 분기중심 (원형) (L82-91)
- **식**: `u=√(1−2RT/Ω)`; `ΔU_hys=(2/F)(Ω·u − 2RT·artanh u)`; 반환 `U_j + ½·s·partial_hys·γ·ΔU_hys`. `Ω≤2RT → ΔU=0`.
- **유도**: 정규용액 spinodal 상한 히스테리시스 gap. 2RT=spinodal 임계, 그 아래는 단상이라 gap=0.
- **★死코드 [확정]**: 클래스·self-test 어디서도 **미호출**(grep 호출 0). 실제 분기중심 산출은 `func_U_branch`(L148)가 담당(dqdv L447). L36 "사용자 원형 보존(1바이트도 변조 X)" 라벨로 동결.
- **★보완 1 [9 드래프트 전부 놓침]**: 死코드 `func_U_j_hys`(L83)의 인자 = `s:int=1`(방향), 대체 함수 `func_U_branch`(L144)의 인자 = `sigma_d`. 死코드라 **호출 흐름엔 무해**하나, 외부에서 `func_U_j_hys`를 직접 호출하면 인자명·기본값 차이(`s=1` 디폴트 vs `sigma_d` 무디폴트)로 **부호 관례 혼동 가능**. 또한 `last_eta`·`last_rest`는 시그니처에만 있고 본체 미사용(死인자), 내부 `partial_hys=1.0`(L90)은 死지역(항상 ×1). **[확정·死]**

#### `func_ksi_eq(T, V_n, U, n=1.0, s=1)` — 평형 점유 (L94-97)
- **식**: `z = s·(V_n−U)/w`, `w=func_w(T,n)`; `ξ_eq = logistic(z)` (수치 안정 분기 L97: z≥0이면 `1/(1+e^{−z})`, z<0이면 `e^z/(1+e^z)`).
- **유도**: 단일 전이의 평형 SOC 점유율. logistic = 2-state Fermi 분포. s=σ_d가 부호를 줘 충·방전 방향 기울기 반전.
- **물리 타당성**: 수치 안정 분기로 큰 |z|에서 overflow/underflow 회피, ξ∈(0,1) 보장.
- **호출자** [S2]: `equilibrium`(L365, s 기본=+1), `dqdv`(L455, σ_d 전달). **[확정]**

#### `func_L_q(T, I, Q_cell, dH_a, dS_a, x, A)` — 지연 길이(전하축) (L100-107)
- **식**: `if I≤0: return −inf`; `T_attempt=(I/Q_cell)·h/kB`; `ΔG_a=ΔH_a−T·ΔS_a`;
  `ln L_q = ln(T_attempt/T) − ln(1+e^{−A/RT}) + ΔG_a/RT − x·A/RT`; `L_q=e^{ln L_q}` (eq:lnLq).
- **유도**: 인과 지연(과전위 완화 메모리 길이)을 전하 단위로. Arrhenius 장벽(ΔG_a/RT) + 전이상태 affinity 보정(−xA/RT, x=χ_d) + attempt frequency 비. `(1+e^{−A/RT})` 분모 = 정·역방향 합 정규화.
- **물리 타당성**: `I≤0 → −inf`는 의도적 sentinel(꼬리 없음 신호); 호출측 `_resolve_lag_length`(L319 선행)·`_causal_lowpass`(L113) 비유한 catch → 평형종. **가드가 의도 흐름 차단 X**(§2 검증).
- **호출자** [S2]: `_resolve_lag_length`(L342, x 자리에 χ_d 주입). **[확정]**

#### `_causal_lowpass(source_signal, grid_step, lag_length)` — 인과 저역통과 (L110-128)
- **식**: `decay = e^{−grid_step/lag}`; 1차 IIR `y[i] = decay·y[i−1] + (1−decay)·x[i]` (eq:memory 합성곱 이산형). scipy `lfilter` 우선, 예외 시 순수 파이썬 루프 폴백(동일식).
- **물리 타당성**: `lag≤0 or 비유한 → source.copy()`(L113-114) = 지연 0. 초기상태 `zi`로 transient 억제(L118). **★DC 이득 = 1**(계수 `[1−decay]/[1,−decay]`, ∑=1) → **면적 보존**(검토1 확정, §0·§2).
- **호출자** [S2]: `dqdv`(L471 방전 정방향, L473 충전 역전-필터-역전). **[확정]**

#### `func_dU_hys(T, Omega)` — 분기 gap (보완 헬퍼) (L133-140)
- **식**: `func_U_j_hys` 내부와 동일. `Ω≤2RT → 0`; else `u=√(1−2RT/Ω)`, `(2/F)(Ω·u−2RT·artanh u)` (eq:hysdU).
- **유도**: 히스 전압 gap의 spinodal 상한 닫힌형. Ω↑ → gap↑.
- **호출자** [S2]: `func_U_branch`(L148), `__main__` 검증(L644, L659). **[확정]**

#### `func_U_branch(T, U_j, Omega, gamma, sigma_d, h_eta=1.0)` — 분기중심 (보완) (L143-148)
- **식**: `U_j^d = U_j + ½·σ_d·h_η·γ·ΔU_hys` (eq:hyscenter), `ΔU_hys=func_dU_hys(T,Ω)`.
- **유도**: 평형중심 U_j를 σ_d 방향으로 ±½γΔU_hys 이동 → 방전peak·충전peak 분리. 死함수 `func_U_j_hys`의 `partial_hys` 하드코딩(1.0)을 `h_eta`(부분 cycle 인자)로 노출·인자화.
- **물리 타당성**: σ_d=±1 대칭 분기 → dis/chg peak 거리 = γ·ΔU_hys (self-test L645-646: `d(dis−chg) ≈ +γ·dU_hys` 실증).
- **호출자** [S2]: `dqdv`(L447, `U_j=0`으로 호출해 shift만 추출 후 배열 center에 가산). **[확정]**

#### `func_dH_a_eff(dH_a, Omega, chi_d)` — 유효 활성화엔탈피 (보완) (L152-155)
- **식**: `ΔH_a^eff = ΔH_a − χ_d·Ω` (eq:dHeff).
- **유도**: 깊은 꼬리에서 정규용액 상호작용 상수 몫이 장벽에 흡수. χ_d(방향별)로 충·방전 비대칭 장벽.
- **호출자** [S2]: `_chi_and_dH_eff`(L299), `use_dH_eff=True`일 때만. **[확정]**

#### `func_chi_d(chi, sigma_d)` — 방향별 전달계수 (보완·기본 규칙) (L158-163)
- **식**: `σ_d≥0(방전) → χ_d=χ`; `σ_d<0(충전) → χ_d=1−χ` (eq:chisum 합-1).
- **유도**: 꼬리 깊은 쪽 거울 대칭(방전 ξ→1 / 충전 ξ→0)으로 역방향 장벽 상수몫이 갈림. 생성자 `chi_split`로 교체 가능(L161-162; self-test L628-635 custom rule).
- **호출자** [S2]: `_chi_d`(L290) → `_chi_and_dH_eff`(L297). **[확정]**

#### 가드 헬퍼 `_finite` / `_finite_pos` / `_finite_nonneg` (L167-188)
- `_finite`: NaN/±inf → ValueError. `_finite_pos`: 추가 `>0`(폭·용량·온도 분모용). `_finite_nonneg`: `≥0`(|I|·저항용). 전부 fail-fast. **[확정]**

### 1.3 클래스 `GraphiteAnodeDischargeDQDV` 메서드

#### `__init__` (L221-259)
- 스칼라 인자 유한·범위 가드(L234-248) → `seed_L_V` 계산(L256-259). `chi = x`(미지정 시, L237). `chi_split` callable 검사(L238-239). transitions 원본 참조 저장(L232, 사본화 X — self-test L690은 호출측이 `dict(t)`로 복제). **[확정]**

#### `_build_seed_L_V(T, I, Q_cell)` (L262-269)
- 전이별 방전(σ_d=+1) 기준 L_V seed 리스트. **진단·초기값 전용**(L254-255 주석; dqdv는 실제 (T,I,Q_cell)로 재산출). `__main__` L577에서만 출력. **[확정·진단]**

#### `_n_factor(tr, T)` (L272-278)
- `'n'` 직접 → 반환; 없으면 `'w'`에서 `n = w·F/(RT)` 역산(L277); 둘 다 없으면 1.0.
- ★**키 우선순위 함정**: `'n'`이 있으면 `'w'`는 inert(헤더 L9-10 경고). GRAPHITE_STAGING_LIT는 모든 전이에 `'n':1.0` 보유 → `'w':0.012~0.020`는 **무시됨**(死데이터). 폭 = RT/F 고정. → §2·§3. **[확정]**

#### `_width(tr, T)` (L281-284)
- `func_w(T, _n_factor(tr,T))`. use_w_eff 경로는 v1.0.10에서 제거(면적보존 버그, L7·283). **[확정]**

#### `_chi_d(sigma_d)` (L287-290) / `_chi_and_dH_eff(dH_a, Omega, sigma_d, use_dH_eff)` (L293-300)
- `_chi_d`: `self.chi_split(self.chi, sigma_d)`. `_chi_and_dH_eff`: `(χ_d, ΔH_a^eff)` 동시 산출, per-tr override(None=전역), `use_dH_eff=False` → ΔH_a^eff=ΔH_a. **[확정]**

#### `_resolve_lag_length(transition, T, I, Q_cell, n_j, sigma_d=+1)` (L303-347)
- 우선순위: ① `'L_V'` 직접 지정(피팅·테스트 우회, L313-318) → ② `I≤0 or 'dH_a' 부재 → 0`(L319-320, 평형종) → ③ 동역학 산출.
- 동역학: `A = min(z_cut·|n|·RT, A_cap_RT·RT)`(L331) → `_chi_and_dH_eff`(L338) → `func_L_q`(L342) → 비유한이면 0(L343-344) → `×|dVdq_qa|`(L347).
- **★원본 버그 정정 주석**(L322-327): 원본 `min(s·F·(OCV−U), 4RT)`에서 s를 min 밖으로 빼 충전 시 음수 상한 버그를 정정. s(방향)는 크기에 안 들어가고 χ_d/ΔH_eff가 받음. **[확정]**

#### `equilibrium(V_n, T=298.15)` (L350-367)
- **식**: `dQ/dV = C_bg + Σ_j Q_j·ξ_eq(1−ξ_eq)/w` (eq:eqpeak, 방향 불변, |I|→0).
- U_j: `dH_rxn`&`dS_rxn` 있으면 func_U_j, 없으면 `tr['U']`(L359-362). **히스·동역학 없음**(순수 평형).
- **★보완 2 [9 드래프트 전부 놓침]**: `T = _finite_pos("T", T)`(L352) → equilibrium은 **T 스칼라 전용**. dqdv와 달리 배열 T(V) 미지원(dqdv는 L402-424에서 T_is_array 분기로 비등온 지원). **[확정]**

#### `dqdv(V_app, T, I_abs, Q_cell, s=+1)` (L370-480)
- 핵심 forward. 분극(L408) → 작업격자(L415, 저전위쪽 pad로 꼬리 수용) → 비등온 T(V) interp(L418-422) → 전이 루프(L431-477) → `np.interp` 복원(L479).
- 평형/지연 분기: `lag_len_V < min_lag_grid_steps·grid_step` → 평형 peak(L462-464); else 인과 꼬리(L465-475). 충전(σ_d<0)은 격자 뒤집어 필터 후 되돌림(L473) = 방향 반전 인과기억.
- **식**: `peak_shape = (ξ_eq − r̄)/L_V` (eq:closed, 평형−지연의 미분 이산형, L475).
- **★보완 3 [9 드래프트 전부 놓침]**: `n_work = max(n_work_min, V_n.size*2)`(L412) → seed_L_V sub-grid 접힘 임계(`lag_len_V < min_lag_grid_steps·grid_step`)가 **사용자 V 점수에 종속**(grid_step = v_span / n_work). 즉 꼬리 활성/비활성 경계가 **해상도 의존**(같은 물리 L_V라도 입력 V 점수에 따라 평형종/꼬리종 분기). **[확정]**

#### `curve(...)` facade (L483-508) / `_direction_to_sigma(direction)` (L510-524)
- `curve`: 실험조건(방향문자열·C-rate·Q_cell·T) → `|I| = c_rate·Q_cell`(L505, I_abs 미지정 시) → `dqdv` 재사용. **새 물리 X**(L490; self-test L613-615 curve==dqdv 일치 실증).
- `_direction_to_sigma`: 문자열/정수 → σ_d. 미지원 문자열 → ValueError(L521). **[확정]**

### 1.4 ★ equilibrium vs dqdv 7축 비교표 [O3 §1-G 통합]

| 축 | `equilibrium` (L350) | `dqdv` (L370) |
|---|---|---|
| **물리 의미** | |I|→0 **평형 peak**(eq:eqpeak) | **관측 peak**(eq:hysmaster): 평형−지연 |
| **peak 형태** | Q·ξ(1−ξ)/w (대칭 logistic 종) | Q·(ξ_eq−ξ_lag)/L_V (지연 꼬리) — 단, lag<2칸이면 평형 종으로 분기 |
| **중심** | U_j (히스 미적용) | center = U_j + ½σ_d·h_η·γ·ΔU_hys (분기, **σ_d로 방·충 갈림**) |
| **방향성** | **없음**(s 미전달=+1 고정, L365) | σ_d가 ① 분극 V_n ② 분기중심 ③ χ_d/ΔH_eff ④ 격자역전 4곳에 |
| **분극** | 없음(V_n 직접) | V_n = V_app − σ_d·I_abs·R_n (L408) |
| **동역학** | 없음 | L_V(T,I,Q_cell,A,χ_d,ΔH_eff) 꼬리 |
| **격자/온도** | 입력 V 직접, **T 스칼라 전용**(보완 2) | 패딩 작업격자 + 보간, 배열 T(V) 지원 |

> **★요청 핵심 답 + 정정 1**: equilibrium은 *평형 peak*(분포 자체), dqdv는 *관측 꼬리·히스*(완화 지연 + 분기 중심). dqdv가 |I|→0(L_V→0)이면 분기 스위치로 equilibrium의 peak 형태로 환원되나, **center의 히스 분기는 잔존** — γ>0이면 |I|→0에서도 dqdv는 충방전 peak 위치가 갈린다(self-test L637-646 실증).
>
> **★정정 1 (S1 "방향 불변" 자기모순 배제)**: equilibrium의 "방향 불변"은 **평형 peak 모양**에 한정된 진술이다. equilibrium은 분기중심을 미적용(s 기본 +1, U_j 그대로, L365)하므로, **γ>0인 데이터셋에서 equilibrium peak(@U_j)와 dqdv의 분기 peak(@U_j±½γΔU_hys)는 불일치**한다. 따라서 "equilibrium 식이 방향 불변이므로 dqdv도 방향 불변"식의 서술(S1)은 **자기모순으로 배제** — dqdv는 σ_d가 4곳(분극·분기중심·χ_d/ΔH_eff·격자역전)에 들어가 명백히 방향 의존이다(O3/S3 식 근거).

---

## §2. ★ 조건 audit (충족도·결함·흑연 전용) [골격 = O3]

### 2-A. 물리수식 충족도 [확정] [O3 §2-A]

| 식 (tex) | 코드 구현 (줄) | 충족 |
|---|---|---|
| 분극 V_n=V_app−σ_d|I|R_n | L408 | ✔ |
| 평형중심 U_j=(−ΔH+TΔS)/F | func_U_j L79 | ✔ |
| 히스 gap ΔU_hys (artanh) | func_dU_hys L133-140 / func_U_j_hys L88-89 | ✔ (두 곳 동일식) |
| 분기중심 U^d=U+½σ_d h_η γ ΔU_hys | func_U_branch L148, 호출 L447 | ✔ |
| 폭 w=nRT/F | func_w L75 | ✔ (w_eff 제거 = 1.0.10 변경) |
| 평형점유 ξ_eq=logistic[s(V−U)/w] | func_ksi_eq L96-97 (overflow-safe) | ✔ |
| 평형 peak Q·ξ(1−ξ)/w | L366·L464 | ✔ (면적=Q 검산 §0) |
| χ_d 합-1 | func_chi_d L163 | ✔ |
| L_q (eq:Lqfull) | func_L_q L106 | ✔ (로그식 직접대응 §0) |
| ΔH_a^eff=ΔH_a−χ_d·Ω | func_dH_a_eff L155 | ✔ |
| 꼬리 인과기억(σ_d) | _causal_lowpass + 격자역전 L470-473 | ✔ |
| 합산 dQ/dV=C_bg+ΣQ_j[평형−꼬리] | L477·L427 | ✔ |

→ closed-form 12식 **전부 코드에 매핑** [확정].

### 2-B. 부호·차원·극한 적대 검산 — 11행 [O2 §2.1 11행 통합]

| 항목 | 식·줄 | 검산 | 판정 |
|---|---|---|---|
| **차원: w** | nRT/F (L75) | [J/mol/K·K]/[C/mol]=J/C=V. n 무차원 | ✅ |
| **차원: U_j** | (−ΔH+TΔS)/F (L79) | [J/mol]/[C/mol]=V; TΔS도 J/mol | ✅ |
| **차원: ξ_eq** | logistic[s(V−U)/w] (L96-97) | (V−V)/V=무차원 → ξ∈(0,1) | ✅ |
| **차원: peak** | Q·ξ(1−ξ)/w (L366) | [C]·무차원/[V]=C/V (dQ/dV) | ✅ |
| **차원: L_q** | T_attempt=(I/Q_cell)·h/kB (L104) | [A/C]·[J·s]/[J/K]=[1/s·s·K]=K → ln(K/K) 무차원; ΔG/RT 무차원 | ✅ L_q 무차원 |
| **차원: L_V** | |dVdq_qa|·L_q (L347) | [V]·무차원=V; peak=(ξ−occ)/L_V → 1/V, ×Q[C] → C/V | ✅ |
| **차원: ΔU_hys** | (2/F)(Ω…) (L140) | [J/mol]/[C/mol]=V; artanh 무차원 | ✅ |
| **부호: ΔS_rxn>0 → ∂U/∂T>0** | +T·dS_rxn/F (L79) | 열역학 정합 | ✅ |
| **부호: 분극** | V_n=V−σ_d|I|R_n (L408) | 방전 σ_d=+1: 음극 전위 하강(과전압). 충전 −1: 상승 | ✅ 물리 일관 |
| **부호: 분기** | +½σ_d γ ΔU_hys (L148/447) | 방전 중심 ↑, 충전 ↓. 부호 관례는 문건 eq:hyscenter 정의 위임 | ⚠ 문건 의존 [근거 미발견] |
| **극한: Ω≤2RT** | dU=0 (L85/137) | spinodal 미형성, √(음수) 회피 명시 분기 | ✅ (§0 검산) |
| **극한: |I|→0** | L_q→0(T_attempt→0) → 평형 peak 환원 | self-test L663-665 max diff~0 | ✅ |
| **극한: γ=0 또는 Ω=0** | hys_shift 미실행(L444 게이트 `gamma != 0.0 and Omega > 0.0` 거짓 → else center=U_j) | γ=0 또는 Ω=0 → center=U_j (방·충 동일) | ✅ |

**적대 결론**: 부호·차원·극한 정합. 유일 주의 = 꼬리 undershoot 음수 영역(C-rate高·L_V大에서 (ξ−r̄)<0)은 인과 메모리 모델의 자연 결과(死코드/버그 아님). 분기 부호 관례만 문건 의존(코드만으로 [근거 미발견]).

### 2-C. ★ 피팅 실용 결함 (C1/C2 silent-off·가드 부재) [C1·C2 통합]

물리수식은 충족하나, **optimizer가 자유 탐색하는 피팅 함수로 쓸 때**의 실용 결함 4건. 모두 코드 수정 범위 밖(보고만).

| # | 등급 | 결함 | 증거(줄) | 영향 | 권고 |
|---|---|---|---|---|---|
| **F1** | 결함 | **n≤0 미가드 → NaN/음수** [C1·C2] | `_n_factor` n 그대로 반환(L272-278), `_width`도 양수 검사 없이 func_w(L281-284) | n=0 → w=0 → ξ(1−ξ)/w = NaN; n<0 → 음수 폭 → 음수 dQ/dV(별도 edge 검산 확인) | 피팅 bounds `n>0` 필수 |
| **F2** | 위험 | **dVdq_qa 누락 → silent 꼬리off** [C1·C2] | `transition.get('dVdq_qa', 0.0)`에 abs 곱(L346-347) | dH_a 있어도 dVdq_qa 누락이면 L_V=0 → 동역학 꼬리 silent 소거. 의도적 평형 전이와 누락 실수가 **구분 안 됨** | 동역학 전이는 schema에서 dVdq_qa>0 필수 |
| **F3** | 위험 | **chi/x 범위 미가드** [C1·C2] | 생성자 유한성만(L234,237), `func_chi_d`도 범위 검사 없음(L158-163) | χ<0 또는 χ>1이면 전이상태 분율/장벽 분배가 물리 범위 이탈 → ΔH_a^eff 과변동 | 피팅 자유변수 `[0,1]` bound |
| **F4** | 위험 | **Cbg 유한성 미검** [C1·C2] | 생성자 주석 "사용자 책임"(L236), equilibrium/dqdv 출력 검사 없이 가산(L354-357·427-429) | callable Cbg가 NaN/inf 반환 시 곡선 전체 오염 | fitting wrapper에서 Cbg(V) 유한성 검증 |

**추가 silent-off 함정 [C2·C3]**: `dH_a is None → L_V=0`(L319-320, 꼬리 off 스위치). `dH_a=0.0`은 None이 아니라 막히지 않음. `L_V` 직접 지정(L313 선행 return)은 dH_a/chi/Omega/z_cut/dVdq_qa를 **전부 우회** — 동시 지정 시 후자들이 꼬리에 반영 안 됨(과식별 주의).

### 2-D. 死코드·시그널체인·면적보존·조건부 inert [O3 §2-C 골격 + 검토1 확정]

| ID | 심각도 | 위치 | 내용 | 근거 |
|---|---|---|---|---|
| **C1** | LOW(문서) | L217 docstring | **z_cut docstring 부정확** — "기본 4.357 = ξ_eq 5%"는 틀림. 실제 = **정규화 미분 ξ(1−ξ)/0.25의 5%**(ξ_eq 자체는 98.73%, 1−ξ=1.27%). tex(L1369-70)는 정확. **코드 docstring만 부정확** | §0 검산 (★정정 2) |
| **D4** | INFO(조건부) | L331 | **z_cut override 조건부 inert** — A=min(z_cut·n·RT, A_cap·RT). **n=1 데이터셋 & z_cut≥4.0일 때만** z_cut이 capped되어 inert(A=4RT). **z_cut<4.0 또는 n≠1이면 binding**. 기본 GRAPHITE_STAGING_LIT는 n=1 전부 + 전역 z_cut=4.357 → inert이나, self-test L687-698은 z_cut=2.0(<4.0)로 격리 확인 = z_cut이 binding하는 경로 실증. "항상 inert"는 기본값 한정 | §0 + L691 (★정정 3) |
| **D5** | INFO | L163·L298 | χ=0.5(기본 x=0.5)면 충방전 χ_d 동일(0.5) → ΔH_eff·L_q **충방전 비대칭 0**. 비대칭은 χ≠0.5서만. self-test L622-635가 chi=0.5 + custom split(충전 0.3)으로 차이 실증 | §0 검산 |
| **死코드** | LOW | L82-91 | `func_U_j_hys` 클래스·self-test 미호출. 분기중심은 func_U_branch(L447) 사용. L36 "원형 보존" 동결. last_eta·last_rest·partial_hys=1.0 死(보완 1 참조). 면적·정확성 무영향 | grep 호출 0 |
| **G1** | NOTE | L462-475 | **분기 스위치 진폭 불연속**: 문턱 L_V=ν·Δ_grid에서 꼬리 분기 진폭과 평형종 진폭(∝1/w)이 정확히 일치하도록 맞춰져 있지 않음 → 작은 점프 가능. tex(L1529-33)가 명시 인정(실용 선택, ν↑로 완화). **버그 아님, 알려진 이산 모드 스위치** | tex L1529 |

**면적보존** [확정]: 평형(∫=1.000)·꼬리(∫=0.99986, 큰 L_V서 격자 경계 손실) 모두 보존. 1.0.10의 use_w_eff 제거(L7)가 ξ_eq 폭과 분모 w 불일치(면적 깨짐 버그)를 바로잡음 — `_causal_lowpass` DC gain=1(검토1 확정). 큰 L_V 피팅에선 grid_pad·전압창과 함께 면적 회귀 gate 별도 권고(C2).

**시그널 체인** [확정]: σ_d가 dqdv 진입(L388)→분극(L408)→분기중심(L447)→ksi_eq(L455)→_resolve_lag_length(L460)→χ_d/ΔH_eff(L338)→격자역전(L470-473)까지 일관 전파. seed_L_V는 σ_d=+1 고정(L268, 진단용). 끊김 없음. 비등온 T(V)서 분기 shift는 T_rep=mean(T_work) 스칼라 근사(L447) — 의도적 단순화.

### 2-E. ★ 흑연 음극 전용 (LCO·발열·전자엔트로피 부재) [확정] [검토1 확정 + O3 §2-D]

- **LCO 부재** [확정]: 코드에 LCO/cobalt/order-disorder 항 없음. 클래스명 `GraphiteAnodeDischargeDQDV`, 데이터셋 `GRAPHITE_STAGING_LIT` stage 4→3/3→2L/2L→2/2→1(흑연 LiC_x intercalation). U≈0.085~0.210 V = 흑연 음극 전위대. `grep "LCO|q_rev|dS_e|cathode|양극|발열|전자엔트로피"` → No matches(전 파일, C1·C2·C3 교차 확인).
- **발열(q_rev/self-heating) 부재** [확정]: T는 외생 입력(등온 스칼라 or T(V) 프로파일 L402-424). 발열항·열생성·dT/dt 결합·가역 발열 Q=TΔS 없음. 비등온은 사용자 주입 프로파일일 뿐 내부 열모델 아님.
- **전자 엔트로피(dS_e/Sommerfeld) 부재** [확정]: ΔS_rxn(L78, 반응/구성 엔트로피, U_j 환산)·ΔS_a(L100, 활성화 엔트로피)만. 전자 상태밀도 기반 전자 엔트로피항 없음.
- → **흑연 음극 staging dQ/dV의 평형+동역학 꼬리+히스 전용**. 양극·열·전자구조 확장 의도적 배제(Ch1 범위 정합).

### 2-F. 초벌 피팅 4단계 순서 [C3 §3 통합]

피팅 식별성 붕괴(과적합)를 피하는 단계적 자유화 순서:

1. **저율/평형 데이터**: `Cbg`, `Q_j`, `U_j`(또는 `dH_rxn/dS_rxn` 환산 중심), `n_j`만 자유화. lit dict는 n=1.0이라 'w' 초기값 비작동 → `n`을 명시 핸들로 다룬다.
2. **충/방전 pair**: `Rn`, `gamma` 추가. `Omega` 고정 후 `gamma` 먼저 fit하거나, `gamma=1` 가정 후 `Omega`만 움직여 Ω↔γ 식별성 붕괴 회피.
3. **rate-series tail**: 먼저 `L_V` 직접 fit으로 전이별 꼬리 길이 관측 가능성 확인 → 이후 `L_V` 제거하고 `dH_a`·`dVdq_qa`·`chi`·`z_cut` 물리 파라미터로 환산.
4. **다온도 rate-series**: `dS_rxn`·`dS_a`·`use_dH_eff/Omega` 결합 검토. 단일 온도에서 이들 자유화는 과적합 위험.

> [C3 추정·주의] 기본 동역학 seed L_V는 매우 작아(4.91e-08~4.75e-10 V; self-test print 는 `.4f` 절단으로 `0.0000` 표시 — 인용값은 raw 저장값 기준) 일반 grid에서 sub-grid 판정(L462-465)에 걸려 평형 peak로 접힘 — rate tail 피팅하려면 L_V 직접 fit 또는 동역학 파라미터 재스케일 필요(보완 3의 해상도 의존성과 연동).

---

## §3. ★ 피팅 파라미터 인벤토리 [골격 = O3 2계층 + C3 3등급/순서 + S 축 다이어그램]

### 3-1. 주 파라미터 (1차, 8종) — 지배영역 1줄 [O3 §3] + 3등급 [C3]

> "지배영역" = dQ/dV 곡선에서 그 파라미터가 주로 형태를 좌우하는 곳.
> 권고 등급 [C3]: **자유**(데이터서 직접 식별성 높음) / **조건부 자유**(특정 실험·충분 데이터서만) / **고정/사전값**(초벌 고정, 후속 민감도).

| 기호 | 코드 키/인자 | 줄 | 역할 (식) | 지배영역 | 초기값(LIT) | 등급 [C3] |
|---|---|---|---|---|---|---|
| **U_j** | `'U'` 또는 (`dH_rxn`,`dS_rxn`) | L78, L360 | 평형 중심 (func_U_j) | **peak 위치**(V축) | 0.210/0.140/0.120/0.085 V | 자유(열역학 환산 우선) |
| **n_j** | `'n'`(또는 'w' 역산) | L272-278 | 폭 다중도 w=nRT/F | **peak 폭**(전이 전체) | 1.0 (전 전이) | 자유 (**n>0 bound 필수**, F1) |
| **Q_j** | `'Q'` | L366, L477 | 전이 용량 가중 | **peak 면적/높이** | 0.10/0.12/0.25/0.50 | 자유 (ΣQ 정규화 제약 권고) |
| **Ω_j** | `'Omega'` | L441, L335 | 정규용액 상호작용 (히스 gap·ΔH_eff) | **히스 분기 + 꼬리** | 6000~13000 J/mol | 조건부 자유 (Ω>2RT=4955@298K부터 gap; γ와 결합) |
| **dH_a** | `'dH_a'` | L333, L536… | 활성화 장벽 (func_L_q Arrhenius) | **꼬리 길이 L_V**(exp 지수) | 40000~48000 J/mol | 조건부 자유 (rate-series; 지수 감도) |
| **χ (chi)** | 생성자 `chi`/`x` | L210, L237 | 전이상태 분율 → χ_d (func_chi_d) | **꼬리 충방전 비대칭** | x=0.5 → chi=0.5 | 조건부 자유 (**[0,1] bound**, F3; χ=0.5면 비대칭 0=D5) |
| **L_V** | `'L_V'` (선택) | L209, L313 | 지연 길이 직접지정(동역학 우회) | **꼬리 길이** | 미지정 | 조건부 (초벌 자유 안정; 물리 fit서 제거) |
| **dVdq_qa** | `'dVdq_qa'` | L347, L536… | L_q→L_V 환산 (컷점 OCV 기울기) | **꼬리 V스케일/진폭** | 0.30 V (전 전이) | 조건부 자유 (**누락=silent off**, F2) |

### 3-2. 보조 파라미터 (2차, 10종) [O3 §3 보조 + C3]

| 기호 | 키/인자 | 줄 | 역할 | 지배영역 | 초기값 | 등급 [C3] |
|---|---|---|---|---|---|---|
| ΔH_rxn | `'dH_rxn'` | L78, L534… | U_j=(−ΔH+TΔS)/F enthalpy항 | peak 위치 intercept | −11700~−13000 J/mol | 단온도서 U와 중복→고정; 다온도 조건부 자유 |
| ΔS_rxn | `'dS_rxn'` | L78, L534… | U_j 온도 기울기 ∂U/∂T=ΔS/F | peak 위치 T의존 | +29/0/−5/−16 J/mol/K | 다온도 데이터 전 고정 |
| γ (gamma) | `'gamma'` | L442 | 히스 분기 축소 인자 (func_U_branch) | 히스 분기(dis-chg split=γ·ΔU_hys) | 미지정(0=히스 off) | 충방전 pair서 자유(Ω와 결합, 하나 고정) |
| h_eta | `'h_eta'` | L443 | 부분 cycle 인자 | 히스 분기 스케일 | 미지정(1.0) | 초벌 고정(부분 cycle 데이터서 조건부) |
| dS_a | `'dS_a'` | L100, L334 | ΔG_a=ΔH_a−TΔS_a | 꼬리 T의존 | 0.0 (전 전이) | 초벌 고정 0(다온도서 조건부) |
| z_cut | 생성자/`'z_cut'` | L226, L329 | 컷 affinity A=z_cut·nRT | 꼬리 시작 구동력 | 4.357 | 고정 (n=1서 A_cap에 capped=inert, D4; **단 z_cut<4.0이면 binding**) |
| A_cap_RT | 생성자/`'A_cap_RT'` | L226, L330 | A 상한 = A_cap·RT | 꼬리 산출 상한 | 4.0 | 고정 |
| use_dH_eff | 생성자/override | L225, L298 | ΔH_a^eff 보강 토글 | 꼬리 Ω-동역학 결합 | True | 모델 선택 스위치(고정) |
| Rn | 생성자 `Rn` | L235, L408 | 분극 V_n=V−σ_d|I|Rn | **전체 V-shift**(IR, C-rate 의존) | 0.0(LIT)/0.01(self-test) | rate-series서 자유 |
| Cbg | 생성자 `Cbg` | L236, L427 | 배경 dQ/dV (상수/V함수) | baseline 오프셋 | 0.0/0.05(self-test) | 자유 (**callable 유한성 미검**, F4) |

> 순수 수치 제어(피팅 X, 고정): `grid_pad_lo/hi`(0.15)·`n_work_min`(2048)·`min_lag_grid_steps`(2.0)·`v_span_floor`(1e-6)·`seed_T/I/Q_cell`(298.15/0.1/1.0, 진단용). `direction/c_rate/I_abs/Q_cell/T` = 실험 메타데이터(고정 입력).

### 3-3. 곡선 지배영역 축 다이어그램 [S1·S2·S3 통합]

```
V축 (dQ/dV 곡선)  ← 낮은 V (만충) ──────── 높은 V (방전 말) →

peak 위치   ──────── U_j (또는 dH_rxn + dS_rxn 온도이동) + Rn·|I|·σ_d (분극 이동)
peak 폭     ──────── n_j (또는 w 폴백) = nRT/F · T 비례 · 면적보존 조건
peak 높이   ──────── Q_j (용량 가중; Q 고정·n↑ → 낮아짐, 면적=Q 불변)
히스 분기   ──────── Omega · gamma (Ω>2RT 조건) + h_eta (부분 cycle)
꼬리 길이   ──────── dH_a + dVdq_qa → L_V (또는 L_V 직접) + Omega(ΔH_eff 보강)
꼬리 비대칭 ──────── chi → χ_d (방전 χ vs 충전 1−χ; χ=0.5면 대칭)
꼬리 방향   ──────── sigma_d (방전: V증가 방향 인과 / 충전: V감소 방향 역전)
꼬리 온도   ──────── dH_a − T·dS_a (dS_a=0이면 순 Arrhenius)
베이스라인  ──────── Cbg
```

**지배영역 요약** [확정]: 위치=U_j / 폭=n_j(w) / 면적=Q_j / 히스 split=Ω·γ / 꼬리=dH_a·dVdq_qa·L_V / 비대칭=χ / 전체 IR shift=Rn / baseline=Cbg. 꼬리 최고감도 = **dH_a(지수)**, 위치 최고감도 = **U_j/dH_rxn**.

---

## §4. ★ 9 드래프트 전부 놓친 보완 4건 (추가) [요청 명시]

1. **`func_U_j_hys`(L83) 인자 `s:int=1` vs 대체 `func_U_branch`(L144) `sigma_d`** — 死코드라 호출 흐름엔 무해. 단 인자명·기본값 차이(`s=1` 디폴트 vs `sigma_d` 무디폴트)로 외부 직접 호출 시 부호 관례 혼동 가능. (§1.2 func_U_j_hys 항)
2. **`equilibrium`(L350)은 T 스칼라 전용**(L352 `T = _finite_pos("T", T)`) — dqdv(L402-424 T_is_array 분기)와 달리 배열 T(V) 미지원. (§1.3 equilibrium 항·§1.4 7축표)
3. **`n_work=max(n_work_min, V_n.size*2)`(L412) → seed_L_V sub-grid 접힘 임계가 사용자 V 점수에 종속** — 꼬리 활성/비활성 경계(min_lag_grid_steps·grid_step)가 grid_step=v_span/n_work를 통해 **해상도 의존**. 같은 물리 L_V라도 입력 V 점수에 따라 평형종/꼬리종 분기. (§1.3 dqdv 항)
4. **코드 self-test(L567-703)에 면적=Q assert 부재** — 헤더는 면적 실증을 외부 `plot_dqdv.py`에 위임(L11). self-test는 `_ok`(유한성)·guards 7/7·curve==dqdv·히스 split·override isolation만 검증, **면적 회귀 가드 없음**(테스트 커버리지 결함). (§1.0 #24)

---

## §5. 정정·배제 요약 (★ 검토1 지시 반영 + adversarial finalizer 보정)

- **★정정 1**: S1 "방향 불변" 자기모순 서술 **배제**. equilibrium은 분기중심 미적용(s 기본 +1, L365)으로 dqdv와 불일치(γ>0서 equilibrium peak@U_j vs dqdv 분기 peak@U_j±½γΔU_hys). (§1.4)
- **★정정 2**: z_cut docstring 부정확(L217 "ξ_eq 5%" 틀림 → 정규화 미분 ξ(1−ξ)/0.25의 5%; ξ_eq 자체 98.73%). (§0·§2-D C1) — *코드 docstring 부정확 판정은 tex(L1369-70) 문건 대조에 의존(코드 단독 아님).*
- **★정정 3**: D4 조건부 — z_cut override는 **n=1 & z_cut≥4.0서만** inert(A=4RT). z_cut<4.0 또는 n≠1이면 binding. "항상"은 기본값 한정. (§0·§2-D D4)
- **★검토1 확정 채택**: 흑연 음극 전용(LCO·발열·전자엔트로피 부재, §2-E) · `_causal_lowpass` DC gain=1 면적보존(L110-128) · `func_U_j_hys` 死코드(L82-91, func_U_branch L447 대체) · 'w' 폴백 inert('n':1.0 우선, L274).
- **★adversarial finalizer 보정(vN-11)**: ① z_cut docstring 줄 인용 L218→**L217**(§0·§2-D C1·§5 정정 2; L218은 A_cap_RT docstring). ② §2-B 극한 행 "γ=0 → center=U_j"를 **"γ=0 또는 Ω=0"**로 보강(게이트 L444 `gamma != 0.0 and Omega > 0.0`). ③ seed L_V 인용에 `.4f` 절단 부기(§2-F). ④ z_cut docstring 판정의 tex 문건 의존성 부기(§5 정정 2). 그 외(물리식 12개·24심볼 coverage·정정 1/3·보완 1~4) adversarial 전부 PASS → 본문 불변.

---

*조립: 2026-07-01 | vN-11 finalizer(adversarial 정정 4건 반영 + 11항목 result 래핑) | 본체 파일: V1010_P1_map_v10.md 승계 | 산출: V1010_P1_code-audit_RESULT.md*
