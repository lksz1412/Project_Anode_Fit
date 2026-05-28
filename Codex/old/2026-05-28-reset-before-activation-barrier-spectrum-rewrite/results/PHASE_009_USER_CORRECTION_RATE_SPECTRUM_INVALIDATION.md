# Phase 009 — User Correction: Barrier Is Not The Tail Kernel

## Summary

Gate result:

`INVALIDATE_CH1_V1_CORE_MODEL_LAYER`

The user objected that the Chapter 1 v1 manuscript still treats the activation barrier too directly, as if the stretched tail could be represented by a barrier-shaped object in the integral.

The objection is valid.

The core correction is:

- The observed ICA tail is not shaped directly by a barrier function.
- A barrier, if used, is a hidden variable that maps to a rate or relaxation length.
- The observed post-peak tail is an integral over relaxation modes.
- Long tails come from slow modes / large relaxation lengths, not from integrating a "barrier-shaped tail."

Therefore:

`graphite_ica_chapter1_clean_slate_v1.tex`

is not canonical.

## Corrected Conceptual Layering

### Wrong Layering In v1

The v1 manuscript was too close to this chain:

```text
potential + temperature
-> activation barrier
-> single rate
-> single exponential tail
-> ICA tail
```

This is not sufficient for the user's intended interpretation of stretched tails.

### Correct Layering

The corrected chain must be:

```text
domain / local transition environment
-> local relaxation rate k
-> local relaxation length L = v_Q/k
-> exponential residual kernel for that mode
-> integral over the relaxation-length spectrum
-> observed ICA tail
```

If an activation barrier is introduced, it enters only as a hidden variable that maps into `k` or `L`:

```text
barrier distribution rho_G(G)
-> rate distribution rho_k(k)
-> relaxation-length distribution rho_L(L)
-> tail kernel integral
```

The observable tail is not `rho_G(G)`.

## Corrected Mathematical Core

For a local transition mode indexed by `u`, define

```tex
\frac{\dd \theta_u}{\dd Q}
=
\frac{k_u}{v_Q}
\left(\theta_e-\theta_u\right)
```

and

```tex
r_u=\theta_e-\theta_u.
```

In the post-peak region where the equilibrium target forcing is small,

```tex
r_u(Q)
\simeq
r_u(Q_a)
\exp\!\left[-\frac{Q-Q_a}{L_u}\right],
\qquad
L_u=\frac{v_Q}{k_u}.
```

The total phase-progress contribution is not one exponential:

```tex
\frac{\dd \Theta}{\dd Q}
\simeq
\int_0^\infty
A(L;T,\psi)
\frac{1}{L}
\exp\!\left[-\frac{Q-Q_a}{L}\right]
\dd L .
```

Here:

- `A(L;T,\psi)` is the amplitude/weight spectrum of relaxation lengths.
- Long post-peak tails are controlled by the large-`L` part of this spectrum.
- Temperature and present potential act primarily by shifting or reshaping the rate/length spectrum.

If a barrier variable `G` is used only as a microscopic parameterization,

```tex
k(G,T,\psi)
=
k_0(T)
\exp\!\left[
-\frac{G-W_\psi}{RT}
\right]
```

in the applicable activated-rate range, then

```tex
L(G,T,\psi)
=
\frac{v_Q}{k_0(T)}
\exp\!\left[
\frac{G-W_\psi}{RT}
\right].
```

The transformation from barrier distribution to length distribution is nonlinear:

```tex
A_L(L;T,\psi)
\propto
\rho_G(G(L))
\left|
\frac{\dd G}{\dd L}
\right|
```

with

```tex
G(L)
=
W_\psi
+
RT\ln\left(\frac{k_0(T)L}{v_Q}\right),
\qquad
\frac{\dd G}{\dd L}
=
\frac{RT}{L}.
```

Thus the integral shape is a relaxation-kernel integral, not a barrier integral with the same shape.

## Required Rewrite Consequences

The next Chapter 1 rewrite must:

1. Make the relaxation-length spectrum primary.
2. Treat barrier only as one possible hidden parameterization of the rate spectrum.
3. Remove "single active barrier -> single tail length" as the central result.
4. Keep the single-exponential `L_Q=v_Q/k` only as one local mode.
5. Derive the observed tail as a mixture/integral of local exponential residual kernels.
6. Explain low-temperature long tails as a shift of weight toward larger `L`.
7. Explain high-temperature shorter tails as a shift of weight toward smaller `L`.
8. Explain present-potential assistance as a shift/compression of the relaxation-length spectrum, not as a direct visible barrier shape.
9. Re-run the 10-pass logic loop after this rewrite.

## Gate

Gate:

`INVALIDATE_CH1_V1_CORE_MODEL_LAYER`

Reason:

The current v1 manuscript contains useful residual equations, but its main explanatory layer is still too close to a single active-barrier/single-tail-length model. It does not yet match the user's integral-spectrum interpretation of stretched ICA tails.

