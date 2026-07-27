# v1.0.25.3 conformance model

This branch-local package is a clean implementation downstream of
`V1025_2_PHYSICS_DECISION_LEDGER.md`. It does not modify or import the release
implementation.

The public boundary is intentional:

- `EmpiricalSkewProfile` represents a positive magnitude observation only.
  `empirical_blend14_v10252()` loads the surviving stored-8dp direct14 fit.
- `IdealTransition`, `PhysicalHost`, and `PhysicalHostBlend` represent signed
  chemical storage with fixed state orientation and explicit electron
  stoichiometry. The blend is equilibrium-only.
- `ObservationContract` records whether sign is retained or destroyed.
- the two causal APIs distinguish a monotonic voltage curve from a
  time-ordered trajectory and require an explicit initial/prehistory state.
- `EyringRateSI` produces rates in s^-1. `LegacyCompatibleHourRate` is a
  separate strictly positive magnitude type and converts only through an
  explicit method. Signed C-rate is handled only by the conversion function.
- reversible, terminal-lumped irreversible, and local-network irreversible
  heat are separate functions with separate domains.

Regular-solution equilibrium is intentionally absent from this production
candidate. Under PHY-008 it remains theory-only until stable/metastable branch
selection, coexistence closure, conservation, identifiability, and solver tests
are accepted.

There is no mutable global profile, material case string, branch-controlled
state reversal, observation-to-chemical fallback, nonfinite-lag fallback, or
implicit empirical-to-physical conversion.
