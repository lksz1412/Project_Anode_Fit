# T4 fig:barrier — Eyring activation landscape, (a) equilibrium, (b) driven.
# Reaction coordinate x in [-1.5, 1.5]; wells at x=-1 (filled site) and x=+1 (empty site + ion),
# transition state at x=0.  Equilibrium landscape: G_eq(x) = dGa * cos^2(pi x / 2)  (smooth double well,
# both minima at 0, barrier height dGa at x=0).  [visualizes k ~ k0 exp(-dGa/RT), eq. Eyring]
# Driven landscape (affinity A>0, split fraction chi): tilt so the product well is lowered by A.
#   G_drv(x) = G_eq(x) - A * (x + 1)/2      (reactant x=-1 unchanged, product x=+1 lowered by A)
# => forward barrier = dGa - chi*A, reverse barrier = dGa + (1-chi)*A, with chi = 1/2 here.  [eq:bv]
import math

dGa = 1.00
A   = 0.60
chi = 0.5

def Geq(x):
    return dGa * math.cos(math.pi * x / 2.0) ** 2

def Gdrv(x):
    return Geq(x) - A * (x + 1.0) / 2.0

xs = [-1.5 + 3.0 * i / 40 for i in range(41)]

print("EQUILIBRIUM G_eq (x, G):")
print(" ".join(f"({x:.3f},{Geq(x):.4f})" for x in xs))
print()
print("DRIVEN G_drv (x, G):")
print(" ".join(f"({x:.3f},{Gdrv(x):.4f})" for x in xs))
print()

# key heights
print(f"reactant well  G_drv(-1) = {Gdrv(-1):.4f}")
print(f"transition st  G_drv(0)  = {Gdrv(0):.4f}   (= dGa - chi*A = {dGa - chi*A:.4f})")
print(f"product well   G_drv(+1) = {Gdrv(1):.4f}   (= -A = {-A:.4f})")
print(f"forward barrier = G_drv(0)-G_drv(-1) = {Gdrv(0)-Gdrv(-1):.4f}  (dGa - chi*A = {dGa-chi*A:.4f})")
print(f"reverse barrier = G_drv(0)-G_drv(+1) = {Gdrv(0)-Gdrv(1):.4f}  (dGa + (1-chi)*A = {dGa+(1-chi)*A:.4f})")
print(f"equilibrium barrier dGa = {dGa:.4f}")
