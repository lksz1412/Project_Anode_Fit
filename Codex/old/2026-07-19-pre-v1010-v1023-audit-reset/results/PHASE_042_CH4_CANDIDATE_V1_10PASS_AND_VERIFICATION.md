# Phase 042 - Ch4 Candidate V1 10-Pass Review and Verification

## Scope

- Input reference: `D:\Projects\Project_Anode_Fit\Codex\results\PHASE_020_CLAUDE_REBUILT_REFERENCE_2026-06-01\graphite_ica_ch4_rebuilt.tex`
- Output candidate: `D:\Projects\Project_Anode_Fit\Codex\results\graphite_ica_ch4_codex_candidate_v1.tex`
- PDF check output: `C:\Users\lksz1\OneDrive\문서\New project\_texcheck_codex_ch4_v1\graphite_ica_ch4_codex_candidate_v1.pdf`
- Source read coverage:
  - Reference: 1-190, 191-380, 381-570, 571-760, 761-929.
  - Candidate: 1-180, 181-360, 361-540, 541-720, 721-859 before final small edits; final touched regions rechecked around inherited formulas, Ch4 heat equations, and AL/conclusion sections.

## Source Defects Found

1. Worker metadata was embedded in the TeX body: RB/CHARTER/Phase wording, author/date, self-check table, and Chapter 6/solver handoff.
2. Ch1 V5 convention was violated by unsplit `Q_\bg` in charge balance, OCV temperature derivative, and background heat progress/coordinate split.
3. Ch3 V1 convention was violated by inherited wording that treated `\chi_j` and `\beta_j` as identical.
4. Ch4 contained Chapter 6 / solver implementation references despite the current project scope being theory-only.
5. Section titles with inline math produced PDF bookmark warnings; Unicode symbols in the AL table and body contributed to rendering warnings.

## Applied Repairs

1. Removed worker-facing metadata from the TeX body and replaced title/maketitle handling with a clean manual title block.
2. Replaced unsplit `Q_\bg` with `Q_\bg^{\eq}` and aligned progress notation to `\dot Q_\bg^{\eq,\prog}` / `\dot Q_\bg^{\eq,\coord}`.
3. Replaced `\chi_j\equiv\beta_j` with the Ch3 V1 distinction:
   - `\chi_j`: Chapter 1 Level-A scalar mobility sensitivity.
   - `\beta_j`: Chapter 3 Level-B directional transfer coefficient.
   - comparison only through `\chi_{j,\mathrm{proj}}`.
4. Preserved Ch4's core derivation:
   - network/master-equation entropy production,
   - `\mathcal A_j^{\chem}=RT\ln(\mathcal J_j^+/\mathcal J_j^-)`,
   - detailed-balance-limited reduction to `n_j^{\eff}F\eta_j`,
   - `\dot{\mathcal Q}_{\irr,n}=\sum_j n_j^{\eff}I_j\eta_j\ge0`.
5. Removed Chapter 6/solver transfer items and left only Chapter 5 theory handoff.
6. Replaced Peltier symbol `\Pi_j` with `P_{\rev,j}` to avoid the XeLaTeX math-font missing-glyph warning source.
7. Removed Unicode em dash and Unicode AL-table symbols as mechanical rendering cleanup.

## 10-Pass Review

1. Global spine pass: Ch1 V5 `Q_\bg^{\eq}`, `V_n/V_{n,\app}/V_{n,\drive}/V_{n,\OCV}`, `\chi_j`/`\beta_j` separation checked.
2. Ch2 heat split pass: reversible heat = equilibrium entropy coefficient / reaction entropy; irreversible heat = overpotential entropy production; no mixing.
3. Ch3 kinetic interface pass: `r_j^\pm`, `\mathcal J_j^\pm`, detailed balance, `n_j^{\eff}` inherited with explicit bounded conditions.
4. Micro-to-macro algebra pass: `\mathcal J^+/\mathcal J^-` decomposition, detailed-balance substitution, `V_{n,\drive}=V_n` restriction, and `F` cancellation checked.
5. Sign/second-law pass: `(a-b)\ln(a/b)\ge0`, `I_j` and `\eta_j` same-sign argument, and summed nonnegative heat checked.
6. Reversible heat pass: OCV coefficient, transition entropy basis, and double-counting restriction checked.
7. Background heat pass: `Q_\bg^{\eq}` progress vs coordinate shift checked.
8. Transport/rest pass: `R_n`, `R_{\ct}`, `R_{n,\eff}` separation and rest relaxation internal-current interpretation checked.
9. Scope pass: no solver/implementation/Chapter 6 handoff remains in the TeX body.
10. Static/render pass: labels, refs, cites, bibitems, and PDF compile log checked.

## Static Verification

- Environment command family: PowerShell static regex checks.
- begin/end: 53 / 53
- labels: 46
- duplicate labels: 0
- refs: 92
- missing refs: 0
- cites: 11
- bibitems: 10
- missing cites: 0
- unused bibitems: 0
- risk scan: no `RB_`, `CHARTER`, `Author`, `Date`, `재구성본`, `자체 검수`, `검수표`, `Chapter 6`, `Ch6`, `solver`, direct unsplit `Q_\bg`, `\Pi`, `\chi_j=\beta_j`, or `\beta_j=\chi_j`.

## XeLaTeX Verification

- Engine: `C:\Users\lksz1\AppData\Local\Programs\MiKTeX\miktex\bin\x64\xelatex.exe`
- Runs: repeated XeLaTeX passes after repairs.
- PDF: generated, 18 pages, final size 362277 bytes.
- Final log counts:
  - fatal errors: 0
  - citation warnings: 0
  - reference warnings: 0
  - hyperref warnings: 0
  - missing character: 1
  - overfull hbox: 8
  - underfull hbox: 1
  - font warnings: 5
- Residual note: one `Missing character` log entry remains around the long AL table region. The source was scanned for worker metadata, unsplit `Q_\bg`, explicit unicode arrows/dashes/comparison symbols, and `\Pi`; those were removed. The PDF is generated, but this is retained as a layout-log residual rather than reported as a clean render.

## Gate Result

Conditional pass for theory/content continuity; render log has one residual `Missing character` warning and layout warnings. Proceed to Chapter 5 while preserving this residual in the ledger.

