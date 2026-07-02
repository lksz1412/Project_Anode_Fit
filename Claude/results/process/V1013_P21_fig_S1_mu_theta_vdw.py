"""
V1013 P2.1 draft S1 -- Figure candidate for Part 0 sec:sm-meanfield.
Purpose: mean-field chemical potential mu(theta)-mu0 in units of RT, for several
Omega/RT ratios -- shows the monotonic -> van-der-Waals-loop (non-monotonic)
transition at Omega/RT=2, matching the double-well curvature flip in
V1013_P21_fig_S1_gxi_doublewell.py (same equation family, first derivative view).

[mu(theta)-mu0]/RT = ln[theta/(1-theta)] + (Omega/RT)*(1-2*theta)

Output: V1013_P21_fig_S1_mu_theta_vdw.png, 300 dpi, ASCII-only labels.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

theta = np.linspace(0.003, 0.997, 3000)
logit = np.log(theta / (1 - theta))

omega_over_RT = [0.0, 1.0, 2.0, 3.0, 4.0]

fig, ax = plt.subplots(figsize=(6.2, 4.4))
colors = plt.cm.plasma(np.linspace(0.1, 0.85, len(omega_over_RT)))

for w_rt, c in zip(omega_over_RT, colors):
    mu = logit + w_rt * (1 - 2 * theta)
    label = f"Omega/RT={w_rt:.0f}" + ("  (critical)" if w_rt == 2.0 else "")
    ax.plot(theta, mu, color=c, lw=1.8, label=label)
    if w_rt > 2.0:
        u = np.sqrt(1.0 - 2.0 / w_rt)
        for xs in (0.5 * (1 - u), 0.5 * (1 + u)):
            mu_s = np.log(xs / (1 - xs)) + w_rt * (1 - 2 * xs)
            ax.plot(xs, mu_s, "o", color=c, ms=4)

ax.axhline(0, color="0.7", lw=0.6)
ax.axvline(0.5, color="0.7", lw=0.6, ls=":")
ax.set_xlabel(r"$\theta$  (occupation)")
ax.set_ylabel(r"$[\mu(\theta)-\mu^0]/RT$")
ax.set_title("Mean-field chemical potential vs occupation\n(non-monotonic 'loop' for Omega>2RT = phase separation)")
ax.legend(fontsize=8, loc="upper left")
ax.set_xlim(0, 1)
ax.set_ylim(-8, 8)
fig.tight_layout()
fig.savefig("V1013_P21_fig_S1_mu_theta_vdw.png", dpi=300)
print("saved V1013_P21_fig_S1_mu_theta_vdw.png")

# --- numeric self-check: mu(theta) is antisymmetric about theta=1/2 (mu(1/2)=0 always) ---
for w_rt in omega_over_RT:
    mu_half = np.log(0.5 / 0.5) + w_rt * (1 - 2 * 0.5)
    print(f"Omega/RT={w_rt:.1f}  mu(1/2)-mu0 = {mu_half:+.6f} RT  (must be exactly 0)")
