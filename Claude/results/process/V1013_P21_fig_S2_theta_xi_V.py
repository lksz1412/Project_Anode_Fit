# -*- coding: utf-8 -*-
"""V1013 P2.1 Part 0 figure (S2) -- single-site/lattice occupation logistic vs V.

Purpose: visualize eq:sm-theta / eq:xieq -- the equilibrium occupation theta(V)
and its complement (delithiation progress) xi(V) = 1 - theta(V), evaluated at
three temperatures, to show the RT/F width scaling explicitly (no shape
change, only width change with T).

This script imports the ACTUAL codebase functions (func_ksi_eq, func_w) from
Anode_Fit_v1.0.13.py -- values are real formula evaluations, not fabricated.
Reference transition: GRAPHITE_STAGING_LIT[3] (stage 2->1, U=0.085 V, the
LiC6 two-phase transition) is used only for its center U -- the width plotted
here is the IDEAL w = RT/F (n=1), which is what Part 0 Step 1/4 derives
(the two-phase width status itself is Part I's sec:width discussion, not
reproduced here).
"""
import importlib.util
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

CODE = r"D:\Projects\Project_Anode_Fit\Claude\docs\v1.0.13\Anode_Fit_v1.0.13.py"
OUT = r"D:\Projects\Project_Anode_Fit\Claude\results\process\V1013_P21_fig_S2_theta_xi_V.png"

spec = importlib.util.spec_from_file_location("anodefit_v1013", CODE)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

R, F = m.R, m.F
U_center = m.GRAPHITE_STAGING_LIT[3]['U']  # 0.085 V, stage 2->1 (LiC6), real table value
n_j = 1.0  # ideal width multiplicity (Part 0 scope: Omega=0 limit)

V = np.linspace(U_center - 0.09, U_center + 0.09, 800)
temps = [260.0, 298.15, 340.0]
sigma_d = +1  # discharge convention (main text default), delithiation = +1

fig, axes = plt.subplots(1, 2, figsize=(10.5, 4.4))

for T in temps:
    w = float(m.func_w(T, n_j))
    xi_eq = np.asarray(m.func_ksi_eq(T, V, U_center, n_j, sigma_d), dtype=float)
    theta_eq = 1.0 - xi_eq
    axes[0].plot(V, xi_eq, label=f"T={T:.2f} K (w=RT/F={w*1000:.1f} mV)")
    axes[1].plot(V, theta_eq, label=f"T={T:.2f} K")

# self-check printed to stdout: center value must be exactly 0.5 at V=U_center
for T in temps:
    w = float(m.func_w(T, n_j))
    xi_at_center = float(m.func_ksi_eq(T, np.array([U_center]), U_center, n_j, sigma_d)[0])
    assert abs(xi_at_center - 0.5) < 1e-12, "center occupation must be exactly 1/2"
    print(f"T={T:.2f} K: w=RT/F={w:.6f} V, xi_eq(V=U)={xi_at_center:.6f} (expect 0.5)")

axes[0].axvline(U_center, color="gray", ls=":", lw=1)
axes[0].axhline(0.5, color="gray", ls=":", lw=1)
axes[0].set_xlabel("V [V]  (graphite half-cell, stage 2->1 center U=0.085 V)")
axes[0].set_ylabel(r"$\xi_{eq}$  (delithiation progress)")
axes[0].set_title("(a) xi_eq(V), sigma_d=+1 (discharge = delithiation)")
axes[0].legend(fontsize=8, loc="upper left")

axes[1].axvline(U_center, color="gray", ls=":", lw=1)
axes[1].axhline(0.5, color="gray", ls=":", lw=1)
axes[1].set_xlabel("V [V]")
axes[1].set_ylabel(r"$\theta_{eq}=1-\xi_{eq}$  (Li occupation)")
axes[1].set_title("(b) theta_eq(V) = 1 - xi_eq(V)")
axes[1].legend(fontsize=8, loc="upper right")

fig.suptitle("Part 0 fig 1 (S2): single-site grand-canonical occupation vs V"
             " (eq:sm-theta / eq:xieq, ideal width w=RT/F, real func_ksi_eq)")
fig.tight_layout(rect=[0, 0, 1, 0.94])
fig.savefig(OUT, dpi=160)
print(f"saved: {OUT}")
