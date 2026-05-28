# Rebuild v2 Phase 006 Chapter 1 Math Result

Project: `D:\Projects\Project_Anode_Fit`

Plan: `D:\Projects\Project_Anode_Fit\Codex\plans\2026-05-27-graphite-ica-from-scratch-rebuild-plan-v2-canonical.md`

Phase: `Phase 006 - Chapter 1 Mathematical Foundation Package`

Date: 2026-05-27

Gate: `PASS_REBUILD_V2_CHAPTER1_MATH`

## Scope

Phase 006 created the mathematical foundation package for Chapter 1. This phase did not create the final LaTeX manuscript. It converted the Phase 002-005 evidence, inventory, architecture, notation, and DAG contracts into a Chapter 1-ready mathematical package.

## Step Execution

| Step | Planned Action | Status | Evidence |
|---:|---|---|---|
| 161 | Create `REBUILD_V2_CHAPTER1_MATH_PACKAGE.md`. | DONE | File created. |
| 162 | Write Chapter 1 problem statement in manuscript-ready prose. | DONE | Package section `Chapter 1 Problem Statement`. |
| 163 | State why OCV-input-only formulation is insufficient. | DONE | Package section `Why An OCV-Input-Only Formulation Is Insufficient`. |
| 164 | Define measured charge coordinate. | DONE | Equations C1.1-C1.3. |
| 165 | Define analysis interval and endpoint convention. | DONE | Analysis interval section and total capacity consistency. |
| 166 | Define transition state variables. | DONE | Equations C1.4-C1.5. |
| 167 | Define equilibrium occupancy functions. | DONE | Equation C1.6. |
| 168 | Define charge-balance residual. | DONE | Equations C1.8-C1.9. |
| 169 | Define root existence interval. | DONE | Equation C1.10. |
| 170 | Define slope floor. | DONE | Equation C1.11. |
| 171 | Define uniqueness or branch-selection rule. | DONE | Branch-selection paragraph. |
| 172 | Define internal potential root. | DONE | Equations C1.12-C1.13. |
| 173 | Define equilibrium OCV special case. | DONE | Equations C1.14-C1.15. |
| 174 | Define total capacity consistency. | DONE | Equation C1.16. |
| 175 | Define apparent voltage. | DONE | Equation C1.17. |
| 176 | Define driving voltage. | DONE | Equation C1.18. |
| 177 | Define kinetic interface without full Chapter 3. | DONE | Equations C1.19-C1.20 and boundary wording. |
| 178 | Define time-domain state equation. | DONE | Equation C1.21. |
| 179 | Define q-domain state equation. | DONE | Equation C1.22 with `I_abs>0` condition. |
| 180 | Define Volterra integral form. | DONE | Equation C1.23. |
| 181 | State exact self-consistency loop. | DONE | Equation C1.24 and explanatory paragraph. |
| 182 | Define rest relaxation at fixed q. | DONE | Equations C1.25-C1.26. |
| 183 | Define derivative of charge balance in general thermal case. | DONE | Equation C1.27. |
| 184 | Define isothermal simplification. | DONE | Equation C1.28. |
| 185 | Define apparent voltage derivative. | DONE | Equation C1.29. |
| 186 | Define ICA. | DONE | Equation C1.30. |
| 187 | Define DVA. | DONE | Equation C1.31. |
| 188 | Define monotonicity condition. | DONE | Equation C1.32. |
| 189 | Define denominator-singularity warning. | DONE | Warning section added. |
| 190 | Define validation residuals for Chapter 1. | DONE | Equation C1.33 and validation checks. |
| 191 | Explain `Q_bg` as storage. | DONE | Dedicated section added. |
| 192 | Explain why `V_OCV` is derived. | DONE | OCV special-case section added. |
| 193 | Explain exact versus approximate formulation. | DONE | Dedicated section added. |
| 194 | Add `Manuscript Equations To Insert` table. | DONE | Table added. |
| 195 | Add `Manuscript Claims Allowed` table. | DONE | Table added. |
| 196 | Add `Manuscript Claims Forbidden` table. | DONE | Table added. |
| 197 | Add `Requires Later Chapter` table. | DONE | Table added. |
| 198 | Cross-check against equation dependency DAG. | DONE | Cross-check summary records PASS. |
| 199 | Cross-check against notation bible. | DONE | Cross-check summary records PASS. |
| 200 | Cross-check retained concepts against source evidence index. | DONE | Cross-check summary records PASS with refs. 6/7 caution. |
| 201 | Record whether package is Chapter 1-ready. | DONE | Package states ready as math package, not final body. |
| 202 | Save Phase 006 result. | DONE | This file saved. |
| 203 | Update execution ledger. | DONE | `REBUILD_V2_EXECUTION_LEDGER.md` updated after this result. |
| 204 | Gate Phase 006. | PASS | `PASS_REBUILD_V2_CHAPTER1_MATH`. |
| 205 | Gate requires charge balance, OCV special case, DAE/Volterra form, ICA/DVA derivation. | PASS | All present. |
| 206 | Stop if package introduces `V_OCV` before charge balance. | NOT TRIGGERED | OCV appears after residual/root. |
| 207 | Stop if package treats `Q_bg` as visual baseline only. | NOT TRIGGERED | `Q_bg` is explicitly storage. |
| 208 | Stop if package allows kinetics to change charge conservation. | NOT TRIGGERED | Kinetics update states only. |
| 209 | Stop if package cannot state how `V_n` is solved. | NOT TRIGGERED | Root operator and residual stated. |
| 210 | Stop if package cannot state when q-domain dynamics are invalid. | NOT TRIGGERED | Rest and `I_abs=0` invalidity stated. |
| 211 | Proceed only if Chapter 1 can be written without Chapter 2-5 content. | PASS | Heat, kinetics expansion, fitting, hysteresis deferred. |
| 212 | Record open mathematical risks. | DONE | Section added. |
| 213 | Record open physical risks. | DONE | Section added. |
| 214 | Record open notation risks. | DONE | Section added. |
| 215 | Record items needing user decision. | DONE | Section added. |
| 216 | Record exact equations not yet visually verified. | DONE | Section added. |
| 217 | Record exact source references for central equation. | DONE | Source reference table added. |
| 218 | Record exact source references for final ICA/DVA equations. | DONE | Source reference table added. |
| 219 | Record exact source references for rest relaxation. | DONE | Source reference table added. |
| 220 | Record exact source references for voltage distinctions. | DONE | Source reference table added. |

## Key Outcome

The Chapter 1 mathematical structure is now fixed as:

1. measured charge coordinate;
2. internal state and storage definitions;
3. charge-balance residual;
4. root-solved internal potential `V_n`;
5. equilibrium OCV as a special root;
6. apparent/driving voltages;
7. kinetic interface;
8. time and charge-domain dynamics;
9. Volterra-like self-consistent integral form;
10. rest relaxation;
11. derivative observables and ICA/DVA;
12. validation residuals and open-risk boundaries.

## Gate Check

| Gate Item | Result |
|---|---|
| Charge balance included | PASS |
| `V_n` root solve included | PASS |
| OCV special case included after charge balance | PASS |
| DAE/Volterra form included | PASS |
| q-domain invalidity at rest stated | PASS |
| ICA/DVA derivation included | PASS |
| `Q_bg` treated as storage | PASS |
| Kinetics prevented from changing charge conservation | PASS |
| Source references recorded | PASS |
| Open risks recorded | PASS |

Gate result: `PASS_REBUILD_V2_CHAPTER1_MATH`

## Files Created Or Updated

| File | Action |
|---|---|
| `D:\Projects\Project_Anode_Fit\Codex\results\REBUILD_V2_CHAPTER1_MATH_PACKAGE.md` | created |
| `D:\Projects\Project_Anode_Fit\Codex\results\REBUILD_V2_PHASE_006_CHAPTER1_MATH_RESULT.md` | created |
| `D:\Projects\Project_Anode_Fit\Codex\results\REBUILD_V2_EXECUTION_LEDGER.md` | updated |

## Next Phase Entry Condition

Proceed to Phase 007 Step 221 only if the next work is refs. 6/7 closure method packaging. The next phase must not import molecular-pair physics into graphite and must not claim exact ref. 6/7 derivations before full verification.
