import numpy as np
import matplotlib.pyplot as plt


def logistic(z):
    return 1.0 / (1.0 + np.exp(-z))


u = np.linspace(-6.0, 6.0, 800)
xi_plus = logistic(u)
xi_minus = logistic(-u)

fig, ax = plt.subplots(figsize=(7.2, 4.6), dpi=180)
ax.plot(u, xi_plus, lw=2.4, color="#1f77b4", label="delithiation slot: sigma_d=+1")
ax.plot(u, xi_minus, lw=2.4, color="#d62728", label="lithiation slot: sigma_d=-1")
ax.plot(u, xi_plus * (1.0 - xi_plus), lw=1.7, color="#2ca02c", ls="--",
        label="peak shape: xi(1-xi)")

ax.axvline(0.0, color="0.25", lw=0.9)
ax.axhline(0.5, color="0.65", lw=0.8, ls=":")
ax.set_xlim(-6.0, 6.0)
ax.set_ylim(-0.04, 1.04)
ax.set_xlabel("u = (V - U) / w")
ax.set_ylabel("dimensionless response")
ax.set_title("LCO direction slot: equilibrium complement, same peak shape")

ax.annotate("LCO charge: V up, delithiation, sigma_d=+1",
            xy=(2.7, logistic(2.7)), xytext=(0.15, 0.83),
            arrowprops={"arrowstyle": "->", "lw": 1.1, "color": "#1f77b4"},
            color="#1f77b4", fontsize=8.8)
ax.annotate("LCO discharge: V down, lithiation, sigma_d=-1",
            xy=(-2.7, logistic(2.7)), xytext=(-5.75, 0.72),
            arrowprops={"arrowstyle": "->", "lw": 1.1, "color": "#d62728"},
            color="#d62728", fontsize=8.8)
ax.annotate("direction-dependent slots: polarization, branch, tail",
            xy=(0.0, 0.25), xytext=(-4.9, 0.18),
            arrowprops={"arrowstyle": "->", "lw": 1.0, "color": "0.25"},
            color="0.15", fontsize=8.5)

ax.legend(loc="lower right", fontsize=8.1, frameon=False)
ax.grid(True, color="0.9", lw=0.7)
fig.tight_layout()

out = __file__.replace(".py", ".png")
fig.savefig(out, bbox_inches="tight")
print(out)
