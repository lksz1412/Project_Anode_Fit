import math


def logistic(z: float) -> float:
    return 1.0 / (1.0 + math.exp(-z))


def coords(points):
    return " ".join(f"({x:.4f},{y:.4f})" for x, y in points)


# Engineering-grid node centers used by T1_spine.tex.
nodes = {
    "input": (-1.1, 3.1),
    "N0": (-1.1, 1.95),
    "N1": (-1.1, 0.80),
    "N2": (2.6, 1.95),
    "N3": (5.2, 1.95),
    "N4_N5": (7.8, 1.95),
    "N6": (2.6, 0.35),
    "N7": (5.2, 0.35),
    "N8": (7.8, 0.35),
    "N9": (10.6, 1.15),
    "output": (10.6, -0.25),
}

xs = [-3, -2, -1.5, -1, -0.5, 0, 0.5, 1, 1.5, 2, 2.5, 3, 4]
bell = [(x, 2.2 * logistic(x) * (1.0 - logistic(x)) / 0.25) for x in xs]
tail = [(-3.0, 0.20), (-2.0, 0.48), (-1.0, 1.20), (0.0, 2.03),
        (0.8, 2.18), (1.6, 1.80), (2.4, 1.14), (3.2, 0.64), (4.0, 0.34)]

print("node centers")
for name, xy in nodes.items():
    print(f"{name}: ({xy[0]:.2f}, {xy[1]:.2f})")
print("equilibrium bell:", coords(bell))
print("causal tail:", coords(tail))
