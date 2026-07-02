# -*- coding: ascii -*-
"""V1013_P21_fig_F2_theta_single_site.py  (draft F2, Part 0 sec 0.1/0.4)

Single-site grand-canonical occupancy  theta = 1/(1 + exp[ sF(V-U)/RT ])
evaluated (no fabrication) at three temperatures + the T->0 step limit.
Shows: (i) Fermi-function shape, (ii) thermal width w = RT/F scaling,
(iii) beta->infty step / beta->0 flattening toward 1/2.

Outputs:
  - PNG  : same basename .png (visual check)
  - TikZ : coordinate lists printed to stdout, to paste into the document
           tikzpicture convention (plot[smooth] coordinates {...}).
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

R = 8.314462618      # J/(mol K)
F = 96485.33212      # C/mol

dV = np.linspace(-0.15, 0.15, 601)          # V - U  [V]
temps = [268.15, 298.15, 328.15]            # K
styles = ["-", "-", "-"]
colors = ["#1a4a8a", "#c0392b", "#4a8a1a"]

def theta(dv, T):
    z = F * dv / (R * T)                    # s = +1 derivation convention
    # overflow-safe logistic (same split as code func_ksi_eq)
    return np.where(z >= 0, np.exp(-z) / (1 + np.exp(-z)), 1 / (1 + np.exp(z)))

fig, ax = plt.subplots(figsize=(5.6, 3.6))
for T, c in zip(temps, colors):
    w_mV = 1e3 * R * T / F
    ax.plot(dV * 1e3, theta(dV, T), color=c, lw=1.6,
            label="T = %.0f K  (RT/F = %.1f mV)" % (T, w_mV))
# T->0 step limit
ax.plot([-150, 0, 0, 150], [1, 1, 0, 0], "k--", lw=1.0, label="T -> 0 step limit")
ax.axhline(0.5, color="0.6", lw=0.6, ls=":")
ax.axvline(0.0, color="0.6", lw=0.6, ls=":")
ax.set_xlabel("V - U  [mV]")
ax.set_ylabel("theta (site occupancy)")
ax.set_title("Single-site occupancy theta = 1/(1+exp[F(V-U)/RT])")
ax.legend(fontsize=8, loc="upper right")
ax.set_xlim(-150, 150); ax.set_ylim(-0.02, 1.05)
fig.tight_layout()
fig.savefig(__file__.replace(".py", ".png"), dpi=160)

# ---- TikZ coordinate emission (document convention) ----
print("% TikZ coordinates for fig sm-theta (x = (V-U)/mV /100, y = theta)")
for T in temps:
    xs = np.linspace(-0.15, 0.15, 25)
    ys = theta(xs, T)
    pts = " ".join("(%.3f,%.4f)" % (x * 1e3 / 100.0, y) for x, y in zip(xs, ys))
    print("%% T=%.2f K" % T)
    print("\\draw[thick] plot[smooth] coordinates {%s};" % pts)
# reference values quoted in text
for T in temps:
    print("%% check T=%.2f: RT/F=%.4f mV ; theta(+50mV)=%.4f ; theta(-50mV)=%.4f"
          % (T, 1e3 * R * T / F, theta(np.array([0.05]), T)[0], theta(np.array([-0.05]), T)[0]))
