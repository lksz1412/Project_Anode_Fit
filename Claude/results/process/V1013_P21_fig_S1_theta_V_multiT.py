"""
V1013 P2.1 draft S1 -- Figure candidate for Part 0 sec:sm-echem.
Purpose: single-site (Omega=0) equilibrium occupation xi_eq(V) at several temperatures,
showing that the logistic width w=RT/F broadens with T (ideal-limit prediction,
eq:sm-xieq-ideal in the draft). Real equation evaluation, no hand-drawn coordinates.

xi_eq(V) = 1 / (1 + exp[-(V-U)/w]),   w = R*T/F   (s=+1 fixed derivation sign)

Output: V1013_P21_fig_S1_theta_V_multiT.png (same directory), 300 dpi, ASCII-only labels.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

R = 8.314462618      # J/(mol K)
F = 96485.33212       # C/mol
U = 0.0               # V, reference center (arbitrary zero)

T_list = [233.15, 273.15, 298.15, 323.15, 363.15]  # K
V = np.linspace(-0.15, 0.15, 2000)  # V, relative to U

fig, ax = plt.subplots(figsize=(6.0, 4.2))
colors = plt.cm.viridis(np.linspace(0.15, 0.85, len(T_list)))

for T, c in zip(T_list, colors):
    w = R * T / F  # V
    xi_eq = 1.0 / (1.0 + np.exp(-(V - U) / w))
    ax.plot(V * 1000, xi_eq, color=c, lw=1.8,
            label=f"T={T-273.15:.0f} C, w=RT/F={w*1000:.1f} mV")

# sanity markers: at V=U, xi_eq=1/2 for every T (independent of w)
ax.axhline(0.5, color="0.6", lw=0.6, ls=":")
ax.axvline(0.0, color="0.6", lw=0.6, ls=":")

ax.set_xlabel("V - U  [mV]  (s = +1 fixed derivation sign)")
ax.set_ylabel(r"$\xi_{eq}$  (single-site occupation, delithiated fraction)")
ax.set_title("Single-site grand-canonical occupation vs V, Omega=0\n(width w=RT/F broadens with T)")
ax.legend(fontsize=8, loc="upper left")
ax.set_xlim(-150, 150)
ax.set_ylim(0, 1)
fig.tight_layout()
fig.savefig("V1013_P21_fig_S1_theta_V_multiT.png", dpi=300)
print("saved V1013_P21_fig_S1_theta_V_multiT.png")

# --- numeric self-check printed to stdout (for the physics self-audit record) ---
for T in T_list:
    w = R * T / F
    xi_at_U = 1.0 / (1.0 + np.exp(-(0.0) / w))
    xi_at_2w = 1.0 / (1.0 + np.exp(-(2 * w) / w))
    print(f"T={T:7.2f} K  w={w*1000:7.3f} mV  xi_eq(V=U)={xi_at_U:.6f}  xi_eq(V=U+2w)={xi_at_2w:.6f}")
