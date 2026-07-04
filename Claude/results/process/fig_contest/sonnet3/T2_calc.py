"""T2 fig:staging -- coordinate generator.

Improvement over the v7-11 figure: the gallery-filling cartoon (schematic,
even column spacing, unchanged in spirit from the original) is now tied to
a TRUE-TO-SCALE voltage axis carrying the four staging transitions' initial
values, each with a real dQ/dV peak glyph evaluated from the same
logistic-derivative bell used everywhere else in the chapter
(eq:belliden: xi(1-xi), height Q_j/(4 w_j) from eq:eqpeak), using the
literal initial values from table tab:staging (l.1984-1987) and the width
fallback values quoted at l.1210 (0.020/0.016/0.014/0.012 V).

This script prints ready-to-paste TikZ 'plot coordinates' strings so the
.tex file's numbers are a direct, checkable transcription of this
evaluation (no schematic freehand curve).
"""

import math

# ---- table tab:staging, initial values (l.1984-1987) ----
transitions = [
    # name,        U [V],  Q [Qcell], w [V]  (w from l.1210 width fallback list)
    ("4->3",   0.210, 0.10, 0.020),
    ("3->2L",  0.140, 0.12, 0.016),
    ("2L->2",  0.120, 0.25, 0.014),
    ("2->1",   0.085, 0.50, 0.012),
]

# ---- top-diagram schematic column geometry (unchanged from v7-11 figure) ----
colw = 0.85
col_x0 = {"4": 0.0, "3": 1.4, "2L": 2.8, "2": 4.2, "1": 5.6}
col_center = {k: v + colw / 2 for k, v in col_x0.items()}
boundary = {
    "4->3":  (col_center["4"] + col_center["3"]) / 2,
    "3->2L": (col_center["3"] + col_center["2L"]) / 2,
    "2L->2": (col_center["2L"] + col_center["2"]) / 2,
    "2->1":  (col_center["2"] + col_center["1"]) / 2,
}
print("== schematic top-diagram transition-boundary x (unchanged column layout) ==")
for name, x in boundary.items():
    print(f"{name:8s} boundary_x = {x:.3f}")

# ---- true-to-scale voltage axis mapping ----
Vmax, Vmin = 0.230, 0.065
xlo, xhi = 0.3, 6.2
k = (xhi - xlo) / (Vmax - Vmin)  # units of x per volt


def x_of_V(V):
    return xlo + (Vmax - V) * k


print(f"\n== voltage-axis mapping: x(V) = {xlo} + (({Vmax}) - V) * {k:.4f} ==")
axis_x = {name: x_of_V(U) for name, U, Q, w in transitions}
for name, x in axis_x.items():
    print(f"{name:8s} U={dict((n,U) for n,U,Q,w in transitions)[name]:.3f} V  ->  x = {x:.3f}")

# ---- bell heights: Q/(4w) at xi=1/2 (eq:eqpeak), globally rescaled ----
raw_heights = [Q / (4 * w) for _, U, Q, w in transitions]
hmax = max(raw_heights)
scale = 1.6 / hmax
print(f"\n== relative peak heights Q/(4w) (eq:eqpeak), global scale factor {scale:.4f} to cap at 1.6 ==")
for (name, U, Q, w), h in zip(transitions, raw_heights):
    print(f"{name:8s} Q/(4w) = {h:7.3f}  ->  drawn height = {h*scale:.3f}")

# ---- per-transition bell curve samples: dQ/dV = Q * xi(1-xi)/w vs V, in (x,y) ----
print("\n== TikZ plot coordinates per transition (V spans U +/- 3.4 w) ==")
for name, U, Q, w in transitions:
    pts = []
    for i in range(-17, 18):
        V = U + (i / 17) * 3.4 * w
        z = (V - U) / w
        xi = 1.0 / (1.0 + math.exp(-z))
        dqdv = Q * xi * (1 - xi) / w
        x = x_of_V(V)
        y = dqdv * scale
        pts.append(f"({x:.3f},{y:.4f})")
    print(f"% {name}  (U={U} V, w={w} V, Q={Q} Qcell)")
    print(" ".join(pts))
    print()
