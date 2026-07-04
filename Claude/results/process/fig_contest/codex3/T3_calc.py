"""Coordinate source for T3_hysloop.tex."""

from math import log, sqrt


def y_eq(xi: float) -> float:
    return log(xi / (1.0 - xi)) + 4.0 * (1.0 - 2.0 * xi)


xis = [
    0.02, 0.04, 0.06, 0.08, 0.10, 0.12, 0.1464, 0.18, 0.22,
    0.28, 0.34, 0.40, 0.46, 0.50, 0.54, 0.60, 0.66, 0.72,
    0.78, 0.82, 0.8536, 0.88, 0.90, 0.92, 0.94, 0.96, 0.98,
]
spinodal_lo = (1.0 - sqrt(0.5)) / 2.0
spinodal_hi = (1.0 + sqrt(0.5)) / 2.0

print("T3 V_eq coordinates for y = ln[xi/(1-xi)] + 4(1-2xi)")
print(" ".join(f"({x:.4f},{y_eq(x):.4f})" for x in xis))
print(f"spinodal_lo=({spinodal_lo:.4f},{y_eq(spinodal_lo):.4f})")
print(f"spinodal_hi=({spinodal_hi:.4f},{y_eq(spinodal_hi):.4f})")
