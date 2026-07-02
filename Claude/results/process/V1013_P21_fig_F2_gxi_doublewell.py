# -*- coding: ascii -*-
"""V1013_P21_fig_F2_gxi_doublewell.py  (draft F2, Part 0 sec 0.3)

Regular-solution composition free energy (mixing part, per mole of sites,
in units of RT), evaluated (no fabrication):

    f(xi)/RT = xi ln xi + (1-xi) ln(1-xi) + (Omega/RT) xi (1-xi)

for Omega/RT in {0, 1, 2, 2.5, 3}.  Shows single well -> flat quartic
onset at Omega = 2RT -> double well; spinodal points xi_s = (1 +- u)/2,
u = sqrt(1 - 2RT/Omega), marked for Omega/RT = 2.5, 3.

Outputs: PNG + TikZ coordinate lists (document tikzpicture convention).
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

xi = np.linspace(1e-4, 1 - 1e-4, 2001)
omegas = [0.0, 1.0, 2.0, 2.5, 3.0]          # Omega / RT
colors = ["#777777", "#4a8a1a", "#1a4a8a", "#c07820", "#c0392b"]

def f_over_RT(x, om):
    return x * np.log(x) + (1 - x) * np.log(1 - x) + om * x * (1 - x)

fig, ax = plt.subplots(figsize=(5.6, 3.8))
for om, c in zip(omegas, colors):
    ax.plot(xi, f_over_RT(xi, om), color=c, lw=1.6, label="Omega = %.1f RT" % om)
    if om > 2.0:
        u = np.sqrt(1 - 2.0 / om)
        for xs in (0.5 * (1 - u), 0.5 * (1 + u)):
            ax.plot(xs, f_over_RT(np.array([xs]), om), "o", color=c, ms=4)
ax.set_xlabel("xi")
ax.set_ylabel("f(xi)/RT  (mixing part)")
ax.set_title("g(xi) mixing part: double-well onset at Omega = 2RT", fontsize=11)
ax.legend(fontsize=8, loc="lower center")
fig.tight_layout()
fig.savefig(__file__.replace(".py", ".png"), dpi=160)

# ---- TikZ coordinate emission ----
print("% TikZ coordinates for fig sm-gxi (x = xi, y = f/RT)")
for om in omegas:
    xs = np.concatenate([[0.004, 0.01, 0.02, 0.04], np.linspace(0.07, 0.93, 19),
                         [0.96, 0.98, 0.99, 0.996]])
    ys = f_over_RT(xs, om)
    pts = " ".join("(%.3f,%.4f)" % (x, y) for x, y in zip(xs, ys))
    print("%% Omega=%.1fRT" % om)
    print("\\draw plot[smooth] coordinates {%s};" % pts)
for om in (2.5, 3.0):
    u = np.sqrt(1 - 2.0 / om)
    print("%% Omega=%.1fRT: u=%.4f xi_s-=%.4f xi_s+=%.4f f(xi_s)/RT=%.4f"
          % (om, u, 0.5 * (1 - u), 0.5 * (1 + u),
             f_over_RT(np.array([0.5 * (1 - u)]), om)[0]))
# corner checks quoted in the self-check record
print("%% check Omega=3RT: f(0.5)/RT=%.4f  f(0.07)/RT=%.4f (doc fig:doublewell ~0.057/-0.058)"
      % (f_over_RT(np.array([0.5]), 3.0)[0], f_over_RT(np.array([0.07]), 3.0)[0]))
