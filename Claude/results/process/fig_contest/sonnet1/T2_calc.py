# T2 fig:staging — bottom-axis dQ/dV peaks linked to the gallery-filling columns above.
# Uses the initial-value table (tab:staging) and the equilibrium-peak formula (eq:eqpeak,
# gamma=0 / no tail at the initial state per Sec. "staging 전이 초기값"):
#   xi_eq(V) = 1/(1+exp[-(V-U_j)/w_j])         (sigma_d=+1, discharge, no branch shift)
#   dQ/dV|_j = Q_j * xi_eq(1-xi_eq) / w_j        (eq:eqpeak, single transition, no tail)
# Table values (tab:staging, w fallback list stated in the paragraph right after the table):
#   stage      U [V]   Q [Qcell]   w [V]
#   4->3       0.210   0.10        0.020
#   3->2L      0.140   0.12        0.016
#   2L->2      0.120   0.25        0.014
#   2->1       0.085   0.50        0.012
import math

stages = [
    ("4 to 3",    0.210, 0.10, 0.020),
    ("3 to 2L",   0.140, 0.12, 0.016),
    ("2L to 2",   0.120, 0.25, 0.014),
    ("2 to 1",    0.085, 0.50, 0.012),
]

def dqdv(V, U, Q, w):
    xi = 1.0 / (1.0 + math.exp(-(V - U) / w))
    return Q * xi * (1 - xi) / w

V_grid = [round(0.02 + 0.002 * i, 4) for i in range(int((0.27 - 0.02) / 0.002) + 1)]

curves = {}
for name, U, Q, w in stages:
    peak_height = Q * 0.25 / w
    pts = [(V, round(dqdv(V, U, Q, w), 4)) for V in V_grid
           if abs(V - U) <= 5 * w]   # keep only the visually relevant window per peak
    curves[name] = dict(U=U, Q=Q, w=w, peak_height=round(peak_height, 4), pts=pts)

# bottom-axis layout: map V in [0.05,0.25] onto gallery x-units [0,6.45] (V decreasing
# left-to-right, matching the lithiation direction of the gallery above: x=6.45*(0.25-V)/0.20)
def x_of_V(V):
    return round(6.45 * (0.25 - V) / 0.20, 4)

if __name__ == "__main__":
    for name, U, Q, w in stages:
        c = curves[name]
        print(f"{name}: U={U} V, Q={Q} Qcell, w={w} V, peak height Q/(4w) = {c['peak_height']}, "
              f"x-position = {x_of_V(U)}")
    print()
    for name, _, _, _ in stages:
        # subsample every 3rd point for a clean tikz plot[smooth] coordinate list
        sub = curves[name]["pts"][::3]
        tikz_pts = " ".join(f"({x_of_V(V)},{round(val,3)})" for V, val in sub)
        print(f"--- {name}: tikz coordinates (x=gallery units, y=dQ/dV) ---")
        print(tikz_pts)
        print()
