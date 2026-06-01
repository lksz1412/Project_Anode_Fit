# Phase 017 — Chapter 1 v5 Convention-Safe Polish Result

Date: 2026-05-29

## Scope

User request:

- Absorb the good points from the latest comparison.
- Avoid introducing new convention problems.
- Avoid introducing new logic problems.

This phase did not rewrite Chapter 1 theory. It produced a v5 manuscript candidate by applying narrowly scoped polish to the v4 candidate.

## Input Files

| Role | File | Coverage |
|---|---|---|
| Project instruction | `D:\Projects\Project_Anode_Fit\Codex\AGENTS.md` | read top-level applicable sections |
| Comparison basis | `D:\Projects\Project_Anode_Fit\Codex\results\PHASE_016_CH1_V4_V3_COMPARISON.md` | read repair candidates and verdict |
| Source manuscript | `D:\Projects\Project_Anode_Fit\Codex\results\graphite_ica_chapter1_rebuilt_v4_consistency_repaired.tex` | targeted repair locations read; Phase 016 already recorded full read lines 1-856 |
| Generated manuscript | `D:\Projects\Project_Anode_Fit\Codex\results\graphite_ica_chapter1_rebuilt_v5_convention_safe_polish.tex` | full read lines 1-858 in chunks: 1-220, 221-440, 441-660, 661-858 |

## Created Files

| File | Purpose |
|---|---|
| `D:\Projects\Project_Anode_Fit\Codex\plans\2026-05-29-chapter1-v5-convention-safe-polish-plan.md` | Phase 017 plan |
| `D:\Projects\Project_Anode_Fit\Codex\results\graphite_ica_chapter1_rebuilt_v5_convention_safe_polish.tex` | Chapter 1 v5 manuscript candidate |
| `D:\Projects\Project_Anode_Fit\Codex\work\create_ch1_v5_convention_safe_polish.ps1` | reproducible exact-replacement generation script |
| `D:\Projects\Project_Anode_Fit\Codex\results\PHASE_017_CH1_V5_CONVENTION_SAFE_POLISH_RESULT.md` | this result |
| `D:\Projects\Project_Anode_Fit\Codex\results\PHASE_017_CH1_V5_CONVENTION_SAFE_POLISH_LEDGER.md` | phase ledger |
| `D:\Projects\Project_Anode_Fit\Codex\results\PHASE_017_CH1_V5_CONVENTION_SAFE_POLISH_HANDOVER.md` | handover |

## Applied Changes

### C1 — Neutralized version-specific labels

- `DQ-v3-1` -> `VG-1`
- `DQ-v3-2` -> `VG-2`

Reason: `DQ-v3-*` was a version/history marker inside the manuscript body.

### C2 — Removed process-history markers from manuscript body

Rewrote or removed:

- `사용자 2026-05-28`
- `AGP`
- `Codex 산출물과의 대조`
- `Grounding 감사 (AGP self-check)`
- audit-style `통과` table statuses
- standalone `DQ` status in S10 / AL-7, replaced by `GATED`

Reason: these are useful working notes, but they read as process metadata rather than paper-facing theory/validation prose.

### C3 — Expanded the undefined shorthand `K_\lambda`

Old schematic:

```latex
\int A_L(\lambda)K_\lambda\,d\lambda
```

New explicit chain:

```latex
\int_0^\infty A_L(\lambda;T,\psi)\lambda^{-1}
\exp[-(q-q_a)/\lambda]\,d\lambda
```

Reason: v4 already defined the actual exponential kernel. v5 avoids introducing a second undefined kernel symbol in the physical chain.

### C4 — Converted internal audit table into manuscript-style validation status

Section now reads:

```latex
\section{종합·validation status·참고문헌}
\subsection{Assumption and validation status}
```

Statuses now use paper-facing descriptions such as `documented`, `controlled as hypothesis`, `bounded with stated scope`, `retained as core mechanism`, and `forward model only`.

## Verification Evidence

Generated v5:

| Item | Value |
|---|---|
| Path | `D:\Projects\Project_Anode_Fit\Codex\results\graphite_ica_chapter1_rebuilt_v5_convention_safe_polish.tex` |
| Lines | 858 |
| SHA256 | `9E5DCCE75CB650251FAAA7741591B1D23B89632545BAFF157EB5798E53E690F1` |

Static LaTeX checks:

| Check | Result |
|---|---:|
| `\begin{...}` count | 52 |
| `\end{...}` count | 52 |
| `{` count | 750 |
| `}` count | 750 |
| labels | 55 |
| refs | 25 |
| missing refs | 0 |
| bibitems | 20 |
| cites | 20 |
| missing cites | 0 |

Targeted risk pattern checks:

| Pattern | Count |
|---|---:|
| `\xi` | 0 |
| `L=v_Q/k` | 0 |
| `$L(G)$` | 0 |
| `large-$L$` | 0 |
| `short-$L$` | 0 |
| `\frac{\dd r_j}{\dd Q}` | 0 |
| `Q_{a,j}` | 0 |
| `\Theta(Q)` | 0 |
| core `dQ/dV_n` | 0 |
| `solver` | 0 |
| `fallback` | 0 |
| `회귀` | 0 |
| `K_\lambda` | 0 |
| `DQ-v3` | 0 |
| standalone `DQ` status (`& DQ &`, `BOUNDED+DQ`) | 0 |
| `Codex` | 0 |
| `AGP` | 0 |
| `2026-05-28` | 0 |
| `Grounding 감사` / `self-check` | 0 |
| generic `\,dL` | 0 |
| `K_L` | 0 |
| `delta(L-L_0)` | 0 |
| `code route/procedure/coding route` | 0 |
| `closed analytic shortcut` | 0 |
| `switch criterion` | 0 |
| `single-mode floor` | 0 |
| audit-style `통과` | 0 |

PDF build:

- `xelatex`: `NOT_FOUND`
- PDF not generated in this phase.

## Logic/Convention Review Notes

Confirmed preserved:

- `q` remains the primary coordinate.
- `L_q` remains the primary normalized relaxation length.
- `L_Q` appears only as explicit dimensional conversion.
- `\theta` remains the state variable; no `\xi` state-symbol drift was introduced.
- Plan B remains the conservative theoretical baseline.
- Plan A remains candidate analytic compression gated by Fredholm/Volterra and M1-M5 criteria.
- Activation barrier is retained.
- Step-function / hard-switch interpretation remains excluded.
- The central kernel integral remains the Chapter 1 load-bearing equation.

Confirmed repaired:

- Version-specific `DQ-v3-*` labels removed.
- Undefined `K_\lambda` shorthand removed.
- Process metadata in the summary/validation area removed.
- Standalone internal `DQ` status removed.

## Remaining Gates

- External source audit of the user's PhD paper's Refs 6/7 was not re-performed in this phase.
- Plan A must remain gated until the Fredholm/Volterra mapping and limiting-case checks are explicitly source-audited.
- PDF build remains unverified until a TeX engine such as `xelatex` is available.

## Incident / Correction Note

The first generation script attempt stopped before writing v5 because exact replacement order changed one later target. The second attempt stopped because `DQ-v3-2` had already been removed by earlier exact replacements. Both were pre-write safety stops. The script was corrected, rerun, and the final v5 file above was generated and verified.
