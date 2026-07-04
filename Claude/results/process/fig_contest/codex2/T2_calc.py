import math


def logistic_derivative(x: float, center: float, width: float = 0.006) -> float:
    z = (x - center) / width
    xi = 1.0 / (1.0 + math.exp(-z))
    return xi * (1.0 - xi)


u_values = [0.210, 0.140, 0.120, 0.085]
u_min, u_max = 0.060, 0.230
axis_len = 8.2


def map_u(u: float) -> float:
    return axis_len * (u - u_min) / (u_max - u_min)


print("transition voltage positions on 0.060--0.230 V axis")
for u in u_values:
    print(f"U={u:.3f} V -> x={map_u(u):.4f} cm")

grid = [0.060 + i * 0.010 for i in range(18)]
for u in u_values:
    pts = [(map_u(v), 0.55 * logistic_derivative(v, u) / 0.25) for v in grid]
    print(f"peak around {u:.3f} V:", " ".join(f"({x:.4f},{y:.4f})" for x, y in pts if y > 0.01))
