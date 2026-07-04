"""T3 fig:hysloop — non-monotone V_eq(xi), Omega_j=4RT, s=1 (exact eval).

Implements eq:Veq exactly:
    y(xi) = (sF/RT)(V_eq - U_j) = ln[xi/(1-xi)] + (Omega_j/RT)(1 - 2*xi)
with Omega_j = 4RT (so Omega_j/RT = 4, s = +1, the convention fixed in the
document for the boxed hysteresis-gap derivation, sec:hys).

Also reproduces the spinodal roots (eq:spinodal) for Omega_j = 4RT and
checks that the curve's local extrema coincide with them (dV_eq/dxi = 0 at
xi_s^pm, since dy/dxi = RT^-1 g''(xi) there per eq:gpp) — i.e. this is not
just plausible-looking data, the printed xi_s^pm are the actual roots of
dy/dxi=0 for this y(xi), confirmed analytically and numerically below.
"""
import numpy as np

RT_over_Omega = 1.0 / 4.0  # Omega_j = 4 RT
u = np.sqrt(1 - 2 * RT_over_Omega)  # eq:spinodal, u_j = sqrt(1-2RT/Omega)
xi_s_minus = 0.5 * (1 - u)
xi_s_plus = 0.5 * (1 + u)


def y(xi):
    return np.log(xi / (1 - xi)) + 4.0 * (1 - 2 * xi)


def dydxi(xi):
    # analytic derivative: RT * d/dxi[ln(xi/(1-xi))] = 1/[xi(1-xi)], and
    # d/dxi[4(1-2xi)] = -8; matches eq:gpp/RT form 1/[xi(1-xi)] - 2*(Omega/RT)
    return 1.0 / (xi * (1 - xi)) - 8.0


if __name__ == "__main__":
    print(f"u_j = {u:.7f}")
    print(f"xi_s^- = {xi_s_minus:.7f}  (boxed fig used 0.1464)")
    print(f"xi_s^+ = {xi_s_plus:.7f}  (boxed fig used 0.8536)")
    print(f"dy/dxi at xi_s^- = {dydxi(xi_s_minus):.2e}  (should be ~0)")
    print(f"dy/dxi at xi_s^+ = {dydxi(xi_s_plus):.2e}  (should be ~0)")
    print(f"y(xi_s^-) = {y(xi_s_minus):.4f}   y(xi_s^+) = {y(xi_s_plus):.4f}")
    print(f"gap (extrema difference) = {y(xi_s_minus) - y(xi_s_plus):.4f}")
    # closed-form gap check via eq:dUhys boxed form (s=1, in units of RT/F):
    # DeltaU_hys * F/RT = 2*(Omega/RT)*u - 4*artanh(u)  [since eq:dUhys is
    # (2/F)[Omega*u - 2RT artanh u]; dividing by RT/F gives 2(Omega/RT)u -
    # 4 artanh u]
    gap_boxed = 2 * 4.0 * u - 4 * np.arctanh(u)
    print(f"gap (eq:dUhys boxed, RT/F units) = {gap_boxed:.4f}  (must match line above)")

    # dense sample for the main smooth curve, plus the two overshoot
    # sub-arcs (rounded 4dp exactly like the current document convention)
    xs_main = [0.02, 0.05, 0.08, 0.10, 0.1464, 0.20, 0.30, 0.40, 0.50,
               0.60, 0.70, 0.80, 0.8536, 0.90, 0.92, 0.95, 0.98]
    print("\nmain curve (xi, y):")
    for xi in xs_main:
        print(f"  ({xi:.4f},{y(xi):.4f})")

    xs_dis = [0.02, 0.05, 0.08, 0.10, 0.1464]
    xs_chg = [0.98, 0.95, 0.92, 0.90, 0.8536]
    print("\ndischarge overshoot arc:", [(round(x, 4), round(float(y(x)), 4)) for x in xs_dis])
    print("charge overshoot arc   :", [(round(x, 4), round(float(y(x)), 4)) for x in xs_chg])
