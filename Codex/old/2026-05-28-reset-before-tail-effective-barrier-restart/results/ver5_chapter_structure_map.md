# ver5 Chapter Structure Map

Source:
`D:\Projects\Project_BatteryData_Display_임시저장소\새 폴더\drive-download-20260527T100231Z-3-001\graphite_ica_dynamic_ver5.tex`

Created: 2026-05-27

Phase: 002

## Read Coverage

| Source | Required Range | Actual Range Read | Status | Notes |
|---|---:|---:|---|---|
| `graphite_ica_dynamic_ver5.tex` | 1-1974 | 1-400, 401-800, 801-1200, 1201-1600, 1601-1974 | READ_FULL | First line `\documentclass...`; last line `\end{document}`; heading/label scan cross-checked |

## Overall Finding

`graphite_ica_dynamic_ver5.tex` is a single LaTeX document that stacks five historical layers:

1. `ver.1`: dynamic graphite ICA/DVA base formula.
2. `ver.2`: heat-generation approximation and fitting layer.
3. `ver.3`: electrochemical reaction-kinetics layer.
4. `ver.4`: integrated state/observation/fitting system.
5. `ver.5`: hysteresis/branch-memory layer.

The user's proposed rename from `ver.1`-`ver.5` to Chapter 1-5 is structurally supported by the source. However, the historical `ver.1` block in this file is not automatically the final Chapter 1 because the user has separately identified `graphite_ica_charge_balance_ver1_rechecked2.tex` as the corrected restart file. Therefore, this map treats the old `ver.1` block as the structural ancestor of Chapter 1, not as final Chapter 1 content.

## Candidate Chapter Mapping

| Candidate Chapter | Historical Label | Source Line Range | Core Claim | Key Equations / Objects | Interface To Other Chapters | Confidence |
|---|---|---:|---|---|---|---|
| Preamble | document setup | 1-61 | Article setup, Korean/LaTeX packages, title still says `ver.1` | macros for `\OCV`, `\app`, `\eff`, `\SOC`; title/header metadata | none | 확정 |
| Chapter 1 | ver.1 basic formula | 62-523 | Graphite staging ICA/DVA is modeled through phase-transition progress variables `\xi_j`; peaks arise from `d\xi_j/dq`; kinetic delay creates peak broadening and tail | `eq:main_spine`, `eq:OCV_voltage_model`, `eq:xi_eq_basis`, `eq:k_basic`, `eq:xi_ode_t`, `eq:xi_ode_q`, `eq:xi_distribution`, `eq:Qn`, `eq:ICA_param`, `eq:DVA_param` | Passes `d\xi_j/dq`, `Q_n(q)`, `V_{n,\app}`, `R_n`, and fitting constraints to later layers | Historical block 확정; final Chapter 1 content 추정 until Phase 003 |
| Chapter 2 | ver.2 heat layer | 525-852 | Adds irreversible and reversible heat approximations while preserving Chapter 1 progress dynamics | `eq:v2_Vapp_from_v1`, `eq:v2_xi_dyn_from_v1`, `eq:v2_heat_decomp`, `eq:v2_irr_I2R`, `eq:v2_entropy_basis`, `eq:v2_heat_final`, `eq:v2_lumped_heat`, `eq:v2_heat_loss_function` | Uses `d\xi_j/dq` from Chapter 1 as heat/entropy basis; passes heat terms to Chapter 4 | 확정 |
| Chapter 3 | ver.3 electrochemical kinetics | 855-1118 | Generalizes the driving force into reaction affinity/overpotential and connects the relaxation model to Butler-Volmer and forward/backward rates | `eq:v3_xieq_rule`, `eq:v3_k_basic`, `eq:v3_A_eta`, `eq:v3_BV_general`, `eq:v3_asinh_eta`, `eq:v3_forward_backward`, `eq:v3_xieq_from_rates`, `eq:v3_current_partition` | Supplies reaction-resolved or reduced driving-force forms to Chapter 4 and branch-specific Chapter 5 | 확정 |
| Chapter 4 | ver.4 integrated system | 1122-1516 | Combines Chapters 1-3 into a computable state vector, state equations, observation equations, objective function, and fitting sequence | `eq:v4_state_vector`, `eq:v4_state_q`, `eq:v4_state_xi`, `eq:v4_state_T`, `eq:v4_obs_vn`, `eq:v4_obs_Qn`, `eq:v4_obs_ica`, `eq:v4_obs_dva`, `eq:v4_loss` | Defines the common state/observation system that Chapter 5 extends with branch and memory variables | 확정 |
| Chapter 5 | ver.5 hysteresis layer | 1520-1974 | Extends the integrated system with branch index, branch-specific progress dynamics, structural memory variables, branch ICA/DVA, hysteresis energy, and branch fitting order | `eq:v5_affinity_branch`, `eq:v5_voltage_full`, `eq:v5_xi_branch_time`, `eq:v5_xi_branch_q`, `eq:v5_Geff_branch`, `eq:v5_k_branch`, `eq:v5_fb_branch`, `eq:v5_z_time`, `eq:v5_vmem`, `eq:v5_ica_branch`, `eq:v5_dva_branch`, `eq:v5_loop_energy` | Final branch/hysteresis extension of Chapter 1-4 stack | 확정 |

## Section Inventory

### Preamble and Chapter 1 Candidate

| Line Range | Original Heading | Historical Label | Candidate Chapter | Role |
|---:|---|---|---|---|
| 1-61 | document setup/title | ver.1 metadata | preamble | Sets title/header as `동역학 기반 흑연 음극 ICA/DVA 기본식 ver.1` even though the file contains later layers |
| 62-89 | `문서의 목적과 적용 범위` | ver.1 | Chapter 1 | Establishes spine `Delta G_eff -> k_j -> dxi/dt -> xi(q) -> dxi/dq -> dQ/dV, dV/dQ` |
| 91-135 | `공통 컨벤션` | ver.1 | Chapter 1 | Defines symbols, q coordinate, voltage conventions, and `V_{n,\app}=V_{n,\OCV}+s_IIR_n` |
| 137-152 | `흑연 staging과 effective transition index` | ver.1 | Chapter 1 | Maps graphite staging to effective peak index `j` |
| 154-174 | `전위 모델: OCV 기준과 0.2C 기준` | ver.1 | Chapter 1 | Defines OCV and 0.2C reference voltage formulas |
| 176-201 | `평형 진행률` | ver.1 | Chapter 1 | Defines `\xi_{j,\eq}` from `V_{n,\OCV}` using logistic/erf forms |
| 203-250 | `유효 장벽과 상변이 속도상수` | ver.1 | Chapter 1 | Defines `Delta G_a`, driving force `A_j`, `Delta G_eff`, `k_j`, and runaway guards |
| 252-284 | `상변이 진행률 동역학` | ver.1 | Chapter 1 | Defines relaxation ODE in time and q coordinates |
| 286-323 | `장벽 분포 평균 동역학` | ver.1 | Chapter 1 | Adds distributed barrier domains and averaged progress rate |
| 325-365 | `ICA와 DVA 유도` | ver.1 | Chapter 1 | Defines `Q_n(q)`, `dQ/dq`, `dV/dq`, `dQ/dV`, and `dV/dQ` |
| 367-394 | C-rate and temperature sections | ver.1 | Chapter 1 | Explains broadening/tail and temperature dependence |
| 396-468 | empirical fit, procedure, objective, identifiability | ver.1 | Chapter 1 | Connects EMG initialization, fitting loss, and constraints |
| 470-500 | model level and `ver.2로 전달되는 기준식` | ver.1 | Chapter 1 -> Chapter 2 interface | Names equations passed to heat layer |
| 502-523 | checklist and references | ver.1 | Chapter 1 support | Checklist and five literature refs |

### Chapter 2 Candidate

| Line Range | Original Heading | Historical Label | Candidate Chapter | Role |
|---:|---|---|---|---|
| 525-563 | header and `ver.1에서 전달받는 기준식` | ver.2 | Chapter 2 | Declares that heat layer keeps Chapter 1 definitions |
| 565-584 | `열 발생 항의 분해` and sign convention | ver.2 | Chapter 2 | Splits irreversible and reversible heat |
| 586-628 | `비가역 열 근사` | ver.2 | Chapter 2 | Defines effective overpotential and `I^2R_n` approximation |
| 630-650 | `가역 열의 기본식` | ver.2 | Chapter 2 | Defines entropy coefficient and warns against apparent-voltage derivative misuse |
| 652-711 | progress-rate entropy basis | ver.2 | Chapter 2 | Uses `d\xi_j/dq` as reduced entropy/heat basis |
| 713-749 | final heat equation and thermal feedback | ver.2 | Chapter 2 | Defines heat model and temperature feedback into Chapter 1 quantities |
| 751-810 | separation, fitting, objective, identifiability | ver.2 | Chapter 2 | Fitting strategy for heat coefficients |
| 812-835 | `ver.3으로 전달되는 기준식` | ver.2 | Chapter 2 -> Chapter 3 interface | Passes driving force and heat formula to reaction kinetics |
| 837-852 | checklist | ver.2 | Chapter 2 support | Confirms ver.1 definitions preserved |

### Chapter 3 Candidate

| Line Range | Original Heading | Historical Label | Candidate Chapter | Role |
|---:|---|---|---|---|
| 855-869 | `ver.3 전기화학 반응속도론 계층` | ver.3 | Chapter 3 | States separation between OCV-based equilibrium and overpotential-based rate |
| 871-894 | driving force generalization | ver.3 | Chapter 3 | Generalizes `A_j` into `F eta_j` and warns against double-counting |
| 896-961 | Butler-Volmer and approximations | ver.3 | Chapter 3 | Adds BV, low-overpotential, asinh, and Tafel forms |
| 963-975 | exchange current and temperature dependence | ver.3 | Chapter 3 | Defines `i_0(q,T)` and `nu_j(T)` temperature terms |
| 977-1008 | forward/backward rate | ver.3 | Chapter 3 | Shows relaxation model as reduced form of forward/backward rates |
| 1010-1037 | current partition and model choice | ver.3 | Chapter 3 | Adds channel current and reduced/reaction-resolved/hybrid choice |
| 1039-1064 | identifiability and fitting | ver.3 | Chapter 3 | Staged fitting and parameter coupling |
| 1066-1099 | `ver.4로 전달되는 기준식` | ver.3 | Chapter 3 -> Chapter 4 interface | Passes rate and driving-force forms to integrated system |
| 1101-1118 | checklist | ver.3 | Chapter 3 support | Confirms preceding layers unchanged |

### Chapter 4 Candidate

| Line Range | Original Heading | Historical Label | Candidate Chapter | Role |
|---:|---|---|---|---|
| 1122-1131 | `ver.4 통합 시스템 적층 확장` | ver.4 | Chapter 4 | Declares integration of ver.1-3 without changing them |
| 1133-1176 | `ver.1에서 전달받은 기본 동역학` | ver.4 | Chapter 4 | Restates voltage, equilibrium progress, ODEs |
| 1178-1204 | `ver.2에서 전달받은 발열식` | ver.4 | Chapter 4 | Restates heat split and reduced heat model |
| 1206-1251 | `ver.3에서 전달받은 반응속도론 연결` | ver.4 | Chapter 4 | Restates driving force, barrier, rate, BV double-count warning |
| 1253-1320 | state variables and state equations | ver.4 | Chapter 4 | Defines state vector, inputs, q/xi/T equations |
| 1322-1379 | observation equations | ver.4 | Chapter 4 | Defines voltage, capacity, ICA, DVA observations |
| 1381-1395 | integrated calculation procedure | ver.4 | Chapter 4 | Stepwise simulation order |
| 1397-1448 | loss, fitting order, model level | ver.4 | Chapter 4 | Multi-observable objective and staged fitting |
| 1450-1497 | validation and `ver.5로 전달되는 기준식` | ver.4 | Chapter 4 -> Chapter 5 interface | Passes branch-extension baseline |
| 1499-1516 | checklist | ver.4 | Chapter 4 support | Confirms no modification of previous layers |

### Chapter 5 Candidate

| Line Range | Original Heading | Historical Label | Candidate Chapter | Role |
|---:|---|---|---|---|
| 1520-1538 | `ver.5 히스테리시스 적층 확장` | ver.5 | Chapter 5 | Adds hysteresis layer without changing Chapter 1-4 |
| 1540-1569 | branch index and signs | ver.5 | Chapter 5 | Defines `p`, `s_I^p`, `s_{\phi,j}^p`, branch affinity |
| 1571-1604 | hysteresis decomposition | ver.5 | Chapter 5 | Splits resistance, dynamic delay, structural memory, thermal components |
| 1606-1640 | branch progress dynamics | ver.5 | Chapter 5 | Adds branch index to `xi_j` ODE and equilibrium progress |
| 1642-1704 | branch barrier, rate, forward/backward model | ver.5 | Chapter 5 | Adds branch-specific `Delta G_eff`, `k_j`, and forward/backward rates |
| 1706-1741 | structural memory variable | ver.5 | Chapter 5 | Defines `z_j`, `z` relaxation, memory voltage term |
| 1743-1768 | branch barrier distribution | ver.5 | Chapter 5 | Adds branch-indexed distribution dynamics |
| 1770-1807 | branch ICA and DVA | ver.5 | Chapter 5 | Defines branch `Q_n`, `dQ/dq`, ICA, DVA |
| 1809-1885 | observed hysteresis and energy | ver.5 | Chapter 5 | Defines branch voltage difference, residual hysteresis, loop energy |
| 1887-1935 | simultaneous fitting objective and order | ver.5 | Chapter 5 | Multi-branch voltage/ICA/DVA/temperature objective and staged fitting |
| 1937-1974 | identifiability and checklist | ver.5 | Chapter 5 support | Lists parameter confounding risks and validation checklist |

## Key Equation Extraction

### Chapter 1 Candidate - Dynamic ICA/DVA Base

| Object | Line Evidence | Role |
|---|---:|---|
| Main spine | 66-79 | `Delta G_eff -> k_j -> dxi/dt -> xi(q) -> dxi/dq -> dQ/dV, dV/dQ` |
| Apparent voltage | 130-132, 157-159 | Defines `V_{n,\app}=V_{n,\OCV}+s_IIR_n` |
| 0.2C conversion | 165-172 | Rewrites apparent voltage from 0.2C reference |
| Equilibrium progress | 179-197 | Defines `\xi_{j,\eq}` from OCV via logistic/erf |
| Effective barrier and rate | 206-232 | Defines `Delta G_a`, `A_j`, `Delta G_eff`, `k_j` |
| Progress ODE | 255-273 | Defines time and q-domain dynamics for `\xi_j` |
| Barrier distribution | 291-319 | Defines `k_j(g)`, `\xi_j(g,q)`, averaged `\xi_j(q)` |
| Capacity and derivatives | 328-363 | Defines `Q_n`, `dQ/dq`, `dV/dq`, ICA, DVA |
| Fitting and identifiability | 398-468 | EMG initial fit, objective, constraints |
| Chapter 2 interface | 485-500 | Passes `d\xi_j/dq`, `dQ/dq`, ICA formula |

### Chapter 2 Candidate - Heat Layer

| Object | Line Evidence | Role |
|---|---:|---|
| Inputs from Chapter 1 | 533-558 | Reuses `V_{n,\app}`, `\xi_{j,\eq}`, `d\xi_j/dq`, `Q_n`, distribution |
| Heat decomposition | 567-569 | Splits heat into irreversible and reversible |
| Irreversible heat | 589-609 | Uses effective overpotential and `I^2R_n` |
| Reversible heat | 632-644 | Uses entropy coefficient |
| Progress-based entropy basis | 655-705 | Uses `d\xi_j/dq` as heat/entropy basis |
| Thermal feedback | 734-748 | Temperature feeds back into `Delta G_a`, `k_j`, `R_n`, OCV, `\xi_eq`, `h_n` |
| Heat objective | 781-792 | Adds temperature loss and regularization |
| Chapter 3 interface | 815-833 | Passes driving force, rate, progress, heat |

### Chapter 3 Candidate - Reaction Kinetics

| Object | Line Evidence | Role |
|---|---:|---|
| OCV equilibrium vs kinetic rate separation | 860-869 | Keeps `\xi_eq` OCV-based while `k_j` uses driving force |
| Driving force generalization | 873-887 | Generalizes `A_j` into `F eta_j` |
| Double-count warning | 891-894 | Avoids double-counting between `R_n` and BV terms |
| BV equation | 898-905 | Defines `i_j` from `i_0`, `eta_j`, transfer coefficient |
| Low-overpotential / asinh / Tafel | 911-961 | Adds practical inverse forms |
| Temperature-dependent `i_0` | 965-975 | Adds SOC and temperature dependence |
| Forward/backward rate | 980-1008 | Shows relaxation model is reduced form of reversible rates |
| Current partition | 1012-1019 | Links `I_j=Q_j dxi_j/dt` and total current |
| Chapter 4 interface | 1069-1099 | Passes voltage, equilibrium, driving force, barrier, rate |

### Chapter 4 Candidate - Integrated System

| Object | Line Evidence | Role |
|---|---:|---|
| Integrated state vector | 1256-1258 | State includes `q`, all `xi_j`, and `T` |
| Distribution quadrature | 1263-1268 | Practical finite grid for barrier distribution |
| Inputs | 1272-1274 | Current, ambient temperature, heat transfer |
| State equations | 1281-1317 | q, xi, distributed xi, and temperature equations |
| Observation equations | 1326-1376 | voltage, capacity, ICA, DVA, temperature derivative terms |
| Calculation procedure | 1381-1395 | Stepwise forward simulation |
| Integrated loss | 1400-1413 | Voltage, ICA, DVA, temperature, regularization |
| Fitting order | 1419-1430 | Staged parameter fitting |
| Chapter 5 interface | 1471-1497 | Passes baseline to hysteresis layer |

### Chapter 5 Candidate - Hysteresis Layer

| Object | Line Evidence | Role |
|---|---:|---|
| Branch signs | 1542-1568 | Defines branch index and separates current sign from transformation sign |
| Full branch voltage model | 1586-1597 | Adds resistance, memory, and dynamic residual terms |
| Branch progress ODE | 1608-1626 | Adds branch-indexed progress dynamics |
| Branch barrier and rate | 1644-1668 | Adds branch-indexed `Delta G_eff` and `k_j` |
| Branch forward/backward rates | 1678-1701 | Adds branch-specific reversible rates |
| Memory variable | 1708-1735 | Defines `z_j`, its ODE, and memory-voltage basis |
| Branch distribution | 1745-1760 | Branch-indexed barrier distribution dynamics |
| Branch ICA/DVA | 1772-1803 | Branch-specific capacity and derivative observations |
| Hysteresis residual and energy | 1811-1882 | Defines branch voltage difference and loop energy |
| Branch fitting objective | 1889-1919 | Simultaneous voltage/ICA/DVA/temperature branch loss |
| Identifiability risks | 1937-1952 | Lists confounded hysteresis terms |

## Notation and Structural Issues For Later Phases

| ID | Evidence | Issue | Phase To Resolve |
|---|---|---|---|
| V5-ISS-001 | 18, 25, 46 vs 525-1974 | File title/header still says `ver.1` although the file contains ver.1-ver.5 stacked material | Phase 006/007 |
| V5-ISS-002 | 62-523 vs user instruction | Historical ver.1 block is dynamic-progress based, while user identified `graphite_ica_charge_balance_ver1_rechecked2.tex` as corrected Chapter 1 restart | Phase 003 |
| V5-ISS-003 | 98, 328-335, 349-363 | `q` is normalized discharge progress while `Q_n(q)` is also a modeled capacity; derivative units and capacity-coordinate mapping need audit | Phase 003/005 |
| V5-ISS-004 | 110 and 690 | `w_j` is used as equilibrium transition width in Chapter 1 and as `Q_{j,\tot}/Q_{\cell}` in Chapter 2 | Phase 006 |
| V5-ISS-005 | 179-197, 860-869, 999-1001 | `\xi_{j,\eq}` is OCV-defined in Chapter 1/3 but also expressed as `k^+/(k^++k^-)` in forward/backward interpretation; requires consistency rule | Phase 005/006 |
| V5-ISS-006 | 130-132, 157-159, 891-894, 1244-1251 | `R_n` and Butler-Volmer/overpotential layers can double-count polarization | Phase 005/006 |
| V5-ISS-007 | 630-650, 1374-1379 | Temperature derivative of apparent voltage can mix reversible and irreversible contributions | Phase 006 |
| V5-ISS-008 | 1523-1974 | Hysteresis layer has many flexible terms (`R_n^p`, `k_j^p`, `z_j`, `rho_j^p`) with explicit identifiability risks | Phase 006/007 |

## Chapter Direction Captured From ver5

The file's intended architecture is a stack, not five separate unrelated drafts:

```text
Chapter 1 candidate:
  thermodynamic/dynamic graphite ICA-DVA base
  xi_j, xi_eq, k_j, Q_n(q), dQ/dV, dV/dQ

Chapter 2 candidate:
  heat layer using Chapter 1 dxi_j/dq as a basis

Chapter 3 candidate:
  reaction kinetics and forward/backward rate interpretation of Chapter 1 relaxation

Chapter 4 candidate:
  integrated state, observation, heat, objective, and fitting system

Chapter 5 candidate:
  hysteresis/branch/memory extension layered on Chapter 1-4
```

For the user's current project direction, Chapter 1 should not be copied from this historical ver.1 block without correction. The final Chapter 1 must be rebuilt from `graphite_ica_charge_balance_ver1_rechecked2.tex` and then fitted into this stack.
