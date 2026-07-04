# -*- coding: utf-8 -*-
# T8 fig:widthbudget (opus3) — two-phase broadening width budget as a 4-row accumulation
# (eq:widthbudget). Each row adds one component; coordinates are direct numerical evaluation.
#   row0  equilibrium delta at plateau (Maxwell) potential
#   row1  (+) intrinsic logistic-derivative bell, scale w=1:  b(x)=e^-x/(1+e^-x)^2 = 0.25 sech^2(x/2)
#           sigma_int = pi w / sqrt(3)
#   row2  (x) ensemble eta spread, Gaussian sigma_eta = 1.25 sigma_int -> symmetric variance add
#           sigma_sym = sqrt(sigma_int^2 + sigma_eta^2) = sqrt(1+1.25^2) sigma_int ~ 1.6 sigma_int
#   row3  (+) one-sided exponential tail, ell = L_V = 1.5 w (finite-rate, asymmetric)
# x = (V - U_j)/w.
import numpy as np

w = 1.0
# compute on a padded grid [-12,16] to preserve area under convolution; display window is [-6,10]
dx = 0.02
x = np.arange(-12.0, 16.0 + dx / 2, dx)
N = len(x)


def logistic_deriv(t):
    e = np.exp(-t)
    return e / (1.0 + e) ** 2  # peak 0.25 at 0, area 1


b_int = logistic_deriv(x)
sigma_int = np.pi * w / np.sqrt(3.0)

# (x) symmetric Gaussian convolution, sigma_eta = 1.25 sigma_int (variance adds)
sigma_eta = 1.25 * sigma_int
gx = np.arange(-4 * sigma_eta, 4 * sigma_eta + dx / 2, dx)
gauss = np.exp(-0.5 * (gx / sigma_eta) ** 2)
gauss /= gauss.sum()
half = (len(gauss) - 1) // 2
b_broad = np.convolve(b_int, gauss, mode="full")[half: half + N]  # centered, area-preserving

# (+) causal one-sided exponential tail, L_V = 1.5 w
L = 1.5 * w
kx = np.arange(0.0, 10 * L + dx / 2, dx)
expk = np.exp(-kx / L)
expk /= expk.sum()
b_skew = np.convolve(b_broad, expk, mode="full")[:N]  # causal -> tail to +x

sigma_sym = np.sqrt(sigma_int ** 2 + sigma_eta ** 2)
print(f"sigma_int = pi w/sqrt3       = {sigma_int:.4f}")
print(f"sigma_eta = 1.25 sigma_int   = {sigma_eta:.4f}")
print(f"sigma_sym = sqrt(int^2+eta^2)= {sigma_sym:.4f}   (= {sigma_sym/sigma_int:.4f} sigma_int)")
print(f"tail length ell = L_V        = {L:.4f}")
print(f"peaks: intrinsic={b_int.max():.4f}  broadened={b_broad.max():.4f} at x={x[b_broad.argmax()]:.2f}  skewed={b_skew.max():.4f} at x={x[b_skew.argmax()]:.2f}")
print(f"areas: int={np.trapezoid(b_int,x):.4f}  broad={np.trapezoid(b_broad,x):.4f}  skew={np.trapezoid(b_skew,x):.4f}")


def sample(y, xs):
    yi = np.interp(xs, x, y)
    return " ".join(f"({a:.2f},{b:.4f})" for a, b in zip(xs, yi))


xs = np.arange(-6.0, 10.01, 0.5)
print("\n% row1 intrinsic bell:")
print(sample(b_int, xs))
print("\n% row2 broadened bell (x eta):")
print(sample(b_broad, xs))
print("\n% row3 skewed (+ tail L_V):")
print(sample(b_skew, xs))
print(f"\n% delta height (row0) use ~ {b_int.max():.3f} arrow; sigmas as horizontal scale bars")
