#!/usr/bin/env python3
# T1 fig:spine  --  the calculation progress N0..N9 that draws one dQ/dV curve.
# This is a structural (flow) diagram, not a numerically-sampled curve; T1_calc.py fixes the
# node y-ladder and the branch geometry so the layout is reproducible/verifiable.
# Each spine node carries: N-index, produced quantity, its governing equation label.
# Per-transition loop = N2..N8 (repeated j=1..Np).  Branch at the peak stage:
#   equilibrium species (N6, eq:eqpeak)  vs  causal tail (N8, eq:peakshape) via mode switch eq:branch.
NODES = [
    ("input", "V_app, dir->sigma_d, c-rate->|I|, T, Q_cell", "given"),
    ("N0", "map inputs -> sigma_d,|I|",            "eq:n0map"),
    ("N1", "polarization V_n=V_app-sigma_d|I|R_n", "eq:vn"),
    ("N2", "center U_j(T)=(-dH+T dS)/F",           "eq:center"),
    ("N3", "hysteresis branch U_j^d",              "eq:Ubranch"),
    ("N4", "width w_j=n_j RT/F",                   "eq:wbase"),
    ("N5", "fill xi_eq=logistic[sigma_d(V-U)/w]",  "eq:xieq"),
    ("BR", "mode switch: L_V < nu d_grid ?",       "eq:branch"),
    ("N9", "sum + interp  C_bg + sum_j Q_j[.]",    "eq:sum"),
    ("out", "dQ/dV at V_n",                        "given"),
]
# vertical ladder
y0, dy = 0.0, -1.30
print("# node ladder (x=0 spine), y = y0 + k*dy, dy=%.2f" % dy)
for k,(nid,q,eq) in enumerate(NODES):
    print(f"  {nid:5s} y={y0+k*dy:+.2f}   [{eq:11s}] {q}")

# branch children placed either side of the BR row (index 7) pushed one row down
br_y = y0 + 7*dy
child_y = br_y + dy*0.55
print(f"\n# branch row BR at y={br_y:+.2f}")
print(f"#   left child  N6 equilibrium species  (eq:eqpeak)  at (x=-3.05, y={child_y:+.2f})")
print(f"#   right child N7->N8 causal tail       (eq:peakshape) at (x=+3.05, y={child_y:+.2f})")
print(f"#   N7 lag-length L_V feeds N8           (eq:LV)      at (x=+3.05, y={br_y-0.05:+.2f})")
print("# per-transition loop bracket encloses rows N2..N8 (j=1..Np)")
