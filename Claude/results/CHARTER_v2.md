# Chapter 1 Rebuild — Charter v2

**Date**: 2026-05-28
**Authority**: User verbatim 2026-05-27 + 2026-05-28 (statements 1, 2, 3)
**Supersedes**: `Claude/old/results/PHASE_E0_foundation_reset_charter_RESULT.md` (Charter v1) + Charter Addendum 1 + Charter Addendum 2 (v1 부속)
**Predecessor archive**: `Claude/old/` (Phase A~D, Phase E0~E4, direction review 모두 보존)
**Scope**: Charter for the **second-attempt** rebuild of Chapter 1. v1 attempt rejected by user 2026-05-28 ("처음부터 다시").

---

## §00. ★ 작업의 핵심 (사용자 verbatim, 본 Charter 의 절대 기준)

> 본 §00 은 사용자가 직접 제공한 작업의 핵심 내용 verbatim. Charter 의 모든 §·spine·decision 은 본 §00 을 절대 기준으로 한다. 본 내용과 충돌하는 모든 후속 결정은 무효.

### §00.1 작업 동기 + 물리 현상 + 이론적 가설 (사용자 verbatim, 2026-05-28 statement 2)

> "LIB의 ICA 분석에서 온도와 현시점의 전위 상태에 따라서 그 그래프의 개형이 특히 피크부분이 상변이에 의해서 나타나는데 그 상변이의 의해 나타나는 **피크 꼬리의 개형이 늘어지느냐 빨리 떨어지느냐**가 달라지는것을 확인했다. 특히 **온도가 낮을때는 꼬리가 길고, 온도가 높으면 그 꼬리가 상대적으로 짧게 끝나는** 현상이 관측되었어. 원래라면 그렇게 온도에 대해 **약간 가우시안 피크 형상**이 나타나고 더이상 진행이 안될 것으로 생각되는데 그 **온도에 의한 배리어** 외에 추가적인 **극판 자체 전위에 따른 배리어를 낮추는 효과**가 있다고 봤고 그 **유효 배리어의 논리를 확정**하고 그 것을 이용해 **피크의 거동을 해석하는 피팅하는데 쓸수 있는 논리 식을 구하는게 이 작업의 핵심**이야."

### §00.2 작업의 4 가지 원칙 (사용자 verbatim, 2026-05-28 statement 1)

> "1. 피팅 솔버 코드 구축X
> 2. 흑연의 ICA 즉 dQdV를 해석하는 이론적 배경을 작업
> 3. 논리 전개를 가다듬어서 가능하면 논문이나 특허로 발전시킬까 고민중
> 4. 산출물은 원본 처럼 가능하면 모든 수식 전개의 **논리적 비약이 없고**, **생략 없이** 모든 과정을 **대학교 학부생 수준의 지식**으로도 그 논리 전개 과정을 따라갈 수 있게 정리해주길 바라고 있다."

### §00.3 v1 폐기와 v2 시작 사유 (사용자 verbatim, 2026-05-28 statement 3)

> "리뷰가 끝나면 작업 계획부터 다시 처음부터 진행하자. 그게 맞는것 같다. 하루종일 작업한게 아깝지만 처음부터 다시 계획부터 짜서 시작하는게 맞겠다. 이전까지의 작업물을 old 폴더 하나 만들어서 밀어넣고, 다시 처음부터 시작하자."

### §00.4 핵심 키워드 (본 Charter 전체 적용)

- **ICA peak** — 피크는 상변이 신호
- **꼬리 거동** — 본 작업의 1 차 초점 (피크 면적은 피팅 영역, 본 작업 X)
- **온도 배리어** — Gibbs 활성화 자유에너지 ΔG_a(T)
- **극판 전위 보조 유효 배리어** — 전위 의존 lowering −χ·A
- **유효 배리어 = ΔG_eff = ΔG_a − χ·A** ★ spine 출발점
- **가우시안 peak** — 평형 분포의 형상 (logistic·임의 sigmoid 가 아닌 가우시안 명시)
- **저T 꼬리 길고, 고T 꼬리 짧음** — T 의존성 해석 대상
- **피팅 가능 논리식** — 본 작업의 deliverable
- **학부생 수준 전개 + 논리 비약 0 + 생략 0** — 작성 원칙
- **논문 또는 특허 수준 정밀도** — 정밀도 기준
- **피팅 솔버 코드 X** — 범위 외

### §00.5 본 Charter 의 본 §00 정합 의무

본 Charter 의 모든 §0-§12 + Master Roadmap v2 + 모든 phase plan/result 는 본 §00 을 절대 기준으로 한다. 충돌 발생 시:
- 본 §00 우선.
- 본 §00 과 모순되는 모든 식·문장·spine·결정은 **즉시 invalid** 처리.
- 본 §00 외 추가 사용자 verbatim 이 들어오면 본 §00 에 immediate append.

---

## §0. v1 폐기와 v2 시작의 사유

v1 attempt (Phase A~D 정독 + Phase E0~E4 ρ(μ) spine 작성, 1203 줄 LaTeX + 5 governance documents + 4 phase results) 는 사용자 의도와 **spine 출발점에서 misalignment**. 구체적 근거 = `old/results/DIRECTION_REVIEW_2026-05-28.md` §9 종합 정합도 표.

사용자 명시 (2026-05-28 statement 3):
> "리뷰가 끝나면 작업 계획부터 다시 처음부터 진행하자. 그게 맞는것 같다. 하루종일 작업한게 아깝지만 처음부터 다시 계획부터 짜서 시작하는게 맞겠다."

v1 의 모든 산출은 `Claude/old/` 에 보존되며, v2 는 v1 의 어떤 LaTeX 본문도 재사용하지 않고 처음부터 새로 작성한다. v1 의 ``파악된 사실'' (ver5/ver1_rechecked2 의 §·식 위치, JCP ref 6/7 의 DOI 등) 만 input 사실로 사용.

---

## §1. Objective (사용자 의도 verbatim 정리)

### 1.1 본 작업의 출발 사실 (사용자 2026-05-27, 5-28 statements 1+2)

> "LIB의 ICA 분석에서 온도와 현시점의 전위 상태에 따라서 그 그래프의 개형이 특히 피크부분이 상변이에 의해서 나타나는데 그 상변이의 의해 나타나는 피크 꼬리의 개형이 늘어지느냐 빨리 떨어지느냐가 달라지는것을 확인했다. 특히 온도가 낮을때는 꼬리가 길고, 온도가 높으면 그 꼬리가 상대적으로 짧게 끝나는 현상이 관측되었어. 원래라면 그렇게 온도에 대해 약간 가우시안 피크 형상이 나타나고 더이상 진행이 안될 것으로 생각되는데 그 온도에 의한 배리어 외에 추가적인 극판 자체 전위에 따른 배리어를 낮추는 효과가 있다고 봤고 그 유효 배리어의 논리를 확정하고 그 것을 이용해 피크의 거동을 해석하는 피팅하는데 쓸수 있는 논리 식을 구하는게 이 작업의 핵심이야."

### 1.2 의도 element 6 개 (I1~I6)

| # | 의도 | spine 위치 |
|---|---|---|
| **I1** | 본 작업 = **꼬리 거동** 의 논리 전개 (피크 면적 X, 피팅 단계로 deferred) | 종료점 |
| **I2** | 피크 = 상변이 신호, 꼬리 = lag (kinetic relaxation 미완성) | 동역학 |
| **I3** | 저 T → 꼬리 길고, 고 T → 꼬리 짧음 | T 의존성 |
| **I4** | 평형 = **가우시안 peak** 형상 (logistic / 임의 sigmoid 가 아닌 가우시안 명시) | 평형 분포 |
| **I5** | **유효 배리어 = 온도 배리어 ΔG_a(T) + 전위 의존 lowering −χ·A(전위)** | spine 출발점 |
| **I6** | 유효 배리어 논리 확정 + 꼬리 거동 해석 + **피팅 가능 논리식** 도출 | 본 작업의 deliverable |

### 1.3 4 가지 작업 원칙 (사용자 2026-05-28 statement 1)

| # | 원칙 |
|---|---|
| P1 | **피팅 솔버 코드 구축 X** (본 세션 범위 외) |
| P2 | **ICA 이론적 배경** 작업 |
| P3 | 가능하면 **논문 또는 특허** 로 발전 가능한 수준의 정밀도 |
| P4 | 모든 수식 전개에 **논리적 비약 0 + 생략 0 + 대학교 학부생 수준 지식으로 따라갈 수 있게** |

### 1.4 본 Chapter 1 의 학술적 위상 (v2 명시)

본 Chapter 1 v2 는 **graphite 음극 ICA(dQ/dV) 꼬리 거동의 열역학적·동역학적 해석 프레임워크** 를 학술 논문 또는 특허 수준의 정밀도로 정리한다. 본 작업의 **load-bearing 차별점** = 사용자 본인 박사학위 연구 (Refs 6, 7, JCP 2017) 의 Fredholm 적분 방정식 제2종 비율 치환법을 **graphite ICA 꼬리 거동의 시간 적분형 self-consistent equation 해법** 으로 정확히 위치시키는 것.

---

## §2. Spine v2 (Locked, 사용자 의도 정합)

### 2.1 Spine 구조 (A1~A12)

다음 12 개 정의·식이 본 Chapter 1 v2 의 spine 을 구성한다. 모든 후속 derivation 은 spine 의 어느 한 식의 도출 또는 응용이다.

```
[기초 정의 — ver5 §6.1-§6.4 보존, §6.5 폐기]

(A1) ΔG_{a,j}(T) = ΔH_{a,j} − T · ΔS_{a,j}
        [Gibbs 활성화 자유에너지. 사용자 의도 I5 의 "온도에 의한 배리어".]

(A2) A_j(V_{n,app}, T) = s_{φ,j} · F · (V_{n,app} − U_j(T))
        [전위 보조 구동력. 사용자 의도 I5 의 "극판 자체 전위에 따른 배리어 lowering" 의 driving force.]

(A3) ★ ΔG_{eff,j}(T, A_j) = ΔG_{a,j}(T) − χ_j · A_j
        [★★★ 유효 배리어. 사용자 의도 verbatim "유효 배리어의 논리". spine 출발점.]

(A4) k_j(T, A_j) = ν_j(T) · exp(−ΔG_{eff,j} / (R·T))
        [Arrhenius 류 속도상수. 사용자 의도 I3 의 T 의존성 + I5 의 전위 lowering 결합.]

[평형 분포 — ver5 §5.2 erf 채택, §5.1 logistic 폐기]

(A5) ξ_{eq,j}(V_n, T) = (1/2) · [1 + erf((V_n − U_j(T)) / (σ_j(T)·√2))]
        [평형 진행률 = 가우시안 분포의 누적 적분. 사용자 명시 I4 "가우시안 피크 형상":
         dξ_{eq,j}/dV_n = (1/(σ_j √(2π))) · exp(−(V_n − U_j)²/(2 σ_j²)) = 가우시안 peak.]

[동역학 — ver5 §7 보존]

(A6) dξ_j/dt = k_j(T, A_j) · (ξ_{eq,j}(V_n, T) − ξ_j)
        [Relaxation 동역학. 사용자 의도 I2 (lag) + I6 (꼬리 거동의 동역학).]

(A7) dξ_j/dq = (Q_cell / |I|) · k_j · (ξ_{eq,j} − ξ_j)         [정전류 q 좌표]

[V_n 결정 — V_n,OCV 외부 lookup 채택 (DQ-DIR-1 기본 선택 1)]

(A8) V_n(q, T) = V_{n,OCV}(q, T)
        [평형 시 V_n. 외부 lookup 함수로 가정 (실험 OCV 곡선).
         이유: V_n implicit 격상으로 인한 self-consistent loop 회피 (Refs 6/7 는 ξ 의 시간 적분식 에 적용).
         user clarification 시 V_n implicit 으로 변경 가능 (Charter v2.1).]

[★ 시간 적분 형식 — 본 spine 의 self-consistent 부분]

(A9) ξ_j(t) = ξ_j(0) + ∫_0^t dt' k_j(t') · (ξ_{eq,j}(t') − ξ_j(t'))
        [Volterra 형식. integrand 안에 ξ_j(t') 자기 등장. k 와 ξ_eq 가 시간 의존 시 self-consistent.]

[★ Refs 6/7 (사용자 박사 연구) 의 정확한 적용 위치]

(A10) ξ_j(t)/ξ_j(t') ≈ ξ_j^{simple}(t)/ξ_j^{simple}(t')
        [비율 치환. ξ_j^{simple} = k 와 ξ_eq 가 시간 무관일 때의 closed-form 해 = 1 − exp(−k·t)·(ξ_eq − ξ(0))/ξ_eq 류.]

(A11) ξ_j(t) closed-form = ... (Phase E9_v2 에서 Refs 6/7 의 (33)→(34)→(39) 류 도출 적용)
        [본 spine 의 핵심 deliverable. 시간/전위/T 에 따른 closed-form ξ_j.]

[관측]

(A12) (dQ/dV)_j ∝ Q_{j,tot} · (dξ_j/dq) / (dV_{n,app}/dq)
        [j-th transition 의 ICA 기여. 꼬리 모양 = (A11) closed-form 의 ξ_j(t)
         가 ξ_{eq,j}(V_n) 를 못 따라잡은 lag 가 dξ_j/dq 의 꼬리로 나타남.
         피팅 가능 논리식 = (A1)~(A11) 의 파라미터 (ΔH_a, ΔS_a, χ, ν, U, σ) 로 표현된 closed-form.]
```

### 2.2 Spine 외 사용 가능 식 (보조)

- ver5 §3 effective transition `j = 1, ..., N_p`: spine 의 j-index 의미.
- ver5 §8 장벽 분포 평균 `ρ_j(g)`: 단일 k_j 가 꼬리 길이 부족 시 보조 도구로 ``advanced note'' 단원에 별 처리 (DQ-DIR-4 권장 안 = "보조 단원으로 유지").
- ver1_rechecked2 §6.1 V_n / V_{n,app} / V_{n,drive} 3 분리: A2/A6/A8 의 변수 의미 명확화에 보존.
- 연속 ρ(μ; q, T) 일반화 (v1 의 spine): **본 spine 의 advanced note 또는 appendix 로 선택적 제공** (DQ-DIR-5 권장 안 = "필요시만").

---

## §3. Anti-Pattern List (v2 정밀화)

v1 Charter §2 의 AP1-AP8 + Charter Addendum 1 §11.4 의 추가 check 를 정밀화하여 본 v2 의 anti-pattern 으로 재선언.

### 3.1 Spine 정의식에서 금지

| # | Pattern | 사유 | v1 Charter 와의 차이 |
|---|---|---|---|
| AP1 | `max(ΔG_{eff,j}, 0)` (ReLU step) | 사용자 verbatim "스텝 펑션" 정합 | 동일 |
| AP2 | `min(k_j, k_max)` (saturation step) | 동일 | 동일 |
| AP3 | `ξ_{eq,j}` 의 logistic 형태 (1/(1+exp(...))) | 사용자 명시 가우시안 분포 (≠ logistic) | 동일 |
| **AP4 (재분류)** | `ξ_{eq,j}` 의 erf 형태 | **v2 에서는 OK-derived** (사용자 명시 가우시안 분포의 누적 적분 = erf 가 자연 결과) | **★ 재분류** |
| AP5 | discrete N_p 자체를 anti-pattern 으로 본 v1 분류 | **v2 에서는 OK** (사용자 의도 = discrete-j ξ_j spine) | **★ 재분류** |
| AP6 | softplus regularization 을 정의식에 사용 | 동일 | 동일 |
| AP7 | 임의 sigmoid 가족을 정의식에 사용 | 동일 | 동일 |
| AP8 | 활성화 장벽 분포 ρ_j(g) 를 spine 의 primary state 로 사용 | spine 은 ξ_j; ρ_j(g) 는 advanced note 단원 | v1 에 부재, v2 신설 |

### 3.2 Spine 정의식에서 OK-derived (v1 에서 anti-pattern 이었으나 v2 에서 OK)

| Element | v2 OK 사유 |
|---|---|
| `erf((V−U)/(σ√2))` | 사용자 명시 가우시안 분포의 누적 적분 (A5). 물리 가정 기반. |
| `discrete N_p`, `ξ_j`, `k_j`, `U_j`, `w_j`, `Q_{j,tot}` | 사용자 의도 spine 의 primary 표현 (ver5 §6 + §7 의 정합 부분 보존). 연속 μ-space 표현은 advanced note. |
| `ν_j(T)`, `χ_j`, `ΔH_a,j`, `ΔS_a,j` | (A1)~(A4) 의 정합 표현. |

### 3.3 Spine 외 (보조 단원, advanced note, appendix) 의 사용

- ρ(μ; q, T) continuous 일반화 = OK (advanced note 한정)
- ρ_j(g) 장벽 분포 평균 = OK (advanced note 한정, v1 의 Phase E0 charter §3.1 의 K_n cross-kernel 와는 다름)

---

## §4. Smooth-Limit Consistency Rule (v1 보존)

`ε_Q → 0` 등의 regularization parameter 는 v1 Charter §5 와 동일하게 smooth-limit 표기 의무.

신 spine v2 의 (A1)-(A12) 자체에는 regularization 이 부재 (gauss 적분 결과 erf 가 모두 부드러운 형태) — 본 rule 의 자동 충족.

---

## §5. Writing Precision Standard (Charter Addendum 1 §11 흡수)

v1 의 Charter Addendum 1 §11 (논리적 비약 0 + 생략 0 + 학부생 수준 친절성) 을 본 v2 의 §5 로 흡수. 본문 그대로:

- §5.1 **No-logical-jump rule**: 매 식이 명시적 단계로 도출.
- §5.2 **No-omission rule**: 변수 치환·적분·미분·극한 모든 단계 명시.
- §5.3 **Undergraduate-level prose**: 학부 전기화학 + 열역학 + 미적분 + 선형대수 가정.
- §5.4 **Pass 1 keyword check + reporting**.
- §5.5 **Phase Result 의 §"Writing precision audit" 의무**.

(v1 Charter Addendum 1 §11 본문 전문 = `Claude/old/results/PHASE_E0_foundation_reset_charter_RESULT_ADDENDUM_1.md`)

---

## §6. Audit Dimension #11 (v1 Charter §6 + Addendum 1 §11.4 흡수)

System-fidelity Pass 1/2/3 절차. AP4/AP5 의 재분류 반영.

| Pass 1 keyword | v2 분류 |
|---|---|
| `\max`, `\min`, `\Heaviside`, `\sign`, `\clip` | FAIL-definitional 가능성, Pass 2 검토 |
| `\operatorname{erf}` | **OK-derived** (사용자 명시 가우시안 누적, A5 의 정합 표현) |
| `\sigma(\cdot)`, logistic, `1/(1+\exp(\cdot))` | FAIL-definitional (AP3) |
| `softplus`, `\ln(1+\exp(\cdot))` | FAIL-definitional (AP6) |
| discrete N_p, ξ_j, k_j, U_j | OK (spine primary) |
| "trivially", "obviously", "clearly" 단독 | FAIL — §5.4 정합 |
| "It can be shown that" without derivation | FAIL |

---

## §7. Physical Phenomenon Motivation (Charter Addendum 2 §16 흡수)

v1 의 Charter Addendum 2 §16 (O1, O2, O3) 의 핵심을 본 v2 §7 로 흡수. 본 작업 (Chapter 1 v2) 가 재현해야 할 실험 관측:

| # | 관측 | spine 의 어느 식이 설명? |
|---|---|---|
| **O1** | 피크 위치 = staging transition 화학 퍼텐셜 | (A5) ξ_{eq,j} 의 peak 중심 U_j(T) |
| **O2** | 피크 면적 ≈ 온도 무관 (사용자 = 피팅 영역으로 deferred) | (A5) 의 integral 면적 = 1 (정규화) × Q_{j,tot}; T 무관성은 피팅 단계 검증 |
| **O3 ★** | **꼬리 모양 T 의존: 저T 길고 고T 짧음** | (A4) k_j 의 T 의존성 + (A6) lag → (A11) closed-form 의 꼬리 형태 |

**O3 가 본 Chapter 1 v2 의 load-bearing observable**. 사용자 의도 I1 의 직접 표현.

---

## §8. Variable Inventory (v2 신규)

### 8.1 Canonical 변수 (spine 정의식에 직접 등장)

| 기호 | LaTeX | 단위 | 의미 |
|---|---|---|---|
| j | j | (index) | Effective staging transition index, j = 1, ..., N_p |
| T | T | K | 절대 온도 |
| t | t | s | 시간 |
| q | q | 무차원 | 방전 진행 좌표 |
| I | I | A | 셀 전류 |
| s_I, s_{φ,j} | s_I, s_{\phi,j} | ±1 | 부호 conv |
| F | F | C/mol | Faraday 상수 |
| R | R | J/(mol·K) | 기체 상수 |
| Q_cell | Q_{\cell} | C | 셀 기준 용량 |
| V_n | V_n | V | 음극 내부 전위 |
| V_{n,app} | V_{n,\app} | V | 음극 관측 전위 |
| V_{n,drive} | V_{n,\drive} | V | 반응 구동 전위 |
| V_{n,OCV} | V_{n,\OCV}(q, T) | V | 외부 lookup OCV 함수 (A8) |
| R_n | R_n(q, T, |I|) | Ω | 음극 유효 저항 |
| ξ_j | \xi_j | 무차원 | j-th transition 진행률 |
| ξ_{eq,j} | \xi_{\eq,j} | 무차원 | j-th transition 평형 진행률 |
| ΔH_{a,j} | \Delta H_{a,j} | J/mol | 활성화 엔탈피 (피팅 파라미터) |
| ΔS_{a,j} | \Delta S_{a,j} | J/(mol·K) | 활성화 엔트로피 (피팅 파라미터) |
| ΔG_{a,j} | \Delta G_{a,j}(T) | J/mol | Gibbs 활성화 자유에너지 (A1) |
| A_j | \mathcal A_j(V_{n,app}, T) | J/mol | 전위 보조 구동력 (A2) |
| ΔG_{eff,j} | \Delta G_{\eff,j}(T, A_j) | J/mol | ★ 유효 배리어 (A3) |
| χ_j | \chi_j | 무차원 | 전위 보조 결합 계수 (A3) |
| ν_j | \nu_j(T) | 1/s | Arrhenius prefactor (A4) |
| k_j | k_j(T, A_j) | 1/s | 속도상수 (A4) |
| U_j | U_j(T) | V | j-th transition 중심 전위 (A2, A5) |
| σ_j | \sigma_j(T) | V | j-th transition 가우시안 폭 (A5) |
| Q_{j,tot} | Q_{j,\tot} | C | j-th transition 총용량 기여 (A12) |
| Q_n | Q_n(q) | C | 음극 누적 용량 |
| Q_{bg} | Q_{\bg}(q) | C | 배경 용량 (jaw transition 외) |

### 8.2 Derived 변수

- ξ_j^{simple}(t): (A10) 의 단순 case closed-form, k 와 ξ_eq 가 시간 무관 시 = 1 − exp(−k t) (ξ_eq − ξ(0))
- dξ_j/dq, dQ_n/dq, dV_{n,app}/dq: 미분 항
- (dQ/dV)_j: (A12), 관측

### 8.3 Advanced note 전용 변수 (spine 외)

- ρ(μ; q, T): v1 의 continuous distribution. 본 v2 의 advanced appendix 에 선택 제공.
- ρ_j(g): ver5 §8 의 장벽 분포. 본 v2 의 advanced note 에 선택 제공.

---

## §9. Refs 6, 7 (사용자 박사 연구) 의 정확한 위치

- **Ref 6**: S. Lee, C. Y. Son, J. Sung, S. H. Chong, "Communication: Propagator for diffusive dynamics of an interacting molecular pair", J. Chem. Phys. **134**, 121102 (2011). **DOI: 10.1063/1.3565476**.
- **Ref 7**: C. Y. Son, J. Kim, J.-H. Kim, J. S. Kim, S. Lee, "An accurate expression for the rates of diffusion-influenced bimolecular reactions with long-range reactivity", J. Chem. Phys. **138**, 164123 (2013). **DOI: 10.1063/1.4802584**.

### 9.1 본 v2 spine 에서의 적용 위치

- (A9) Volterra 시간 적분식 자체가 Fredholm 적분 방정식 제2종 형태 — Refs 6, 7 의 비율 치환법 적용 가능.
- (A10) 비율 치환 = ξ_j(t)/ξ_j(t') ≈ ξ_j^{simple}(t)/ξ_j^{simple}(t').
- (A11) 비율 치환 적용 결과 = closed-form ξ_j(t) 해석해. JCP 2017 Eq.(33)→(34)→(39) 유도 패턴 적용.

### 9.2 v1 과의 차이

- v1: Refs 6/7 = ρ(μ) continuous 적분식의 해법 (Loop C).
- v2: Refs 6/7 = ξ_j 시간 적분식의 해법 (사용자 의도 spine 의 직접 응용).

---

## §10. Decisions Locked (Charter v2 시점)

| ID | 결정 |
|---|---|
| **DEC-1** | spine = (A1)~(A12) 명시. discrete-j ξ_j primary. |
| **DEC-2** | V_n 결정 = V_{n,OCV}(q, T) 외부 lookup (A8). V_n implicit 으로 변경 시 Charter v2.1. |
| **DEC-3** | 평형 분포 = erf (A5) = 가우시안 누적. logistic 폐기. |
| **DEC-4** | Refs 6/7 = ξ 시간 적분식 (A9-A11) 의 비율 치환 closed-form. |
| **DEC-5** | 이전 v1 모든 산출물 = Claude/old/ 에 보존, 본 v2 작업의 input 사실 (ver5/ver1_rechecked2 정독 결과 + JCP DOI) 만 재참조. |
| **DEC-6** | Cumulative step = 1 부터 신 시리즈 (Phase 0_v2 = step 1 시작). |
| **DEC-7** | ver5 §8 (장벽 분포 평균) = advanced note 보조 단원 (DQ-DIR-4 채택). |
| **DEC-8** | ρ(μ) continuous 일반화 = appendix 선택 제공 (DQ-DIR-5 채택). |

---

## §11. Decision Queue (Charter v2 시점 open)

| ID | 항목 | Resolution timing |
|---|---|---|
| **DQ-v2-1** | V_n 결정 = 외부 lookup (DEC-2) 인지, user clarification 시 implicit 변경? | Phase 검수 또는 user 직접 |
| **DQ-v2-2** | Refs 6/7 의 (A10) 비율 치환 ξ^{simple} 후보 의 정확한 형태 (1 − exp(−kt) 가 맞는지) | Phase 9_v2 (Refs 6/7 적용) 시 |
| **DQ-v2-3** | σ_j(T) 의 T 의존성 functional form (kT 비례 가정?) | Phase 5_v2 (ξ_eq 도출) 시 |
| **DQ-v2-4** | ν_j(T) 의 T 의존성 functional form (Arrhenius 류 추가? T-independent?) | Phase 6_v2 (k 도출) 시 |
| **DQ-v2-5** | χ_j 의 추정 — ver5 의 일반적 값, 또는 실험적 boundary? | Phase 4_v2 (ΔG_eff 정의) 시 |

---

## §12. Meta

- 본 Charter v2 는 새 작업의 governance. 향후 모든 phase plan/result 는 본 Charter v2 + §5 Writing Precision Standard + §6 Dim #11 + §7 O1-O3 motivation 정합.
- Claude/old/ 의 v1 산출물은 **사실 자료** 로만 참조 (ver5/ver1_rechecked2 의 §·식 위치, JCP DOI 등). v1 의 spine 결정·결론 은 본 v2 의 진행에 영향 X.
- DEC-1 ~ DEC-8 은 본 Charter v2 의 lock 사항. 사용자가 추가 정보 제공 시 v2.1 등으로 갱신.
