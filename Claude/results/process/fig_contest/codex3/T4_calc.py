"""Coordinate source for T4_barrier.tex."""


from math import cos, pi


def base_g(x: float) -> float:
    return 0.10 + 0.90 * cos(pi * (x - 3.0) / 4.0) ** 2


def driven_g(x: float, affinity: float = 0.70) -> float:
    # Reactant x=1 unchanged, product x=5 lowered by A, transition x=3 lowered by chi A.
    return base_g(x) - affinity * (x - 1.0) / 4.0


xs = [0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0]
print("T4 equilibrium landscape")
print(" ".join(f"({x:.1f},{base_g(x):.3f})" for x in xs))
print("T4 driven landscape, A=0.70, chi=0.50")
print(" ".join(f"({x:.1f},{driven_g(x):.3f})" for x in xs))
print(f"forward barrier={driven_g(3.0) - driven_g(1.0):.3f}")
print(f"reverse barrier={driven_g(3.0) - driven_g(5.0):.3f}")
