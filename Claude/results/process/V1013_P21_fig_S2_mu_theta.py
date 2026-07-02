# -*- coding: utf-8 -*-
"""V1013 P2.1 Part 0 figure (S2) -- mean-field chemical potential mu(theta) vs Omega.

Purpose: visualize eq:mu -- mu_Li(theta) - mu^0 = RT*ln[theta/(1-theta)] + Omega*(1-2*theta)
for the same real Omega spread as fig_S2_gxi_doublewell.py, to show the
monotonic (single-valued V_eq) -> non-monotonic (multi-valued, hysteresis
precursor) transition at Omega=2RT (Part 0 Step 3 self-check: slope at
theta=1/2 changes sign exactly at Omega=2RT).

Self-check: d(mu)/d(theta) at theta=1/2, evaluated by central finite
difference on the closed-form mu(theta), is compared to the closed-form
slope (2*Omega-4RT)/1 (from d/dtheta[RT ln(theta/(1-theta))] = RT/[theta(1-theta)]
=4RT at theta=1/2, plus d/dtheta[Omega(1-2theta)]=-2Omega -> total slope
4RT-2Omega, sign flips at Omega=2RT).
"""
import importlib.util
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

CODE = r"D:\Projects\Project_Anode_Fit\Claude\docs\v1.0.13\Anode_Fit_v1.0.13.py"
OUT = r"D:\Projects\Project_Anode_Fit\Claude\results\process\V1013_P21_fig_S2_mu_theta.png"

spec = importlib.util.spec_from_file_location("anodefit_v1013", CODE)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

R, F = m.R, m.F
T = 298.15
two_RT = 2.0 * R * T

omegas_real = [tr['Omega'] for tr in m.GRAPHITE_STAGING_LIT]
omega_set = [0.0, two_RT] + omegas_real
labels = ["Omega=0 (ideal Nernst)", f"Omega=2RT={two_RT:.0f} (marginal)"] + \
         [f"Omega={int(o)}" for o in omegas_real]

def mu_minus_mu0(theta, Omega):
    return R * T * np.log(theta / (1 - theta)) + Omega * (1 - 2 * theta)

theta = np.linspace(0.01, 0.99, 900)

fig, ax = plt.subplots(figsize=(7.2, 5.2))
for Omega, lab in zip(omega_set, labels):
    mu = mu_minus_mu0(theta, Omega)
    ax.plot(theta, mu, label=lab, lw=1.6)

    # closed-form slope at theta=1/2 vs central finite-difference on the closed form
    slope_closed = 4.0 * R * T - 2.0 * Omega
    h = 1e-6
    slope_fd = (mu_minus_mu0(0.5 + h, Omega) - mu_minus_mu0(0.5 - h, Omega)) / (2 * h)
    assert abs(slope_closed - slope_fd) < 1e-3, f"slope mismatch at Omega={Omega}"
    # dmu/dtheta|_{1/2} = 4RT-2*Omega = g''(1/2): >0 -> stable/monotonic increasing,
    # <0 -> unstable at center -> mu(theta) backward-bends -> non-monotonic (S-loop),
    # =0 -> marginal (Omega=2RT threshold, Part 0 eq:spinodal onset).
    tag = "non-monotonic (S-loop; unstable center, spinodal pair)" if slope_closed < -1e-6 else \
          ("marginal (slope=0 at center, Omega=2RT onset)" if abs(slope_closed) < 1e-6 else
           "monotonic increasing (stable, normal isotherm)")
    print(f"Omega={Omega:8.1f}: closed-form slope@theta=1/2={slope_closed:9.2f}  "
          f"finite-diff={slope_fd:9.2f}  match={abs(slope_closed - slope_fd) < 1e-3}  -> {tag}")

ax.axhline(0, color="gray", lw=0.6)
ax.axvline(0.5, color="gray", ls=":", lw=1)
ax.set_xlabel(r"$\theta$  (Li occupation)")
ax.set_ylabel(r"$\mu_\mathrm{Li}(\theta)-\mu^0$  [J/mol]")
ax.set_title("Part 0 fig 3 (S2): mean-field mu(theta) vs Omega (eq:mu)\n"
             "slope at theta=1/2 flips sign at Omega=2RT (verified: closed-form = finite-diff)")
ax.legend(fontsize=7.5, loc="upper left")
fig.tight_layout()
fig.savefig(OUT, dpi=160)
print(f"saved: {OUT}")
