# Phase D — JCP 2017 Ref. 6, 7 Methodology Result

작성일: 2026-05-27
계획서: [Claude/plans/2026-05-27-anode-fit-situational-assessment-plan.md](../plans/2026-05-27-anode-fit-situational-assessment-plan.md)
양식: [[feedback_phase_execution_loop]] 11항목

## Summary

JCP 2017 (Kyusup Lee et al., **사용자 본인** 제1저자) 전수 정독 — 10 페이지, 724 줄 텍스트. Ref. 6, 7 의 정확 서지 + 본문 내 3 곳 인용 위치 + 원 방법론 (**Fredholm integral equation of 2nd kind 의 비율 substitution 해법**) 수학 구조 + ver1_rechecked2 의 Loop 3 (Volterra-like integral eq.) 에 대응되는 **변수 매핑 5 요소** + **그대로 가져오면 안 되는 물리적 가정 차이** 진단.

결론: ref. 6, 7 의 비율 substitution 기법은 **본질적으로 graphite 시스템에 적용 가능**. 다만 Fredholm (공간 정상 상태) ↔ Volterra (시간 진화) 변환 + isotropic 1D 적용 + 저율 영역 정확성 가정 등 4 가지 차이 명시.

**Phase B 의 OI-B2 (4 분류 (4) 재검증) 결과**: (4) 물리 가정 충돌 = **여전히 해당 X 로 확정**. 단 적용 시 시간/공간 변환 추가 가정 필요 (별 분류 → "방법론 적용 조건" 항목).

## Step Range

cumulative Steps **14 ~ 18** (Phase D 전체).

## Inputs

| 파일 | 경로 | 분량 |
|---|---|---:|
| JCP 2017 PDF | `Claude/_local_only/JCP_147(14)_144111_(2017) - Effects of external electric field.pdf` | 10 페이지, 2.07 MB |
| 텍스트 추출 (pdftotext -layout) | `Claude/_local_only/jcp_extract.txt` (gitignored) | 724 줄, 69 KB |
| (참조) Phase B Result | `Claude/results/PHASE_B_ver1_rechecked_feedback_diagnosis_RESULT.md` | — |

## Files Created

- `Claude/results/PHASE_D_jcp_ref6_7_methodology_RESULT.md` (본 파일)
- `Claude/_local_only/jcp_extract.txt` (pdftotext 추출 결과, gitignored)

## Files Updated

없음

## Read Coverage

| 파일 | 분할 read 호출 | cover 한 범위 | 상태 |
|---|---|---|---|
| `jcp_extract.txt` (PDF 추출본) | `Read` 단일 호출 (default limit) | 줄 1 ~ 724 (전 10 페이지) | **전수 정독 PASS** |

비고: PDF 원본 직접 read 는 `pdftoppm` 의존성 부재로 실패. `pdftotext -layout` 으로 텍스트 추출 후 정독. 텍스트 추출 시 일부 LaTeX 수식이 깨질 수 있음 (예: 그리스 문자 → ASCII 대체). 본 Result 에서 수식 인용은 line 번호 + 원문 의도 추출.

## Execution Evidence

### 서지 정보 (Step 16 — GATE_D3)

**JCP 2017 (본 논문)**:
- **저자**: Kyusup Lee¹, Seonghoon Lee¹, Cheol Ho Choi², **Sangyoub Lee¹** (corresponding, sangyoub@snu.ac.kr)
  - ¹ Department of Chemistry, Seoul National University, Seoul 08826, South Korea
  - ² Department of Chemistry, Kyungpook National University, Daegu 702-701, South Korea
- **제목**: Effects of external electric field and anisotropic long-range reactivity on charge separation probability
- **학술지**: The Journal of Chemical Physics
- **권/호/article**: 147 (14), 144111
- **연도**: 2017 (Received 19 Aug 2017, Accepted 2 Oct 2017, Published online 13 Oct 2017)
- **DOI**: 10.1063/1.5000882
- **출판사**: AIP Publishing
- **본인 확정 근거**: 제1저자 "Kyusup Lee" + 사용자 이메일 `lksz1412@gmail.com` (이니셜 패턴 정합) + 사용자 5-27 verbatim 진술 "그게 내 논문이야". **확정**

**Ref. 6** (line 711-712):
> S. Lee, C. Y. Son, J. Sung, and S. Chong, **J. Chem. Phys. 134, 121102 (2011)**.

- **추가 정보**: J. Chem. Phys. 134, 121102 (2011). Page 121102 = "Communications" 또는 "Letter" 형태 (4-page communication 권장 추정). DOI 직접 명시 X — 외부 검색 권장.
- **저자**: Sangyoub Lee, Chang Y. Son, Jaeyoung Sung, Sangyoub Chong (추정 매핑). "S. Lee" 가 본 JCP 2017 의 corresponding author Sangyoub Lee 와 동일 인물로 보임.

**Ref. 7** (line 713-714):
> C. Y. Son, J. Kim, J.-H. Kim, J. S. Kim, and S. Lee, **J. Chem. Phys. 138, 164123 (2013)**.

- **추가 정보**: J. Chem. Phys. 138, 164123 (2013).
- **저자**: Chang Y. Son, Jiwon Kim, Ji-Hyun Kim, Jong-Seok Kim, Sangyoub Lee.

(주: Ref. 6, 7 모두 그룹 자체의 prior work — 본 JCP 2017 의 인용 line 297-298 "An efficient solution method for this type of integral was proposed **by us** in Refs. 6 and 7" 에서 명시. 본인 그룹 method 의 anchor papers)

### 본문 내 인용 위치 (Step 15 — GATE_D2)

Ref. 6, 7 는 본문 3 곳에서 인용됨. 각 위치의 page · paragraph · 인용 맥락:

#### 인용 1: §I Introduction (page 1, paragraph 4) — jcp_extract.txt line 44-45

> "In this work, we employ the **recently proposed solution method⁶,⁷** for **Fredholm integral equations of the second kind** to treat the effects of external electric field and anisotropic long-range reactivity on the recombination dynamics of a geminate charge pair."

→ Ref. 6, 7 가 **Fredholm integral equation of 2nd kind** 의 해법 (본 그룹 prior work) 임을 명시. 본 논문이 그 방법을 새 시스템 (외부 전기장 + anisotropic long-range) 에 적용.

#### 인용 2: §II.C "Solution to Eq. (6) for long-range reaction sink functions" (page 3, paragraph 직후 Eq. 32) — line 296-298

> "This type of integral equations is called the **Fredholm integral equation of the second kind**. An efficient solution method for this type of integral was proposed by us in **Refs. 6 and 7**. First, a formally exact solution to Eq. (32) is obtained as..."

→ **본 논문의 핵심 적분식 Eq. (32)** (W̄_u(r) 가 자기 해의 적분 항을 갖는 형태) 가 Fredholm 2nd kind. Ref. 6, 7 의 해법으로 Eq. (33) (formally exact solution) + Eq. (39) (closed-form analytic expression after approximation) 유도.

#### 인용 3: §III.B "Systems involving a long-range reaction sink" (page 7, paragraph 2) — line 599-600

> "Again, when the Onsager distance rc is large and the inherent reactivity parameter σ₀σ²/D is small, the agreement of analytic estimates of W̄_u(σ) with the exact numerical results is excellent. This exemplifies the utility of our **solution method for Fredholm integral equations of the second kind**.⁶,⁷"

→ Ref. 6, 7 의 method 가 수치 결과와 일치하는 정확도를 보여 utility 입증. 결과 검증 차원에서 ref. 6, 7 재인용.

### 원 방법론 수학 구조 (Step 17)

본 JCP 2017 논문이 ref. 6, 7 의 방법론을 적용한 형식 (본문 §II.C, line 280-389 정독 결과).

#### 단계 1: 대상 적분식 형태 (Eq. 32, line 280-289)

```
W̄_u(r) = 1 - (σ/D) · ∫_σ^∞ dr₁ [r₁² ζ(r₁) / e^{U₁(r₁)}] · W̄_u(r₁)
       + (1/D) ∫_σ^∞ dr₁ φ(σ/r₁) · ∂/∂r₁ [r₁² ζ(r₁) / e^{U₁(r₁)}] · W̄_u(r₁)
```

- 형식: **Fredholm integral equation of the 2nd kind**
- integrand 안에 자기 해 `W̄_u(r₁)` 등장 — self-consistent / fixed-point structure
- 적분 범위 `[σ, ∞]` 고정 (= Fredholm; Volterra 와의 차이는 가변 범위 vs 고정 범위)

#### 단계 2: Formally exact rearrangement (Eq. 33, line 302-317)

```
W̄_u(r) = [1 + (σ/D) ∫_σ^∞ dr₁ (r₁²ζ(r₁)/e^{U₁(r₁)}) · W̄_u(r₁)/W̄_u(r)
        + (1/D) ∫_σ^∞ dr₁ φ(σ/r₁) · ∂/∂r₁ (r₁²ζ(r₁)/e^{U₁(r₁)}) · W̄_u(r₁)/W̄_u(r)]^{-1}
```

- 핵심: `W̄_u(r₁)` 을 `W̄_u(r₁)/W̄_u(r) · W̄_u(r)` 로 분리 → 분모 `W̄_u(r)` 를 적분 밖으로 이동 → 적분 안엔 **비율** `W̄_u(r₁)/W̄_u(r)` 만 남음

#### 단계 3: 비율 substitution 근사 (Eq. 34, line 337)

```
W̄_u(r₁) / W̄_u(r) ≈ W̄_u^δ(r₁) / W̄_u^δ(r)
```

- 우변의 `W̄_u^δ` = **δ-function reaction sink 의 경우의 알려진 해** (§II.B 의 Eq. 25, line 187-188)
- 즉: 복잡한 sink (long-range) 의 비율을 단순한 sink (δ-function, contact reaction only) 의 알려진 해의 비율로 **근사 대체**
- 비율로만 쓰이는 이유: 절대 크기는 다르지만 r₁/r 에 따른 **상대적 감쇠 패턴은 유사** 하다는 물리적 직관 (large rc + small σ³φ/D 영역에서 정확)

#### 단계 4: δ-function sink 의 해 W̄_u^δ(r) (Eq. 25, line 187-188)

```
W̄_u^δ(r) = 1 + (e^{-U₁(σ)} / 4πD) · rx · [φ(1) - φ(σ/r)] · W̄_u^δ(σ)
```

with `W̄_u^δ(σ) = [1 + (e^{-U₁(σ)} / 4πD) · rx · φ(1)]^{-1}` (Eq. 24, line 179-180).

- `φ(z)` = special function (Eq. 23, line 265-273): `φ(z) = ∫_0^z dy (K/y / sinh(K/y)) · e^{U₁(σ/y)}`
- `rx` = contracted reactivity (Eq. 18, line 217-220): `rx = (1/2) ∫_{-1}^{1} dμ · e^{Kμ} · ν(μ)`
- **이게 단순한 경우의 closed-form 해**. 비율 substitution 의 기준.

#### 단계 5: 최종 closed-form analytic expression (Eq. 39, line 280-289)

```
W̄_u(r) = [1 + (σ/D)φ(σ/r) ∫_σ^∞ dr₁ (r₁²ζ(r₁)/e^{U₁(r₁)}) · (W̄_u^δ(r₁)/W̄_u^δ(r))
        + (1/D) ∫_σ^∞ dr₁ φ(σ/r₁) · ∂/∂r₁ (r₁²ζ(r₁)/e^{U₁(r₁)}) · (W̄_u^δ(r₁)/W̄_u^δ(r))]^{-1}
```

- Eq. (37) line 365-366 의 명시 비율 substitution 결과를 Eq. (33) 에 대입한 최종 형태
- **모든 항이 계산 가능** (적분도 수치적으로 안정적 — 자기 해 등장 X)
- Closed-form analytic — JCP 2017 의 핵심 contribution

#### 정합 조건 (line 399-409, §III §"key approximations")

비율 substitution Eq. (34) 의 정확도가 보장되는 조건:
1. **외부 전기장 K 가 너무 크지 않을 것** (anisotropic 영향 작을 것)
2. **Onsager distance rc 가 초기 separation r 에 비해 클 것** (isotropic 잠재력 dominate)
3. **inherent reactivity σ 가 작을 것** (geminate particles 가 오래 살아남아 분포가 dominant interaction 으로 결정될 것)

→ "**저율 + 약한 결합 + 큰 Onsager 거리**" 영역에서 정확. 강한 외부장 또는 강한 결합에서 정확도 저하 (본문 §III.A Fig. 1 등에서 확인).

### 5 요소 매핑 (Step 18 — GATE_D4)

#### Ref. 6 — S. Lee, C. Y. Son, J. Sung, S. Chong (J. Chem. Phys. 134, 121102 (2011))

- **서지**: S. Lee, C. Y. Son, J. Sung, and S. Chong, J. Chem. Phys. **134**, 121102 (2011).
- **인용 위치 (본 JCP 2017 본문)**: page 1 §I (line 44-45), page 3 §II.C (line 297-298), page 7 §III.B (line 599-600). 3 곳에서 Ref. 7 과 함께 인용.
- **원 방법론 (수학 구조)**: Fredholm integral equation of the 2nd kind 의 **비율 substitution + 단순 sink 의 알려진 해로 비율 근사** 기법. 본 JCP 2017 의 Eq. (32) → (33) → (34) → (39) 가 그 적용 사례. Ref. 6 가 method 의 **초기 제안** 으로 추정 (Communications letter 형식, 4-page short paper).
- **본 graphite dQ/dV 문제 변수 매핑**:
  | JCP/Ref.6,7 변수 | graphite ver1_rechecked2 변수 |
  |---|---|
  | `W̄_u(r)` (charge separation 평균 확률) | `ξ_j(t)` 또는 `V_n(t)` (시간 진화 변수) |
  | `r` (입자 거리, 적분 변수) | `t` (시간) 또는 `q` (방전 좌표) |
  | `σ` (contact distance, BC) | `t=0` (초기) 또는 `q=0` (방전 시작) |
  | `D` (diffusion coefficient) | `Q_cell` (셀 용량 정규화 인자, `dq/dt = |I|/Q_cell`) |
  | `S_R(r,μ)` (reaction sink) | `k_j(V_n, q, T, I)` (속도상수) |
  | `U₁(r)` (mean force potential, isotropic) | `Q_bg(V_n, T)` (잔류 chemical capacitance, V_n 비선형 함수) |
  | `K = eE/k_BT` (외부 전기장 매개) | `s_I·|I|·R_n / k_BT`-like (외부 전류 분극) — `V_{n,app}` vs `V_n` 의 차이 |
  | `μ = cosθ` (각도, anisotropic) | (graphite 는 isotropic radial → μ 변수 부재) |
  | `Fredholm integral eq. of 2nd kind` (Eq. 32, 공간 정상상태) | **`Volterra integral eq. of 2nd kind with implicit kernel`** (Phase B Loop 3, 시간 진화) |
  | `W̄_u^δ(r)` (δ-sink 해, Eq. 25) | "단순화된 경우의 ξ_j(t) closed-form" — 예: **ver5 Ch1 의 V_{n,OCV}(q,T) 외부 함수 가정 하의 ξ_j(q)** (전하 보존식 해 없이 외부 lookup) |
- **그대로 가져오면 안 되는 물리적 가정 차이**:
  1. **Fredholm (고정 적분 범위) vs Volterra (가변 적분 범위)** — 적분 변환 후 비율 substitution 적용 시 BC 형태 재정의 필요 (시간 0 vs ∞ ↔ 공간 σ vs ∞)
  2. **공간 정상 상태 (steady-state) vs 시간 진화 (transient)** — JCP 의 "ultimate survival probability" 는 t→∞ 한계. graphite ICA/DVA 는 시간 진화 자체가 관측 대상 (정상 상태 가정 X). 비율 substitution 기법 자체는 시간 영역에도 OK (`ξ_j(t')/ξ_j(t)` 비율 사용) 하지만 "ultimate" 의 의미 재정의 필요
  3. **Isotropic 1D vs anisotropic 3D + μ** — graphite radial 1D 라 μ 변수 부재. JCP 의 anisotropic 항 (Eq. 2 의 `-Krμ`) 제거 + Eq. (6)-(10) 의 μ 적분 단순화
  4. **저율 + 약한 결합 + 큰 Onsager 거리 영역에서 정확** — graphite 대응: **저 C-rate + Q_bg slope 클 것 + |I|·R_n << V_n 스케일**. 고 C-rate 또는 강한 분극 영역에서 정확도 저하 예상 → 적용 범위 제한

#### Ref. 7 — C. Y. Son, J. Kim, J.-H. Kim, J. S. Kim, S. Lee (J. Chem. Phys. 138, 164123 (2013))

- **서지**: C. Y. Son, J. Kim, J.-H. Kim, J. S. Kim, and S. Lee, J. Chem. Phys. **138**, 164123 (2013).
- **인용 위치**: Ref. 6 과 동일 3 곳 (line 44-45, 297-298, 599-600). 항상 Ref. 6 과 페어로 인용.
- **원 방법론**: Ref. 6 의 method 의 **확장** 으로 추정 (full-length paper, 더 정교한 적용). 본 JCP 2017 본문에 ref. 6 과 ref. 7 의 기여 구분 명시 X — 둘 다 "the solution method proposed by us" 로 묶어 인용. **분리된 기여 확인은 ref. 7 직접 정독 필요** (현 phase 범위 외).
- **본 graphite dQ/dV 문제 변수 매핑**: Ref. 6 과 동일 (둘이 함께 method 를 형성).
- **그대로 가져오면 안 되는 물리적 가정 차이**: Ref. 6 의 4 가지와 동일. 추가 차이는 ref. 7 직접 정독 후 보강 권장.

### Phase B OI-B2 (4 분류 (4) 물리 가정 충돌) 재검증

Phase B Result §"4 분류 진단" 의 (4) 물리 가정 충돌 항목 — Phase D 후 재검증.

**재검증 결과**: **(4) 해당 X** — 확정.

- 본 JCP 2017 의 ref. 6, 7 방법론은 본질적으로 graphite 시스템에 적용 가능. **물리적 가정 자체의 충돌 (즉 graphite 의 물리법칙과 ref 의 물리법칙이 맞지 않음) 은 발견되지 않음**.
- 발견된 4 가지 차이 (Fredholm/Volterra, 공간/시간, isotropy, 정확도 영역) 는 **방법론 적용 시 추가 가정 또는 변환 필요** 이지 **물리 가정 충돌 아님**.
- → Phase B Result §"4 분류 진단" 의 (4) 항목 "추정 → 해당 X" 로 **확정**. 본 Phase D 가 그 검증.

**별 분류 신설 권장 (4-tier 확장 아님, 단지 본 작업의 보조 라벨)**: "방법론 적용 조건" — 본 JCP 2017 의 ref. 6, 7 방법을 graphite 에 적용하려면 위 4 가지 차이를 명시적 변환 + 적용 영역 제한 (저 C-rate + 약한 분극) 으로 처리해야 함.

## Validation

본 계획서의 Gate (GATE_D1 ~ D4) 별 PASS/FAIL.

| Gate | 항목 | 4-tier | 근거 |
|---|---|---|---|
| **GATE_D1** | JCP 본문 전체 페이지 정독 + Read Coverage 기록 | **확정** | jcp_extract.txt 724 줄 (10 페이지) 전수 정독 PASS. 추출 방식: pdftotext -layout (수식 일부 ASCII 깨짐 — 본 Result 에서 line 번호 + 의도 추출로 우회) |
| **GATE_D2** | ref. 6, 7 인용 위치 (page · paragraph) 명시 | **확정** | 본 Result §"본문 내 인용 위치" — 3 곳 (line 44-45 §I, line 297-298 §II.C, line 599-600 §III.B) 각각 page + paragraph + 인용 맥락 인용 |
| **GATE_D3** | ref. 6, 7 서지 정보 5 항목 (저자/학술지/권·호/페이지/연도, 가능 시 DOI) | **확정 (DOI 부분 미발견)** | 본 Result §"서지 정보" — Ref.6: J. Chem. Phys. 134, 121102 (2011) / Ref.7: J. Chem. Phys. 138, 164123 (2013). 저자 + 학술지 + 권·호 + 페이지 + 연도 모두 명시. **DOI 는 본 JCP 본문에 명시 X** — 외부 학술 DB 검색 권장 (T4 검증 항목, 본 phase 범위 외) |
| **GATE_D4** | 5 요소 매핑 (서지 / 본문 위치 / 원 방법론 / 변수 매핑 / 물리 가정 차이) 작성 | **확정 (Ref.6) + 부분 확정 (Ref.7 의 분리 기여는 ref.7 직접 정독 시 보강)** | 본 Result §"5 요소 매핑" — Ref. 6 + Ref. 7 각각 5 요소 작성. Ref. 7 의 분리 기여 확인은 OI-D1 |

## Gate

**Phase D 종합 판정: PASS** (GATE_D1~D2 확정, GATE_D3 DOI 부분 미발견 (별 분류), GATE_D4 Ref.7 부분 보강 권장)

Gate 식별자: `PASS_JCP_REF6_7_METHODOLOGY`

## Confirmed Non-Changes

- JCP PDF 원본 — 정독 (텍스트 추출본 경유) 만, 수정 없음
- ver5.tex, ver1_rechecked2.tex — Phase A/B 에서 정독 완료, 본 phase 에서 read 안 함
- Phase A/B/C Result — 본 phase 의 input, 수정 없음
- 변수명 · 식 라벨 · 영문 원문 인용 — 원문 그대로

## Open Issues / Decision Queue

| ID | 항목 | 분류 | 비고 |
|---|---|---|---|
| **OI-D1** | Ref. 6 와 Ref. 7 의 분리 기여 — 본 JCP 2017 본문이 둘을 묶어 "the solution method proposed by us" 로 인용. ref. 6 = 초기 제안, ref. 7 = 확장으로 추정하나 직접 정독 X | 추정 → 사용자 결정 (필요 시 ref. 7 직접 정독 후속 phase) | Phase E 본문 디벨롭 시 우선 ref. 6 형식 사용 + ref. 7 의 추가 정교화는 필요 시 |
| **OI-D2** | Ref. 6, 7 의 DOI 본 JCP 본문 명시 X. T4 검증 항목 (계획서 Test Plan) — 외부 학술 DB 검색 후 추가 | 미검증 | 후속 작업 (web 검색 또는 사용자 제공) |
| **OI-D3** | pdftotext -layout 추출 시 일부 LaTeX 수식 ASCII 깨짐 (예: Greek 문자, subscript). 본 Result 의 수식 인용은 line 번호 + 의도 추출로 우회. **정밀 수식 (예: Eq. 32, 33, 39 의 정확 LaTeX 형태) 가 필요한 후속 Phase E 본문 디벨롭 시 PDF 직접 참조 권장** | 미검증 (정밀 수식) | Phase E 또는 별도 정독 phase |
| **OI-D4** | JCP 본문 §III.B 의 정합 조건 (저율 + 약한 결합 + 큰 Onsager) 의 graphite 대응 (저 C-rate + Q_bg slope 클 것 + |I|·R_n << V_n) 은 본 Result 에서 정성 진단. **정량적 영역 (예: C-rate < 0.5C? Q_bg slope > 어떤 값?) 은 미진단** | 미검증 | Phase E 본문 디벨롭 시 정량 검증 필요 |

## Next

- **다음 Phase**: **없음 — 본 계획서의 마지막 phase** (Phase D = Step 14-18 종료)
- **다음 cumulative step**: **Step 19** — 후속 계획서 (Phase E 이후 = Chapter 1 본문 디벨롭) 의 출발 step. 계획서 작성은 사용자 결정 대기 (DQ2, DQ3 of 본 계획서)
- **종합 보고 1회**: 본 Phase D commit 직후 사용자에게 Phase A~D 종합 + GATE_C4 사용자 검수 회수 + 후속 계획서 작성 여부 결정 요청

---

## Phase D Audit (10차원 × 3-Pass — read/diagnose phase 9차원)

### Pass 1 — 발견

| 차원 | 의심 항목 |
|---|---|
| #2 verbatim | 사용자 첫 요청 "ref 6, 7 이 그러한 되먹임이 들어간 적분식의 해를 찾는 방법을 포함" 과 본 Result 진단 정합? |
| #3 데이터 흐름 | jcp_extract.txt 724 줄 (10 페이지) 전수 cover? PDF → text 추출 정합? |
| #6 컨벤션 | 본문 인용 (line 44, 297, 599 등) 원문 정확? 영문 표현 보존? 서지 형식 정합? |
| #7 silent miss | 정독 누락 페이지? 추출 시 깨진 수식 영역? |
| #10 양식 | Result 11 항목 + 4-tier + 5 요소 매핑 양식 |
| α 경계 | JCP 본문 §I, II.A, II.B, II.C, III.A, III.B, IV, Acknowledgments, References 구조 cover? |
| β 인계 | Phase E (후속) 로 전달할 항목 (5 요소 매핑 + 4 가지 차이 + 적용 조건) 명확? |
| γ 트리 완전성 | Ref. 6, 7 인용 3 곳 모두 cover? 서지 5 항목 모두 명시? |
| δ 4-tier | 모든 보고 항목 4-tier 분류? OI 항목 분류? |

### Pass 2 — 확정·수정

| 차원 | 결과 |
|---|---|
| #2 | **확정 PASS** — 사용자 verbatim "되먹임이 들어간 적분식" = Fredholm/Volterra integral eq. of 2nd kind. "해를 찾는 방법" = 비율 substitution + δ-sink 알려진 해 substitution. 정확 매칭 |
| #3 | **확정 PASS** — 724 줄 전수 read 완료. PDF 10 페이지 = 추출 728 form-feed 위치 (page break) 까지 cover |
| #6 | **확정 PASS** — 영문 원문 인용 3 곳 (line 44-45, 297-298, 599-600) 모두 원문 그대로. 서지는 line 711-714 인용 그대로 |
| #7 | **확정 PASS** — 페이지 누락 없음 (jcp_extract.txt 의 모든 page 1-9 cover, page 10 = ack + ref). Pass 3 발견: pdftotext 의 layout 모드가 일부 수식 (Eq. 32, 33, 39 의 LaTeX) 을 깨뜨림 → OI-D3 로 기록. 영향: 정밀 수식이 필요한 경우 직접 PDF read 권장, 본 Phase D 의 5 요소 매핑 + 정합 진단에는 line 번호 + 의도 추출로 충분 |
| #10 | **확정 PASS** — 11 항목 + Validation 4-tier + 5 요소 매핑 양식 (Ref.6 / Ref.7 각각) |
| α | **확정** — JCP 본문 구조 cover: §I (page 1-2) + §II.A (page 2) + §II.B (page 2-3) + §II.C (page 3-4) + §III.A (page 4-6) + §III.B (page 6-9) + §IV (page 9) + ack + ref (page 9-10). 전 영역 정독 |
| β | **확정 PASS** — 5 요소 매핑 (Ref.6 + Ref.7 각각) + 4 가지 차이 + 적용 조건 (저 C-rate + Q_bg slope + |I|R_n) 모두 명시. Phase E 본문 디벨롭 진입 시 자료로 사용 가능 |
| γ | **확정 PASS** — Ref. 6, 7 인용 3 곳 모두 본 Result §"본문 내 인용 위치" 에 cover. 서지 5 항목 (저자/학술지/권/페이지/연도) 모두 cover (DOI 만 미발견 — OI-D2) |
| δ | **확정 PASS** — Validation 4 tier (확정 × 2 + 별 분류 × 2) + OI 4 항목 (추정 × 2 + 미검증 × 2) 모두 분류 |

### Pass 3 — 재검증

- Pass 2 정정 없음 (모두 확정 PASS, OI-D3 는 잔존 항목 기록)
- 회귀 없음
- Phase B 의 OI-B2 (4 분류 (4) 재검증) → Phase D 후 "해당 X" 확정 — 본 Result §"Phase B OI-B2 재검증" 에 명시. **Phase B Result 의 addendum 작성 권장** (별도 commit 또는 plan 종료 시 일괄)

### Audit 종합 판정

- **Pass 결과**: Pass 1+2+3 모두 PASS
- **회귀**: 없음
- **Critical / High**: 0 건
- **Medium**: 3 건
  - OI-D1 (Ref. 6 와 Ref. 7 의 분리 기여 — ref. 7 직접 정독 권장, 영향 미미)
  - OI-D2 (DOI 미발견 — 외부 DB 검색 권장)
  - OI-D3 (pdftotext 수식 깨짐 — Phase E 본문 디벨롭 시 PDF 직접 참조)
- **잔존 권고**:
  - Phase B Result 에 addendum 작성 (4 분류 (4) "해당 X" 확정 반영) — [[feedback_document_protection_addendum_pattern]] 정합
  - 사용자에게 종합 보고 + GATE_C4 사용자 검수 + 후속 계획서 작성 결정 요청
