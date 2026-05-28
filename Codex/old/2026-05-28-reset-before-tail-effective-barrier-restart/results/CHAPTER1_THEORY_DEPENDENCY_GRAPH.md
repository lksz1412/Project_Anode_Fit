# Chapter 1 Theory Dependency Graph

Project: `D:\Projects\Project_Anode_Fit`

Plan: `D:\Projects\Project_Anode_Fit\Codex\plans\2026-05-28-chapter1-theory-ralph-wiggum-loop-plan.md`

Created: 2026-05-28

## Scope

This graph fixes the logical order for the Chapter 1 theory-complete manuscript. Its purpose is to prevent circular voltage logic and to force the ICA/dQdV peak-shape explanation to follow from charge balance and phase-transition state variables.

## Reader-Level Dependency Order

| Order | Object | Depends On | Defined Before Use? | Used For |
|---:|---|---|---|---|
| 1 | analysis branch and orientation | user-chosen charge/discharge branch | required first | sign convention |
| 2 | time `t` | analysis interval | yes | current integration |
| 3 | external charge `Q_ext(t)` | current magnitude after branch orientation | yes | measured charge coordinate |
| 4 | normalized charge `q` | `Q_ext`, `Q_cell` | yes | independent coordinate |
| 5 | ICA/DVA observable definitions | `Q_ext`, measured voltage | yes | target quantities |
| 6 | transition index `j` | effective graphite phase transitions | yes | state list |
| 7 | transition progress `xi_j` | transition index and branch direction | yes | internal storage state |
| 8 | transition capacity `Q_{j,tot}` | transition `j` | yes | peak area scale |
| 9 | background storage `Q_bg(V,T)` | graphite voltage and temperature | yes | non-peak storage |
| 10 | charge-balance residual `G(V;q,T,xi)` | `Q_ext`, `Q_bg`, `xi_j`, capacities | yes | implicit voltage equation |
| 11 | internal potential `V_n` | root of `G=0` | yes | thermodynamic state coordinate |
| 12 | equilibrium progress `xi_{j,eq}(V,T)` | free-energy preference at voltage and temperature | yes, with dummy `V` before `V_n` substitution | equilibrium branch |
| 13 | equilibrium OCV `V_{n,OCV}(q,T)` | charge-balance root with `xi_j=xi_{j,eq}` | yes | special equilibrium case |
| 14 | apparent voltage `V_app` | internal potential plus observation/polarization map | yes | measured-voltage derivative |
| 15 | dynamic progress equation | `V_n`, `xi_j`, `xi_{j,eq}`, temperature-dependent relaxation | yes | tail/broadening |
| 16 | fixed-point integral form | dynamic progress equation plus implicit `V_n` | yes | self-consistency without contradiction |
| 17 | `dV_n/dq` | differentiated charge balance | yes | derivative chain |
| 18 | `dV_app/dq` | `dV_n/dq` and observation map | yes | measured derivative |
| 19 | `dQ_ext/dV_app` | reciprocal chain with `Q_ext=Q_cell q` | yes | ICA |
| 20 | `dV_app/dQ_ext` | reciprocal chain | yes | DVA |
| 21 | peak area | integral of `Q_{j,tot} d xi_j/dV` | yes | area conservation |
| 22 | peak location | maximum of transition derivative contribution | yes | phase-transition center |
| 23 | peak width/tail | equilibrium width plus relaxation length in charge coordinate | yes | low-T/high-T tail explanation |

## Forbidden Dependency Patterns

| Pattern | Why It Fails | Repair |
|---|---|---|
| using `V_n(q)` before charge balance | makes voltage an assumed input rather than a solved state | define `V_n` as root of `G=0` first |
| defining `xi_j` from OCV before `V_n` root exists | hides the self-consistent feedback | define `xi_{j,eq}(V,T)` with dummy voltage, then substitute |
| deriving ICA before `dV/dq` | skips the denominator that controls peak shape | derive charge-balance derivative first |
| treating peak area and tail shape as the same property | confuses capacity conservation with distribution in voltage | area from integral, tail from derivative distribution |
| explaining low-temperature long tail by equilibrium broadening alone | equilibrium thermal width and kinetic lag have different temperature trends | separate equilibrium width from relaxation length |
| invoking solver/fitting implementation as proof | outside current task | keep proof at equation/logic level |

## Central Logical Chain

```text
Q_ext(t)
  -> q(t)
  -> internal states xi_j(q)
  -> charge-balance residual G(V;q,T,xi)
  -> root V_n(q)
  -> equilibrium target xi_eq(V_n,T)
  -> dynamic lag dxi_j/dq
  -> differentiated charge balance dV_n/dq
  -> measured derivative dV_app/dq
  -> ICA dQ_ext/dV_app
  -> peak area / location / width / tail interpretation
```

## Temperature-Tail Logic

| Quantity | Meaning | Low-Temperature Effect | High-Temperature Effect |
|---|---|---|---|
| equilibrium transition width | thermodynamic spread of the equilibrium occupancy curve | often sharper for simple `RT`-scaled occupancy | often broader for simple `RT`-scaled occupancy |
| relaxation rate `k_j(V,T)` | speed at which `xi_j` approaches `xi_{j,eq}` | smaller under activated relaxation | larger under activated relaxation |
| charge-coordinate relaxation length `ell_j=|I|/(Q_cell k_j)` | charge span over which lag decays | larger, so tail persists longer | smaller, so tail decays sooner |
| integrated transition capacity `Q_{j,tot} Delta xi_j` | area carried by a completed transition after baseline separation | unchanged if the transition completes | unchanged if the transition completes |

This separation is required because the user's observed low-temperature long tail and high-temperature short tail cannot be explained cleanly by equilibrium broadening alone.
