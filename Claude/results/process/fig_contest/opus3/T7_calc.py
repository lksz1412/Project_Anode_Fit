# -*- coding: utf-8 -*-
# T7 fig:reversal (opus3) — causal-memory tail direction, discharge vs charge (mirror),
# with the tail computed by the ACTUAL first-order low-pass (eq:lowpass) and grid reversal
# (eq:reversal), not a schematic sketch.
#   equilibrium bell (direction invariant):  b(V) = xi_eq(1-xi_eq)/w  (eq:eqpeak)
#   lag (eq:lowpass): xi_lag_i = rho xi_lag_{i-1} + (1-rho) xi_eq_i,  rho = exp(-dgrid/L_V)
#   charge (eq:reversal): xi_lag = Reverse[ LowPass( Reverse[xi_eq] ) ]
#   peak shape (eq:peakshape): (xi_eq - xi_lag)/L_V   (stays positive)
# Units: w=1, L_V=1.2 w, grid step dgrid=0.05 w.  V in units of w about the center U_j^d.
import numpy as np

w = 1.0
L_V = 1.2
dgrid = 0.05
rho = np.exp(-dgrid / L_V)
V = np.arange(-4.5, 4.5 + 1e-9, dgrid)


def lowpass(sig):
    out = np.empty_like(sig)
    out[0] = sig[0]
    for i in range(1, len(sig)):
        out[i] = rho * out[i - 1] + (1.0 - rho) * sig[i]
    return out


# discharge: sigma_d=+1 -> xi_eq rising in V; filter along ascending grid (time = V up)
xi_dis = 1.0 / (1.0 + np.exp(-(V) / w))
lag_dis = lowpass(xi_dis)
peak_dis = (xi_dis - lag_dis) / L_V

# charge: sigma_d=-1 -> xi_eq rising in TIME as V decreases; reverse-filter-reverse
xi_chg = 1.0 / (1.0 + np.exp(+(V) / w))          # falling in V
lag_chg = lowpass(xi_chg[::-1])[::-1]
peak_chg = (xi_chg - lag_chg) / L_V

# equilibrium bell (same both directions)
bell = xi_dis * (1.0 - xi_dis) / w

print(f"rho = {rho:.5f}   L_V = {L_V}   dgrid = {dgrid}")
print(f"discharge peak: max={peak_dis.max():.4f} at V={V[peak_dis.argmax()]:.3f}  min={peak_dis.min():.4f} (positive-only={np.all(peak_dis>=-1e-9)})")
print(f"charge    peak: max={peak_chg.max():.4f} at V={V[peak_chg.argmax()]:.3f}  min={peak_chg.min():.4f} (positive-only={np.all(peak_chg>=-1e-9)})")
print(f"equilibrium bell peak={bell.max():.4f} at V={V[bell.argmax()]:.3f}")
print(f"areas (trapz): bell={np.trapezoid(bell,V):.4f}  peak_dis={np.trapezoid(peak_dis,V):.4f}  peak_chg={np.trapezoid(peak_chg,V):.4f}")


def sample(x, y, xs):
    yi = np.interp(xs, x, y)
    return " ".join(f"({a:.2f},{b:.4f})" for a, b in zip(xs, yi))


coarse = np.arange(-4.0, 4.01, 0.5)
tail = np.arange(-4.0, 4.01, 0.25)
print("\n% equilibrium bell (dotted):")
print(sample(V, bell, coarse))
print("\n% discharge peak-with-tail (solid):")
print(sample(V, peak_dis, tail))
print("\n% charge peak-with-tail (solid):")
print(sample(V, peak_chg, tail))
