# Phase 009 Isolated Runtime Test Evidence

Status: in progress. This record captures executed software evidence only; it does not close `DOC_CODE_PASS` or any scientific claim.

## Runtime boundary

- Source snapshot: `D:\Projects\Project_Anode_Fit\Codex\work\source_snapshots\8ea83fc6825d2e62c360e08d7738ef26d3171914`
- Runtime copy: `D:\Projects\Project_Anode_Fit\Codex\work\audit_runtime\8ea83fc6825d2e62c360e08d7738ef26d3171914`
- Copied packages: `v1.0.19` and `v1.0.23`
- v1.0.23 copy check: 83 source files, 83 runtime files, 0 SHA-256 mismatches before execution
- Python: bundled CPython 3.12.13
- NumPy: 2.3.5
- Git commands: none

## Commands and results

### Syntax compilation

`python -m compileall -q <runtime-v1.0.23>` completed with exit code 0. Bytecode was redirected inside the isolated runtime.

### Main gate harness

`test_gates_v1023.py` completed with exit code 0.

Confirmed software results:

- G1: 30 arrays, v1.0.23 versus v1.0.19, bit-exact, maximum absolute difference 0.
- Auxiliary golden reference: 13/13 arrays bit-exact, maximum absolute difference 0.
- G2: documented worked values and five-point reversible-heat table reproduced at display precision.
- G2 derivative roundtrip: reported maximum complete-versus-finite-difference difference `2.948e-07 mV/K` on the harness grid.
- G3: absent `theta_E` remains bit-exact; the selected `theta_E=700 K` option is live away from the reference temperature.
- `n(T)` appendix checks passed, including analytic-versus-finite-difference width derivative.
- R6-G1: `f_Si=0` blend paths are bit-exact with graphite-only paths.
- R6-G2: the internal mass-to-capacity sweep is finite and numerically continuous.
- R6-G3: numerical integration reproduces the model's own `Q_gr+Q_Si` values.
- R6 coverage: three Si cases instantiate; declared GS-1/GS-2 functions raise `NotImplementedError`.

Scientific limitation of these passes:

- G1 compares v1.0.23 to v1.0.19, not the immediate v1.0.22 baseline.
- G2 and the separately executed 30-point entropy probe compare analytic and numerical paths of the same model.
- R6-G2/G3 do not test the external fixed-total-mass identity. They therefore cannot detect the `1/(1-m_Si)` absolute-capacity inflation identified by the independent normalization probe.
- No main gate tests representation invariance between physically identical Ah/hour and coulomb/second inputs.

### Self-consistent gate harness

First execution from the thread working directory failed with exit code 1:

```text
FileNotFoundError: ...\New project\Anode_Fit_v1.0.23.py
```

Cause: `test_gates_v1023_selfconsistent.py:16` resolves `Anode_Fit_v1.0.23.py` relative to the process current working directory rather than `__file__`.

Re-execution with the runtime v1.0.23 directory as the working directory completed with exit code 0:

- G-E1 frozen recovery passed.
- G-E2 ratio ON/OFF equality at zero coupling passed.
- G-E3 selected same-update Picard comparisons passed.
- G-E4 padded/interior transfer-function comparison passed with relative RMS `3.96e-06`.
- G-E5 selected liveness case passed.

Scientific limitation of these passes:

- G-E3's reference is an iteration of the same approximate update and lacks an independent nonlinear solution, residual convergence record, and asymptotic-order test.
- G-E4 uses a selected padded/flat-boundary case and does not establish an unconditional public FFT boundary contract.
- Passing the harness does not resolve the independent detailed-balance denominator omission in the ratio closure.

## Direct disposition

- `확정`: the tested default and documented numerical paths are internally reproducible in the recorded runtime.
- `확정`: the self-consistent test has a current-working-directory dependency.
- `미검증`: external physical validity, parameter identifiability, real-data accuracy, and universal smoothness.
- `확정`: the existing tests do not exercise the fixed-total-mass blend oracle or hour-to-second representation invariance.

## Next gate conditions

1. Complete the equation-to-symbol traceability matrix.
2. Add external-oracle tests for units and mass normalization.
3. Add an independent nonlinear Volterra reference and convergence study.
4. Reproduce document figures/examples and distinguish code mismatch from invalid document physics.
5. Run a fresh independent refutation of every Critical/High code-fidelity finding.
