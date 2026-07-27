# Phase 046–053 v1.0.25.3 Reconstruction Result

## Outcome

A clean branch-local candidate was completed on
`codex/v1025_2-physics-conformance` without editing the v1.0.25.2 release
sources. The candidate version name is **v1.0.25.3 conformance**; it has not
been committed, pushed, merged or declared a release.

The reconstruction follows this evidence hierarchy:

1. v1.0.19 supplies the last relatively coherent legacy numerical core.
2. v1.0.22 contributes only the equilibrium common-potential host-blend idea.
3. v1.0.25 contributes the area-preserving empirical skew observation form.
4. v1.0.25.2 contributes the surviving stored-8dp direct14 empirical artifact.
5. v1.0.26 contributes no scientific authority. Files beneath a v1.0.26-named
   comparison directory are used only as forensic provenance for the surviving
   v1.0.25.2 artifact.

## Delivered Candidate

- Manuscript master:
  `Codex/results/v1025_2_physics_branch/manuscript/anode_physics_master.tex`
- Rendered PDF:
  `output/pdf/Anode_Physics_v1.0.25.3_conformance.pdf`
- Clean implementation:
  `Codex/work/v1025_2_physics_branch/conformance_model/`
- Immutable empirical artifact:
  `Codex/results/v1025_2_physics_branch/artifacts/empirical_blend14_v10252.json`
- Independent verification:
  `Codex/work/v1025_2_physics_branch/tests/`
- Updated decision-level matrix:
  `Codex/results/V1025_3_PHYSICS_IMPLEMENTATION_CONFORMANCE_MATRIX.md`

## Manuscript Result

The manuscript now proceeds in the required physical direction:

`state and sign conventions → charge conservation → equilibrium → kinetics →
heat and hysteresis → observation map`.

The physics body does not depend on implementation structure. Implementation
symbols occur only in `appendices/implementation_interface.tex`; repository
paths, version history and test output remain outside the manuscript.

The 16-source tree contains:

- common notation, sign/boundary conventions and evidence grades;
- equilibrium/observation, thermodynamics/heat, kinetics, integrated DAE/EOS
  and hysteresis chapters;
- graphite, LCO and graphite–Si material modules;
- a separately classified empirical direct14 observation module;
- assumption, derivation and implementation-interface appendices.

Each major claim has a stable OBS/BAL/EQ/KIN/THM/HYS/MAT/EMP/ASM identifier.
Material modules state what is literature-compatible, what remains empirical,
and what is OPEN. In particular, empirical peak count and fit quality do not
become host, phase, electron-number, entropy, kinetic or heat assignments.

## Implementation Result

The clean package implements only closures that can presently be defended:

- immutable SI constants and numerically stable logistic evaluation;
- fixed state orientation, signed transition storage and explicit electron
  stoichiometry;
- explicit chemical background and monotonic equilibrium charge-balance
  inversion;
- equilibrium-only common-potential physical host blending;
- signed, fixed-sign and irreversible magnitude observation contracts;
- separate monotonic-curve and time-trajectory causal relaxation APIs with
  explicit initial-state provenance;
- SI Eyring rate and an explicitly segregated legacy hour-rate magnitude;
- separate reversible, terminal-lumped and local-network irreversible heat
  laws with fail-fast domains;
- immutable empirical direct14 loading with full artifact and array hashes.

No mutable material/profile switch, observation-to-chemical fallback,
nonfinite-lag-to-equilibrium fallback, branch state reversal, production
regular-solution solver or empirical-to-physical conversion is present.

During final root review, three additional guards were added:

- negative chemical-background capacitance is rejected;
- physical-constant arguments are type-checked;
- causal integration rejects a missing/non-contract initial state.

## Frozen Empirical Result

The accepted object is a **positive magnitude observation profile**, not a
physical host model.

- components: 14
- stored parameter count: 57
- stored precision: 8 decimal places
- processed points: 1,280
- processed voltage window: 0.060–0.700 V
- source protocol: `UNKNOWN`
- stored-parameter SHA-256:
  `08216da1095a02bcb789a60f577f4afd1d581ad659a8129edaba7dc0dc5910d5`
- reconstructed prediction SHA-256:
  `53cc3c3795be327b90a5d040497074bc51f5a141d0b7629bd34a60682d71f800`
- reconstructed residual SHA-256:
  `1b874701ac72403f2836b352386e3c3a4f658c49238fd2fcf0a4931fd79398ec`
- independently recomputed:
  `R² = 0.99964941790404`
- working-likelihood:
  `BIC_57 = -4760.653827485789`

The original full-precision optimizer vector, original prediction, selected
seed/restart state, termination metadata, package environment and active-set
state are unavailable. Stored equality to a declared bound is therefore not
reported as proof of an active constraint or a global optimum.

## Verification

| Gate | Result |
|---|---|
| branch conformance suite | 51/51 PASS with Python warnings promoted to errors |
| manuscript include/static boundary | 16 sources, 15 include edges, 183 labels, 32 references, 0 issues |
| direct14 source/dependency/artifact/array hashes | PASS |
| direct14 prediction, residual and R² reconstruction | PASS |
| physical-host derivative, monotonic certificate and inverse recovery | PASS |
| observation sign destruction/recovery contracts | PASS |
| causal curve/trajectory and initial-state contracts | PASS |
| SI Eyring, `/3600` conversion and heat-sign/domain checks | PASS |
| legacy v1.0.25 gates | 9/9 PASS |
| legacy v1.0.24/v1.0.19 regression and blend gates | PASS |
| XeLaTeX | PASS, 28 A4 pages |
| final TeX log | 0 missing characters, 0 overfull boxes, 0 unresolved refs/citations |
| PDF visual QA | all 28 pages rendered; contact sheets plus key full-page checks PASS |
| PDF font check | NanumGothic regular/bold embedded and Unicode-mapped |

Final aggregate hashes:

- 16 TeX-source manifest stream:
  `f674b63fa232a5edc8099450380379c45a2ba0a6910ee2a576c10aae39ef9ad8`
- implementation Python-source manifest stream:
  `f30b9738553848c3851c3b7f0b6d6b7d712a4e83f374cbf8bb3d7bc2aaed13d2`
- test Python-source manifest stream:
  `98664d088eb29a24156b02d952bb5f7f487c84f3478249824a5d48caa276150f`
- empirical artifact file:
  `5f352eb95f0fe70cf4f277d4d3073015d3f43db04cc0471d4c016bf270aaea6a`
- final PDF:
  `9832400c55df88874699a0eaaf0f392da6dcd82e9389990b25b62e07978f83`

## Deliberately Open

The following are not defects to be hidden by a new fit:

1. experimental protocol for the frozen direct14 source;
2. microscopic host/phase assignment of the 14 empirical components;
3. material-specific regular-solution parameters and stable/metastable branch
   construction;
4. forward/backward kinetic-network closure and relaxation-spectrum amplitude;
5. fixed-charge OCV entropy decomposition and half-cell spatial heat allocation;
6. Si stress/plasticity/fracture/contact and finite-rate host current allocation;
7. closed-cycle conditions needed to equate hysteresis-loop area with heat.

## Original-Tree Guard

`Claude/docs/v1.0.24.1/CODE_GUIDE_v24.html` was already dirty at entry and was
kept outside the work scope. No Claude release source was edited. The final
tracked-file status under `Claude/` still contains only that pre-existing path.
