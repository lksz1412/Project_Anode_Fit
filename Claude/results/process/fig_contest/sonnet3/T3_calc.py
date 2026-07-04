"""T3 fig:hysloop -- coordinate generator.

Non-monotone equilibrium potential V_eq(xi) from eq:Veq (l.1077):
    y(xi) = ln[xi/(1-xi)] + (Omega/RT)*(1-2*xi)      [y = (sF/RT)(V_eq-U_j), s=+1]

Spinodal extrema from eq:spinodal (l.1036-1038):
    u = sqrt(1 - 2RT/Omega),   xi_s^-,+ = (1 -/+ u)/2

Gap (eq:dUhys, l.1104): Delta*F = 2*[Omega*u - 2RT*artanh(u)]  (in J/mol; the
y-plot below is already in RT-normalized units so the plotted gap is
directly y(xi_s^-) - y(xi_s^+) = -2*ln[(1-u)/(1+u)]... this script checks
that identity numerically instead of trusting algebra by hand.)

Main curve: Omega = 4RT (matches the existing figure, kept for continuity).
Two extra family members are the SMALLEST and LARGEST initial Omega/RT
ratios actually tabulated for graphite staging in table tab:staging
(l.1984-1987, Omega in J/mol, RT=298.15 K): this ties the "curve family"
device to real transitions in this chapter rather than arbitrary round
numbers.
"""

import math

R = 8.314462618
T = 298.15
RT = R * T
print(f"RT(298.15K) = {RT:.2f} J/mol, 2RT = {2*RT:.2f} J/mol")

staging_omega = {"4->3": 6000.0, "3->2L": 8000.0, "2L->2": 10000.0, "2->1": 13000.0}
ratios = {k: v / RT for k, v in staging_omega.items()}
for k, v in ratios.items():
    print(f"{k:8s} Omega={staging_omega[k]:>6.0f} J/mol -> Omega/RT = {v:.3f}")
omega_min_name = min(ratios, key=ratios.get)
omega_max_name = max(ratios, key=ratios.get)
print(f"family members chosen: {omega_min_name} (min, Omega/RT={ratios[omega_min_name]:.3f}), "
      f"{omega_max_name} (max, Omega/RT={ratios[omega_max_name]:.3f}), main=4RT (figure continuity)")


def veq_curve(omega_over_RT, n=41, eps=0.02, insert_xi=()):
    """y(xi) = ln[xi/(1-xi)] + omega_over_RT*(1-2*xi), xi in [eps,1-eps].

    insert_xi: exact xi values (e.g. the spinodal extrema) spliced into the
    uniform grid so 'plot smooth' passes exactly through the true peak/
    trough instead of only near it.
    """
    xs = [eps + (1 - 2 * eps) * i / (n - 1) for i in range(n)]
    for xi0 in insert_xi:
        xs.append(xi0)
    xs = sorted(set(round(x, 6) for x in xs))
    pts = []
    for xi in xs:
        y = math.log(xi / (1 - xi)) + omega_over_RT * (1 - 2 * xi)
        pts.append((xi, y))
    return pts


def spinodal(omega_over_RT):
    u = math.sqrt(1 - 2.0 / omega_over_RT)
    xi_minus = 0.5 * (1 - u)  # potential maximum (discharge overshoot target)
    xi_plus = 0.5 * (1 + u)   # potential minimum (charge overshoot target)
    y_minus = math.log(xi_minus / (1 - xi_minus)) + omega_over_RT * (1 - 2 * xi_minus)
    y_plus = math.log(xi_plus / (1 - xi_plus)) + omega_over_RT * (1 - 2 * xi_plus)
    return u, xi_minus, xi_plus, y_minus, y_plus


def gap_closed_form(omega_over_RT):
    """Delta U * F/RT  (eq:dUhys with s=1, in RT units): 2*[Omega/RT*u - 2*artanh(u)]."""
    u = math.sqrt(1 - 2.0 / omega_over_RT)
    return 2 * (omega_over_RT * u - 2 * math.atanh(u))


for name, w in [("Omega=4RT (main)", 4.0),
                (f"{omega_min_name} (Omega/RT={ratios[omega_min_name]:.3f})", ratios[omega_min_name]),
                (f"{omega_max_name} (Omega/RT={ratios[omega_max_name]:.3f})", ratios[omega_max_name])]:
    u, xm, xp, ym, yp = spinodal(w)
    gap_direct = ym - yp
    gap_formula = gap_closed_form(w)
    print(f"\n-- {name} --")
    print(f"u={u:.4f}  xi_s^-={xm:.4f} (y={ym:.4f})   xi_s^+={xp:.4f} (y={yp:.4f})")
    print(f"gap (y_minus - y_plus)      = {gap_direct:.4f}")
    print(f"gap (closed form eq:dUhys)  = {gap_formula:.4f}  [should match]")
    assert abs(gap_direct - gap_formula) < 1e-9, "closed form does not match direct spinodal evaluation"

print("\n[ok] closed-form gap (eq:dUhys) matches direct spinodal-endpoint evaluation for all three Omega values.")

print("\n== main curve Omega=4RT, plot coordinates (xi, y) ==")
u4_, xm4_, xp4_, _, _ = spinodal(4.0)
main = veq_curve(4.0, n=41, eps=0.02, insert_xi=(xm4_, xp4_))
print(" ".join(f"({xi:.4f},{y:.4f})" for xi, y in main))

u4, xm4, xp4, ym4, yp4 = spinodal(4.0)
print(f"\nspinodal main: xi_s^-={xm4:.4f} y={ym4:.4f} | xi_s^+={xp4:.4f} y={yp4:.4f} | gap={ym4-yp4:.4f}")

# discharge overshoot sub-path: eps..xi_s^-
disc = [p for p in veq_curve(4.0, n=161, eps=0.02) if p[0] <= xm4 + 1e-9]
disc = disc[-9:]  # last few points approaching the maximum, for a short bold arrow path
print("\ndischarge overshoot tail points (approaching xi_s^-):")
print(" ".join(f"({xi:.4f},{y:.4f})" for xi, y in disc))

charge = [p for p in veq_curve(4.0, n=161, eps=0.02) if p[0] >= xp4 - 1e-9]
charge = charge[:9]
print("\ncharge overshoot tail points (approaching xi_s^+):")
print(" ".join(f"({xi:.4f},{y:.4f})" for xi, y in charge))

for name, w in [(omega_min_name, ratios[omega_min_name]), (omega_max_name, ratios[omega_max_name])]:
    print(f"\n== family curve {name} (Omega/RT={w:.3f}) coordinates ==")
    _, xm_, xp_, _, _ = spinodal(w)
    pts = veq_curve(w, n=41, eps=0.02, insert_xi=(xm_, xp_))
    print(" ".join(f"({xi:.4f},{y:.4f})" for xi, y in pts))
