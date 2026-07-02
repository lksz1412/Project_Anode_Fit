# -*- coding: utf-8 -*-
"""V1013 P2.1 Track 2 figure (S2) -- charge/discharge cell-label vs delithiation
direction correspondence, graphite anode vs LCO cathode.

Purpose: visualize the confirmed direction convention (V1012_P43_verify10.md
B-2, f=+sigma_d, "delithiation progress = +1" applied consistently) -- show
that reading sigma_d=+1 as "delithiation" (NOT as a fixed cell-label) gives
the SAME increasing-with-V S-curve shape for both electrodes, even though
the cell label that maps to sigma_d=+1 flips (discharge for graphite,
charge for LCO).

Uses the ACTUAL func_ksi_eq from Anode_Fit_v1.0.13.py and the REAL tabulated
centers: GRAPHITE_STAGING_LIT[3] (stage 2->1, U=0.085 V) and
LCO_MSMR_LIT[0] (main plateau, U=3.930 V). Ideal width w=n*RT/F (n from the
table) is used in both panels -- this figure is about the DIRECTION
convention, not about the two-phase width status (Part I sec:width scope).
"""
import importlib.util
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

CODE = r"D:\Projects\Project_Anode_Fit\Claude\docs\v1.0.13\Anode_Fit_v1.0.13.py"
OUT = r"D:\Projects\Project_Anode_Fit\Claude\results\process\V1013_P21_fig_S2_direction_map.png"

spec = importlib.util.spec_from_file_location("anodefit_v1013", CODE)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

T = 298.15
sigma_d = +1  # the confirmed slot: +1 = delithiation progress (V1012_P43_verify10.md B-2)

# --- graphite anode: main direction is discharge = delithiation -> sigma_d=+1 IS the
#     cell-label "discharge" (labels coincide, sec:lco-map L309-311) ---
gr = m.GRAPHITE_STAGING_LIT[3]  # stage 2->1 (LiC6), U=0.085 V, real table entry
V_gr = np.linspace(gr['U'] - 0.09, gr['U'] + 0.09, 600)
xi_gr = np.asarray(m.func_ksi_eq(T, V_gr, gr['U'], gr['n'], sigma_d), dtype=float)

# --- LCO cathode: delithiation is CHARGE (cell-label flips), so the sigma_d=+1
#     slot is fed by the CHARGE curve, not by the cell "discharge" label
#     (sec:lco-peak direction-slot rule, confirmed) ---
lco = m.LCO_MSMR_LIT[0]  # main plateau, U=3.930 V, real table entry
V_lco = np.linspace(lco['U'] - 0.09, lco['U'] + 0.09, 600)
xi_lco = np.asarray(m.func_ksi_eq(T, V_lco, lco['U'], lco['n'], sigma_d), dtype=float)

# self-check: both curves must be monotonically non-decreasing in V (delithiation
# progresses upward with V once sigma_d=+1 is read as "delithiation" consistently)
assert np.all(np.diff(xi_gr) >= -1e-12), "graphite xi_eq(V) must be non-decreasing"
assert np.all(np.diff(xi_lco) >= -1e-12), "LCO xi_eq(V) must be non-decreasing"
print("graphite: xi_eq(V) monotonic increasing -- OK (sigma_d=+1 slot <-> cell label 'discharge')")
print("LCO:      xi_eq(V) monotonic increasing -- OK (sigma_d=+1 slot <-> cell label 'charge')")

fig, axes = plt.subplots(1, 2, figsize=(10.5, 4.6))

axes[0].plot(V_gr, xi_gr, color="tab:blue", lw=2)
axes[0].axvline(gr['U'], color="gray", ls=":", lw=1)
axes[0].set_title("(a) graphite anode: cell-label DISCHARGE\n== delithiation (sigma_d=+1 slot)")
axes[0].set_xlabel("V [V] vs Li/Li+  (U=0.085 V, stage 2->1)")
axes[0].set_ylabel(r"$\xi_{eq}$ (delithiation progress)")
axes[0].annotate("delithiation direction ->", xy=(0.62, 0.30), xycoords="axes fraction",
                  fontsize=8, color="tab:blue")

axes[1].plot(V_lco, xi_lco, color="tab:red", lw=2)
axes[1].axvline(lco['U'], color="gray", ls=":", lw=1)
axes[1].set_title("(b) LCO cathode: cell-label CHARGE\n== delithiation (sigma_d=+1 slot)")
axes[1].set_xlabel("V [V] vs Li/Li+  (U=3.930 V, main plateau)")
axes[1].set_ylabel(r"$\xi_{eq}$ (delithiation progress)")
axes[1].annotate("delithiation direction ->", xy=(0.62, 0.30), xycoords="axes fraction",
                  fontsize=8, color="tab:red")

for ax in axes:
    ax.axhline(0.5, color="gray", ls=":", lw=0.8)
    ax.set_ylim(-0.02, 1.02)

fig.suptitle("Track 2 fig (S2): sigma_d=+1 slot = delithiation, cell-label flips\n"
             "graphite: discharge->delithiation | LCO: charge->delithiation (both curves rise identically)")
fig.tight_layout(rect=[0, 0, 1, 0.88])
fig.savefig(OUT, dpi=160)
print(f"saved: {OUT}")
