"""Coordinate source for T8_widthbudget.tex."""

from math import exp

xs = [-6, -5, -4, -3, -2, -1, -0.5, 0, 0.5, 1, 1.5, 2, 2.5, 3, 4, 5, 6, 7, 8, 9, 10]


def logistic_deriv(x: float, scale: float = 1.0) -> float:
    xi = 1.0 / (1.0 + exp(-x / scale))
    return xi * (1.0 - xi) / scale


def skewed_tail(x: float, length: float = 1.5, step: float = 0.02) -> float:
    u = -18.0
    total = 0.0
    while u <= x:
        total += logistic_deriv(u, 1.6) * exp(-(x - u) / length) / length * step
        u += step
    return total


print("T8 width budget curves")
print("intrinsic " + " ".join(f"({x:.1f},{logistic_deriv(x):.4f})" for x in xs))
print("symmetric " + " ".join(f"({x:.1f},{logistic_deriv(x, 1.6):.4f})" for x in xs))
print("tail      " + " ".join(f"({x:.1f},{skewed_tail(x):.4f})" for x in xs))
