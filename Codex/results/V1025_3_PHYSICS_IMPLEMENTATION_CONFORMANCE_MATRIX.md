# v1.0.25.3 Physics–Implementation Conformance Matrix

## Scope

This matrix evaluates only the branch-local candidate under
`Codex/work/v1025_2_physics_branch/conformance_model/` against the 32 decisions
in `V1025_2_PHYSICS_DECISION_LEDGER.md`. It does not upgrade the legacy release
implementation and does not treat the discarded v1.0.26 work as scientific
authority.

Status meanings:

- `CONFORMANT`: implemented and exercised by an explicit gate.
- `BOUNDED`: the implemented subset is conformant, while the unimplemented
  closure remains explicit.
- `FROZEN EMPIRICAL`: reproducible observation artifact, not a physical model.
- `NOT IMPLEMENTED`: manuscript physics is retained, but no computational
  closure is claimed.

## Decision-Level Matrix

| Physics ID | Branch implementation | Verification | Status | Remaining boundary |
|---|---|---|---|---|
| PHY-001 | `IdealTransition.orientation` and signed transition capacity remain immutable across charge/discharge usage | orientation and signed-storage gates | CONFORMANT | no branch landscape |
| PHY-002 | physical API exposes internal equilibrium potential only; applied and drive potentials are not silently aliased | API/static inspection | BOUNDED | terminal and transport maps not implemented |
| PHY-003 | `relax_monotonic_curve` and `relax_time_trajectory` are separate APIs | reversal, duplicate-axis and acquisition-order gates | CONFORMANT | none for the implemented first-order closure |
| PHY-004 | `LinearChemicalBackground`, empirical baseline and `ObservationContract` are distinct types | background derivative and sign-recovery gates | CONFORMANT | no general nonlinear background free energy |
| PHY-005 | electron stoichiometry is an explicit transition field and never derived from width | ideal-transition gates | CONFORMANT | reaction assignment remains user evidence |
| PHY-006 | only the ideal independent-site transition is in the production candidate | derivative and limiting-domain gates | BOUNDED | nonideal branch solver intentionally absent |
| PHY-007 | skew-logistic components exist only in `EmpiricalSkewProfile` | area, nonnegativity and profile-hash gates | CONFORMANT | no physical interpretation is exposed |
| PHY-008 | regular solution is excluded from the production package and retained as theory in the manuscript | public-API and source inspection | CONFORMANT BY EXCLUSION | stable/metastable/coexistence solver not implemented |
| PHY-009 | ideal equilibrium width, empirical skew width and causal lag are owned by different types | API and cross-object immutability gates | BOUNDED | physical static-disorder distribution not implemented |
| PHY-010 | `PhysicalHost.chemical_capacity` is the explicit background-plus-signed-transition balance | derivative and inverse-recovery gates | CONFORMANT | spatial field balance absent |
| PHY-011 | inverse use requires an analytic monotonic sign certificate and a valid bracket | nonmonotonic and unbracketed-target gates | CONFORMANT | mixed-sign EOS requires a future proof |
| PHY-012 | `PhysicalHostBlend` and `EmpiricalSkewProfile` have disjoint contracts | pooled balance and API separation gates | CONFORMANT | finite-rate host current allocation absent |
| PHY-013 | no graphite/LCO/Si numerical constants are promoted to defaults; material claims remain manuscript modules | source/static inspection | BOUNDED | evidence-backed material presets not implemented |
| PHY-014 | no forward/backward kinetic network is claimed; causal target relaxation is separate | API inspection | NOT IMPLEMENTED | occupancy-flux and target/mobility closure required |
| PHY-015 | `EyringRateSI` makes the transmission factor explicit | independent SI formula gate | CONFORMANT | temperature-dependent transmission needs a new closure |
| PHY-016 | physical rates are s⁻¹; hour-basis compatibility is a named immutable type with explicit `/3600` conversion | exact unit-conversion gates | CONFORMANT | none |
| PHY-017 | both causal APIs require `CausalInitialState` with declared provenance | missing/invalid initial-state gates | CONFORMANT | measured prehistory remains external input |
| PHY-018 | the manuscript separates normalized relaxation measure from residual amplitude | manuscript static/full-read check | NOT IMPLEMENTED | spectrum and amplitude types required |
| PHY-019 | transition-center temperature dependence is explicit; fixed-state, fixed-charge and path derivatives are not conflated | API/source inspection | BOUNDED | coupled fixed-charge OCV derivative solver absent |
| PHY-020 | `reversible_heat_generation_w` implements generation-positive `-I T dUeq/dT` | two-current-sign gates | CONFORMANT | half-cell spatial allocation remains open |
| PHY-021 | no entropy decomposition is inferred from empirical shape | API/source inspection | NOT IMPLEMENTED | measured or fully derived entropy basis required |
| PHY-022 | local network production and terminal-lumped loss are separate helpers with separate domains | nonnegativity, symmetry and domain gates | CONFORMANT | general transport-field dissipation absent |
| PHY-023 | heat helpers do not add a second relaxation-heat term | API/source inspection | BOUNDED | full hidden-energy balance not implemented |
| PHY-024 | no thermal-tail power law is shipped | API/source inspection | NOT IMPLEMENTED | fresh energy/power derivation required |
| PHY-025 | no charge/discharge state reversal or empirical branch offset is shipped | API/source inspection | NOT IMPLEMENTED | landscape, target or mobility branch closure required |
| PHY-026 | local flux-ratio production is implemented, but no global branch detailed-balance claim is made | local-network heat gates | BOUNDED | explicit kinetic graph required |
| PHY-027 | no loop-area-to-heat helper is shipped | API/source inspection | NOT IMPLEMENTED | closed-state-cycle accounting required |
| PHY-028 | stored-8dp direct14 artifact is immutable and hash-checked on every load | source, artifact, array, prediction and residual hash gates | FROZEN EMPIRICAL | original optimizer state unavailable |
| PHY-029 | empirical metadata and API forbid host/mechanism assignment | type and metadata gates | CONFORMANT | experimental protocol remains unknown |
| PHY-030 | evidence grade and authority note travel with the empirical profile; material claims carry explicit grades in the manuscript | metadata/static inspection | CONFORMANT | future presets need the same contract |
| PHY-031 | implementation language is allowed only in the implementation appendix; paths and work history remain external | complete include-graph verifier and adversarial self-tests | CONFORMANT | none |
| PHY-032 | public types cite physics IDs and every implemented block has unit/sign/domain/invariant tests | source inspection and 51-test suite | CONFORMANT | future closures must extend this matrix |

## Release Interpretation

The branch candidate is a conformant core and a frozen empirical reference, not
a complete finite-rate graphite–Si–LCO production model. Rows marked
`NOT IMPLEMENTED` are deliberate scientific boundaries, not silent fallbacks.
The empirical direct14 profile may be used to reproduce the accepted processed
curve; it may not be used to assign hosts, phases, reaction stoichiometry,
entropy, kinetics or heat.
