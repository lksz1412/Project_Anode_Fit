def geq(x: float) -> float:
    return 0.10 + 0.90 * ((x - 1.0) ** 2 * (x - 5.0) ** 2 / 16.0)


def gdriven(x: float, affinity: float = 0.35) -> float:
    return geq(x) - affinity * ((x - 1.0) / 4.0)


xs = [0.25 * i for i in range(25)]
print("equilibrium quartic double-well:")
print(" ".join(f"({x:.4f},{geq(x):.4f})" for x in xs))
print("driven landscape, A=0.35, chi=1/2:")
print(" ".join(f"({x:.4f},{gdriven(x):.4f})" for x in xs))
print("barriers: DeltaG_a=0.9000, forward=0.7250, reverse=1.0750")
