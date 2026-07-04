"""T8 fig:widthbudget — real numeric convolution of the three broadening stages.

eq:widthbudget states the two symmetric contributions (intrinsic logistic-
derivative species and ensemble eta-spread) add in QUADRATURE (variance),
and the asymmetric finite-rate tail adds a one-sided exponential smear on
top. Rather than hand-drawing plausible-looking bells (as the current
document figure does -- three curves typed by estimation), this script
actually performs the two convolutions numerically on a fine grid and
samples the result, so the tikz curve is a genuine numerical integral,
matching the caption's existing claim "수치 적분" literally.

Stage 0: base bell f0(x) = xi(1-xi), xi=logistic(x)      [w_j=1 units]
         (this is exactly the standard logistic-distribution density,
         variance pi^2/3 -- eq:widthbudget's sigma_int in scale-1 units)
Stage 1: convolve f0 with a Gaussian of sigma_eta = 1.25*sigma_int
         -> f1 = f0 (*) gaussian   (symmetric variance-additive broadening)
Stage 2: convolve f1 with a one-sided exponential (rate 1/L_V, L_V=1.5w)
         -> f2 = f1 (*) exp_onesided   (asymmetric causal-memory tail)
"""
import numpy as np

DX = 0.01
X = np.arange(-30, 30 + DX, DX)

SIGMA_INT = np.pi / np.sqrt(3)       # w_j=1 units, eq:widthbudget
SIGMA_ETA = 1.25 * SIGMA_INT
L_V = 1.5


def base_bell(x):
    xe = 1.0 / (1.0 + np.exp(-x))
    return xe * (1 - xe)


def gaussian(x, sigma):
    return np.exp(-0.5 * (x / sigma) ** 2) / (sigma * np.sqrt(2 * np.pi))


def onesided_exp(x, lv):
    return np.where(x >= 0, np.exp(-x / lv) / lv, 0.0)


def convolve_norm(f, g, dx):
    c = np.convolve(f, g, mode="same") * dx
    return c


if __name__ == "__main__":
    f0 = base_bell(X)
    print(f"stage0 area = {np.sum(f0)*DX:.5f} (expect 1)")
    print(f"stage0 peak = {f0.max():.5f} at x=0 (expect 0.25 exactly)")

    g = gaussian(X, SIGMA_ETA)
    f1 = convolve_norm(f0, g, DX)
    print(f"\nsigma_int = {SIGMA_INT:.5f}, sigma_eta = {SIGMA_ETA:.5f}")
    sigma_sym = np.sqrt(SIGMA_INT**2 + SIGMA_ETA**2)
    print(f"sigma_sym (predicted, eq:widthbudget) = {sigma_sym:.5f} "
          f"({sigma_sym/SIGMA_INT:.4f} x sigma_int)")
    print(f"stage1 area = {np.sum(f1)*DX:.5f} (expect 1)")
    print(f"stage1 peak = {f1.max():.5f} at x={X[np.argmax(f1)]:.3f}")

    h = onesided_exp(X, L_V)
    f2 = convolve_norm(f1, h, DX)
    print(f"\nstage2 area = {np.sum(f2)*DX:.5f} (expect 1)")
    print(f"stage2 peak = {f2.max():.5f} at x={X[np.argmax(f2)]:.3f}")

    def centroid(f):
        return float(np.sum(X * f) * DX / (np.sum(f) * DX))
    print(f"\ncentroid f0={centroid(f0):+.4f}  f1={centroid(f1):+.4f}  f2={centroid(f2):+.4f}"
          "  (f2 should shift positive: one-sided exp tail on x>0)")

    # sample points matching the figure's plotted domain (w_j units)
    xs_plot = [-6, -5, -4, -3, -2, -1, -0.5, 0, 0.5, 1, 1.5, 2, 2.5, 3, 4, 5, 6, 7, 8, 9, 10]
    f0_s = np.interp(xs_plot, X, f0)
    f1_s = np.interp(xs_plot, X, f1)
    f2_s = np.interp(xs_plot, X, f2)
    print("\nsample coordinates (x, f0, f1, f2):")
    for x, a, b, c in zip(xs_plot, f0_s, f1_s, f2_s):
        print(f"  x={x:>5}: f0={a:.4f}  f1={b:.4f}  f2={c:.4f}")
