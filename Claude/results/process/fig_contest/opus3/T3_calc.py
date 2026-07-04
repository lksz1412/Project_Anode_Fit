# -*- coding: utf-8 -*-
# T3 fig:hysloop (opus3) — non-monotone equilibrium potential V_eq(xi), Omega=4RT.
# Eq. eq:Veq :  y(xi) = (sF/RT)(V_eq - U_j) = ln[xi/(1-xi)] + (Omega/RT)(1-2xi),  s=+1.
# Here Omega/RT = 4.  Coordinates are the direct numerical evaluation of this equation.
import numpy as np

OMEGA = 4.0  # Omega/RT


def y(xi):
    return np.log(xi / (1.0 - xi)) + OMEGA * (1.0 - 2.0 * xi)


# spinodal: u = sqrt(1 - 2RT/Omega); xi_s^± = 1/2 (1 ± u)
u = np.sqrt(1.0 - 2.0 / OMEGA)
xi_sm = 0.5 * (1.0 - u)   # xi_s^-  (discharge overshoot end, y max)
xi_sp = 0.5 * (1.0 + u)   # xi_s^+  (charge overshoot end, y min)
y_sm = y(xi_sm)
y_sp = y(xi_sp)

print(f"u = {u:.6f}")
print(f"xi_s^- = {xi_sm:.6f}   y(xi_s^-) = {y_sm:.6f}")
print(f"xi_s^+ = {xi_sp:.6f}   y(xi_s^+) = {y_sp:.6f}")
print(f"spinodal gap  DeltaU(units RT/sF) = y_sm - y_sp = {y_sm - y_sp:.6f}")
print(f"Maxwell/common potential level  y=0  at xi=0.5 -> y(0.5)={y(0.5):.6f}")


def block(xs):
    return " ".join(f"({x:.4f},{y(x):.4f})" for x in xs)


# full curve (avoid singular endpoints)
full = [0.02, 0.04, 0.06, 0.08, 0.10, xi_sm, 0.20, 0.30, 0.40, 0.50,
        0.60, 0.70, 0.80, xi_sp, 0.90, 0.92, 0.94, 0.96, 0.98]
print("\n% FULL CURVE")
print(block(full))

# discharge rising branch: xi in [0.02 .. xi_s^-]
dis = [0.02, 0.04, 0.06, 0.08, 0.10, 0.12, xi_sm]
print("\n% DISCHARGE OVERSHOOT (rising to xi_s^-)")
print(block(dis))

# charge overshoot: xi in [0.98 .. xi_s^+] (descending path drawn high->low xi)
chg = [0.98, 0.96, 0.94, 0.92, 0.90, 0.88, xi_sp]
print("\n% CHARGE OVERSHOOT (descending to xi_s^+)")
print(block(chg))

print(f"\n% spinodal levels: y=+{y_sm:.4f} (xi_s^-),  y={y_sp:.4f} (xi_s^+)")
print(f"% points: (xi_s^-,y_sm)=({xi_sm:.4f},{y_sm:.4f})  (xi_s^+,y_sp)=({xi_sp:.4f},{y_sp:.4f})")
