"""T2 fig:staging — gallery-filling geometry + U-axis tick positions.

The figure itself is a structural schematic (graphene sheets + intercalated
Li occupancy per stage), not a fitted curve, so "numeric evaluation" here
means: (1) the column/gallery layout arithmetic used for the tikz
coordinates, and (2) the four transition potentials U_j, which are the
tier-B/tier-C literature initial values already boxed in tab:staging
(graphite_ica_ch1_v1.0.14.tex, lines 1981-1985) — reproduced here, not
re-derived, so the figure's bottom axis is traceable to that table.
"""

COLW = 0.85          # column width [tikz x units]
COL_GAP_CENTERS = 1.4  # spacing between successive column x-origins
STAGES = ["stage 4", "stage 3", "stage 2L", "stage 2", "stage 1"]

# column x-origins (left edge) and centers
col_x0 = [i * COL_GAP_CENTERS for i in range(5)]
col_center = [x0 + COLW / 2 for x0 in col_x0]

# transition U initial values, tab:staging (V vs Li/Li+), in stage order
# 4->3, 3->2L, 2L->2, 2->1
TRANSITIONS = [
    ("4->3", 0.210),
    ("3->2L", 0.140),
    ("2L->2", 0.120),
    ("2->1", 0.085),
]

# each transition sits at the midpoint between the two adjacent column
# centers it connects (interface between column i and i+1)
transition_x = [0.5 * (col_center[i] + col_center[i + 1]) for i in range(4)]

if __name__ == "__main__":
    print("column centers:", [f"{c:.3f}" for c in col_center])
    print("stage labels  :", STAGES)
    print()
    print(f"{'transition':10s} {'U [V]':8s} {'x position':10s}")
    for (name, u), x in zip(TRANSITIONS, transition_x):
        print(f"{name:10s} {u:<8.3f} {x:<10.3f}")
    # sanity: transitions must lie strictly between their flanking columns
    for i, x in enumerate(transition_x):
        assert col_center[i] < x < col_center[i + 1]
    # sanity: U strictly decreasing left->right, matching discharge
    # (delithiation) direction drawn right-to-left across the gallery
    # columns per sec:notation sign convention (V increases as stage
    # number falls during discharge)
    us = [u for _, u in TRANSITIONS]
    assert all(us[i] > us[i + 1] for i in range(len(us) - 1))
    print("\nOK: transitions interior to flanking columns; U monotone decreasing L->R.")
