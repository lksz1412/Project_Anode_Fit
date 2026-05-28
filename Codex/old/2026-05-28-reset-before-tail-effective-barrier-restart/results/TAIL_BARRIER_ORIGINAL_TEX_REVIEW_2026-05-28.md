# Tail Effective Barrier Original TeX Review

Project: `D:\Projects\Project_Anode_Fit`

Date: 2026-05-28

Request basis: user clarified that the present target is not peak area, fitting code, or solver construction. The target is the theoretical logic for why graphite LIB ICA peak tails become longer at low temperature and shorter at higher temperature, with an additional electrode-potential-dependent barrier lowering effect beyond the thermal barrier.

## Scope

Reviewed source files:

| File | Role | Coverage status |
|---|---|---|
| `D:\Projects\Project_BatteryData_Display_임시저장소\새 폴더\drive-download-20260527T100231Z-3-001\graphite_ica_dynamic_ver5.tex` | historical ver1-ver5 stacked source; should be reinterpreted as chapter structure | prior full read map existed; this pass re-read targeted tail/barrier/voltage-state ranges |
| `D:\Projects\Project_BatteryData_Display_임시저장소\새 폴더\drive-download-20260527T100231Z-3-001\graphite_ica_charge_balance_ver1_rechecked2.tex` | corrected Chapter 1 foundation for charge balance and internal potential | targeted re-read of charge balance, voltage roles, effective barrier, dynamics, ICA/DVA ranges |

This pass does not claim a new full line-by-line reread of both files. It is a focused re-review against the corrected user scope: tail shape, temperature dependence, present electrode potential, effective barrier, and logical self-consistency.

## Corrected Direction

The correct manuscript direction is:

> Build Chapter 1 from first principles as a tail-shape theory for graphite ICA, where the observed ICA tail is controlled by finite phase-transition relaxation and an effective kinetic barrier
> \[
> \Delta G_{\mathrm{eff},j}^{+}(q,T,I)
> \]
> that combines intrinsic thermal activation and present electrode-potential-assisted barrier lowering.

The central question is not why the total phase-transition capacity or peak area is fixed. Peak area belongs to later fitting and capacity partitioning. The present theoretical chapter should explain the tail length/asymmetry:

\[
\text{low }T \Rightarrow \text{larger effective kinetic resistance} \Rightarrow \text{long tail}
\]

\[
\text{high }T \Rightarrow \text{faster relaxation} \Rightarrow \text{shorter tail}
\]

\[
\text{stronger forward driving potential} \Rightarrow \Delta G_{\mathrm{eff}}^{+}\downarrow \Rightarrow k_j\uparrow \Rightarrow \text{shorter tail}
\]

## Evidence From `graphite_ica_dynamic_ver5.tex`

| Lines | Finding | Use in rebuilt direction |
|---|---|---|
| 55-63 | The file already defines the purpose as explaining graphite phase-transition peaks and peak-tail behavior through phase-progress kinetics. | Salvage as the high-level thesis, but rewrite as Chapter 1 rather than historical ver1. |
| 65-79 | Main spine is `Delta G_eff -> k_j -> dxi/dt -> xi(q) -> dxi/dq -> dQ/dV, dV/dQ`. | Salvage as the backbone. This is exactly the direction needed after the user correction. |
| 176-201 | Equilibrium progress is defined from `V_{n,OCV}`; equilibrium logistic/erf peaks are separated from finite-rate actual peaks. The text explicitly says low rate/high T gives `xi≈xi_eq`, while finite C-rate/low T gives lag and tail. | Salvage, but make the Gaussian/erf peak only the equilibrium reference, not the final explanation of the observed tail. |
| 203-245 | Defines intrinsic activation free energy, potential-assisted affinity, effective barrier, and bounded rate: `Delta G_a=Delta H_a-T Delta S_a`, `A=s_phi F(V_app-U_j)`, `Delta G_eff=Delta G_a-chi A`, `k=nu exp[-Delta G_eff^+/(RT)]`. | Salvage core equations. Replace `V_app` by the more careful `V_drive` role from the rechecked ver1 where needed. |
| 252-284 | Defines relaxation dynamics and charge-coordinate conversion: `dxi/dq=(Q_cell/|I|) k (xi_eq-xi)`. It explicitly says C-rate enters through both residence time and `k` via voltage/affinity. | Salvage. This is the tail-length derivation entry point. |
| 286-323 | Barrier distribution makes long tails through slow high-barrier domains; high T can shorten tail through `RT` and `nu(T)`. | Salvage as optional extension after the single-barrier tail length is derived. Do not make the distribution the first principle. |
| 857-869 | ver3 states the crucial separation: equilibrium location is determined by OCV/quasi-equilibrium voltage, while the rate constant is determined by overpotential/driving force. | Salvage as a hard logical rule. This prevents double-counting and fixes a major confusion risk. |
| 871-894 | Generalizes affinity to `F eta_j` and warns not to double-count charge-transfer effects in both `R_n` and Butler-Volmer. | Salvage as a warning/extension. Keep reduced model first. |
| 963-1008 | Introduces temperature-dependent `i0`, `nu(T)`, and forward/backward rates, and notes identifiability issues. | Use only as later extension. Do not burden Chapter 1 tail derivation with full BV unless needed. |
| 1207-1242 | Restates `A`, `Delta G_eff`, positive barrier, and rate in integrated model. | Confirms the structure is stable across historical versions. |
| 1642-1674 | Branch-specific effective barrier and double-count warning. | Reserve for later hysteresis/branch chapter. Not needed in the first tail derivation except as a future extension. |
| 1844-1863 | Tail length `lambda_j^p` is treated as an empirical comparison quantity, not a main model parameter. | Useful warning: the rebuilt Chapter 1 should derive a theoretical tail scale rather than introduce arbitrary empirical tail parameters first. |

## Evidence From `graphite_ica_charge_balance_ver1_rechecked2.tex`

| Lines | Finding | Use in rebuilt direction |
|---|---|---|
| 48-65 | The corrected ver1 defines the core flow as `Q_ext -> charge balance -> V_n -> V_app -> dQ/dV`, and explicitly rejects threshold-cut barrier completion. | This must be the true Chapter 1 foundation. It fixes the self-consistent voltage problem. |
| 118-129 | Charge balance is `Q_cell q = Q_bg(V_n,T)+sum Q_j,tot xi_j`; `V_n` is not externally prescribed but solved from charge balance. `Q_bg` is residual chemical capacitance, not a plotting baseline. | Essential. This prevents the earlier logical error where voltage and state fed each other without a root definition. |
| 148-162 | Equilibrium OCV is the charge-balance root when `xi_j=xi_eq(V_n,T)`. | Salvage. `V_OCV` should be a derived equilibrium branch, not a magic input. |
| 203-238 | Separates `V_n`, `V_{n,app}`, and `V_{n,drive}`; defines `V_app=V_n+s_I |I| R_n`; warns that `V_drive≈V_app` is a reduced approximation and `R_n`/`k_j` must not explain the same effect freely. | This is the main correction to ver5. The rebuilt theory must use `V_drive` in the kinetic barrier, not casually merge all voltage roles. |
| 240-266 | Defines `Delta G_a(T)`, `Delta G_eff=Delta G_a-chi A`, softplus positive barrier, and final `k=nu exp[-Delta G_eff^+/(RT)]`. | Core of the user-requested effective barrier logic. |
| 268-286 | Defines `dxi/dt` and `dxi/dq` with `xi_eq(V_n,T)-xi`. | Required bridge from barrier to observed tail. |
| 320-350 | Defines kinetic barrier distribution over `g>=0`; warns not to confuse kinetic barrier distribution with equilibrium transition-center distribution. | Use only after the single-barrier derivation, to explain stretched/non-single-exponential tails. |
| 353-412 | Derives `dV_n/dq`, `dV_app/dq`, ICA, and DVA from charge balance. | Required to connect `dxi/dq` to observed `dQ/dV` without hand-waving. |
| 414-418 | C-rate effect is a competition: larger current reduces residence time, but changes `V_drive`/`A_j` and may increase `k_j`; thus `dxi/dq proportional k_j(I)/|I|`. | Must be stated explicitly. Tail length cannot be explained by temperature alone. |
| 437-456 | Empirical peak functions are only initial/comparison models; tail comes from `k_j`, `rho(g)`, `R_n`, and charge balance. `R_n` and `k_j` must not be freely fit together. | Confirms that the current output should be theoretical derivation, not EMG/empirical fitting. |
| 480-491 | Internal checklist confirms voltage separation, barrier distribution support, regularization, and ICA/DVA definitions. | Useful as a validation checklist for the rebuilt manuscript. |

## What Was Right

1. The original ver5 did contain the correct high-level kinetic spine: effective barrier controls rate, rate controls phase-progress lag, and lag controls ICA/DVA tail.
2. The corrected ver1 solved the strongest structural problem: `V_n` is determined by charge balance rather than assumed as an independent external coordinate.
3. The three-voltage distinction in corrected ver1 is the right way to express the present electrode-potential effect:
   - `V_n`: internal potential from charge balance;
   - `V_{n,app}`: measured apparent potential after polarization;
   - `V_{n,drive}`: kinetic driving voltage entering barrier lowering.
4. The effective barrier equation already matches the user direction:
   \[
   \Delta G_{\mathrm{eff},j}
   =
   \Delta G_{a,j}(T)-\chi_j\mathcal A_j.
   \]
5. The q-coordinate relaxation equation gives a direct route to tail length:
   \[
   \frac{d\xi_j}{dq}
   =
   \frac{Q_{\mathrm{cell}}}{|I|}
   k_j
   \left(\xi_{j,\mathrm{eq}}-\xi_j\right).
   \]

## What Was Wrong Or Misleading

1. Peak area was over-centered in the later Codex artifact. That is not the current theoretical core. Area may define available transition capacity later, but it should not lead the Chapter 1 argument.
2. Treating the observed peak as a Gaussian-like equilibrium peak is insufficient. Logistic/erf/Gaussian forms can describe equilibrium transition width, but they do not explain a long asymmetric tail under finite relaxation.
3. If `V_app`, `V_drive`, and `V_OCV` are merged too casually, the theory double-counts polarization or makes the feedback loop implicit without a root condition.
4. If `R_n` and `k_j` are both freely allowed to explain the same broadening/tail, the model loses logical identifiability.
5. The barrier distribution must not be used as a threshold rule where all domains below a barrier react immediately. The source files correctly reject that. Each barrier group must relax dynamically.

## Rebuilt Logic Spine

The rebuilt Chapter 1 should follow this order.

### 1. Charge Coordinate And Internal Potential

\[
Q_{\mathrm{ext}}(t)=\int_0^t |I(s)|\,ds,
\qquad
q=\frac{Q_{\mathrm{ext}}}{Q_{\mathrm{cell}}}.
\]

\[
Q_{\mathrm{cell}}q
=
Q_{\mathrm{bg}}(V_n,T)
+
\sum_j Q_{j,\mathrm{tot}}\xi_j.
\]

For given `q`, `T`, and `xi_j`, this equation determines `V_n`. This closes the feedback loop.

### 2. Equilibrium Transition Reference

\[
\xi_{j,\mathrm{eq}}
=
\xi_{j,\mathrm{eq}}(V_n,T).
\]

The equilibrium peak width from logistic/erf/Gaussian-like forms is only the quasi-equilibrium reference. It is not the finite-rate tail mechanism.

### 3. Present-Potential Driving Force

\[
V_{n,\mathrm{app}}
=
V_n+s_I |I| R_n(q,T,|I|).
\]

\[
\mathcal A_j
=
s_{\phi,j}F\left[V_{n,\mathrm{drive}}-U_j(T)\right].
\]

In the simplest reduced model:

\[
V_{n,\mathrm{drive}}\approx V_{n,\mathrm{app}}.
\]

This approximation must be accompanied by the rule that `R_n` and `k_j` are not simultaneously free to explain the same tail/broadening.

### 4. Effective Barrier

\[
\Delta G_{a,j}(T)
=
\Delta H_{a,j}-T\Delta S_{a,j}.
\]

\[
\Delta G_{\mathrm{eff},j}
=
\Delta G_{a,j}(T)-\chi_j\mathcal A_j.
\]

Use a bounded positive effective barrier such as:

\[
\Delta G_{\mathrm{eff},j}^{+}
=
\epsilon_G
\ln\left[
1+\exp\left(\frac{\Delta G_{\mathrm{eff},j}}{\epsilon_G}\right)
\right].
\]

\[
k_j
=
\nu_j(T)
\exp\left[
-\frac{\Delta G_{\mathrm{eff},j}^{+}}{RT}
\right].
\]

This is the mathematical expression of the user hypothesis: temperature sets the thermal activation scale, while the present electrode-potential state lowers the remaining barrier.

### 5. Tail Scale

The finite-rate state equation is:

\[
\frac{d\xi_j}{dq}
=
\frac{Q_{\mathrm{cell}}}{|I|}
k_j(q,T,I)
\left[
\xi_{j,\mathrm{eq}}(V_n,T)-\xi_j
\right].
\]

In a local tail region where `xi_eq` has mostly moved ahead and the remaining unrelaxed fraction is

\[
u_j=\xi_{j,\mathrm{eq}}-\xi_j,
\]

the local decay scale is controlled by

\[
\kappa_j(q,T,I)
=
\frac{Q_{\mathrm{cell}}}{|I|}k_j(q,T,I),
\qquad
\ell_{q,j}
=
\frac{1}{\kappa_j}
=
\frac{|I|}{Q_{\mathrm{cell}}k_j}.
\]

Substituting the effective barrier:

\[
\boxed{
\ell_{q,j}
=
\frac{|I|}{Q_{\mathrm{cell}}\nu_j(T)}
\exp\left[
\frac{\Delta G_{\mathrm{eff},j}^{+}(q,T,I)}{RT}
\right]
}
\]

This is the most important rebuilt expression.

### 6. Interpretation Of The Observed Tail

- Low temperature increases the exponential barrier penalty and often lowers the prefactor `nu_j(T)`, so `ell_q` grows and the ICA tail becomes long.
- Higher temperature reduces the barrier penalty and often increases `nu_j(T)`, so `ell_q` shrinks and the tail ends sooner.
- Stronger forward driving potential increases `A_j`, lowers `Delta G_eff^+`, increases `k_j`, and shortens the tail.
- If current is increased, two effects compete: residence time per `dq` decreases through `Q_cell/|I|`, but driving potential may increase `k_j`. The sign of tail change depends on `k_j(I,V_drive)/|I|`.
- The ICA tail is not a fitted area argument. It is the image of `d xi_j/dq` under the voltage mapping:
  \[
  \frac{dQ_{\mathrm{ext}}}{dV_{n,\mathrm{app}}}
  =
  \frac{Q_{\mathrm{cell}}}{dV_{n,\mathrm{app}}/dq},
  \]
  with `dV_app/dq` affected by charge balance and `d xi_j/dq`.

## Recommended Manuscript Rebuild

Do not patch the existing broad Chapter 1 artifact into final form. Treat it only as a scaffold/reference.

Recommended new target file:

`D:\Projects\Project_Anode_Fit\Codex\results\graphite_ica_tail_effective_barrier_theory.tex`

Suggested Chapter 1 structure:

1. Problem statement: observed graphite ICA tail changes with temperature and present potential state.
2. Why equilibrium Gaussian/logistic peak alone is insufficient.
3. Charge balance and internal potential root.
4. Three voltage roles: internal, apparent, driving.
5. Intrinsic thermal barrier.
6. Electrode-potential-assisted effective barrier.
7. Relaxation equation in time and charge coordinates.
8. Tail decay and tail-length derivation.
9. Barrier distribution as optional extension for stretched tails.
10. ICA/DVA connection through charge-balance derivatives.
11. Logical guardrails: no double-counting, no threshold barrier completion, no peak-area-centered argument, no fitting-code requirement.

## Current Artifact Classification

| Artifact | Status under corrected direction |
|---|---|
| `graphite_ica_chapter1_theory_complete.tex` | Reference only. It contains useful charge-balance and relaxation pieces, but it over-centers peak area and is not accepted as the current Chapter 1 completion. |
| `TAIL_BARRIER_SCOPE_REVIEW_2026-05-28.md` | Directionally correct but should be considered preliminary because it was written before this focused original-source re-review. |
| `TAIL_BARRIER_DEPENDENCY_CONTRACT.md` | Mostly correct. The present review confirms its dependency spine and strengthens its source-line grounding. |
| older `REBUILD_V2_*` plan/result chain | Superseded for the current tail-effective-barrier task except as historical context. |

## Gate Result

Gate: Does the original tex material support the newly clarified direction?

Result: PASS with corrections.

Reason:

- ver5 supports the effective-barrier-to-tail kinetic spine.
- corrected ver1 supplies the missing self-consistent charge-balance foundation and voltage-role separation.
- the rebuilt manuscript should now be authored from scratch around tail length and effective barrier, not by modifying the broad prior artifact.

Remaining non-goals:

- no solver implementation;
- no fitting code;
- no peak area fitting theory as the central argument;
- no PDF/ref6/ref7 method import in this specific review pass.

