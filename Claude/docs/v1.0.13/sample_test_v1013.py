# -*- coding: utf-8 -*-
"""Anode_Fit v1.0.13 -- sample test figure (P4.4; English/ASCII labels only, glyph-safe).

Uses only v1.0.13 functions/classes (no re-implementation):
    GraphiteAnodeDischargeDQDV, LCOCathodeDQDV, func_dSe_molar,
    GRAPHITE_STAGING_LIT, LCO_MSMR_LIT, and the reversible_heat method.
Panels (2x2):
    (a) graphite anode dQ/dV (discharge, 298 K): default n=1 vs fitted n=0.12
    (b) LCO cathode dQ/dV (MSMR isomorphism) at three C-rates
    (c) reversible heat q_rev = -I*T*(dU/dT) for graphite and LCO
    (d) LCO electronic entropy MIT gate dS_e(x)
Output: sample_test_v1013.png (same folder, dpi=150). Deterministic (no RNG).
"""
import sys, importlib.util, copy
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
matplotlib.rcParams["font.family"] = "DejaVu Sans"      # ASCII-safe default font
matplotlib.rcParams["axes.unicode_minus"] = False        # avoid minus-glyph issues
matplotlib.rcParams["mathtext.default"] = "regular"

CODE = r"D:\Projects\Project_Anode_Fit\Claude\docs\v1.0.13\Anode_Fit_v1.0.13.py"
OUT = r"D:\Projects\Project_Anode_Fit\Claude\docs\v1.0.13\sample_test_v1013.png"
spec = importlib.util.spec_from_file_location("anodefit", CODE)
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)

# ---- instantiate v1.0.13 classes (representative parameters) ----
gr = m.GraphiteAnodeDischargeDQDV(m.GRAPHITE_STAGING_LIT, x=0.5, Rn=0.01, Cbg=0.0)
lco = m.LCOCathodeDQDV(m.LCO_MSMR_LIT, x=0.5, Rn=0.01, Cbg=0.0)

# fitted graphite: narrow the phenomenological width (n per transition)
# so the 4 staging transitions separate ('n' takes precedence over 'w' fallback)
fit_staging = copy.deepcopy(m.GRAPHITE_STAGING_LIT)
for tr in fit_staging:
    tr["n"] = 0.12                       # phenomenological free fit width (model unchanged)
gr_fit = m.GraphiteAnodeDischargeDQDV(fit_staging, x=0.5, Rn=0.01, Cbg=0.0)

Vg = np.linspace(0.03, 0.34, 1400)       # graphite anode window [V vs Li/Li+]
Vc = np.linspace(3.75, 4.15, 1200)       # LCO cathode window [V vs Li/Li+]

fig, ax = plt.subplots(2, 2, figsize=(13, 9.5))
fig.suptitle("Anode_Fit v1.0.13 - sample test (graphite anode + LCO cathode + reversible heat)",
             fontsize=13, fontweight="bold")

# (a) graphite dQ/dV: default (n=1, merged bell) vs fitted (n=0.12, 4 staging separated)
yg_def = np.asarray(gr.dqdv(Vg, T=298.15, I_abs=0.05, Q_cell=1.0, s=+1))
yg_fit = np.asarray(gr_fit.dqdv(Vg, T=298.15, I_abs=0.05, Q_cell=1.0, s=+1))
ax[0, 0].plot(Vg, yg_def, "C0", lw=1.8, label="default n=1 (broad, merged bell)")
ax[0, 0].plot(Vg, yg_fit, "C3", lw=1.6, label="fitted n=0.12 (4 staging resolved)")
for U in (0.210, 0.140, 0.120, 0.085):
    ax[0, 0].axvline(U, color="gray", ls=":", lw=0.7)
ax[0, 0].set_title("(a) Graphite anode dQ/dV (discharge, 298 K, |I|=0.05)")
ax[0, 0].set_xlabel("V [V vs Li/Li+]")
ax[0, 0].set_ylabel("dQ/dV [Q_cell/V]")
ax[0, 0].legend(fontsize=8, loc="upper right")
ax[0, 0].text(0.02, 0.95, "phenomenological width w = free fit parameter\n"
              "(two-phase bell = intended apparent-U distribution)",
              transform=ax[0, 0].transAxes, fontsize=7.5, va="top", color="0.35")

# (b) LCO cathode dQ/dV (MSMR isomorphism) at three C-rates via curve() facade
for c_rate, lab in [(0.02, "0.02C"), (0.05, "0.05C"), (0.2, "0.2C")]:
    ax[0, 1].plot(Vc, lco.curve(Vc, direction="discharge", c_rate=c_rate,
                                Q_cell=1.0, T=298.15),
                  lw=1.5, label="discharge " + lab)
ax[0, 1].set_title("(b) LCO cathode dQ/dV (MSMR isomorphism, 298 K)")
ax[0, 1].set_xlabel("V [V vs Li/Li+]")
ax[0, 1].set_ylabel("dQ/dV [Q_cell/V]")
ax[0, 1].legend(fontsize=8)

# (c) reversible heat q_rev = -I*T*(dU/dT) (T applied once), I = 1 A
qg = np.asarray(gr.reversible_heat(Vg, T=298.15, I=1.0))
ql = np.asarray(lco.reversible_heat(Vc, T=298.15, I=1.0))
ax[1, 0].plot(Vg, qg, "C0", lw=1.6, label="graphite (bottom axis)")
axb = ax[1, 0].twiny()
axb.plot(Vc, ql, "C3", lw=1.6)
axb.set_xlabel("V cathode [V vs Li/Li+]", color="C3")
ax[1, 0].plot([], [], "C3", lw=1.6, label="LCO (top axis)")
ax[1, 0].axhline(0, color="k", lw=0.5, ls=":")
ax[1, 0].fill_between(Vg, qg, 0, where=(qg < 0), color="C0", alpha=0.15)
ax[1, 0].set_title("(c) Reversible heat q_rev = -I*T*(dU/dT), I = 1 A")
ax[1, 0].set_xlabel("V anode [V vs Li/Li+]")
ax[1, 0].set_ylabel("q_rev [W]")
ax[1, 0].legend(fontsize=8, loc="lower left")

# (d) electronic entropy MIT gate dS_e(x) -- func_dSe_molar
xx = np.linspace(0.2, 1.0, 400)
x_mit_demo = float(m.LCO_MSMR_LIT[0]["x_MIT"])  # v1.0.13 loop B: T1 realigned to physical anchor 0.85
ax[1, 1].plot(xx, m.func_dSe_molar(xx, 298.15, 13.0, x_mit_demo, 0.05), "C3", lw=1.8,
              label=f"x_MIT = {x_mit_demo:.2f} (LCO_MSMR_LIT = physical anchor)")
ax[1, 1].plot(xx, m.func_dSe_molar(xx, 298.15, 13.0, 0.50, 0.05), "C1", lw=1.4, ls="--",
              label="x_MIT = 0.50 (pre-v1.0.13 tier-C demo, reference)")
ax[1, 1].axhline(-46, color="gray", ls=":", lw=0.8)
ax[1, 1].set_title("(d) LCO electronic entropy gate dS_e(x) (MIT)")
ax[1, 1].set_xlabel("x in LixCoO2 [-]")
ax[1, 1].set_ylabel("dS_e [J/(mol K)]")
ax[1, 1].legend(fontsize=8, loc="lower right")

plt.tight_layout(rect=(0, 0, 1, 0.97))
plt.savefig(OUT, dpi=150)

# ---- console verification (report only; no physics assertion) ----
def n_peaks(y):
    return int(sum(1 for i in range(1, len(y) - 1)
                   if y[i] > y[i - 1] and y[i] >= y[i + 1] and y[i] > 0.3))

def finite(y):
    return bool(np.all(np.isfinite(y)))

print(f"saved: {OUT}")
print(f"(a) graphite finite={finite(yg_def) and finite(yg_fit)} | "
      f"local maxima: default n=1 -> {n_peaks(yg_def)} | fitted n=0.12 -> {n_peaks(yg_fit)}")
yl_02 = np.asarray(lco.curve(Vc, direction="discharge", c_rate=0.2, Q_cell=1.0, T=298.15))
print(f"(b) LCO 0.2C finite={finite(yl_02)} | max dQ/dV={yl_02.max():.3f} "
      f"@V={Vc[int(np.argmax(yl_02))]:.3f}")
print(f"(c) q_rev finite={finite(qg) and finite(ql)} | "
      f"graphite [{qg.min():.3f},{qg.max():.3f}] W | LCO [{ql.min():.3f},{ql.max():.3f}] W")
print(f"(d) dS_e gate depth @x_MIT: "
      f"{float(m.func_dSe_molar(0.85, 298.15, 13.0, 0.85, 0.05)):.2f} J/(mol K) (target ~ -46)")
print("=== SAMPLE TEST v1.0.13 DONE ===")
