# Phase 018 — Chapter 1 v5 vs v4 Comparison

Date: 2026-05-29

## Scope

User request:

- "한번더 대조 가자. 직전 생성버전과 비교 ㄱㄱ"

Compared files:

| Role | File | SHA256 |
|---|---|---|
| Previous generated version | `D:\Projects\Project_Anode_Fit\Codex\results\graphite_ica_chapter1_rebuilt_v4_consistency_repaired.tex` | `615CD1F828B61C7A24E56FE7FA55F01F306768CEEBC69655D8B50BBB60A8CCC6` |
| Latest generated version | `D:\Projects\Project_Anode_Fit\Codex\results\graphite_ica_chapter1_rebuilt_v5_convention_safe_polish.tex` | `9E5DCCE75CB650251FAAA7741591B1D23B89632545BAFF157EB5798E53E690F1` |

Read coverage:

- v4 full read by line-numbered chunks: lines 1-856.
- v5 full read by line-numbered chunks: lines 1-858.
- Phase 017 handover read before comparison.

## Static Checks

| Check | v4 | v5 |
|---|---:|---:|
| line split count including final trailing blank | 857 | 858 |
| line-numbered read coverage | 1-856 | 1-858 |
| `\begin{...}` / `\end{...}` | `52/52` | `52/52` |
| braces | `749/749` | `750/750` |
| labels | 55 | 55 |
| refs | 25 | 25 |
| missing refs | 0 | 0 |
| bibitems | 20 | 20 |
| cites | 20 | 20 |
| missing cites | 0 | 0 |
| `xelatex` | `NOT_FOUND` | `NOT_FOUND` |

Diff stat:

```text
1 file changed, 38 insertions(+), 37 deletions(-)
```

## Targeted Risk Pattern Comparison

| Pattern | v4 | v5 | Interpretation |
|---|---:|---:|---|
| `\xi` | 0 | 0 | no theta/xi drift |
| `L=v_Q/k` | 0 | 0 | no generic length regression |
| `$L(G)$` | 0 | 0 | no generic L mapping regression |
| `large-$L$` | 0 | 0 | no generic large-L prose |
| `short-$L$` | 0 | 0 | no generic short-L prose |
| `\frac{\dd r_j}{\dd Q}` | 0 | 0 | Plan B remains in `q` |
| `Q_{a,j}` | 0 | 0 | Plan B tail remains in `q_{a,j}` |
| `\Theta(Q)` | 0 | 0 | no normalized/dimensional coordinate drift |
| core `dQ/dV_n` | 0 | 0 | core mapping remains `dQ_\ext/dV_n` |
| `solver` | 0 | 0 | no implementation framing |
| `fallback` | 0 | 0 | no code fallback framing |
| `회귀` | 0 | 0 | no code-style fallback wording |
| `K_\lambda` | 1 | 0 | undefined shorthand removed |
| `DQ-v3` | 3 | 0 | version-specific tags removed |
| standalone `DQ` status | 2 | 0 | internal decision-queue style status removed |
| `Codex` | 1 | 0 | process-history marker removed |
| `AGP` | 3 | 0 | process/audit marker removed |
| `2026-05-28` | 3 | 0 | dated work-history marker removed |
| `Grounding 감사` / `self-check` | 3 | 0 | audit-table framing removed |
| audit-style `통과` | 15 | 0 | process PASS wording removed |
| generic `\,dL` | 0 | 0 | no generic kernel variable drift |
| `K_L` | 0 | 0 | no generic kernel shorthand regression |

## Verdict

v5 is better than v4 and should remain the current Codex Chapter 1 candidate.

No blocking new mathematical inconsistency was found. The actual load-bearing physics chain remains the same:

```text
charge conservation
-> theta_eq target
-> Delta G_eff = Delta G_a - chi A
-> k(G,T,psi)
-> L_q
-> A_L(lambda;T,psi)
-> exponential spectrum kernel integral
-> dQ_ext/dV_n
```

v5 changes are narrow and publication-facing:

1. It removes process/history labels from the manuscript body.
2. It neutralizes version-specific validation tags.
3. It replaces the undefined `K_\lambda` shorthand with the already-established explicit exponential kernel.
4. It converts the internal audit table into a paper-style assumption/validation status table.

## What v5 Improved Over v4

### 1. Version labels no longer leak into manuscript prose

v4 used `DQ-v3-1` and `DQ-v3-2` in the body. v5 replaces them with neutral validation gate labels:

- `VG-1`: target shape is data-determined.
- `VG-2`: Refs 6/7 Plan A closure requires Fredholm/Volterra applicability validation.

This is a manuscript-cleanliness improvement, not a physics change.

### 2. Internal workflow labels were removed

v4 contained process-facing labels:

- `Codex 산출물과의 대조`
- `AGP`
- `사용자 2026-05-28`
- `Grounding 감사 (AGP self-check)`
- table status `통과`

v5 rewrites these into paper-facing statements such as `Validation rule`, `smooth-only convention`, and `Assumption and validation status`.

This matches the project rule that LaTeX manuscript body should contain theory and interpretation, while phase/audit history belongs in `Codex\results`.

### 3. `K_\lambda` shorthand was correctly expanded

v4 had:

```latex
\int A_L(\lambda)K_\lambda\,d\lambda
```

v5 has:

```latex
\int_0^\infty A_L(\lambda;T,\psi)\lambda^{-1}
\exp[-(q-q_a)/\lambda]\,d\lambda
```

This is an improvement because the manuscript no longer introduces an undefined kernel symbol in the physical chain. The expanded expression is consistent with equation `\eqref{eq:kernel_integral}` and the general kernel definition `\eqref{eq:K_def}`.

### 4. The Plan A/Plan B hierarchy is preserved

v5 does not promote Plan A. It keeps:

- Plan B as conservative theoretical baseline.
- Plan A as candidate analytic compression.
- Refs 6/7 gated by Fredholm/Volterra applicability and M1-M5 checks.

The replacement of `DQ` with `GATED` is cleaner and more paper-facing.

## What Did Not Change

The following core equations and sections are unchanged in substance:

- charge balance `Q_cell q = Q_bg + Q_p Theta`
- differential charge balance
- smooth equilibrium target and lattice-gas special case
- effective barrier `Delta G_eff = Delta G_a - chi A`
- Eyring rate expression
- single-mode residual ODE in `q`
- `L_q = |I|/(Q_cell k)`
- barrier-to-length exponential mapping
- spectrum definition `A_L(lambda;T,psi)`
- central kernel integral
- Volterra-type self-consistent structure
- Plan B residual/length/tail equations
- ICA mapping `dQ_ext/dV_n`
- `T/psi` spectrum-shift interpretation
- falsification protocol and non-identifiability warning

## Remaining Non-Blocking Notes

### N1 — `Grounding` theorem environment remains

The theorem name `Grounding` remains at the preamble and in the smooth-only box. This is not a process-history issue by itself; it functions as a manuscript label for assumption grounding. It is different from v4's `Grounding 감사 (AGP self-check)`, which v5 removed.

### N2 — Refs 6/7 audit remains not re-run

This comparison did not reopen the user's PDF or the original Refs 6/7 papers. Therefore Plan A remains correctly gated.

### N3 — PDF still not compiled

`xelatex` is not available in the current environment, so no PDF compile was performed.

## Recommendation

Keep v5 as the current Chapter 1 candidate.

No immediate repair is required from this v5-v4 comparison. The next meaningful work is either:

- compare v5 against Claude's latest Chapter 1 output if the user wants another external contrast, or
- run the Refs 6/7 source audit before attempting to strengthen Plan A.
