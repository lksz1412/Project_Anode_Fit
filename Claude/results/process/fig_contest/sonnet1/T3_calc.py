# T3 fig:hysloop — non-monotone equilibrium potential V_eq(xi) and spinodal overshoot.
# Source equations (graphite_ica_ch1_v1.0.14.tex):
#   eq:Veq   : V_eq,j(xi) = U_j + (RT/sF) ln[xi/(1-xi)] + (Omega_j/sF)(1-2xi)
#              plotted dimensionless as y = (sF/RT)(V_eq-U_j) = ln[xi/(1-xi)] + (Omega_j/RT)(1-2xi)
#   eq:spinodal : xi_s^pm = 1/2 (1 +- u),  u = sqrt(1 - 2RT/Omega_j)
#   eq:dUhys : Delta U_hys = (2/F)[Omega*u - 2RT*artanh(u)]   (gap, volts)
# Case used (matches body text figure): Omega_j = 4RT  ->  y(xi) = ln[xi/(1-xi)] + 4(1-2xi)
import math

R = 8.314462618
F = 96485.33212
T = 298.15
RT = R * T
Omega = 4.0 * RT               # Omega_j = 4RT (dimensionless-in-RT case used by the document)

u = math.sqrt(1.0 - 2.0 * RT / Omega)   # = sqrt(1-0.5) = sqrt(0.5)
xi_s_minus = 0.5 * (1 - u)
xi_s_plus = 0.5 * (1 + u)

def y_of_xi(xi):
    # y = (sF/RT)(V_eq - U_j), s=+1 (derivation convention)
    return math.log(xi / (1 - xi)) + (Omega / RT) * (1 - 2 * xi)

# curated grid: dense near the ends (steep logit branches) + exact spinodal points,
# coarser through the middle — avoids xi=0,1 singularities.
xis = sorted(set([0.02, 0.04, 0.06, 0.08, 0.10, 0.12, xi_s_minus, 0.16, 0.20, 0.25,
                   0.30, 0.35, 0.40, 0.45, 0.50, 0.55, 0.60, 0.65, 0.70, 0.75, 0.80,
                   0.84, xi_s_plus, 0.88, 0.90, 0.92, 0.94, 0.96, 0.98]))
pts = [(round(xi, 4), round(y_of_xi(xi), 4)) for xi in xis]

# spinodal points (exact)
y_s_minus = y_of_xi(xi_s_minus)
y_s_plus = y_of_xi(xi_s_plus)

# discharge overshoot branch: xi in (0, xi_s_minus], rising to the maximum
xis_dis = [x for x in xis if x <= xi_s_minus + 1e-9]
xis_dis.append(xi_s_minus)
xis_dis = sorted(set(round(x, 4) for x in xis_dis))
pts_dis = [(x, round(y_of_xi(x), 4)) for x in xis_dis]

# charge overshoot branch: xi in [xi_s_plus, 1)
xis_chg = [x for x in xis if x >= xi_s_plus - 1e-9]
xis_chg.append(xi_s_plus)
xis_chg = sorted(set(round(x, 4) for x in xis_chg))
pts_chg = [(x, round(y_of_xi(x), 4)) for x in xis_chg]

# gap magnitude in volts (closed form, eq:dUhys), independent cross-check
artanh_u = 0.5 * math.log((1 + u) / (1 - u))
dU_hys_V = (2.0 / F) * (Omega * u - 2.0 * RT * artanh_u)
# cross-check via dimensionless peak-to-peak * RT/F
dU_hys_V_check = (y_s_minus - y_s_plus) * RT / F

if __name__ == "__main__":
    print("u =", u)
    print("xi_s^- =", round(xi_s_minus, 4), " xi_s^+ =", round(xi_s_plus, 4))
    print("y(xi_s^-) =", round(y_s_minus, 4), " y(xi_s^+) =", round(y_s_plus, 4))
    print("Delta U_hys [V] (closed form) =", round(dU_hys_V, 5))
    print("Delta U_hys [V] (from y-range) =", round(dU_hys_V_check, 5))
    print()
    print("full curve points:")
    print(pts)
    print()
    print("discharge overshoot branch points:")
    print(pts_dis)
    print()
    print("charge overshoot branch points:")
    print(pts_chg)
