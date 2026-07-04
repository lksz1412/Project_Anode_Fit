"""T6 fig:logistic — xi_eq(V) and its derivative bell at three temperatures.

Exact evaluation of eq:xieq (sigma_d=+1, U_j^d=0, n_j=1 so w_j=RT/F) and the
bell identity eq:belliden (dxi_eq/dV = xi_eq(1-xi_eq)/w_j), for T in
{268, 298, 328} K -- the width w_j = n_j R T / F genuinely changes with T
(eq:wbase), which the previous version's normalized z=(V-U)/w axis hid
(any single T collapses to the same curve in z-space). Plotting against
real (V-U_j) in mV makes the T-dependence visible, and the central slope
1/(4 w_j) is exactly the bell's peak height (checked below).
"""
import numpy as np

R = 8.314
F = 96485.0
TEMPS = [268.0, 298.0, 328.0]


def width_V(T, n=1.0):
    return n * R * T / F  # eq:wbase, volts


def xi_eq(v, w):
    z = v / w
    # overflow-safe two-branch form, same idea as eq:xieq numerics note
    out = np.where(z >= 0, 1.0 / (1.0 + np.exp(-z)),
                   np.exp(z) / (1.0 + np.exp(z)))
    return out


def bell(v, w):
    xe = xi_eq(v, w)
    return xe * (1 - xe) / w  # dxi_eq/dV, eq:belliden


if __name__ == "__main__":
    v_mv = np.linspace(-100, 100, 41)  # mV grid, dense enough for plot[smooth]
    v = v_mv / 1000.0

    for T in TEMPS:
        w = width_V(T)
        print(f"T={T:.0f} K:  w = {w*1000:.3f} mV   central slope 1/(4w) = {1.0/(4*w):.3f} /V"
              f"  ({1.0/(4*w)/1000:.5f} /mV)")

    print("\nsample xi_eq(V) and bell(V) at T=298 K (mV grid, 20 mV step):")
    w298 = width_V(298.0)
    for vmv in range(-100, 101, 20):
        vv = vmv / 1000.0
        print(f"  V-U={vmv:4d} mV:  xi_eq={float(xi_eq(vv, w298)):.4f}  "
              f"bell={float(bell(vv, w298)):.4f} /V")

    # peak-height check: bell(0) must equal 1/(4w) exactly for all T
    for T in TEMPS:
        w = width_V(T)
        assert abs(bell(0.0, w) - 1.0 / (4 * w)) < 1e-12
    print("\nOK: bell(0) == 1/(4w) exactly for all three temperatures.")

    # emit full coordinate lists (rounded) for the tikz plot, one line per T.
    # x = raw mV (tikz picture uses x=0.045cm per unit => ~9cm total width).
    # bell values are in 1/V (order 9-11); a single common scale factor
    # BELL_SCALE=0.08 maps them into the same [0,1]-ish visual range as
    # xi_eq WITHOUT per-curve renormalization, so relative peak heights
    # (colder = taller/narrower) stay physically comparable across T.
    BELL_SCALE = 0.08
    print(f"\nBELL_SCALE = {BELL_SCALE} (applied identically to all three T)")
    for T in TEMPS:
        w = width_V(T)
        xs = np.arange(-100, 101, 10)
        xis = xi_eq(xs / 1000.0, w)
        bells = bell(xs / 1000.0, w) * BELL_SCALE
        coords_xi = " ".join(f"({x:.0f},{float(y):.4f})" for x, y in zip(xs, xis))
        coords_bell = " ".join(f"({x:.0f},{float(y):.4f})" for x, y in zip(xs, bells))
        peak = 1.0 / (4 * w) * BELL_SCALE
        print(f"\nT={T:.0f}K  (w={w*1000:.3f} mV, scaled bell peak={peak:.4f}):")
        print(f"  xi_eq coords:\n  {coords_xi}")
        print(f"  bell coords:\n  {coords_bell}")
