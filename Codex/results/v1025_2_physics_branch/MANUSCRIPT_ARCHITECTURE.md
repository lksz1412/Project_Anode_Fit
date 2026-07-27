# v1.0.25.2 Physics-Conformance Manuscript Architecture

## Status

`ARCHITECTURE CANDIDATE — SOURCE FILES NOT YET PROMOTED`

기존 Codex candidate와 `Claude/docs/v1.0.25.2` 원문은 변경하지 않는다.
이 디렉터리의 새 source만 보완본 후보가 된다.

## Governing direction

\[
\text{physical assumptions}
\longrightarrow
\text{state and conservation laws}
\longrightarrow
\text{equilibrium}
\longrightarrow
\text{kinetics}
\longrightarrow
\text{heat/hysteresis}
\longrightarrow
\text{observation}
\longrightarrow
\text{implementation}.
\]

역방향 의존은 허용하지 않는다. 특히 current class/function/default가
manuscript의 물리식을 결정하지 않는다.

## Target tree

```text
v1025_2_physics_branch/
├── manuscript/
│   ├── anode_physics_master.tex
│   ├── common/
│   │   ├── notation.tex
│   │   ├── conventions.tex
│   │   └── evidence_grades.tex
│   ├── chapters/
│   │   ├── ch01_equilibrium_observation.tex
│   │   ├── ch02_thermodynamics_heat.tex
│   │   ├── ch03_kinetics.tex
│   │   ├── ch04_integrated_eos.tex
│   │   └── ch05_hysteresis.tex
│   ├── materials/
│   │   ├── graphite_application.tex
│   │   ├── lco_application.tex
│   │   └── si_blend_application.tex
│   ├── empirical/
│   │   └── skew14_profile.tex
│   └── appendices/
│       ├── assumption_register.tex
│       ├── derivation_checks.tex
│       └── implementation_interface.tex
└── MANUSCRIPT_ARCHITECTURE.md
```

`implementation_interface.tex`만 code symbol을 언급할 수 있다. 실제 file
path, branch, commit, test output은 이 appendix에도 넣지 않고 외부 Markdown
conformance ledger에 둔다.

## Chapter ownership

### Chapter 1 — Equilibrium, charge balance, and observation

Owns:

- physical state definitions
- applied/internal/equilibrium potential distinction
- chemical charge balance
- signed chemical-storage coefficient versus dataset-level sign/magnitude map
- background-storage versus observation-baseline split
- ideal logistic baseline
- empirical skew observation layer
- ICA/DVA coordinate transformation
- identifiability at the equilibrium/observation level

Does not own:

- activation barrier spectrum
- reversible/irreversible heat
- branch-dependent state redefinition
- material-specific LCO or Si closure

Primary salvage:

- Codex Ch1 charge balance and potential distinctions
- v1.0.25.2 graphite equilibrium/observation derivations

Mandatory repairs:

- remove width-derived electron number
- correct small-tail ICA coefficient
- separate normalized relaxation measure from residual amplitude
- classify regular solution and skew logistic by evidence/status

### Chapter 2 — Thermodynamics and heat

Owns:

- fixed-state and fixed-charge temperature derivatives
- standard versus configurational/partial-molar entropy
- reversible heat sign convention
- local entropy production
- control-volume energy balance
- double-counting exclusions

Does not replace:

- the LCO material chapter

Primary salvage:

- Codex Ch2 derivative hierarchy and entropy distinctions
- Codex Ch4 raw network entropy-production formula
- v1.0.25.2 fixed-charge implicit OCV derivative

Mandatory repairs:

- generation-positive reversible-heat sign
- OCV/transition entropy basis closure
- no \(RT/(Fw)\) heat multiplier
- no externally factored \(|I|\) for all internal dissipation
- rederive or delete thermal-tail mirror
- distinguish full-cell heat from half-cell local allocation

### Chapter 3 — Kinetics

Owns:

- forward/backward rates
- mobility versus stationary target
- local detailed balance
- Eyring/transition-state prefactor and transmission coefficient
- reaction stoichiometry
- causal relaxation and prehistory contract
- rate-unit convention

Primary salvage:

- Codex Ch3 mass-action skeleton
- \(\chi\) versus \(\beta\) separation
- Chapter 1 Level-A limiting model

Mandatory repairs:

- replace \(n_{\mathrm{eff}}=RT/(Fw)\) with physical \(z\)
- distinguish center-referenced mobility coordinate from chemical affinity
- use SI time units in the physical profile
- separate finite monotonic curve from time trajectory

### Chapter 4 — Integrated EOS/DAE

Owns:

- coupled state vector
- algebraic charge balance
- kinetic evolution
- thermal balance
- host coupling
- observation map
- initial/boundary conditions
- admissibility and limiting cases

This chapter is new. The current Codex Chapter 4 heat candidate is not used as
its spine; its useful entropy-production material moves to Chapter 2.

Required core:

\[
\mathbf 0=\mathbf G(\mathbf x,V_n,T,q),
\qquad
\dot{\mathbf x}=\mathbf f(\mathbf x,V_n,T,I),
\qquad
C_{\mathrm{th}}\dot T=\dot Q_{\mathrm{src}}-\dot Q_{\mathrm{loss}},
\qquad
y=\mathcal H(\mathbf x,V_n,T,I).
\]

The exact constitutive choices remain modular and evidence-graded.

### Chapter 5 — Hysteresis and cycling

Owns:

- fixed state orientation
- signed reaction extent/current
- fixed dataset observation sign separated from positive empirical magnitude
- true equilibrium versus metastable target
- branch-local free energy, nucleation and pinning
- dynamic lag versus rate-independent hysteresis
- cycle work and heat conditions
- rest and reversal

Primary salvage:

- current candidate's signed capacity coordinate
- observed gap decomposition
- full-cell/half-cell caution

Mandatory repairs:

- do not reverse the logistic orientation of the same \(\xi\)
- rederive charge heat without the false orientation flip
- distinguish local detailed balance from global equilibrium
- state observation-time/nucleation protocol for any \(I\to0\) claim

## Material modules

### Graphite

Preserve:

- staging evidence map
- phase-count versus curve-resolution distinction
- equilibrium/observation data

Open:

- transition-specific equilibrium width law
- static versus kinetic tail separation
- physical status of fitted narrow widths and saturated skew

### LCO

Preserve as a separate application:

- electronic/vibrational/configurational entropy decomposition
- order/disorder evidence
- fixed-charge entropy coefficient

Repair:

- do not equate a one-parameter regular-solution threshold with a specific
  ordered phase without the cluster-expansion bridge
- do not use unstable curvature as a positive equilibrium peak by absolute value
- separate half-cell entropy coefficient from local heat allocation

### Si and graphite--Si blend

Preserve:

- common-potential equilibrium coupling
- capacity/mass-fraction conversion
- Larché--Cahn reversible stress shift
- explicit mechanical and nonadditive gaps

Restrict:

- tier-C Si transitions are examples/seeds, not silent production truth
- additive finite-rate host response is an explicit first-order approximation
- plastic hysteresis and host current allocation remain unimplemented

## Empirical profile

The accepted 14-skew fit is not hidden inside a material model.

It owns:

- dataset and preprocessing hashes
- voltage window and sampling
- parameter order and surviving stored-8dp vector, with the missing original
  optimizer precision recorded as a provenance limitation
- background
- metric definition
- prediction/residual hashes

It does not own:

- host identity
- phase identity
- activation enthalpy
- reversible heat
- hysteresis mechanism

## Stable identifiers

Planned namespaces:

| Prefix | Owner |
|---|---|
| `OBS-*` | observation and coordinate map |
| `BAL-*` | charge/mass/energy balance |
| `EQ-*` | equilibrium |
| `KIN-*` | kinetics and memory |
| `THM-*` | temperature and heat |
| `HYS-*` | hysteresis and cycling |
| `MAT-GR-*` | graphite application |
| `MAT-LCO-*` | LCO application |
| `MAT-SI-*` | Si/blend application |
| `EMP-*` | empirical profile |
| `ASM-*` | assumption register |

Implementation symbols map to these IDs only in the implementation interface and
external conformance matrix.

## Migration map

| Existing source | Action |
|---|---|
| Codex Ch1 candidate | salvage charge balance, potential hierarchy, identifiability; repair blockers |
| Codex Ch2 candidate | salvage derivative/heat skeleton as new common Chapter 2; do not overwrite LCO |
| Codex Ch3 candidate | salvage forward/backward kinetics; replace width-derived electron number |
| Codex Ch4 candidate | move raw entropy-production material into Chapter 2 advanced section |
| Codex Ch5 candidate | salvage signed coordinate and branch taxonomy; replace state-orientation flip |
| v1.0.25.2 graphite | material evidence and tested equilibrium baseline |
| v1.0.25.2 LCO | preserve as LCO application; repair overclaims |
| v1.0.25.2 Si/blend | preserve as Si/blend application; retain GS boundaries |
| accepted 14-skew fit | immutable empirical module |
| code maps and test tables | external conformance artifacts |

## Promotion order

1. common notation and sign convention
2. Chapter 1 equilibrium/observation
3. Chapter 2 thermodynamics/heat
4. Chapter 3 kinetics
5. Chapter 4 integrated EOS
6. Chapter 5 hysteresis
7. material modules
8. empirical profile
9. implementation interface

각 장은 다음을 통과해야 다음 장의 입력이 된다.

- symbol ownership
- dimensions
- sign convention
- fixed/total derivative label
- limiting cases
- identifiability/evidence grade
- no implementation language outside the allowed boundary
