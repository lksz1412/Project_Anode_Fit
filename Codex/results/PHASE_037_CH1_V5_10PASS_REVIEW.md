# Phase 037 — Chapter 1 V5 10-Pass Review

## Summary

Chapter 1 V5 was reviewed with ten distinct passes focused on different failure modes. This phase did not treat build success as logical success; build verification is recorded separately in Phase 038.

## Target

- File: `D:\Projects\Project_Anode_Fit\Codex\results\graphite_ica_ch1_codex_candidate_v5.tex`
- Lines: 993
- SHA256 after repair: `D5D77DC97E8FB598C39B69F339F15E048273F03D1E767A576A5816DD469A64A1`

## Coverage

Whole-file coverage was checked by section/range inventory:

- 1-120
- 121-240
- 241-360
- 361-480
- 481-600
- 601-720
- 721-840
- 841-993

The section list spans introduction, notation, convention/AL, staging, charge conservation, equilibrium, rate, dynamics, spectrum, kernel, Volterra, Plan B, Plan A, fiteq, simplefit, falsification, numeric appendix, and Ch2--5 handoff.

## Pass Results

| Pass | Focus | Result |
|---|---|---|
| P1 | structure/metadata/convention | PASS. No process metadata in title/body. Sections are ordered from observation to downstream handoff. |
| P2 | variable introduction | PASS after repair. Basic constants, `q_a`, `C_bg`, `kappa(T)`, `D`, and `eta_ct` are defined. |
| P3 | equation continuity | PASS with note. Volterra and Plan A now include intermediate assumptions/equations. |
| P4 | assumptions/grounding | PASS with bounded notes. AL-1--16 continuous; AL-9 gates single-mode fitting. |
| P5 | units/signs | PASS. Eyring correction uses minus sign and current-prefactor-free `ln[|I|/(LT)]`. |
| P6 | dependency chain | PASS. Observation -> charge balance -> equilibrium -> rate -> dynamics -> spectrum -> Volterra -> fiteq remains intact. |
| P7 | reverse forward-ref | PASS by static refs/cites. No missing labels/citations. |
| P8 | fitting usability | PASS with bounded scope. `L`, `Z_L`, `chi_j`, and `y_kappa` extraction order is stated; narrow-spectrum gate is explicit. |
| P9 | adversarial physics | PASS for previously found criticals. Stretched spectrum no longer self-falsifies single-L Arrhenius; `Q_bg` roles are split. |
| P10 | final user criteria | PASS for Ch1 repair gate. Remaining issues are layout warnings and downstream chapter work, not Ch1 critical logic blockers. |

## Remaining Bounded Issues

- `Plan A` remains a validated approximation, not the low-temperature stretched-tail authority. V5 explicitly routes low-temperature/stretched cases to Plan B or spectrum forward prediction.
- `kappa(T)` remains either independently supplied or bounded by the derivative condition. Without that, Eyring slope is apparent rather than pure.
- Layout warnings remain from long tables and dense equations; they do not block TeX compilation but should be cleaned before publication formatting.

## Gate

No unresolved Critical/High from Claude's Ch1 review remains as an unbounded Ch1 logic blocker. Chapter 2 may start only using the V5 downstream interface.
