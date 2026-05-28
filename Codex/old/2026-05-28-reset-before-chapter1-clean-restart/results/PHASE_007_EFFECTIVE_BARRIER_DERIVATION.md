# Phase 007 — Effective Barrier Derivation

## Summary

This phase derives the temperature- and present-potential-dependent effective barrier. The derivation passes the sign, unit, and voltage-role checks needed for Chapter 1.

Gate result: `PASS_EFFECTIVE_BARRIER_DERIVATION`

## Step Range

Planned steps: 91-112

Actual steps completed: 91-112

## Source Basis

| Element | Source |
|---|---|
| intrinsic activation free energy | `graphite_ica_charge_balance_ver1_rechecked2.tex:240-244` |
| affinity / driving voltage | `graphite_ica_charge_balance_ver1_rechecked2.tex:224-238` |
| effective barrier | `graphite_ica_charge_balance_ver1_rechecked2.tex:245-249` |
| positive barrier / softplus | `graphite_ica_charge_balance_ver1_rechecked2.tex:250-266` |
| reduced electrochemical alternative `A_j=F eta_j` | `graphite_ica_dynamic_ver5.tex:871-888` |
| double-counting warning | `graphite_ica_charge_balance_ver1_rechecked2.tex:236-238`; `graphite_ica_dynamic_ver5.tex:891-894` |

## 1. Intrinsic Thermal Barrier

For a graphite staging transition `j`, define the intrinsic activation free energy:

```tex
\Delta G_{a,j}(T)=\Delta H_{a,j}-T\Delta S_{a,j}.
```

Unit check:

```text
Delta H_a,j: J mol^-1
T: K
Delta S_a,j: J mol^-1 K^-1
T Delta S_a,j: J mol^-1
Delta G_a,j: J mol^-1
```

Interpretation:

- `Delta H_a,j` is the enthalpic part of the activation barrier.
- `-T Delta S_a,j` is the entropic part.
- Temperature can affect the barrier through this expression, and it also appears later in the Arrhenius denominator `RT`.

This is the thermal baseline. It does not yet include the present electrode-potential assistance requested by the user.

## 2. Present-Potential Driving Affinity

The kinetic driving voltage is `V_{n,\drive}`. It is kept separate from the internal potential `V_n` and apparent potential `V_{n,\app}`:

```tex
V_n
\neq
V_{n,\app}
\neq
V_{n,\drive}
```

unless a reduced approximation is explicitly declared.

Define the affinity:

```tex
\mathcal A_j
=s_{\phi,j}F\left[V_{n,\drive}-U_j(T)\right].
```

Here:

- `U_j(T)` is the transition-center potential;
- `s_{\phi,j}` fixes the forward direction;
- `F` is the Faraday constant;
- `V_{n,\drive}-U_j(T)` is the signed potential displacement relevant to the transition.

Unit check:

```text
F: C mol^-1
voltage: V = J C^-1
F * voltage: J mol^-1
A_j: J mol^-1
```

Therefore `A_j` can be added to or subtracted from an activation free energy.

## 3. Sign Convention

Define the forward transition direction as the direction in which `xi_j` increases.

Choose `s_{\phi,j}` so that:

```text
A_j > 0
```

when the present electrode potential assists that forward transition.

Examples:

- If increasing `V_{n,\drive}` above `U_j(T)` helps the transition progress, use `s_{\phi,j}=+1`.
- If increasing `V_{n,\drive}` above `U_j(T)` suppresses that transition, use `s_{\phi,j}=-1`.

The sign is not decorative. It is the part of the model that makes “present potential lowers the barrier” mathematically true only in the physically assisted direction.

## 4. Coupling Coefficient

Introduce a nonnegative coupling coefficient:

```tex
\chi_j \ge 0.
```

In the simplest reading, `chi_j` is dimensionless because both `Delta G_a,j` and `A_j` have units of `J mol^-1`.

Interpretation:

- `chi_j=0`: present potential does not alter the barrier.
- larger `chi_j`: the same driving affinity lowers the barrier more strongly.
- `chi_j` must not be used to hide unrelated resistance or equilibrium-width effects.

## 5. Effective Barrier

The effective barrier is:

```tex
\Delta G_{\eff,j}
=\Delta G_{a,j}(T)-\chi_j\mathcal A_j.
```

Substituting the affinity:

```tex
\Delta G_{\eff,j}
=\Delta H_{a,j}-T\Delta S_{a,j}
-\chi_j s_{\phi,j}F\left[V_{n,\drive}-U_j(T)\right].
```

Sign audit:

```text
If A_j > 0 and chi_j >= 0:
  Delta G_eff,j < Delta G_a,j
  the forward barrier is lowered.

If A_j = 0:
  Delta G_eff,j = Delta G_a,j
  the model reduces to the thermal barrier.

If A_j < 0 and chi_j >= 0:
  Delta G_eff,j > Delta G_a,j
  the forward transition is hindered.
```

This is the requested “temperature barrier plus electrode-potential-assisted effective barrier” logic.

## 6. Positive Effective Barrier

The reduced expression can produce `Delta G_eff,j < 0` under strong driving. If inserted directly into an Arrhenius expression, this would make:

```tex
k_j>\nu_j(T)
```

which exceeds the interpretation of `nu_j(T)` as the limiting attempt frequency/prefactor.

Use a smooth positive barrier:

```tex
\Delta G_{\eff,j}^{+}
=\epsilon_G
\ln\left[
1+\exp\left(\frac{\Delta G_{\eff,j}}{\epsilon_G}\right)
\right].
```

Corrected TeX form for manuscript:

```tex
\Delta G_{\eff,j}^{+}
=\epsilon_G\ln\left[
1+\exp\left(\frac{\Delta G_{\eff,j}}{\epsilon_G}\right)
\right].
```

where:

```text
epsilon_G: J mol^-1
```

Limits:

```text
Delta G_eff >> epsilon_G:
  Delta G_eff^+ approx Delta G_eff

Delta G_eff << -epsilon_G:
  Delta G_eff^+ approx 0
```

Therefore the rate can approach `nu_j(T)` but does not exceed it through the barrier term.

Important: `epsilon_G` is a numerical regularization scale, not a new physical barrier.

## 7. Rate Constant

Define the relaxation rate:

```tex
\boxed{
k_j=\nu_j(T)\exp\!\left(-\frac{\Delta G_{\eff,j}^{+}}{RT}\right)
}
```

Unit check:

```text
R: J mol^-1 K^-1
T: K
RT: J mol^-1
Delta G_eff^+: J mol^-1
Delta G_eff^+/(RT): dimensionless
nu_j(T): s^-1
k_j: s^-1
```

## 8. Barrier Lowering Increases Rate

Because:

```tex
\ln k_j=\ln\nu_j(T)-\frac{\Delta G_{\eff,j}^{+}}{RT},
```

a lower positive effective barrier increases `k_j`.

For the softplus barrier:

```tex
\frac{\partial \Delta G_{\eff,j}^{+}}{\partial \Delta G_{\eff,j}}
=
\frac{1}{1+\exp[-\Delta G_{\eff,j}/\epsilon_G]}.
```

and:

```tex
\frac{\partial \Delta G_{\eff,j}}{\partial \mathcal A_j}
=-\chi_j.
```

Therefore:

```tex
\frac{\partial \ln k_j}{\partial \mathcal A_j}
=
\frac{\chi_j}{RT}
\frac{1}{1+\exp[-\Delta G_{\eff,j}/\epsilon_G]}.
```

For `chi_j>0`, this derivative is nonnegative. A favorable increase in `A_j` increases `k_j` until the rate approaches the prefactor-limited regime.

## 9. Temperature Limits

The rate expression is:

```tex
k_j(T,V)
=\nu_j(T)\exp\!\bigl[-\Delta G_{\eff,j}^{+}(T,V)/(RT)\bigr].
```

Low-temperature tendency:

- `RT` is smaller, so the same positive barrier creates a larger negative exponent magnitude.
- `nu_j(T)` may also decrease depending on the prefactor model.
- Therefore `k_j` tends to be smaller, which supports a longer kinetic tail.

High-temperature tendency:

- `RT` is larger, reducing the penalty of a positive barrier.
- `nu_j(T)` often increases in thermally activated processes.
- If the net temperature dependence makes `k_j` larger, the tail shortens.

Important qualification:

`Delta G_a,j(T)=Delta H_a,j-T Delta S_a,j` can increase or decrease with `T` depending on the sign of `Delta S_a,j`. The manuscript should not claim temperature always lowers `Delta G_a`. It should claim that the observed high-temperature short tail is explained when the net effect of `RT`, `nu_j(T)`, and `Delta G_a,j(T)` increases `k_j`.

## 10. Present-Potential Effect

At fixed `T`, the present-potential contribution is:

```tex
\mathcal A_j=s_{\phi,j}F[V_{n,\drive}-U_j(T)].
```

If the current electrode-potential state moves in the assisting direction:

```text
A_j increases
  -> Delta G_eff decreases
  -> Delta G_eff^+ decreases or saturates near zero
  -> k_j increases
  -> phase progress catches up faster
  -> tail shortens
```

If the present-potential state is weakly assisting or adverse:

```text
A_j small or negative
  -> Delta G_eff remains high
  -> k_j remains small
  -> phase progress lags
  -> tail becomes longer
```

This is the exact logic needed for the user's observation: temperature alone does not fully determine the tail. The present electrode-potential state can also shorten or lengthen the tail by changing the effective barrier.

## 11. Double-Counting Audit

| Risk | Required guard |
|---|---|
| `V_{n,\drive}\approx V_{n,\app}` imports resistance shift into `A_j` | constrain `R_n` independently or state the reduced-model assumption |
| `xi_eq` uses `V_{n,\app}` while `k_j` also uses `V_{n,\app}` | use `V_n` or quasi-equilibrium voltage for `xi_eq`; reserve drive/overpotential for rate |
| `R_n` and `k_j` both fit the same broadening | do not claim parameter identifiability without independent constraints |
| Butler-Volmer `eta_j` and lumped `R_n` both include charge-transfer effects | use one resolved model or explicitly partition components |

## 12. Assumptions

| Assumption | Status |
|---|---|
| Single transition `j` can be derived before summing over `j` | accepted for Chapter 1 |
| `chi_j>=0` | required for sign interpretation |
| `s_phi,j` is chosen to match the forward direction of `xi_j` | required |
| `V_{n,\drive}` exists as a distinct kinetic driving voltage | required |
| `V_{n,\drive}\approx V_{n,\app}` is only a reduced approximation | required |
| Softplus barrier is numerical regularization | required |
| The Arrhenius form is reduced-order phenomenology | accepted |

## Validation

| Check | Result |
|---|---|
| Started from `Delta G_a,j(T)=Delta H_a,j-T Delta S_a,j` | PASS |
| Units of intrinsic barrier checked | PASS |
| Defined affinity `A_j=s_phi F[V_drive-U_j]` | PASS |
| Units of `F * voltage` checked | PASS |
| Sign `s_phi` and forward direction explained | PASS |
| Coupling coefficient `chi_j` defined | PASS |
| Derived `Delta G_eff=Delta G_a-chi A` | PASS |
| Explained favorable affinity lowers barrier | PASS |
| Explained adverse affinity raises barrier | PASS |
| Introduced positive barrier handling | PASS |
| Chose softplus as default smooth positive barrier | PASS |
| Derived `k_j=nu exp[-DeltaG_eff^+/(RT)]` | PASS |
| Exponent dimension checked | PASS |
| Low-T/high-T limits stated with entropy qualification | PASS |
| Present-potential barrier-lowering effect stated independently of temperature | PASS |
| Double-counting audit run | PASS |

## Gate

Gate: `PASS_EFFECTIVE_BARRIER_DERIVATION`

Status: PASS

Reason:

- the sign, unit, and role logic passes;
- forward assisting potential lowers `Delta G_eff` and increases `k_j`;
- adverse potential raises `Delta G_eff` and decreases `k_j`;
- `R_n`, `V_drive`, and `k_j` double-counting risks are explicitly guarded.

## Confirmed Non-Changes

- No source `.tex` file was modified.
- No PDF was modified.
- `D:\Projects\Project_Anode_Fit\Claude` was not modified.
- No commit, push, merge, or branch operation was performed.

## Open Issues / Decision Queue

| Issue | Status |
|---|---|
| Tail residual equation still needs derivation from `dxi/dq` | pending Phase 008 |
| ICA/DVA mapping still needs separate audit | pending Phase 009 |
| Whether to include derivative `partial ln k / partial A` in final manuscript body or appendix | can decide after Phase 011 draft |

No user decision is required before Phase 008.

## Next

Proceed directly to Phase 008 — Tail Decay Derivation.
