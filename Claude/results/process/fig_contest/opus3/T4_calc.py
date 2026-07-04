# -*- coding: utf-8 -*-
# T4 fig:barrier (opus3) — single reaction hop, equilibrium vs driven landscape overlaid.
# Reaction-coordinate free-energy surface over one hop (departure well -> TS -> arrival well),
# x in [1,5], analytic raised cosine so coordinates are a direct numerical evaluation:
#   G0(x)      = 0.55 - 0.45 cos( pi (x-1)/2 )          (equilibrium, symmetric)
#   Gdrv(x)    = G0(x) - A (x-1)/4                       (driven, tilted by affinity A)
# Wells at x=1 (departure) and x=5 (arrival); transition state at x=3.
# Barriers:  forward = G_TS - G_departure = dGa - chi*A ;  reverse = G_TS - G_arrival = dGa + (1-chi)*A.
# chi = 1/2, A = 0.35 (arb. free-energy units), dGa = G_TS(eq) - G_well(eq) = 1.0 - 0.1 = 0.9.
import numpy as np

A = 0.35
chi = 0.5
dGa = 0.9


def G0(x):
    return 0.55 - 0.45 * np.cos(np.pi * (x - 1.0) / 2.0)


def Gdrv(x):
    return G0(x) - A * (x - 1.0) / 4.0


xs = np.linspace(1.0, 5.0, 25)
print("% EQUILIBRIUM G0(x)")
print(" ".join(f"({x:.3f},{G0(x):.4f})" for x in xs))
print("\n% DRIVEN Gdrv(x)")
print(" ".join(f"({x:.3f},{Gdrv(x):.4f})" for x in xs))

# key points
print("\n-- key points --")
for name, x in [("departure well", 1.0), ("TS", 3.0), ("arrival well", 5.0)]:
    print(f"{name:16s} x={x}:  G0={G0(x):.4f}  Gdrv={Gdrv(x):.4f}")

fwd_eq = G0(3) - G0(1)
fwd_drv = Gdrv(3) - Gdrv(1)
rev_drv = Gdrv(3) - Gdrv(5)
print(f"\ndGa (eq barrier)              = {fwd_eq:.4f}")
print(f"forward barrier (driven)      = {fwd_drv:.4f}   [= dGa - chi*A = {dGa - chi*A:.4f}]")
print(f"reverse barrier (driven)      = {rev_drv:.4f}   [= dGa + (1-chi)*A = {dGa + (1-chi)*A:.4f}]")
print(f"well drop (arrival lowered)   = {G0(5) - Gdrv(5):.4f}   [= A = {A:.4f}]")
print(f"TS lowered by chi*A           = {G0(3) - Gdrv(3):.4f}   [= chi*A = {chi*A:.4f}]")
print(f"detailed balance  r+/r- = exp(A/RT); rate ratio grows with affinity A (eq:db)")
