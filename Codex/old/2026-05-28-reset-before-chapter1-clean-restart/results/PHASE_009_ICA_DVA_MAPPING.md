# Phase 009 — ICA/DVA Observable Mapping

## Summary

This phase maps the phase-progress tail term `d xi_j/dq` into the observable graphite negative-electrode ICA and DVA expressions. The mapping is charge-balance consistent: `d xi_j/dq` first changes `dV_n/dq`, then `dV_{n,\app}/dq`, and only then appears in `dQ_ext/dV_{n,\app}` and `dV_{n,\app}/dQ_ext`.

Gate result: `PASS_ICA_DVA_MAPPING`

## Step Range

Planned steps: 137-158

Actual steps completed: 137-158

## Source Basis

| Element | Source |
|---|---|
| charge balance | `graphite_ica_charge_balance_ver1_rechecked2.tex:118-129` |
| phase-progress dynamics | `graphite_ica_charge_balance_ver1_rechecked2.tex:268-286` |
| charge-balance differentiation | `graphite_ica_charge_balance_ver1_rechecked2.tex:353-368` |
| apparent voltage derivative | `graphite_ica_charge_balance_ver1_rechecked2.tex:379-391` |
| ICA/DVA observables | `graphite_ica_charge_balance_ver1_rechecked2.tex:394-412` |
| monotonicity constraint | `graphite_ica_charge_balance_ver1_rechecked2.tex:370-377` |

## 1. Start From Charge Balance

The internal potential is determined by:

```tex
Q_{\cell}q
=Q_{\bg}(V_n,T)
+\sum_{j=1}^{N_p}Q_{j,\tot}\xi_j.
```

This is the reason the ICA/DVA mapping must pass through `V_n`. The phase progress does not simply add a visual peak; it changes the internal potential required to satisfy charge balance.

## 2. Differentiate With Respect To `q`

Differentiate both sides:

```tex
\frac{d}{dq}(Q_{\cell}q)
=
\frac{d}{dq}Q_{\bg}(V_n,T)
+\sum_j Q_{j,\tot}\frac{d\xi_j}{dq}.
```

The left side is:

```tex
\frac{d}{dq}(Q_{\cell}q)=Q_{\cell}.
```

For the background term, use the chain rule:

```tex
\frac{d}{dq}Q_{\bg}(V_n,T)
=
\frac{\partial Q_{\bg}}{\partial V_n}
\frac{dV_n}{dq}
+
\frac{\partial Q_{\bg}}{\partial T}
\frac{dT}{dq}.
```

Therefore:

```tex
Q_{\cell}
=
\frac{\partial Q_{\bg}}{\partial V_n}
\frac{dV_n}{dq}
+
\frac{\partial Q_{\bg}}{\partial T}
\frac{dT}{dq}
+
\sum_jQ_{j,\tot}\frac{d\xi_j}{dq}.
```

Use explicit multiplication in the manuscript:

```tex
Q_{\cell}
=
\left(\frac{\partial Q_{\bg}}{\partial V_n}\right)
\left(\frac{dV_n}{dq}\right)
+
\left(\frac{\partial Q_{\bg}}{\partial T}\right)
\left(\frac{dT}{dq}\right)
+
\sum_jQ_{j,\tot}\frac{d\xi_j}{dq}.
```

## 3. Solve For Internal Voltage Slope

Solving for `dV_n/dq`:

```tex
\boxed{
\frac{dV_n}{dq}
=
\frac{
Q_{\cell}
-\left(\dfrac{\partial Q_{\bg}}{\partial T}\right)\dfrac{dT}{dq}
-\sum_jQ_{j,\tot}\dfrac{d\xi_j}{dq}
}{
\dfrac{\partial Q_{\bg}}{\partial V_n}
}
}
```

In the isothermal Chapter 1 core:

```tex
\boxed{
\frac{dV_n}{dq}
=
\frac{
Q_{\cell}
-\sum_jQ_{j,\tot}\dfrac{d\xi_j}{dq}
}{
\dfrac{\partial Q_{\bg}}{\partial V_n}
}
}
```

This equation is the key observable bridge. A kinetic tail in `d xi_j/dq` appears as a tail-shaped term in the internal voltage slope.

## 4. Apparent Voltage Slope

The apparent negative-electrode potential is:

```tex
V_{n,\app}
=V_n+s_I|I|R_n(q,T,|I|).
```

For isothermal constant current:

```tex
\boxed{
\frac{dV_{n,\app}}{dq}
=
\frac{dV_n}{dq}
+
s_I|I|\frac{\partial R_n}{\partial q}.
}
```

Substitute the isothermal internal slope:

```tex
\boxed{
\frac{dV_{n,\app}}{dq}
=
\frac{
Q_{\cell}
-\sum_jQ_{j,\tot}\dfrac{d\xi_j}{dq}
}{
\dfrac{\partial Q_{\bg}}{\partial V_n}
}
+
s_I|I|\frac{\partial R_n}{\partial q}.
}
```

This keeps the roles separated:

- `d xi_j/dq` is the phase-transition kinetic contribution;
- `R_n` is the apparent voltage-shift contribution;
- they must not be freely used to fit the same tail without constraints.

## 5. ICA

Since:

```tex
Q_{\ext}=Q_{\cell}q,
\qquad
\frac{dQ_{\ext}}{dq}=Q_{\cell},
```

the graphite negative-electrode ICA is:

```tex
\boxed{
\frac{dQ_{\ext}}{dV_{n,\app}}
=
\frac{Q_{\cell}}{\dfrac{dV_{n,\app}}{dq}}
}
```

Substitution gives:

```tex
\frac{dQ_{\ext}}{dV_{n,\app}}
=
\frac{Q_{\cell}}
{
\dfrac{
Q_{\cell}
-\sum_jQ_{j,\tot}\dfrac{d\xi_j}{dq}
}{
\dfrac{\partial Q_{\bg}}{\partial V_n}
}
+
s_I|I|\dfrac{\partial R_n}{\partial q}
}.
```

Therefore the ICA tail is not a separate empirical object. It is the reciprocal-voltage-slope expression containing the kinetic lag term `d xi_j/dq`.

## 6. DVA

The corresponding DVA is:

```tex
\boxed{
\frac{dV_{n,\app}}{dQ_{\ext}}
=
\frac{1}{Q_{\cell}}
\frac{dV_{n,\app}}{dq}.
}
```

Substitute the apparent voltage slope:

```tex
\frac{dV_{n,\app}}{dQ_{\ext}}
=
\frac{1}{Q_{\cell}}
\left[
\frac{
Q_{\cell}
-\sum_jQ_{j,\tot}\dfrac{d\xi_j}{dq}
}{
\dfrac{\partial Q_{\bg}}{\partial V_n}
}
+
s_I|I|\frac{\partial R_n}{\partial q}
\right].
```

ICA and DVA are reciprocal descriptions of the same slope structure, not independent sources of tail physics.

## 7. Local Tail In The Observable

From Phase 008, in the post-peak local tail:

```tex
\frac{d\xi_j}{dq}
=\kappa_j u_j
\approx
\kappa_j u_j(q_a)
\exp\left[-\frac{q-q_a}{\ell_{q,j}}\right].
```

For one dominant transition and slowly varying background, write:

```tex
\frac{dV_{n,\app}}{dq}
\approx
D_0(q)
-B_j
\exp\left[-\frac{q-q_a}{\ell_{q,j}}\right],
```

where:

```tex
B_j
=
\frac{Q_{j,\tot}\kappa_j u_j(q_a)}
{\partial Q_{\bg}/\partial V_n}
```

up to the sign convention of the selected discharge coordinate, and `D_0(q)` collects the slowly varying background and `R_n` terms.

Then:

```tex
\frac{dQ_{\ext}}{dV_{n,\app}}
\approx
\frac{Q_{\cell}}
{D_0(q)-B_j\exp[-(q-q_a)/\ell_{q,j}]}.
```

If the tail perturbation is small compared with the local background slope:

```tex
\frac{dQ_{\ext}}{dV_{n,\app}}
\approx
\frac{Q_{\cell}}{D_0(q)}
\left[
1+
\frac{B_j}{D_0(q)}
\exp\left(-\frac{q-q_a}{\ell_{q,j}}\right)
\right].
```

Thus the observable ICA tail inherits the kinetic decay scale `ell_q,j`, while the apparent amplitude and sign are modulated by charge-balance slope and resistance terms.

## 8. Sign And Monotonicity Guard

For the default discharge convention in the corrected source, the model should preserve the physical sign of the voltage slope over the fitting interval. In the isothermal expression:

```tex
\frac{dV_n}{dq}
=
\frac{
Q_{\cell}
-\sum_jQ_{j,\tot}\dfrac{d\xi_j}{dq}
}{
\dfrac{\partial Q_{\bg}}{\partial V_n}
},
```

a sufficient guard under positive background slope is:

```tex
\sum_jQ_{j,\tot}\frac{d\xi_j}{dq}
\le Q_{\cell}.
```

This is not a tail-area statement. It is a monotonicity and physical-slope constraint.

## 9. Mapping Consequences

The mapping supports these conclusions:

- a phase-transition tail in ICA comes from nonzero `d xi_j/dq` after the equilibrium transition center has passed;
- the tail length is controlled by `ell_q,j`, not by equilibrium width `w_j` alone;
- `w_j` shapes the equilibrium target, while `k_j` controls lag and tail decay;
- `R_n` shifts or tilts apparent voltage and must be constrained separately from kinetic lag;
- peak area remains a later fitting/capacity issue and is not the main Chapter 1 derivation target.

## Validation

| Check | Result |
|---|---|
| Started from charge balance | PASS |
| Differentiated charge balance with respect to `q` | PASS |
| Included thermal derivative term before isothermal simplification | PASS |
| Solved for `dV_n/dq` | PASS |
| Derived isothermal `dV_n/dq` | PASS |
| Differentiated apparent voltage in isothermal constant-current form | PASS |
| Derived ICA as `Q_cell/(dV_app/dq)` | PASS |
| Derived DVA as `(1/Q_cell)dV_app/dq` | PASS |
| Inserted tail form `d xi/dq ~ exp[-(q-q_a)/ell_q]` | PASS |
| Showed observable tail inherits kinetic scale under local approximation | PASS |
| Monotonicity/sign guard included | PASS |
| Peak-area drift avoided | PASS |

## Gate

Gate: `PASS_ICA_DVA_MAPPING`

Status: PASS

Reason:

- `d xi_j/dq` is mapped into ICA/DVA through charge-balance differentiation;
- apparent voltage and resistance roles remain explicit;
- the observable tail is tied to the kinetic tail scale derived in Phase 008;
- no empirical peak function is used as a substitute for the derivation.

## Confirmed Non-Changes

- No source `.tex` file was modified.
- No PDF was modified.
- `D:\Projects\Project_Anode_Fit\Claude` was not modified.
- No commit, push, merge, or branch operation was performed.

## Open Issues / Decision Queue

| Issue | Status |
|---|---|
| Barrier-distribution extension still needs separation from equilibrium-width effects | pending Phase 010 |
| Final manuscript wording must clarify negative-electrode vs full-cell voltage scope | pending Phase 011 |
| Reciprocal ICA expression can become nonlinear near very small `dV_app/dq`; final manuscript should avoid over-linearizing the peak center | pending Phase 011 |

No user decision is required before Phase 010.

## Next

Proceed directly to Phase 010 — Barrier Distribution Extension.
