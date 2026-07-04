"""T7 fig:reversal — real low-pass (eq:lowpass) tail, discharge vs charge.

Unlike the current document figure (hand-drawn representative curves), this
implements the actual discrete recursion:

    xi_lag[i] = rho*xi_lag[i-1] + (1-rho)*xi_eq[i]        (eq:lowpass)
    rho = exp(-Delta_grid / L_V)

with xi_lag[0] = xi_eq[0] (padding choice, sec:tail), and applies the
charge grid-reversal exactly as eq:reversal specifies:

    discharge (sigma_d=+1): xi_lag = LowPass(xi_eq)                 [grid ascending = time order]
    charge    (sigma_d=-1): xi_lag = Reverse[LowPass(Reverse[xi_eq])] [time order is descending V]

peak shape = (xi_eq - xi_lag)/L_V  (eq:peakshape), plotted against z =
sigma_d*(V-U_j^d)/w_j (so "progress" always increases left->right in the
z used for each panel, matching each panel's own time direction).
"""
import numpy as np

DZ = 0.05          # grid spacing in w-units (fine, for an accurate recursion)
L_V = 1.2          # lag length in w-units (>= few * DZ, per sec:tail L_V >> Delta_grid)
Z_RANGE = 8.0


def logistic(z):
    return np.where(z >= 0, 1.0 / (1.0 + np.exp(-z)), np.exp(z) / (1.0 + np.exp(z)))


def lowpass(xi_eq, dz=DZ, lv=L_V):
    rho = np.exp(-dz / lv)
    xi_lag = np.empty_like(xi_eq)
    xi_lag[0] = xi_eq[0]
    for i in range(1, len(xi_eq)):
        xi_lag[i] = rho * xi_lag[i - 1] + (1 - rho) * xi_eq[i]
    return xi_lag, rho


if __name__ == "__main__":
    z = np.arange(-Z_RANGE, Z_RANGE + 1e-9, DZ)

    # discharge: sigma_d=+1, ascending grid = time order (no reversal)
    xi_eq_dis = logistic(z)
    xi_lag_dis, rho = lowpass(xi_eq_dis)
    peak_dis = (xi_eq_dis - xi_lag_dis) / L_V

    # charge: sigma_d=-1, descending V is time order -> reverse, filter, reverse back
    xi_eq_chg = logistic(-z)
    xi_lag_chg_rev, _ = lowpass(xi_eq_chg[::-1])
    xi_lag_chg = xi_lag_chg_rev[::-1]
    peak_chg = (xi_eq_chg - xi_lag_chg) / L_V

    # equilibrium bell (direction-invariant reference), same z axis
    bell = xi_eq_dis * (1 - xi_eq_dis)

    print(f"rho = exp(-{DZ}/{L_V}) = {rho:.5f}  (close to 1: L_V >> Delta_grid, OK)")
    print(f"max peak_dis = {peak_dis.max():.4f} at z = {z[np.argmax(peak_dis)]:.2f}")
    print(f"max peak_chg = {peak_chg.max():.4f} at z = {z[np.argmax(peak_chg)]:.2f}")
    print(f"max bell     = {bell.max():.4f} at z = {z[np.argmax(bell)]:.2f}")

    # skew check: discharge tail should lean to HIGHER z (higher V), charge to LOWER z
    def centroid_offset(curve):
        return float(np.sum(z * curve) / np.sum(curve))
    print(f"\ncentroid(peak_dis) = {centroid_offset(peak_dis):+.4f}  (expect > 0, tail -> higher V)")
    print(f"centroid(peak_chg) = {centroid_offset(peak_chg):+.4f}  (expect < 0, tail -> lower V)")
    print(f"centroid(bell)     = {centroid_offset(bell):+.4f}  (expect ~0, symmetric)")

    # downsample to a plottable grid (every 8th point => step 0.4, range -6..6)
    mask = (z >= -6.0) & (z <= 6.0)
    idx = np.where(mask)[0][::8]
    print("\nz sample:", [round(float(z[i]), 2) for i in idx])
    print("peak_dis:", [round(float(peak_dis[i]), 4) for i in idx])
    print("peak_chg:", [round(float(peak_chg[i]), 4) for i in idx])
    print("bell    :", [round(float(bell[i]), 4) for i in idx])
