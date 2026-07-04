#!/usr/bin/env python3
# T4 fig:barrier  --  Eyring activation landscape along the reaction coordinate.
#   (a) equilibrium (A=0): two wells of equal depth, barrier dG_a.
#   (b) driven (A>0, chi=1/2): tilt the landscape by the affinity A along reaction progress phi(x):
#       G_drv(x) = G_base(x) - A*phi(x),  phi in [0,1] from reactant well to product well.
#       forward barrier  = dG_a - chi A    (TS at phi=chi drops by chi A)
#       reverse barrier  = dG_a + (1-chi) A (product well drops by A -> reverse rises)
#   Eff. enthalpy note: dH_a^eff = dH_a - chi_d Omega (eq:dHeff).
# Base landscape: wells at x=1 (filled) and x=5 (empty), barrier at x=3.
#   G_base(x) = wb + dGa * sin^2( pi (x-1)/4 )  on [1,5]; symmetric raised cosine.
import math

wb   = 0.10      # well bottom
dGa  = 0.90      # barrier magnitude (peak = 1.00)
A    = 0.50      # affinity (driving force)
chi  = 0.50      # transition-state fractional position

def Gbase(x):
    if x<=1: return wb + dGa*math.sin(math.pi*(1.0-1.0)/4.0)**2 + 0.0*(1-x)  # flat-ish
    if x>=5: return wb
    return wb + dGa*math.sin(math.pi*(x-1.0)/4.0)**2
def phi(x):
    if x<=1: return 0.0
    if x>=5: return 1.0
    return (x-1.0)/4.0
def Gdrv(x):
    return Gbase(x) - A*phi(x)

xs=[0.0,0.5,1.0,1.5,2.0,2.5,3.0,3.5,4.0,4.5,5.0,5.5,6.0]
print("# x   G_base   G_driven")
for x in xs:
    print(f"  {x:.1f}  {Gbase(x):+.4f}  {Gdrv(x):+.4f}")

print("\n% (a) equilibrium landscape G_base:")
print(" ".join(f"({x:.2f},{Gbase(x):.4f})" for x in xs))
print(f"% (b) driven landscape G_driven [A={A:.2f}, chi={chi:.2f}]:")
print(" ".join(f"({x:.2f},{Gdrv(x):.4f})" for x in xs))

# barrier heights
fwd_eq  = (wb+dGa) - wb
fwd_drv = Gdrv(3.0) - Gdrv(1.0)
rev_drv = Gdrv(3.0) - Gdrv(5.0)
print(f"\n# equilibrium barrier dG_a          = {fwd_eq:.3f}")
print(f"# driven forward  dG_a - chi A       = {fwd_drv:.3f}   (= {dGa-chi*A:.3f})")
print(f"# driven reverse  dG_a + (1-chi) A   = {rev_drv:.3f}   (= {dGa+(1-chi)*A:.3f})")
print(f"# product-well drop by A             = {Gbase(5.0)-Gdrv(5.0):.3f}   (= {A:.3f})")
print(f"# TS drop by chi A                    = {Gbase(3.0)-Gdrv(3.0):.3f}   (= {chi*A:.3f})")
print(f"# peak positions: base TS at x=3 y={Gbase(3.0):.3f}; driven TS x=3 y={Gdrv(3.0):.3f}")
