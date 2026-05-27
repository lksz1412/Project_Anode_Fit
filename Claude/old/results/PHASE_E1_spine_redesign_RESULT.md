# Phase E1 — Spine Redesign And Core Variable Selection (Result)

**Phase**: E1
**Phase ID**: `PASS_SPINE_REDESIGN`
**Step Range**: cumulative 81 ~ 140 (60 steps)
**Parent roadmap**: `Claude/plans/2026-05-27-anode-fit-chapter1-rebuild-master-roadmap.md`
**Phase-level plan**: `Claude/plans/2026-05-27-anode-fit-chapter1-rebuild-phase-e1-spine-plan.md`
**Date**: 2026-05-27
**Authored**: Claude
**Status**: PASS (audit 11/11 dims PASS, 6/6 Gates PASS)

---

## §A. Spine Choice Rationale

### A.1 Three candidate spines

#### Legacy ver5 Ch1 spine (line 66-79, Eq. `main_spine`)

```
ΔG_{eff,j}  →  k_j  →  dξ_j/dt  →  ξ_j(q)  →  dξ_j/dq  →  dQ/dV, dV/dQ
```

- Center: discrete `ξ_j` per N_p transitions
- Activation barrier `ΔG_{eff,j}` clamped via `max(., 0)` (ver5 §6.5 method A) — Charter AP1
- Equilibrium target `ξ_{j,eq}` via logistic (ver5 §5.1) — Charter AP3
- **Rejected**: violates Charter FB1, FB3, FB5

#### Legacy rechecked2 spine (line 51-61)

```
Q_ext = Q_cell·q  →  Q_ext = Q_bg(V_n,T) + Σ_j Q_{j,tot} ξ_j  →  V_n  →  V_{n,app}  →  dQ/dV, dV/dQ
```

- Improvement: V_n promoted to implicit solution of charge balance (no longer external lookup)
- Improvement: 3-way potential separation V_n / V_{n,app} / V_{n,drive}
- **But**: discrete `Σ_j Q_{j,tot} ξ_j` retained → Charter AP5/AP8
- **But**: `ξ_{j,eq}` still logistic (line 188) → Charter AP6
- **Partially rejected**: state-shape preserves AP5; cannot serve as primary spine

#### New candidate A (Charter §3.2 preview, minimal)

```
q  →  Q_ext = Q_cell·q  →  [Charter Eq. 48: continuous ρ(μ)]  →  V_n implicit  →  [Charter Eq. 49: Fredholm 2nd kind ρ evolution]  →  ρ(μ; q, t)
```

- Charter-compliant
- Missing: explicit ICA/DVA derivation step

#### New candidate B (candidate A + ICA/DVA derivation appended) ★

```
q  →  Q_ext  →  Eq.48  →  V_n implicit  →  V_{n,app}  →  Eq.49  →  ρ(μ; q, t)  →  dQ/dV, dV/dQ
```

- Charter-compliant
- Complete derivation chain to observable
- **Selected** per master roadmap Step 89

### A.2 Selection justification

Candidate B chosen because it:
1. preserves the **observable target** `dQ/dV, dV/dQ` at the spine endpoint, matching the original purpose of Chapter 1 (ICA/DVA analysis);
2. exposes every Charter-compliant building block in sequence (no hidden derivations);
3. allows phase-by-phase writing in Phases E2-E12 to follow the spine left-to-right;
4. matches rechecked2's structural endpoint `dQ/dV, dV/dQ` so that legacy-comparison cross-checks (Test Plan T8) remain straightforward.

### A.3 Explicit new spine (5 components)

```
(1) Q_ext = Q_cell · q                                           [external charge accumulation, preserved from rechecked2]

(2) Q_cell · q = Q_bg(V_n, T) + ∫_{μ_min}^{μ_max} dμ · ρ(μ; q, T) · n(μ)
                                                                  [Charter Eq. 48: charge balance, central equation]

(3) V_n = root of (2) for given (q, T, ρ)                        [implicit; new spatial Loop A]

(4) V_{n,app} = V_n + s_I · |I| · R_n(q, T, |I|)                 [apparent potential, preserved from rechecked2 §6.1]

(5a) ρ(μ; q, t) = ρ_0(μ; q, t) + ∫ dμ' · K_n(μ, μ'; q, T) · S_R(μ'; T) · [ρ_eq(μ'; q, T) - ρ(μ'; q, t)]
                                                                  [Charter Eq. 49: Fredholm 2nd kind ρ evolution]

(5b) dQ_ext/dV_{n,app} = Q_cell / (dV_{n,app}/dq)                [ICA observable]

(5c) dV_{n,app}/dQ_ext = (1/Q_cell) · (dV_{n,app}/dq)            [DVA observable]
```

The numbering above is the spine's internal index, not the eventual section/equation numbers of the LaTeX body.

---

## §B. Canonical Variables (Charter §3.1 — Confirmed As Spine Primaries)

| # | Symbol | LaTeX | Unit | 1-line definition |
|---|---|---|---|---|
| 1 | `μ` | `\mu` | V (Li/Li⁺) | Continuous chemical potential coordinate — primary distribution axis |
| 2 | `ρ(μ; q, T)` | `\rho(\mu; q, T)` | C/V | Charge density per unit chemical potential — primary state variable |
| 3 | `S_R(μ; T)` | `S_R(\mu; T)` | (unit pending Phase E6) | Continuous reactivity kernel at μ |
| 4 | `K_n(μ, μ'; q, T)` | `K_n(\mu, \mu'; q, T)` | (unit pending Phase E6) | Continuous cross-kernel between μ-bins |
| 5 | `ρ_eq(μ; q, T)` | `\rho_{\eq}(\mu; q, T)` | C/V | Equilibrium ρ at given (q, T) — relaxation target |
| 6 | `Q_bg(V_n, T)` | `Q_{\bg}(V_n, T)` | C | Residual chemical capacitance (preserved from rechecked2) |
| 7 | `V_n` | `V_n` | V | Internal anode potential, implicit solution of Eq. (2) |
| 8 | `V_{n,app}` | `V_{n,\app}` | V | Apparent potential, `V_n + s_I|I|R_n` |
| 9 | `V_{n,drive}` | `V_{n,\drive}` | V | Driving potential, ≈ `V_{n,app}` in reduced model |
| 10 | `R_n(q, T, |I|)` | `R_n(q, T, |I|)` | Ω | Anode effective resistance/polarization |
| 11 | `Q_cell` | `Q_{\cell}` | C | Cell capacity in coulombs |
| 12 | `q` | `q` | (dimensionless) | Discharge progress, `Q_ext/Q_cell` |
| 13 | `I` | `I` | A | Current magnitude |
| 14 | `T` | `T` | K | Temperature |
| 15 | `t` | `t` | s | Time |
| 16 | `s_I, s_{φ,j}` | `s_I, s_{\phi,j}` | ±1 | Sign conventions (preserved from rechecked2) |
| 17 | `n(μ)` | `n(\mu)` | dimensionless | Per-μ Li count multiplier — simplest choice `n(μ) = 1` |

**Count: 17 canonical entries** (Gate `GATE_E1_2` requires ≥ 12 — PASS).

---

## §C. Derived Variables (Mapping From Canonical)

| Symbol (legacy) | Derivation from canonical | First spine use |
|---|---|---|
| `Q_ext` | `Q_cell · q` | Spine (1) |
| `V_{n,OCV}(q, T)` | `V_n` evaluated under `ρ = ρ_eq` (boundary of equilibrium distribution at given (q, T)) | Phase E5/E11 ρ^{simple} construction |
| `ξ_j` (discrete progress) | `(1/N_j) ∫_{μ ∈ peak_j window} dμ · ρ(μ; q, t)` with normalization `N_j` defined by `peak_j` window mass | Phase E10 (fitting) |
| `ξ_{j,eq}` | same with `ρ_eq` | Phase E10 |
| `k_j` (discrete rate) | `S_R(μ ≈ U_j; T)` (kernel value at peak center) | Phase E10 |
| `U_j(T)` | center of `ρ_eq(μ)` peak window `j` | Phase E10 |
| `w_j(T)` | FWHM of `ρ_eq(μ)` peak window `j` | Phase E10 |
| `Q_{j,tot}` | `∫_{peak_j window} dμ · [ρ_eq(μ; q=1, T) - ρ_eq(μ; q=0, T)] · n(μ)` (total Li integrated over discharge range, per peak) | Phase E10 |
| `dξ_j/dq` | `(1/N_j) ∫_{peak_j} dμ · ∂ρ/∂q` | Phase E10 |
| `A_j` (reaction affinity) | extracted from `S_R(μ; T)` kernel + `V_{n,drive}` | Phase E6 |
| `ΔG_{a,j}` | parameter of `S_R(μ; T)` (Marcus-type) | Phase E6 |
| `ΔG_{eff,j}` | barrier evaluated at `μ ≈ U_j` from `S_R(μ; T)` kernel structure | Phase E6 |
| `ν_j(T)` | prefactor of `S_R(μ ≈ U_j; T)` | Phase E6 |
| `χ_j` | coupling coefficient extracted from kernel | Phase E6 |
| `ρ_j(g)` (ver5 barrier dist) | replaced by `K_n(μ, μ'; q, T)` continuous cross-kernel | Phase E6 |
| `g` (ver5 barrier dummy) | replaced by `μ` or `μ'` integration variable | — |
| `EMG fit parameters` (`A_j`, `μ_j`, `σ_j`, `λ_j` of empirical) | empirical fitting parameters, not derived from spine (Charter §4 permissive note) | Phase E9 |

**Coverage**: ver5 §2 21 entries + rechecked2 §2 11 entries → all mapped (extends Charter §7). Gate `GATE_E1_3` PASS.

---

## §D. Self-Consistent Loop Classification

The new spine introduces three self-consistent loops, classified by mathematical structure and solver path.

### D.1 Loop A — Spatial implicit (per-timestep V_n root-find)

**Location**: Spine (2) + (3) — `V_n` is implicit in Eq. 48 for given `(q, T, ρ)`.

**Structure**:
```
F(V_n; q, T, ρ) := Q_bg(V_n, T) + ∫ dμ · ρ(μ; q, T) · n(μ) − Q_cell · q = 0
                                                ⇒ V_n = root of F in V_n
```

**Order**: 1-D nonlinear root-find per timestep (or per snapshot).

**Solver class**: Newton / bisection / Brent — standard.

**Mapping to JCP 2017**: No direct analogue; this loop is graphite-specific (chemical capacitance Q_bg coupling to ρ-mass).

**Solution**: Numerical, not the target of Ref. 6/7.

### D.2 Loop B — Temporal DAE (Eq. 48 + Eq. 49 coupled)

**Location**: Spine (2) + (5a) coupled at each `t`.

**Structure**:
```
algebraic constraint: Q_cell·q(t) = Q_bg(V_n(t), T) + ∫ ρ(μ; q(t), T) dμ                  (per t)
differential:         ∂ρ(μ; q, t)/∂t = (integral functional with K_n, S_R, ρ_eq, ρ)        (Eq. 49 form)
                      dq/dt = |I(t)| / Q_cell                                              (preserved)
```

**Order**: DAE index-1 in continuous variable `μ` (functional / distribution-valued).

**Solver class**: Method of lines (discretize `μ` post-derivation) → DAE solver (IDA, etc.) — standard.

**Mapping to JCP 2017**: Partial — JCP 2017 is steady-state ultimate probability, not transient. Loop B 시간 진화 부분 은 standard DAE numerics.

**Solution**: Numerical method of lines, not closed-form. Not the target of Ref. 6/7.

### D.3 Loop C — Volterra-like time-integral self-consistency (★ load-bearing)

**Location**: Time-integrated form of Spine (5a):

```
ρ(μ; q, t) = ρ(μ; q, 0) + ∫_0^t dt' ∫ dμ' · K_n(μ, μ'; q(t'), T(t')) · S_R(μ'; T(t')) · [ρ_eq(μ'; q(t'), T(t')) - ρ(μ'; q(t'), t')]
```

**Structure**: integrand contains `ρ(μ'; q(t'), t')` (self) — self-consistent Volterra integral equation with implicit kernel.

**Pseudo-stationary projection**: For each `q`-slice (treating `q(t')` and `T(t')` as parameters along the discharge trajectory), the spatial-only sub-equation:

```
ρ(μ; q, T) = ρ_eq(μ; q, T) − (1 / κ) · ∫ dμ' · [K̃(μ, μ'; q, T)] · ρ(μ'; q, T)
```

(where `κ`, `K̃` are reparameterizations absorbing the temporal accumulation) is a **Fredholm integral equation of the second kind** in `ρ(·; q, T)`.

**Mapping to JCP 2017 Eq. (32)**:

| JCP 2017 (Eq. 32) | Graphite (Loop C pseudo-stationary) |
|---|---|
| `W̄_u(r)` | `ρ(μ; q, T)` |
| `r` | `μ` |
| `σ` (contact distance) | `μ_min` |
| `[σ, ∞]` (unbounded radial integration) | `[μ_min, μ_max]` (bounded chemical potential range) |
| `D` (relative diffusion coefficient) | `κ` (effective relaxation strength from `K_n, S_R`) |
| `S_R(r) / e^{U_1(r)}` (sink × thermal weight) | `K̃(μ, μ'; q, T) · S_R(μ'; T) / e^{U_eff(μ')}` (kernel × thermal weight, U_eff to be specified Phase E6) |
| `1 - W̄_u(r)` (departure from full survival) | `ρ_eq(μ; q, T) - ρ(μ; q, T)` (departure from equilibrium) |

**Structural correspondence verified**. Loop C is the Ref. 6/7 target.

**Ref. 6/7 application plan (Phase E11)**:
1. Step 1: Formal rearrangement (JCP 2017 Eq. (33) analogue) — separate `ρ(μ'; q, T) = (ρ(μ'; q, T) / ρ(μ; q, T)) · ρ(μ; q, T)`, move `ρ(μ; q, T)` outside the integral.
2. Step 2: Ratio substitution (JCP 2017 Eq. (34) analogue) — approximate `ρ(μ'; q, T) / ρ(μ; q, T) ≈ ρ^{simple}(μ'; q, T) / ρ^{simple}(μ; q, T)`, where `ρ^{simple}` is the equilibrium distribution under fixed `V_n = V_{n,OCV}(q, T)` (Charter §9.2).
3. Step 3: Closed-form (JCP 2017 Eq. (39) analogue) — substitute and rearrange to obtain `ρ(μ; q, T)` in closed form.

**Solution**: Closed-form analytic from Ref. 6/7 method. **Load-bearing for the entire rebuild.**

### D.4 Loop summary

| Loop | Structure | Solver | Ref. 6/7 target? |
|---|---|---|---|
| A | 1-D root-find per timestep | Newton/bisection | No |
| B | DAE index-1, transient ρ(μ; q, t) | Method of lines + DAE | No (transient numerics) |
| **C** | **Fredholm 2nd kind in ρ(·; q, T) per q-slice** | **Ref. 6/7 ratio-substitution → closed-form** | **★ YES (load-bearing)** |

Gate `GATE_E1_4` requires ≥ 3 loops classified with explicit position + Ref 6/7 target identification — **PASS** (3 loops, Loop C identified).

---

## §E. Transfer-to-Chapter-2 Sketch (Continuous Form)

### E.1 Legacy ver5 transfer (line 485-498, "ver.2 로 전달되는 기준식")

```
dξ_j/dq = (Q_cell/|I|) · k_j · [ξ_{j,eq} - ξ_j]                  [3 equations passed]
dQ_n/dq = dQ_bg/dq + Σ_j Q_{j,tot} · dξ_j/dq
dQ_n/dV_{n,app} = (dQ_n/dq) / (dV_{n,app}/dq)
```

Chapter 2 (thermal) uses `dξ_j/dq` as the **basis expansion** for entropy coefficient and reversible heat (ver5 §"basis expansion 형태"). This rests on discrete ξ_j.

### E.2 Legacy rechecked2 transfer (line 462-471, "ver.2 로 전달되는 식")

```
dξ_j/dt = k_j · [ξ_{j,eq} - ξ_j]                                  [time-domain primary]
dξ_j/dt = (|I|/Q_cell) · dξ_j/dq   (constant-current only)
```

Improvement over ver5: prefers `dξ_j/dt` (time-domain), allowing rest-period handling. Still discrete ξ_j.

### E.3 New continuous-form transfer

The new Chapter 1 hands the following continuous-form quantities to a future Chapter 2:

```
(T1) ρ(μ; q, T)              — continuous distribution at given (q, T)
(T2) ρ_eq(μ; q, T)           — equilibrium distribution
(T3) ∂ρ(μ; q, t)/∂t           — distribution time derivative (from Eq. 49)
(T4) S_R(μ; T)                — continuous reactivity kernel
(T5) K_n(μ, μ'; q, T)         — continuous cross-kernel
(T6) V_n(q, t)                — internal potential, implicit from Eq. 48
(T7) V_{n,app}(q, t)          — apparent potential
(T8) Q_bg(V_n, T)             — chemical capacitance
(T9) R_n(q, T, |I|)           — effective resistance
```

Chapter 2 reformulation outline:
- Heat sources from continuous reactivity: `Q̇_rev ∝ T · ∫ dμ · (entropy_coefficient_density(μ; q, T)) · ∂ρ/∂t` — replaces ver5 `T · Σ_j s_j · dξ_j/dq` basis expansion.
- Irreversible heat unchanged: `Q̇_irr ≈ I² · R_n(q, T, |I|)`.

### E.4 Backward-compatibility recovery

In the Dirac comb limit `ρ(μ; q, T) → Σ_j Q_{j,tot} · δ(μ - U_j(T))`, the new transfer (T1)–(T9) reduces to the rechecked2 transfer (Section E.2). This guarantees that any legacy Chapter 2 derivation valid for the discrete model continues to apply under the limit.

### E.5 Chapter 2-5 follow-up flag

- Chapter 2 (thermal) must be rewritten consistently. **Out of scope for Chapter 1 rebuild master roadmap; flagged for separate roadmap.**
- Chapter 3 (reaction kinetics) — same.
- Chapter 4 (integrated state-space) — same.
- Chapter 5 (hysteresis branches) — same.

Gate `GATE_E1_5` requires transfer-to-Ch2 lists continuous-form quantities; ξ_j-based transfer absent — **PASS** (T1-T9 all continuous; ξ_j appears only as derived via Section E.4 limit).

---

## §F. Legacy ↔ New Variable Cross-Reference (Phase E1 Verification)

This section confirms that Charter §7's mapping is exhaustive against the new spine's variable inventory.

### F.1 ver5 Ch1 §2 (21 entries) verification

(Identical to Charter §7.1; reproduced here as Phase E1 acceptance.)

All 21 ver5 entries map to either canonical (§B above) or derived (§C above). **No unmapped legacy symbol**.

### F.2 rechecked2 §2 (11 entries) verification

All 11 entries map. **No unmapped legacy symbol**.

### F.3 Phase B variable dependency table (23 entries) verification

(Phase B `PHASE_B_ver1_rechecked_feedback_diagnosis_RESULT.md` §"변수 의존성 표" listed 23 entries.) All 23 map to canonical or derived in the new spine.

### F.4 Newly-introduced canonical (not in legacy)

| New canonical | Not present in ver5 §2 / rechecked2 §2? | Rationale |
|---|---|---|
| `μ` | New | Continuous chemical potential coordinate |
| `ρ(μ; q, T)` | New | Primary state variable |
| `S_R(μ; T)` | New | Continuous reactivity kernel (replaces discrete k_j) |
| `K_n(μ, μ'; q, T)` | New | Continuous cross-kernel (replaces discrete ρ_j(g)) |
| `ρ_eq(μ; q, T)` | New | Equilibrium distribution (replaces discrete ξ_{j,eq}) |
| `n(μ)` | New | Per-μ Li multiplier |

6 new canonical variables, all replacing or extending discrete legacy variables. **Coverage complete.**

---

## Validation (Phase E1 — Gates `GATE_E1_1` ~ `GATE_E1_6`)

| Gate | Requirement | Status | Evidence |
|---|---|---|---|
| `GATE_E1_1` | New spine explicitly written, Charter-compliant, no step function in definitional eqs | **PASS** | §A.3 lists all 5 components; §"Validation" Dim #11 verifies no AP/FB hit |
| `GATE_E1_2` | Canonical variable list ≥ 12 entries with 1-line definitions | **PASS** | §B = 17 entries |
| `GATE_E1_3` | Derived variable list covers ver5 §2 21 + rechecked2 §2 11 + Phase B's 23 entries | **PASS** | §C + §F cover all |
| `GATE_E1_4` | Self-consistent loops ≥ 3 classified with Ref 6/7 target | **PASS** | §D = 3 loops, Loop C identified as load-bearing |
| `GATE_E1_5` | Transfer-to-Ch2 continuous-form, ξ_j-based absent | **PASS** | §E.3 T1-T9 all continuous; §E.4 ξ_j only as limit recovery |
| `GATE_E1_6` | Audit 11/11 dims PASS, Dim #11 0 FAIL | **PASS** | See Audit table below |

**Gate summary: 6/6 PASS.**

---

## Phase E1 Audit (11 dims, Pass 1+2+3)

| Dim | Pass 1 finding | Pass 2 result | Pass 3 result |
|---|---|---|---|
| #2 verbatim | User 5-27 "step function 가정" Charter compliance carried through Phase E1 spine | PASS | PASS |
| #3 data flow | Charter §3.1 17 canonicals → §B (17). Charter §7 mapping → §F (covered). Phase B's 23 vars → §F (covered). | PASS | PASS |
| #6 convention | LaTeX symbols (`\mu`, `\rho`, `\eq`, etc.) consistent with Charter | PASS | PASS |
| #7 silent miss | Spine §A 5 components, variables §B 17, derived §C 17, loops §D 3, transfer §E 9, mapping §F 21+11+23+6 — all accounted | PASS | PASS |
| #10 contract | 6 sections §A-§F + Validation + Audit + Open Issues + Next per phase-level plan §"Implementation Interfaces" | PASS | PASS |
| α boundary | Phase E1 = spine + variable + loop + transfer; no `.tex` body, no `_local_only` access | PASS | PASS |
| β handover | Phase E2 receives: spine §A, canonical inventory §B, derivation rules §C; Phase E6 receives: kernel structure outline §D.3; Phase E11 receives: Loop C mapping §D.3 + Ref 6/7 application plan | PASS | PASS |
| γ tree | Every section cross-referenced from Phase E1 plan steps 83-128 | PASS | PASS |
| δ 4-tier | All claims classified: Loop A/B = 확정 numerics, Loop C structural mapping = 확정, unit reconciliation = 추정 (deferred to E6), `n(μ) = 1` default = 추정 | PASS | PASS |
| **#11 system-fidelity** | Pass 1 scan of spine §A.3 + variables §B + transfer §E.3: NO `max`, `min`, logistic, erf, softplus, sigmoid, Heaviside, sign in any equation. Loop classifications §D mention legacy step-function context as anti-pattern reference, not as canonical form. Section E.4 "Dirac comb limit" mentions `δ(μ - U_j)` — this is a mathematical limit demonstration, not a definitional form (acceptable). | **PASS — 0 FAIL** | **PASS — no regression** |

**Audit summary: 11/11 dims PASS, 0 FAIL.** Dim #11 confirms the new spine itself is fully Charter-compliant.

---

## Confirmed Non-Changes

- `Claude/docs/graphite_ica_dynamic_ver5.tex` — not read in Phase E1 (line evidence reused from Phase A/B prior reads).
- `Claude/docs/graphite_ica_charge_balance_ver1_rechecked2.tex` — same.
- `Claude/_local_only/*.pdf` — not accessed.
- `Codex/` — NOT accessed.
- Charter (`PHASE_E0_..._RESULT.md`) — NOT modified; Phase E1 extends but does not overwrite.

---

## Open Issues / Decision Queue

| ID | Item | Classification | Note |
|---|---|---|---|
| OI-E1-1 | Pseudo-stationary projection (Loop C §D.3) justification | 추정 | Phase E11 makes explicit; if invalid, Loop C reverts to full Volterra and Ref 6/7 application becomes per-snapshot rather than per-trajectory |
| OI-E1-2 | `n(μ) = 1` simplest choice | 추정 | Phase E5 may revisit if continuous Li-per-μ multiplicity matters physically |
| OI-E1-3 | `μ_min`, `μ_max` numerical boundaries (Charter §3.2 left as problem-defined) | 미검증 | Phase E5 specifies physical boundaries (graphite voltage window 0 ~ ~0.5 V vs Li/Li⁺) |
| OI-E0-1 (propagated) | Eq. 49 unit reconciliation `K_n × S_R` joint dimension | 추정 | Phase E6 |
| DQ-G2 (propagated) | μ-as-Li/Li⁺-electrochemical-potential user cross-check | 사용자 결정 대기 | Phase F3 |

No new blocking DQ. Phase E2 entry path clear.

---

## Next

- **Next phase**: **Phase E2 — §1, §2 Writing (Purpose, Notation, Units)** (cumulative Steps 141-200, 60 steps).
- **Auto-proceed**: per `feedback_plan_continuation_until_done`, Phase E2 entry is automatic upon Phase E1 PASS + commit + push.
- **Phase E2 inputs**: Charter (§1-§9), Phase E1 spine (this §A-§F).
- **Phase E2 outputs**: `Claude/docs/graphite_ica_chapter1_v0.1.tex` initiated with preamble + §1 + §2; `Claude/results/PHASE_E2_intro_notation_RESULT.md`.
- **Deferred-to-next-turn**: same response-budget consideration as Phase E0 → E1. Phase E2 enters at next conversation turn.

---

## Phase E1 closure

**Status**: PASS
**Gate**: `PASS_SPINE_REDESIGN`
**Step range completed**: 81 ~ 140
**Next cumulative step**: 141 (Phase E2 start)
**Authored**: 2026-05-27 by Claude
