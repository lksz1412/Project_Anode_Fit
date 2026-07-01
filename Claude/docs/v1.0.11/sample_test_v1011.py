# -*- coding: utf-8 -*-
"""Anode_Fit v1.0.10 — final sample test figure (English/ASCII labels only, glyph-safe).
Uses the v1.0.10 functions/classes: GraphiteAnodeDischargeDQDV, LCOCathodeDQDV,
func_dSe_molar, reversible_heat. One 2x2 summary image."""
import sys, importlib.util, copy
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
matplotlib.rcParams["font.family"] = "DejaVu Sans"     # ASCII+Greek mathtext safe
matplotlib.rcParams["axes.unicode_minus"] = False       # avoid minus-glyph issues
matplotlib.rcParams["mathtext.default"] = "regular"

CODE = r"D:\Projects\Project_Anode_Fit\Claude\docs\v1.0.10\Anode_Fit_v1.0.10.py"
OUT = r"D:\Projects\Project_Anode_Fit\Claude\docs\v1.0.10\figs\Anode_Fit_v1.0.10_sample_test.png"
spec = importlib.util.spec_from_file_location("anodefit", CODE)
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)

# ---- instantiate v1.0.10 classes ----
gr = m.GraphiteAnodeDischargeDQDV(m.GRAPHITE_STAGING_LIT, x=0.5, Rn=0.01, Cbg=0.0)
lco = m.LCOCathodeDQDV(m.LCO_MSMR_LIT, x=0.5, Rn=0.01, Cbg=0.0)

# fitted graphite: narrow the phenomenological width (n per transition) -> 4 staging separate
fit_staging = copy.deepcopy(m.GRAPHITE_STAGING_LIT)
for tr in fit_staging:
    tr["n"] = 0.12                        # phenomenological free fit width (model unchanged)
gr_fit = m.GraphiteAnodeDischargeDQDV(fit_staging, x=0.5, Rn=0.01, Cbg=0.0)

Vg = np.linspace(0.03, 0.34, 1400)
Vc = np.linspace(3.75, 4.15, 1200)
_trapz = getattr(np, "trapezoid", getattr(np, "trapz", None))

fig, ax = plt.subplots(2, 2, figsize=(13, 9.5))
fig.suptitle("Anode_Fit v1.0.10  —  sample test (graphite anode + LCO cathode + reversible heat)",
             fontsize=13, fontweight="bold")

# (a) graphite dQ/dV: default (n=1, merged bell) vs fitted (n=0.12, 4 staging separated)
yg_def = np.asarray(gr.dqdv(Vg, T=298.15, I_abs=0.05, Q_cell=1.0, s=+1))
yg_fit = np.asarray(gr_fit.dqdv(Vg, T=298.15, I_abs=0.05, Q_cell=1.0, s=+1))
ax[0,0].plot(Vg, yg_def, "C0", lw=1.8, label="default n=1  (broad, merged bell)")
ax[0,0].plot(Vg, yg_fit, "C3", lw=1.6, label="fitted n=0.12  (4 staging resolved)")
for U in (0.210, 0.140, 0.120, 0.085):
    ax[0,0].axvline(U, color="gray", ls=":", lw=0.7)
ax[0,0].set_title("(a) Graphite anode dQ/dV  (discharge, 298 K)")
ax[0,0].set_xlabel("V  [V vs Li/Li+]"); ax[0,0].set_ylabel("dQ/dV")
ax[0,0].legend(fontsize=8, loc="upper right")
ax[0,0].text(0.02, 0.95, "phenomenological width w is a free fit\n"
             "(two-phase bell = intended apparent-U distribution)",
             transform=ax[0,0].transAxes, fontsize=7.5, va="top", color="0.35")

# (b) LCO cathode dQ/dV (MSMR)
for I, lab in [(0.02, "0.02C"), (0.05, "0.05C"), (0.2, "0.2C")]:
    ax[0,1].plot(Vc, lco.dqdv(Vc, T=298.15, I_abs=I, Q_cell=1.0, s=+1), lw=1.5, label=f"discharge {lab}")
ax[0,1].set_title("(b) LCO cathode dQ/dV  (MSMR isomorphism)")
ax[0,1].set_xlabel("V  [V vs Li/Li+]"); ax[0,1].set_ylabel("dQ/dV")
ax[0,1].legend(fontsize=8)

# (c) reversible heat q_rev = -I T dU/dT
qg = np.asarray(gr.reversible_heat(Vg, T=298.15, I=1.0))
ql = np.asarray(lco.reversible_heat(Vc, T=298.15, I=1.0))
ax[1,0].plot(Vg, qg, "C0", lw=1.6, label="graphite")
axb = ax[1,0].twiny(); axb.plot(Vc, ql, "C3", lw=1.6, label="LCO"); axb.set_xlabel("V cathode [V]", color="C3")
ax[1,0].axhline(0, color="k", lw=0.5, ls=":")
ax[1,0].fill_between(Vg, qg, 0, where=(qg < 0), color="C0", alpha=0.15)
ax[1,0].set_title(r"(c) Reversible heat  $q_{rev} = -I\,T\,\partial U/\partial T$  (T once)")
ax[1,0].set_xlabel("V anode [V]"); ax[1,0].set_ylabel(r"$q_{rev}$  [W]")
ax[1,0].legend(fontsize=8, loc="lower left")

# (d) electronic entropy MIT gate  dS_e(x)
xx = np.linspace(0.2, 1.0, 400)
ax[1,1].plot(xx, m.func_dSe_molar(xx, 298.15, 13.0, 0.85, 0.05), "C3", lw=1.8,
             label=r"$x_{MIT}=0.85$ (physical anchor)")
ax[1,1].plot(xx, m.func_dSe_molar(xx, 298.15, 13.0, 0.50, 0.05), "C1", lw=1.4, ls="--",
             label=r"$x_{MIT}=0.50$ (code tier-C demo)")
ax[1,1].axhline(-46, color="gray", ls=":", lw=0.8)
ax[1,1].set_title(r"(d) LCO electronic entropy gate  $\Delta S_e(x)$  (MIT)")
ax[1,1].set_xlabel(r"x in Li$_x$CoO$_2$"); ax[1,1].set_ylabel(r"$\Delta S_e$  [J/(mol K)]")
ax[1,1].legend(fontsize=8, loc="lower right")

plt.tight_layout(rect=(0, 0, 1, 0.97))
plt.savefig(OUT, dpi=130)

# ---- console verification (no assertion on physics; just report) ----
def n_peaks(y):
    return int(sum(1 for i in range(1, len(y)-1) if y[i] > y[i-1] and y[i] >= y[i+1] and y[i] > 0.3))
print(f"saved: {OUT}")
print(f"(a) graphite local maxima: default n=1 -> {n_peaks(yg_def)} | fitted n=0.12 -> {n_peaks(yg_fit)}")
print(f"(c) q_rev range: graphite [{qg.min():.3f},{qg.max():.3f}] W | LCO [{ql.min():.3f},{ql.max():.3f}] W")
print(f"(d) dS_e gate depth @x_MIT: {float(m.func_dSe_molar(0.85,298.15,13.0,0.85,0.05)):.2f} J/mol/K (target ~ -46)")
print("=== SAMPLE TEST DONE ===")
