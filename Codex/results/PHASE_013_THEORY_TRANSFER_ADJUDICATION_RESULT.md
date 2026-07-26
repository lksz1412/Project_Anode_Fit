# Phase 013 Theory Transfer Adjudication Result

Date: 2026-07-20

## Inputs

- Phase 011 gap matrix and result.
- Phase 012 integrated candidate matrix.
- Complete Chapter 1, LCO, Chapter 3, and common-method worker reports and
  candidate files.
- Current v1.0.23 LCO TeX/code/test evidence recorded by Phases 006 and 010 and
  rechecked in this workstream.

## Output

- Canonical transfer matrix:
  `D:\Projects\Project_Anode_Fit\Codex\results\phase013_theory_integration_adjudication.csv`

The matrix contains 32 adjudications:

| Scope | Rows |
|---|---:|
| Chapter 1 | 7 |
| Chapter 2 LCO | 10 |
| Chapter 3 | 10 |
| Common methods | 5 |

Each row records the current statement, proposed change type, replacement model
or boundary, required state variables, parameters, data, expected code impact,
identifiability risk, and a falsification test.

## Chapter 1 Decision

The chapter should not present a single regular-solution curve and fitted peak
mixture as a unique physical account of graphite. The defensible structure is:

1. multilayer staging thermodynamics;
2. reaction/phase-transformation dynamics;
3. particle and porous-electrode transport/heterogeneity;
4. an explicit measurement and preprocessing operator;
5. nonlinear identifiability and model-discrepancy analysis.

The full-read Cordoba 2024, Borghed 2026, Jamnuch 2023, and BMINN preprint
support bounded corrections. The MCMB numerical entropy prior and targeted
rate/temperature papers require complete reading before equation-level use.

## LCO Decision

The current LCO model has two independent critical defects:

1. **Wrong ordering state space.** Composition x alone cannot encode
   order/disorder at fixed x. Positive `Omega` in an x-only regular solution is
   demixing curvature, not a Li-order parameter.
2. **Unsupported electronic gate.** No direct 2021-2026 LCO source found here
   derives the logistic DOS gate, its O1-to-O3 transfer, `g_max`, or
   `Delta x=0.05`.

Additional implementation defects remain controlling: the current code samples
only `x=x_MIT`, freezes `T=298.15 K`, contains competing width definitions,
and tests same-model regression rather than the documented composition- and
temperature-dependent thermodynamics.

### Option A: Immediate Recovery

Recommended now. Replace microscopic labels with a branch-specific total
`U_ref(x)` and `kappa(x)=dU/dT` representation using constrained splines or a
small smooth basis. Localized features may remain only as empirical features
with fitted amplitude, center, width, covariance, and held-out validation.

This option has low solver burden and repairs false claims. It does not predict
ordering or the metal-insulator mechanism.

### Option B: Medium Rebuild

Use `g(x,eta,T)` with at least one justified sublattice/order coordinate and,
for realistic O3 Li0.5CoO2 symmetry, a complete order-parameter vector. Minimize
over eta for equilibrium; use Cahn-Hilliard for conserved x and Allen-Cahn for
nonconserved order only if dynamics are claimed.

This option requires variant symmetry, transition-temperature, diffraction, and
OCV data. It must demonstrate that projection to x does not create a false
spinodal.

### Option C: Long-term Research Model

Build a direct-LCO DFT configuration set, cluster expansion, semi-grand or
umbrella Monte Carlo, and a differentiable `G(x,eta,T)` surrogate. Add
vibrational and correlated-electronic terms only from compatible
composition/structure calculations.

This is the strongest configurational architecture but is not a parameter patch.
Shojaei's present model itself misses the high-x metal-insulator plateau and
vibrational entropy.

## Chapter 3 Decision

Preserve the restricted equilibrium independent-host model only with explicit
scope. Correct the mass/capacity basis and stress geometry immediately.
Finite-rate, phase/path, finite-strain, SiOx/Si-C internal-host, fracture/LAM,
SEI/inventory, CBD/contact, and ICA-identifiability claims require additional
states rather than algebraic relabeling.

All Chapter 3 recent-paper transfers remain provisional for implementation
because the worker performed targeted article-body reads rather than complete
first-to-last reads.

The late completeness pass adds a direct diagnostic boundary from Wan et al.
(2026) and Natterer et al. (2026): a fitted effective Si OCP and transition SoC
may be useful protocol-conditioned states, but neither low-rate voltage nor EIS
alone proves a unique host-resolved degradation mechanism. SoC, temperature,
aging pathway, preprocessing, and model discrepancy must remain explicit, and
orthogonal host evidence is required for material attribution.

## Cross-chapter Decision

- Static DFT energy, finite-temperature free energy, and measured `dU/dT` are
  different categories and must carry typed provenance.
- Configurational, vibrational, and electronic components are not separately
  identified by total OCV/reversible-heat observations without orthogonal priors.
- Equilibrium coexistence, spinodal stability loss, kinetic hysteresis, and
  derivative-signal width must remain distinct outputs.
- A local Jacobian or fitted decomposition is not a certificate of physical
  uniqueness.

## Validation

- Structured CSV parsing: passed.
- Integration IDs: 32 nonblank, zero duplicates.
- Every cited source ID resolves to the Phase 012 candidate matrix: passed.
- Chapter 1, LCO, Chapter 3, and common-method rows present: passed.
- Every proposed transfer includes a falsification test: passed.
- No source/code/Claude/Git modification occurred.

## Gate

`THEORY_TRANSFER_ADJUDICATION_PASS`

The recommended LCO path is Option A immediately, Option B after direct ordering
data and symmetry decisions, and Option C as a research program. Chapter 1 and
Chapter 3 dispositions remain explicit and are not hidden behind the LCO
priority.
