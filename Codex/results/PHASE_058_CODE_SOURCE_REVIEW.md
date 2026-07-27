# Phase 058 v1.0.10–v1.0.13 production code source review

상태: `CODE_SOURCE_READ_COMPLETE / EXECUTION_ADJUDICATION_PENDING`  
대상: 3개 unique production Python blob, 2,610 lines  
경계: 역사적 source를 수정하지 않았으며 이 문서는 감사 기록이다.

## 계보 요약

- v1.0.10은 현재 lineage의 실질 production kernel을 이미 모두 포함한다.
- v1.0.12는 헤더·설명 정정이 중심이고 물리 실행 경로는 사실상 같다.
- v1.0.13은 다음 네 가지를 실제로 바꾼다.
  1. LCO facade의 charge/discharge를 delithiation sign으로 환산
  2. 단일점/퇴화 voltage span에서 lag를 강제로 끔
  3. entropy coefficient의 config 항에 `n`을 반영하고 `w`-only면 끔
  4. LCO electronic flag를 `x≈0.85`, `U≈3.93 V` 전이로 이동

이 변경들은 제한적인 정합 수리이며, finite-current/low-temperature
physics kernel의 재유도는 아니다.

## 실행 경로

```text
curve
→ direction label mapping
→ I_use = c_rate * Q_cell or I_abs
→ dqdv
→ V_n = V_app - sigma_d |I| R_n
→ per transition U_j(T), branch shift, w(T), xi_eq
→ _resolve_lag_length
→ equilibrium bell OR causal low-pass tail
→ Q_j weighted sum and interpolation
```

열 경로는 별도다.

```text
entropy_coefficient
→ equilibrium xi and overlap weights
→ center dS/F + optional imposed-width config derivative
→ reversible_heat = -I T dU/dT
```

## 핵심 판정

### 보존 가능한 구현 자산

- 함수/클래스 입력 가드와 비파괴 배열 처리
- equilibrium bell의 면적을 `Q_j`에 연결하는 구조
- charge와 discharge의 causal traversal 방향을 반전하는 구현
- v1.0.13의 electrode-aware facade mapping
- theory-only 경로와 현 구현의 동결 근사를 주석에서 구분하려는 태도

### 교정이 필요한 구현

1. `Q_cell` 단위

   `curve`는 `I_use=c_rate*Q_cell`을 계산한다. 이때 `c_rate`가 h⁻¹이면
   `Q_cell`은 Ah여야 A가 된다. 같은 API와 문건은 `Q_cell`을 C라고도
   부르며 `q=Q/Q_cell`과 `I/Q_cell`에 공용한다. 이는 3600배 차이를
   타입이나 변수명으로 차단하지 못한 단위 계약 결함이다.

2. inert `w`

   `_n_factor`는 `n`을 `w`보다 우선한다. 모든 기본 graphite/LCO dict에
   `n=1.0`과 `w`가 함께 있으므로 표에 적힌 `w=0.012–0.030 V`는 사용되지
   않는다. 실제 폭은 모든 전이에서 `RT/F≈25.7 mV`다.

3. `Omega` 역할 과적재

   `Omega`는 regular-solution/hysteresis 입력인 동시에 기본
   `use_dH_eff=True` 때문에 `Delta H_a_eff=Delta H_a-chi_d Omega`로
   kinetics를 직접 바꾼다. 하나의 자유에너지/transition-state
   derivation 없이 같은 수치를 두 물리에 공유한다.

4. 상수 affinity

   기본 `n=1`, `z_cut=4.357`, `A_cap_RT=4.0`이면
   `A=min(4.357RT,4RT)=4RT`다. 따라서 local electrode potential,
   state 또는 current가 장벽을 바꾼다는 사용자 목표와 달리, kinetics의
   affinity는 전이당 온도 비례 상수로 동결된다.

5. coarse-graining 부재

   `k_B T/h`의 molecular attempt frequency를 electrode-scale
   transition progress의 `k_j`로 바로 사용한다. active-site density,
   particle length, diffusion/charge-transfer resistance 또는
   population kinetics로 잇는 coarse-graining 다리가 없다.

6. grid-dependent handoff

   `L_V < min_lag_grid_steps * grid_step`이면 causal kernel을 버리고
   equilibrium bell을 직접 사용한다. 이는 물리적 asymptotic matching이
   아니라 grid-dependent switch다. v1.0.13의 degenerate-span 수리는
   단일점 이상행동만 막고 일반 handoff 불연속은 닫지 않는다.

7. LCO theory-only 전자항

   `LCOCathodeDQDV._effective_dS_rxn`은 항상 `x_center`와
   `T_ref=298.15 K`에서 `func_dSe_molar`를 평가한다. 따라서 문건의
   `x(V)` 국소 게이트, `Delta S_e∝T`, `U(T)`의 T² 곡률은 실행되지 않는다.
   대신 약 `-45.7 J mol^-1 K^-1` 상수와 이에 맞춘 `dH_rxn`이 들어간다.

8. 재료 범위

   이 lineage에는 silicon 또는 graphite+silicon blend production model이
   없다. LCO 기본 dict에도 `Omega`, `gamma`, `dH_a`, `L_V`가 없어
   finite-current lag와 hysteresis가 기본 비활성이다. 따라서 사용자의
   실제 목표 재료·조건 범위를 완결했다고 볼 수 없다.

9. 열 부호 API

   `reversible_heat`의 `I>0 discharge`는 Bernardi cell convention이고
   `curve(direction="discharge")`의 graphite half-cell 방향과 반대 화학
   방향이라고 코드 자체가 인정한다. 두 public API가 같은 “discharge”를
   다르게 쓰므로 최종 코드에서는 reaction-oriented current를 먼저 정하고
   cell/electrode labels를 adapter에서만 변환해야 한다.

## 아직 판정하지 않은 것

- 원래 tests가 위 경로 중 무엇을 실제 assert하는가
- 기본 Eyring 파라미터가 만드는 `L_q`, `L_V`의 수치 크기
- lag branch의 면적 손실과 handoff jump
- scalar/array/non-isothermal path의 재현성
- golden NPZ와 bit-exact 재생성

이 항목은 Steps 27.2–27.5에서 독립 실행으로 판정한다.
