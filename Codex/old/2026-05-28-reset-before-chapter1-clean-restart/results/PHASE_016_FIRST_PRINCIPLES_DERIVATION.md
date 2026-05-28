# Phase 016 — First-Principles Chapter 1 Derivation

## Summary

This phase derives the Chapter 1 logic from the user's physical picture and basic principles. No equation in this derivation is copied from old TeX files. The old files are not used as formula authority.

Gate result: `PASS_FIRST_PRINCIPLES_DERIVATION`

## 1. Observation And Target

Observed phenomenon:

- graphite ICA peak tail changes with temperature and present electrode potential state;
- lower temperature gives a longer tail;
- higher temperature gives a shorter tail;
- an equilibrium symmetric peak shape alone is insufficient;
- a present-potential-assisted effective barrier is needed.

Target:

```text
derive a reduced theory that links temperature and present potential to tail length,
then connects the kinetic tail to the ICA observable.
```

## 2. Beginning Convention Block

The final manuscript must begin by fixing these conventions.

| Convention | Choice |
|---|---|
| Electrode potential | `phi` denotes graphite negative-electrode potential on the analyzed branch, measured against a fixed reference such as Li/Li+ unless stated otherwise. |
| Full-cell voltage | not the main variable in Chapter 1; full-cell mapping is future work. |
| Scan coordinate | `Q` is accumulated branch charge/capacity and increases along the analyzed data direction. |
| Scan speed | `v_Q=dQ/dt>0`. |
| ICA | `I_ICA=dQ/dphi`. |
| DVA | `I_DVA=dphi/dQ`. |
| Tail direction | post-peak means the region after the equilibrium transition center has been passed along increasing `Q`. |
| Assisting potential | `psi>0` is defined to assist forward transformation. |
| Units | `F psi` has `J mol^-1`; barriers use `J mol^-1`; rates use `s^-1`; tail length in `Q` has capacity/charge units. |

## 3. Minimal Variables

| Symbol | Meaning | Origin class |
|---|---|---|
| `Q` | accumulated branch charge/capacity coordinate | definition |
| `v_Q` | positive scan speed `dQ/dt` | definition |
| `phi(Q)` | negative-electrode potential along branch | definition |
| `T` | temperature | definition |
| `theta` | actual transformed fraction of one graphite phase-transition mode | definition |
| `theta_e(phi,T)` | equilibrium transformed fraction | model assumption / thermodynamic state function |
| `r=theta_e-theta` | kinetic lag residual | definition |
| `C_b(phi,T)` | non-transition background differential capacity | model assumption |
| `Q_p` | charge/capacity scale coupled to the transition | model assumption |
| `psi` | signed assisting potential displacement | definition |
| `G_0^\ddagger(T)` | intrinsic activation free energy | thermodynamic work argument |
| `B` | nonnegative effective barrier used in rate | model assumption / derived |
| `k` | relaxation rate | standard kinetic relation |

## 4. Coordinate And Observables

Define branch coordinate and speed:

```tex
v_Q=\frac{dQ}{dt}>0.
```

ICA and DVA are calculus definitions:

```tex
\mathrm{ICA}=\frac{dQ}{d\phi},
\qquad
\mathrm{DVA}=\frac{d\phi}{dQ}.
```

When `phi(Q)` is locally monotone:

```tex
\mathrm{ICA}=\left(\frac{d\phi}{dQ}\right)^{-1}.
```

Origin: `definition`, `calculus`.

## 5. Equilibrium Target And Actual Fraction

Let `theta_e(phi,T)` be a smooth thermodynamic equilibrium transformed fraction for one phase-transition mode:

```tex
0\le\theta_e(\phi,T)\le1.
```

In the transition region, `theta_e` changes rapidly with `phi`; away from it, its derivative along the scan becomes small. No explicit logistic/Gaussian form is assumed in Chapter 1.

The actual fraction is `theta(Q)`. Kinetic lag is:

```tex
r(Q)=\theta_e(\phi(Q),T)-\theta(Q).
```

Origin: `definition`, `model assumption`.

## 6. Minimal Finite-Rate Law

Use the lowest-order relaxation law:

```tex
\frac{d\theta}{dt}=k\,[\theta_e(\phi,T)-\theta].
```

This is a model assumption: the actual phase fraction moves toward its current equilibrium target with one local rate `k`.

Convert to `Q` coordinate using `dQ/dt=v_Q`:

```tex
\frac{d\theta}{dQ}
=
\frac{k}{v_Q}\,[\theta_e-\theta]
=
\frac{k}{v_Q}r.
```

Origin: `model assumption`, then `derived`.

## 7. Residual Equation And Tail

Differentiate `r=theta_e-theta` with respect to `Q`:

```tex
\frac{dr}{dQ}
=
\frac{d\theta_e}{dQ}
-
\frac{d\theta}{dQ}.
```

Substitute the finite-rate law:

```tex
\frac{dr}{dQ}
=
\frac{d\theta_e}{dQ}
-
\frac{k}{v_Q}r.
```

Equivalently:

```tex
\frac{dr}{dQ}+\frac{k}{v_Q}r
=
\frac{d\theta_e}{dQ}.
```

This shows that the tail is not assumed. It is the homogeneous decay of residual lag after the equilibrium target stops moving strongly.

In the post-peak tail region:

```tex
\frac{d\theta_e}{dQ}\approx0.
```

Then:

```tex
\frac{dr}{dQ}\approx-\frac{k}{v_Q}r.
```

For locally constant `k/v_Q`:

```tex
r(Q)\approx r(Q_a)\exp\left[-\frac{Q-Q_a}{L_Q}\right],
\qquad
L_Q=\frac{v_Q}{k}.
```

Origin: `derived`.

## 8. Intrinsic Barrier And Potential Work

Let the intrinsic activation free energy be:

```tex
G_0^\ddagger(T)=H^\ddagger-T S^\ddagger.
```

This is the thermodynamic decomposition of activation free energy.

Let `psi` be the signed assisting potential displacement. If an effective molar charge number `z_eff` participates in the transformation coordinate, the electrical work scale is:

```tex
W_\phi=z_{\mathrm{eff}}F\psi.
```

`psi>0` is defined to assist forward transformation, so this work lowers the forward barrier. If only a fraction `alpha` of that work projects onto the rate-limiting coordinate:

```tex
G^\ddagger_{\mathrm{raw}}(T,\psi)
=
G_0^\ddagger(T)-\alpha z_{\mathrm{eff}}F\psi,
\qquad
0\le\alpha.
```

The nonnegative barrier used in a reduced rate law is:

```tex
B(T,\psi)=\max\!\left(G^\ddagger_{\mathrm{raw}}(T,\psi),0\right).
```

Origin: `thermodynamic work argument`, `model assumption`.

## 9. Rate And Tail Length

Use an Arrhenius-type reduced rate:

```tex
k(T,\psi)=k_0(T)\exp\!\left[-\frac{B(T,\psi)}{RT}\right].
```

Substitute into `L_Q=v_Q/k`:

```tex
L_Q(T,\psi)
=
\frac{v_Q}{k_0(T)}
\exp\!\left[\frac{B(T,\psi)}{RT}\right].
```

Origin: `standard kinetic relation`, `derived`.

## 10. Temperature Interpretation

Log form:

```tex
\ln L_Q
=
\ln v_Q-\ln k_0(T)+\frac{B(T,\psi)}{RT}.
```

Low-temperature long tail condition:

```text
if lower T reduces the net rate k, then L_Q increases.
```

High-temperature short tail condition:

```text
if higher T increases the net rate k, then L_Q decreases.
```

This avoids the overclaim that temperature always shortens the tail regardless of `H^\ddagger`, `S^\ddagger`, `k_0(T)`, and `psi`.

## 11. Present-Potential Effect

In the active-barrier region where `G_raw^\ddagger>0`:

```tex
\frac{\partial B}{\partial \psi}
=
-\alpha z_{\mathrm{eff}}F.
```

Therefore:

```tex
\frac{\partial \ln L_Q}{\partial \psi}
=
-\frac{\alpha z_{\mathrm{eff}}F}{RT}
\le0.
```

Thus a more favorable present potential lowers the effective barrier, increases the rate, and shortens the tail.

Origin: `derived`.

## 12. ICA Mapping From Incremental Conservation

Use a local incremental storage statement. A small charge increment is stored partly in background capacity and partly by changing the phase fraction:

```tex
dQ=C_b(\phi,T)\,d\phi+Q_p\,d\theta.
```

Divide by `dQ`:

```tex
1=C_b(\phi,T)\frac{d\phi}{dQ}
+Q_p\frac{d\theta}{dQ}.
```

Solve for slope:

```tex
\frac{d\phi}{dQ}
=
\frac{1-Q_p\,d\theta/dQ}{C_b(\phi,T)}.
```

Therefore:

```tex
\frac{dQ}{d\phi}
=
\frac{C_b(\phi,T)}{1-Q_p\,d\theta/dQ}.
```

In the post-peak tail:

```tex
\frac{d\theta}{dQ}
\approx
\frac{1}{L_Q}r(Q_a)
\exp\left[-\frac{Q-Q_a}{L_Q}\right].
```

Thus the ICA tail inherits the same kinetic scale `L_Q`; the observed amplitude is modulated by `C_b` and `Q_p`.

Origin: `calculus/conservation`, `derived`.

## 13. Assumptions And Validity Limits

- One phase-transition mode is derived first; multiple modes can be summed later.
- `theta_e` is smooth and has a localized transition region.
- The relaxation law is a minimal reduced-order kinetic model.
- `psi` is defined with the sign that assists forward transformation.
- `C_b` is locally nonzero so `dQ/dphi` is meaningful.
- Near exact peak centers, reciprocal-slope nonlinearity can be strong; Chapter 1 emphasizes tail logic.
- Peak area is not the central argument here.

## 14. Equation-Origin Table

| Equation | Origin class |
|---|---|
| `v_Q=dQ/dt>0` | definition |
| `ICA=dQ/dphi`, `DVA=dphi/dQ` | definition/calculus |
| `0<=theta_e<=1` | model assumption |
| `r=theta_e-theta` | definition |
| `dtheta/dt=k(theta_e-theta)` | model assumption |
| `dtheta/dQ=(k/v_Q)r` | derived |
| `dr/dQ+dtheta/dQ relation` | derived |
| `r(Q)=r(Q_a)exp[-(Q-Q_a)/L_Q]` | derived |
| `L_Q=v_Q/k` | derived |
| `G_0^\ddagger=H^\ddagger-TS^\ddagger` | thermodynamic work argument |
| `W_phi=z_eff F psi` | thermodynamic work argument |
| `G_raw^\ddagger=G_0^\ddagger-alpha z_eff F psi` | model assumption from work-lowering argument |
| `B=max(G_raw^\ddagger,0)` | model assumption |
| `k=k_0 exp[-B/(RT)]` | standard kinetic relation |
| `L_Q=(v_Q/k_0)exp[B/(RT)]` | derived |
| `dQ=C_b dphi+Q_p dtheta` | calculus/conservation model |
| `dQ/dphi=C_b/(1-Q_p dtheta/dQ)` | derived |

## Gate

Gate: `PASS_FIRST_PRINCIPLES_DERIVATION`

Status: PASS

Reason:

- all equations are newly introduced and origin-classified;
- old TeX equations are not cited or copied;
- the convention block requirement is incorporated;
- the derivation directly targets temperature and present-potential effects on ICA tail length.
