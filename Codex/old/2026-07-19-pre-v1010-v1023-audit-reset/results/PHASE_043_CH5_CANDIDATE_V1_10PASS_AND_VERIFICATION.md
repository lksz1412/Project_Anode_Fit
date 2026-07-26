# Phase 043 — Chapter 5 Candidate V1 10-Pass and Verification

## Canonical Candidate

- TeX: `D:\Projects\Project_Anode_Fit\Codex\results\graphite_ica_ch5_codex_candidate_v1.tex`
- Lines: 825
- SHA256: `760DD1488D7C1168C7C530E1C57F91476DE2675760183EA3D327BE5C754D1753`
- PDF check: `C:\Users\lksz1\OneDrive\문서\New project\_texcheck_codex_ch5_v1\graphite_ica_ch5_codex_candidate_v1.pdf`
- PDF size: 355715 bytes

## Inputs and Read Coverage

- Source reference:
  `D:\Projects\Project_Anode_Fit\Codex\results\PHASE_020_CLAUDE_REBUILT_REFERENCE_2026-06-01\graphite_ica_ch5_rebuilt.tex`
- Source reference line count: 899
- Source reference SHA256 from earlier source scan:
  `F1E76E7E8760C77339B6BA76CE767C2569C5F4087C8884A273919CC6BED7CD8C`
- Candidate full-read coverage after edits:
  - 1-170
  - 171-340
  - 341-510
  - 511-680
  - 681-825

## Major Repairs

1. Removed worker metadata from TeX body:
   - `RB_`, `CHARTER`, `Phase A`, `P3-`, `Author`, `Date`, `재구성본`, self-check table, and Chapter 6 handoff sections.
2. Repaired Chapter 1 V5 downstream convention:
   - `Q_\bg` -> `Q_\bg^{\eq}` in inherited charge balance and signed relative balance.
   - Removed `\chi_j\equiv\beta_j`; kept `\chi_j` as Chapter 1 scalar mobility sensitivity and `\beta_j` as Chapter 3 directional transfer coefficient.
   - Replaced `Level A = Level B` wording with the precise statement that Chapter 3 detailed-balance stationary limit recovers Chapter 1 stationary target only under stated conditions.
3. Repaired reversible heat notation:
   - Removed `\Pi_j`.
   - Used `P_{\rev,j}^b=-T(\partial U_j^b/\partial T)` and transition entropy basis for branch reversible heat.
4. Repaired hysteresis heat wording:
   - `loop area` is not identified with true hysteresis heat as a whole.
   - Only the physically separated hysteresis-loss component is allowed as a heat term.
5. Repaired branch sign derivation prose:
   - Removed confusing "potential lower" wording and kept the derivation in the Chapter 1 sign convention: chosen discharge coordinate has \(V_n-U_j>0\) as the transition-driving region.
6. Removed solver/code scope from body:
   - Time integration and validation procedures are mentioned only as outside the Chapter 5 physical equation body, not as a Chapter 6 deliverable.
7. Cleaned PDF bookmarks:
   - Removed math from section titles so hyperref warnings are zero.
8. Cleaned table layout:
   - Broke long symbol-table entries and widened AL tier column.

## 10-Pass Review Summary

| Pass | Focus | Result |
|---|---|---|
| P1 | Structure, metadata, body purity | PASS: no `RB_`, `CHARTER`, `Phase A`, self-check, author/date metadata, or Chapter 6 handoff remains. |
| P2 | Variable introduction | PASS: new Ch5 variables are introduced in the symbol table; `I_s`, `b(t)`, `q_\stt`, `s_{\phi,j}^b`, `h_j`, `\Delta V_\obs`, `\Delta V_\hys` have meanings and units where applicable. |
| P3 | Ch1 V5 convention inheritance | PASS: `Q_\bg^{\eq}` is used; `V_n`, `V_{n,\app}`, `V_{n,\drive}`, `V_{n,\OCV}` roles are preserved; `\chi_j` and `\beta_j` are separated. |
| P4 | Sign derivation | PASS: `s_{\phi,j}^\dis=+1`, `s_{\phi,j}^\chg=-1` are derived from logistic sign consistency; charge branch \(I_j<0\), \(\eta_j^\chg<0\), and product \(I_j\eta_j^\chg>0\) are shown. |
| P5 | Reversible vs irreversible heat | PASS: irreversible heat is nonnegative by flux-force sign alignment; reversible heat remains sign-variable through transition entropy coefficient. |
| P6 | Hysteresis physical meaning | PASS: hysteresis is target memory/branch target shift, not mobility change; branch target is Ch3 stationary target on a branch-local detailed-balance surface. |
| P7 | Loop area and double counting | PASS: observed loop/gap is decomposed; whole loop area is not equated with true hysteresis heat; branch-local kinetic dissipation and metastable free-energy loss are not added twice. |
| P8 | Identifiability | PASS: `\Delta V_\obs\ne\Delta V_\hys` is explicit; polarization, kinetic lag, transport, aging, reversible heat, and hysteresis heat are separated by required experimental constraints. |
| P9 | Assumption grounding | PASS: AL-50 through AL-59 are continuous; no missing AL numbers; all bibliography entries are cited. |
| P10 | Full sweep and TeX build | PASS: static parse clean; XeLaTeX build clean except environment/font substitution warnings noted below. |

## Static Verification

- `\begin{}` count: 52
- `\end{}` count: 52
- labels: 50
- duplicate labels: 0
- refs: 100
- missing refs: 0
- cites: 13
- bibitems: 9
- missing cites: 0
- unused bibitems: 0

Risk-pattern scan:

- `RB_`, `CHARTER`, `Phase A`, `P3-`, `Chapter 6`, `Ch.6`, `solver`, `numerical`, self-check wording, author/date metadata: 0
- direct unsplit `Q_\bg`: 0
- `\chi_j\equiv\beta_j`: 0
- `\Pi_j`: 0
- `Level A = Level B` or equivalent equality wording: 0
- star marker `★`: 0

AL continuity check:

- present ALs: 50,51,52,53,54,55,56,57,58,59
- missing ALs: none

## Build Verification

XeLaTeX was run three times with output directory:

- `C:\Users\lksz1\OneDrive\문서\New project\_texcheck_codex_ch5_v1`

Final log scan:

- PDF exists: true
- PDF size: 355715 bytes
- LaTeX errors: 0
- Undefined refs/cites: 0
- Missing characters: 0
- Overfull boxes: 0
- Underfull boxes: 0
- Hyperref warnings: 0
- Font warnings: 5

Residual warnings:

- The 5 font warnings are Korean italic/bold-italic substitution warnings from the KoTeX font stack.
- MiKTeX reports its update reminder during `dvipdfmx`; this is an environment maintenance warning, not a document failure.

## Gate Result

PASS for Chapter 5 candidate V1.

Chapter 5 is now aligned with the Chapter 1 V5 convention spine and does not contain solver/code/Chapter 6 handoff material in the TeX body.
