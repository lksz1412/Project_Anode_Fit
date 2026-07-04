#!/usr/bin/env python3
# T3 fig:hysloop  --  non-monotone equilibrium potential V_eq(xi), Omega = 4RT.
# Plotted quantity (dimensionless, s=+1):
#   y(xi) = (sF/RT)(V_eq - U_j) = ln[xi/(1-xi)] + (Omega/RT)(1-2 xi),  Omega/RT = 4.
# Spinodal (eq:spinodal):  xi_s^± = 1/2 (1 ± u),  u = sqrt(1 - 2RT/Omega) = sqrt(1/2).
# Gap in RT/F units = y(xi_s^-) - y(xi_s^+) = 2 y(xi_s^-)  (eq:dUhys).
import math

OmR = 4.0  # Omega / RT
u = math.sqrt(1.0 - 2.0/OmR)          # 0.7071067811865476
xsm = 0.5*(1.0 - u)                    # xi_s^-  (rising-branch extremum, discharge)
xsp = 0.5*(1.0 + u)                    # xi_s^+  (falling-branch extremum, charge)

def y(xi):
    return math.log(xi/(1.0-xi)) + OmR*(1.0 - 2.0*xi)

ys = y(xsm)                            # y at xi_s^-   (positive maximum)
gap = 2.0*ys                           # Delta U^hys in RT/F units

print(f"# u = {u:.6f}")
print(f"# xi_s^- = {xsm:.6f}   xi_s^+ = {xsp:.6f}")
print(f"# y(xi_s^-) = {ys:.6f}   y(xi_s^+) = {y(xsp):.6f}")
print(f"# gap (RT/F units) = {gap:.6f}")
print(f"# gap (mV @298K, RT/F=25.693mV) = {gap*25.693:.3f}")

# --- full curve, dense sampling; avoid the singular endpoints ---
grid = [0.015,0.03,0.05,0.07,0.09,0.11,xsm,0.18,0.22,0.27,0.33,0.40,0.50,
        0.60,0.67,0.73,0.78,0.82,xsp,0.91,0.93,0.95,0.97,0.985]
def fmt(pts):
    return " ".join(f"({x:.4f},{v:.4f})" for x,v in pts)
print("\n% full V_eq(xi) curve:")
print(fmt([(x,y(x)) for x in grid]))

# --- discharge overshoot path: rising branch 0 -> xi_s^- ---
dpath = [x for x in [0.015,0.03,0.05,0.07,0.09,0.11,xsm] ]
print("\n% discharge overshoot (rising to xi_s^-):")
print(fmt([(x,y(x)) for x in dpath]))

# --- charge overshoot path: falling branch 1 -> xi_s^+ ---
cpath = [0.985,0.97,0.95,0.93,0.91,xsp]
print("\n% charge overshoot (falling to xi_s^+):")
print(fmt([(x,y(x)) for x in cpath]))

print(f"\n% spinodal markers:  ({xsm:.4f},{ys:.4f})  ({xsp:.4f},{-ys:.4f})")
