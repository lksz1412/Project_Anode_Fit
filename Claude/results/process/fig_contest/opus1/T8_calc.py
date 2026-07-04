# T8 fig:widthbudget — width budget storyboard (eq:widthbudget).
# Stage 0: equilibrium delta at the Maxwell/plateau potential.
# Stage 1 (2): intrinsic logistic-derivative bell, scale w.   f2(x) = (1/(4w)) sech^2(x/(2w))
# Stage 2 (2 (x) 3): variance addition with ensemble eta.  sigma_eta = 1.25 sigma_int
#            => sigma_sym = sqrt(1+1.25^2) sigma_int ~ 1.6 sigma_int => effective scale 1.6 w
#            f23(x) = (1/(4*1.6w)) sech^2(x/(2*1.6w))
# Stage 3 (+1): convolve f23 with one-sided exponential kernel k(t)=(1/L)exp(-t/L), t>=0, L=1.5w  (finite rate).
# x in units of w (w=1).  Numeric convolution on a fine grid.
import math

w  = 1.0
sc = 1.6      # effective broadened scale (from sigma_eta = 1.25 sigma_int)
L  = 1.5      # one-sided exponential length L_V

def sech2(u):
    c = math.cosh(u)
    return 1.0 / (c * c)

def f_intrinsic(x):
    return (1.0 / (4.0 * w)) * sech2(x / (2.0 * w))

def f_broad(x):
    return (1.0 / (4.0 * sc * w)) * sech2(x / (2.0 * sc * w))

# fine grid for convolution
dxf = 0.01
xf = [(-40.0) + dxf * i for i in range(int(80.0 / dxf) + 1)]
fb = [f_broad(x) for x in xf]

# one-sided exponential convolution: g(x) = sum_{t>=0} k(t) f_broad(x - t) dt
def f_tail(x):
    s = 0.0
    t = 0.0
    while t < 30.0:
        s += (1.0 / L) * math.exp(-t / L) * f_broad(x - t) * dxf
        t += dxf
    return s

# output grid for plotting
xs = [-6, -5, -4, -3, -2, -1, -0.5, 0, 0.5, 1, 1.5, 2, 2.5, 3, 4, 5, 6, 7, 8, 9, 10]

print("INTRINSIC f2 (x, f):    peak f2(0) =", round(f_intrinsic(0), 4))
print(" ".join(f"({x:.2f},{f_intrinsic(x):.4f})" for x in xs))
print()
print("BROADENED f23 (x, f):   peak f23(0) =", round(f_broad(0), 4))
print(" ".join(f"({x:.2f},{f_broad(x):.4f})" for x in xs))
print()
print("TAIL f1 (x, f):   (one-sided exp convolution, L=1.5)")
tail_vals = [(x, f_tail(x)) for x in xs]
print(" ".join(f"({x:.2f},{v:.4f})" for x, v in tail_vals))
print()
xmax = max(tail_vals, key=lambda p: p[1])
print(f"tail peak at x={xmax[0]:.2f}, f={xmax[1]:.4f}  (shifted to +x by finite-rate skew)")
# sanity vs doc numbers: f_intrinsic(0)=0.25, f_broad(0)=1/(4*1.6)=0.15625
print(f"check: 1/(4*1.6) = {1.0/(4*1.6):.5f}")
