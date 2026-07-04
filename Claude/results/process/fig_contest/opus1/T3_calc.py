# T3 fig:hysloop — non-monotone equilibrium potential V_eq(xi), Omega=4RT.
# y = (sF/RT)(V_eq - U_j) = ln[xi/(1-xi)] + (Omega/RT)(1-2 xi), with Omega/RT = 4, s=+1.  [eq:Veq]
# spinodal:  u = sqrt(1 - 2RT/Omega) = sqrt(1-2/4);  xi_s^- = (1-u)/2,  xi_s^+ = (1+u)/2.  [eq:spinodal]
# gap (in these units): Delta = y(xi_s^-) - y(xi_s^+).  [eq:dUhys]
import math

OmegaRT = 4.0

def y(xi):
    return math.log(xi / (1.0 - xi)) + OmegaRT * (1.0 - 2.0 * xi)

u = math.sqrt(1.0 - 2.0 / OmegaRT)
xsm = (1.0 - u) / 2.0     # xi_s^-
xsp = (1.0 + u) / 2.0     # xi_s^+
ysm = y(xsm)
ysp = y(xsp)

print(f"u = {u:.4f}")
print(f"xi_s^- = {xsm:.4f}   y(xi_s^-) = {ysm:.4f}")
print(f"xi_s^+ = {xsp:.4f}   y(xi_s^+) = {ysp:.4f}")
print(f"gap Delta = {ysm - ysp:.4f}  (units sF/RT * (V-U))")
print()

# full curve, sampled to render the smooth non-monotone shape (avoid xi->0,1 blowups)
grid = [0.02, 0.05, 0.08, 0.10, xsm, 0.20, 0.30, 0.40, 0.50,
        0.60, 0.70, 0.80, xsp, 0.90, 0.92, 0.95, 0.98]
print("FULL CURVE (xi, y):")
print(" ".join(f"({xi:.4f},{y(xi):.4f})" for xi in sorted(set(grid))))
print()

# discharge overshoot: rising branch from xi~0 up to xi_s^-
disch = [0.02, 0.05, 0.08, 0.10, xsm]
print("DISCHARGE OVERSHOOT (xi, y):")
print(" ".join(f"({xi:.4f},{y(xi):.4f})" for xi in disch))
print()

# charge overshoot: descending branch from xi~1 down to xi_s^+
chg = [0.98, 0.95, 0.92, 0.90, xsp]
print("CHARGE OVERSHOOT (xi, y):")
print(" ".join(f"({xi:.4f},{y(xi):.4f})" for xi in chg))
