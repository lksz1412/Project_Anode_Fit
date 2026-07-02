# -*- coding: utf-8 -*-
"""V1013 P2.1 Part 0 figure (S2) -- regular-solution free energy g(xi) vs Omega.

Purpose: visualize eq:gxi -- g_j(xi) = RT[xi ln xi + (1-xi) ln(1-xi)] + Omega*xi*(1-xi)
(g_j^0 dropped -- constant vertical shift only, does not affect shape/curvature)
for a spread of Omega values spanning the graphite GRAPHITE_STAGING_LIT table
(0 / 6000 / 8000 / 10000 / 13000 J/mol) plus the exact threshold 2RT, to show
the single-well -> double-well transition (eq:gpp / eq:spinodal, Part 0 Step 3).

Self-check (non-fabrication guard): the numerically located inflection points
(g''(xi)=0, found by root-finding on the closed-form second derivative) are
compared against the closed-form spinodal xi_s^+- = 1/2*(1 +- u), u = sqrt(1-2RT/Omega).
Both routes must agree to floating-point precision.
"""
import importlib.util
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

CODE = r"D:\Projects\Project_Anode_Fit\Claude\docs\v1.0.13\Anode_Fit_v1.0.13.py"
OUT = r"D:\Projects\Project_Anode_Fit\Claude\results\process\V1013_P21_fig_S2_gxi_doublewell.png"

spec = importlib.util.spec_from_file_location("anodefit_v1013", CODE)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

R, F = m.R, m.F
T = 298.15
two_RT = 2.0 * R * T  # ~4958 J/mol, exact spinodal threshold (eq:spinodal)

# real Omega values lifted from GRAPHITE_STAGING_LIT (not invented) + the exact threshold
omegas_real = [tr['Omega'] for tr in m.GRAPHITE_STAGING_LIT]  # [6000, 8000, 10000, 13000]
omega_set = [0.0] + [two_RT] + omegas_real
labels = ["Omega=0 (ideal)", f"Omega=2RT={two_RT:.0f} (threshold)"] + \
         [f"Omega={int(o)} (stage {i+1} tbl)" for i, o in enumerate(omegas_real)]

def g_xi(xi, Omega):
    return R * T * (xi * np.log(xi) + (1 - xi) * np.log(1 - xi)) + Omega * xi * (1 - xi)

def gpp_xi(xi, Omega):
    return R * T / (xi * (1 - xi)) - 2.0 * Omega

xi = np.linspace(0.005, 0.995, 2000)

fig, ax = plt.subplots(figsize=(7.4, 5.2))
for Omega, lab in zip(omega_set, labels):
    g = g_xi(xi, Omega)
    ax.plot(xi, g / (R * T), label=lab, lw=1.6)

    if Omega > two_RT:
        # closed-form spinodal (eq:spinodal)
        u = np.sqrt(1.0 - two_RT / Omega)
        xi_s_minus, xi_s_plus = 0.5 * (1 - u), 0.5 * (1 + u)
        # numeric cross-check: bracket-and-bisect root of gpp_xi on (0,0.5) and (0.5,1)
        from scipy.optimize import brentq
        xi_s_minus_num = brentq(lambda x: gpp_xi(x, Omega), 1e-6, 0.5 - 1e-9)
        xi_s_plus_num = brentq(lambda x: gpp_xi(x, Omega), 0.5 + 1e-9, 1 - 1e-6)
        assert abs(xi_s_minus_num - xi_s_minus) < 1e-6, "spinodal- mismatch closed-form vs numeric"
        assert abs(xi_s_plus_num - xi_s_plus) < 1e-6, "spinodal+ mismatch closed-form vs numeric"
        print(f"Omega={Omega:.0f}: closed-form xi_s-/+ = {xi_s_minus:.4f}/{xi_s_plus:.4f}  "
              f"numeric = {xi_s_minus_num:.4f}/{xi_s_plus_num:.4f}  (match)")
        ax.plot([xi_s_minus, xi_s_plus], [g_xi(xi_s_minus, Omega) / (R * T),
                                            g_xi(xi_s_plus, Omega) / (R * T)],
                'k.', ms=5)
    else:
        print(f"Omega={Omega:.0f}: <= 2RT, single well (no real spinodal root)")

ax.set_xlabel(r"$\xi$  (delithiation progress)")
ax.set_ylabel(r"$g_j(\xi)/RT$  (g_j^0 dropped, vertical shift only)")
ax.set_title("Part 0 fig 2 (S2): regular-solution g(xi) vs Omega (eq:gxi)\n"
             "dots = spinodal points (eq:spinodal, closed-form = numeric root, verified)")
ax.legend(fontsize=7.5, loc="upper center", ncol=2)
fig.tight_layout()
fig.savefig(OUT, dpi=160)
print(f"saved: {OUT}")
