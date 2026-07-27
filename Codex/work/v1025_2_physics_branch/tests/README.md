# v1.0.25.3 conformance tests

Run the complete suite without installing pytest:

```bash
cd Codex/work/v1025_2_physics_branch/tests
python3 run_all.py
```

Run only the manuscript verifier:

```bash
python3 verify_manuscript.py
```

The suite independently checks:

- the complete active preprocessing of the archived blend-labelled curve;
- processed input, stored-8dp parameter, prediction, and residual hashes;
- the stored-profile curve, area, and recomputed \(R^2\);
- physical charge balance, derivative, monotonic admissibility, and implicit
  inversion;
- fixed state orientation versus signed/fixed-sign/magnitude observation maps;
- invalid-domain failures and immutable/call-order-independent objects;
- explicit h\(^{-1}\)-to-s\(^{-1}\) conversion and the SI Eyring formula;
- reversible-heat sign, terminal nonnegative-domain guard, and local network
  entropy production;
- strict monotonic-curve input, explicit causal initial state, and acquisition
  order for time trajectories;
- the complete TeX include graph, orphan sources, duplicate/missing labels and
  references, stable physics identifiers, and the implementation-language
  boundary.

`verify_manuscript.py` permits implementation symbols only in
`appendices/implementation_interface.tex`. Source paths, commits, work history,
and recorded test output remain external-ledger material even in that appendix.
