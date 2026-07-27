# v1.0.25.3 Conformance Branch Handover

## Branch State

- branch: `codex/v1025_2-physics-conformance`
- baseline commit:
  `ab196b292e14492b647f87a6c0d1d8c9ed0630ab`
- commit/push/merge performed: **no**
- legacy source edits performed: **no**
- pre-existing excluded dirty file:
  `Claude/docs/v1.0.24.1/CODE_GUIDE_v24.html`

## Review Entry Points

1. Read the result:
   `Codex/results/PHASE_046_053_V1025_3_RECONSTRUCTION_RESULT.md`
2. Read the physics decisions:
   `Codex/results/V1025_2_PHYSICS_DECISION_LEDGER.md`
3. Read the new matrix:
   `Codex/results/V1025_3_PHYSICS_IMPLEMENTATION_CONFORMANCE_MATRIX.md`
4. Review the manuscript:
   `Codex/results/v1025_2_physics_branch/manuscript/anode_physics_master.tex`
5. Review the clean implementation:
   `Codex/work/v1025_2_physics_branch/conformance_model/README.md`
6. Inspect the rendered document:
   `output/pdf/Anode_Physics_v1.0.25.3_conformance.pdf`

## Reproduction Commands

From the repository root:

```bash
python3 -W error Codex/work/v1025_2_physics_branch/tests/run_all.py
python3 Codex/work/v1025_2_physics_branch/tests/verify_manuscript.py
```

Legacy gates:

```bash
cd Claude/docs/v1.0.25.2
python3 test_gates_v1025.py
python3 test_gates_v1024.py
```

The PDF is built with XeLaTeX. A Korean-capable font must be discoverable as
`Noto Serif CJK KR` or `NanumGothic`; the delivered PDF embeds NanumGothic.

## Acceptance Boundary

Safe to review as one candidate:

- the physics-first manuscript;
- the immutable direct14 empirical observation artifact;
- the clean equilibrium/observation/causal/rate/heat core;
- the independent conformance suite.

Do not promote the following to release claims:

- v1.0.26 as scientific authority;
- the direct14 components as graphite/Si phases;
- the stored fit as reproduction of the original optimizer state;
- regular solution, branch kinetics, entropy decomposition, thermal tails or
  Si mechanical/current-allocation laws as implemented production closures.

## Next Decision

The next maintainer should choose one of two paths:

1. **Review-only checkpoint:** inspect the candidate and request focused changes
   while keeping it uncommitted.
2. **Publication checkpoint:** after approval, commit this branch intentionally
   and open a review without merging into the legacy release line.

No further numerical fitting should occur until the missing experimental
protocol and intended physical-host evidence are supplied.
