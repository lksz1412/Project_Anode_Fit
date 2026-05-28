# Phase 010 — Barrier Distribution Extension

## Summary

This phase derives the optional kinetic barrier-distribution extension. The extension does not replace the single-barrier Chapter 1 logic. It generalizes the tail from one local exponential scale to a weighted sum or integral of exponential relaxation scales.

Gate result: `PASS_BARRIER_DISTRIBUTION_EXTENSION`

## Step Range

Planned steps: 159-176

Actual steps completed: 159-176

## Source Basis

| Element | Source |
|---|---|
| corrected kinetic barrier distribution support | `graphite_ica_charge_balance_ver1_rechecked2.tex:320-350` |
| warning that `rho_j(g)` is not equilibrium-center distribution | `graphite_ica_charge_balance_ver1_rechecked2.tex:320-326` |
| distribution rate and progress | `graphite_ica_charge_balance_ver1_rechecked2.tex:328-350` |
| older high-barrier long-tail interpretation | `graphite_ica_dynamic_ver5.tex:286-323` |

## 1. Distribution Meaning

Let `g` be a nonnegative kinetic activation barrier coordinate. Define:

```tex
\int_0^\infty \rho_j(g)\,dg=1.
```

Here `rho_j(g)` is a kinetic activation-barrier distribution.

It is not:

- a distribution of equilibrium transition-center potentials `U_j`;
- a distribution of equilibrium widths `w_j`;
- a visual peak-shape distribution;
- a threshold rule saying every domain below some barrier has already completed.

If equilibrium transition centers are heterogeneous, that should be modeled separately, for example with `p_j(U)`, not by reusing `rho_j(g)`.

## 2. Barrier And Rate For Each Group

For a group with barrier `g`, define:

```tex
\Delta G_{\eff,j}(g)
=g-\chi_j\mathcal A_j.
```

Use the same positive-barrier regularization:

```tex
\Delta G_{\eff,j}^{+}(g)
=\epsilon_G\ln\left[
1+\exp\left(\frac{g-\chi_j\mathcal A_j}{\epsilon_G}\right)
\right].
```

Then:

```tex
\boxed{
k_j(g)
=\nu_j(T)\exp\!\left[-\frac{\Delta G_{\eff,j}^{+}(g)}{RT}\right]
}
```

## 3. Progress Equation For Each Group

Each barrier group relaxes toward the same equilibrium progress target:

```tex
\frac{d\xi_j(g,t)}{dt}
=k_j(g)\left[\xi_{j,\mathrm{eq}}(V_n,T)-\xi_j(g,t)\right].
```

In constant-current `q` coordinate:

```tex
\boxed{
\frac{d\xi_j(g,q)}{dq}
=\left(\frac{Q_{\cell}}{|I|}\right)
\,k_j(g)\left[\xi_{j,\mathrm{eq}}(V_n,T)-\xi_j(g,q)\right].
}
```

## 4. Total Progress

The total progress is the barrier-weighted average:

```tex
\boxed{
\xi_j(q)
=\int_0^\infty\rho_j(g)\xi_j(g,q)\,dg.
}
```

Therefore:

```tex
\boxed{
\frac{d\xi_j}{dq}
=
\int_0^\infty\rho_j(g)
\frac{d\xi_j(g,q)}{dq}
\,dg.
}
```

This is the term that enters the Phase 009 ICA/DVA mapping.

## 5. Distributed Tail Scale

For each barrier group, define:

```tex
\kappa_j(g)
=\left(\frac{Q_{\cell}}{|I|}\right)k_j(g),
\qquad
\ell_{q,j}(g)=\frac{1}{\kappa_j(g)}
=\frac{|I|}{Q_{\cell}k_j(g)}.
```

Substitute the rate:

```tex
\ell_{q,j}(g)
=
\frac{|I|}{Q_{\cell}\nu_j(T)}
\exp\!\left[\frac{\Delta G_{\eff,j}^{+}(g)}{RT}\right].
```

Post-peak, if `xi_eq` is locally saturated:

```tex
u_j(g,q)
\approx
u_j(g,q_a)
\exp\left[-\frac{q-q_a}{\ell_{q,j}(g)}\right].
```

Thus:

```tex
\frac{d\xi_j}{dq}
\approx
\int_0^\infty
\rho_j(g)\,
\kappa_j(g)u_j(g,q_a)
\exp\left[-\frac{q-q_a}{\ell_{q,j}(g)}\right]
\,dg.
```

This is a weighted integral of exponentials. A broad high-barrier tail in `rho_j(g)` creates a long observable tail because high `g` gives small `k_j(g)` and large `ell_q,j(g)`.

## 6. Temperature And Present-Potential Effects

Temperature:

```text
higher T
  -> smaller barrier penalty through RT and often larger nu_j(T)
  -> k_j(g) increases for many g groups
  -> ell_q,j(g) decreases
  -> distributed tail contracts.
```

Present-potential assistance:

```text
larger favorable A_j
  -> g - chi_j A_j decreases
  -> DeltaG_eff^+(g) decreases
  -> k_j(g) increases
  -> ell_q,j(g) decreases
  -> high-barrier groups catch up sooner.
```

Therefore the distribution extension preserves the user's core interpretation: the tail is long at low temperature or weak assistance, and shorter at high temperature or stronger favorable present-potential assistance.

## 7. Relation To Ref. 6/7 Method

Phase 004 verified that refs. 6 and 7 provide a method for Fredholm integral equations of the second kind. The present distribution extension does not yet require importing that method because the model remains a set of barrier-resolved relaxation equations plus an integral average over `g`.

Ref. 6/7 becomes relevant only if a later derivation rewrites the barrier-averaged problem as a self-referential Fredholm-type integral equation. That has not been done in Chapter 1.

Decision:

```text
METHOD_NOT_IMPORTED_IN_PHASE_010_CORE_EXTENSION
```

## 8. Non-Threshold Rule

This extension must not be explained as:

```text
domains with g below a cutoff transform immediately;
domains with g above the cutoff remain untransformed.
```

The correct explanation is:

```text
every barrier group has a finite relaxation rate;
low-barrier groups relax quickly;
high-barrier groups relax slowly;
the observed tail is the remaining contribution of slow groups.
```

This is consistent with the user's request to avoid logical shortcuts and with the corrected source note that the model uses phase-progress dynamics rather than barrier-threshold completion.

## Validation

| Check | Result |
|---|---|
| `rho_j(g)` support set to `g>=0` | PASS |
| `rho_j(g)` classified as kinetic barrier distribution | PASS |
| Equilibrium center distribution kept separate | PASS |
| `DeltaG_eff(g)=g-chi A` defined | PASS |
| positive barrier and rate for each `g` defined | PASS |
| `d xi(g)/dt` and `d xi(g)/dq` defined | PASS |
| total `xi_j` and `d xi_j/dq` obtained by integral over `g` | PASS |
| distributed tail shown as weighted integral of exponentials | PASS |
| high-barrier long-tail interpretation derived | PASS |
| ref. 6/7 not imported prematurely | PASS |
| threshold-completion interpretation rejected | PASS |

## Gate

Gate: `PASS_BARRIER_DISTRIBUTION_EXTENSION`

Status: PASS

Reason:

- the extension is kinetic and line-grounded;
- it preserves the single-barrier derivation while explaining longer non-single-exponential tails;
- it avoids confusing kinetic barrier heterogeneity with equilibrium peak-position heterogeneity;
- it does not import Fredholm methods before a matching graphite integral equation exists.

## Confirmed Non-Changes

- No source `.tex` file was modified.
- No PDF was modified.
- `D:\Projects\Project_Anode_Fit\Claude` was not modified.
- No commit, push, merge, or branch operation was performed.

## Open Issues / Decision Queue

| Issue | Status |
|---|---|
| Final manuscript should decide whether distribution extension belongs in Chapter 1 main body or final subsection | pending Phase 011 |
| Need full logic audit after manuscript draft | pending Phase 012 |

No user decision is required before Phase 011.

## Next

Proceed directly to Phase 011 — Manuscript Draft From Scratch.
