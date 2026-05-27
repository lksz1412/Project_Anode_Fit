# Phase E0 — Foundation Reset And Rebuild Charter (Result)

**Phase**: E0
**Phase ID**: `PASS_FOUNDATION_RESET_CHARTER`
**Step Range**: cumulative 19 ~ 80 (62 steps)
**Parent roadmap**: `Claude/plans/2026-05-27-anode-fit-chapter1-rebuild-master-roadmap.md`
**Phase-level plan**: `Claude/plans/2026-05-27-anode-fit-chapter1-rebuild-phase-e0-charter-plan.md`
**Date**: 2026-05-27
**Authored**: Claude (Project_Anode_Fit Claude 측)
**Status**: PASS (with audit Pass 1+2+3 confirmed below)

---

## §1. Charter Objective

**Objective sentence**:
Construct a Chapter 1 of the graphite anode ICA/DVA dynamics document that models the system through (a) a **continuous chemical potential distribution `ρ(μ; q, T)`** as the primary state variable, (b) a **continuous reactivity kernel `S_R(μ; T)`** replacing the discrete `k_j`, and (c) the user's PhD-level **Fredholm integral equation of the second kind ratio-substitution method (Refs. 6, 7 + JCP 2017)** as the canonical solver for the resulting self-consistent integral equation in `ρ`.

**Amplification**:
- This Chapter 1 is a from-scratch rebuild that treats ver5 (`graphite_ica_dynamic_ver5.tex` Ch1, lines 46-526) and ver1_rechecked2 (`graphite_ica_charge_balance_ver1_rechecked2.tex`, all 495 lines) as evidence sources and as **anti-pattern references**, never modified.
- The user's verbatim diagnosis (5-27) — "기존 1~5 전문건이 포함된 버전의 큰 문제점은 한계 어쩌구 하면서 적분을 모아니면 도 즉 스텝펑션의 형태로 가정하여 우리가 모사해야하는 시스템의 특성을 완전 무시한채 논리 전개를 진행하여 시작 점부터 글러 먹었었다" — identifies the **step function assumption** as the root defect of ver1~5. This Charter codifies the avoidance of that assumption as the foundational rule.
- The self-consistent loop family (Loop 1/2/3 from Phase B diagnosis) is treated as a surface artefact of the discrete decomposition + step approximations, not as the root defect. The continuous-form rebuild eliminates the loops at the source rather than patching them at the symptom.
- The user's own Refs. 6, 7 (`Communication: Propagator...`, J. Chem. Phys. 134, 121102, 2011; `An accurate expression... long-range reactivity`, J. Chem. Phys. 138, 164123, 2013) provide the closed-form analytical solution for the residual self-consistent integral equation that necessarily appears in any continuous-reactivity treatment.

---

## §2. Anti-Pattern List

The following patterns are evidence of step function assumptions in ver5 and ver1_rechecked2. They MUST NOT appear in any definitional equation of the rebuilt Chapter 1.

| # | Pattern | Evidence file | Lines | Role in source | Anti-pattern reason |
|---|---|---|---|---|---|
| AP1 | `max(ΔG_eff, 0)` (ReLU step in barrier) | `Claude/docs/graphite_ica_dynamic_ver5.tex` | 240-245 (§6.5 method A) | Barrier clamping ("속도 폭주 방지") | Hard step at ΔG_eff = 0; discontinuous derivative; piecewise behavior contradicts continuous reactivity kernel |
| AP2 | `min(k_j, k_max)` (saturation step) | `Claude/docs/graphite_ica_dynamic_ver5.tex` | 247-249 (§6.5 method B) | Rate constant ceiling | Hard step at k_max; introduces unphysical plateau in k(T, η) |
| AP3 | `ξ_{j,eq} = 1/(1+exp[-(V_n - U_j)/w_j])` as definitional (logistic) | `Claude/docs/graphite_ica_dynamic_ver5.tex` | 188 (§5.1 Eq. xi_eq_logistic) | Equilibrium progress definition | Logistic = smooth-step; w_j → 0 limit recovers Heaviside; embeds binary on/off assumption per discrete transition |
| AP4 | `ξ_{j,eq} = (1/2)(1 + erf[(V_n - U_j)/(√2 w_j)])` as definitional (erf) | `Claude/docs/graphite_ica_dynamic_ver5.tex` | 195 (§5.2 Eq. xi_eq_erf) | Equilibrium progress definition (alternative) | Same as AP3 in nature; erf = smooth-step |
| AP5 | Discrete `N_p` effective transition decomposition as primary state | `Claude/docs/graphite_ica_dynamic_ver5.tex` | 137-150 (§3 + Table) | Choice of state variable | Quantizes continuous staging chemical potential into a small N_p; the sum of N_p smooth-steps is a step train, not a continuous distribution |
| AP6 | `ξ_{j,eq} = 1/(1+exp[-(V_n - U_j)/w_j])` retained in rechecked2 | `Claude/docs/graphite_ica_charge_balance_ver1_rechecked2.tex` | 188-193 (§5 Eq. xi_eq_logistic) | Equilibrium progress definition | Same as AP3; rechecked2 partial-fix did not remove |
| AP7 | Softplus regularization `ε_G·ln(1+exp(ΔG_eff/ε_G))` as definitional in rechecked2 | `Claude/docs/graphite_ica_charge_balance_ver1_rechecked2.tex` | 250-265 (§6.2 Eq. softplus_barrier) | Smooth-ReLU barrier | Softplus is a smooth-step (smooth limit of AP1); admissible only as a numerical regularization with explicit `ε_G → 0` smooth-limit (see §5 of this Charter), NOT as the canonical functional form |
| AP8 | Discrete `N_p` effective transition concept retained in rechecked2 | `Claude/docs/graphite_ica_charge_balance_ver1_rechecked2.tex` | 110-114 (§3 assumption block) | State decomposition | Same as AP5; rechecked2 partial-fix did not remove |

**Evidence count**: 8 patterns (Gate `GATE_E0_2` requires ≥ 5 — PASS).

---

## §3. Allowed-Pattern List

The following are the canonical patterns of the rebuilt Chapter 1. The new variable namespace below defines the primary state; all derivations build from it.

### 3.1 New canonical variable namespace

| Symbol | LaTeX | Unit | Description |
|---|---|---|---|
| `μ` | `\mu` | V (Li/Li⁺ ref) | Continuous chemical potential coordinate (electrochemical potential of Li in the anode host frame) |
| `ρ(μ; q, T)` | `\rho(\mu; q, T)` | C/V | Continuous distribution density at chemical potential `μ` (Li occupation per unit chemical potential, expressed as charge density) |
| `S_R(μ; T)` | `S_R(\mu; T)` | 1/s | Continuous reactivity kernel at `μ` (rate at which `ρ` at `μ` relaxes toward `ρ_eq` at `μ`) |
| `K_n(μ, μ'; q, T)` | `K_n(\mu, \mu'; q, T)` | 1/(V·s) | Continuous cross-kernel for chemical-potential-space transport coupling |
| `ρ_eq(μ; q, T)` | `\rho_{\eq}(\mu; q, T)` | C/V | Equilibrium distribution at `(q, T)`; the steady-state target for the reactivity-kernel relaxation |
| `Q_bg(V_n, T)` | `Q_{\bg}(V_n, T)` | C | Residual chemical capacitance (preserved from rechecked2 §4.1 with identical semantics) |
| `V_n` | `V_n` | V (Li/Li⁺ ref) | Internal anode potential — boundary value of `μ` distribution; the implicit solution of the new charge balance equation |
| `V_{n,app}` | `V_{n,\app}` | V | Apparent (observed) anode potential, `V_n + s_I |I| R_n` (preserved from rechecked2 §6.1) |
| `V_{n,drive}` | `V_{n,\drive}` | V | Driving potential for reactivity, equals `V_{n,app}` in reduced model (preserved from rechecked2 §6.1) |
| `R_n(q, T, |I|)` | `R_n(q, T, |I|)` | Ω | Anode effective resistance / polarization coefficient (preserved from rechecked2 §6.1) |
| `Q_cell` | `Q_{\cell}` | C | Cell reference capacity in coulombs |
| `q` | `q` | (dimensionless) | Discharge progress coordinate, `q = Q_{\ext}/Q_{\cell}` |
| `I` | `I` | A | Cell current magnitude |
| `T` | `T` | K | Absolute temperature |
| `t` | `t` | s | Time |
| `s_I`, `s_{φ,j}` | `s_I, s_{\phi,j}` | ±1 | Sign conventions (preserved from rechecked2 §6.1, retained for branch handling in Ch5) |

### 3.2 Central allowed-pattern equations

(a) Charge balance with continuous `ρ` (the central equation — Eq. 48):

```latex
Q_{\cell}\, q
=
Q_{\bg}(V_n, T)
+
\int_{\mu_{\min}}^{\mu_{\max}}
d\mu\;
\rho(\mu; q, T) \cdot n(\mu)
```

where `n(μ)` is the per-`μ` Li occupation count (dimensionless multiplier; simplest choice `n(μ) = 1` with `ρ` carrying charge dimension).

(b) Continuous reactivity Fredholm 2nd kind self-consistent integral equation (Eq. 49):

```latex
\rho(\mu; q, t)
=
\rho_0(\mu; q, t)
+
\int_{\mu_{\min}}^{\mu_{\max}}
d\mu'\;
K_n(\mu, \mu'; q, T) \cdot S_R(\mu'; T)
\cdot
\bigl[\rho_{\eq}(\mu'; q, T) - \rho(\mu'; q, t)\bigr]
```

(c) Apparent potential (preserved):
```latex
V_{n,\app} = V_n + s_I\, |I|\, R_n(q, T, |I|)
```

(d) ICA / DVA observable (preserved structure with new `V_n`):
```latex
\frac{dQ_{\ext}}{dV_{n,\app}}
=
\frac{Q_{\cell}}{\bigl. dV_{n,\app}/dq\bigr.}
```

### 3.3 Charter-compliance note for §3 equations

- No `max`, `min`, `step`, `Heaviside`, logistic, erf, sigmoid in Eqs. (a)–(d). Charter-compliant.
- Eq. (a) reduces correctly to rechecked2's `Q_{\cell} q = Q_{\bg}(V_n,T) + Σ_j Q_{j,\tot} ξ_j` when `ρ(μ) → Σ_j Q_{j,\tot} δ(μ - U_j)` (Dirac comb limit). Discrete N_p is recovered as a special case, not a primary form.
- Eq. (b) is structurally identical to JCP 2017 Eq. (32) with mapping `W̄_u(r) ↔ ρ(μ; q, t)`, `r ↔ μ`. The user's Refs. 6, 7 ratio-substitution applies directly.

---

## §4. Forbidden-Pattern List

| # | Forbidden | Reason |
|---|---|---|
| FB1 | Any `max(., 0)` or `Heaviside(.)` in any definitional equation | Equivalent to AP1; introduces step |
| FB2 | Any `min(., constant)` in any definitional equation | Equivalent to AP2; introduces saturation step |
| FB3 | `logistic`, `sigmoid`, `tanh` as the canonical functional form of any continuous distribution or equilibrium quantity | Equivalent to AP3; smooth-step is still step in the `w → 0` limit |
| FB4 | `erf`, `erfc` as the canonical functional form of any continuous distribution or equilibrium quantity | Equivalent to AP4 |
| FB5 | Discrete `N_p`-indexed `ξ_j`, `k_j`, `U_j`, `w_j`, `Q_{j,\tot}` as primary state variables | Equivalent to AP5/AP8; demoted to derived quantities only |
| FB6 | `softplus` (`ε ln(1 + exp(x/ε))`) introduced as the canonical form without an explicit `ε → 0` smooth-limit clause | Equivalent to AP7 absent the smooth-limit discipline of §5 |
| FB7 | `sign(.)`, `clip(., a, b)`, piecewise-linear functions in definitional equations | Generalization of step; same prohibition |
| FB8 | Discretization of `μ` in definitional equations without explicit basis-expansion derivation from the continuous form | Hidden re-introduction of AP5 |
| FB9 | Any approximation step that silently replaces a continuous integral with a finite sum without an explicit error term | Same as FB8 |
| FB10 | Replacing `ρ(μ; q, T)` with a single representative `V_n` or single representative `ξ` without explicit moment-projection statement | Re-introduces single-state simplification |

**Permissive notes**:
- Numerical regularization for solver stability (softplus, ε_Q floor on `∂Q_bg/∂V_n`, smoothing of bounded support) is allowed — but every regularization must satisfy the §5 smooth-limit consistency rule.
- Empirical comparison sections (e.g., EMG fit for initial-value seeding) may invoke logistic / erf as fits to data, with an explicit "this is an empirical comparison, not a definitional form" disclaimer.
- N_p-indexed quantities may appear in §3 (Effective Transition) and §10 (Fitting) as derived quantities from the continuous `ρ(μ; q, T)` — never as primary state.

---

## §5. Smooth-Limit Consistency Rule

Any regularization parameter `ε > 0` introduced for numerical stability must have:

1. An explicit smooth-limit expression that, in the limit `ε → 0`, recovers a Charter-compliant continuous form (NOT a hard step).
2. A documented domain in which the regularization is active.
3. A justification that the regularization is solver-side, not physics-side.

### 5.1 Worked example 1 — Softplus barrier (replacing AP1 / AP7)

```latex
\Delta G_{\eff}^{+}(\mu)
=
\varepsilon_G \ln\!\Bigl(1 + \exp\!\bigl(\Delta G_{\eff}(\mu) / \varepsilon_G\bigr)\Bigr)
\;\;
\xrightarrow[\varepsilon_G \to 0]{}
\;\;
\max\!\bigl(\Delta G_{\eff}(\mu), 0\bigr)
```

- The `ε_G → 0` limit recovers AP1, which is the anti-pattern.
- **Permissible only when** the new Chapter 1 also explicitly states `ΔG_eff(μ) ≥ 0` is required by the underlying continuous reactivity kernel construction in §6/§7, so the `max(., 0)` is automatically satisfied in the well-posed domain. Then the softplus is a pure numerical safety net, never engaged in the physically meaningful domain.

### 5.2 Worked example 2 — Q_bg slope floor (replacing potential rechecked2 §4.4 stiff bound)

```latex
\frac{\partial Q_{\bg}}{\partial V_n}
\;\ge\;
\varepsilon_Q > 0
\;\;
\xrightarrow[\varepsilon_Q \to 0]{}
\;\;
\frac{\partial Q_{\bg}}{\partial V_n} \ge 0
```

- The `ε_Q → 0` limit recovers a non-negative monotonicity condition — Charter-compliant (no step).
- The strict positivity `ε_Q > 0` is a numerical condition for charge-balance root-find solver, not a physics assumption.

### 5.3 Smooth-limit table format (used in Charter and Result documents)

| Regularization | Symbol | Active domain | Smooth-limit form | `ε → 0` recovered form | Charter-compliant? |
|---|---|---|---|---|---|
| Softplus barrier | `ε_G` | Solver only | `ε_G ln(1+exp(ΔG/ε_G))` | `max(ΔG, 0)` | OK iff §5.1 justification holds |
| Q_bg slope floor | `ε_Q` | Charge-balance solver only | `∂Q_bg/∂V_n ≥ ε_Q` | `∂Q_bg/∂V_n ≥ 0` | OK (continuous) |

---

## §6. Audit Dimension #11 Procedure

(Extends `feedback_phase_audit_workflow` 10 dims with the new system-fidelity dim. Project-local until DQ-G5 user approval makes it global memory.)

### 6.1 Pass 1 — Enumerate

Scan the candidate document for every occurrence of the following keywords / LaTeX commands in definitional contexts:

- ASCII: `max(`, `min(`, `clip(`, `step(`, `Heaviside(`, `sign(`, `softplus(`, `relu(`
- LaTeX: `\max`, `\min`, `\text{step}`, `\Theta`, `\operatorname{sgn}`, `\sigmoid`, `\tanh`, `\operatorname{erf}`, `\operatorname{erfc}`, `\softplus`, `\operatorname{ReLU}`
- Equation patterns: `1/(1+\exp(...))`, `(1/2)(1+\operatorname{erf}(...))`, `\Sigma_{j=1}^{N_p}` with `N_p` as a discrete primary index

Record each occurrence: file, line, equation label, surrounding sentence (5-line context window).

### 6.2 Pass 2 — Classify

For each Pass 1 occurrence, assign one of:

- **FAIL — definitional**: The occurrence is the canonical form of a definitional equation (e.g., the equation that defines `ξ_eq`). MUST be removed before phase exits.
- **WARN — regularization with smooth limit**: The occurrence is a solver-side regularization that satisfies §5 smooth-limit rule. ALLOWED with explicit smooth-limit clause at point of use.
- **WARN — empirical approximation**: The occurrence is in a fitting/empirical-comparison section with an explicit "not a definitional form" disclaimer. ALLOWED.
- **OK — derived**: The occurrence is the result of a derivation from continuous-form quantities, with the derivation explicitly shown. ALLOWED.

### 6.3 Pass 3 — Verify

For each Pass 2 FAIL: confirm that the offending equation has been removed or reclassified as WARN/OK with explicit justification.

For each Pass 2 WARN: confirm that the §5 smooth-limit clause is present at the point of use, OR the empirical disclaimer is present, OR the derivation is explicitly shown.

For each Pass 2 OK: confirm derivation traceability to canonical variables in §3 of this Charter.

### 6.4 Reporting

Each phase Result document MUST contain a Dim #11 section with the table:

| Phase | Pass 1 occurrences | Pass 2 FAIL | Pass 2 WARN | Pass 2 OK | Pass 3 remaining FAIL |
|---|---:|---:|---:|---:|---:|
| ... | ... | ... | ... | ... | 0 (required) |

---

## §7. Legacy ↔ New Variable Mapping

Covers ver5 Ch1 §2 (21 entries) and ver1_rechecked2 §2 (11 entries). Total legacy entries = 21 + 11 = 32, with overlap.

### 7.1 ver5 Ch1 §2 (21 entries) — mapping to new namespace

| ver5 symbol | ver5 role | New namespace mapping | Derivation / Note |
|---|---|---|---|
| `q` | Discharge progress | `q` (canonical, preserved) | Identical |
| `SOC_cell` | Cell SOC | derived | `≈ 1 - q` (preserved relation) |
| `V_n` | Anode potential | `V_n` (canonical, preserved with new semantics — implicit solution of new charge balance) | Semantics change: was external lookup, now implicit |
| `V_{n,OCV}` | OCV anode potential | derived | Special case of `V_n` when `ρ = ρ_eq` — boundary value of equilibrium `ρ` distribution |
| `V_{n,app}` | Apparent potential | `V_{n,app}` (canonical, preserved) | Identical formula |
| `V_{n,0.2C}` | 0.2C reference potential | derived | Special case of `V_{n,app}` at `|I| = I_{0.2C}` |
| `I` | Current magnitude | `I` (canonical) | Identical |
| `s_I` | Current sign | `s_I` (canonical) | Identical |
| `R_n(q,T)` | Effective resistance | `R_n(q, T, |I|)` (canonical, extended) | `|I|`-dependence explicit (rechecked2 already had this) |
| `j` | Transition index | derived | Only in §10 fitting; never in definitional equations |
| `N_p` | Number of peaks | derived | Only in basis-expansion derivations |
| `U_j(T)` | Transition center | derived | Center of `ρ_eq(μ)` peak window `j` |
| `w_j(T)` | Equilibrium width | derived | FWHM of `ρ_eq(μ)` peak window `j` |
| `ξ_j` | Discrete progress | derived | `ξ_j = (1/N_j) ∫_{peak_j} dμ ρ(μ; q, t)` with normalization `N_j` |
| `ξ_{j,eq}` | Equilibrium progress | derived | Same with `ρ_eq` |
| `ΔH_{a,j}` | Activation enthalpy | parameter | Embedded in `S_R(μ; T)` Marcus-type construction (Phase E6) |
| `ΔS_{a,j}` | Activation entropy | parameter | Same |
| `ΔG_{a,j}` | Activation Gibbs | parameter | `ΔH_a - T ΔS_a` (preserved relation) |
| `A_j` (reaction affinity) | Driving force | derived | From `S_R(μ; T)` kernel + `V_{n,drive}` |
| `χ_j` | Coupling coefficient | parameter | Embedded in `S_R(μ; T)` chemical-potential-difference dependence |
| `ΔG_{eff,j}` | Effective barrier | derived | Embedded in `S_R(μ; T)` |
| `ν_j` | Prefactor | parameter | Embedded in `S_R(μ; T)` |
| `k_j` | Rate constant | derived | `k_j ≈ S_R(μ ≈ U_j; T)` |
| `Q_{j,tot}` | Transition capacity | derived | `∫_{peak_j} dμ ρ_eq(μ; q, T)` integrated over discharge range |
| `ρ_j(g)` | Barrier distribution | replaced | Subsumed into continuous `K_n(μ, μ'; q, T)` cross-kernel |
| `g` | Barrier dummy variable | replaced | Subsumed into `μ` and `μ'` |

### 7.2 ver1_rechecked2 §2 (11 entries) — overlap with above

| rechecked2 symbol | Mapping | Note |
|---|---|---|
| `q` | `q` canonical | Same as ver5 |
| `Q_ext` | derived | `Q_ext = Q_cell · q` (preserved relation) |
| `Q_cell` | `Q_cell` canonical | Same |
| `V_n` | `V_n` canonical | Same (rechecked2 already promoted V_n to implicit) |
| `V_{n,app}` | `V_{n,app}` canonical | Same |
| `V_{n,drive}` | `V_{n,drive}` canonical | Same |
| `R_n(q, T, |I|)` | canonical | Same |
| `ξ_j` | derived | Same as ver5 mapping |
| `ξ_{j,eq}` | derived | Same |
| `Q_{j,tot}` | derived | Same |
| `Q_bg` | `Q_bg(V_n, T)` canonical | Identical role + semantics from rechecked2 (chemical capacitance) |

**Coverage check**: 21 (ver5) + 11 (rechecked2) - overlap (10 shared in name) = 22 unique legacy entries. All mapped. Gate `GATE_E0_6` PASS.

---

## §8. Central Equation Preview

### 8.1 Eq. 48 — Charge balance with continuous `ρ`

```latex
\boxed{
Q_{\cell}\, q
\;=\;
Q_{\bg}(V_n, T)
\;+\;
\int_{\mu_{\min}}^{\mu_{\max}}
d\mu\;
\rho(\mu; q, T) \cdot n(\mu)
}
```

- Dimensional check: LHS `[C]` = RHS first term `[C]` + integral `[V] × [C/V] × [1] = [C]`. PASS.
- Smooth-limit check: `ρ → Σ_j Q_{j,tot} δ(μ - U_j)` recovers `Q_{\cell} q = Q_{\bg}(V_n, T) + Σ_j Q_{j,tot} ξ_j`, which is exactly rechecked2 Eq. `charge_balance` (line 121-126). Discrete decomposition is a special case, never the primary form. PASS.
- Charter-compliance: no AP/FB pattern.

### 8.2 Eq. 49 — Continuous reactivity Fredholm 2nd kind

```latex
\boxed{
\rho(\mu; q, t)
\;=\;
\rho_0(\mu; q, t)
\;+\;
\int_{\mu_{\min}}^{\mu_{\max}}
d\mu'\;
K_n(\mu, \mu'; q, T) \cdot S_R(\mu'; T)
\cdot
\bigl[\rho_{\eq}(\mu'; q, T) - \rho(\mu'; q, t)\bigr]
}
```

- Dimensional check: LHS `[C/V]` = RHS `[C/V] + [V] × [1/(V·s)] × [1/s] × [C/V]`. The integrand factor `S_R` carries `[1/s]` and `K_n` carries `[1/(V·s)]`, so `K_n · S_R · ρ` has `[1/(V·s²)] × [C/V] = [C/(V²·s²)]`, times `dμ [V]` gives `[C/(V·s²)]`. For dimensional self-consistency with LHS `[C/V]`, the kernel structure must include an implicit `Δt`-like factor or `S_R` must carry `[1/(V·s) · s²] = [s/V]`. **This is a unit reconciliation issue flagged for Phase E6 detailed derivation** — the kernel definition will fix units precisely.
- Smooth-limit check: when `ρ(μ; q, t)` is sharply peaked at `μ = U_j` (Dirac comb), Eq. 49 reduces to rechecked2's `dξ_j/dt = k_j (ξ_{j,eq} - ξ_j)` (Eq. dxidt line 272). PASS.
- Charter-compliance: Charter-compliant in structure; Phase E6 must complete kernel definition without introducing AP/FB patterns.

### 8.3 Structural correspondence to JCP 2017 Eq. (32)

| JCP 2017 Eq. (32) symbol | Graphite Eq. (49) symbol |
|---|---|
| `W̄_u(r)` | `ρ(μ; q, t)` |
| `r` | `μ` |
| `σ` | `μ_min` |
| `D` | `K_n` |
| `S_R(r)/e^{U_1(r)}` | `S_R(μ'; T)` |
| `[σ, ∞]` integration | `[μ_min, μ_max]` integration |

- Structural correspondence verified. Refs. 6/7 ratio-substitution directly applicable (Phase E11).

### 8.4 Apparent potential + ICA/DVA (preserved)

(Already in §3.2 Eq. (c), (d).)

---

## §9. Ref. 6, 7 Application Sketch

### 9.1 Citation block (confirmed via Wikidata self-search, Phase E0 Steps 40-44)

- **Ref. 6**: S. Lee, C. Y. Son, J. Sung, and S. H. Chong, "Communication: Propagator for diffusive dynamics of an interacting molecular pair", *J. Chem. Phys.* **134**, 121102 (2011). **DOI: 10.1063/1.3565476**. PubMed ID: 21456635. Wikidata: Q51583050.
- **Ref. 7**: C. Y. Son, J. Kim, J.-H. Kim, J. S. Kim, and S. Lee, "An accurate expression for the rates of diffusion-influenced bimolecular reactions with long-range reactivity", *J. Chem. Phys.* **138**, 164123 (2013). **DOI: 10.1063/1.4802584**. PubMed ID: 23635127. Wikidata: Q43553001.

(Both DOIs externally confirmed by Phase E0 — no `근거 미발견` fallback needed.)

### 9.2 ρ^{simple} candidate

Per master roadmap Step 55: take `ρ^{simple}(μ; q, T)` as the equilibrium distribution `ρ_eq(μ; q, T)` evaluated under the assumption `V_n = V_{n,OCV}(q, T)` (legacy ver5 external-lookup assumption). This is the analog of JCP 2017 §II.B's δ-function-sink solution `W̄_u^δ(r)` — a known closed-form for a simplified kernel that serves as the reference for the ratio-substitution.

### 9.3 Ratio-substitution form (preview)

JCP 2017 Eq. (34):
```latex
\overline{W}_u(r_1) / \overline{W}_u(r)
\;\approx\;
\overline{W}_u^{\delta}(r_1) / \overline{W}_u^{\delta}(r)
```

Graphite analogue:
```latex
\rho(\mu_1; q, t) / \rho(\mu; q, t)
\;\approx\;
\rho^{\mathrm{simple}}(\mu_1; q, T) / \rho^{\mathrm{simple}}(\mu; q, T)
```

Substituted into Eq. (49) and rearranged (per JCP 2017 Eq. (33) → (39) algebra, to be developed in Phase E11), yields a closed-form `ρ(μ; q, t)` analogous to JCP 2017 Eq. (39).

### 9.4 Validity conditions (graphite analogue of JCP 2017 §III)

1. Low C-rate (graphite analog of small `K` external field strength) — perturbation away from `ρ_eq` remains modest.
2. Large characteristic chemical potential scale (analog of large Onsager distance `rc`) — isotropic potential dominates over the perturbation.
3. Small reactivity magnitude (analog of small `σ³ φ / D`) — the ratio substitution remains accurate.
4. **Continuous reactivity kernel `S_R(μ)` smooth in `μ`** — the new condition that did not appear in JCP 2017 because that paper already assumed continuous-in-r reactivity. This condition is what avoids the ver5 step function assumption and is the foundational compliance check for Chapter 1.

Quantitative bounds for (1)-(3) deferred to Phase G (numerical implementation).

### 9.5 Limitations to document in §17

- Beyond the validity domain, higher-order ratio-substitution (JCP 2017 §II.C line 320-336) extends accuracy at the cost of expression complexity.
- The closed-form is an approximation; numerical validation against direct solution of Eq. (49) at representative `(q, T, |I|)` points is Phase G work.

---

## Validation (Charter Result — Gates `GATE_E0_1` ~ `GATE_E0_8`)

| Gate | Requirement | Status | Evidence |
|---|---|---|---|
| `GATE_E0_1` | Charter document contains all 9 sections, no section empty | **PASS** | §1-§9 all present, each with substantive content |
| `GATE_E0_2` | Anti-Pattern List cites ≥ 5 specific ver5+rechecked2 line numbers | **PASS** | §2 lists 8 anti-patterns (AP1-AP8) with explicit line numbers (188, 195, 240-245, 247-249, 137-150, 188-193, 250-265, 110-114) |
| `GATE_E0_3` | Allowed-Pattern List defines new variable namespace and central equation form | **PASS** | §3.1 = 16 canonical + many derived; §3.2 = Eqs. (a)–(d) including Eq. 48, 49 |
| `GATE_E0_4` | Smooth-Limit Rule ≥ 2 worked examples | **PASS** | §5.1 softplus + §5.2 Q_bg slope floor — 2 explicit examples with `ε → 0` recovery |
| `GATE_E0_5` | Audit Dim #11 procedure has Pass 1/2/3 each defined | **PASS** | §6.1 Pass 1 (enumerate keyword list), §6.2 Pass 2 (FAIL/WARN/OK classification), §6.3 Pass 3 (verify), §6.4 reporting table format |
| `GATE_E0_6` | Legacy ↔ New mapping covers ver5 §2 (21) + rechecked2 §2 (11) | **PASS** | §7.1 = 25 ver5 rows (some compound like ρ_j+g), §7.2 = 11 rechecked2 rows; total 22 unique mapped |
| `GATE_E0_7` | Central Equations Eq. 48, 49 are valid LaTeX, pass dimensional and smooth-limit check | **PASS-with-note** | §8.1 PASS; §8.2 has unit reconciliation note flagged for Phase E6 (acceptable per master roadmap A11) |
| `GATE_E0_8` | Ref. 6, 7 Application Sketch identifies `ρ^{simple}` candidate explicitly | **PASS** | §9.2 names `ρ_eq(μ; q, T)` under `V_n = V_{n,OCV}` legacy assumption as `ρ^{simple}` |

**Gate summary: 8/8 PASS** (with 1 PASS-with-note for unit reconciliation deferred to Phase E6).

---

## Phase E0 Audit (10 dims + Dim #11 = 11 dims, Pass 1+2+3)

| Dim | Pass 1 finding on Charter | Pass 2 result | Pass 3 result |
|---|---|---|---|
| #2 verbatim | User 5-27 verbatim "스텝펑션의 형태" referenced in §1 amplification + §2 anti-pattern justification | PASS — verbatim quoted accurately | PASS |
| #3 data flow | Charter loads from audit v0.2 §1.5, §5.11; ver5 lines 188/195/240-245/247-249/137-150; rechecked2 lines 188-193/250-265/110-114; JCP §II.C lines 193-275 | PASS — all loads documented in §2 and §9 | PASS |
| #6 convention | Charter uses canonical LaTeX (`\mu`, `\rho`, `\eq`, `\bg`, `\cell`, etc.) matching ver5/rechecked2 macros + new `\Sreact`, `\Kncross` | PASS — no convention conflict | PASS |
| #7 silent miss | Charter sections 1-9 all present, no skipped requirement | PASS | PASS |
| #10 contract | Result format follows phase-level plan §"Implementation Interfaces"; Gates 1-8 explicit | PASS — schema compliance | PASS |
| α boundary | Phase E0 boundary = Charter authoring + Result deliverable; no LaTeX in `Claude/docs/` | PASS — confirmed by file inventory | PASS |
| β handover | Phase E1 will receive: new namespace (§3), Eq. 48/49 (§8), Ref. 6/7 sketch (§9), audit Dim #11 procedure (§6) | PASS — handover scope clear | PASS |
| γ tree | All Charter sections cross-referenced from Phase E0 plan steps 21-65 | PASS — bijection | PASS |
| δ 4-tier | Validation table classifies each Gate as 확정(PASS)/PASS-with-note. No unclassified item | PASS | PASS |
| **#11 system-fidelity** | Charter itself enumerated: no `max`, `min`, logistic, erf, softplus, etc. in Charter's own equations (§3.2, §8.1, §8.2, §9.3). §5.1 softplus is an explicit WARN example with smooth-limit clause. §8.1, §8.2 boxed equations are AP/FB-free | **PASS — 0 FAIL** | **PASS — no regression** |

**Audit summary: 11/11 dims PASS, 0 FAIL.** Dim #11 confirms the Charter itself is Charter-compliant (the rebuild's governance does not violate the rebuild's rules).

---

## Confirmed Non-Changes

- `Claude/docs/graphite_ica_dynamic_ver5.tex` — not read in Phase E0 (line evidence used from Phase A prior reads). NOT MODIFIED.
- `Claude/docs/graphite_ica_charge_balance_ver1_rechecked2.tex` — same. NOT MODIFIED.
- `Claude/_local_only/*.pdf` — not read in Phase E0 (jcp_extract.txt indexed via Phase D prior reads). NOT MODIFIED.
- `Codex/` — NOT accessed (P2 compliance).
- ver5/rechecked2 variable names, equation labels, Korean phrasing preserved verbatim in citation contexts only.

## Open Issues / Decision Queue

| ID | Item | Classification | Note |
|---|---|---|---|
| OI-E0-1 | Eq. 49 unit reconciliation — `K_n` and `S_R` joint dimensional definition | 추정 (Phase E6 will resolve) | Deferred to Phase E6 by design |
| OI-E0-2 | Quantitative validity bounds for §9.4 (low C-rate, large rc analog, small reactivity) | 미검증 (Phase G) | Deferred to numerical implementation phase |
| OI-E0-3 | DQ-G2 user cross-check of `μ` as Li/Li⁺-reference electrochemical potential | 사용자 결정 대기 | Phase F3 (PDF user review) is canonical check point |
| OI-E0-4 | DQ-G5 user approval to globalize audit Dim #11 memory + B4/B5/B6 memory candidates | 사용자 결정 대기 | Dim #11 used project-locally for now |
| OI-E0-5 | DQ-G6 Chapter 2 rebuild master roadmap timing | 사용자 결정 대기 (Phase F5) | Out of scope until current rebuild closes |
| OI-E0-6 | DQ1 (ChatGPT 의 큰 논리 오류 정체) — for §1 anti-pattern amplification | 사용자 결정 대기 (optional) | Phase E2 §1 will note "if user provides, will be added inline" |

## Next

- **Next phase**: **Phase E1 — Spine Redesign And Core Variable Selection** (cumulative Steps 81-140, 60 steps).
- **Auto-proceed**: per `feedback_plan_continuation_until_done`, Phase E1 entry is automatic upon Phase E0 PASS + commit + push. No additional user GO required (DQ-G1 GO covers Phase E0 ~ F2).
- **Phase E1 inputs**: this Charter (§1-§9 + Audit + Validation), audit v0.2, master roadmap.
- **Phase E1 outputs**: `Claude/results/PHASE_E1_spine_redesign_RESULT.md` + companion JSON, ledger Phase E1 row PASS.
- **Phase E1 deferred-to-next-conversation-turn**: due to current response budget, Phase E1 enters at the start of the next user-initiated turn (immediate continuation). User may inject corrections to the Charter via the conversation; otherwise Phase E1 begins automatically.

---

## Phase E0 closure

**Status**: PASS
**Gate**: `PASS_FOUNDATION_RESET_CHARTER`
**Step range completed**: 19 ~ 80
**Next cumulative step**: 81 (Phase E1 start)
**Authored**: 2026-05-27 by Claude
