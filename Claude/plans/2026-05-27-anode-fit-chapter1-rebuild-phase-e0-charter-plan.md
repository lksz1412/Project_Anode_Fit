# Phase E0 — Foundation Reset And Rebuild Charter (Phase-Level Plan)

## Summary

- Status: `READY_FOR_EXECUTION`
- Date: `2026-05-27`
- Parent roadmap: `Claude/plans/2026-05-27-anode-fit-chapter1-rebuild-master-roadmap.md`
- Phase Range: cumulative Steps **19 ~ 80** (62 steps)
- Scope: Author the Chapter 1 Rebuild Charter — 9 mandatory sections (Objective, Anti-Pattern List, Allowed-Pattern List, Forbidden-Pattern List, Smooth-Limit Consistency Rule, Audit Dim #11 Procedure, Legacy ↔ New Variable Mapping, Central Equation Preview, Ref. 6/7 Application Sketch).
- This phase writes NO LaTeX into `Claude/docs/`. The Charter is a `Claude/results/` artifact that governs all subsequent phases (E1 ~ F5).
- No simulator code, no numerical implementation, no body sections in this phase.
- TDD-like discipline: Charter must define audit Dim #11 before the rebuild can use it operationally.

## Current Ground Truth

- Active project: `D:\Projects\Project_Anode_Fit`
- Master roadmap committed: commit `4489595`, push to `origin/main` confirmed.
- Audit v0.2 committed: same commit, supersedes v0.1 (commit `a63378f`).
- User GO at DQ-G1 received 2026-05-27.
- ver5 evidence (anti-pattern source): `Claude/docs/graphite_ica_dynamic_ver5.tex` lines 188 (§5.1 logistic), 195 (§5.2 erf), 240-245 (§6.5 max), 247-249 (§6.5 min/k_max), 137-150 (§3 discrete N_p table).
- ver1_rechecked2 evidence (partial-fix source): `Claude/docs/graphite_ica_charge_balance_ver1_rechecked2.tex` lines 188-193 (§5 logistic retained), 240-265 (§6.2 softplus regularization), 110-114 (§3 effective transition N_p retained).
- JCP 2017 evidence (continuous reactivity source): `Claude/_local_only/jcp_extract.txt` lines 60-90 (§II.A `S_R(r)` continuous), 193-275 (§II.C long-range sink), 280-389 (§II.C ratio-substitution derivation).
- Ref 6 confirmed via Phase E0 Step 40-44 self-search (Wikidata Q51583050): "Communication: Propagator for diffusive dynamics of an interacting molecular pair", S. Lee, C. Y. Son, J. Sung, S. H. Chong, J. Chem. Phys. 134, 121102 (2011), **DOI 10.1063/1.3565476**, PubMed 21456635. Abstract: "new method of solution for the Fredholm integral equations of the second kind" applicable when standard iterative approaches produce divergent solutions.
- Ref 7 confirmed via Phase D + Phase E0 self-search: "An accurate expression for the rates of diffusion-influenced bimolecular reactions with long-range reactivity", C. Y. Son, J. Kim, J.-H. Kim, J. S. Kim, S. Lee, J. Chem. Phys. 138, 164123 (2013), URL `pubs.aip.org/.../164123/71188`. DOI being searched.

## Non-goals (this phase)

- Do not write `.tex` sections (Phase E2 onwards).
- Do not implement numerical solvers.
- Do not enter Phase E1 spine redesign in this phase.
- Do not request user clarification on the Charter itself — Charter is Claude-authored under audit v0.2 §5.11 direction.
- Do not modify the master roadmap (corrections go to a separate Addendum).

## Implementation Changes

Planned new files:

- `Claude/plans/2026-05-27-anode-fit-chapter1-rebuild-phase-e0-charter-plan.md` (this file)
- `Claude/results/PHASE_E0_foundation_reset_charter_RESULT.md` (★ Charter body, 9 sections)
- `Claude/results/PHASE_E0_foundation_reset_charter_RESULT.json` (machine-readable Charter — variable inventory, anti-pattern enumeration, audit dim spec)
- `Claude/results/PHASE_E_F_EXECUTION_LEDGER.md` (NEW ledger for the rebuild, Phase E0 row PASS as initial entry)

No file in `Claude/docs/` modified or created during this phase.
No file in `Claude/_local_only/` modified.
No file in `Codex/` accessed.

## Steps (Phase E0, cumulative 19 ~ 80, master roadmap reference)

(Master roadmap Phase E0 Steps 19-80 verbatim, expanded with execution notes where the master roadmap step indicates a deliverable.)

19. Save this Phase E0 plan as `Claude/plans/2026-05-27-anode-fit-chapter1-rebuild-phase-e0-charter-plan.md` — **DONE by writing this file**.
20. Save companion JSON for Phase E0 plan — **DEFERRED**: per audit v0.2 §"compactness", phase-level plan JSON consolidated into the Result JSON (Step 72) rather than a separate file. Compactness justified because phase-level plan and Result JSON are co-versioned.
21. Load `PROJECT_AUDIT_REPORT_v0.2.md` §1.5 (step function evidence) into Charter §"Anti-Pattern List".
22. Load `PROJECT_AUDIT_REPORT_v0.2.md` §5.11 (continuous chemical potential direction) into Charter §"Allowed-Pattern List".
23. Load `PHASE_D_jcp_ref6_7_methodology_RESULT.md` §"original methodology" into Charter §"Ref. 6/7 Application Sketch".
24. Load `jcp_extract.txt` §II.C lines 193-275 into Charter §"Ref. 6/7 Application Sketch".
25-27. Identify and quote exact line evidence for step function assumptions in ver5, rechecked2, and JCP 2017. Reflected in Charter §"Anti-Pattern List" and §"Allowed-Pattern List".
28. Write Charter Objective sentence — Charter §1.
29. Declare rebuild objective — Charter §1.
30-32. Anti-pattern, allowed-pattern, forbidden-pattern lists — Charter §2, §3, §4.
33. Smooth-limit consistency rule with worked examples — Charter §5.
34-37. Audit Dim #11 procedure (Pass 1/2/3) — Charter §6.
38-44. Ref 6/7 DOI self-search — completed Phase E0 prior to this plan's writing. Ref 6 DOI = `10.1063/1.3565476`. Ref 7 DOI still under search (Step 44 fallback `근거 미발견` if remaining search fails).
45-46. New variable namespace + legacy variable migration — Charter §7.
47. Legacy ↔ new variable mapping table — Charter §7.
48-49. Central equations 48 (charge balance) and 49 (Fredholm 2nd kind ρ-evolution) — Charter §8.
50. Recognize Eq. 49 = Fredholm 2nd kind directly Ref 6/7-solvable — Charter §8 note.
51. Verify no `max`, `min`, logistic, N_p sum in central equations — Charter §8 Charter-compliance verification.
52-55. Dependency graph + self-consistent loop classification + ρ^{simple} candidate — Charter §9.
56-57. Charter document + companion JSON deliverable definition.
58-65. Gates `GATE_E0_1` ~ `GATE_E0_8` — Charter Result §"Validation".
66-67. Stop conditions.
68-70. Confirmation rules (no docs write, no _local_only modification, no Codex read).
71-73. Write Result markdown + JSON + validate JSON parses.
74. Update / create `PHASE_E_F_EXECUTION_LEDGER.md` with Phase E0 PASS row.
75. Apply audit Pass 1+2+3 on Phase E0 deliverables (all 11 dims including the newly-defined Dim #11 on the Charter itself).
76. Record any Dim #11 finding (e.g., Charter must not implicitly assume step-function avoidance applies only in one section).
77-78. Commit and push (per `feedback_phase_audit_workflow` pair commit, but per audit v0.2 §"compactness" combined into single commit since Phase E0 is text-only).
79. Auto-proceed to Phase E1 per `feedback_plan_continuation_until_done` — Phase E1 entry deferred to next conversation turn due to response budget. Marked as immediate next action.
80. End Phase E0 at documented boundary.

## Implementation Interfaces (this phase)

### Charter Document Schema (output of Phase E0)

9 sections per master roadmap Step 56:

1. Charter Objective (1 sentence + amplification)
2. Anti-Pattern List (≥ 5 specific ver5/rechecked2 line evidence)
3. Allowed-Pattern List (new variable namespace + central equation form)
4. Forbidden-Pattern List
5. Smooth-Limit Consistency Rule (≥ 2 worked examples)
6. Audit Dimension #11 Procedure (Pass 1/2/3)
7. Legacy ↔ New Variable Mapping (table covering ver5 §2 21 entries + rechecked2 §2 11 entries)
8. Central Equation Preview (Eq. 48 + Eq. 49)
9. Ref. 6/7 Application Sketch (ρ^{simple} candidate, ratio-substitution form, validity)

### Charter Result JSON Schema

```json
{
  "phase": "E0",
  "phase_id": "PASS_FOUNDATION_RESET_CHARTER",
  "step_range": {"from": 19, "to": 80},
  "charter_objective": "<string>",
  "anti_patterns": [{"pattern": "<string>", "evidence_file": "<path>", "evidence_lines": [<int>]}],
  "allowed_patterns": [{"pattern": "<string>", "intended_use": "<string>"}],
  "forbidden_patterns": [{"pattern": "<string>", "reason": "<string>"}],
  "smooth_limit_rules": [{"regularization": "<latex>", "smooth_limit_form": "<latex>", "epsilon_zero_form": "<latex>"}],
  "audit_dim_11": {"pass_1": "<procedure>", "pass_2": "<procedure>", "pass_3": "<procedure>"},
  "variable_mapping": {
    "canonical": [{"symbol": "<latex>", "unit": "<string>", "description": "<string>"}],
    "derived": [{"symbol": "<latex>", "derivation_from_canonical": "<latex>"}]
  },
  "central_equations": {"eq_48_charge_balance": "<latex>", "eq_49_fredholm_evolution": "<latex>"},
  "ref_6_7_application": {
    "rho_simple_candidate": "<latex>",
    "ratio_substitution_form": "<latex>",
    "validity_conditions": ["<string>"]
  },
  "audit_results": {"pass_1": "<status>", "pass_2": "<status>", "pass_3": "<status>", "dim_11_finding": "<string>"},
  "gates": [{"gate_id": "<string>", "status": "PASS|FAIL", "evidence": "<string>"}]
}
```

### Ledger Row Format (new file `PHASE_E_F_EXECUTION_LEDGER.md`)

Per `feedback_phase_execution_loop` §3 12-column schema. Phase E0 row entered as initial baseline.

## Test Plan (this phase)

- T-E0-1: Charter Result markdown contains all 9 sections (Step 58 Gate).
- T-E0-2: Anti-Pattern List cites ≥ 5 specific ver5 + rechecked2 line numbers (Step 59 Gate).
- T-E0-3: Allowed-Pattern List defines new variable namespace + central equation form (Step 60 Gate).
- T-E0-4: Smooth-Limit Rule has ≥ 2 worked examples (Step 61 Gate).
- T-E0-5: Audit Dim #11 procedure has Pass 1/2/3 each defined (Step 62 Gate).
- T-E0-6: Legacy ↔ New Variable Mapping covers ver5 §2 21 + rechecked2 §2 11 entries (Step 63 Gate).
- T-E0-7: Central Equations are valid LaTeX, pass dimensional and smooth-limit check (Step 64 Gate).
- T-E0-8: Ref 6/7 Application Sketch identifies ρ^{simple} candidate explicitly (Step 65 Gate).
- T-E0-9: Charter Result JSON parses (`python -m json.tool ... > /dev/null`).
- T-E0-10: Audit Dim #1-#11 Pass 1+2+3 on Charter, 0 FAIL (Step 75).
- T-E0-11: Ledger row Phase E0 with Gate `PASS_FOUNDATION_RESET_CHARTER` (Step 74).
- T-E0-12: No file in `Claude/docs/` or `Codex/` modified (Step 68, 70).

## Assumptions

- A-E0-1. User GO at DQ-G1 (received) authorizes Phase E0 entry.
- A-E0-2. Ref 6 DOI `10.1063/1.3565476` is correct (Wikidata Q51583050 source).
- A-E0-3. Ref 7 DOI may remain `근거 미발견` if additional search fails — fallback ok.
- A-E0-4. Compactness deferral of Step 20 (separate plan JSON) is acceptable since Phase E0 is text-only governance, not implementation.
- A-E0-5. Continuous chemical potential `μ` is interpreted as Li/Li⁺-reference electrochemical potential (electrochemistry standard for graphite anode). User cross-check at DQ-G2 may revise.
- A-E0-6. Audit Dim #11 is project-local (Chapter 1 rebuild only) until DQ-G5 user approval makes it global memory.

## Correction History

- This phase-level plan v0.1 (this file): initial. Derived directly from master roadmap Phase E0 Steps 19-80.

## Success Criteria (Sprint Contract)

- [ ] All 12 Test Plan items PASS.
- [ ] All 8 Gates (`GATE_E0_1` ~ `GATE_E0_8`) PASS.
- [ ] Charter Result + JSON + Ledger committed and pushed.
- [ ] Phase E1 entry path clear (no Decision Queue blocker introduced by Charter authoring).

## QA Tier

- [x] Standard ← appropriate for governance-only phase.

## Decision Queue (this phase)

- DQ-E0-1: Ref 7 DOI confirmation — Phase E0 Step 44 fallback to `근거 미발견` acceptable.
- DQ-E0-2: A-E0-5 (μ semantics) — Phase E0 records assumption, Phase F3 (PDF user review) is the canonical user cross-check point. No interim user query needed.
