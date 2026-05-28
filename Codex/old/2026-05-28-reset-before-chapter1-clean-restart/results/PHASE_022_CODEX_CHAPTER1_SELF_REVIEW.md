# Phase 022 — Codex Chapter 1 Self Review

## Summary

Reviewed file:

`D:\Projects\Project_Anode_Fit\Codex\results\graphite_ica_chapter1_first_principles_final.tex`

Metadata:

| Item | Value |
|---|---|
| Lines | 446 |
| SHA256 | `55707E79469612B397DA1393197B022796A21CCE48C4E12832943070FD7F7A06` |

Gate result:

`REVIEWED_REQUIRES_REVISION_BEFORE_CANONICAL_USE`

The manuscript has a useful first-principles spine:

1. define convention;
2. define equilibrium fraction and actual fraction;
3. define residual lag;
4. derive the residual ODE;
5. derive `L_Q = v_Q/k`;
6. substitute an effective barrier into the rate;
7. map delayed phase progress into ICA.

However, it should not be treated as final canonical Chapter 1 yet. It has several important logic risks, especially around the effective barrier definition and the separation between equilibrium target motion and kinetic barrier lowering.

## Read Coverage

| Range | Status |
|---|---|
| Lines 1-240 | READ |
| Lines 241-446 | READ |

## Static Verification

| Check | Result |
|---|---|
| `\begin{document}` / `\end{document}` | 1 / 1 |
| Unescaped brace count | 331 / 331 |
| Labels | 23 |
| Duplicate labels | 0 |
| Missing `\ref`/`\eqref` targets | 0 |
| TeX engine availability | Not found: `xelatex`, `pdflatex`, `tectonic` |

Static structure passes, but PDF compilation was not verified because no TeX engine is available in the current environment.

## Findings

### P1 — The `max(G_raw,0)` barrier is too close to a physicalized cap

Location:

- Lines 242-251
- Lines 255-273
- Abstract lines 25-32

Issue:

The manuscript defines

```tex
B(T,\psi)=\max[G_{\raw}^\ddagger(T,\psi),0]
```

and then puts `B` directly into the main Arrhenius rate. This prevents negative barriers, but it also makes a hard capped barrier part of the core physical model. That is risky because the user explicitly wants a physical logic, not a solver/fitting stabilizer. It also creates a non-smooth transition at `G_raw = 0`.

Better treatment:

Use the active-barrier regime as the main derivation:

```tex
B_{\mathrm{act}}(T,\psi)
=
G_0^\ddagger(T)-\alpha z_{\mathrm{eff}}F\psi,
\qquad
B_{\mathrm{act}}>0.
```

Then state separately:

If `B_act <= 0`, the activation step is no longer the rate-limiting barrier in this reduced model. The rate should approach a prefactor-controlled or physically bottleneck-limited regime, not be silently repaired by a hard cap. Any saturation must come from attempt frequency, site availability, transport, phase-boundary motion, or current conservation.

### P1 — Potential-assisted barrier lowering is not yet thermodynamically closed

Location:

- Lines 97-102
- Lines 220-239
- Lines 253-278

Issue:

The same analysis potential `varphi` controls the equilibrium target `theta_e(varphi,T)` and also enters the kinetic assisting coordinate `psi = s_psi[varphi-varphi^star(T)]`. This can be correct, but only if the manuscript explains why this is not double counting.

Currently, `theta_e` and `psi` are introduced separately. The document does not yet derive the barrier-lowering term from a forward/backward transition-state picture or a reduced free-energy landscape. As written, a reviewer could ask:

"Is the thermodynamic driving force already contained in `theta_e`, and then counted again in `k`?"

Better treatment:

Add a short consistency subsection before the final rate expression:

1. `theta_e(varphi,T)` is the equilibrium or quasi-equilibrium target.
2. `k(T,psi)` is the mobility with which the actual state approaches that target.
3. Using `varphi` in both places is allowed only as a reduced model if an underlying forward/backward rate pair can be constructed whose stationary ratio recovers `theta_e`.
4. If such a construction is not provided in Chapter 1, the barrier-lowering term must be explicitly labeled as a constitutive mobility assumption.

### P2 — The ICA tail scale is derived in `Q`, not fully in voltage-axis ICA

Location:

- Lines 194-207
- Lines 343-413

Issue:

The manuscript correctly derives

```tex
r(Q) \sim \exp[-(Q-Q_a)/L_Q],
\qquad
L_Q=v_Q/k.
```

But ICA is plotted against voltage or potential. Lines 404-413 state that the ICA denominator has the same exponential scale `L_Q`, which is true in the `Q` coordinate, but a voltage-axis tail needs the local mapping between `Q` and `varphi`.

Better treatment:

Add a local voltage-axis conversion:

```tex
L_\varphi
\approx
\left|\frac{\dd\varphi}{\dd Q}\right|_{a} L_Q
```

or explicitly say that Chapter 1 first derives the capacity-axis kinetic tail length, and voltage-axis ICA tail length inherits it only through the local `Q <-> varphi` mapping.

### P2 — Monotonicity and sign assumptions need to be explicit

Location:

- Lines 95-115
- Lines 343-402

Issue:

The residual sign and ICA peak sign rely on assumptions that are not fully stated:

- `theta_e` increases along the chosen analysis branch near the transition.
- `Q_p > 0`.
- `C_b > 0`.
- The post-peak residual `r(Q_a)` is positive.
- The denominator `1 - Q_p dtheta/dQ` should remain positive or at least not cross zero in the tail region.

The convention section says `varphi` is chosen in the forward direction, but the local mathematical assumptions should be written next to the derivation. Otherwise the same equations could be read with the opposite branch sign.

Better treatment:

Add an "analysis branch assumptions" block before the residual derivation and repeat the ICA denominator condition as a tail-region validity condition.

### P2 — Projection coefficient `alpha` should be bounded or renamed

Location:

- Lines 227-239

Issue:

The text calls `alpha` a projection coefficient but only states `alpha >= 0`. A projection coefficient usually should satisfy `0 <= alpha <= 1`. If values above 1 are intended, then `alpha z_eff` is not simply a projection; it is an effective coupling coefficient.

Better treatment:

Either define:

```tex
0 \le \alpha \le 1
```

or replace `alpha z_eff` with a single effective coupling parameter:

```tex
\lambda_\psi \ge 0,
\qquad
G_{\raw}^\ddagger=G_0^\ddagger-\lambda_\psi F\psi.
```

### P3 — Equilibrium heterogeneity is dismissed too quickly

Location:

- Lines 61-70
- Lines 72-86

Issue:

The manuscript says equilibrium peak broadening alone is insufficient for the observed post-peak tail. That is probably directionally right for the user's observed temperature/C-rate behavior, but an equilibrium distribution of transition potentials or particle heterogeneity can also produce asymmetric-looking tails.

Better treatment:

Clarify that Chapter 1 is deriving the kinetic residual tail component, not proving that every observed tail must be kinetic. The stronger claim should be:

Equilibrium broadening can shape the peak, but a temperature- and present-potential-dependent residual post-peak decay is naturally explained by finite kinetic relaxation.

### P3 — Activation enthalpy and entropy are treated as constants without saying local approximation

Location:

- Lines 211-218

Issue:

`G_0^\ddagger(T)=H^\ddagger-TS^\ddagger` is fine as a local activation free-energy representation, but `H^\ddagger` and `S^\ddagger` may themselves be weakly temperature-dependent.

Better treatment:

State that this is a local temperature-window approximation, or write `H^\ddagger(T)` and `S^\ddagger(T)` if broader temperature ranges are intended.

## What Is Good And Should Be Kept

### 1. The residual equation is the strongest part

Lines 149-207 are the core of the manuscript and should be preserved. The forced residual ODE is exactly the kind of no-leap derivation the user requested:

```tex
\frac{\dd r}{\dd Q}
+
\frac{k}{v_Q}r
=
\frac{\dd\theta_e}{\dd Q}
```

This cleanly explains why post-peak tail length is controlled by `v_Q/k`.

### 2. The manuscript correctly avoids peak-area centered logic

Lines 432-440 keep the focus on tail length and effective barrier rather than peak area. This matches the user's correction.

### 3. The convention-first structure is correct

Lines 35-57 are useful. The document starts like a review-style chapter and fixes the branch, coordinate, ICA/DVA, tail direction, sign, and unit conventions before deriving anything.

### 4. Chapter 2-5 are kept as roadmap only

Lines 57 and 442-444 keep heat, electrochemical kinetics, thermal terms, and hysteresis outside Chapter 1. This matches the user's requested chapter structure.

## Recommended Revision Strategy

Do not throw away the manuscript. The residual-tail spine is good.

Revise Chapter 1 in place conceptually, but create a new file rather than overwriting the reviewed final:

Suggested new output:

`D:\Projects\Project_Anode_Fit\Codex\results\graphite_ica_chapter1_first_principles_final_v2.tex`

Minimum revision steps:

1. Add branch monotonicity and sign assumptions.
2. Replace `B=max(G_raw,0)` as the central equation with an active-barrier regime plus separate barrier-exhausted/bottleneck regime.
3. Add a consistency subsection explaining how `theta_e(varphi,T)` and `k(T,psi)` avoid double counting.
4. Bound or rename `alpha`.
5. Add voltage-axis tail conversion or explicitly limit `L_Q` to capacity-axis tail length.
6. Soften the equilibrium-insufficiency claim to allow equilibrium heterogeneity while preserving the kinetic-tail argument.
7. Add local-temperature-window caveat for activation enthalpy/entropy.

## Gate

Gate:

`REVIEWED_REQUIRES_REVISION_BEFORE_CANONICAL_USE`

Reason:

The manuscript has the correct central residual-tail derivation, but the effective-barrier and ICA-axis mapping need repair before it should be treated as a finished Chapter 1 theory document.
