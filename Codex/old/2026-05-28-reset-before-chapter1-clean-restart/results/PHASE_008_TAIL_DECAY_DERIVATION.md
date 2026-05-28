# Phase 008 — Tail Decay Derivation

## Summary

This phase derives the local peak-tail decay scale from the phase-progress relaxation equation. The tail is not asserted from a fitted peak shape; it follows from the residual lag between the equilibrium progress `xi_{j,\eq}` and the actual progress `xi_j`.

Gate result: `PASS_TAIL_DECAY_DERIVATION`

## Step Range

Planned steps: 113-136

Actual steps completed: 113-136

## Source Basis

| Element | Source |
|---|---|
| constant-current coordinate `dq/dt=|I|/Q_cell` | `graphite_ica_charge_balance_ver1_rechecked2.tex:95-106` |
| relaxation equation in time | `graphite_ica_charge_balance_ver1_rechecked2.tex:268-277` |
| relaxation equation in charge coordinate | `graphite_ica_charge_balance_ver1_rechecked2.tex:279-286` |
| C-rate competition | `graphite_ica_charge_balance_ver1_rechecked2.tex:414-418` |
| effective barrier rate | `graphite_ica_charge_balance_ver1_rechecked2.tex:240-266`; Phase 007 |

## 1. Time-Domain Relaxation

For transition `j`, the actual phase progress relaxes toward the equilibrium target:

```tex
\frac{d\xi_j}{dt}
=k_j\left[\xi_{j,\mathrm{eq}}-\xi_j\right].
```

Here:

- `xi_{j,\mathrm{eq}}` is the equilibrium target determined by internal potential and temperature;
- `xi_j` is the actual phase progress;
- `k_j` is the effective-barrier-controlled relaxation rate.

If `xi_j < xi_{j,\mathrm{eq}}`, the bracket is positive and the transition progresses forward. If `xi_j=xi_{j,\mathrm{eq}}`, the local relaxation term vanishes.

## 2. Convert Time To Charge Coordinate

At constant current:

```tex
q=\frac{Q_{\ext}}{Q_{\cell}},
\qquad
\frac{dq}{dt}=\frac{|I|}{Q_{\cell}}.
```

By the chain rule:

```tex
\frac{d\xi_j}{dt}
=\frac{d\xi_j}{dq}\frac{dq}{dt}
=\frac{d\xi_j}{dq}\frac{|I|}{Q_{\cell}}.
```

Insert the relaxation equation:

```tex
\frac{d\xi_j}{dq}\frac{|I|}{Q_{\cell}}
=k_j\left[\xi_{j,\mathrm{eq}}-\xi_j\right].
```

Multiply both sides by `Q_cell/|I|`:

```tex
\boxed{
\frac{d\xi_j}{dq}
=\left(\frac{Q_{\cell}}{|I|}\right)
\,k_j\left[\xi_{j,\mathrm{eq}}-\xi_j\right].
}
```

Define the charge-coordinate relaxation coefficient:

```tex
\kappa_j(q)
=\left(\frac{Q_{\cell}}{|I|}\right)k_j(q).
```

Then:

```tex
\frac{d\xi_j}{dq}
=\kappa_j(q)\left[\xi_{j,\mathrm{eq}}(q)-\xi_j(q)\right].
```

## 3. Define The Tail Residual

Define the local residual lag:

```tex
u_j(q)=\xi_{j,\mathrm{eq}}(q)-\xi_j(q).
```

Differentiate:

```tex
\frac{du_j}{dq}
=\frac{d\xi_{j,\mathrm{eq}}}{dq}
-\frac{d\xi_j}{dq}.
```

Substitute the charge-coordinate relaxation equation:

```tex
\frac{du_j}{dq}
=\frac{d\xi_{j,\mathrm{eq}}}{dq}
-\kappa_j(q)u_j(q).
```

Equivalently:

```tex
\frac{du_j}{dq}
+\kappa_j(q)u_j(q)
=\frac{d\xi_{j,\mathrm{eq}}}{dq}.
```

This equation is important because it shows the exact local condition under which a pure exponential tail appears. The residual is not always a pure exponential; it is forced by any continuing motion of the equilibrium target.

## 4. General Residual Solution

Let:

```tex
K(q_a,q)=\int_{q_a}^{q}\kappa_j(r)\,dr.
```

The linear equation

```tex
\frac{du_j}{dq}+\kappa_j(q)u_j(q)
=\frac{d\xi_{j,\mathrm{eq}}}{dq}
```

has the solution:

```tex
u_j(q)
=u_j(q_a)\exp[-K(q_a,q)]
+\int_{q_a}^{q}
\exp[-K(s,q)]
\frac{d\xi_{j,\mathrm{eq}}(s)}{ds}
\,ds.
```

Interpretation:

- the first term is decay of the lag already present at `q_a`;
- the second term is new lag generated while the equilibrium target is still changing;
- the post-peak tail is controlled by the first term once `d xi_eq/dq` becomes small after the equilibrium transition region.

## 5. Local Tail Approximation

In the tail region after the equilibrium transition has mostly moved through:

```tex
\frac{d\xi_{j,\mathrm{eq}}}{dq}\approx 0.
```

Then:

```tex
\frac{du_j}{dq}\approx-\kappa_j(q)u_j(q).
```

Therefore:

```tex
u_j(q)
\approx
u_j(q_a)\exp\left[
-\int_{q_a}^{q}\kappa_j(s)\,ds
\right].
```

Equivalent compact form:

```tex
u_j(q)
\approx
u_j(q_a)\exp\!\left[-\int_{q_a}^{q}\kappa_j(s)\,ds\right].
```

If `kappa_j` is locally constant:

```tex
u_j(q)
\approx
u_j(q_a)\exp[-\kappa_j(q-q_a)].
```

Define the local charge-coordinate tail length:

```tex
\boxed{
\ell_{q,j}=\frac{1}{\kappa_j}
}
```

so that:

```tex
u_j(q)
\approx
u_j(q_a)\exp\left[-\frac{q-q_a}{\ell_{q,j}}\right].
```

## 6. Tail Scale In Terms Of Rate

Since:

```tex
\kappa_j=\left(\frac{Q_{\cell}}{|I|}\right)k_j,
```

the local charge-coordinate tail length is:

```tex
\boxed{
\ell_{q,j}
=\frac{|I|}{Q_{\cell}k_j}
}
```

This is the first key tail result.

Meaning:

- small `k_j` gives large `ell_q,j`, hence a long tail in `q`;
- large `k_j` gives small `ell_q,j`, hence a short tail in `q`;
- increasing `|I|` lengthens the `q`-tail if `k_j` is held fixed, because the system has less time per unit `q`.

## 7. Substitute The Effective-Barrier Rate

From Phase 007:

```tex
k_j
=\nu_j(T)\exp\!\left(-\frac{\Delta G_{\eff,j}^{+}}{RT}\right).
```

Therefore:

```tex
\ell_{q,j}
=\frac{|I|}{Q_{\cell}\nu_j(T)}
\exp\!\left(\frac{\Delta G_{\eff,j}^{+}}{RT}\right).
```

Boxed local tail scale:

```tex
\boxed{
\ell_{q,j}(q,T,I)
=\frac{|I|}{Q_{\cell}\nu_j(T)}
\exp\!\left[
\frac{\Delta G_{\eff,j}^{+}(q,T,I)}{RT}
\right]
}
```

This is the second key tail result.

## 8. Low-Temperature Long-Tail Limit

The logarithmic form is:

```tex
\ln \ell_{q,j}
=\ln |I|-\ln Q_{\cell}-\ln \nu_j(T)
+\frac{\Delta G_{\eff,j}^{+}}{RT}.
```

At lower temperature:

- `RT` is smaller, so a positive barrier gives a larger exponential factor;
- `nu_j(T)` may also decrease in thermally activated processes;
- the net result is often larger `ell_q,j`, consistent with a longer tail.

Careful qualification:

This is not a blanket statement that every parameter always makes the tail longer at low `T`. It is the model condition for the observed trend: low temperature produces long tails when the net temperature dependence reduces `k_j`.

## 9. High-Temperature Short-Tail Limit

At higher temperature:

- `RT` is larger, reducing the exponential penalty of a positive barrier;
- `nu_j(T)` often increases;
- if the net effect increases `k_j`, then `ell_q,j=|I|/(Q_cell k_j)` decreases.

This explains why the observed high-temperature peak tail can end more quickly.

## 10. Present-Potential Barrier-Lowering Effect

The effective barrier is:

```tex
\Delta G_{\eff,j}
=\Delta G_{a,j}(T)-\chi_j\mathcal A_j.
```

For the softplus barrier:

```tex
\Delta G_{\eff,j}^{+}
=\epsilon_G\ln\left[1+\exp\left(\frac{\Delta G_{\eff,j}}{\epsilon_G}\right)\right].
```

Let:

```tex
\sigma(x)=\frac{1}{1+\exp(-x)}.
```

Then:

```tex
\frac{\partial \Delta G_{\eff,j}^{+}}{\partial \Delta G_{\eff,j}}
=\sigma\!\left(\frac{\Delta G_{\eff,j}}{\epsilon_G}\right)
```

and:

```tex
\frac{\partial \Delta G_{\eff,j}}{\partial \mathcal A_j}
=-\chi_j.
```

Since:

```tex
\ln\ell_{q,j}
=\ln |I|-\ln Q_{\cell}-\ln\nu_j(T)
+\frac{\Delta G_{\eff,j}^{+}}{RT},
```

we obtain:

```tex
\boxed{
\frac{\partial \ln \ell_{q,j}}{\partial \mathcal A_j}
=
-\frac{\chi_j}{RT}\,
\sigma\!\left(\frac{\Delta G_{\eff,j}}{\epsilon_G}\right)
}
```

For `chi_j>=0`, this derivative is nonpositive. Therefore favorable present-potential assistance shortens the charge-coordinate tail:

```text
A_j increases
  -> Delta G_eff decreases
  -> Delta G_eff^+ decreases
  -> ln ell_q decreases
  -> ell_q decreases
  -> tail shortens.
```

## 11. C-Rate Competition

The tail scale is:

```tex
\ell_{q,j}
=\frac{|I|}{Q_{\cell}k_j(T,I)}.
```

Taking a logarithmic derivative with respect to current magnitude:

```tex
\frac{\partial\ln \ell_{q,j}}{\partial\ln |I|}
=1-\frac{\partial\ln k_j}{\partial\ln |I|}.
```

Therefore:

```text
if k_j is independent of |I|:
  larger |I| lengthens the q-tail.

if larger |I| raises V_drive and k_j:
  the result depends on whether k_j grows faster or slower than |I|.

if partial ln k_j / partial ln |I| > 1:
  drive-enhanced kinetics can overcompensate residence-time loss and shorten the q-tail.
```

This is why the source says C-rate effects are a competition between residence time and drive-enhanced rate, not a one-direction rule.

## 12. Approximation Conditions

The simple exponential tail scale is valid locally when:

- `d xi_eq/dq` is small in the post-peak tail region;
- `kappa_j(q)` changes slowly across the fitted local tail segment;
- the single transition `j` dominates the observed tail segment;
- charge-balance differentiation does not become singular;
- `R_n` and `k_j` are not both freely assigned the same broadening.

It can fail when:

- the equilibrium target is still moving strongly;
- multiple nearby transitions overlap;
- a broad kinetic barrier distribution produces a sum of exponentials rather than one local exponential;
- branch hysteresis or heat coupling becomes first-order important;
- apparent-voltage shifts are double-counted as both equilibrium displacement and kinetic acceleration.

## 13. Algebra Audit

| Step | Result |
|---|---|
| `d xi/dt = k(xi_eq-xi)` | PASS |
| `dq/dt=|I|/Q_cell` | PASS |
| chain rule gives `d xi/dq=(Q_cell/|I|)k(xi_eq-xi)` | PASS |
| residual `u=xi_eq-xi` gives `u'=xi_eq'-kappa u` | PASS |
| local post-peak condition `xi_eq'≈0` gives `u'=-kappa u` | PASS |
| integral solution gives exponential decay for constant/slow `kappa` | PASS |
| `ell_q=1/kappa=|I|/(Q_cell k)` | PASS |
| substituting Arrhenius rate gives `ell_q=|I|/(Q_cell nu) exp(DeltaG_eff^+/(RT))` | PASS |

## 14. Limiting-Case Audit

| Limit | Model behavior | Interpretation |
|---|---|---|
| `k_j -> 0` | `ell_q -> infinity` | very slow transition gives long tail |
| `k_j -> nu_j` | `ell_q -> |I|/(Q_cell nu_j)` | prefactor-limited shortest local tail at that current |
| `|I| -> 0` with finite `k_j` | `ell_q -> 0` | quasi-equilibrium following in charge coordinate |
| favorable `A_j` increases | `ell_q` decreases | present potential lowers barrier and shortens tail |
| adverse `A_j` decreases | `ell_q` increases | barrier rises and lag persists |
| higher `T` increases net `k_j` | `ell_q` decreases | high-temperature short-tail observation |
| lower `T` decreases net `k_j` | `ell_q` increases | low-temperature long-tail observation |

## 15. User-Observation Alignment

The user's observation is represented directly:

```text
low T
  -> smaller net k_j
  -> larger ell_q,j
  -> longer tail

high T
  -> larger net k_j
  -> smaller ell_q,j
  -> shorter tail

favorable present electrode potential
  -> larger A_j
  -> lower DeltaG_eff^+
  -> larger k_j
  -> smaller ell_q,j
  -> faster tail decay
```

This also explains why an equilibrium Gaussian-like peak is insufficient. Equilibrium width controls the target curve `xi_eq`; the tail length comes from how slowly `xi_j` catches that target.

## Validation

| Check | Result |
|---|---|
| Started from `d xi_j/dt=k_j[xi_eq-xi]` | PASS |
| Used constant-current `dq/dt=|I|/Q_cell` | PASS |
| Converted to `d xi_j/dq=(Q_cell/|I|)k_j[xi_eq-xi]` | PASS |
| Defined residual `u_j=xi_eq-xi_j` | PASS |
| Derived exact residual equation with forcing `d xi_eq/dq` | PASS |
| Derived local exponential tail under post-peak approximation | PASS |
| Defined `kappa_j=(Q_cell/|I|)k_j` | PASS |
| Defined `ell_q,j=1/kappa_j=|I|/(Q_cell k_j)` | PASS |
| Substituted effective-barrier rate | PASS |
| Derived `ell_q,j=|I|/[Q_cell nu_j(T)] exp[DeltaG_eff^+/(RT)]` | PASS |
| Low-T and high-T limits checked with net-rate qualification | PASS |
| Present-potential tail-shortening derivative checked | PASS |
| C-rate competition stated | PASS |
| Approximation limits stated | PASS |

## Gate

Gate: `PASS_TAIL_DECAY_DERIVATION`

Status: PASS

Reason:

- tail length is derived from the relaxation equation rather than asserted;
- the residual equation exposes the approximation behind a pure exponential tail;
- the final local tail scale follows algebraically from the effective-barrier rate;
- the result matches the user’s low-temperature long-tail and high-temperature short-tail observation under stated net-rate conditions.

## Confirmed Non-Changes

- No source `.tex` file was modified.
- No PDF was modified.
- `D:\Projects\Project_Anode_Fit\Claude` was not modified.
- No commit, push, merge, or branch operation was performed.

## Open Issues / Decision Queue

| Issue | Status |
|---|---|
| ICA/DVA observable mapping still needs charge-balance audit | pending Phase 009 |
| Barrier-distribution extension may convert one exponential into a sum or integral of exponentials | pending Phase 010 |
| Whether derivative `partial ln ell / partial A` belongs in main text or appendix | pending Phase 011 |

No user decision is required before Phase 009.

## Next

Proceed directly to Phase 009 — ICA/DVA Observable Mapping.
