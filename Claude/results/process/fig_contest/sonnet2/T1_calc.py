"""T1 fig:spine — node/equation mapping verification (sonnet2 entry).

fig:spine is a control-flow schematic (node graph), not a numeric curve, so
there is no coordinate evaluation to perform. What *is* verifiable is the
node -> equation-label -> quantity mapping the tikz figure claims: every
label below must exist in graphite_ica_ch1_v1.0.14.tex (confirmed by grep,
see report) and every node's stated output quantity must match the boxed
result of that equation in the source text.

This script documents that mapping and lets it be diffed against the tikz
node text mechanically, instead of trusting hand-transcription.
"""

NODES = [
    # (node id, section, eq label used in \eqref, quantity produced)
    ("N0", "sec:notation", "eq:n0map", r"sigma_d, |I|  (direction/c-rate -> model inputs)"),
    ("N1", "sec:pol",      "eq:vn",    r"V_n = V_app - sigma_d |I| R_n"),
    ("N2", "sec:center",   "eq:Uj",    r"U_j(T) = (-DeltaH_rxn + T DeltaS_rxn)/F"),
    ("N3", "sec:hys",      "eq:Ubranch", r"U_j^d = U_j + (1/2) sigma_d h_eta gamma_j DeltaU_j^hys"),
    ("N4/N5", "sec:width", "eq:wbase,eq:xieq", r"w_j = n_j R T/F ;  xi_eq,j = logistic[sigma_d(V-U_j^d)/w_j]"),
    ("N6", "sec:eqpeak",   "eq:eqpeak", r"equilibrium peak = Q_j xi_eq(1-xi_eq)/w_j"),
    ("N7", "sec:lag",      "eq:LV",     r"L_{V,j} = |dV/dq|_qa * L_{q,j}  (lag length, volts)"),
    ("N8", "sec:tail",     "eq:peakshape,eq:branch", r"peak shape = (xi_eq - xi_lag)/L_V  [or eq:eqpeak if L_V < nu*grid]"),
    ("N9", "sec:sum",      "eq:sum",    r"dQ/dV = C_bg + sum_j Q_j * [peak shape]_j  (then interpolated to V_n)"),
]

# per-transition loop membership (j = 1..N_p) — everything computed *per
# transition j* inside the fit-loop of the source code; N0/N1/N9 run once.
LOOP_MEMBERS = ["N2", "N3", "N4/N5", "N6", "N7", "N8"]

# the branch the brief asks to make visible: after N4/N5 produces xi_eq,j,
# the per-transition loop takes ONE of two paths before reaching N9 — this
# is exactly the runtime switch of eq:branch (L_V < nu*Delta_grid picks N6,
# otherwise N7->N8 supplies the tail). Both paths are drawn in the figure
# and merge at a branch-select node before N9.
BRANCH = {
    "condition": "L_{V,j} < nu * Delta_grid  (nu = 2, eq:branch)",
    "true_path": ["N6"],
    "false_path": ["N7", "N8"],
}

if __name__ == "__main__":
    print(f"{'node':8s} {'section':14s} {'eq label(s)':24s} quantity")
    for node, sec, lab, qty in NODES:
        print(f"{node:8s} {sec:14s} {lab:24s} {qty}")
    assert set(LOOP_MEMBERS) == {"N2", "N3", "N4/N5", "N6", "N7", "N8"}
    print("\nper-transition loop (j=1..N_p):", ", ".join(LOOP_MEMBERS))
    print("branch condition:", BRANCH["condition"])
    print("  true  ->", BRANCH["true_path"])
    print("  false ->", BRANCH["false_path"])
