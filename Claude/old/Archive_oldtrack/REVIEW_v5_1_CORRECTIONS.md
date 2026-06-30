# Review & Corrections: graphite_ica_chapter1.tex v5 → v5.1

**Date**: 2026-05-29
**Trigger**: 사용자 지적 — "코덱스는 뭔가 문제가 있다고 확인했는데? 너는 없냐? 검수안해 봤어??"
(직전 비교 문건들이 Codex 의 정당한 지적을 "fork(취향 차이)"로 축소한 complacency 를 사용자가 정확히 포착.)
**대상**: `Claude/docs/graphite_ica_chapter1.tex` (v5 merged canonical → v5.1 corrected)
**근거**: 본문 전수 정독 + 적대적 재검수 + Codex `PHASE_012_..._DUAL_CLOSURE_COMPARISON.md` 대조

---

## §0. 결론
v5 는 "~98% 수렴" 이 아니라 **실제 결함 4건(확정) + 노출결함 1건 + minor 1건**을 안고 있었다.
이 중 2건은 Codex 가 이미 지적했고(내가 축소함), 2건은 본 검수에서 추가로 발견(물리 결함 포함),
1건은 적대 검수가 "수학적 모순"으로 과장한 것을 "노출 결함"으로 정정. 전부 v5.1 에서 수정.

---

## §1. 확정 결함과 수정 (CONFIRMED)

### C1. §closure 가 P1 위반 — numerical solver / validator / ε-switch 워크플로우 [Codex 지적·맞음]
- **증상(v5)**: Plan B 가 "식 eq:volterra_self 를 *direct numerical integration* 으로 평가 …
  numerically exact reference … Plan A 의 **validator**"; M5 = `ε=‖Θ_A−Θ_B‖/‖Θ_B‖≤ε_tol`
  (Θ_B = direct numerical 해). → 이론 chapter 가 검증 파이프라인으로 드리프트.
- **P1 위반**: "피팅 솔버·수치검증 워크플로우 구축은 Chapter 1 범위 외".
- **수정(v5.1)**:
  - Plan B → "자기완결적 **reduced analytic theory** (B1–B3); 핵심 physical conclusion 은
    spectrum integral 로부터 **해석적으로** 따라 나옴". numerical-validator/numerically-exact
    문구 삭제. self-consistent Θ(q) 의 정량 평가는 "fitting/구현 단계 영역 (P1 외)".
  - M5: "정량 오차 ε" → "**limiting-case 해석적 일치**" (단계 0 controlled-approximation 극한에서
    Plan A → Plan B B1–B3 로 해석적 환원, 차이는 근사 파라미터로 bounded). 정량 ε 측정은 P1 외.
  - governance 요약문(L537)·abstract·spine·summary·grounding-audit 의 "ε"/"validator" 잔재 전부 정리.

### C2. Refs 6/7 과중심 — 문서 내부 자기모순 [Codex 지적·맞음]
- **증상(v5)**: §phd 제목 "(Refs 6/7) = kernel integral 의 closure", 본문 "본 Chapter 의
  **load-bearing 수단**" — 그러나 R5 는 "**mathematical method candidate** (M1–M5 gated)".
  같은 문서가 정의(definitive) ↔ 후보(candidate) 로 모순.
- **수정(v5.1)**:
  - §phd 제목 → "**candidate analytic closure method**". 본문 "load-bearing 수단" →
    "candidate analytic method (Plan A); M1–M5 통과 시에만 승격; Chapter 논리 core 는 항상 Plan B".
  - eq:closed 주변 "Codex 측 operator 의 실현" 삭제, "candidate; M1–M5 미통과 시 core 는 Plan B" 명시.
  - R5 에 "dual hierarchy = coding/solver 분기 아닌 **논리적 책임 분리** (물리 core=Plan B,
    analytic convenience=Plan A)" 추가 (Codex R5 강점 흡수).

### C3. eq:spectrum 의 A_0 double-counting [본 검수 추가 발견 — 물리 결함, Codex 도 미포착]
- **증상(v5)**: `A_L = ρ_G(G(L))·(RT/L)·A_0`, 그런데 `A_0` 정의 = "initial residual amplitude
  ·**population weight**·accessibility". population(개수)은 이미 `ρ_G` + Jacobian `RT/L` 이
  담으므로 `A_0` 에 population 을 또 넣으면 **이중 계상**.
- **수정(v5.1)**: A_0 ≡ **mode 당 amplitude** (r(q_a) × capacity weight w^Θ × accessibility)
  **뿐**; population 은 ρ_G(+Jacobian)이 담으므로 A_0 에서 제외 (double counting 방지) 명시.

### C4. provenance 누출 (manuscript 본문에 작업 메타데이터) [본 검수 + Codex §3]
- **증상(v5)**: L398 "(Codex 산출물과의 대조에서 채택한 spectrum 관점)", L484 "Codex 측
  abstract operator C_ratio 의 명시적 실현" 이 렌더링 본문에 노출.
- **수정(v5.1)**: 둘 다 중립 표현으로 교체/삭제. (header `%` 주석의 provenance 는 비렌더링이라 유지.)

---

## §2. 노출 결함 (적대 검수가 "모순"으로 과장 → 정정) — 환각/판단오류 구분

### E1. eq:kernel_integral 의 `1/L` 이 eq:single_kernel 과 "모순"? → **아님 (노출 결함만 맞음)**
- 적대 검수 주장: single_kernel 에는 `1/L` 이 없는데 kernel_integral 엔 있어 정규화 불일치.
- **정정(사실)**: single_kernel 은 residual `r` 의 감쇠, kernel_integral 은 progress rate
  `dθ/dq`. `r=θ_eq−θ`, `dθ_eq/dq≃0` 에서 `dθ/dq=−dr/dq=r/L=(r(q_a)/L)exp[−(q−q_a)/L]` —
  `1/L` 은 **미분에서 정당하게** 나온다. 수학적 모순 아님.
- **단, 노출 결함은 맞음**: v5 가 이 한 줄 유도를 빠뜨려 독자가 외견상 불일치로 오독 가능.
- **수정(v5.1)**: §kernel 에 **Derivation D7b** 추가 (dθ/dq = r/L 유도 명시) → `1/L` 근거화,
  외견상 불일치 해소.

---

## §3. Minor

### M-ica. eq:ica 유도 압축 + peak singularity 무주석
- **수정(v5.1)**: chain-rule 단계 `dΘ/dV_n=(dΘ/dQ)(dQ/dV_n)` 명시 삽입; "ICA peak = 분모
  `1−Q_p(dΘ/dQ)` 가 작아지는 영역 (smooth 감소; step jump 아님; reduced regime 서 bounded)" 주석 추가.

---

## §4. v5.1 에서 손대지 않은 것 (의도적 보존)
- 물리 core (charge-balance implicit V_n, effective barrier ΔG_eff=ΔG_a−χA, Eyring rate,
  lattice-gas 특수해, barrier→length 지수 매핑, falsification + χ_j/η_ct co-linearity, N1–N4).
- Plan A concrete eq:closed 자체 (사용자 "1안 우선 + PhD 방법 적용" 의도 충족) — 단 candidate 로 격하.
- AL-# grounding tier, Assumption Ledger 연계.

## §5. 후속
1. ~~v5.1 재검수~~ → 완료 (§6).
2. Codex v3 와 재대조 (이번엔 결함을 결함으로 — 수렴률 수치 자제).
3. LaTeX 빌드 검증 (사용자: xelatex+kotex / Overleaf).

---

## §6. 적대적 재검수 결과 (v5.1, 2026-05-29) → MINOR-REVISION → 반영 완료

C1–C4·D7b·eq:ica 수정이 본문에서 실제로 성립함을 확인 (LaTeX 무결: 15 cite/모든 eqref·ref
resolve, 중복 label 없음; ε/validator/Codex/load-bearing/"direct numerical" 잔재는 `%` 주석
라인에만 — 렌더 본문 clean; max/min/Heaviside 는 전부 "금지" 절에만). 잔여 지적 처리:

- **[HIGH→해소] D1: spectrum integral 의 1/L² 가 double-count 아닌가?**
  - **자체 유도로 확인**: 1/L 두 개는 출처가 다르다 — (i) kinematic `dθ/dq=r/L` (D7b),
    (ii) Jacobian `RT/L` 의 `ρ_G dG→dL` 변수변환. 1/L² 은 의도된 것이며 정상. (1/L 을 무턱대고
    제거했으면 오히려 실제 버그를 주입할 뻔 — 환각/판단오류 구분 차원에서 자체 재유도가 핵심이었음.)
  - **차원**: L 은 무차원(q-단위) → ρ_G[1/(J/mol)]·(RT/L)[J/mol]·A_0[무차원] = 무차원 density,
    ∫A_L dL = 무차원 amplitude weight. 일관.
  - **반영(N1)**: §kernel 에 "두 1/L 의 출처" 명시 절 추가.
- **[HIGH→해소] D2: A_L 정체성 이중 서술 (population density vs amplitude-weighted)**
  - **반영(N2)**: notation 표의 A_L = "amplitude-weighted density; ∫A_L dL=총 amplitude
    weight" 로 통일, A_0 행 신설 (population 은 ρ_G 가 담음 명기).
- **[MEDIUM→해소] D3: §fitting deliverable 에 eq:closed 가 gated caveat 없이 "the closure" 로 노출**
  - **반영(N3)**: "Plan A candidate; M1–M5 gated; 미통과 시 Plan B kernel integral" caveat 삽입.
- **[LOW] D4 (A_0 notation 누락) → N2 로 동시 해소. D5 (abstract 줄바꿈) = 사용자 한글+영어
  혼용 스타일이라 결함 아님, 보존.**

**재검수가 정정한 점(환각 방지)**: 적대 검수의 "1/L 모순/double-count" 표현은 *수학적 결함이
아니라 노출/정규화 서술 부족*. 자체 재유도로 1/L² 정당성 확인 후 expository 보강만 적용 (수식
불변). 적대 검수도 E1(저자의 1/L 단일-mode 추론)이 옳다고 최종 인정.

**v5.1 최종 상태**: P1 정합(solver/numerical-validation 워크플로우 제거) · Refs 6/7 candidate
gated · Plan B core · A_0 double-count 해소 · 1/L 정규화 명시 · provenance 제거 · LaTeX 무결.
