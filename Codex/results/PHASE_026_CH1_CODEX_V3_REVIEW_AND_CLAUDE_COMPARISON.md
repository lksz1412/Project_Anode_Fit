# PHASE 026 - Chapter 1 Codex v3 Review and Claude Final Comparison

## Scope

- Codex candidate: `D:\Projects\Project_Anode_Fit\Codex\results\graphite_ica_ch1_codex_candidate_v3.tex`
- Claude final candidate: `D:\Projects\Project_Anode_Fit\Claude\docs\graphite_ica_ch1_rebuilt.tex`
- Claude handover checked: `D:\Projects\Project_Anode_Fit\Claude\results\HANDOVER_RB_2026-06-02.md`
- Claude rework ledger checked: `D:\Projects\Project_Anode_Fit\Claude\results\RB_LEDGER_CH1_REWORK.md`

## Read Coverage

- Codex v3 was read from line 1 through line 621.
- Claude ch1 rebuilt was read from line 1 through line 923.
- Review basis: full line-range read, static label/ref/cite check, targeted risk-pattern search, and XeLaTeX build check.

## Mechanical Verification

### Codex v3

- Lines: 621
- SHA256: `18713FC7A0AC8988CB5F8A60AF67D2060823438930603AD15858DDA8AFF2994A`
- Labels: 52
- Duplicate labels: none
- Missing refs: none
- Missing cites: none
- XeLaTeX: builds after 2 passes
- PDF: `C:\Users\lksz1\OneDrive\문서\New project\_texcheck_codex_ch1\codex_ch1.pdf`
- Log residuals: LaTeX Error 0, undefined reference/citation 0, overfull hbox 3, missing character 0.

### Claude ch1 rebuilt

- Lines: 923
- SHA256: `7D4AEFDFD54EB96B20605DAD9D17FB7103FC7C580...`
- Labels: 47
- Duplicate labels: none
- Missing refs: none
- Missing cites: none
- XeLaTeX: builds after 2 passes
- PDF: `C:\Users\lksz1\OneDrive\문서\New project\_texcheck_claude_ch1\claude_ch1.pdf`
- Log residuals: LaTeX Error 0, undefined reference/citation 0, overfull hbox 4, missing character 1, hyperref PDF-string token warnings 13.

## 1. Codex v3 Content Review

### Confirmed Strengths

1. The core phenomenon is correctly centered in the introduction: low-temperature long ICA tail, equilibrium thermal width insufficiency, kinetic lag, and electrode-potential-assisted effective relaxation barrier.
2. The branch convention is safer than Claude's current text. Codex explicitly separates crystallographic stage number from measured discharge/delithiation branch-local peak label.
3. The `chi_j` convention is safer. Codex defines `chi_j` as Level-A scalar relaxation-barrier sensitivity and explicitly does not identify it with Butler--Volmer transfer coefficient `beta_j` in Chapter 1.
4. The barrier-to-length mapping is physically coherent: `L = |I|/(Q_cell k_j)` and `L(G)=|I|/(Q_cell k_0) exp[(G-chi A)/(RT)]` correctly gives longer tails at lower T when the effective barrier remains positive.
5. Codex avoids a visible Heaviside/step-function expression and uses a domain lower bound `L >= L_min` instead. This is cleaner for the user's concern about artificial switch-like logic.
6. The measured ICA relation is correctly bounded: exponential progress derivative does not automatically make measured ICA exactly exponential; the exponential fitting formula is restricted to small-tail/local-baseline approximation.

### Defects / Insufficient Parts

#### C1 - Plan A introduces variables without enough definition

- Location: Codex lines 449-465.
- Issue: `a(q)`, `c(q)`, and `Theta_init(q)` appear in the closure expression, but Codex does not give the same clear definitions Claude gives.
- Why it matters: This violates the user's criterion that no new variable may appear without physical meaning. In particular, `a(q)` is not explicitly defined as the Taylor intercept around `Theta^(0)`.
- Repair direction: Import Claude's explicit baseline definition: `Theta^(0)` first, then `a(q') = Theta_eq(V_n(Theta^(0)(q'))) - b(q')Theta^(0)(q')`, then `c(q)=Theta_init+int K a`.

#### C2 - Plan B is too thin to function as a reference method

- Location: Codex lines 438-441 and 581-589.
- Issue: It says to use a barrier grid and solve charge conservation, but lacks quadrature normalization, grid convergence criterion, and relative Plan A/Plan B validation formula.
- Why it matters: The document claims self-consistency can be checked, but does not provide enough information for a reader to reproduce the check.
- Repair direction: Absorb Claude's normalized grid expression, `sum_m w_m rho_G(g_m)=1`, relative error criterion, and discretization/noise tolerance chain.

#### C3 - Simple fitting protocol is conceptually right but not self-contained enough

- Location: Codex lines 497-545.
- Issue: Codex has the baseline-subtracted `Y_tail` and the single-mode formula, but lacks the stronger non-circular extraction sequence in Claude: first fix stage/OCV and `R_n`, then fix `q_a`, fit `L`, derive `chi_j`, then use corrected Eyring variable for enthalpy.
- Why it matters: The user wants Chapter 1 alone to yield a usable approximation. Codex v3 gives a formula but not yet a robust enough working recipe.
- Repair direction: Add Claude's stepwise fitting section, but remove or soften problematic claims noted below.

#### C4 - Eyring temperature correction is underdeveloped

- Location: Codex lines 537-538.
- Issue: Codex notes that prefactor variation must be corrected or negligible, but does not provide the corrected regression variable.
- Why it matters: A reader can still mistakenly use `ln(1/L)` vs `1/T` directly and overinterpret the slope.
- Repair direction: Add the corrected Eyring-style form from Claude, e.g. `ln(1/(L T)) + chi_j A_j(T)/(RT)` vs `1/T`, with the caveat that `kappa(T)` and entropy assumptions remain bounded.

#### C5 - Transport / charge-transfer degeneracy is insufficiently separated

- Location: Codex lines 572-579.
- Issue: Codex mentions covariance between `R_n` and `chi_j`, but does not fully separate diffusion-limited tails, charge-transfer polarization, and barrier-spectrum attribution.
- Why it matters: Without this, the document can overclaim that observed tail behavior is specifically due to relaxation-barrier lowering.
- Repair direction: Absorb Claude's N5 discriminator: GITT transient shape, current-interrupt/R_ct separation, and the rule that barrier-spectrum attribution is forbidden without independent separation.

## 2. Claude Final Comparison

### Claude Strengths Worth Absorbing

1. Claude is much stronger in followability. It expands the logistic derivation, single-mode ODE, residual-to-derivative bridge, Volterra derivation, Plan A closure, and fitting sequence with fewer skipped steps.
2. Claude's Plan B and Plan A sections are more usable. It gives the quadrature normalization, relative Plan A/B error, and explicit `Theta^(0)` baseline logic.
3. Claude has a better practical fitting section. The `q_a` fixation, nuisance amplitude, `V_app -> V_n` correction, Eyring prefactor correction, and non-circular `chi_j`/enthalpy sequence are valuable.
4. Claude's falsification section is stronger. The N5 transport/charge-transfer degeneracy warning is important and should be retained.
5. Claude includes the 0.2C anchor relation, which is useful for this project context if the user's real data use a low-rate reference curve.

### Claude Defects / Risks

#### K1 - `chi_j` convention conflict

- Location: Claude line 123, and lines 319-352.
- Issue: The notation table says `chi_j` is the same object as Chapter 3 transfer coefficient `beta_j`, while the later keybox says Chapter 1 uses common-mode mobility acceleration and directional forward/backward splitting belongs to Chapter 3.
- Why it matters: This is a real convention conflict. `chi_j` should not be declared identical to `beta_j` in Chapter 1. At most it may become mappable to a directional coefficient under an additional Level-B kinetic model.
- Repair direction: Use Codex's safer wording: `chi_j` is not `beta_j` by definition in Chapter 1; Chapter 3 may introduce a mapping only after directional kinetics are defined.

#### K2 - Single-mode amplitude inconsistency

- Location: Claude lines 523-536 and 733-742.
- Issue: Claude's kernel absorbs residual amplitude into `A_L`, but then calls the single-mode limit `A_L=delta(L-L*)` or `delta(L-L0)` without carrying an amplitude. Later the simple-fit section reintroduces `Theta_0` separately.
- Why it matters: If `A_L` is an amplitude spectrum, the strict single-mode limit should be `A_L(L)=Theta_0 delta(L-L*)` or the text must explicitly say `Theta_0` has been factored out separately.
- Repair direction: Use Codex's explicit amplitude-bearing delta form.

#### K3 - Heaviside support expression is mathematically acceptable but presentation-risky

- Location: Claude lines 482-500.
- Issue: Claude writes `H(L-L_min)`. This is not a kinetic step function; it is only a support indicator from `G>=0`. However, the user has already objected to switch-like barrier handling, so this notation is likely to trigger misreading.
- Repair direction: Prefer Codex's lower-limit formulation `int_{L_min}^infty` and explain that this is a domain condition, not a physical switching law.

#### K4 - Paper-facing metadata remains in Claude TeX

- Location: Claude lines 2-13 and 54-55.
- Issue: Process metadata, author/date, RB plan text remain in the article body/preamble.
- Why it matters: Project rules say change history and process metadata belong in results/ledger, not in the scientific document body.
- Repair direction: Remove before adopting as Codex final.

#### K5 - Bibliography is less publication-ready than Codex's

- Location: Claude lines 911-916 and 894-895.
- Issue: The user's JCP paper and refs 6/7 are partially placeholder-like; one reference title is abbreviated with ellipsis.
- Why it matters: The user asked for paper/patent-grade logic. Bibliography should not contain placeholders.
- Repair direction: Use Codex's corrected full bibliographic entries for `jcp2017`, `lee2011`, and `son2013`, and complete the Ohzuku title.

#### K6 - C-rate conclusion should be more cautious

- Location: Claude lines 775-784 and 801-803.
- Issue: Claude says the simplefit plus 0.2C anchor explains higher C-rate as shorter tail and worse peak overlap. The relation is not universally one-directional because `L=|I|/(Q_cell k)` has a current prefactor that increases `L` if `k` is fixed, while potential assistance can reduce `L` by increasing `k`.
- Repair direction: Keep Claude's 0.2C anchor, but use Codex's competition wording: current prefactor, potential-assisted rate increase, and apparent-axis polarization compete.

## 3. Comparative Verdict

- Codex v3 is safer in convention and avoids the most dangerous logical overclaims, but it is too compressed for the user's target. It is not yet a complete paper-grade Chapter 1 because Plan A/B, fitting workflow, Eyring correction, and degeneracy/falsification are underdeveloped.
- Claude final is closer to the desired textbook-level explanatory density and practical self-contained fitting deliverable, but it contains convention conflicts and a few presentation/notation risks that should not be copied blindly.
- Best path: rebuild the next Codex version from Codex's safer convention spine plus Claude's detailed explanatory scaffolding. Do not directly adopt Claude text wholesale.

## 4. Recommended Rebuild Direction

1. Keep Codex's core conventions:
   - `j` as branch-local peak label.
   - `chi_j` as Level-A scalar relaxation-barrier sensitivity, not `beta_j`.
   - lower-limit support instead of visible Heaviside support factor.
   - exact ICA relation plus small-tail fitting limitation.
2. Absorb Claude's strengths:
   - stepwise undergrad derivations,
   - `Theta^(0)`, `a(q)`, `b(q)`, `c(q)` definitions,
   - Plan B normalization and Plan A/B validation,
   - simple fitting sequence including `q_a`, nuisance amplitude, Eyring correction, and `V_app -> V_n`,
   - N5 degeneracy/falsification block,
   - optional 0.2C anchor.
3. Correct Claude before absorption:
   - remove `chi_j = beta_j` identity,
   - fix single-mode amplitude as `Theta_0 delta(L-L*)`,
   - replace `H(L-L_min)` presentation with integration-domain language,
   - remove process metadata,
   - replace placeholder bibliography.

## 5. Gate Result

- Codex v3: mechanically buildable and logically safer, but G-follow/G-usable gate is PARTIAL, not final PASS.
- Claude final: mechanically buildable and more complete for G-follow/G-usable, but convention gate FAIL until `chi_j` and amplitude-spectrum issues are repaired.
- Final Chapter 1 should be a merged/rebuilt v4, not either file as-is.
