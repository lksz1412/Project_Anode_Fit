# T2 fig:staging — bottom dQ/dV(V) axis coordinates.
# dQ/dV = sum_j Q_j * xi_j(1-xi_j)/w_j  with xi_j = logistic((V-U_j)/w_j)  [eq:xieq, eq:eqpeak, discharge sigma_d=+1]
# Transition centers U_j and starting widths w_j are the doc initial values (tab:staging / sec:width).
import math

U = [0.210, 0.140, 0.120, 0.085]      # V   (stage 4->3, 3->2L, 2L->2, 2->1)
w = [0.020, 0.016, 0.014, 0.012]      # V   starting width scales
Q = [1.0, 1.0, 1.0, 1.0]             # equal capacity weights (schematic amplitude)
names = ["4->3", "3->2L", "2L->2", "2->1"]

def dqdv(V):
    s = 0.0
    for Uj, wj, Qj in zip(U, w, Q):
        z = (V - Uj) / wj
        xi = 1.0 / (1.0 + math.exp(-z))
        s += Qj * xi * (1.0 - xi) / wj
    return s

# V grid
Vmin, Vmax = 0.050, 0.250
N = 121
Vs = [Vmin + (Vmax - Vmin) * i / (N - 1) for i in range(N)]
ys = [dqdv(V) for V in Vs]
ymax = max(ys)

# tikz mapping: x increases as V DECREASES (stage-4/high-U on the left, aligning with top columns).
W = 6.45   # bottom axis width (matches top stage arrow span 0..6.45)
H = 1.5    # plotted curve height (tikz units)
def xplot(V):
    return (Vmax - V) / (Vmax - Vmin) * W
def yplot(y):
    return y / ymax * H

coords = " ".join(f"({xplot(V):.3f},{yplot(y):.3f})" for V, y in zip(Vs, ys))
print("CURVE:")
print(coords)
print()
print("PEAKS (name, U, xplot, ypeak):")
for nm, Uj in zip(names, U):
    yp = yplot(dqdv(Uj))
    print(f"  {nm:6s} U={Uj:.3f}  x={xplot(Uj):.3f}  y={yp:.3f}")
print()
# axis V ticks at these values -> xplot
print("V-TICKS (V, xplot):")
for Vt in [0.25, 0.20, 0.15, 0.10, 0.05]:
    print(f"  V={Vt:.2f}  x={xplot(Vt):.3f}")
print()
# stage-boundary x positions in the TOP panel (col starts 0,1.4,2.8,4.2,5.6; colw 0.85)
print("STAGE-BOUNDARY x (top panel) and matching peak xplot (bottom):")
bnd = [1.125, 2.525, 3.925, 5.325]
for nm, Uj, b in zip(names, U, bnd):
    print(f"  {nm:6s} boundary_x={b:.3f}  peak_xplot={xplot(Uj):.3f}")
