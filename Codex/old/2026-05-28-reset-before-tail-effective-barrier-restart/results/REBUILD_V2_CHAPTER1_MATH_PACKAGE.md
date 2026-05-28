# Rebuild v2 Chapter 1 Mathematical Foundation Package

Project: `D:\Projects\Project_Anode_Fit`

Plan: `D:\Projects\Project_Anode_Fit\Codex\plans\2026-05-27-graphite-ica-from-scratch-rebuild-plan-v2-canonical.md`

Phase: `Phase 006 - Chapter 1 Mathematical Foundation Package`

Created: 2026-05-27

## Package Role

This package is the mathematical content basis for the rebuilt Chapter 1. It is not the final LaTeX manuscript file. It fixes the equations, logical order, allowed claims, forbidden claims, and open risks that must be respected when the blank manuscript is assembled later.

Chapter 1-ready status: **ready as a mathematical package, not yet final manuscript body**.

## Chapter 1 Problem Statement

LIB graphite ICA/DVA fitting should not begin from a prescribed empirical anode OCV curve as though that curve were the dynamic internal voltage. The measured coordinate is the external charge passed through the circuit, while the graphite internal potential must be solved from the charge stored in background storage and staging-transition states. The central task of Chapter 1 is therefore to define the map

\[
(q,T,\boldsymbol{\xi}) \longmapsto V_n
\]

through charge conservation, and only then to define apparent voltage, dynamic relaxation, and derivative observables.

The role of the chapter is to turn the apparent feedback loop

\[
\boldsymbol{\xi} \rightarrow V_n \rightarrow \boldsymbol{\xi}_{\mathrm{eq}}(V_n,T), k_j(V_n,\cdots) \rightarrow \boldsymbol{\xi}
\]

into a well-defined self-consistent mathematical problem. Once `V_n` is explicitly defined as a root of charge balance, the feedback is no longer a hidden logical contradiction. It becomes a nonlinear DAE/Volterra-like formulation that can be solved directly or approximated by a controlled reference-closure method in later phases.

## Why An OCV-Input-Only Formulation Is Insufficient

An OCV-input-only formulation treats an empirical equilibrium-voltage curve indexed only by \(q\) and \(T\) as though it were the primary voltage available at every dynamic state. That reverses the dependency order. In a staged graphite model, the state variables \(\xi_j\) also store charge, and the same external \(q\) can correspond to different internal distributions during dynamic relaxation or hysteretic paths. Therefore a dynamic voltage cannot be obtained by reading only a scalar OCV curve against \(q\).

The corrected formulation is:

1. measure or define \(Q_{\mathrm{ext}}\), \(Q_{\mathrm{cell}}\), \(q\), and \(T\);
2. define storage terms and internal states using a dummy voltage \(V\);
3. impose charge balance;
4. solve the internal potential \(V_n\);
5. define equilibrium OCV only as the special state where all \(\xi_j\) are at equilibrium.

This is the first major logical repair relative to the old ver5 direction.

## Analysis Interval And Endpoint Convention

Let the analysis interval be \(t\in[t_0,t_1]\). The current convention must be fixed before equations are used. For this package, \(I_{\mathrm{abs}}(t)=|I(t)|\) denotes the current magnitude after the charge/discharge orientation has been handled separately.

\[
Q_{\mathrm{ext}}(t)=\int_{t_0}^{t} I_{\mathrm{abs}}(t')\,\mathrm{d}t',
\qquad
q(t)=\frac{Q_{\mathrm{ext}}(t)}{Q_{\mathrm{cell}}}.
\tag{C1.1}
\]

Here \(Q_{\mathrm{cell}}>0\) is the reference cell capacity. If the capacity is recorded in ampere-hour,

\[
Q_{\mathrm{cell}}[\mathrm{C}]=3600\,Q_{\mathrm{cell}}[\mathrm{Ah}].
\tag{C1.2}
\]

For a nonzero-current segment,

\[
\frac{\mathrm{d}q}{\mathrm{d}t}
=\frac{I_{\mathrm{abs}}}{Q_{\mathrm{cell}}},
\qquad
\frac{\mathrm{d}}{\mathrm{d}q}
=\frac{Q_{\mathrm{cell}}}{I_{\mathrm{abs}}}
\frac{\mathrm{d}}{\mathrm{d}t}.
\tag{C1.3}
\]

Equation (C1.3) is invalid during rest because \(I_{\mathrm{abs}}=0\). Rest relaxation must be written in the time domain at fixed \(q\).

## Transition State Variables

The staged graphite response is represented by \(N_p\) internal progress variables:

\[
\boldsymbol{\xi}=(\xi_1,\ldots,\xi_{N_p}),
\qquad
0\le \xi_j\le 1.
\tag{C1.4}
\]

The transition capacity associated with state \(j\) is \(Q_{j,\mathrm{tot}}\), and the normalized transition fraction is

\[
a_j=\frac{Q_{j,\mathrm{tot}}}{Q_{\mathrm{cell}}}.
\tag{C1.5}
\]

The symbol \(w_j\) is reserved for voltage width only. It must not be reused as a capacity fraction.

## Equilibrium Occupancy Functions

Before \(V_n\) is solved, equilibrium functions are written against a dummy voltage argument \(V\):

\[
\xi_{j,\mathrm{eq}}(V,T)
=
\left[
1+
\exp\!\left(
-s_{\xi,j}\frac{V-U_j(T)}{w_j(T)}
\right)
\right]^{-1}.
\tag{C1.6}
\]

Here \(U_j(T)\) is the transition center, \(w_j(T)>0\) is the transition width, and \(s_{\xi,j}\in\{-1,+1\}\) fixes orientation. The logistic form is a usable default, but the chapter should state it as a model choice. A different monotone equilibrium function can be substituted if it preserves the same dependency order.

## Background Storage Is Storage, Not A Cosmetic Baseline

The term \(Q_{\mathrm{bg}}(V,T;\theta)\) is the background charge-storage contribution of graphite outside the discrete staging transition capacities:

\[
Q_{\mathrm{bg}}=Q_{\mathrm{bg}}(V,T;\theta).
\tag{C1.7}
\]

It is not a visual baseline subtracted from an ICA curve after the fact. It participates directly in charge conservation. Consequently, changing \(Q_{\mathrm{bg}}\) changes the root-solved internal potential and the derivative observables.

## Charge-Balance Residual

With the dummy voltage \(V\), the charge-balance residual is

\[
\mathcal{G}(V;q,T,\boldsymbol{\xi};\theta)
=
Q_{\mathrm{bg}}(V,T;\theta)
+
\sum_{j=1}^{N_p} Q_{j,\mathrm{tot}}\xi_j
-
Q_{\mathrm{cell}}q.
\tag{C1.8}
\]

The central charge-balance equation is

\[
Q_{\mathrm{cell}}q
=
Q_{\mathrm{bg}}(V_n,T;\theta)
+
\sum_{j=1}^{N_p} Q_{j,\mathrm{tot}}\xi_j.
\tag{C1.9}
\]

Equation (C1.9) must not be written before the residual/root definition in the final manuscript; otherwise \(V_n\) appears to be known before it has been solved.

## Root Existence Interval, Slope Floor, And Branch Selection

Let \(\mathcal{I}_V=[V_{\min},V_{\max}]\) be the admissible graphite voltage interval. For each \((q,T,\boldsymbol{\xi})\), the model requires at least one root

\[
\mathcal{G}(V;q,T,\boldsymbol{\xi};\theta)=0,
\qquad
V\in\mathcal{I}_V.
\tag{C1.10}
\]

A useful local conditioning condition is

\[
\frac{\partial Q_{\mathrm{bg}}}{\partial V}(V,T;\theta)
\ge
\epsilon_Q>0
\quad
\text{on the evaluated interval.}
\tag{C1.11}
\]

This slope floor is a numerical conditioning rule. It should be presented as a safeguard against singular inversion, not as a new physical staging feature.

If multiple admissible roots are possible, the manuscript must state a branch-selection rule. The default rule for the Chapter 1 package is: select the continuous branch connected to the initial condition and reject root jumps that violate the voltage interval, state domain, or validation residual. Any stronger thermodynamic branch rule needs additional physical justification.

## Internal Potential Root

The root operator is

\[
\mathcal{V}(q,T,\boldsymbol{\xi};\theta)
=
\operatorname*{root}_{V\in\mathcal{I}_V}
\mathcal{G}(V;q,T,\boldsymbol{\xi};\theta).
\tag{C1.12}
\]

The internal graphite potential is then

\[
V_n
=
\mathcal{V}(q,T,\boldsymbol{\xi};\theta),
\qquad
\mathcal{G}(V_n;q,T,\boldsymbol{\xi};\theta)=0.
\tag{C1.13}
\]

This is the second major logical repair: \(V_n\) is not fitted or prescribed directly as a function of \(q\). It is the voltage that makes the storage relation match the measured external charge for the current internal state.

## Equilibrium OCV As A Special Case

The equilibrium OCV is derived by requiring every internal transition state to equal its equilibrium occupancy at the same voltage:

\[
Q_{\mathrm{cell}}q
=
Q_{\mathrm{bg}}(V,T;\theta)
+
\sum_{j=1}^{N_p}
Q_{j,\mathrm{tot}}\xi_{j,\mathrm{eq}}(V,T).
\tag{C1.14}
\]

The equilibrium anode OCV is the root of (C1.14):

\[
V_{n,\mathrm{OCV}}(q,T)
=
\operatorname*{root}_{V\in\mathcal{I}_V}
\left[
Q_{\mathrm{bg}}(V,T;\theta)
+
\sum_{j=1}^{N_p}
Q_{j,\mathrm{tot}}\xi_{j,\mathrm{eq}}(V,T)
-
Q_{\mathrm{cell}}q
\right].
\tag{C1.15}
\]

Thus \(V_{n,\mathrm{OCV}}\) is not a primitive input curve in the dynamic model. It is the equilibrium branch of the same charge-balance system.

## Total Capacity Consistency

The endpoint capacity of the analysis interval must be consistent with the same storage model:

\[
\Delta Q_{\mathrm{cell}}
\approx
\Delta Q_{\mathrm{bg}}
+
\sum_{j=1}^{N_p} Q_{j,\mathrm{tot}}\Delta \xi_j.
\tag{C1.16}
\]

This relation is not a fitting-performance claim. It is a consistency requirement that prevents \(Q_{\mathrm{bg}}\), \(Q_{j,\mathrm{tot}}\), \(U_j\), and \(w_j\) from being treated as unrelated curve-shape knobs.

## Apparent And Driving Voltages

The internal potential, apparent voltage, and driving voltage have separate roles:

\[
V_{n,\mathrm{app}}
=
V_n+s_I I_{\mathrm{abs}}R_n(q,T,I_{\mathrm{abs}}),
\tag{C1.17}
\]

\[
V_{n,\mathrm{drive}}
=
\Phi_{\mathrm{drive}}(V_n,V_{n,\mathrm{app}},I,T;\theta).
\tag{C1.18}
\]

The approximation \(V_{n,\mathrm{drive}}\approx V_{n,\mathrm{app}}\) may be used only when it is explicitly declared. It must not be silently combined with an unconstrained fit of both \(R_n\) and kinetic prefactors, because both can absorb dynamic voltage shifts.

## Kinetic Interface

Chapter 1 only defines the kinetic interface. It does not derive the full Chapter 3 kinetic model. A generic relaxation-rate interface is

\[
k_j=k_j(V_n,q,T,I;\theta),
\qquad
k_j\ge 0.
\tag{C1.19}
\]

If an affinity is needed for later chapters, it can be written as

\[
\mathcal{A}_j
=
s_{\phi,j}F\left(V_{n,\mathrm{drive}}-U_j(T)\right).
\tag{C1.20}
\]

This affinity is downstream of \(V_{n,\mathrm{drive}}\), which is downstream of the root-solved \(V_n\). Kinetics cannot change the charge-conservation equation; they only update the internal states that subsequently change the next root solve.

## Time-Domain State Equation

After \(V_n\) is solved, the internal state dynamics are

\[
\frac{\mathrm{d}\xi_j}{\mathrm{d}t}
=
k_j(V_n,q,T,I;\theta)
\left[
\xi_{j,\mathrm{eq}}(V_n,T)-\xi_j
\right].
\tag{C1.21}
\]

This equation must be read together with the root relation (C1.13). The right-hand side is not explicit in \(\boldsymbol{\xi}\) until \(V_n=\mathcal{V}(q,T,\boldsymbol{\xi};\theta)\) is solved.

## Charge-Domain State Equation

For \(I_{\mathrm{abs}}>0\),

\[
\frac{\mathrm{d}\xi_j}{\mathrm{d}q}
=
\frac{Q_{\mathrm{cell}}}{I_{\mathrm{abs}}}
k_j(V_n,q,T,I;\theta)
\left[
\xi_{j,\mathrm{eq}}(V_n,T)-\xi_j
\right].
\tag{C1.22}
\]

Equation (C1.22) is not valid at rest or in current intervals where the charge coordinate is not monotone. Rest must use the time-domain equation at fixed \(q\).

## Volterra Integral Form And Exact Self-Consistency Loop

On a nonzero-current segment, the charge-domain state equation can be written as

\[
\xi_j(q)
=
\xi_j(q_0)
+
\int_{q_0}^{q}
\frac{Q_{\mathrm{cell}}}{I_{\mathrm{abs}}(s)}
k_j(V_n(s),s,T(s),I(s);\theta)
\left[
\xi_{j,\mathrm{eq}}(V_n(s),T(s))-\xi_j(s)
\right]
\,\mathrm{d}s.
\tag{C1.23}
\]

The feedback is exact:

\[
\boldsymbol{\xi}(s)
\xrightarrow{\;\mathcal{G}=0\;}
V_n(s)
\xrightarrow{\;k_j,\xi_{j,\mathrm{eq}}\;}
\frac{\mathrm{d}\boldsymbol{\xi}}{\mathrm{d}s}
\xrightarrow{\;\text{integration}\;}
\boldsymbol{\xi}(q).
\tag{C1.24}
\]

This is the graphite-specific self-consistent problem that later closure methods must approximate. Refs. 6/7 may inform how to construct a reference/correction closure, but they do not replace (C1.23) as the direct baseline.

## Rest Relaxation At Fixed q

During rest,

\[
\frac{\mathrm{d}q}{\mathrm{d}t}=0,
\qquad
V_n(t)=\mathcal{V}(q_{\mathrm{rest}},T(t),\boldsymbol{\xi}(t);\theta),
\tag{C1.25}
\]

and the state evolves by the time-domain equation

\[
\frac{\mathrm{d}\xi_j}{\mathrm{d}t}
=
k_j(V_n,q_{\mathrm{rest}},T,0;\theta)
\left[
\xi_{j,\mathrm{eq}}(V_n,T)-\xi_j
\right].
\tag{C1.26}
\]

This rest form is required because \(q\)-domain dynamics divide by current magnitude and therefore become singular at \(I_{\mathrm{abs}}=0\).

## General Thermal Derivative Of Charge Balance

Differentiate the residual

\[
\mathcal{G}(V_n;q,T,\boldsymbol{\xi};\theta)=0
\]

with respect to \(q\). If \(T=T(q)\) and parameters may depend on temperature, then

\[
0
=
\frac{\partial Q_{\mathrm{bg}}}{\partial V}
\frac{\mathrm{d}V_n}{\mathrm{d}q}
+
\frac{\partial Q_{\mathrm{bg}}}{\partial T}
\frac{\mathrm{d}T}{\mathrm{d}q}
+
\sum_{j=1}^{N_p}
\left[
Q_{j,\mathrm{tot}}
\frac{\mathrm{d}\xi_j}{\mathrm{d}q}
+
\xi_j
\frac{\mathrm{d}Q_{j,\mathrm{tot}}}{\mathrm{d}T}
\frac{\mathrm{d}T}{\mathrm{d}q}
\right]
-
Q_{\mathrm{cell}}.
\tag{C1.27}
\]

If transition capacities are temperature-independent over the analysis window, the \(\mathrm{d}Q_{j,\mathrm{tot}}/\mathrm{d}T\) term is removed.

## Isothermal Simplification

For isothermal analysis with temperature-independent transition capacities,

\[
\frac{\mathrm{d}V_n}{\mathrm{d}q}
=
\frac{
Q_{\mathrm{cell}}
-
\sum_{j=1}^{N_p}Q_{j,\mathrm{tot}}
\frac{\mathrm{d}\xi_j}{\mathrm{d}q}
}{
\frac{\partial Q_{\mathrm{bg}}}{\partial V}(V_n,T;\theta)
}.
\tag{C1.28}
\]

This expression is allowed only after \(\mathrm{d}\xi_j/\mathrm{d}q\) has been defined.

## Apparent Voltage Derivative

If (C1.17) is used,

\[
\frac{\mathrm{d}V_{n,\mathrm{app}}}{\mathrm{d}q}
=
\frac{\mathrm{d}V_n}{\mathrm{d}q}
+
s_I
\frac{\mathrm{d}}{\mathrm{d}q}
\left[
I_{\mathrm{abs}}R_n(q,T,I_{\mathrm{abs}})
\right].
\tag{C1.29}
\]

For constant-current, isothermal segments with a simple \(R_n(q)\), this derivative simplifies, but that simplification belongs in the solver/fitting protocol unless the assumptions are explicitly stated.

## ICA And DVA

The ICA observable is based on external charge:

\[
\frac{\mathrm{d}Q_{\mathrm{ext}}}{\mathrm{d}V_{n,\mathrm{app}}}
=
\frac{Q_{\mathrm{cell}}}
{\frac{\mathrm{d}V_{n,\mathrm{app}}}{\mathrm{d}q}}.
\tag{C1.30}
\]

The DVA observable is

\[
\frac{\mathrm{d}V_{n,\mathrm{app}}}{\mathrm{d}Q_{\mathrm{ext}}}
=
\frac{1}{Q_{\mathrm{cell}}}
\frac{\mathrm{d}V_{n,\mathrm{app}}}{\mathrm{d}q}.
\tag{C1.31}
\]

These equations should not be described as fitted data results. They are observable definitions derived from the chosen charge coordinate and voltage model.

## Monotonicity And Denominator-Singularity Warning

The derivative observables require

\[
\frac{\mathrm{d}V_{n,\mathrm{app}}}{\mathrm{d}q}
\ne 0
\tag{C1.32}
\]

over any interval where ICA is evaluated directly. If the denominator approaches zero, the ICA peak can become numerically singular or physically ambiguous. The manuscript may state this as a validation warning, not as a completed data-quality result.

The root solve also requires the effective storage slope in the denominator of (C1.28) to remain away from zero. If it does not, either the storage model, branch selection, or numerical regularization must be revised.

## Chapter 1 Validation Residuals

The Chapter 1 validation protocol should include:

\[
r_{\mathcal{G}}(q)
=
\frac{\mathcal{G}(V_n;q,T,\boldsymbol{\xi};\theta)}
{Q_{\mathrm{cell}}}.
\tag{C1.33}
\]

Allowed checks:

- \(|r_{\mathcal{G}}(q)|\) remains below the declared numerical tolerance.
- \(V_n\in\mathcal{I}_V\).
- all \(\xi_j\) remain inside their declared domains.
- the slope floor or equivalent conditioning rule is not violated.
- \(I_{\mathrm{abs}}>0\) wherever charge-domain dynamics are used.
- ICA/DVA denominators do not cross unphysical singularities.
- any approximate closure is compared against direct root-solve integration.

These are validation requirements, not claims that validation has already been run.

## Exact Versus Approximate Formulation

The exact baseline is the direct root-solve formulation: at every integration point, solve (C1.13), evaluate rates and equilibrium occupancies at the solved \(V_n\), and update \(\boldsymbol{\xi}\). The approximate closure appears only after this baseline is stated.

The closure direction inspired by refs. 6/7 should be phrased as:

1. choose a reference path \(\boldsymbol{\xi}^{\mathrm{ref}}(q)\);
2. compute \(V_n^{\mathrm{ref}}(q)=\mathcal{V}(q,T,\boldsymbol{\xi}^{\mathrm{ref}};\theta)\);
3. express the direct integral as a reference integrand multiplied by a dimensionless feedback correction;
4. define how the correction is approximated;
5. validate the approximation against the direct baseline.

The physical molecular-pair assumptions of refs. 6/7 are not imported.

## Manuscript Equations To Insert

| Eq | Purpose | Insert Condition | Source / Cross-Check |
|---|---|---|---|
| C1.1-C1.3 | measured charge coordinate and charge-domain conversion | after current convention is stated | DAG E01-E02; source evidence corrected ver1 lines 95-105 |
| C1.4-C1.6 | internal states and equilibrium occupancy | before charge balance | DAG E03-E04; source evidence corrected ver1 lines 109-117 and 184-201 |
| C1.7-C1.13 | background storage, residual, root operator, `V_n` | before any OCV or kinetics | DAG E05-E09; central equation source corrected ver1 lines 121-127 |
| C1.14-C1.15 | equilibrium OCV as special root | only after root operator | DAG E10; source evidence corrected ver1 lines 148-162 |
| C1.17-C1.20 | apparent/driving voltage and kinetic interface | after `V_n` is solved | DAG E11-E14; source evidence corrected ver1 lines 203-237 |
| C1.21-C1.23 | dynamics and Volterra form | after kinetic interface | DAG E15-E18; source evidence corrected ver1 lines 240-286 |
| C1.25-C1.26 | rest relaxation | after dynamics | DAG E17; source evidence corrected ver1 lines 289-299 |
| C1.27-C1.29 | derivative of charge balance and apparent voltage | after `dxi_j/dq` | DAG E22-E23; source evidence corrected ver1 lines 353-411 |
| C1.30-C1.31 | ICA/DVA | after apparent voltage derivative | DAG E24-E25; source evidence corrected ver1 lines 394-411 |
| C1.33 | validation residual | after all core equations | DAG E26; validation-gate inventory |

## Manuscript Claims Allowed

| Claim | Allowed Strength | Evidence |
|---|---|---|
| `V_n` is solved from charge balance, not prescribed | strong | corrected ver1 lines 121-129; notation bible; DAG E07-E09 |
| `V_{n,OCV}` is an equilibrium special root | strong | corrected ver1 lines 148-162; DAG E10 |
| `Q_bg` is storage | strong | source evidence and notation bible |
| the dynamic problem is self-consistent and Volterra-like | strong as classification | dependency graph and self-consistent mapping |
| direct root-solve integration is the exact baseline | strong as method definition | DAG E18-E19 |
| refs. 6/7 motivate a reference/correction closure pattern | cautious | ref notes and source evidence; original refs not yet READ_FULL |
| ICA/DVA are derivatives with respect to external charge and apparent voltage | strong as definition | corrected ver1 lines 353-411; DAG E22-E25 |

## Manuscript Claims Forbidden

| Forbidden Claim | Reason |
|---|---|
| `V_n` or `V_{n,OCV}(q,T)` is the prescribed dynamic voltage input | reverses dependency order |
| `Q_bg` is only a cosmetic baseline | contradicts charge-balance storage role |
| kinetics can modify charge conservation directly | kinetics update internal states; charge conservation remains the residual |
| q-domain dynamics are valid at rest | division by `I_abs` fails at rest |
| refs. 6/7 physically describe graphite staging | source-domain physics is molecular-pair diffusion/reaction |
| closure approximation is validated | no direct solver validation has been run yet |
| fitted parameter values or fit quality are known | no fitting dataset or protocol phase has passed |
| exact equations from PDF/ref. 6/ref. 7 have been visually verified | not yet verified |

## Requires Later Chapter Or Later Phase

| Item | Destination | Reason |
|---|---|---|
| detailed heat coupling | Chapter 2 / Phase 010 | Chapter 1 treats `T` as input |
| full electrochemical kinetics or Butler-Volmer expansion | Chapter 3 / Phase 010 | Chapter 1 only defines kinetic interface |
| `R_n` and kinetic-prefactor identifiability strategy | Chapter 4 / Phase 009 | fitting controls needed |
| reference-closure derivation details | Phase 007 | original refs. 6/7 full read and closure contract needed |
| direct solver algorithm and error checks | Phase 008 | solver protocol not yet complete |
| numerical fitting claims | Phase 009 or later | requires data and validation |
| hysteresis/memory state equations | Chapter 5 / Phase 010 | beyond Chapter 1 foundation |

## Cross-Check Summary

| Cross-Check Target | Result |
|---|---|
| `REBUILD_V2_EQUATION_DEPENDENCY_DAG.md` | PASS. Equations C1.1-C1.33 follow DAG E01-E26. |
| `REBUILD_V2_NOTATION_BIBLE.md` | PASS. Symbols preserve role, unit/domain intent, and `V_n` root ordering. |
| `REBUILD_V2_SOURCE_EVIDENCE_INDEX.md` | PASS with cautions. Central claims trace to corrected ver1, while refs. 6/7 exact derivations remain unverified. |
| Phase 003 salvage/reject inventory | PASS. Old draft/ver5 body prose not reused as manuscript base. |

## Open Mathematical Risks

- A rigorous uniqueness condition for the charge-balance root is not fully proven. Current package uses admissible interval, slope floor, and branch-selection rule.
- The general thermal derivative (C1.27) may need adjustment if parameters other than \(Q_{j,\mathrm{tot}}\) are temperature-dependent inside the derivative.
- The logistic equilibrium occupancy is a model choice, not yet a uniquely justified physical law.
- The Volterra-like integral form is structurally correct, but numerical stiffness and solution regularity remain Phase 008 topics.
- The closure correction form is not yet derived in graphite variables; it is deferred to Phase 007.

## Open Physical Risks

- Stage-transition orientation signs must be matched to the selected charge/discharge convention.
- `Q_bg` must be physically constrained enough to avoid absorbing staging features during fitting.
- `R_n` and kinetic prefactors can double-count dynamic shifts unless Phase 009 constrains fitting.
- Heat coupling can feed back through `T`; Chapter 1 treats `T` as input until Chapter 2 defines coupling.
- Hysteresis/memory states may alter effective \(\boldsymbol{\xi}\) interpretation and must not be introduced without preserving charge balance.

## Open Notation Risks

- Final manuscript must decide whether to write vectors as `bold xi`, `\bm{\xi}`, or another macro.
- Final manuscript must decide whether the apparent voltage subscript is always `n,app` or whether a cell-voltage observable is introduced separately.
- If Faraday constant \(F\) appears near closure integrands, closure symbols should avoid `F_j^{ref}` and use a different symbol such as \(\Phi_j^{\mathrm{ref}}\).
- The sign conventions \(s_I\), \(s_{\xi,j}\), and \(s_{\phi,j}\) remain declared controls rather than fixed numerical choices.

## Items Needing User Decision

| Item | Default | Why It Matters |
|---|---|---|
| final language | Korean prose with standard mathematical notation | affects final Chapter 1 writing style |
| output scope | Chapter 1 full + Chapter 2-5 skeleton | affects how much downstream content appears in final manuscript |
| whether to include pseudocode in main text | keep in protocol/appendix | affects whether final manuscript reads as theory note or method paper |
| strength of refs. 6/7 positioning | cautious method-pattern statement | stronger claim requires full refs. 6/7 read |
| branch-selection rule wording | continuous admissible branch from initial condition | stronger thermodynamic claim requires more proof |

## Exact Equations Not Yet Visually Verified

- Exact equations from the 2017 JCP PDF are not visually verified for glyph/layout fidelity.
- Exact equations from ref. 6 are not full-read or visually verified in this project record.
- Exact equations from ref. 7 are not full-read or visually verified in this project record.
- This package uses only the portable closure pattern from available notes, not exact ref. 6/7 formulas.

## Exact Source References For Central Equation

| Item | Source Reference |
|---|---|
| measured `Q_ext` and `q` | corrected ver1 source lines 95-105, recorded in `ver1_charge_balance_dependency_graph.md` and Phase 002 evidence index |
| central charge balance `Q_cell q = Q_bg(V_n,T)+sum Q_j,tot xi_j` | corrected ver1 source lines 121-127, recorded in Phase 002 evidence index |
| `V_n` solved from residual/root | corrected ver1 source lines 121-129; self-consistent mapping |
| equilibrium OCV special root | corrected ver1 source lines 148-162 |
| voltage distinctions | corrected ver1 source lines 203-237 |
| dynamics and self-consistent loop | corrected ver1 source lines 240-286 |
| rest relaxation | corrected ver1 source lines 289-299 |
| ICA/DVA equations | corrected ver1 source lines 353-411 and especially 394-411 for observable definitions |

## Phase 006 Gate Statement

Gate: `PASS_REBUILD_V2_CHAPTER1_MATH`

The package passes because it includes charge balance, OCV as a special case, DAE/Volterra form, ICA/DVA derivation, `Q_bg` storage treatment, q-domain rest invalidity, and source references for central equations. It remains blocked from final LaTeX manuscript assembly until Phase 007-010 are complete.
