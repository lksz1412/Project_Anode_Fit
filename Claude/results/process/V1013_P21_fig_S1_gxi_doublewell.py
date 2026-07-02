"""
V1013 P2.1 draft S1 -- Figure candidate for Part 0 sec:sm-meanfield.
Purpose: regular-solution free energy g(xi)/RT (linear+constant reference dropped)
for several Omega/RT ratios, showing the single-well -> double-well transition at
the mean-field critical ratio Omega/RT = 2 (eq:sm-spinodal in the draft).

g(xi) - g0 = RT[xi ln(xi) + (1-xi) ln(1-xi)] + Omega*xi*(1-xi)

Output: V1013_P21_fig_S1_gxi_doublewell.png, 300 dpi, ASCII-only labels.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

xi = np.linspace(0.003, 0.997, 3000)
mix = xi * np.log(xi) + (1 - xi) * np.log(1 - xi)  # dimensionless, = S_config/(-R) shape

omega_over_RT = [0.0, 1.0, 2.0, 3.0, 4.0]

fig, ax = plt.subplots(figsize=(6.2, 4.4))
colors = plt.cm.plasma(np.linspace(0.1, 0.85, len(omega_over_RT)))

for w_rt, c in zip(omega_over_RT, colors):
    g_over_RT = mix + w_rt * xi * (1 - xi)
    label = f"Omega/RT={w_rt:.0f}" + ("  (critical)" if w_rt == 2.0 else "")
    ax.plot(xi, g_over_RT, color=c, lw=1.8, label=label)

    # mark spinodal points for Omega/RT > 2 (real evaluation, not decorative)
    if w_rt > 2.0:
        u = np.sqrt(1.0 - 2.0 / w_rt)
        for xs in (0.5 * (1 - u), 0.5 * (1 + u)):
            g_s = xs * np.log(xs) + (1 - xs) * np.log(1 - xs) + w_rt * xs * (1 - xs)
            ax.plot(xs, g_s, "o", color=c, ms=4)

ax.set_xlabel(r"$\xi$  (progress fraction)")
ax.set_ylabel(r"$[g(\xi)-g_0]/RT$")
ax.set_title("Regular-solution free energy vs progress fraction\n(dots = spinodal points, eq:sm-spinodal)")
ax.legend(fontsize=8, loc="upper center", ncol=2)
ax.set_xlim(0, 1)
fig.tight_layout()
fig.savefig("V1013_P21_fig_S1_gxi_doublewell.png", dpi=300)
print("saved V1013_P21_fig_S1_gxi_doublewell.png")

# --- numeric self-check: g''(xi) sign at xi=0.5 for each Omega/RT ---
for w_rt in omega_over_RT:
    gpp_half = 1.0 / (0.5 * 0.5) - 2.0 * w_rt  # RT*(1/[xi(1-xi)]) - 2*Omega, in units of RT
    print(f"Omega/RT={w_rt:.1f}  g''(1/2)/RT = {gpp_half:+.3f}  ({'unstable(<0)' if gpp_half<0 else 'stable(>=0)'})")
