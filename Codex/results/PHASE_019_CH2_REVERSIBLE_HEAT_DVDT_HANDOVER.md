# Phase 019 Handover - Chapter 2 Reversible Heat and dV/dT

## Current Ground Truth

Current Chapter 1 canonical candidate:

- `D:\Projects\Project_Anode_Fit\Codex\results\graphite_ica_chapter1_rebuilt_v5_convention_safe_polish.tex`

Current Chapter 2 candidate:

- `D:\Projects\Project_Anode_Fit\Codex\results\graphite_ica_chapter2_reversible_heat_dvdt_v1.tex`
- SHA256: `21BF4933DE5D332B9EF61BC5F10645F11254BF11811C68855496FA5A2C5B6F63`

## What Chapter 2 Establishes

Chapter 2 extends Chapter 1 to thermal quantities while preserving the core ICA-tail mechanism:

```text
charge conservation
-> equilibrium dV/dT
-> entropy coefficient h_n^eq
-> reversible heat
-> dynamic/apparent dV/dT separation
-> tail-spectrum contribution to finite-current thermal response
```

The central fixed-`q` equilibrium derivative is:

```latex
h_n^{\eqs}(q,T)
=
-\frac{
\left(\partial Q_{\bg}/\partial T\right)_V
+Q_p\left(\partial\Theta_{\eqs}/\partial T\right)_V}
{C_{\bg}(V_{n,\eqs},T)
+Q_p\left(\partial\Theta_{\eqs}/\partial V\right)_T}
```

Reversible heat:

```latex
\dot Q_{\rev,n}=-I_sT h_n^{\eqs}
```

Apparent derivative:

```latex
h_n^{\app}
=
h_n^{\dyn}
+
\left(\partial\eta_n/\partial T\right)_{q,\calH}
```

## Critical Boundaries

- `h_n^eq` is an equilibrium entropy coefficient.
- `h_n^app` is not an entropy coefficient unless relaxation and polarization correction reduce it to equilibrium.
- Chapter 1 tail kernel affects dynamic apparent thermal response.
- Tail area or tail shape is not automatically reversible heat.
- `dot Q_irr,n` remains separate from `dot Q_rev,n`.
- No solver/fitting implementation has been performed.

## Review Status

10 review passes completed:

1. Convention audit.
2. Charge-balance algebra audit.
3. Thermodynamic identity/sign audit.
4. Apparent vs equilibrium audit.
5. Reversible vs irreversible heat audit.
6. Tail-kernel thermal-response audit.
7. Physical assumption and literature audit.
8. Undergraduate-followability audit.
9. Chapter handoff audit.
10. Manuscript hygiene/process-label audit.

Blocking issues found and repaired:

- Old-coordinate mention in a convention sentence.
- Process-version wording in manuscript body.
- Missing sign-bridge derivation from free energy to reversible heat.
- Missing peak-anchor shift term in tail-kernel temperature derivative.

## Verification

Run:

```powershell
& 'D:\Projects\Project_Anode_Fit\Codex\work\verify_ch2_reversible_heat_dvdt_v1.ps1' `
  -TexPath 'D:\Projects\Project_Anode_Fit\Codex\results\graphite_ica_chapter2_reversible_heat_dvdt_v1.tex'
```

Expected snapshot:

```text
Lines: 932
SHA256: 21BF4933DE5D332B9EF61BC5F10645F11254BF11811C68855496FA5A2C5B6F63
MissingRefs: []
MissingCites: []
Xelatex: NOT_FOUND
```

## Next Recommended Phase

Chapter 3 should start from Chapter 2 definitions and add electrochemical reaction kinetics:

- expand `k_j(G,T,psi)` into a reaction-kinetic expression;
- connect overpotential `eta_n` to charge-transfer or Butler-Volmer-like terms;
- derive how kinetic lag modifies `R_Theta`, `h_n^dyn`, and apparent ICA tail behavior;
- keep reversible heat tied to `h_n^eq`.

