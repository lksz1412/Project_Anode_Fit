# -*- coding: ascii -*-
"""V1013_P21_fig_F2_mu_theta.py  (draft F2, Part 0 sec 0.3)

Mean-field lattice-gas chemical potential (interaction quotient, in RT),
evaluated (no fabrication):

    (mu - mu0)/RT = ln[theta/(1-theta)] + (Omega/RT)(1 - 2 theta)

for Omega/RT in {0, 2, 3}.  Shows: monotone (ideal / threshold) ->
non-monotone above Omega = 2RT; extrema sit at the spinodal
theta_s = (1 -+ u)/2 (complement coordinate of xi_s).

Outputs: PNG + TikZ coordinate lists (document tikzpicture convention).
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

th = np.linspace(0.02, 0.98, 2001)
omegas = [0.0, 2.0, 3.0]
colors = ["#777777", "#1a4a8a", "#c0392b"]

def mu_over_RT(t, om):
    return np.log(t / (1 - t)) + om * (1 - 2 * t)

fig, ax = plt.subplots(figsize=(5.6, 3.8))
for om, c in zip(omegas, colors):
    ax.plot(th, mu_over_RT(th, om), color=c, lw=1.6, label="Omega = %.0f RT" % om)
u3 = np.sqrt(1 - 2.0 / 3.0)
for ts in (0.5 * (1 - u3), 0.5 * (1 + u3)):
    ax.plot(ts, mu_over_RT(np.array([ts]), 3.0), "o", color="#c0392b", ms=4)
ax.axhline(0.0, color="0.6", lw=0.6, ls=":")
ax.set_xlabel("theta")
ax.set_ylabel("(mu - mu0)/RT")
ax.set_title("mu(theta): non-monotone above Omega = 2RT", fontsize=11)
ax.set_ylim(-4.5, 4.5)
ax.legend(fontsize=8, loc="upper left")
fig.tight_layout()
fig.savefig(__file__.replace(".py", ".png"), dpi=160)

# ---- TikZ coordinate emission ----
print("% TikZ coordinates for fig sm-mu (x = theta, y = (mu-mu0)/RT, clipped 0.03..0.97)")
for om in omegas:
    xs = np.concatenate([[0.03, 0.05], np.linspace(0.08, 0.92, 22), [0.95, 0.97]])
    ys = mu_over_RT(xs, om)
    pts = " ".join("(%.3f,%.4f)" % (x, y) for x, y in zip(xs, ys))
    print("%% Omega=%.0fRT" % om)
    print("\\draw plot[smooth] coordinates {%s};" % pts)
print("%% Omega=3RT extrema: theta_s-=%.4f mu/RT=%.4f ; theta_s+=%.4f mu/RT=%.4f"
      % (0.5 * (1 - u3), mu_over_RT(np.array([0.5 * (1 - u3)]), 3.0)[0],
         0.5 * (1 + u3), mu_over_RT(np.array([0.5 * (1 + u3)]), 3.0)[0]))
print("%% Omega=2RT: dmu/dtheta at 1/2 = 4 - 2*2 = 0 (flat inflection) ; value mu(1/2)=%.4f"
      % mu_over_RT(np.array([0.5]), 2.0)[0])
