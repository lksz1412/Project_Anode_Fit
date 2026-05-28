# v2 (유효배리어 closed-form) vs v3 (ChatGPT 전하보존 6장) 정합성 심층 대조

**Date**: 2026-05-28
**대상 v2**: `Claude/docs/graphite_ica_chapter1.tex` (spine A1-A12, 1891 lines)
**대상 v3**: `~/Downloads/graphite_ica_ch1_ch6_physical_v3_rechecked.tex` (ChatGPT, charge-balance 6장)
**목적**: 식별식 단위 1:1 대조 → SAME / RECONCILABLE / CONTRADICTORY 판정
**사용자 지시**: "두 모델 정합성 심층 대조" (2026-05-28)

---

## §0. 한 줄 결론

**v2와 v3는 배리어→Arrhenius→relaxation→비율치환 핵심 사슬이 식별식 수준에서 동일하다.
진짜 모순은 단 1개 (평형분포 erf vs logistic) 뿐이며, 이는 저속 OCV peak 꼬리
데이터로 실험적으로 판정 가능하다. 나머지 차이는 모두 v3가 v2를 일반화하거나
v2의 미결정(DQ-v2-1)을 해소한 관계다.**

---

## §1. 식별식 1:1 대조표

| 물리 성분 | v2 식 | v3 식 | 판정 | 근거 |
|---|---|---|---|---|
| 온도 배리어 | A1: `ΔG_a = ΔH_a − T·ΔS_a` | `ΔG_a,j(T) = ΔH_a,j − T·ΔS_a,j` | **SAME** | 동일 |
| 전위 driving force | A2: `A = s_φ F(V_app − U)` | eq:A_drive: `A_j = s_φ,j F(V_drive − U_j)` | **SAME** | (V_drive=V_n,app 근사 시 동일) |
| ★ 유효 배리어 | A3: `ΔG_eff = ΔG_a − χ·A` | eq:Geff: `ΔG_eff,j = ΔG_a,j − χ_j·A_j` | **SAME** | 글자까지 일치. 양 모델 공유 핵심 |
| 속도 상수 | A4: `k = ν exp(−ΔG_eff/RT)` | eq:k_act_physical: `k_act = ν exp(−ΔG_eff/RT)` | **SAME** | 동일 (v2 k = v3 k_act) |
| ΔG_eff<0 처리 | "정의 영역 한정 (ΔG_eff≥0)" | eq:k_phys_limited: `1/k_phys = 1/k_act + 1/k_lim` | **RECONCILABLE** | §2.A |
| 평형 분포 | A5: `ξ_eq = ½[1+erf((V−U)/(σ√2))]` | eq:xi_eq_logistic: `ξ_eq = 1/(1+exp(−(V−U)/w))` | **★ CONTRADICTORY** | §2.B (유일한 진짜 모순) |
| 진행률 동역학 | A6: `dξ/dt = k(ξ_eq − ξ)` | eq:dxidt: `dξ_j/dt = k_phys(ξ_eq − ξ_j)` | **SAME** | 동일 형식 |
| q 좌표 변환 | A7: `dξ/dq = (Q_cell/|I|)k(ξ_eq−ξ)` | eq:dxidq: 동일 | **SAME** | 동일 |
| V_n 결정 | A8: `V_n = V_n,OCV(q,T)` 외부 lookup (DEC-2, DQ-v2-1 open) | eq:charge_balance: `Q_cell·q = Q_bg + Σ Q_tot ξ_j` root | **RECONCILABLE** | §2.C (v3가 DQ-v2-1 해소) |
| 시간 적분형 | A9: Volterra `ξ = ξ_0 + ∫k(ξ_eq−ξ)dt'` | (동일 ODE의 시간적분, ch6 DAE) | **SAME** | 동일 방정식 |
| closed-form 해법 | ★ A10-A11: Refs 6/7 비율치환 | ch6 "Fredholm/Pade ratio 계열" 검증 후보 | **RECONCILABLE** | §2.D (동일 기법, 위상만 다름) |
| ICA 관측식 | A12: `(dQ/dV)_j = Q_tot(dξ/dq)/(dV_app/dq)` | eq:ica_final: `dQ_ext/dV_app = Q_cell/(dV_app/dq)` | **SAME** | (v2는 j-분해, v3는 총합 — 동일 chain rule) |
| 배리어 분포 | (DEC-8 부록 옵션) | ρ_j(g;T) (ch1 §"장벽 분포 확장") | **SAME (위상)** | 양쪽 다 옵션/확장 |
| 열 해석 | (Chapter 2 후속 roadmap, 범위 외) | ch2 + ch4 (가역/비가역 열) | v3 superset | §3 |
| 전기화학 BV | (없음) | ch3 (forward/backward, Butler-Volmer) | v3 superset | §3 |
| 충방전 hysteresis | (없음) | ch5 (signed current, metastable branch) | v3 superset | §3 |
| 수치해법 | (P1: solver X → closed-form) | ch6 (DAE/root-find/g-grid) | **TENSION** | §2.E |

**집계**: SAME 8 · RECONCILABLE 3 · CONTRADICTORY 1 · v3-superset 3 · TENSION 1.

---

## §2. RECONCILABLE / CONTRADICTORY 상세

### A. ΔG_eff<0 처리 — RECONCILABLE (두 해법, 같은 문제)

두 모델 모두 "ΔG_eff<0에서 Arrhenius가 비물리적으로 폭주"라는 동일 문제를 인식.
- **v2**: spine 정의 영역을 ΔG_eff≥0으로 한정 (꼬리 영역은 V_app≈U_j 근방이라 자동 충족).
- **v3**: `1/k_phys = 1/k_act + 1/k_lim` 직렬 병목으로 정규화 (k_lim = transport/site/diffusion/current).

→ **모순 아님.** v2의 k는 v3의 k_act = (k_lim→∞ 극한). v3는 ΔG_eff<0 영역까지 물리적으로
확장한 **strict 일반화**이고, v2는 꼬리 영역(ΔG_eff>0)에 한정한 **단순화**다. 같은 문제의
회피(v2) vs 정규화(v3). v3가 더 완전, v2가 더 간결.

### B. 평형 분포 erf vs logistic — ★ 유일한 진짜 모순

이게 두 모델의 **유일한 식별식 수준 모순**이다.

| | v2 erf (Gaussian) | v3 logistic |
|---|---|---|
| `ξ_eq` | `½[1+erf((V−U)/(σ√2))]` | `1/(1+exp(−(V−U)/w))` |
| `dξ_eq/dV` (peak) | `(1/σ√2π)exp(−(V−U)²/2σ²)` | `(1/w)ξ_eq(1−ξ_eq) = (1/4w)sech²(·)` |
| peak 중심 거동 | 거의 동일 (FWHM 매칭 가능: σ ↔ w) | 거의 동일 |
| **꼬리 감쇠** | `e^(−(V−U)²/2σ²)` (가우시안, 빠름) | `e^(−|V−U|/w)` (지수, 느림/heavy) |

**왜 진짜 모순인가:**
1. 두 함수는 꼬리에서 근본적으로 다르다 (가우시안 vs 지수 감쇠). peak 근처 매칭은 되나
   꼬리는 발산. 저속(준평형, GITT/0.05C) 조건에서 ξ_j→ξ_eq이므로 **평형 꼬리 형상이
   직접 관측**된다 → 실험적으로 구별 가능. 둘 다 맞을 수 없다.
2. **★ 사용자 가설과의 정합성이 갈린다.** 사용자 verbatim: "원래라면 가우시안 피크
   형상이 나타나고 더이상 진행이 안될 것... 추가적 극판 전위 배리어 lowering 효과로
   꼬리." 즉 사용자 mental model = **평형은 가우시안(빨리 끝남), 늘어진 꼬리는 배리어
   (비평형) 효과**.
   - v2 (erf): 평형 baseline을 가우시안으로 두어 → 잔여 꼬리를 배리어/동역학 효과로
     **깨끗이 귀속** → 사용자 가설 검증에 적합.
   - v3 (logistic): 평형 width w_j에 이미 지수 꼬리를 내장 → 꼬리 일부를 평형으로
     흡수 → **사용자가 입증하려는 배리어-꼬리 효과를 가릴 위험.**

**구조적 얽힘 (중요):**
- v2 relaxation 형식 `k(ξ_eq−ξ)`는 ξ_eq 형태에 **agnostic** — erf 그대로 잘 작동.
- v3 forward/backward 형식 `r+(1−ξ)−r−ξ`는 detailed balance `ln(r+/r−)=(V−U)/w`가
  **logistic일 때만 V에 선형**. erf로 바꾸면 ch3 detailed balance가 inverse-erf로
  지저분해짐. 즉 **v3의 깔끔한 ch3 구조는 logistic 선택에 의존**.
→ 평형 형태 선택이 kinetics 표현과 얽혀 있다. v2는 어느 쪽도 수용, v3는 logistic 선호.

**판정 방법**: 저속 OCV(≈0.05C 또는 GITT 준평형) dQ/dV peak의 꼬리 감쇠를
`log(dQ/dV)` vs `(V−U)` (지수면 선형) 또는 vs `(V−U)²` (가우시안이면 선형)로 plot →
어느 쪽이 직선인지로 결정. **이 하나의 실험이 erf/logistic 분기를 닫는다.**

### C. V_n 결정 — RECONCILABLE (v3가 v2의 DQ-v2-1을 해소)

- v2 A8: `V_n = V_n,OCV(q,T)` 외부 lookup, **DEC-2 + DQ-v2-1 = "사용자가 implicit로
  변경 가능"으로 명시 open** 상태였음.
- v3: `Q_cell·q = Q_bg(V_n,T) + Σ Q_tot ξ_j`에서 V_n을 암시적 root로 계산.

**정합 관계**: v3의 **평형** 전하보존(ξ_j=ξ_eq)을 V_n에 대해 풀면 정확히
`V_n = V_n,OCV(q,T)` (v3 eq:ocv_implicit). 즉 **v3의 V_OCV = v2의 외부 lookup**이고,
v3는 그것을 전하보존에서 **유도**하며 비평형에서 보정한다.
→ **모순 아님. v3는 v2가 열어둔 DQ-v2-1을 "implicit" 쪽으로 해소한 branch.** v2가 이미
변경 가능성을 예고했으므로 충돌이 아니라 **결정의 구체화**다. v3가 더 엄밀(비평형 V_n
보정 포함).

### D. closed-form vs 수치 — RECONCILABLE (동일 기법, 위상만 다름)

- v2 A10-A11: 시간적분 Volterra를 Refs 6/7 **비율치환**으로 closed-form 해.
- v3 ch6: 같은 ODE/DAE를 수치적분 + **"Fredholm/Pade ratio 계열 해법"을 검증 후보로
  명시**.

**결정적 발견**: v3 ch6이 명시한 "Fredholm/Pade ratio approximation"이 **정확히 v2의
load-bearing 기법(Refs 6/7 비율치환)**이다. 즉:
- v2: 비율치환 = **1차 deliverable (closed-form)**.
- v3: 비율치환 = **ch6 검증-tier 가속 solver 후보** (direct g-grid가 reference, ratio가
  가속).
→ **모순 아님. 동일 수학 기법이 두 모델에서 위상만 다르다.** v2의 전체 기여가 v3 ch6의
한 절로 매핑된다. v2 closed-form = v3 수치해의 해석적 근사.

### E. P1 (solver X) — TENSION (모순은 아니나 정신과 어긋남)

- v2: P1 준수, closed-form만, solver 없음.
- v3 ch6: root-finding/DAE/g-grid/Prony 등 **수치해법 설계 전반**.
- P1 원문: "피팅 솔버 코드 구축 X." v3 ch6은 코드가 아니라 해법 **방법론** 기술 →
  글자 위반은 아님. 그러나 "이론 영역에 머문다"는 P1 정신은 v2 쪽에 가깝다.

---

## §3. v3 단독 영역 (v2 범위 외 — 충돌 무관)

v3 ch2(열)·ch3(전기화학 BV)·ch4(엔트로피 생성 열)·ch5(충방전 hysteresis)는 v2가
"Chapter 2 후속 roadmap"으로 명시 연기한 영역. **충돌이 아니라 v3가 더 넓은 scope.**
v2 ch1 내용 전부가 v3 ch1(+ch6 closed-form)에 매핑되고, v3 ch2-5는 그 위의 superset.

---

## §4. 종합 판정

```
                 v3 (전하보존 6장 superset)
   ┌───────────────────────────────────────────────┐
   │  ch1: 배리어·Arrhenius·relaxation·q변환         │ ← v2 A1-A4,A6,A7 과 SAME
   │       V_n charge-balance root                  │ ← v2 A8 의 DQ-v2-1 해소(RECONCILABLE)
   │       ξ_eq = logistic                          │ ← v2 A5(erf) 와 ★CONTRADICTORY
   │  ch6: DAE + Fredholm/Pade ratio                │ ← v2 A10-A11 = 동일기법(RECONCILABLE)
   │  ch2-5: 열·전기화학·hysteresis                 │ ← v2 범위 외 (superset)
   └───────────────────────────────────────────────┘
```

- **물리 핵심 사슬(배리어→속도→동역학→비율치환)은 v2=v3 동일.** 두 모델은 별개가
  아니라 **같은 코어의 좁은 버전(v2) vs 넓은 버전(v3)**이다.
- **진짜 모순은 평형분포 erf vs logistic 단 1개.** 그리고 이게 하필 사용자 핵심
  질문(꼬리=배리어 효과?)의 판별축이며, **저속 OCV 꼬리 데이터 1개로 결정 가능**.
- v2의 closed-form은 v3 ch6의 검증-tier 기법으로 이미 포함됨. V_n은 v3가 v2의 미결정을
  엄밀하게 해소.

## §5. 권고 (사용자 결정 보조)

**합성 경로 (자연스러운 reconciliation):**
1. 코어(A1-A4, A6-A7) = 양 모델 공유 → 그대로 유지.
2. V_n = v3 charge-balance root 채택 (DQ-v2-1을 implicit로 확정, 평형서 V_OCV로 환원).
3. 평형분포 = **저속 OCV 꼬리 plot으로 erf/logistic 실측 판정** (이 실험 전엔 사용자
   가설에 충실한 erf를 baseline로, logistic을 대안으로 병기).
4. closed-form(v2 비율치환) = v3 ch6의 가속·검증 solver로 위치 (이미 v3가 그 자리를
   마련해 둠).
5. v3 ch2-5(열·전기화학·hysteresis) = v2 ch1 완료 후의 후속 chapter.

→ 즉 **"v3 골격 + erf 판정 보류 + v2 closed-form을 ch6 가속기로"** 가 두 모델을 잃지
않는 합집합. 단, 평형분포 실측 전까지 erf/logistic은 미결(DQ)로 남긴다.
