# -*- coding: utf-8 -*-
# T2 fig:staging (opus3) — graphite staging gallery filling linked to a shared potential axis.
# Geometry + the transition -> U_j -> dQ/dV-peak mapping (values from tab:staging).
# Columns are evenly spaced (schematic layers); the bottom axis is a TRUE linear V axis so the
# slanted leader lines encode the real (non-uniform) transition-potential spacing.
import numpy as np

# tab:staging: transition, U [V], Q [Q_cell]
TRANS = [("4->3", 0.210, 0.10),
         ("3->2L", 0.140, 0.12),
         ("2L->2", 0.120, 0.25),
         ("2->1", 0.085, 0.50)]

U = np.array([t[1] for t in TRANS])
Q = np.array([t[2] for t in TRANS])
assert np.all(np.diff(U) < 0), "U must decrease along 4->3->2L->2->1"
print("potentials strictly decreasing 4->1:", list(U), "OK")

# five stage columns: left edges, width, centers
pitch, colw = 1.6, 0.9
left = np.arange(5) * pitch
center = left + colw / 2.0
print("column left edges:", [f"{v:.2f}" for v in left])
print("column centers   :", [f"{v:.2f}" for v in center])

# transition midpoints (between adjacent column centers)
mid = (center[:-1] + center[1:]) / 2.0
print("transition midpoints (top):", [f"{v:.3f}" for v in mid])

# bottom potential axis: linear V -> x, decreasing V left->right
Vmax, Vmin = 0.23, 0.06
xspan = 7.3


def xV(v):
    return (Vmax - v) / (Vmax - Vmin) * xspan


ticks = xV(U)
print("\ntransition   U[V]   tick_x(on V-axis)   Q     peak_height(0.4+1.8Q)")
peak_h = 0.4 + 1.8 * Q
for (name, u, q), tx, ph in zip(TRANS, ticks, peak_h):
    print(f"{name:7s}  {u:.3f}   x={tx:.3f}            {q:.2f}  {ph:.3f}")

print("\nleaders (top transition midpoint) -> (axis tick):")
for (name, u, q), m, tx in zip(TRANS, mid, ticks):
    print(f"  {name:7s}:  ({m:.3f}, top) -> ({tx:.3f}, axis)")

print(f"\naxis endpoints: V={Vmax} at x={xV(Vmax):.2f}  ... V={Vmin} at x={xV(Vmin):.2f}")
print("axis reference ticks (label positions):")
for v in [0.20, 0.15, 0.10]:
    print(f"  V={v:.2f} -> x={xV(v):.3f}")

# gallery fill pattern per stage (k = layer index 1..6), preserved from original figure
PATTERN = {"stage4": ("dark", [1, 5]), "stage3": ("dark", [1, 4]),
           "stage2L": ("light", [1, 3, 5]), "stage2": ("dark", [1, 3, 5]),
           "stage1": ("dark", [1, 2, 3, 4, 5, 6])}
print("\ngallery fill pattern (preserved):")
for s, (shade, ks) in PATTERN.items():
    print(f"  {s:8s} {shade:6s} galleries k={ks}")
