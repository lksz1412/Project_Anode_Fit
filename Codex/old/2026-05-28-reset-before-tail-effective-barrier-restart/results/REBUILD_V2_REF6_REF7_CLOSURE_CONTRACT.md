# Rebuild v2 Ref. 6/7 Closure Contract

Project: `D:\Projects\Project_Anode_Fit`

Plan: `D:\Projects\Project_Anode_Fit\Codex\plans\2026-05-27-graphite-ica-from-scratch-rebuild-plan-v2-canonical.md`

Phase: `Phase 007 - refs. 6/7 Closure Method Package`

Created: 2026-05-27

## Contract Role

This contract defines how refs. 6/7 may be used in the rebuilt graphite ICA/DVA manuscript. The permitted use is methodological: a reference-solution correction/ratio closure for a self-consistent integral problem. The forbidden use is physical: importing molecular-pair diffusion/reaction assumptions into graphite staging.

The exact graphite system remains the Phase 006 charge-balance-constrained DAE/Volterra formulation. The closure is an approximation or fitting surrogate placed after the exact formulation.

## Local Evidence For Refs. 6/7 In The 2017 Paper

| Evidence Item | Local Evidence | Claim Allowed |
|---|---|---|
| 2017 user paper PDF | `JCP_147(14)_144111_(2017) - Effects of external electric field.pdf`, pages 1-10 extracted text | The paper is local and was text-extracted in prior Phase 004. |
| in-text citation on page 2 | `ref6_ref7_method_notes.md`, "In-Text Uses" table | The 2017 paper says it uses the recently proposed method of refs. 6/7 for Fredholm second-kind equations. |
| in-text citation on page 5 | `ref6_ref7_method_notes.md`, "In-Text Uses" table | The 2017 paper identifies its derived equation for an unknown survival/separation quantity as a Fredholm second-kind equation and invokes refs. 6/7. |
| in-text citation on page 8 | `ref6_ref7_method_notes.md`, "In-Text Uses" table | The 2017 paper uses comparison with numerical results to support the utility of the refs. 6/7 method. |
| equation-glyph fidelity | `ref6_ref7_method_notes.md`, read coverage | Exact equation glyphs require visual/source checking before final transcription. |

## Bibliographic Entries

| Ref | Entry | DOI | Evidence Status |
|---|---|---|---|
| user paper | Kyusup Lee, Seonghoon Lee, Cheol Ho Choi, Sangyoub Lee, "Effects of external electric field and anisotropic long-range reactivity on charge separation probability," The Journal of Chemical Physics 147, 144111 (2017). | `10.1063/1.5000882` | local PDF text-extracted pages 1-10 |
| ref. 6 | S. Lee, C. Y. Son, J. Sung, and S. Chong, "Communication: Propagator for diffusive dynamics of an interacting molecular pair," The Journal of Chemical Physics 134, 121102 (2011). | `10.1063/1.3565476` | bibliographic metadata recorded in prior notes; original paper not yet READ_FULL |
| ref. 7 | C. Y. Son, J. Kim, J.-H. Kim, J. S. Kim, and S. Lee, "An accurate expression for the rates of diffusion-influenced bimolecular reactions with long-range reactivity," The Journal of Chemical Physics 138, 164123 (2013). | `10.1063/1.4802584` | bibliographic metadata recorded in prior notes; original paper not yet READ_FULL |

## Source Method Pattern From The 2017 Paper

The portable method pattern is:

1. reduce the physical problem to an integral equation in which the unknown appears both outside and inside the integral;
2. rewrite the expression to isolate the difficult unknown feedback as a relative ratio or correction rather than guessing the whole unknown function;
3. choose a simpler reference problem that is already solved or more stable;
4. replace the unknown ratio/correction with the reference ratio/correction;
5. obtain a closed approximation;
6. compare the closure against a direct numerical solution and state the regime where it fails.

In the 2017 paper, the physical problem is a long-range reaction/survival problem, and the equation type is described as Fredholm second-kind. In graphite, the primary exact formulation is not literally the same equation type; it is a causal charge-domain DAE/Volterra-like system. Therefore this manuscript may transfer the closure pattern, not the physical model or equation-type identity.

## Graphite Exact Problem To Which Closure May Apply

The exact graphite problem is defined by Phase 006:

\[
\mathcal{G}(V_n;q,T,\boldsymbol{\xi};\theta)=0,
\qquad
V_n=\mathcal{V}(q,T,\boldsymbol{\xi};\theta),
\]

\[
\frac{\mathrm{d}\xi_j}{\mathrm{d}q}
=
\frac{Q_{\mathrm{cell}}}{I_{\mathrm{abs}}}
k_j(V_n,q,T,I;\theta)
\left[
\xi_{j,\mathrm{eq}}(V_n,T)-\xi_j
\right],
\qquad I_{\mathrm{abs}}>0.
\]

The corresponding integral form is

\[
\xi_j(q)
=
\xi_j(q_0)
+
\int_{q_0}^{q}
\Psi_j(s,\boldsymbol{\xi}(s);\theta)
\,\mathrm{d}s,
\]

where

\[
\Psi_j(s,\boldsymbol{\xi}(s);\theta)
=
\frac{Q_{\mathrm{cell}}}{I_{\mathrm{abs}}(s)}
k_j(V_n(s),s,T(s),I(s);\theta)
\left[
\xi_{j,\mathrm{eq}}(V_n(s),T(s))-\xi_j(s)
\right],
\]

and \(V_n(s)=\mathcal{V}(s,T(s),\boldsymbol{\xi}(s);\theta)\).

This is the truth model. Any closure must approximate this model and be compared back to it.

## Why The Graphite Problem Is Not The Same Physical Problem

| Aspect | 2017/ref. 6/7 domain | Graphite ICA/DVA domain | Consequence |
|---|---|---|---|
| unknown | survival/separation probability | internal states and root-solved graphite potential | only mathematical self-consistency is portable |
| coordinate | molecular separation / reaction geometry | external charge coordinate `q` and time | do not import radial geometry |
| physics | geminate-pair diffusion and long-range reactivity | graphite storage, staging, and circuit charge balance | do not import reaction-pair assumptions |
| benchmark | finite-element/numerical solution of reaction problem | direct DAE/root-solve integration and data residuals | benchmark idea is portable, not the PDE |
| equation class | Fredholm second-kind in cited context | nonlinear DAE/Volterra-like primary form | do not label graphite as Fredholm without derivation |

## Direct DAE / Root-Solve Truth Model

The direct model is the baseline for all closures:

1. choose \(q_i,T_i,I_i\), initial \(\boldsymbol{\xi}_0\), and parameters \(\theta\);
2. solve \(\mathcal{G}(V_{n,i};q_i,T_i,\boldsymbol{\xi}_i;\theta)=0\);
3. evaluate \(\xi_{j,\mathrm{eq}}(V_{n,i},T_i)\) and \(k_j(V_{n,i},q_i,T_i,I_i;\theta)\);
4. update \(\boldsymbol{\xi}_{i+1}\);
5. repeat over the charge/time grid;
6. compute ICA/DVA observables and validation residuals.

The closure may be faster or more analytic, but it is not more fundamental than this model.

## Reference Path Options

### Quasi-Equilibrium Reference Path

\[
\xi_j^{\mathrm{ref}}(q)
=
\xi_{j,\mathrm{eq}}(V_{n,\mathrm{OCV}}(q,T),T).
\]

Use when the target is the thermodynamic dQ/dV shape and the current is low enough that kinetic lag is expected to be small.

### Low-Rate Direct-Solve Reference Path

Run the direct model at a low-rate condition or with rate parameters in a near-equilibrium regime:

\[
\boldsymbol{\xi}^{\mathrm{ref}}(q)
=
\boldsymbol{\xi}^{\mathrm{direct}}_{\mathrm{low\ rate}}(q).
\]

Use when quasi-equilibrium is too ideal but a stable numerical reference is available.

### Frozen-Feedback Reference Path

Freeze part of the feedback at a known or previous path:

\[
V_n^{\mathrm{ref}}(q)
=
\mathcal{V}(q,T,\boldsymbol{\xi}^{\mathrm{ref}}(q);\theta),
\]

then evaluate rates and equilibrium occupancies relative to that reference.

Use when a closed fitting expression is needed but a direct full feedback loop is too expensive.

## Default Reference Selection Criteria

| Criterion | Preferred Reference |
|---|---|
| low-rate thermodynamic shape only | quasi-equilibrium reference |
| moderate dynamic lag with stable numerical baseline | low-rate direct-solve reference |
| need analytic/fast fitting surrogate | frozen-feedback reference with strict residual gates |
| strong hysteresis, rest relaxation, or branch switching | no closure by default; use direct solve |
| denominator or correction ratio near singularity | use additive residual correction or direct solve |

Default for Chapter 1 wording: **quasi-equilibrium reference as a conceptual reference, direct root-solve as truth model, no validated closure claim yet**.

## Correction Functional

Define the direct integrand as \(\Psi_j(q,\boldsymbol{\xi};\theta)\) and the reference integrand as

\[
\Psi_j^{\mathrm{ref}}(q;\theta)
=
\Psi_j(q,\boldsymbol{\xi}^{\mathrm{ref}}(q);\theta).
\]

A multiplicative correction may be written as

\[
\mathcal{C}_j(q)
=
\frac{\Psi_j(q,\boldsymbol{\xi}(q);\theta)}
{\Psi_j^{\mathrm{ref}}(q;\theta)}.
\]

Then

\[
\xi_j(q)
=
\xi_j(q_0)
+
\int_{q_0}^{q}
\Psi_j^{\mathrm{ref}}(s;\theta)
\mathcal{C}_j(s)
\,\mathrm{d}s.
\]

The correction \(\mathcal{C}_j\) is dimensionless. It is acceptable only if its denominator is nonzero and well-conditioned, or if a regularized denominator is explicitly declared.

## Denominator Safety And Additive Fallback

If a ratio is used, require

\[
\left|\Psi_j^{\mathrm{ref}}(q;\theta)\right|
\ge
\epsilon_{\Psi,j}
\]

on the interval where the ratio is evaluated. If this fails, use an additive correction:

\[
\Delta_j(q)
=
\Psi_j(q,\boldsymbol{\xi}(q);\theta)
-
\Psi_j^{\mathrm{ref}}(q;\theta),
\]

\[
\xi_j(q)
=
\xi_j(q_0)
+
\int_{q_0}^{q}
\left[
\Psi_j^{\mathrm{ref}}(s;\theta)+\Delta_j(s)
\right]
\,\mathrm{d}s.
\]

The additive correction may be less scale-invariant, but it avoids a singular ratio when the reference integrand crosses zero.

## Closure Residual Against Direct Solve

The closure must be evaluated against a direct solution:

\[
r_{\xi,j}^{\mathrm{cl}}(q_i)
=
\xi_{j}^{\mathrm{closure}}(q_i)
-
\xi_{j}^{\mathrm{direct}}(q_i),
\]

\[
r_{V}^{\mathrm{cl}}(q_i)
=
V_{n}^{\mathrm{closure}}(q_i)
-
V_{n}^{\mathrm{direct}}(q_i).
\]

For observables:

\[
r_{\mathrm{ICA}}^{\mathrm{cl}}(q_i)
=
\left(\frac{\mathrm{d}Q_{\mathrm{ext}}}{\mathrm{d}V_{n,\mathrm{app}}}\right)_{\mathrm{closure},i}
-
\left(\frac{\mathrm{d}Q_{\mathrm{ext}}}{\mathrm{d}V_{n,\mathrm{app}}}\right)_{\mathrm{direct},i}.
\]

These residuals define validation targets. They are not yet measured results.

## Closure Acceptance Gates

| Gate | Required Check | Pass Meaning |
|---|---|---|
| exact-system separation | manuscript states direct root-solve model before closure | closure is not hidden as exact theory |
| charge-balance residual | `G(V_n;q,T,xi)/Q_cell` remains within tolerance for closure path | closure still respects charge conservation |
| state residual | `xi_closure - xi_direct` stays below tolerance | closure tracks direct state path |
| voltage residual | `V_closure - V_direct` stays below tolerance | voltage feedback is approximated acceptably |
| low-rate limit | closure approaches quasi-equilibrium/direct low-rate path | thermodynamic limit preserved |
| rest compatibility | rest is handled in time domain at fixed `q` | no invalid q-domain rest closure |
| denominator safety | ratio denominators remain above declared floor | no singular correction |
| observable residual | ICA/DVA residuals remain acceptable | fitting observable shape remains credible |

## Closure Rejection Conditions

| Condition | Rejection Reason |
|---|---|
| direct solver comparison is unavailable | cannot validate closure |
| correction ratio denominator crosses zero or becomes too small | ratio is ill-conditioned |
| closure violates charge-balance residual tolerance | closure breaks the exact constraint |
| closure shifts peaks by fitting `R_n` and kinetics without constraint | identifiability failure |
| high-rate behavior deviates beyond tolerance | closure outside intended regime |
| rest relaxation cannot be represented at fixed `q` | q-domain approximation misused |
| branch switching occurs without a rule | root selection is unstable |
| distributed barrier extension is added without new validation | overfitting risk |

## Low-Rate, High-Rate, Rest, And Distributed-Barrier Checks

Low-rate limit:

- closure should approach the equilibrium special-root path or a validated low-rate direct solve;
- the sign and ordering of ICA/DVA peak locations should remain consistent with the thermodynamic reference.

High-rate rejection:

- if dynamic lag, voltage shift, or state residuals exceed tolerance, the closure must be rejected for that rate regime;
- high-rate agreement cannot be assumed from low-rate success.

Rest relaxation:

- closure must switch to the time-domain fixed-\(q\) form during rest;
- if the closure cannot represent relaxation at fixed \(q\), it is not valid for rest data.

Distributed barriers:

- if a later model introduces \(\rho_j(g)\) or distributed transition barriers, the reference path and correction must be redefined over the distributed variable;
- single-barrier closure gates do not automatically transfer.

## Portable Method Parts

| Part | Portable To Graphite? | Graphite Use |
|---|---:|---|
| isolate unknown feedback as ratio/correction | yes | define \(\mathcal{C}_j(q)\) or \(\Delta_j(q)\) relative to a reference path |
| use simpler reference problem | yes | quasi-equilibrium, low-rate direct solve, or frozen-feedback path |
| obtain closed approximate expression | yes, conditionally | only after denominator and residual gates are stated |
| compare against direct numerical solution | yes | direct DAE/root-solve integration is benchmark |
| state approximation regime | yes | low-rate, high-rate, rest, branch, and denominator checks |
| molecular survival probability formula | no | not graphite physics |

## Non-Portable Assumptions

| Assumption | Status | Reason |
|---|---|---|
| geminate-pair recombination | non-portable | not graphite staging thermodynamics |
| Smoluchowski radial diffusion coordinate | non-portable | graphite coordinate is charge/time, not molecular separation |
| Coulomb or screened Coulomb pair potential | non-portable | graphite potential is charge-balance/internal electrochemical potential |
| contact sink or delta-sink reaction physics | non-portable | graphite has transition capacities and storage terms |
| Onsager distance / Debye-Huckel length | non-portable | no corresponding Chapter 1 graphite parameter |
| orientation averaging in external electric field | non-portable as physics | only the idea of regime/approximation control is portable |
| finite-element Smoluchowski benchmark | partly portable as benchmark concept | direct numerical comparison is portable, not the PDE |

## Manuscript Wording

Allowed wording:

> The closure strategy is inspired by the reference-solution correction approach used in refs. 6 and 7 for self-consistent integral equations, but the graphite formulation is first defined independently through charge balance and direct root-solve dynamics.

Allowed wording:

> In this work, refs. 6 and 7 motivate how a difficult feedback term may be approximated relative to a simpler reference problem. The molecular-pair physics of those references is not assumed for graphite.

Forbidden wording:

- "Refs. 6 and 7 solve the graphite DAE."
- "The graphite problem is Fredholm second-kind" unless a separate derivation proves that reformulation.
- "The ref. 6/7 approximation validates the fit" before direct-solver comparison.
- "The Coulomb/Onsager/contact-sink assumptions explain graphite staging."

## Citation Policy

| Source | When To Cite | Claim Strength |
|---|---|---|
| 2017 user paper | when describing local bridge evidence and how refs. 6/7 were used in that work | strong for local citation context |
| ref. 6 | when naming the original method source and bibliographic lineage | metadata/cautious method claim until full read |
| ref. 7 | when naming the rate-expression extension and bibliographic lineage | metadata/cautious method claim until full read |
| Phase 006 package | when defining graphite exact formulation | strong internal project source |
| future Phase 008 solver validation | when claiming closure accuracy | required before any performance claim |

## Conditions Requiring Full Original Refs. 6/7 Retrieval

Retrieve and full-read refs. 6/7 before any of the following:

- quoting or transcribing exact equations from ref. 6 or ref. 7;
- claiming a specific derivation step belongs to ref. 6 or ref. 7 rather than the 2017 paper;
- comparing mathematical error bounds from refs. 6/7 to graphite closure;
- using a ref. 6/7 equation number in final manuscript;
- making a stronger claim than "inspired by" or "methodologically analogous."

## Manuscript Claims Allowed

| Claim | Allowed Strength |
|---|---|
| refs. 6/7 are cited in the 2017 user paper as a method for Fredholm second-kind equations | strong from local PDF notes |
| the transferable pattern is reference-solution correction/ratio closure | cautious but usable |
| graphite exact system is DAE/Volterra-like, not literally the same physical problem | strong from Phase 006 and mapping notes |
| direct root-solve comparison is required before closure accuracy claims | strong |
| closure can be proposed as a fitting surrogate after exact formulation | conditional |

## Manuscript Claims Forbidden

| Forbidden Claim | Reason |
|---|---|
| closure is exact graphite theory | violates exact/approximate separation |
| graphite is Fredholm second-kind by default | not derived; primary form is DAE/Volterra-like |
| refs. 6/7 justify a physical LIB graphite assumption | non-portable physics |
| closure is validated without direct solver comparison | no validation artifact yet |
| original refs. 6/7 derivations were fully read | not recorded |
| exact equations from refs. 6/7 are visually verified | not recorded |

## Open Issues

| Issue | Status | Handling |
|---|---|---|
| full original refs. 6/7 unread | open | keep claims cautious; retrieve before stronger literature claims |
| exact equation glyphs visually unverified | open | do not transcribe exact PDF/ref equations |
| correction functional remains schematic | open | Phase 008 must turn this into solver/validation protocol |
| tolerance values undefined | open | Phase 008 defines residual thresholds |
| default reference path not user-approved | open | use quasi-equilibrium reference only as conceptual default |

## Phase 008 Dependency

Phase 008 must convert this contract into a direct solver and validation protocol. It must define grid inputs, root solve, state update, closure evaluation, residual tolerances, low-rate checks, high-rate rejection checks, and rest handling.

## Gate Statement

Gate: `PASS_REBUILD_V2_REF_CLOSURE`

This contract passes because it separates the exact graphite system from approximate closure, points refs. 6/7 claims to local evidence or recorded metadata, lists non-portable assumptions, requires direct-solver comparison, and places closure after the Phase 006 exact formulation.
