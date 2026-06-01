# Phase 019 Chapter 2 Review - 10 Passes

## Scope

Reviewed manuscript:

- `D:\Projects\Project_Anode_Fit\Codex\results\graphite_ica_chapter2_reversible_heat_dvdt_v1.tex`

Canonical input:

- `D:\Projects\Project_Anode_Fit\Codex\results\graphite_ica_chapter1_rebuilt_v5_convention_safe_polish.tex`

Review target:

- Chapter 2 must extend Chapter 1 into reversible heat, entropy coefficient, and `dV/dT`.
- It must preserve Chapter 1 convention: `q`, `theta_j`, `Theta`, `L_q`, `A_L(lambda;T,psi)`.
- It must distinguish equilibrium entropy coefficient from finite-current apparent `dV/dT`.
- It must not import old `ver.2` equations as authority.
- It must not use a step-function barrier interpretation.

## Final Static Verification

Command:

```powershell
& 'D:\Projects\Project_Anode_Fit\Codex\work\verify_ch2_reversible_heat_dvdt_v1.ps1' `
  -TexPath 'D:\Projects\Project_Anode_Fit\Codex\results\graphite_ica_chapter2_reversible_heat_dvdt_v1.tex' |
  ConvertTo-Json -Depth 5
```

Result:

```text
Lines: 932
SHA256: 21BF4933DE5D332B9EF61BC5F10645F11254BF11811C68855496FA5A2C5B6F63
BeginCount: 61
EndCount: 61
OpenBraceCount: 740
CloseBraceCount: 740
LabelCount: 76
RefCount: 21
MissingRefs: []
CiteCount: 3
BibitemCount: 5
MissingCites: []
Xelatex: NOT_FOUND
```

Forbidden/risky pattern counts:

```text
xi_symbol: 0
Codex: 0
audit_lower: 0
Ralph: 0
solver: 0
fallback: 0
korean_regression: 0
zero_to_one_ascii: 0
step_function: 0
Vapp_entropy_direct: 0
```

Required concept counts:

```text
h_eq_definition: 29
h_dyn_definition: 5
h_app_definition: 9
qrev: 8
qirr: 6
tail_spectrum: 7
charge_balance_fixed_q: 5
```

## 10-Pass Review Ledger

### Pass 1 - Convention Audit

Checked:

- `q` remains the primary coordinate.
- `theta_j`, `Theta`, `theta_eq,j`, `r_j` match Chapter 1 convention.
- `L_q` and `A_L(lambda;T,psi)` are used for tail theory.
- No conflicting transformed progress coordinate is introduced.

Findings:

- Initial staged draft contained one explicit old-coordinate symbol in a negative convention sentence.
- Initial staged draft mentioned `Chapter 1 v5` in the manuscript body, which was too close to process/version wording.

Repairs:

- Replaced the old-coordinate sentence with `No separate transformed progress coordinate is introduced`.
- Replaced `Chapter 1 v5` with `Chapter 1`.

Gate result: PASS.

### Pass 2 - Charge-Balance Algebra Audit

Checked:

- Equilibrium charge balance starts from
  `Q_cell q = Q_bg(V_eq,T)+Q_p Theta_eq(V_eq,T)`.
- Fixed-`q` differentiation uses the implicit function rule.
- Denominator is `C_bg + Q_p (partial Theta_eq / partial V)_T`.
- Numerator is `(partial Q_bg / partial T)_V + Q_p(partial Theta_eq / partial T)_V`.
- Units reduce to `V/K`.

Findings:

- Algebra is internally consistent.
- The manuscript explicitly shows `F(V,T;q)`, `F_V`, `F_T`, and substitution.

Repairs:

- None required.

Gate result: PASS.

### Pass 3 - Thermodynamic Identity and Sign Audit

Checked:

- `h_n^eq` is defined operationally as `(partial V_n,eq / partial T)_q`.
- Reversible heat uses equilibrium potential only.
- Sign convention is explicit and not hidden.

Findings:

- The first draft had the correct operational definition, but the sign bridge from free energy to heat could be more explicit for undergraduate-level traceability.

Repairs:

- Added `Delta Gbar_n = sigma_V F V_n,eq`.
- Added `Delta Sbar_n = - sigma_V F h_n^eq`.
- Added signed molar-rate bridge and the general reversible heat sign equation before reducing to `dot Q_rev,n = -I_s T h_n^eq`.

Gate result: PASS.

### Pass 4 - Apparent vs Equilibrium Audit

Checked:

- `V_n,app` is separated into internal potential plus polarization.
- Apparent derivative `h_n^app` is not equated with entropy coefficient.
- Dynamic derivative `h_n^dyn` is defined before apparent polarization is added.

Findings:

- The separation is explicit in equations and warnings.
- Static pattern check found no direct `V_n,app` to entropy-coefficient misuse.

Repairs:

- None after earlier wording cleanup.

Gate result: PASS.

### Pass 5 - Reversible vs Irreversible Heat Audit

Checked:

- `dot Q_rev,n` is tied to `h_n^eq`.
- `dot Q_irr,n` is tied to overpotential/polarization or reduced `|I|^2 R_n`.
- Dynamic lag is not double counted as both reversible heat and irreversible heat.

Findings:

- Manuscript states the conservative boundary:
  reversible heat uses `h_n^eq`;
  ohmic/overpotential losses enter `dot Q_irr,n`;
  kinetic-lag tail terms remain apparent/dynamic until Chapter 3 derives a kinetic heat law.

Repairs:

- None required.

Gate result: PASS.

### Pass 6 - Tail-Kernel Thermal-Response Audit

Checked:

- Chapter 1 tail kernel is used as a dynamic inventory response, not as reversible heat.
- Temperature dependence in `lambda`-space and `G`-space is not conflated.
- Peak-anchor shifts are handled.

Findings:

- Initial draft gave the clean `lambda`-space temperature derivative but did not state the condition that the derivative is peak-aligned.
- At fixed absolute `q`, a temperature-dependent peak anchor `q_a(T,psi)` creates an additional chain-rule term.

Repairs:

- Added peak-aligned coordinate `s=q-q_a`.
- Added the fixed-absolute-`q` derivative with the extra `A_L lambda^{-2} (partial q_a / partial T)_psi` term.
- Added measurement instruction: state whether tails are compared in absolute `q` or after peak alignment.

Gate result: PASS.

### Pass 7 - Physical Assumption and Literature Audit

Checked:

- Assumptions are explicit.
- Reversible/irreversible heat split is literature-grounded.
- DOI/source details for heat references are not invented.

Findings:

- Bernardi, Pawlikowski, and Newman DOI verified as `10.1149/1.2113792`.
- Thomas and Newman DOI verified as `10.1149/1.1531194`.
- Manuscript cites energy-balance and porous insertion electrode thermal modeling references.

Repairs:

- None required after citation insertion.

Gate result: PASS.

### Pass 8 - Undergraduate-Followability Audit

Checked:

- Hidden derivative steps are expanded.
- Symbols are defined before use.
- Main result follows from visible equations.

Findings:

- The `h_n^eq` derivation is shown through `F(V,T;q)=0`, chain rule, `F_V`, `F_T`, and units.
- Sign convention now has a visible free-energy and entropy bridge.

Repairs:

- Covered by Pass 3 repair.

Gate result: PASS.

### Pass 9 - Chapter Handoff Audit

Checked:

- Chapter 2 stays inside heat and `dV/dT` extension.
- Chapter 3/4/5 are only handoff targets, not prematurely solved.

Findings:

- Handoff equations are limited to `h_n^eq`, `dot Q_rev,n`, and `h_n^app`.
- Later chapter descriptions are short and scoped.

Repairs:

- None required.

Gate result: PASS.

### Pass 10 - Manuscript Hygiene and Process-Label Audit

Checked:

- No process labels in LaTeX body.
- No `Codex`, review labels, `Ralph`, `solver`, `fallback`, old-coordinate symbol, or ASCII step-function pattern.
- LaTeX braces, environments, refs, and cites are internally balanced.

Findings:

- Final static check passed.
- The manuscript contains one negative conceptual statement that a barrier is not a sudden `0\to1` threshold; this is intentional physical clarification, not a step-function model.

Repairs:

- None after final static check.

Gate result: PASS.

## Remaining Limitations

- PDF build was not run because `xelatex` is `NOT_FOUND` in the current environment.
- This phase did not perform a new external audit of the user's older Refs 6/7 because Chapter 2 does not promote the Fredholm/Plan A closure.
- The manuscript is a theory foundation. It intentionally does not implement fitting or a solver.

## Verdict

Chapter 2 v1 passes the requested 10-pass logic review under the current Chapter 1 convention. The main repairs made during review were:

- remove old-coordinate/process-version contamination;
- strengthen the thermodynamic sign derivation;
- add the missing peak-anchor term for tail-kernel temperature derivatives.

