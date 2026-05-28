# Tail Effective Barrier Chapter 1 Restart Plan

> For agentic workers: REQUIRED SUB-SKILL: use `superpowers:executing-plans` for inline execution, and use `superpowers:subagent-driven-development` only if the user explicitly asks for subagents. Steps use checkbox syntax for tracking.

**Goal:** Rebuild Chapter 1 from zero-active-artifact state as a logically complete theoretical derivation for graphite LIB ICA tail behavior governed by temperature and electrode-potential-dependent effective barrier lowering.

**Architecture:** The new work starts from original source files, not from the previous draft chain. Previous Codex outputs are archived under `Codex\old` and may be opened only as historical context, not as active proof. The rebuilt manuscript will proceed from charge balance to internal potential, driving voltage, affinity, effective barrier, relaxation in charge coordinate, tail-length expression, and ICA/DVA mapping.

**Tech Stack:** LaTeX manuscript files, Markdown phase plans/results/ledgers, PowerShell file/read verification, optional PDF text/OCR extraction only when needed and explicitly recorded.

---

## User Core Problem Statement

This section is the fixed starting point of the restart. Every phase, derivation, audit, and manuscript section must be checked against this problem statement before it is treated as valid.

사용자가 제시한 핵심 문제는 다음과 같다.

- LIB graphite ICA 분석에서 관찰되는 대상은 상변이 피크 자체만이 아니라, 피크 뒤쪽 tail의 개형이다.
- 이 tail은 온도와 현 시점의 극판 전위 상태에 따라 달라진다.
- 관찰상 낮은 온도에서는 tail이 길게 늘어지고, 높은 온도에서는 tail이 상대적으로 짧게 끝난다.
- 단순히 온도에 의해 약간 넓어진 Gaussian-like equilibrium peak가 나타난 뒤 끝나는 그림만으로는 이 현상을 설명하기 어렵다.
- 따라서 thermal barrier 외에, 현재 극판 전위 상태가 상변이 진행의 effective barrier를 낮추는 효과가 있다고 보고 그 논리를 수식으로 정립해야 한다.
- 핵심 식은 나중에 피팅에 사용할 수 있어야 하지만, 지금 작업은 피팅 코드, solver 구축, parameter extraction이 아니라 이론적 배경과 논리 전개이다.
- 피크 면적은 추후 피팅/용량 분해의 영역이며, 이번 Chapter 1의 중심 논증은 tail 거동과 effective barrier이다.
- 최종 문건은 가능한 한 모든 수식 전개가 생략 없이 이어져야 하며, 대학교 학부생 수준의 지식으로도 논리 전개를 따라갈 수 있어야 한다.
- 논리 비약은 허용하지 않는다. 전위 정의, 장벽 정의, 속도식, 진행률 방정식, tail scale, ICA/DVA 연결 사이의 모든 의존관계를 명시해야 한다.
- 기존 산출물을 고쳐 살리는 방식이 아니라, 기존 원천 파일은 참고하되 active manuscript는 처음부터 다시 작성한다.

Scope-drift rule:

- If a step primarily optimizes fitting, solver design, peak area, branch hysteresis, heat coupling, or code implementation before the tail-effective-barrier derivation is complete, it is out of scope for this restart.
- If a derivation skips from observed ICA peak shape directly to a fitted peak function without deriving `Delta G_eff`, `k_j`, `d xi_j/dq`, and `ell_q,j`, it fails the logic gate.
- If a manuscript section cannot be explained to an undergraduate reader through definitions and intermediate equations, it must be rewritten before being accepted.

## Summary

This plan restarts the project after the previous broad Chapter 1 attempt was found to over-center peak area, solver/fitting concerns, and inherited artifacts. The active task is now narrowed to the theory of ICA peak-tail shape in graphite anodes.

The central observation to explain is:

- in LIB graphite ICA, the peak tail changes with temperature and present electrode potential state;
- low temperature shows a longer tail;
- higher temperature shows a shorter tail;
- a simple equilibrium Gaussian/logistic peak is insufficient;
- beyond the thermal barrier, present electrode potential can lower the effective transition barrier;
- the desired output is a logically complete theoretical derivation usable later for fitting, not a fitting implementation.

The rebuilt Chapter 1 must derive the tail behavior through:

```text
charge coordinate
  -> charge balance
  -> internal potential V_n
  -> apparent and driving voltages
  -> affinity A_j
  -> intrinsic thermal barrier Delta G_a,j(T)
  -> effective barrier Delta G_eff,j^+
  -> rate k_j
  -> phase-progress relaxation d xi_j / dq
  -> tail decay scale ell_q,j
  -> ICA/DVA observable mapping
```

Execution rule:

- Do not stop at phase boundaries just to report.
- Continue through the next phase automatically unless a real user decision is needed.
- Still write phase result files and ledger rows so the work can be resumed after context compression.
- Phase and step ranges are minimum required coverage, not a hard maximum. If extra source checks, derivation passes, audit loops, or repair phases are needed to complete the logic, add them and record the reason, result path, gate, and next step in the ledger.
- After context compaction or session recovery, do not rely on conversation memory. Re-open this plan, locate the relevant phase result and ledger entry, verify the saved record directly, and continue from that evidence.

## Current Ground Truth

### Active Workspace

| Item | State |
|---|---|
| Active project | `D:\Projects\Project_Anode_Fit` |
| Codex workspace | `D:\Projects\Project_Anode_Fit\Codex` |
| Active plans directory | `D:\Projects\Project_Anode_Fit\Codex\plans` |
| Active results directory | `D:\Projects\Project_Anode_Fit\Codex\results` |
| Claude boundary | `D:\Projects\Project_Anode_Fit\Claude` must not be modified |
| Original source boundary | original download folder is read-only source unless user explicitly asks otherwise |

### Reset State

Previous Codex plans and results were moved to:

`D:\Projects\Project_Anode_Fit\Codex\old\2026-05-28-reset-before-tail-effective-barrier-restart`

Archive contents confirmed at reset time:

| Archive subfolder | Count |
|---|---:|
| `plans` | 7 files |
| `results` | 51 files |
| `work` | 0 items at the time of archive |

Active `Codex\plans` retains only:

`D:\Projects\Project_Anode_Fit\Codex\plans\phase_planning_operations_guide.md`

Active `Codex\results` is empty at restart.

### Source Files To Re-Establish From Scratch

| Source | Path | Required coverage |
|---|---|---|
| historical ver1-ver5 stack | `D:\Projects\Project_BatteryData_Display_임시저장소\새 폴더\drive-download-20260527T100231Z-3-001\graphite_ica_dynamic_ver5.tex` | full read with line ranges; then focused extraction |
| corrected ver1 charge-balance source | `D:\Projects\Project_BatteryData_Display_임시저장소\새 폴더\drive-download-20260527T100231Z-3-001\graphite_ica_charge_balance_ver1_rechecked2.tex` | full read with line ranges; then focused extraction |
| user paper PDF | `D:\Projects\Project_BatteryData_Display_임시저장소\새 폴더\drive-download-20260527T100231Z-3-001\JCP_147(14)_144111_(2017) - Effects of external electric field.pdf` | inspect bibliography and ref. 6, 7 method context before importing methodology |

### Already Known But Must Be Re-Proved In This Restart

These are not accepted as completed until re-established from source in new phase results:

- `graphite_ica_dynamic_ver5.tex` contains a useful spine: effective barrier to rate to phase-progress lag to ICA/DVA tail.
- `graphite_ica_charge_balance_ver1_rechecked2.tex` fixes the self-consistent voltage issue by making `V_n` a charge-balance root.
- The correct active direction is tail/effective barrier theory, not peak-area-centered theory.

## Phase Range

| Phase | Name | Step range | Primary output | Gate |
|---|---|---:|---|---|
| Phase 001 | Restart Baseline And Source Inventory | 1-12 | `PHASE_001_RESTART_BASELINE_RESULT.md` | active workspace and sources confirmed |
| Phase 002 | Full TeX Read Coverage | 13-26 | `PHASE_002_FULL_TEX_READ_RESULT.md` | both `.tex` files read with coverage table |
| Phase 003 | Source Evidence Extraction | 27-42 | `PHASE_003_SOURCE_EVIDENCE_INDEX.md` | line-grounded evidence map created |
| Phase 004 | PDF Ref. 6/7 Method Extraction | 43-58 | `PHASE_004_REF6_REF7_METHOD_RESULT.md` | ref. 6/7 method context verified or marked unavailable |
| Phase 005 | Problem Definition And Scope Contract | 59-72 | `PHASE_005_TAIL_SCOPE_CONTRACT.md` | peak-area/solver/fitting non-goals locked |
| Phase 006 | Notation And Dependency Bible | 73-90 | `PHASE_006_NOTATION_DEPENDENCY_BIBLE.md` | variables and dependencies are non-circular or explicitly implicit |
| Phase 007 | Effective Barrier Derivation | 91-112 | `PHASE_007_EFFECTIVE_BARRIER_DERIVATION.md` | barrier equation passes sign, unit, and role checks |
| Phase 008 | Tail Decay Derivation | 113-136 | `PHASE_008_TAIL_DECAY_DERIVATION.md` | `ell_q,j` derived without skipped steps |
| Phase 009 | ICA/DVA Observable Mapping | 137-158 | `PHASE_009_ICA_DVA_MAPPING.md` | `d xi/dq` to `dQ/dV` mapping is charge-balance consistent |
| Phase 010 | Barrier Distribution Extension | 159-176 | `PHASE_010_BARRIER_DISTRIBUTION_EXTENSION.md` | distribution is kinetic, not threshold completion |
| Phase 011 | Manuscript Draft From Scratch | 177-206 | `graphite_ica_tail_effective_barrier_theory_chapter1.tex` | draft includes only verified derivations |
| Phase 012 | Ralph Wiggum Logic Verification Loop | 207-238 | `PHASE_012_RALPH_WIGGUM_LOGIC_AUDIT.md` | no blocking logical gaps remain or gaps are explicitly listed |
| Phase 013 | Final Packaging And Handover | 239-252 | `PHASE_013_FINAL_HANDOVER.md` and ledger | outputs trace to source and gates |

## Non-goals

- Do not write fitting code.
- Do not build a numerical solver.
- Do not make PDF generation a required gate.
- Do not center the theory on peak area.
- Do not alter original `.tex`, PDF, image, or Python source files in the download folder.
- Do not modify `D:\Projects\Project_Anode_Fit\Claude`.
- Do not use previous Codex outputs as active evidence unless the result explicitly labels them as historical context.
- Do not import PDF ref. 6/7 methodology until the bibliography and method context are actually checked.
- Do not introduce branch/hysteresis Chapter 5 mechanics into Chapter 1 except as a future extension note.
- Do not claim `READ_FULL`, `PASS`, or `논리 검증 완료` without fresh evidence in the current restart result chain.

## Implementation Changes

### Create

| Path | Purpose |
|---|---|
| `D:\Projects\Project_Anode_Fit\Codex\plans\2026-05-28-tail-effective-barrier-restart-plan.md` | canonical restart plan |
| `D:\Projects\Project_Anode_Fit\Codex\plans\2026-05-28-tail-effective-barrier-restart-plan.json` | machine-readable phase/step metadata |
| `D:\Projects\Project_Anode_Fit\Codex\results\PHASE_001_RESTART_BASELINE_RESULT.md` | reset/source inventory result |
| `D:\Projects\Project_Anode_Fit\Codex\results\PHASE_002_FULL_TEX_READ_RESULT.md` | full `.tex` read coverage |
| `D:\Projects\Project_Anode_Fit\Codex\results\PHASE_003_SOURCE_EVIDENCE_INDEX.md` | line-grounded evidence index |
| `D:\Projects\Project_Anode_Fit\Codex\results\PHASE_004_REF6_REF7_METHOD_RESULT.md` | PDF ref. 6/7 method extraction |
| `D:\Projects\Project_Anode_Fit\Codex\results\PHASE_005_TAIL_SCOPE_CONTRACT.md` | problem and non-goal contract |
| `D:\Projects\Project_Anode_Fit\Codex\results\PHASE_006_NOTATION_DEPENDENCY_BIBLE.md` | notation and dependency contract |
| `D:\Projects\Project_Anode_Fit\Codex\results\PHASE_007_EFFECTIVE_BARRIER_DERIVATION.md` | effective barrier derivation |
| `D:\Projects\Project_Anode_Fit\Codex\results\PHASE_008_TAIL_DECAY_DERIVATION.md` | tail-length derivation |
| `D:\Projects\Project_Anode_Fit\Codex\results\PHASE_009_ICA_DVA_MAPPING.md` | observable mapping derivation |
| `D:\Projects\Project_Anode_Fit\Codex\results\PHASE_010_BARRIER_DISTRIBUTION_EXTENSION.md` | distribution extension |
| `D:\Projects\Project_Anode_Fit\Codex\results\graphite_ica_tail_effective_barrier_theory_chapter1.tex` | rebuilt Chapter 1 manuscript |
| `D:\Projects\Project_Anode_Fit\Codex\results\PHASE_012_RALPH_WIGGUM_LOGIC_AUDIT.md` | logic-loop audit |
| `D:\Projects\Project_Anode_Fit\Codex\results\PHASE_001_013_RESTART_EXECUTION_LEDGER.md` | phase ledger |
| `D:\Projects\Project_Anode_Fit\Codex\results\PHASE_013_FINAL_HANDOVER.md` | final handover |

### Preserve

| Path | Rule |
|---|---|
| `D:\Projects\Project_Anode_Fit\Codex\AGENTS.md` | read-only unless user asks to change project rules |
| `D:\Projects\Project_Anode_Fit\Codex\plans\phase_planning_operations_guide.md` | active operational guide |
| `D:\Projects\Project_Anode_Fit\Codex\old\2026-05-28-reset-before-tail-effective-barrier-restart` | previous work archive; do not edit except to add an archive manifest if needed |

## Phase 001 — Restart Baseline And Source Inventory

Purpose: confirm the clean restart state, archive location, source file metadata, and active workspace before any scientific derivation resumes.

Inputs:

- `D:\Projects\Project_Anode_Fit\Codex\AGENTS.md`
- `D:\Projects\Project_Anode_Fit\Codex\plans\phase_planning_operations_guide.md`
- the three source files listed in Current Ground Truth

Steps:

- [ ] Step 1: Verify active project path is `D:\Projects\Project_Anode_Fit`.
- [ ] Step 2: Verify active Codex path is `D:\Projects\Project_Anode_Fit\Codex`.
- [ ] Step 3: Verify previous outputs are under `Codex\old\2026-05-28-reset-before-tail-effective-barrier-restart`.
- [ ] Step 4: Count archived `plans`, `results`, and `work` items.
- [ ] Step 5: Verify active `Codex\plans` contains the operations guide and this restart plan.
- [ ] Step 6: Verify active `Codex\results` contains only new restart artifacts created after this plan.
- [ ] Step 7: Record source file path, size, last write time, and line count/page count.
- [ ] Step 8: Record that original source files will not be modified.
- [ ] Step 9: Record that Claude folder will not be modified.
- [ ] Step 10: Create `PHASE_001_RESTART_BASELINE_RESULT.md`.
- [ ] Step 11: Initialize `PHASE_001_013_RESTART_EXECUTION_LEDGER.md`.
- [ ] Step 12: Gate `PASS_RESTART_BASELINE` only if paths and source inventory are confirmed.

Gate:

- active workspace is cleanly separated from `old`;
- source files exist and are readable;
- no original source file was modified.

## Phase 002 — Full TeX Read Coverage

Purpose: re-read the two `.tex` source files from the beginning in the current restart chain so later reasoning does not rely on archived summaries.

Inputs:

- `graphite_ica_dynamic_ver5.tex`
- `graphite_ica_charge_balance_ver1_rechecked2.tex`

Steps:

- [ ] Step 13: Count total lines for `graphite_ica_dynamic_ver5.tex`.
- [ ] Step 14: Count total lines for `graphite_ica_charge_balance_ver1_rechecked2.tex`.
- [ ] Step 15: Read `graphite_ica_dynamic_ver5.tex` lines 1-400.
- [ ] Step 16: Read `graphite_ica_dynamic_ver5.tex` lines 401-800.
- [ ] Step 17: Read `graphite_ica_dynamic_ver5.tex` lines 801-1200.
- [ ] Step 18: Read `graphite_ica_dynamic_ver5.tex` lines 1201-1600.
- [ ] Step 19: Read `graphite_ica_dynamic_ver5.tex` lines 1601-end.
- [ ] Step 20: Read `graphite_ica_charge_balance_ver1_rechecked2.tex` lines 1-250.
- [ ] Step 21: Read `graphite_ica_charge_balance_ver1_rechecked2.tex` lines 251-end.
- [ ] Step 22: Re-read any truncated or suspicious output ranges with narrower windows.
- [ ] Step 23: Build a read coverage table with file, line range, status, and notes.
- [ ] Step 24: Mark historical ver1-ver5 blocks in `graphite_ica_dynamic_ver5.tex`.
- [ ] Step 25: Create `PHASE_002_FULL_TEX_READ_RESULT.md`.
- [ ] Step 26: Gate `PASS_TEX_READ_FULL` only if every line range is actually covered.

Gate:

- no line range is inferred from search-only output;
- `READ_FULL` is used only for files whose full ranges were actually read.

## Phase 003 — Source Evidence Extraction

Purpose: extract only source-grounded evidence relevant to the corrected tail/effective-barrier direction.

Steps:

- [ ] Step 27: Extract all lines defining the main kinetic spine.
- [ ] Step 28: Extract all lines defining charge balance and internal `V_n`.
- [ ] Step 29: Extract all lines distinguishing `V_n`, `V_{n,app}`, `V_{n,drive}`, and `V_{n,OCV}`.
- [ ] Step 30: Extract all lines defining `xi_j`, `xi_{j,eq}`, logistic/erf equilibrium forms, and equilibrium peak limits.
- [ ] Step 31: Extract all lines defining `Delta G_a,j(T)`.
- [ ] Step 32: Extract all lines defining affinity `A_j`.
- [ ] Step 33: Extract all lines defining `Delta G_eff,j` and positive barrier handling.
- [ ] Step 34: Extract all lines defining `k_j`.
- [ ] Step 35: Extract all lines defining `d xi_j/dt` and `d xi_j/dq`.
- [ ] Step 36: Extract all lines defining barrier distribution `rho_j(g)`.
- [ ] Step 37: Extract all lines defining ICA/DVA mapping.
- [ ] Step 38: Extract all lines warning about double-counting or identifiability.
- [ ] Step 39: Classify each evidence item as `core`, `extension`, `warning`, `reject`, or `future chapter`.
- [ ] Step 40: Create `PHASE_003_SOURCE_EVIDENCE_INDEX.md`.
- [ ] Step 41: Update ledger.
- [ ] Step 42: Gate `PASS_SOURCE_EVIDENCE_INDEX` only if every core equation has a source line reference.

Gate:

- no core equation enters the derivation without either source support or explicit new derivation status;
- peak-area material is classified as later fitting context unless directly needed for charge balance.

## Phase 004 — PDF Ref. 6/7 Method Extraction

Purpose: verify the method in the user's paper and its ref. 6, 7 before using it to support self-consistent integral or implicit-equation handling.

Inputs:

- `JCP_147(14)_144111_(2017) - Effects of external electric field.pdf`

Steps:

- [ ] Step 43: Determine whether PDF text is extractable without OCR.
- [ ] Step 44: Extract bibliography entries for ref. 6 and ref. 7.
- [ ] Step 45: Locate where ref. 6 and ref. 7 are cited in the user's paper.
- [ ] Step 46: Extract the mathematical problem class associated with those refs.
- [ ] Step 47: Identify whether the method solves an integral equation, an implicit equation, an eigenvalue problem, a fixed-point equation, or another structure.
- [ ] Step 48: Record exact equations from the user's paper that use or motivate the method.
- [ ] Step 49: If OCR is needed, record OCR uncertainty and do not infer unclear symbols.
- [ ] Step 50: Map source variables to current project variables only after the source method is understood.
- [ ] Step 51: Mark assumptions that transfer safely.
- [ ] Step 52: Mark assumptions that do not transfer to graphite ICA.
- [ ] Step 53: Decide whether the ref. 6/7 method is needed in Chapter 1 theory or only in future numerical treatment.
- [ ] Step 54: Create `PHASE_004_REF6_REF7_METHOD_RESULT.md`.
- [ ] Step 55: If the method cannot be verified, mark `METHOD_NOT_IMPORTED` instead of guessing.
- [ ] Step 56: Update ledger.
- [ ] Step 57: Gate `PASS_REF_METHOD_VERIFIED` only if bibliography, citation context, and method structure are confirmed.
- [ ] Step 58: If gate fails, continue Chapter 1 with explicit note that ref. 6/7 is not imported.

Gate:

- no PDF-derived method is used without verified citation context;
- OCR uncertainty is not silently corrected.

## Phase 005 — Problem Definition And Scope Contract

Purpose: lock the new scientific problem statement and prevent drift back to solver/fitting/peak-area-centered work.

Steps:

- [ ] Step 59: Write the observation statement: low-temperature long tail, high-temperature short tail.
- [ ] Step 60: State that equilibrium Gaussian/logistic broadening alone is insufficient for asymmetric finite-rate tail.
- [ ] Step 61: State that peak area is a later capacity/fitting constraint, not the present derivation target.
- [ ] Step 62: Define the present-potential barrier-lowering hypothesis.
- [ ] Step 63: Define the minimum Chapter 1 deliverable as a derivation, not code.
- [ ] Step 64: Define the accepted level of explanation: undergraduate-level step-by-step derivation with no skipped logical jumps.
- [ ] Step 65: Define allowed extensions: kinetic barrier distribution, forward/backward rates, and ref. 6/7 implicit method only if needed.
- [ ] Step 66: Define prohibited extensions: full solver, fitting routine, branch/hysteresis model, heat model as a main chapter body.
- [ ] Step 67: Create a source-to-claim table.
- [ ] Step 68: Create `PHASE_005_TAIL_SCOPE_CONTRACT.md`.
- [ ] Step 69: Update ledger.
- [ ] Step 70: Re-read the user's corrected prompt and map each user requirement to a scope item.
- [ ] Step 71: Mark any unmet user requirement as an open issue.
- [ ] Step 72: Gate `PASS_SCOPE_LOCK` only if all user requirements are represented.

Gate:

- theory-only target is locked;
- no major user requirement is missing.

## Phase 006 — Notation And Dependency Bible

Purpose: create the notation and dependency structure before deriving equations.

Steps:

- [ ] Step 73: Define `Q_ext`, `Q_cell`, and `q`.
- [ ] Step 74: Define `Q_bg(V_n,T)` as residual chemical capacitance.
- [ ] Step 75: Define `xi_j` and `xi_{j,eq}`.
- [ ] Step 76: Define `V_n` as the internal potential solved from charge balance.
- [ ] Step 77: Define `V_{n,app}` as observed apparent potential.
- [ ] Step 78: Define `V_{n,drive}` as kinetic driving voltage.
- [ ] Step 79: Define `V_{n,OCV}` as equilibrium charge-balance root.
- [ ] Step 80: Define `U_j(T)`, `w_j(T)`, and direction sign `s_phi,j`.
- [ ] Step 81: Define `A_j`, `chi_j`, `Delta G_a,j`, `Delta G_eff,j`, `Delta G_eff,j^+`, `nu_j`, and `k_j`.
- [ ] Step 82: Define which variables are state variables, algebraic variables, parameters, and observables.
- [ ] Step 83: Draw a dependency DAG in Markdown text form.
- [ ] Step 84: Mark intentional implicit loops and their closing equations.
- [ ] Step 85: Mark prohibited circular definitions.
- [ ] Step 86: Create a symbol table for manuscript use.
- [ ] Step 87: Create `PHASE_006_NOTATION_DEPENDENCY_BIBLE.md`.
- [ ] Step 88: Update ledger.
- [ ] Step 89: Gate `PASS_NOTATION_DEPENDENCY` only if every symbol in the core spine has a single role.
- [ ] Step 90: If a symbol role conflicts across sources, create a conflict table instead of resolving by guess.

Gate:

- `V_n`, `V_{n,app}`, `V_{n,drive}`, and `V_{n,OCV}` are not conflated;
- implicit feedback is closed by charge balance.

## Phase 007 — Effective Barrier Derivation

Purpose: derive the temperature and present-potential dependent effective barrier in a way that can survive logic review.

Steps:

- [ ] Step 91: Start from intrinsic activation free energy `Delta G_a,j(T)=Delta H_a,j-T Delta S_a,j`.
- [ ] Step 92: Explain the units of `Delta G_a,j`.
- [ ] Step 93: Define affinity `A_j=s_phi,j F[V_{n,drive}-U_j(T)]`.
- [ ] Step 94: Check units of `F * voltage`.
- [ ] Step 95: Explain sign `s_phi,j` and forward driving direction.
- [ ] Step 96: Define coupling coefficient `chi_j`.
- [ ] Step 97: Derive `Delta G_eff,j=Delta G_a,j(T)-chi_j A_j`.
- [ ] Step 98: Explain why positive forward affinity lowers the barrier.
- [ ] Step 99: Explain why adverse affinity raises the effective barrier.
- [ ] Step 100: Introduce `Delta G_eff,j^+` to avoid unphysical unlimited rate.
- [ ] Step 101: Choose softplus as the default smooth positive barrier.
- [ ] Step 102: Derive `k_j=nu_j(T) exp[-Delta G_eff,j^+/(RT)]`.
- [ ] Step 103: Check the exponent is dimensionless.
- [ ] Step 104: Explain low-T and high-T qualitative limits.
- [ ] Step 105: Explain present-potential barrier lowering independently of temperature.
- [ ] Step 106: Record all assumptions.
- [ ] Step 107: Create `PHASE_007_EFFECTIVE_BARRIER_DERIVATION.md`.
- [ ] Step 108: Update ledger.
- [ ] Step 109: Run sign audit.
- [ ] Step 110: Run dimensional audit.
- [ ] Step 111: Run double-counting audit for `R_n`, `V_drive`, and `k_j`.
- [ ] Step 112: Gate `PASS_EFFECTIVE_BARRIER_DERIVATION` only if sign/unit/role checks pass.

Gate:

- `Delta G_eff` decreases under forward driving potential;
- `k_j` increases when `Delta G_eff^+` decreases;
- no voltage role is double-counted.

## Phase 008 — Tail Decay Derivation

Purpose: derive the tail length expression from the relaxation equation without skipping steps.

Steps:

- [ ] Step 113: Start from `d xi_j/dt = k_j [xi_{j,eq}-xi_j]`.
- [ ] Step 114: Define constant-current relation `dq/dt=|I|/Q_cell`.
- [ ] Step 115: Convert to `d xi_j/dq=(Q_cell/|I|)k_j[xi_{j,eq}-xi_j]`.
- [ ] Step 116: Define the local tail residual `u_j=xi_{j,eq}-xi_j` in the region after equilibrium progress has moved ahead.
- [ ] Step 117: Derive `du_j/dq=-kappa_j u_j` under the local frozen/slowly varying `xi_eq` approximation.
- [ ] Step 118: Define `kappa_j=(Q_cell/|I|)k_j`.
- [ ] Step 119: Solve `u_j(q)=u_j(q_a) exp[-int_{q_a}^{q} kappa_j(s) ds]`.
- [ ] Step 120: For locally constant `kappa_j`, derive `u_j(q)=u_j(q_a) exp[-(q-q_a)/ell_q,j]`.
- [ ] Step 121: Define `ell_q,j=1/kappa_j=|I|/(Q_cell k_j)`.
- [ ] Step 122: Substitute the effective barrier rate.
- [ ] Step 123: Derive `ell_q,j=|I|/[Q_cell nu_j(T)] exp[Delta G_eff,j^+/(RT)]`.
- [ ] Step 124: Explain low-temperature long-tail limit.
- [ ] Step 125: Explain high-temperature short-tail limit.
- [ ] Step 126: Explain present-potential barrier-lowering short-tail effect.
- [ ] Step 127: Explain C-rate competition: residence time versus drive-enhanced `k_j`.
- [ ] Step 128: State where the local frozen/slowly varying approximation is used.
- [ ] Step 129: State when the approximation fails.
- [ ] Step 130: Create `PHASE_008_TAIL_DECAY_DERIVATION.md`.
- [ ] Step 131: Update ledger.
- [ ] Step 132: Run algebra audit.
- [ ] Step 133: Run limiting-case audit.
- [ ] Step 134: Run user-observation alignment audit.
- [ ] Step 135: Mark unresolved derivation limits explicitly.
- [ ] Step 136: Gate `PASS_TAIL_DECAY_DERIVATION` only if `ell_q,j` follows from the previous equations.

Gate:

- tail length is derived rather than asserted;
- assumptions behind the local tail solution are visible.

## Phase 009 — ICA/DVA Observable Mapping

Purpose: connect the derived tail dynamics to ICA/DVA without turning the section into fitting code.

Steps:

- [ ] Step 137: Start from charge balance.
- [ ] Step 138: Differentiate charge balance with respect to `q`.
- [ ] Step 139: Derive `dV_n/dq`.
- [ ] Step 140: Add apparent voltage derivative `dV_{n,app}/dq`.
- [ ] Step 141: Define `dQ_ext/dV_{n,app}=Q_cell/(dV_{n,app}/dq)`.
- [ ] Step 142: Define `dV_{n,app}/dQ_ext=(1/Q_cell)dV_{n,app}/dq`.
- [ ] Step 143: Show how `d xi_j/dq` enters `dV_n/dq`.
- [ ] Step 144: Explain why a delayed `xi_j` creates a tail in the observed voltage coordinate.
- [ ] Step 145: Explain why the ICA tail is not simply peak area.
- [ ] Step 146: Explain what remains for future fitting.
- [ ] Step 147: Create `PHASE_009_ICA_DVA_MAPPING.md`.
- [ ] Step 148: Update ledger.
- [ ] Step 149: Run dependency audit from `xi_j` to `dQ/dV`.
- [ ] Step 150: Run monotonicity/sign audit for `dV/dq`.
- [ ] Step 151: Check consistency with source line references.
- [ ] Step 152: Mark any terms intentionally omitted from Chapter 1.
- [ ] Step 153: Confirm no fitting objective is introduced.
- [ ] Step 154: Confirm no solver algorithm is introduced.
- [ ] Step 155: Confirm `R_n` is limited to voltage-axis/polarization role.
- [ ] Step 156: Confirm `k_j` is limited to phase-progress rate role.
- [ ] Step 157: Record gate result.
- [ ] Step 158: Gate `PASS_ICA_DVA_MAPPING` only if observable mapping is source-consistent.

Gate:

- `dQ/dV` is connected to `d xi/dq` through charge-balance derivatives;
- no empirical peak model becomes the core theory.

## Phase 010 — Barrier Distribution Extension

Purpose: add only the minimum distribution theory needed to explain stretched tails beyond a single relaxation scale.

Steps:

- [ ] Step 159: Define kinetic barrier variable `g>=0`.
- [ ] Step 160: Define `rho_j(g)` as a kinetic activation barrier distribution.
- [ ] Step 161: State that `rho_j(g)` is not an equilibrium transition-center distribution.
- [ ] Step 162: Define `Delta G_eff,j(g)=g-chi_j A_j`.
- [ ] Step 163: Define positive barrier `Delta G_eff,j^+(g)`.
- [ ] Step 164: Define `k_j(g)=nu_j(T) exp[-Delta G_eff,j^+(g)/(RT)]`.
- [ ] Step 165: Define `d xi_j(g)/dq`.
- [ ] Step 166: Define averaged `xi_j=integral rho_j(g) xi_j(g) dg`.
- [ ] Step 167: Define averaged `d xi_j/dq`.
- [ ] Step 168: Explain why high-`g` groups create long tails.
- [ ] Step 169: Explain why higher `T` and larger forward `A_j` shorten high-`g` tail contribution.
- [ ] Step 170: Explicitly reject threshold completion.
- [ ] Step 171: Create `PHASE_010_BARRIER_DISTRIBUTION_EXTENSION.md`.
- [ ] Step 172: Update ledger.
- [ ] Step 173: Run distribution normalization audit.
- [ ] Step 174: Run role-confusion audit for `rho_j(g)` versus `w_j`.
- [ ] Step 175: Mark distribution as extension, not required for first derivation.
- [ ] Step 176: Gate `PASS_BARRIER_DISTRIBUTION_EXTENSION`.

Gate:

- distribution is a kinetic extension;
- no threshold barrier logic is introduced.

## Phase 011 — Manuscript Draft From Scratch

Purpose: write the new Chapter 1 manuscript without patching the archived drafts.

Output:

`D:\Projects\Project_Anode_Fit\Codex\results\graphite_ica_tail_effective_barrier_theory_chapter1.tex`

Steps:

- [ ] Step 177: Create a new LaTeX file from a clean preamble.
- [ ] Step 178: Write title and abstract focused on ICA tail behavior.
- [ ] Step 179: Write Section 1: observation and problem statement.
- [ ] Step 180: Write Section 2: why equilibrium peak shape is insufficient.
- [ ] Step 181: Write Section 3: charge coordinate and charge balance.
- [ ] Step 182: Write Section 4: voltage roles.
- [ ] Step 183: Write Section 5: equilibrium transition progress.
- [ ] Step 184: Write Section 6: intrinsic thermal barrier.
- [ ] Step 185: Write Section 7: present-potential-assisted effective barrier.
- [ ] Step 186: Write Section 8: transition rate.
- [ ] Step 187: Write Section 9: progress relaxation in time.
- [ ] Step 188: Write Section 10: progress relaxation in charge coordinate.
- [ ] Step 189: Write Section 11: tail decay and `ell_q,j`.
- [ ] Step 190: Write Section 12: interpretation of low/high temperature and present potential.
- [ ] Step 191: Write Section 13: ICA/DVA mapping.
- [ ] Step 192: Write Section 14: optional kinetic barrier distribution.
- [ ] Step 193: Write Section 15: logical guardrails and future fitting boundary.
- [ ] Step 194: Add notation table.
- [ ] Step 195: Add source-grounded comments only where they help the reader; do not add work history.
- [ ] Step 196: Avoid phase labels, dates, and audit metadata in manuscript body.
- [ ] Step 197: Create `PHASE_011_DRAFT_RESULT.md`.
- [ ] Step 198: Update ledger.
- [ ] Step 199: Run LaTeX syntax scan for unbalanced environments.
- [ ] Step 200: Run equation label/reference scan.
- [ ] Step 201: Run symbol consistency scan.
- [ ] Step 202: Run Korean/English acronym first-use scan.
- [ ] Step 203: Run line search for banned drift terms: solver implementation, fitting code, peak-area-centered argument.
- [ ] Step 204: Mark any unresolved manuscript gaps.
- [ ] Step 205: Record gate result.
- [ ] Step 206: Gate `PASS_DRAFT_STRUCTURE` only if every manuscript section traces to phase derivations.

Gate:

- manuscript is newly written;
- no archived draft text is accepted by inertia;
- no work-history metadata appears in the manuscript body.

## Phase 012 — Ralph Wiggum Logic Verification Loop

Purpose: repeatedly audit the manuscript logic until no blocking gap remains or a clear unresolved issue requires user decision.

Loop rule:

```text
hard gate -> parse failure -> update result/ledger -> repair from fresh context -> re-run
```

Maximum loop count: 10.

Escalation rule: if the same blocking error remains after 3 repair attempts, write a decision item instead of hiding it.

Audit dimensions:

- source traceability;
- charge-balance closure;
- voltage-role separation;
- sign logic;
- unit/dimension logic;
- local tail approximation;
- limiting cases;
- ICA/DVA mapping;
- no double-counting;
- no solver/fitting drift.

Steps:

- [ ] Step 207: Create audit checklist from Phases 005-010 gates.
- [ ] Step 208: Pass 1 broad logic scan.
- [ ] Step 209: Record all candidate issues.
- [ ] Step 210: Classify each issue as blocking, non-blocking, future extension, or false alarm.
- [ ] Step 211: Repair blocking issue 1 if present.
- [ ] Step 212: Repair blocking issue 2 if present.
- [ ] Step 213: Repair blocking issue 3 if present.
- [ ] Step 214: Re-run full checklist.
- [ ] Step 215: Pass 2 dependency scan.
- [ ] Step 216: Repair dependency issues if present.
- [ ] Step 217: Re-run dependency scan.
- [ ] Step 218: Pass 3 sign/unit scan.
- [ ] Step 219: Repair sign/unit issues if present.
- [ ] Step 220: Re-run sign/unit scan.
- [ ] Step 221: Pass 4 user-observation alignment scan.
- [ ] Step 222: Repair alignment issues if present.
- [ ] Step 223: Re-run alignment scan.
- [ ] Step 224: Pass 5 manuscript readability scan for undergraduate-level derivation continuity.
- [ ] Step 225: Repair continuity gaps if present.
- [ ] Step 226: Re-run readability scan.
- [ ] Step 227: Create `PHASE_012_RALPH_WIGGUM_LOGIC_AUDIT.md`.
- [ ] Step 228: Update ledger.
- [ ] Step 229: If all gates pass, mark `PASS_LOGIC_AUDIT`.
- [ ] Step 230: If non-blocking issues remain, list them as future work.
- [ ] Step 231: If blocking issues remain, mark `BLOCKED_DECISION_REQUIRED`.
- [ ] Step 232: Confirm every equation in the final manuscript appears in the dependency bible or derivation result.
- [ ] Step 233: Confirm every introduced assumption appears near the equation that uses it.
- [ ] Step 234: Confirm no old artifact is cited as proof.
- [ ] Step 235: Confirm no source file was modified.
- [ ] Step 236: Confirm no Claude file was modified.
- [ ] Step 237: Record final audit status.
- [ ] Step 238: Gate `PASS_RALPH_WIGGUM_LOGIC_LOOP` only if no blocking gap remains.

Gate:

- no blocking logical gap remains unreported;
- repairs are verified after each loop.

## Phase 013 — Final Packaging And Handover

Purpose: package the rebuilt Chapter 1 and leave a clean continuation point.

Steps:

- [ ] Step 239: Create final file inventory.
- [ ] Step 240: Verify plan/result/ledger paths.
- [ ] Step 241: Verify source read coverage is recorded.
- [ ] Step 242: Verify final manuscript path exists.
- [ ] Step 243: Verify old archive path remains intact.
- [ ] Step 244: Verify no original source file was modified.
- [ ] Step 245: Verify no Claude file was modified.
- [ ] Step 246: Create `PHASE_013_FINAL_HANDOVER.md`.
- [ ] Step 247: Update `PHASE_001_013_RESTART_EXECUTION_LEDGER.md`.
- [ ] Step 248: Prepare concise user-facing summary.
- [ ] Step 249: List any user decisions that truly remain.
- [ ] Step 250: List files to inspect next.
- [ ] Step 251: Gate `PASS_FINAL_HANDOVER`.
- [ ] Step 252: Stop only if user decision is needed or the requested manuscript is ready for user review.

Gate:

- final deliverables and evidence chain are traceable from source to manuscript;
- active workspace is understandable without relying on conversation memory.

## Implementation Interfaces

### Core Manuscript Equation Spine

The rebuilt manuscript must contain these equations in this order unless a phase result justifies a change:

```tex
Q_{\mathrm{ext}}(t)=\int_0^t |I(s)|\,ds
```

```tex
q=\frac{Q_{\mathrm{ext}}}{Q_{\mathrm{cell}}}
```

```tex
Q_{\mathrm{cell}}q
=
Q_{\mathrm{bg}}(V_n,T)
+
\sum_{j=1}^{N_p}Q_{j,\mathrm{tot}}\xi_j
```

```tex
V_{n,\mathrm{app}}
=
V_n+s_I|I|R_n(q,T,|I|)
```

```tex
\mathcal A_j
=
s_{\phi,j}F\left[V_{n,\mathrm{drive}}-U_j(T)\right]
```

```tex
\Delta G_{a,j}(T)
=
\Delta H_{a,j}-T\Delta S_{a,j}
```

```tex
\Delta G_{\mathrm{eff},j}
=
\Delta G_{a,j}(T)-\chi_j\mathcal A_j
```

```tex
\Delta G_{\mathrm{eff},j}^{+}
=
\epsilon_G\ln\left[
1+\exp\left(\frac{\Delta G_{\mathrm{eff},j}}{\epsilon_G}\right)
\right]
```

```tex
k_j
=
\nu_j(T)\exp\left[
-\frac{\Delta G_{\mathrm{eff},j}^{+}}{RT}
\right]
```

```tex
\frac{d\xi_j}{dq}
=
\frac{Q_{\mathrm{cell}}}{|I|}
k_j(q,T,I)
\left[\xi_{j,\mathrm{eq}}(V_n,T)-\xi_j\right]
```

```tex
\ell_{q,j}
=
\frac{|I|}{Q_{\mathrm{cell}}k_j}
```

```tex
\ell_{q,j}
=
\frac{|I|}{Q_{\mathrm{cell}}\nu_j(T)}
\exp\left[
\frac{\Delta G_{\mathrm{eff},j}^{+}(q,T,I)}{RT}
\right]
```

Correction note for execution: the rate expression must be rendered with a single negative sign in the exponent:

```tex
\exp\left[-\frac{\Delta G_{\mathrm{eff},j}^{+}}{RT}\right]
```

### Result Document Required Fields

Every phase result must include:

```markdown
## Summary
## Step Range
## Inputs
## Files Created
## Files Updated
## Read Coverage
## Execution Evidence
## Validation
## Gate
## Confirmed Non-Changes
## Open Issues / Decision Queue
## Next
```

### Ledger Row Required Fields

```markdown
| Phase | Planned Steps | Actual Steps | Purpose | Status | Plan | Result | Validation | Gate | Next Step |
```

### Ralph Wiggum Failure Record

Every failed logic loop must record:

```markdown
| Loop | Failed Gate | Failure Type | Evidence | Repair Action | Re-run Result |
```

Failure types:

- `SIGN`
- `UNIT`
- `CIRCULAR_DEPENDENCY`
- `SOURCE_TRACE`
- `ASSUMPTION_GAP`
- `OBSERVATION_MISMATCH`
- `DOUBLE_COUNTING`
- `SCOPE_DRIFT`

## Test Plan

### File And Workspace Tests

- Confirm `Codex\old\2026-05-28-reset-before-tail-effective-barrier-restart` exists.
- Confirm active plan and result files are in `Codex\plans` and `Codex\results`.
- Confirm original source folder files are not modified.
- Confirm Claude folder is not modified.

### Read Coverage Tests

- Count source lines before reading.
- Record every read range.
- Re-read any truncated range.
- Do not use `READ_FULL` unless full coverage is recorded.

### Mathematical Tests

- Unit check for every exponential argument.
- Sign check for forward affinity and barrier lowering.
- Dependency check for `V_n`, `V_app`, `V_drive`, `V_OCV`.
- Limiting case check:
  - low `T` gives longer `ell_q` if other terms are comparable;
  - high `T` gives shorter `ell_q` if other terms are comparable;
  - larger forward `A_j` lowers `Delta G_eff^+` and shortens `ell_q`;
  - larger `|I|` has competing residence-time and drive effects.
- Double-counting check for `R_n`, `eta_j`, `V_drive`, and `k_j`.

### Manuscript Tests

- LaTeX environment balance scan.
- Equation label/reference scan.
- Symbol table scan.
- Acronym first-use scan for ICA, DVA, LIB, OCV.
- Search for banned scope drift terms in the final manuscript:
  - fitting code;
  - solver implementation;
  - peak area as central proof;
  - branch/hysteresis as Chapter 1 core.

### Gate Tests

- Each phase gate must cite the actual result file.
- Failed gates must not be marked pass.
- If PDF ref. 6/7 cannot be verified, the plan continues with a visible non-import decision.

## Assumptions

- The active Chapter 1 target is a theoretical derivation, not implementation.
- The reduced model may start with `V_{n,drive}\approx V_{n,app}`, but the manuscript must state the approximation and double-counting guard.
- The single-barrier tail scale is derived before introducing `rho_j(g)`.
- The PDF method from ref. 6/7 is potentially relevant to implicit/self-consistent handling, but it is not automatically part of the Chapter 1 derivation until verified.
- Phase boundary reporting to the user is not required unless a decision is needed, but phase result files are still required.

## Correction History

| Date | Correction |
|---|---|
| 2026-05-28 | Restarted after user clarified that previous work was too broad and peak-area/solver/fitting-centered. Previous Codex artifacts were archived under `Codex\old`; the new plan starts from original source files and centers tail-effective-barrier theory. |
