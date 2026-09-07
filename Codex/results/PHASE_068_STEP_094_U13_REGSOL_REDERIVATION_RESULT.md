# Phase 068 Step 94 — U13 정칙용액 문턱 독립 재유도 결과

정본일: 2026-09-07

계획: `Codex/plans/2026-09-07-phase068-claude-codex-fork-adjudication-detailed-plan.md`

Current-state marker: `P068_STEP94_U13_REDERIVATION_PRECOMMIT`

State-marker authority: 이 필드는 현재 실행 단위의 machine-authoritative marker다. 이전 Step 93 precommit 문구는 역사 기록이다.

## Transaction

- expected parent: `0b850ea9ffa33e04356d11b83190f9a7cfbea37c`
- predecessor persistence: `PASS_P068_STEP93_PERSISTENCE`
- required subject: `audit(phase068): rederive u13 threshold regularity`
- containing commit: `PENDING_AT_PRECOMMIT_BY_DESIGN`
- selected content terminal: `PASS_P068_STEP94_U13_REDERIVATION`
- reserved persistence terminal: `PASS_P068_STEP94_PERSISTENCE`
- status: `PASS_PENDING_PERSISTENCE`
- next cumulative Step after persistence: Step 95

Exact-seven transaction:

1. `Codex/work/v1025_phase068/build_phase068_step94.py`
2. `Codex/work/v1025_phase068/validate_phase068_step94.py`
3. `Codex/results/PHASE_068_U13_REGSOL_REDERIVATION.json`
4. `Codex/results/PHASE_068_STEP_094_U13_REGSOL_REDERIVATION_RESULT.md`
5. `Codex/results/PHASE_055_069_FULL_LINEAGE_REAUDIT_EXECUTION_LEDGER.md`
6. `Codex/results/PHASE_059_090_CANONICAL_COMPLETION_EXECUTION_LEDGER.md`
7. `Codex/results/ACTIVE_HANDOVER_CANONICAL_COMPLETION.md`

Required status is `A/A/A/A/M/M/M`, all modes `100644`. No other path belongs to this Step.

## Summary

The broadened regular-solution measure in `eq:sifr-twophase` is **C1 at**
`a=Omega/(R*T)=2` under the declared fixed-kernel assumptions. The earlier U13 claim that the
first derivative diverges is refuted. The later U13 conclusion that the value and first derivative
join is confirmed, but its numerical footnote contains a separate factor-of-two normalization defect:
the quoted `5.90` was computed with `epsilon=a-2`, whereas the footnote defines
`eta=abs(a/2-1)=abs(epsilon)/2`. The same ratio in the footnote's own coordinate is therefore about
`11.79828`, not `5.90`.

This conclusion does **not** come from one finite max-norm ratio. It follows from an independent
binodal series, an exact moving-boundary cancellation, the common left/right derivative formula,
the central-replacement remainder `O(epsilon^(7/2))`, and numerical one-sided/Richardson checks.

The judgment is deliberately bounded:

- `Q`, `U0`, `T`, `w`, and `alpha` are fixed while differentiating in `a` or `Omega`.
- `R,T,F,Q,w` are positive and `alpha>0`.
- the mathematical kernel is normalized, translation invariant and sufficiently smooth; bounded
  continuous `kappa`, `kappa'`, and `kappa''` suffice for the stated C1 boundary, while the displayed
  higher-order remainder uses the smooth fixed logistic/skew-logistic family.
- the full-line area theorem applies to the **unclipped mathematical kernel**. Historical finite-window
  values and the historical `np.clip` evaluation device are numerical observations, not the theorem.
- zero-width and varying-kernel limits, material/mechanism truth, held-out data, canonical adoption,
  publication readiness, and any whole-commit transfer are outside this Step.

## Frozen Inputs and Direct Read Coverage

All eight source objects below were read from byte 0 through EOF. Total coverage is `8` objects,
`126,576` raw bytes and `1,870` physical lines.

| ID | Commit | Path | Blob | Bytes | Lines | Coverage |
|---|---|---|---|---:|---:|---|
| U13-BEFORE | `3b5fd059ed09cdcdde38668c399cb35b8afbcca9` | `Claude/docs/v1.0.25.2/_sections/ch3v22_sec02b_sifr.tex` | `ea762ff015f47e03b79e99f051deae5ddef44f9c` | 26,835 | 253 | `READ_FULL` |
| U13-AFTER | `2802395dd03e6cabe3e981bddddbba139e3963bc` | same path | `05f1d84713017dde303f56ca7004b61aa0496979` | 27,406 | 258 | `READ_FULL` |
| P44-SCRIPT | `11f90544865dd179739ca5bc5062b28c1078e504` | `Codex/work/v1025_2_physics_branch/phase044_regsol_threshold_probe.py` | `ee7ac08df3698a21500f7a0cf02ed8f814d65344` | 4,469 | 143 | `READ_FULL` |
| P44-OUTPUT | same | `Codex/results/PHASE_044_REGSOL_THRESHOLD_PROBE.json` | `aa51785f88445760d29d3ec3a5c8d219464c995a` | 3,290 | 87 | `READ_FULL` |
| P54-SCRIPT | same | `Codex/work/v1025_2_physics_branch/phase054_regsol_crosscheck.py` | `853df8d32b95b96d60adee6fc842ca4307713ab1` | 7,700 | 227 | `READ_FULL` |
| P54-OUTPUT | same | `Codex/results/PHASE_054_V1025_2_REGSOL_CROSSCHECK.json` | `58f6b037c9d4e0d3bc9f07a2847ee4cde16fd338` | 11,893 | 347 | `READ_FULL` |
| WIDTH-DEFINITION | `3b5fd059ed09cdcdde38668c399cb35b8afbcca9` | `Claude/docs/v1.0.25.2/_sections/ch1_sec05_width.tex` | `2003860215e0a721876bace4364b3b7a6a594031` | 33,982 | 424 | `READ_FULL` |
| PEAK-DEFINITION | same | `Claude/docs/v1.0.25.2/_sections/ch1_sec06_eqpeak.tex` | `fe0816cf46d4ddb8cbb4b6fbb012e3b6e979a17b` | 11,001 | 131 | `READ_FULL` |

The U13 patch changed only the threshold footnote. The source equation, measure and kernel definitions
were not treated as conclusions; the derivation below starts from their equations.

The persisted Step 93 matrix/result were also recovered from expected parent
`0b850ea9ffa33e04356d11b83190f9a7cfbea37c`, whose sole parent is
`25e3120ff0f38c5fa2bf603413034920640b3e62` and whose subject is
`audit(phase068): revalidate phase044 phase054 reviews`. This is an object certificate, not a claim
that Step 94 re-executed the whole Step 93 validator.

## Independent Derivation

### 1. Coordinates and binodal series

Set

\[
a=\frac{\Omega}{RT}=2+\epsilon,\qquad
c=\frac{RT}{F},\qquad
\theta=\frac12+y,\qquad
\theta_a=\frac12-x.
\]

The documented binodal equation is

\[
\ln\!\frac{\theta}{1-\theta}+a(1-2\theta)=0.
\]

At the lower coexistence root this becomes

\[
0=2\epsilon x-\frac{16}{3}x^3-\frac{64}{5}x^5
-\frac{256}{7}x^7+O(x^9).
\]

Series reversion gives

\[
\boxed{x^2=\frac38\epsilon-\frac{27}{80}\epsilon^2
+\frac{1377}{5600}\epsilon^3+O(\epsilon^4)}
\]

and hence

\[
\boxed{2x=\sqrt{\frac32}\,\epsilon^{1/2}
\left(1-\frac9{20}\epsilon+\frac{1269}{5600}\epsilon^2
+O(\epsilon^3)\right)}.
\]

Thus the gap weight itself opens as `sqrt(epsilon)`. This fact alone says nothing about the
regularity of the **sum** of the gap term and the two stable-branch terms.

### 2. Full reference integral and the central replacement

Write the regular-solution voltage as

\[
V_a(\theta)=U^\circ-c\left[
\ln\!\frac{\theta}{1-\theta}+a(1-2\theta)
\right]
\]

and define the smooth full-composition extension

\[
H(a,V)=Q\int_0^1\kappa\!\left(V-V_a(\theta)\right)\,d\theta.
\]

For `a<=2`, the documented prescription has `theta_a=1/2`, zero gap weight and `B_a=H(a,V)`.
For `a=2+epsilon>2`, the actual broadened curve equals `H` plus the correction that removes the
unstable central interval and replaces it with its Maxwell mass at `U0`.

With `z=V-U0` and `theta=1/2+y`, the central voltage shift is

\[
d_\epsilon(y)=V_{2+\epsilon}\!\left(\frac12+y\right)-U^\circ
=c\left[2\epsilon y-\frac{16}{3}y^3-\frac{64}{5}y^5-\cdots\right],
\]

an odd function of `y`. Therefore

\[
R_\epsilon(V)=Q\left[
2x\kappa(z)-\int_{-x}^{x}\kappa\!\left(z-d_\epsilon(y)\right)dy
\right].
\]

The constant terms cancel exactly. The first-order kernel term integrates to zero because
`d_epsilon(y)` is odd on the symmetric interval. **No symmetry of `kappa` is required.** The next term is

\[
R_\epsilon(V)
=-\frac{Q\kappa''(z)}{2}\int_{-x}^{x}d_\epsilon(y)^2dy+\cdots
=-\frac{\sqrt6}{35}Qc^2\kappa''(z)\epsilon^{7/2}
+O(\epsilon^{9/2}).
\]

Equivalently, the coefficient is
`-(32/105)*Q*c^2*(3/8)^(3/2)*kappa''(V-U0)`.
This establishes more than cancellation of only the visible square-root mass: all lower central
replacement orders through the first derivative vanish.

### 3. Common one-sided derivative

Since

\[
\partial_a\,[V-V_a(\theta)]=c(1-2\theta),
\]

the derivative of the full reference integral at `a=2` is

\[
\boxed{
D(V)=Qc\int_0^1(1-2\theta)
\kappa'\!\left(V-V_2(\theta)\right)d\theta}.
\]

For `a<2`, this is the left derivative by dominated differentiation. For `a>2`, the moving-boundary
terms cancel exactly because both binodal endpoints map to `U0`, and

\[
R'_\epsilon(V)=-\frac{\sqrt6}{10}Qc^2\kappa''(V-U^\circ)
\epsilon^{5/2}+O(\epsilon^{7/2})\longrightarrow0.
\]

Consequently

\[
\left.\frac{\partial B}{\partial a}\right|_{2^-}
=\left.\frac{\partial B}{\partial a}\right|_{2^+}=D(V),
\qquad
\left.\frac{\partial B}{\partial\Omega}\right|_{2RT^\pm}
=\frac{D(V)}{RT}.
\]

This establishes `C1` in `a` and in `Omega` under the fixed-parameter assumptions. It does not establish
`C-infinity`; a generic one-sided `epsilon^(7/2)` remainder is a specific reason not to promote the
result beyond the regularity actually tested and derived.

## Separate Proposition Judgments

| Proposition | Analytic status | Authority ceiling |
|---|---|---|
| Full-real-line area equals `Q` | `CONFIRMED` for an integrable unit-normalized mathematical kernel | fixed-kernel measure only |
| Subcritical gap weight | `CONFIRMED`: exactly zero for `a<=2` by the documented prescription | same |
| C0 at `a=2` | `CONFIRMED` | same |
| Left derivative | `CONFIRMED`; equals `D(V)` | same |
| Right derivative | `CONFIRMED`; equals `D(V)` | same |
| C1 equality and derivative continuity | `CONFIRMED_UNDER_DECLARED_ASSUMPTIONS` | same |
| U13 footnote `epsilon`/`5.90` consistency | `SOURCE_NUMERIC_NORMALIZATION_DEFECT_CONFIRMED` | source-text correction only |

Authority string used by machine evidence:
`MATHEMATICAL_FIXED_SMOOTH_KERNEL_MEASURE_ONLY_NOT_MATERIAL_OR_CANONICAL_AUTHORITY`.

## Epsilon Normalization Defect

The historical Phase 044/054 probes use

\[
\epsilon_{\rm hist}=\frac{\Omega}{RT}-2=a-2.
\]

The later U13 footnote instead defines

\[
\eta_{\rm footnote}=\left|\frac{\Omega}{2RT}-1\right|
=\frac{|a-2|}{2}=\frac{|\epsilon_{\rm hist}|}{2}.
\]

Therefore the same finite difference obeys

\[
\frac{\max|\Delta|}{\eta_{\rm footnote}}
=2\frac{\max|\Delta|}{\epsilon_{\rm hist}}.
\]

The historical `alpha=1`, `w=0.010 V`, `Q=1` limit is
`5.899139896744739` in `epsilon_hist` units and `11.798279793489478` in the footnote's units.
The text's `5.90` therefore needs a factor-two rewrite if its displayed definition is retained. The
epsilon interval printed alongside it also needs the same coordinate conversion. This defect is
independent of, and does not refute, the conditional C1 conclusion.

The numbers are parameter-dependent, not universal constants. Historical `alpha=4` `9.69` is a
sampled grid maximum, not an analytic continuous supremum.

## Historical Reproduction

The exact historical source bytes were evaluated read-only under Python 3.12 and 3.14. Phase 044
contributes `8` threshold rows. Phase 054 contributes `9` threshold rows and `24` normalization rows.
The additional narrow-window reference makes the current normalization evidence count `25`.

Representative and boundary rows are:

| alpha | epsilon_hist | right max quotient | left max quotient |
|---:|---:|---:|---:|
| 1 | `1e-3` | 5.896187704867 | 5.902086664495 |
| 1 | `1e-5` | 5.899110243135 | 5.899169392976 |
| 4 | `1e-3` | 9.685058551501 | 9.694748066224 |
| 4 | `1e-5` | 9.689860765150 | 9.689957868630 |
| 8 | `1e-3` | 10.765511404973 | 10.776281839988 |
| 8 | `1e-5` | 10.770849851838 | 10.770957776884 |

Saved-output versus fresh numerical drift was bounded rather than hidden:

- Phase 044 maximum scalar absolute drift: `1.1842384850524468e-9`.
- Phase 054 maximum scalar absolute drift: `3.552713678800501e-12`.
- Phase 054 subcritical gap weight: exactly `0.0`.
- Phase 054 `7.77e-16` area error is a particular `[-1,1] V`, 4001-point numerical observation,
  not a general finite-window or full-line error bound.

## Extended Numerical Evidence

The current validator uses an independently implemented Gauss-Legendre rule rather than importing the
historical scripts' `leggauss`. It evaluates `11` `(alpha,width)` cases over five epsilons
`1e-3..1e-7`, giving `55` one-sided/Richardson rows; four quadrature comparisons and five window/grid
comparisons give `9` convergence rows. Independent 35- and 55-decimal-digit tanh-sinh calculations give
`12` high-precision rows.

Fixed `w=0.010 V`, `alpha=1`, `V=U0` gives

\[
D(U^\circ)=5.899139896744739.
\]

The one-sided first-order quotient errors converge as `O(epsilon)` and the Richardson combinations as
`O(epsilon^2)` until binary64 subtraction and quadrature errors dominate. The largest retained
Richardson discrepancy is `2.93876e-5`, below the declared conservative `2e-3` gate. The high-precision
rows independently remove the binary64 cancellation ambiguity.

The central replacement is separately tested against its analytic `epsilon^(7/2)` coefficient. For
`alpha=1`, `V=U0`, `w=.01`, the coefficient tends to about `5.774144648055635`; skew cases reproduce the
appropriate sign and `kappa''(V-U0)` dependence.

Sensitivity boundaries retained in the evidence:

- `alpha=0.5,1,2,4,8` at `w=.01`, plus `alpha=1,4,8` at `w=.005` and `.02`.
- epsilon `1e-3,1e-4,1e-5,1e-6,1e-7`.
- quadrature orders `800/1600/3200` for selected configurations.
- windows/grids `±.12 V` at `601/1201/2401`, `±.24 V` at 2401 and `±1 V` at 4001.
- all max norms are sampled maxima. In particular, the historical `alpha=4` grid approaches about
  `9.69183` under refined peak search; this is still a numerical peak estimate, not an analytic global
  supremum theorem.

## Area Identity Versus Finite Windows

For an unclipped normalized kernel,

\[
\int_{-\infty}^{\infty}B_a(V)dV
=Q[(1-2\theta_a)+\theta_a+\theta_a]=Q.
\]

The skew-logistic kernel is normalized for fixed `w>0`, `alpha>0` by the substitution from voltage to
the logistic coordinate. Finite windows omit tail mass and add grid/quadrature error. For the
`a=2`, `alpha=1`, `w=.01`, `Q=1` reference, representative trapezoidal areas are approximately
`0.95929039` on `±.06 V`, `0.99665874` on `±.12 V`, `0.99996912` on `±.24 V`, and
`0.999999999999962` on `±1 V` with the stated grids.

The historical `np.clip(z,-350,350)` is an overflow-control implementation detail. If extended
literally over the whole real line it leaves a tiny constant tail and is not the normalized mathematical
kernel. The full-line theorem and finite historical execution are therefore intentionally separate.

## Validation Contract and Negative Controls

The machine artifact is collected last. The validator independently enforces:

- exact eight-source commit/tree/path/blob/mode/byte/line identities and full-read coverage;
- exact rational binodal-series coefficients and seven separate proposition rows;
- `8+9` historical threshold, `25` normalization, `55` extension, `9` convergence and `12`
  high-precision rows;
- exact Step 93 predecessor commit, parent, subject, matrix seal, result blob and
  `PASS_P068_STEP93_PERSISTENCE` certificate;
- result-first control identities, the normalization defect, authority ceiling and zero source
  modifications/whole-commit adoptions;
- `28` named negative controls, `16` builder self-tests, deterministic preview bytes, strict JSON
  bounds, exact-seven content/staged/persistence Git gates and protected-ref non-change.

The numerical routines run under Python 3.12.10/NumPy 2.3.5 and Python 3.14.4/NumPy 2.5.0;
mpmath 1.3.0 supplies the independent high-precision path. Runtime agreement is numerical/internal
evidence only, not external scientific authority.

## Confirmed, Open, and Prohibited Conclusions

### Confirmed

- The exact widened measure conserves area `Q` on the full real line for a normalized kernel.
- The subcritical gap weight is identically zero.
- The broadened curve is C0 at the regular-solution threshold.
- Both one-sided derivatives exist and equal the displayed common `D(V)`.
- The broadened curve is C1 at the threshold under the declared fixed smooth-kernel assumptions.
- The new U13 footnote has a factor-two epsilon/coefficient inconsistency.

### Open or outside this Step

- Higher regularity beyond C1 as a promoted model theorem.
- Any path where `w`, `alpha`, `Q`, `U0` or `T` varies nonsmoothly with `Omega`.
- Simultaneous `w->0`, empirical parameter validity, material mechanism, external literature truth,
  held-out fitting, canonical source adoption, final LaTeX/PDF or publication readiness.

### Prohibited inference

- A finite `max|Delta|/epsilon` ratio alone is not a C1 proof.
- A sampled grid maximum is not a continuous supremum.
- A finite-window area close to one is not the exact full-line area theorem.
- A passing internal validator does not make U13 canonical, material-valid or publication-ready.
- This Step authorizes no edit to `Claude/**`, no production-source repair and no whole-commit adoption.

## Gate and Next Condition

Selected content Gate: `PASS_P068_STEP94_U13_REDERIVATION`.

The selected Gate means the frozen source objects, analytic derivation, numerical reproduction,
normalization defect and authority boundary are complete for Step 94. It remains
`PASS_PENDING_PERSISTENCE` until exact-seven staged validation, commit, push, live-origin equality,
protected-ref non-change, clean-tree verification and dual `PASS_P068_STEP94_PERSISTENCE` complete.

Only then may Step 95 — parallel conformance-model authority, value and duplication — begin.
