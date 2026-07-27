# v1.0.25.2 Accepted Empirical Skew-14 Profile

## Status

`EMPIRICAL CURVE REFERENCE — NOT A HOST OR MECHANISM ASSIGNMENT`

이 profile은 정해진 데이터 처리와 fitting 조건에서 실제 blend
\(\mathrm dQ/\mathrm dV\) 곡선을 표현한다. graphite/Si host 귀속, phase
identity, equilibrium mechanism, activation parameter 또는 heat closure를
정의하지 않는다.

## Frozen observation contract

- source data:
  `Claude/results/comp_v24/sintef_data/sigr.csv`
- SHA-256:
  `e571a66fb9574c4aa7bfdec7acada2eb732029232e7ab83dc7d9645e39fb01e6`
- experimental protocol:
  `UNKNOWN` in the current provenance addendum
- voltage window:
  0.060--0.700 V
- voltage-bin width:
  0.5 mV
- processed points:
  1,280
- residual:
  unweighted linear \(\mathrm dQ/\mathrm dV\)

Active preprocessing:

1. finite rows
2. stable capacity sort and duplicate-capacity collapse
3. increasing isotonic regression of \(V(Q)\)
4. cumulative-capacity rebinning on uniform voltage edges
5. positive longest contiguous derivative segment
6. absolute Savitzky--Golay ensemble

The active path does not execute the dMSMCD or wavelet operations named in the
driver header.
Step 6 discards the signed derivative convention. Consequently the fitted
positive component areas cannot identify a signed chemical-storage coefficient
or reaction/state orientation.

## Observation model

\[
y(V)=B_{\mathrm{obs}}+
\sum_{j=1}^{14}
Q_j\frac{\alpha_j}{w_j}
\sigma_j(V)^{\alpha_j}[1-\sigma_j(V)],
\qquad
\sigma_j(V)=
\left[1+\exp\left(-\frac{V-U_j}{w_j}\right)\right]^{-1}.
\]

Each empirical cumulative component is
\(q_{\mathrm{shape},j}=\sigma_j^{\alpha_j}\), so its derivative is nonnegative
and has area \(Q_j\). This mathematical property does not make
\(q_{\mathrm{shape},j}\) a chemical occupancy or assign a material host,
thermodynamic phase, entropy or heat state to the component. Here \(Q_j\ge0\)
is an empirical observation-area amplitude, not the signed coefficient
\(a_j=\partial Q_{\mathrm{chem}}/\partial\xi_j\).

## Surviving canonical artifact

The most precise surviving parameter artifact is
`Claude/results/comp_v26_data/out_versions/summary_versions.json`,
entry `C_skew/blend`, with order

\[
[U_1\ldots U_{14},\,
w_1\ldots w_{14},\,
Q_1\ldots Q_{14},\,
\alpha_1\ldots\alpha_{14},\,
B_{\mathrm{obs}}\;(\text{stored field }Cbg)].
\]

It contains a 57-value vector rounded to eight decimal places. The builder
calculated metrics and a prediction from its selected `best` vector, then
rounded the vector before saving it and omitted the original prediction from
the summary. The builder did not require `r.success` and did not save
termination status, evaluation count or Jacobian. Therefore:

- optimizer full precision is unavailable;
- the original optimizer prediction/residual is unavailable;
- original optimizer convergence and global optimality are not established;
- the stored-8dp vector is the canonical **surviving** reference;
- the six-decimal transition JSON is a presentation artifact.

Little-endian float64 hashes:

| Array | SHA-256 |
|---|---|
| processed voltage | `6c7ca15d7b9eaf80561d2d2d834856c9b3076f31f6d7e4e6ce304ddb266020b4` |
| processed observation | `da0beeb95e2eac332e870e2a342354109f611503d5641a6c3c3045871f9d791e` |
| stored-8dp parameter vector | `08216da1095a02bcb789a60f577f4afd1d581ad659a8129edaba7dc0dc5910d5` |
| stored-8dp reconstructed prediction | `53cc3c3795be327b90a5d040497074bc51f5a141d0b7629bd34a60682d71f800` |
| stored-8dp reconstructed residual | `1b874701ac72403f2836b352386e3c3a4f658c49238fd2fcf0a4931fd79398ec` |

## Independent reconstruction

From the stored-8dp vector:

| Quantity | Result |
|---|---:|
| \(R^2\) | 0.99964941790404 |
| BIC, 57 counted parameters | -4760.653827485789 |
| frozen \(s=+1\) release path vs independent direct formula, max abs | \(1.4211\times10^{-14}\) mAh/V |
| stored-8dp vs presentation-6dp curve, max abs | 0.0069744215 mAh/V |

The builder computed \(R^2=0.99965\) and BIC \(=-4760.7\) from the then-selected
unrounded `best` prediction and rounded the metrics. The recomputed stored-8dp
values are close but are not proof of the lost optimizer state. Because
preprocessing smooths and correlates neighboring residuals, BIC should be
treated as an i.i.d.-Gaussian working-likelihood comparison statistic inside
this preprocessing/objective, not an exact independent-noise evidence
statement.

## Identification diagnostics

- accepted blend14:
  \(\alpha=0.15400039\ldots7.70072936\);
  \(w_{\min}=1.94054\) mV \(>0.5\) mV grid;
  stored-8dp \(w_{\max}=0.12\) V equals the numerical upper bound
- standalone graphite7:
  \(w_{\min}=0.15824\) mV \(<0.25\) mV grid
- standalone Si7:
  stored-8dp \(\alpha=0.15\) and \(8.0\) equal the two numerical alpha bounds

These warnings belong to their respective profiles. They are not pooled into
one claim about the accepted blend14. The original full-precision vector and
active-set state are unavailable, so stored-value equality is not asserted to
be an optimizer bound hit.

## Release-wiring distinction

The shipped `BlendedAnodeDQDV` default transition path combines a standalone
graphite7 profile and a standalone Si7 profile, then rescales Si capacity with
\(f_{\mathrm{Si}}\). It does not load this direct blend14 profile. Its
constructor observation baseline is zero unless explicitly supplied; the separately
declared fitted graphite and Si observation-baseline constants are not
consumed.

On the same processed blend data, holding the shipped 7+7 shapes fixed and
fitting only \(f_{\mathrm{Si}}\) and a nonnegative observation baseline gives

\[
f_{\mathrm{Si}}=0.58122565,\qquad
B_{\mathrm{obs}}\simeq0,\qquad
R^2=-1.61321666.
\]

This is a release-conformance test, not a scientific contest between the two
model classes. The direct14 has 57 blend-fitted coefficients; the 7+7 shapes
came from separate host datasets and protocols. The result establishes only
that the successful direct14 fit is not wired as the shipped default.

## Required preservation and future-fit contract

Future work shall:

- expose this profile through a dedicated empirical entry point;
- keep it separate from the physical host-blend model;
- preserve the processed-data and stored-vector hashes;
- persist the unrounded optimizer vector, prediction, residual, bounds, seeds,
  restart/RNG state, package versions and dtype for any new fit;
- validate transfer claims on held-out or jointly fitted graphite/Si/blend
  data under one declared protocol and normalization;
- avoid phase, host, heat or kinetic interpretation without independent
  evidence;
- do not infer chemical-storage, reaction-extent or current sign from this
  magnitude-processed profile.
