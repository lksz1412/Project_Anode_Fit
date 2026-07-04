import math


def logistic_derivative(x: float, scale: float = 1.0) -> float:
    z = x / scale
    xi = 1.0 / (1.0 + math.exp(-z))
    return xi * (1.0 - xi) / scale


def broadened(x: float) -> float:
    return logistic_derivative(x, 1.6)


def tail_convolution(x: float, lag: float = 1.5, du: float = 0.01) -> float:
    lo = -20.0
    n = int((x - lo) / du)
    area = 0.0
    for i in range(n + 1):
        u = lo + i * du
        weight = 0.5 if i in (0, n) else 1.0
        area += weight * broadened(u) * (1.0 / lag) * math.exp(-(x - u) / lag) * du
    return area


xs = [-6, -5, -4, -3, -2, -1, -0.5, 0, 0.5, 1, 1.5, 2, 2.5, 3, 4, 5, 6, 7, 8, 9, 10]
print("intrinsic:", " ".join(f"({x:.4f},{logistic_derivative(x):.4f})" for x in xs))
print("broad:", " ".join(f"({x:.4f},{broadened(x):.4f})" for x in xs))
print("tail:", " ".join(f"({x:.4f},{tail_convolution(x):.4f})" for x in xs))
