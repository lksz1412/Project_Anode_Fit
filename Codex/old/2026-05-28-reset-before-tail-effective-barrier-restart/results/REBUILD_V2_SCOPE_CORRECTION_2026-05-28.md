# Rebuild v2 Scope Correction

Project: `D:\Projects\Project_Anode_Fit`

Date: 2026-05-28

Source: user clarification in current Codex thread

## Corrected User Goal

The current task is not to implement a numerical solver, fitting code, or data-fitting pipeline.

The current task is to build the theoretical and mathematical background for interpreting graphite ICA / dQdV. The intended output is a Chapter 1-level document whose equation development is logically continuous, with no unexplained jumps, and whose derivation can be followed by a university undergraduate reader.

The work may later be developed into a paper or patent, so the priority is rigor and traceable logical development, not software execution.

## Implications For Current Artifacts

| Artifact / Concept | Correct Handling |
|---|---|
| solver implementation | out of current scope |
| fitting code | out of current scope |
| experimental data fitting | out of current scope |
| direct numerical solver sections | may be retained only as theoretical validation language, not as a requested implementation direction |
| fitting protocol sections | should be reduced or moved out of Chapter 1 if they distract from the theoretical derivation |
| Chapter 1 status | must be judged by derivation completeness, not by implementation readiness |
| refs. 6/7 method | use only to support an integral/self-consistent equation treatment if it helps remove logical circularity |

## Correct Chapter 1 Acceptance Standard

A Chapter 1 complete artifact must:

1. define the measured charge coordinate and ICA/dQdV observable without assuming the desired peak shape;
2. define graphite storage components and transition variables before using them in voltage equations;
3. derive the charge-balance residual before introducing `V_n`;
4. define `V_n` as an implicit root of charge balance, not as an independently prescribed curve;
5. derive equilibrium OCV as a special case of the same charge-balance root;
6. show how self-consistent feedback enters without treating it as a contradiction;
7. if an integral/self-consistent closure is introduced, explain each step and every approximation explicitly;
8. derive `dV/dq`, `dQ/dV`, and related ICA/DVA expressions through visible intermediate steps;
9. explain how graphite ICA peak locations, widths, and areas arise from thermodynamic state transitions and charge balance;
10. avoid claims that require actual numerical fitting, solver traces, or experimental parameter extraction.

## Current Rebuild v2 Status Under Corrected Scope

The existing Phase 014 output should be treated as a structured logical rebuild and source-controlled manuscript scaffold, not as the final Chapter 1 acceptance artifact under the clarified standard.

The current manuscript contains much of the necessary foundation, but it still includes implementation-adjacent sections such as `Direct Solver Definition` and `Fitting Protocol`. Those sections should be rewritten, shortened, or moved out of the Chapter 1 body when producing the user-facing Chapter 1 complete version.

## Next Correct Work Unit

Create a new Chapter 1 completion pass focused only on theoretical derivation:

- working output name: `graphite_ica_chapter1_theory_complete.tex`;
- source basis: corrected ver1, Phase 006 math package, Phase 007 closure contract, and current rebuilt manuscript as reference only;
- remove or demote solver/fitting implementation language;
- expand every derivation step between charge balance, implicit potential, derivative observables, and ICA/dQdV shape interpretation;
- include no implementation plan, no code plan, and no fitted result claims.

## Boundary

Do not start solver construction or fitting-code design unless the user explicitly asks for it in a later task.
