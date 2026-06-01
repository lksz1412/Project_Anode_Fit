# Phase 016 — Chapter 1 v4 vs v3 Comparison

Date: 2026-05-29

## Scope

User request: compare the latest generated version with the immediately previous generated version.

Compared files:

| Role | File | Lines | SHA256 |
|---|---|---:|---|
| Previous generated version | `D:\Projects\Project_Anode_Fit\Codex\results\graphite_ica_chapter1_rebuilt_v3_canonical_merge.tex` | 748 | `3456DFEA20078191FAD0F1388C75ECCD083C029080986ACA8210E2CC6995B809` |
| Latest generated version | `D:\Projects\Project_Anode_Fit\Codex\results\graphite_ica_chapter1_rebuilt_v4_consistency_repaired.tex` | 856 | `615CD1F828B61C7A24E56FE7FA55F01F306768CEEBC69655D8B50BBB60A8CCC6` |

Read coverage:

- v3 full read lines 1-748.
- v4 full read lines 1-856.
- Phase 015 handover read before comparison.

## Static Checks

| Check | v3 | v4 |
|---|---:|---:|
| lines | 748 | 856 |
| begin/end | `43/43` | `52/52` |
| braces | `664/664` | `749/749` |
| labels | 46 | 55 |
| refs | 21 | 25 |
| missing refs | 0 | 0 |
| missing cites | 0 | 0 |

Diff stat:

```text
1 file changed, 193 insertions(+), 85 deletions(-)
```

## Targeted Risk Pattern Comparison

| Pattern | v3 | v4 | Interpretation |
|---|---:|---:|---|
| `\xi` | 2 | 0 | theta/xi drift removed |
| `L=v_Q/k` | 3 | 0 | ambiguous length convention removed |
| `$L(G)$` | 1 | 0 | generic L mapping removed |
| `large-$L$` | 5 | 0 | all large-length prose now `L_q` |
| `short-$L$` | 6 | 0 | all short-length prose now `L_q` |
| `\frac{\dd r_j}{\dd Q}` | 1 | 0 | Plan B now uses `q` |
| `Q_{a,j}` | 1 | 0 | Plan B tail now uses `q_{a,j}` |
| `\Theta(Q)` | 1 | 0 | Plan A ratio convention repaired |
| `dQ/dV_n` | 3 | 0 | core mapping now `dQ_ext/dV_n` |
| `solver` | 3 | 0 | implementation-colored wording removed |
| `code route` / `code procedure` / `coding route` | 3 total | 0 | code fallback framing removed |
| `closed analytic shortcut` | 1 | 0 | replaced with neutral `compact analytic expression` |
| `\,dL`, `K_L`, `delta(L-L_0)` | 7 total | 0 | remaining generic-L kernel remnants removed |

## Verdict

v4 is materially better than v3 and should replace v3 as the current Codex candidate.

The main Phase 014 problems were actually fixed:

1. `q` / `Q` coordinate drift is repaired.
2. `theta` / `xi` state-symbol drift is repaired.
3. `L` ambiguity is repaired by using `L_q` as the primary normalized relaxation length and `L_Q` only for dimensional conversion.
4. The Plan B residual equation, tail kernel, ICA mapping, and later fitting interface now share one coordinate convention.
5. The derivation is more undergraduate-followable than v3 because displayed derivation blocks were restored.

No blocking new mathematical inconsistency was found in the v4 core chain:

```text
charge conservation -> theta_eq target -> k(G,T,psi) -> L_q -> A_L(lambda) -> kernel integral -> dQ_ext/dV_n
```

## What v4 Improved Over v3

### 1. Coordinate and dimensional consistency

v3 used `q` in the main derivation but reverted to dimensional `Q` in Plan B. v4 keeps the main theory in `q`:

```latex
\frac{\dd r_j}{\dd q}+\frac{Q_\cell k_j}{|I|}r_j
=
\frac{\dd\theta_{\eq,j}}{\dd q}
```

and defines dimensional conversion separately:

```latex
L_Q=Q_\cell L_q=v_Q/k.
```

This removes the highest-risk v3 problem.

### 2. ICA mapping is now consistent with charge balance

v3 wrote:

```latex
\frac{dQ}{dV_n}=
\frac{C_\bg}{1-Q_p(d\Theta/dQ)}.
```

v4 derives:

```latex
\frac{dQ_\ext}{dV_n}
=
Q_\cell\frac{dq}{dV_n}
=
\frac{C_\bg}
{1-(Q_p/Q_\cell)(d\Theta/dq)}.
```

This is the correct normalized-coordinate form following from:

```latex
Q_\cell=C_\bg\,dV_n/dq+Q_p\,d\Theta/dq.
```

### 3. Plan A / Plan B hierarchy is cleaner

v3 still contained code-flavored language such as `solver`, `code route`, `code procedure`, and `coding route`. v4 removes that framing.

v4 now says:

- Plan B is the baseline theoretical formulation.
- Plan A is candidate analytic compression after validation.

This better matches the user's correction that the work is logic/theory, not solver construction.

### 4. Derivation density improved

v4 restores derivation details that v3 compressed:

- regular-solution chemical potential;
- electrochemical equilibrium condition;
- ideal logistic limit;
- derivative of `theta_eq`;
- charge-balance differential form;
- forward/backward rate derivation of first-order relaxation.

This is closer to the user's requirement that an undergraduate reader can follow the derivation without hidden jumps.

### 5. Assumption Ledger is now self-contained

v3 referenced AL tags but did not include the actual ledger body. v4 embeds AL-1 through AL-10. This improves standalone reviewability.

## Remaining Issues / Repair Candidates

### R1 — Version-specific `DQ-v3-*` tags remain in the manuscript body

v4 still contains:

- line 147: `DQ-v3-2`
- line 332: `DQ-v3-1`
- line 774: `DQ-v3-2`

This is not a physics or equation error, but it is a manuscript-cleanliness issue. For a publication/patent-facing version, these should become neutral labels such as:

```text
DQ-1, DQ-2
```

or:

```text
Validation Gate 1, Validation Gate 2
```

### R2 — `K_\lambda` appears as a schematic shorthand

v4 line 504 uses:

```latex
\int A_L(\lambda)K_\lambda\,d\lambda
```

The actual kernel is defined nearby as `\mathcal K(q,q')`, so this is not a core inconsistency. Still, for a final manuscript, either define `K_\lambda` explicitly or replace the shorthand with the explicit exponential kernel expression.

### R3 — `Grounding 감사` table is useful for working drafts but may read like process metadata

v4 lines 780-791 keep a self-check table with `통과`. This is useful internally, but if the document is turned into a paper/patent-style chapter, it should probably move to an appendix or be rewritten as "Assumption and validation status" rather than an audit table.

### R4 — External validation of Refs 6/7 was not re-performed in this comparison phase

This comparison used the existing v3/v4 files and Phase 015 records. It did not reopen the user's PDF or independently re-check the original ref. 6/7 papers. Therefore:

- v4's Plan A wording is internally safer than v3;
- but final publication-level use of Plan A still needs the explicit Refs 6/7 source audit already required by the project rules.

## Non-Issues Confirmed

- The remaining general `dQ/dV` in title/abstract/observation is acceptable because it names the measured ICA concept.
- The core equation layer now uses `dQ_ext/dV_n`, and `dQ/dV_{n,app}` appears only in the observation/measurement layer.
- `dTheta/dQ_ext=(1/Q_cell)dTheta/dq` is intentional dimensional conversion, not drift.
- `dG/dL_q` is the intended Jacobian statement, not a leftover `L` convention.

## Recommendation

Use v4 as the current canonical candidate.

Before the next full rewrite or paper-facing polish, apply a small cleanup pass:

1. Rename `DQ-v3-1/2` labels to neutral `DQ-1/2` or `VG-1/2`.
2. Define or expand `K_\lambda`.
3. Decide whether the `Grounding 감사` table stays in the main text, moves to appendix, or becomes a more paper-like validation table.
4. Re-run a source audit for Refs 6/7 before treating Plan A as publication-ready.
