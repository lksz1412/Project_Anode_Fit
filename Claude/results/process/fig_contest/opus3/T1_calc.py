# -*- coding: utf-8 -*-
# T1 fig:spine (opus3) — calculation spine N0..N9. This is a flow diagram (no plotted curve),
# so this script documents/verifies the node -> equation -> output-quantity map and the
# per-transition loop membership + the equilibrium/tail branch (eq:branch). It asserts every
# referenced \label exists in the chapter source so the diagram stays consistent with the text.
import re
import os

TEX = r"D:\Projects\Project_Anode_Fit\Claude\docs\v1.0.14\graphite_ica_ch1_v1.0.14.tex"

# node : (label refs used on the node, output quantity, in per-transition loop?)
NODES = [
    ("N0", ["eq:n0map"],                 "sigma_d, |I|, T, Q_cell -> inputs", False),
    ("N1", ["eq:n0map"],                 "V_n = V_app - sigma_d|I|R_n",       False),
    ("N2", ["eq:center"],                "U_j(T) = (-dH+TdS)/F",              True),
    ("N3", ["eq:dUhys", "eq:Ubranch", "eq:center"], "branch center U_j^d",   True),
    ("N4", ["eq:wbase"],                 "width w_j = n_j RT/F",              True),
    ("N5", ["eq:xieq"],                  "xi_eq (logistic)",                  True),
    ("N6", ["eq:eqpeak"],                "equilibrium peak xi_eq(1-xi_eq)/w", True),
    ("N7", ["eq:LV"],                    "lag length L_V",                    True),
    ("N8", ["eq:peakshape", "eq:reversal", "eq:branch"], "causal tail (xi_eq-xi_lag)/L_V", True),
    ("N9", ["eq:branch"],                "sum+interp C_bg + sum_j Q_j[.]",   False),
]

with open(TEX, encoding="utf-8") as f:
    src = f.read()
labels = set(re.findall(r"\\label\{([^}]+)\}", src))

print("node  in-loop  output                              labels(ok?)")
missing = []
for name, labs, out, loop in NODES:
    ok = all(l in labels for l in labs)
    for l in labs:
        if l not in labels:
            missing.append((name, l))
    print(f"{name:4s}  {str(loop):6s}  {out:34s}  {labs} -> {'OK' if ok else 'MISSING'}")

loop_nodes = [n for n, _, _, loop in NODES if loop]
print(f"\nper-transition loop body (j=1..N_p): {' -> '.join(loop_nodes)}")
print("branch at N5->{N6 equilibrium peak (L_V<nu*dgrid), N8 causal tail (else)} merge at N9  [eq:branch]")
print(f"\nmissing labels: {missing if missing else 'none -- all node equation refs resolve'}")
assert not missing, f"unresolved labels: {missing}"
print("PASS: all node equation references exist in chapter source.")
