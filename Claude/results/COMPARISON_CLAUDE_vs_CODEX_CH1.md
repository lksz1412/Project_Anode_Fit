# Chapter 1 비교: Claude v3 vs Codex (activation-barrier spectrum)

**Date**: 2026-05-28
**대상**:
- Claude: `Claude/docs/graphite_ica_chapter1.tex` (v3, ~810 lines)
- Codex: `Codex/results/graphite_ica_chapter1_activation_barrier_spectrum_v1.tex` (358 lines)
**근거**: 양쪽 본문 전문 정독 + Codex `PHASE_003_CH1_SPECTRUM_HANDOVER.md` + Claude `REVIEW_LEDGER_v3_CH1.md`

---

## §0. TL;DR

두 chapter 는 **같은 출발점**(activation barrier 는 state 를 0→1 로 점프시키는
threshold 가 아니라 rate constant 를 정하는 hidden variable; step-function 금지; relaxation
kinetics `dθ/dt=k(θ_e−θ)` with target/mobility 구분)을 공유한다. 그러나 **tail 의 핵심
메커니즘에서 갈린다**:

- **Claude v3** = transition 당 \*\*단일 relaxation length\*\* `ℓ_tail=|I|/(Q_cell k_j)`.
  tail = 단일 exponential lag envelope. 강점: grounding 엄밀(Assumption Ledger),
  사용자 PhD Refs 6/7 ratio-substitution 사용, **falsification + χ-discriminator**, charge-
  balance implicit V_n.
- **Codex** = \*\*relaxation-length spectrum 의 kernel integral\*\*
  `dΘ_tail/dQ ≈ ∫ A_L(L)(1/L)exp(−ΔQ/L)dL`. tail = 여러 mode 의 mixture → **stretched
  (non-exponential) tail** 자연 발생. 강점: stretched tail 설명력, equilibrium 형태
  미확정(보수적).

★ **결정적 사실**: Codex 는 자기 초기 버전(single tail-length 모델)을 **명시적으로
폐기**하고 spectrum 으로 전환했다 (handover: "prior version centered too much on a single
active-barrier/single-tail-length model"). 그런데 **Claude v3 의 tail 식이 정확히 그 single
tail-length 모델**이다. 즉 Codex 는 Claude 가 선 지점을 한 단계 더 지나갔다 — 단,
그 과정에서 Claude 가 갖춘 rigor 요소들(PhD 방법·falsification·grounding tier)을 갖추지
않았다.

---

## §1. Architecture 대조

| 축 | Claude v3 | Codex |
|---|---|---|
| 본문 규모 | ~810 lines, 13 sections, 14 derivation blocks | 358 lines, 9 sections |
| 참고문헌 | 20 (Eyring, Evans-Polanyi, Marcus, Bard-Faulkner, McKinnon-Haering, Bazant, Dahn, Ohzuku, de Groot-Mazur, Onsager, Plonka, Lee2011, Son2013, Doyle-Fuller-Newman, Newman, Bässler, Dubarry, Fly, Asenbauer) | 5 (Dahn, Funabiki, Eyring×2, Bazant) |
| Grounding 체계 | Assumption Ledger AL-1~10, GROUNDED/BOUNDED/FLAGGED tier | 본문 내 인용, 별도 tier 체계 없음 |
| Equilibrium isotherm | lattice-gas `μ(ξ)` GROUNDED baseline (smooth) + erf FLAGGED | `θ_e(φ,T)` **형태 미지정 (일반)** — 더 보수적 |
| V/전위 결정 | charge-balance implicit `V_n` (DFN grounded) + 3-potential 구분 | `φ` analysis potential 직접 사용, ICA mapping `dQ/dφ=C_b/(1−Q_p dΘ/dQ)` |
| Effective barrier | `ΔG_eff=ΔG_a−χ𝒜`, **Marcus-bounded** | `k=k_0 exp(−(G−W_ψ)/RT)`, `W_ψ=Λ_ψFψ` (Marcus 언급 없음) |
| ★ Tail 메커니즘 | **단일** kinetic lag, `ℓ_tail=|I|/(Q_cell k_j)` (exponential) | **spectrum** kernel integral (stretched) |
| 사용자 PhD Refs 6/7 | **사용** (Volterra + ratio-substitution closed-form, load-bearing) | **미사용** (Refs 6/7 부재) |
| Falsification | **전용 §11** + χ-discriminator + N1-N4 null rules | **없음** (해석만, competing-source 배제 절차 없음) |
| Step-function 금지 | 명시 (max/min/Heaviside 정의식 0) | 명시 (`θ=H(G_c−G)` 금지) |
| 검토 | 10-round (3 독립 agent + self), 11 fix | 10-pass logic review (자체) |

---

## §2. ★ 핵심 분기: tail 메커니즘

### Codex (spectrum)
- single local mode: `dr/dQ + (k/v_Q)r = dθ_e/dQ` → post-peak (`dθ_e/dQ≈0`) 에서
  `r∝exp(−(Q−Q_a)/L)`, `L=v_Q/k`. (= Claude 의 단일 mode 와 동일)
- ★ barrier→rate→length 매핑: `L(G)=(v_Q/k_0)exp((G−W_ψ)/RT)`. barrier 의 작은 분산이
  length 에서 **지수적으로 확대** → stretched tail.
- ★ 중심식: `dΘ_tail/dQ ≈ ∫₀^∞ A_L(L)(1/L)exp(−(Q−Q_a)/L)dL` (relaxation-length
  spectrum 의 mixture).
- T·ψ 의존: low T → exp factor↑ + k_0↓ → spectrum 이 large-L 로 이동 → long tail.
  ψ>0 → `W_ψ`↑ → short-L 로 이동 → short tail (`∂lnL/∂ψ=−Λ_ψF/RT`).

### Claude v3 (single length)
- 동일 single-mode 출발: `dΔ/dq + (Q_cell k/|I|)Δ = dξ_eq/dq`; post-peak 에서
  `Δ∝exp(−(Q−Q_0)/ℓ_tail)`, `ℓ_tail=|I|/(Q_cell k_j)`.
- tail = transition 당 **하나의** exponential envelope. stretched-ness 는 AL-6
  (barrier distribution) 로 **옵션** 처리 (비유일 매핑 경고와 함께 demote).

### 평가
- **관측 tail 이 genuinely stretched (non-exponential) 이면 Codex 의 spectrum 이 더
  적합**하다. 실제 graphite tail 은 단일 지수보다 늘어진(stretched) 경우가 많아, Codex 의
  방향이 현상에 더 부합할 여지가 크다.
- **단 Codex spectrum 의 약점**: barrier→length inverse mapping 이 **non-unique**
  (Plonka; 동일 stretched tail 을 무수한 `ρ_G` 가 재현). Codex 는 "observed tail ≠ ρ_G
  shape" 라고 일부 인지하나, 이 non-identifiability 를 falsification/제약으로 닫지 않는다.
  Claude 는 이 점을 AL-6 에서 명시 경고했으나 메커니즘 자체를 옵션으로 미룸.
- 즉 **Claude = 단일 length (검증 가능하나 stretched 설명 약함)** vs
  **Codex = spectrum (stretched 설명 강하나 non-unique·미검증)**. 상보적.

---

## §3. 각자가 강한 곳

### Claude v3 가 강한 곳
1. **Grounding 엄밀성**: Assumption Ledger + GROUNDED/BOUNDED/FLAGGED tier. 사용자
   5-28 표준("모든 가정 문헌/이론 근거; 없으면 flagged")에 더 직접 부합.
2. **사용자 PhD Refs 6/7 사용**: ratio-substitution / propagator 를 Volterra closed-form
   에 적용 (load-bearing). 사용자가 핵심 도구로 지목한 자기 연구 — Codex 는 전혀 미사용.
3. **Falsification + χ-discriminator**: competing tail source(R_n/transport/disorder)
   배제 절차 + 비퇴화 판별(χ-의존 Arrhenius slope, |I|-scaling 퇴화 명시) + N1-N4 null
   rules. 논문 referee 방어력. Codex 에는 부재.
4. **Charge-balance implicit V_n** (DFN grounded) + 3-potential 엄밀 구분.
5. **Marcus bound** (선형 lowering 의 유효범위 명시).

### Codex 가 강한 곳
1. **Stretched tail 설명력**: spectrum kernel integral 이 늘어진 tail 을 자연 산출.
   single-length 한계를 스스로 인지하고 넘어섰다.
2. **Equilibrium 형태 미확정 (보수)**: `θ_e` 를 특정 형태로 안 박음 → 사용자 정정
   ("가우시안은 예시, 형태 미확정")과 잘 맞음. Claude 는 lattice-gas 를 baseline 으로
   commit (단 flagged 로 hedge).
3. **간결성·가독성**: 358 lines 로 핵심 chain 이 선명. Claude 는 rigor 대가로 길다.
4. **barrier→length 지수 확대**라는 stretched 의 정량적 근원 제시 (Claude 에 없는 통찰).

---

## §4. 사용자 의도 정합성

| 사용자 의도 | Claude v3 | Codex |
|---|---|---|
| activation barrier 유지 (5-28) | ✅ 중심 | ✅ 중심 |
| step-function 0→1 점프 금지 | ✅ | ✅ (명시적, 깔끔) |
| "가우시안"=예시, 형태 미확정 | ✅ (lattice-gas baseline+flag) | ✅ (θ_e 일반, 형태 무지정 — 더 부합) |
| 모든 가정 grounded (5-28) | ✅✅ (Ledger tier) | △ (인용 있으나 tier 체계 없음) |
| 사용자 PhD Refs 6/7 활용 | ✅✅ | ❌ 미사용 |
| 논문급 무비약·falsification | ✅✅ (falsification §) | △ (해석 충실하나 falsification 부재) |
| 꼬리 늘어짐(stretched) 설명 | △ (단일 지수; 분포는 옵션) | ✅✅ (spectrum) |

---

## §5. 종합 권고 (synthesis)

두 chapter 는 **경쟁이 아니라 상보**다. 이상적 Chapter 1 = **Codex 의 relaxation-length
spectrum (stretched tail) + Claude 의 rigor 3종(① grounding tier ② 사용자 PhD Refs 6/7
③ falsification+χ-discriminator) + charge-balance V_n**.

특히 주목할 합류점: 사용자 PhD Refs 6/7 (propagator / integral-equation 기법)는 Codex 의
**kernel integral `∫A_L(L)(1/L)exp(−ΔQ/L)dL` 를 엄밀히 닫는 바로 그 도구**가 될 수 있다.
즉 Codex 의 spectrum 적분에 Claude 가 가진 사용자 PhD 방법을 적용하면, "stretched tail =
relaxation-length spectrum 의 propagator-closed kernel integral" 이라는 **두 접근의 자연
통합**이 가능하다.

### 결정 포인트 (사용자)
1. tail 을 **단일 length (Claude)** 로 둘지 **spectrum (Codex)** 로 둘지 — 핵심은 관측
   tail 이 genuinely stretched 인지. (저속 OCV/dQ-dV 의 tail 이 단일 지수인지 stretched
   인지 실측이 판별.)
2. 통합본을 만들지 (spectrum + rigor + Refs 6/7), 아니면 한쪽을 정본으로 갈지.
3. Codex 가 누락한 falsification·Refs 6/7·grounding tier 를 Codex 본에 이식할지.

---

## §6. 한 줄 결론
- **현상 적합성 (stretched tail)**: Codex 우세 (spectrum).
- **rigor·사용자 PhD 방법·falsification·grounding**: Claude 우세.
- **최선**: Codex 의 spectrum 골격 위에 Claude 의 Refs 6/7 closed-form·falsification·
  Assumption Ledger 를 얹는 통합. (단일 length 인 Claude v3 는 Codex 가 이미 넘어선
  지점이므로, 통합 시 Claude 의 tail 식은 spectrum 의 single-mode kernel 로 재배치.)
