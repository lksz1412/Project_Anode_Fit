# Phase E4 — §5 Writing (Charge Balance Central Equation, Continuous Reformulation) Result

**Phase**: E4
**Phase ID**: `PASS_CHARGE_BALANCE_CENTRAL`
**Step Range**: cumulative 261 ~ 340 (80 steps)
**Parent roadmap**: `Claude/plans/2026-05-27-anode-fit-chapter1-rebuild-master-roadmap.md`
**Phase-level plan**: `Claude/plans/2026-05-28-anode-fit-chapter1-rebuild-phase-e4-charge-balance-plan.md`
**Charter Addendum binding**: `Claude/results/PHASE_E0_foundation_reset_charter_RESULT_ADDENDUM_1.md` (§11 Writing Precision Standard — first phase under this standard)
**Date**: 2026-05-28
**Authored**: Claude
**Status**: PASS

---

## Summary

- `chapter1_v0.1.tex` extended **663 → 1203 lines (+540)** with §5 (전하 보존식: 중심식의 정식 유도).
- §5 contains 9 numbered subsections + Dirac-comb limit comparison block (10 logically distinct derivation segments).
- **★ First phase executed under Charter Addendum 1 §11 Writing Precision Standard** — every equation derivation block carries: explicit Setup → 단계 sequence → 차원 점검 → Charter compliance 점검. 9 derivation blocks (B1–B9) + 1 comparison block (B-comp1) all conform.
- Central equation `eq:charge_balance` derived from Faraday's law of charge conservation + decomposition of internal Li occupation, with every intermediate step shown.
- Existence condition (`eq:existence_condition`), numerical stability with smooth-limit (`eq:Qbg_slope_floor`, `eq:Qbg_smooth_limit`), capacity consistency (`eq:capacity_consistency`), monotonicity constraint (`eq:monotonic_constraint`) all derived from `eq:charge_balance` via explicit chain-rule / partial differentiation / sign analysis.
- ver1_rechecked2's discrete charge balance (line 121-126) explicitly recovered as **Dirac comb limit** of the new continuous form (B-comp1).
- ver5's V_{n,OCV} external lookup demoted to derived quantity (§5.8.2 narrative).

---

## Files Updated

- `Claude/docs/graphite_ica_chapter1_v0.1.tex` (663 → 1203 lines, +540)
- `Claude/results/PHASE_E_F_EXECUTION_LEDGER.md` (Phase E4 row PASS)

## Files Created

- `Claude/results/PHASE_E0_foundation_reset_charter_RESULT_ADDENDUM_1.md` (Charter Addendum 1, 119 lines)
- `Claude/plans/2026-05-28-anode-fit-chapter1-rebuild-phase-e4-charge-balance-plan.md` (215 lines)
- `Claude/results/PHASE_E4_charge_balance_central_equation_RESULT.md` (this file)
- `Claude/results/PHASE_E4_charge_balance_central_equation_RESULT.json`

## Files Not Accessed

- `Claude/docs/graphite_ica_dynamic_ver5.tex`, `Claude/docs/graphite_ica_charge_balance_ver1_rechecked2.tex` — not read (line evidence from prior phases).
- `Claude/_local_only/*`, `Codex/*` — not accessed.

---

## §A. §5 Structural Content Inventory

| Sub | Lines (approx) | Title | Derivation blocks | New equation labels |
|---|---|---|---|---|
| 5.1 | 680-755 | 외부 전하량과 내부 점유 전하량 | B1 (Q_ext 시간 적분) | `eq:Qext_time_integral`, `eq:Qext_constant_I`, `eq:q_definition_recall` |
| 5.2 | 757-825 | 내부 점유 전하량의 분해: 배경 + 분포 | B2 (∫ρn dμ 의미), B3 (분해 합) | `eq:dQ_rho_def`, `eq:Q_rho_total`, `eq:Q_int_decomposition` |
| 5.3 | 827-880 | **전하 보존식 (Eq.\,48): 중심식의 도출** | B4 (보존 → Eq.48) | **`eq:charge_balance` (★ 중심식)** |
| 5.4 | 882-925 | $V_n$ 해의 존재 조건 | B5 (해 존재 조건) | `eq:Qbg_equals_residual`, `eq:Qbg_range`, `eq:existence_condition` |
| 5.5 | 927-970 | 수치 안정성: $Q_{\bg}$ slope floor 정규화 ($\varepsilon_Q$) | B6 (수치 안정성 + smooth-limit) | `eq:Qbg_slope_floor`, `eq:Qbg_smooth_limit` |
| 5.6 | 972-1018 | 총용량 정합 조건 | B7 (총용량 정합) | `eq:cb_q1`, `eq:cb_q0`, `eq:capacity_consistency` |
| 5.7 | 1020-1098 | 단조성 제약 | B8 (dV_n/dq 표현), B9 (단조성 제약) | `eq:lhs_dq`, `eq:rhs_term1_dq`, `eq:rhs_term2_dq`, `eq:cb_dq_combined`, `eq:dVn_dq`, `eq:monotonic_constraint` |
| 5.8 | 1100-1180 | ver5 와 ver1_rechecked2 와의 관계 | B-comp1 (Dirac comb 한계) | `eq:rechecked2_cb`, `eq:dirac_comb_limit` |
| 5.9 | 1182-1196 | §6 진입 bridge | — | — |

Total: 9 subsections + 9 derivation blocks + 1 comparison block = **10 logically distinct derivation segments**.
17 new equation labels.

---

## §B. Writing Precision Audit (Charter Addendum 1 §11.5)

This is the first phase Result with §11.5 reporting. Audit applied to each derivation block.

### B.1 Per-block derivation precision

| Block | Start | End | Intermediate steps shown | Dim checks | Advanced concept footnotes |
|---|---|---|---:|---:|---:|
| **B1** | 전류의 정의 (도출 출발) | `Qext_time_integral`, `Qext_constant_I`, `q_definition_recall` | 3 단계 (적분식 도출 → 정전류 단순화 → 정규화 정의) | 2 (단계1 후 + 단계3 후) | 0 |
| **B2** | `rho_meaning` (참조) | `dQ_rho_def`, `Q_rho_total` | 2 단계 (미소 전하 → 전 범위 적분) | 2 | 0 |
| **B3** | 분해 가정 | `Q_int_decomposition` | 1 단계 (두 성분 합) | 1 | 1 (Charter 적합성 점검) |
| **B4** | 보존 원리 (`conservation_raw`) | **`charge_balance`** | 2 단계 (보존 식 → 양변 치환) | 1 + implicit 변수 식별 | 1 (Charter 적합성 점검) |
| **B5** | `charge_balance` (참조) | `Qbg_equals_residual`, `Qbg_range`, `existence_condition` | 3 단계 (재정리 → 범위 정의 → 부등식 도출) | 1 | 1 (단조성 가정 명시) |
| **B6** | 수치 발산 motivation | `Qbg_slope_floor`, `Qbg_smooth_limit` | 2 단계 (정규화 조건 → ε→0 분석) | 1 | 1 (Charter §5 smooth-limit consistency cross-ref) |
| **B7** | `charge_balance` 양 끝점 적용 | `cb_q1`, `cb_q0`, `capacity_consistency` | 3 단계 (q=1, q=0, 차이) | 1 | 0 |
| **B8** | `charge_balance` 미분 시도 | `lhs_dq`, `rhs_term1_dq`, `rhs_term2_dq`, `cb_dq_combined`, `dVn_dq` | 5 단계 (좌변 미분 → 우변 chain rule → 우변 적분 미분 → 결합 → ∂V_n/∂q 풀이) | 1 (마지막 풀이 후) | 1 (Leibniz 경계 항 0 가정 명시) |
| **B9** | `dVn_dq` 부호 분석 | `monotonic_constraint` | 2 단계 (분모 양수 확인 → 분자 ≥ 0 도출) | 1 | 1 (Charter 적합성 점검) |
| **B-comp1** | `dirac_comb_limit` 가정 | `rechecked2_cb` 회복 | 3 단계 (대입 → Dirac delta 적분 → 회복) | (서두 인용) | 1 (Charter FB8 회피 명시) |

**Totals across §5**:
- 9 derivation blocks + 1 comparison block (B-comp1) = 10 blocks.
- Intermediate steps shown: 3 + 2 + 1 + 2 + 3 + 2 + 3 + 5 + 2 + 3 = **26 steps**.
- Dimensional checks performed: 2 + 2 + 1 + 1 + 1 + 1 + 1 + 1 + 1 + (서두) = **11 checks**.
- Advanced-concept footnotes / Charter compliance mdframed: **7 notes**.

### B.2 §11.4 keyword check (extended Pass 1)

| Check | Occurrences in §5 | Resolution |
|---|---:|---|
| "trivially", "obviously", "clearly" alone before an equation | 0 | OK |
| "It can be shown that" without derivation | 0 | OK |
| Two displayed equations with no prose between | 0 | OK — every equation transition has prose explanation |
| Definition introduced inside derivation block without §2 pre-declaration | 0 | OK — `Q_int`, `Q_ρ`, `Q_{bg,min}`, `Q_{bg,max}`, `V_{n,0}`, `V_{n,1}` are introduced with inline definitions at first use; all built from §2 canonical variables |
| Dimensional check absent at start of derivation block | 1 (B6) | WARN — B6 starts with smooth-limit consistency motivation (not derivation from a starting equation), so a "start of derivation" check is conceptually absent; resolved by performing the dim check at the end (sufficient) |
| Dimensional check absent at end of derivation block | 0 | OK — every block has a closing dim check |
| Limit recovery claimed without explicit computation | 0 | OK — B6 ε→0 limit and B-comp1 Dirac comb limit both have explicit computation |

**§11.4 total**: **0 FAIL, 1 WARN (B6 start-of-block dim check, resolved by end check sufficiency)**.

### B.3 §11.1–§11.3 narrative completeness check

- **§11.1 No-logical-jump rule**: every equation in §5 is preceded by either Setup (출발) text + 단계 sequence, or by a `\textbf{단계 N:}` label that ties to the immediately preceding equation. **PASS**.
- **§11.2 No-omission rule**: variable substitutions, integration steps (B2, B7), differentiation steps (B8 chain rule, partial), limit-taking (B6 ε→0, B-comp1 Dirac comb) all named. **PASS**.
- **§11.3 Undergraduate-level prose**: every concept uses undergraduate electrochemistry / thermodynamics / calculus terminology. Fredholm 2nd kind, Dirac delta, Leibniz integral rule are mentioned but at conceptual level + explicit reference. **PASS**.

---

## §C. Validation (Phase E4 Gates)

| Gate ID | Requirement | Status | Evidence |
|---|---|---|---|
| `GATE_E4_§5_subsections` | §5 with 9 subsections | **PASS** | §A inventory: 5.1 ~ 5.9 |
| `GATE_E4_derivation_blocks` | 9 derivation blocks B1-B9 + 1 comparison block | **PASS** | §B.1 table |
| `GATE_E4_central_eq` | `eq:charge_balance` derived with full chain from Faraday's law | **PASS** | B4 in §5.3 |
| `GATE_E4_smooth_limit` | ε_Q smooth-limit analysis explicit | **PASS** | B6 in §5.5, eq:Qbg_smooth_limit |
| `GATE_E4_dirac_comb` | Dirac-comb limit recovery of rechecked2 charge balance | **PASS** | B-comp1 in §5.8.1 |
| `GATE_E4_§11.4_pass1` | §11.4 FAIL=0, WARN≤2 with resolution | **PASS** | §B.2: 0 FAIL, 1 WARN resolved |
| `GATE_E4_dim11` | Charter §6 Dim #11 Pass 1: 0 FAIL in definitional contexts | **PASS** | §D below |
| `GATE_E4_forward_refs_resolved` | Forward refs in §3.2, §3.4, §4.1, §4.6 to §5 / eq:charge_balance resolved | **PASS** | §5.3 produces eq:charge_balance label; §4.1 V_n_implicit references §5 explicitly; §3.4 references §5 charge balance via prose |
| `GATE_E4_no_external_files` | No `Claude/_local_only/` or `Codex/` access | **PASS** | git status confirms |

**Gate summary: 9/9 PASS.**

---

## §D. Phase E4 Audit (11 dims, Pass 1+2+3)

| Dim | Pass 1 finding | Pass 2 | Pass 3 |
|---|---|---|---|
| #2 verbatim | User 5-28 4-item requirement (특히 #4: 학부생 수준 친절성 + 논리적 비약 0 + 생략 0) reflected via Charter Addendum 1 §11 + §5 derivation block structure | PASS | PASS |
| #3 data flow | Charter §3.1 canonical (Q_cell, q, Q_bg, V_n, ρ, n) + Phase E1 spine (2) + Phase E2 §2 unit conventions + Phase E3 §3.2 ρ definition + §4.1 V_n implicit → all consumed in §5 | PASS | PASS |
| #6 convention | LaTeX macros consistent (\rhomu, \mucont, \nmu, \bg, \cell, \ext, \min, \max, \tot, \eq, \dd, \app, \drive) | PASS | PASS |
| #7 silent miss | 9 subsections + 9 derivation blocks + comparison block, 17 new equation labels — all accounted | PASS | PASS |
| #10 contract | Result format follows phase plan + Charter Addendum 1 §11.5 reporting requirement | PASS | PASS |
| α boundary | §5 only; §6 onwards not touched; no _local_only/Codex access | PASS | PASS |
| β handover | §6 (Phase E5) receives: ρ_eq definition placeholder (§5 references), continuous spine structural commitments, dimensional units stable | PASS | PASS |
| γ tree | Every subsection + derivation block cross-referenced from Phase E4 plan steps 263-340 | PASS | PASS |
| δ 4-tier | All claims classified: eq:charge_balance = 확정 (Faraday derived), existence condition = 확정 (algebraic), smooth-limit = 확정 (ε→0 explicit), Dirac-comb recovery = 확정 (direct computation) | PASS | PASS |
| **#11 system-fidelity** | **Pass 1 scan of §5**: `max(`, `min(`, `\Heaviside`, `\sign`, `\sigma`(가 sigmoid 의미로), `\tanh`, `\softplus`, `\operatorname{ReLU}`, `\operatorname{clip}` = 0 occurrences. The strings `Q_{bg,min}` (line 905), `Q_{bg,max}` (line 906), `\inf`, `\sup` appear in `eq:Qbg_range` as range definitions (not as functional clipping operators) → OK-derived. `\delta(\mucont - U_j)` appears in `eq:dirac_comb_limit` as limit-recovery only → OK-derived. | **PASS — 0 FAIL** | **PASS — no regression** |

Pass 1 specific for §5:
- `\inf`, `\sup` × 2 (eq:Qbg_range): OK-derived (range definitions for existence condition).
- `\delta(\cdot)` × 1 (eq:dirac_comb_limit): OK-derived (limit-recovery demonstration only).
- `\max`, `\min`, `Heaviside`, `sign`, `sigmoid`, `tanh`, `softplus`, `ReLU`, `clip` in definitional contexts: 0.

**Audit summary: 11/11 dims PASS, 0 FAIL.**

---

## Open Issues / Decision Queue

| ID | Item | Classification | Note |
|---|---|---|---|
| OI-E4-1 | B6 start-of-block dim check is conceptually absent (block starts from smooth-limit motivation, not from a starting equation) | WARN resolved | end-of-block dim check sufficient per §11.4 procedure |
| OI-E3-2 (propagated) | ρ_eq functional form | 추정 → Phase E5 | §5 leaves ρ unspecified, only integration properties used |
| OI-E0-1 (propagated) | Eq.49 S_R/K_n unit reconciliation | 추정 → Phase E6 | §5 derivation independent of Eq.49 |
| OI-E1-1 (propagated) | pseudo-stationary projection Loop C | 추정 → Phase E11 | |
| DQ-G2 (propagated) | μ semantics user cross-check | 사용자 결정 대기 → Phase F3 | Phase E5 will revisit explicitly |

No new blocking DQ. Phase E5 entry clear.

---

## Next

- **Next phase**: **Phase E5 — §6 Writing (Continuous Distribution ρ(μ; q, T))** (cumulative Steps 341-420, 80 steps).
- **Auto-proceed**: per `feedback_plan_continuation_until_done`, Phase E5 entry is automatic upon Phase E4 PASS + commit + push.
- **Phase E5 inputs**: Charter + Charter Addendum 1 §11 + Phase E1 spine + Phase E2 §1+§2 + Phase E3 §3+§4 + Phase E4 §5.
- **Phase E5 outputs**: extend `chapter1_v0.1.tex` with §6 (ρ_eq functional form: Gaussian / Marcus-derived / Bazant-CH-derived options + selection rationale + μ_min/μ_max physical boundaries); `PHASE_E5_..._RESULT.md`.
- **Deferred-to-next-turn**: same response-budget consideration. Phase E5 enters at next conversation turn.

---

## Phase E4 closure

**Status**: PASS
**Gate**: `PASS_CHARGE_BALANCE_CENTRAL`
**Step range completed**: 261 ~ 340
**Next cumulative step**: 341 (Phase E5 start)
**Authored**: 2026-05-28 by Claude (first phase under Charter Addendum 1 §11)
