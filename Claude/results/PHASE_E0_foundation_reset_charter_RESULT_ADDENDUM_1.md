# Charter Addendum 1 — Session Purpose And Writing Precision Standard

**Date**: 2026-05-28
**Format**: [[feedback_document_protection_addendum_pattern]] §"Addendum"
**Supersedes**: nothing (Charter body unchanged)
**Amends**: `Claude/results/PHASE_E0_foundation_reset_charter_RESULT.md` — adds §10 (Session Purpose) and §11 (Writing Precision Standard) as new normative sections; extends Charter §6 (Audit Dim #11) Pass 1 keyword list and reporting requirements.
**Authority**: User statement 2026-05-28 verbatim.

## Reason

User verbatim 2026-05-28:

> "내가 이 세션에 바라는거 구치화
>  1. 피팅 솔버 코드 구축 X
>  2. 흑연의 ICA 즉 dQdV를 해석하는 이론적 배경을 작업
>  3. 논리 전개를 가다듬어서 가능하면 논문이나 특허로 발전시킬까 고민중
>  4. 산출물은 원본 처럼 가능하면 모든 수식 전개의 논리적 비약이 없고, 생략 없이
>     모든 과정을 대학교 학부생 수준의 지식으로도 그 논리 전개 과정을 따라갈 수
>     있게 정리해주길 바라고 있다. 참고하라."

These 4 items together upgrade the Charter from "structural correctness" to **academic-publication-grade derivational completeness**. Item 4 in particular imposes a precision standard that the existing Charter §6 audit Dim #11 (system-fidelity) does not enforce.

## §10. Session Purpose (New)

The Chapter 1 Rebuild produces a document with the following four purposes simultaneously satisfied.

| # | Purpose | Status in Charter §1-§9 | Status in this Addendum |
|---|---|---|---|
| 10.1 | No fitting solver code is built in this session. | Implicit (Phase G deferred). | **Explicit: out of scope.** |
| 10.2 | The deliverable is the theoretical foundation for interpreting the graphite ICA `dQ/dV` (and DVA `dV/dQ`) curve. | Implicit (Charter §1 objective). | **Explicit primary deliverable type.** |
| 10.3 | The exposition is to be refined to a level potentially developable into a journal article or patent. | Not stated. | **Explicit precision target.** |
| 10.4 | Every equation derivation must (a) have no logical jump, (b) omit no intermediate step, and (c) be followable by a reader with undergraduate-level knowledge in electrochemistry, thermodynamics, and calculus. | Not stated. | **Explicit writing precision standard (§11 below).** |

## §11. Writing Precision Standard (New, Normative)

### 11.1 No-logical-jump rule

Every equation `(B)` in the new Chapter 1 must be obtained from one or more preceding equations `(A_1, A_2, ..., A_k)` and explicitly named identities, definitions, or assumptions, such that the textual prose between `(A_i)` and `(B)` contains every algebraic, calculus, or substitution step required for the reader to verify the transition.

A logical jump is defined as any of:

- Substituting a definition without stating which definition is substituted.
- Applying an identity (algebraic, calculus chain-rule, integration-by-parts, mean-value theorem, etc.) without naming it.
- Combining two intermediate results without stating the combination order.
- Stating a final form without showing the intermediate algebra.
- Omitting a sign-handling step or a dimensional check at a transition.

### 11.2 No-omission rule

The derivation chain from a definition to a working equation must list every intermediate equation. Compact summary equations may appear at section endings as "summary of derivation", but the full derivation chain must precede the summary.

Specifically, the following intermediate steps must never be omitted:

- Variable substitution (state which variable is substituted with what expression).
- Integration step (state the variable of integration, limits, and integration technique).
- Differentiation step (state which variable, chain rule applications if any).
- Limit-taking step (state the limit form and what it recovers).
- Dimensional check at the start and end of each derivation block (state both sides' SI units).

### 11.3 Undergraduate-level prose requirement

The reader is assumed to have:

- Undergraduate electrochemistry (Nernst equation, electrode potential, Butler-Volmer at the conceptual level).
- Undergraduate thermodynamics (Gibbs free energy, chemical potential definition, entropy basics).
- Undergraduate calculus (single-variable integration and differentiation, basic ODE concepts, change-of-variable).
- Basic linear algebra (vectors, integration over distributions).
- **No** advanced functional analysis, **no** advanced PDE theory, **no** stochastic calculus assumed.

When a concept requires more advanced background (e.g., Fredholm integral equation of the second kind), the text must:

1. Define the term in undergraduate-accessible language at first use.
2. Cite the introductory reference.
3. Defer the rigorous functional-analysis treatment to a footnote or a clearly-marked "advanced note" mdframed, never assuming the reader has read it.

### 11.4 Charter §6 Audit Dim #11 extension

Charter §6 Pass 1 keyword scan is extended with the following \emph{narrative-completeness} keywords / structural checks:

| Check | Pass criterion |
|---|---|
| "trivially", "obviously", "clearly" appearing alone before an equation | FAIL — replace with an explicit derivation step. |
| "It can be shown that" without subsequent derivation | FAIL — derive or cite source. |
| Equation transition with no prose between two displayed equations | WARN — add at least one sentence describing the manipulation. |
| Definition introduced inside a derivation block without being already in §2 notation table | FAIL — pre-declare in §2 or in a dedicated definition box. |
| Dimensional check absent at the start of a derivation block | WARN. |
| Dimensional check absent at the end of a derivation block | WARN. |
| Limit recovery (e.g., `ε → 0`, Dirac comb, isothermal) claimed without explicit computation | WARN — show the limit computation. |

### 11.5 Reporting requirement for each phase Result document

Each subsequent phase Result (Phase E4 onward) must include a `§"Writing precision audit"` section listing:

- Every derivation block in the phase's added LaTeX content.
- For each block: the starting equation (or definition), the ending equation, the count of intermediate steps shown, the count of dimensional checks performed, and the count of advanced-concept footnotes / mdframed used.
- Any §11.4 FAIL or WARN occurrences and their resolution.

## §12. Backward Application Note

This Addendum is forward-applicable from Phase E4 onward. Phases E0-E3 deliverables are NOT retroactively re-audited under §11; however:

- The Charter Anti-Pattern List (§2) and Forbidden-Pattern List (§4) already enforce structural correctness.
- Phase E2 §1 and §2, Phase E3 §3 and §4 are governance / notation / conceptual setup, not derivation chains, so §11.1–§11.3 do not produce backlog.
- Phase E4 §5 (charge balance derivation) is the first phase where §11 applies fully.

## §13. Effect On Master Roadmap

- Master roadmap `Claude/plans/2026-05-27-anode-fit-chapter1-rebuild-master-roadmap.md` is not modified. The session purpose (§10) is consistent with the master roadmap's existing Non-goals (item 4 "Do not implement numerical solvers in this roadmap"). The writing precision standard (§11) is a tightening of audit Dim #11, fully compatible with master roadmap Phase E4 onward.
- Test Plan T1-T20 in master roadmap is not modified; the new §11 reporting requirement is an addition to each phase Result, not a Test Plan revision.

## §14. Re-validation

- Phases E0-E3 Result audits remain valid per [[feedback_phase_audit_workflow]] Pass 3 — no regression introduced.
- Chapter 1 v0.1 source file (`Claude/docs/graphite_ica_chapter1_v0.1.tex`) §1-§4 content is preserved; §5 onward will be written under the §11 standard.

## §15. Ledger Update

Add a row to `Claude/results/PHASE_E_F_EXECUTION_LEDGER.md` Updates table:

| 2026-05-28 | Charter Addendum 1 | User 5-28 4 가지 요구 (피팅 솔버 X, ICA 이론적 배경, 논문/특허 수준, 학부생 수준 친절성 + 논리적 비약 0 + 생략 0) 영구 반영. Charter §10 (Session Purpose) + §11 (Writing Precision Standard) 신설. Phase E4 부터 inline 적용. |
