"""Coordinate source for T7_reversal.tex."""

from math import cosh, exp

zs = [-4.0, -3.5, -3.0, -2.5, -2.0, -1.5, -1.0, -0.5, 0.0,
      0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0]


def bell(z: float) -> float:
    return 1.0 / (4.0 * cosh(z / 2.0) ** 2)


def causal(z: float, length: float = 1.1, step: float = 0.01) -> float:
    u = -12.0
    total = 0.0
    while u <= z:
        total += bell(u) * exp(-(z - u) / length) / length * step
        u += step
    return total


print("T7 equilibrium bell, discharge causal tail, charge mirror")
print("eq  " + " ".join(f"({z:.1f},{2.2*bell(z)/0.25:.4f})" for z in zs))
print("dis " + " ".join(f"({z:.1f},{2.2*causal(z)/0.25:.4f})" for z in zs))
print("chg " + " ".join(f"({z:.1f},{2.2*causal(-z)/0.25:.4f})" for z in zs))
