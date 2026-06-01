# Phase 014 — Chapter 1 v3 vs Previous Codex v2 Comparison

Date: 2026-05-28

## Scope

Primary comparison requested by user: compare the latest generated Codex Chapter 1 artifact with the immediately previous Codex generated artifact.

| Role | File | Lines | SHA256 |
|---|---|---:|---|
| Previous generated Codex version | `D:\Projects\Project_Anode_Fit\Codex\results\graphite_ica_chapter1_rebuilt_v2_dual_closure.tex` | 1013 | `8C38421A18A6F2ABE666C8C1F3A4B79EB64A97D2919C93C2955B450A4654E537` |
| Latest generated Codex version | `D:\Projects\Project_Anode_Fit\Codex\results\graphite_ica_chapter1_rebuilt_v3_canonical_merge.tex` | 748 | `3456DFEA20078191FAD0F1388C75ECCD083C029080986ACA8210E2CC6995B809` |

Read coverage:

- v2 full read lines 1-1013.
- v3 full read lines 1-748.

## Static Checks

| Check | v2 | v3 |
|---|---:|---:|
| begin/end | `54/54` | `43/43` |
| braces | `643/643` | `664/664` |
| labels/refs | `90/35`, missing `0` | `46/48`, missing `0` |
| cites/bibitems | `15/15`, missing `0`, uncited `0` | `27/20`, missing `0`, uncited `0` |
| caution-pattern hits | `2` | `6` |

Caution-pattern hit interpretation:

- v2 hits are benign: `fitting model` in scope prose and `closed-form analytic shortcut` in a negating sentence.
- v3 hits are mostly forbidden-model discussion around `$0\!\to\!1$`; these are allowed because they reject the step model. No adopted step-function model was found.

## High-Level Verdict

v3 is better as a manuscript-facing candidate, but v2 is better as a step-by-step derivation notebook.

Canonical direction remains:

```text
Use v3 as the manuscript shell,
but repair v3's notation/coordinate drift using v2's consistency.
```

v3 should not be treated as mathematically cleaner than v2 yet. It is structurally stronger, but it introduced several consistency risks while merging Claude's `theta/q` convention with Codex v2's `xi/Q` closure equations.

## What v3 Improved Over v2

### 1. Manuscript structure

v3 adds a stronger paper-style outer shell:

- user verbatim section;
- explicit interpretation correction from the user;
- H1-H6 hypothesis block;
- S1-S14 grounded spine;
- AL tags and self-audit;
- graphite staging sequence section;
- full-cell / apparent-potential bridge;
- stronger falsification protocol;
- DOI-rich bibliography.

v2 was clearer as a derivation document, but it did not have enough manuscript governance and grounding structure.

### 2. User intent is more visible

v3 preserves the user's key points at the front:

```text
low T -> long tail
high T -> shorter tail
activation barrier is valid
old step-function completion is forbidden
Plan B is theory, not code fallback
```

This makes v3 easier to review and closer to paper/patent style.

### 3. Better graphite-specific framing

v3 includes graphite staging:

```text
stage 4 -> 3 -> 2L -> 2 -> 1
```

v2 discusses graphite staging more generally but does not integrate the staging sequence as cleanly.

### 4. Better voltage bridge and falsification

v3 improves:

- distinction between internal anode potential `V_n`, apparent anode potential `V_{n,app}`, and full-cell terminal voltage;
- warning about potential-assistance slope vs charge-transfer / Tafel co-linearity;
- non-unique inverse warning;
- competing mechanisms table.

This is a real improvement over v2.

### 5. Plan A / Plan B rhetoric is safer than Claude-style fallback language

v3 has removed the implementation-colored language from the adopted theory:

```text
Plan A = candidate analytic closure
Plan B = conservative theoretical formulation
```

This matches the user's latest correction better than solver-oriented wording.

## What v2 Still Does Better

### 1. Undergraduate-followable derivation

v2 is much stronger for step-by-step derivation:

- state variable definition;
- lattice-gas chemical potential equation;
- explicit equilibrium condition;
- ideal logistic target;
- derivative of `xi_eq` with respect to `V_n`;
- charge-balance differential form;
- forward/backward rates -> relaxation equation;
- residual equation derivation;
- local post-peak exponential kernel;
- barrier-to-length Jacobian.

v3 compresses several of these into prose or inline equations. That improves manuscript compactness, but weakens the user's requirement that a university undergraduate can follow every step without a hidden jump.

### 2. Notation consistency

v2 is internally consistent around:

```text
state variable = xi_j
coordinate = Q
local length = L = v_Q/k
Plan B residual = d r_j/dQ + (k_j/v_Q) r_j = d xi_eq,j/dQ
```

v3 mixes conventions:

```text
main state variable = theta_j
main local coordinate = q
local kernel = exp[-(q-q_a)/L]
Plan B residual = d r_j/dQ + (k_j/v_Q)r_j = d xi_eq,j/dQ
Plan B tail = exp[-(Q-Q_a,j)/L]
```

This is the most important repair item.

### 3. v2 is cleaner as a logic-only baseline

v2's Plan B section says the right thing in plain form:

```text
local ODE + relaxation-length spectrum kernel integral = conservative theoretical formulation
```

v3 carries the same idea, but its surrounding manuscript layers add AL/fitting/governance language that may obscure the core if not polished.

## Main v3 Problems Found

### P1 — Coordinate drift: `q` vs `Q`

v3 primarily uses normalized coordinate `q=Q_ext/Q_cell`, and derives:

```latex
\frac{dr}{dq}+\frac{Q_\cell k}{|I|}r=\frac{d\theta_\eq}{dq}
```

But Plan B later uses:

```latex
\frac{\dd r_j}{\dd Q}+\frac{k_j}{v_Q}r_j=\frac{\dd\xi_{\eq,j}}{\dd Q}
```

Affected v3 lines observed:

- line 323-331: q-coordinate derivation and `L=|I|/(Q_cell k)`.
- line 493-508: Plan B switches back to dimensional `Q` and `xi`.
- line 541: says `d\Theta/dQ` although the central kernel is `d\Theta_tail/dq`.

Fix: choose one coordinate convention for Chapter 1, or explicitly define both:

```text
Q-coordinate: L_Q = v_Q/k, kernel exp[-(Q-Q_a)/L_Q]
q-coordinate: L_q = L_Q/Q_cell = |I|/(Q_cell k), kernel exp[-(q-q_a)/L_q]
```

Then every equation should carry `L_Q` or `L_q`, not a single ambiguous `L`.

### P2 — State symbol drift: `theta` vs `xi`

v3's main table and derivation use `theta_j`, but the imported Plan B and Plan A condition still mention `xi_j`.

Affected v3 lines observed:

- line 466: ratio candidates include `\xi_j(s)/\xi_j(Q)`.
- line 493-495: Plan B residual uses `\xi_{\eq,j}`.

Fix: either:

1. use `theta_j` everywhere in v3, or
2. define `theta_j \equiv xi_j` once and say the manuscript uses `theta` for graphite site fraction while previous derivation used `xi`.

Given the current manuscript shell, option 1 is cleaner.

### P3 — v3 lost some derivation granularity

v3 is more publishable, but it lost v2's detailed derivation of:

- regular-solution chemical potential as a displayed equation;
- equilibrium condition leading to logistic target;
- derivative of equilibrium target and width argument;
- forward/backward-rate derivation of first-order relaxation;
- charge-balance differential derivation of ICA.

Fix: reinsert these as compact displayed derivation blocks, not as long tutorial prose. This would keep v3 manuscript structure while satisfying the user's no-logic-gap requirement.

### P4 — AL tags are useful but currently external

v3 refers to AL-# tags, but the actual Assumption Ledger content is not included in the `.tex` file. If this is meant to stand alone as a Chapter 1 manuscript, AL tags need either:

- a short Assumption Ledger table in the chapter, or
- an appendix/reference to the exact ledger document.

Otherwise a reviewer sees `AL-7` but cannot verify what AL-7 says.

### P5 — Later fitting section still leans slightly Plan A

v3's later fitting interface says:

```text
Refs 6/7 closure expression -> dQ/dV_n
```

This is not wrong if it is clearly Plan A, but for the current theory-only chapter the safer wording is:

```text
Plan B core expression always exists; Plan A candidate closure may replace the self-consistent layer after validation.
```

Fix: revise the later fitting section to list both paths rather than only the Refs 6/7 closure path.

## Requirement-by-Requirement Comparison

| Requirement | v2 | v3 | Better |
|---|---|---|---|
| Low T long tail explained | yes | yes | tie |
| High T short tail explained | yes | yes | tie |
| Activation barrier retained but not step completion | yes | yes | tie |
| Plan B as theory, not code fallback | strong | strong | tie |
| Manuscript / paper style | medium | strong | v3 |
| Undergraduate-followable derivation | strong | medium | v2 |
| Notation consistency | strong | medium-low | v2 |
| Graphite staging specificity | medium | strong | v3 |
| Voltage bridge | medium | strong | v3 |
| Falsification protocol | good | strong | v3 |
| Literature / DOI grounding | medium | strong | v3 |
| Standalone self-containment | strong for derivation, weaker for literature | medium, because AL is external | mixed |

## Recommended Next Action

Do not discard v3. It is the better canonical manuscript base.

But before calling it Chapter 1 final, run one repair pass focused only on consistency:

1. Normalize notation: `theta` everywhere or `xi` everywhere.
2. Normalize coordinate: either `Q/L_Q` or `q/L_q`, with an explicit conversion if both are retained.
3. Reinsert v2's key derivation blocks where v3 became too compressed.
4. Add a compact AL table or remove unsupported AL-tag dependency from standalone manuscript mode.
5. Change later fitting interface so Plan B remains visibly primary and Plan A remains a candidate closure.

## Final Judgment

v3 is the right direction structurally.

v2 is still the safer derivation reference.

The best next canonical version should be:

```text
v3 manuscript shell
+ v2 derivation granularity
+ corrected theta/q vs xi/Q notation and coordinate consistency
```

Current status:

```text
v3 = strong manuscript candidate, not yet final logic-fixed manuscript.
```
