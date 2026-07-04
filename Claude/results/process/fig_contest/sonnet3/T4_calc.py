"""T4 fig:barrier -- coordinate generator.

The chapter's eq:bv (l.1220) fixes only the DISCRETE quantities of the
Eyring landscape: well heights (0 and -A) and barrier heights measured
from each well (Delta_Ga - chi*A forward, Delta_Ga + (1-chi)*A reverse).
It does not give a continuous functional form for the curve connecting
well -> barrier -> well (no chapter figure ever did — the v7-11 figure's
curve was a freehand 'plot smooth' with no formula at all). This script
replaces that freehand curve with an explicit, reproducible smoothstep
(raised-cosine) interpolation between the exact analytic endpoints, so
"schematic" freehand numbers are eliminated: every plotted point is
either an exact endpoint from eq:bv or an evaluation of a disclosed
interpolation formula, not a guess.

chi controls the transition-state HORIZONTAL position along the reaction
coordinate (chi=0 -> TS at the reactant well, chi=1 -> TS at the product
well), consistent with the chapter's description of chi as "transition
state fractional position" (symbol table l.249).
"""

import math

xL, xR = -1.0, 1.0


def smoothstep(x0, y0, x1, y1, n=13):
    """Raised-cosine interpolation, zero slope at both ends."""
    pts = []
    for i in range(n):
        t = i / (n - 1)
        s = (1 - math.cos(math.pi * t)) / 2
        x = x0 + (x1 - x0) * t
        y = y0 + (y1 - y0) * s
        pts.append((x, y))
    return pts


def landscape(dGa, A, chi, n_half=13):
    wellL, wellR = 0.0, -A
    xTS = xL + (xR - xL) * chi
    apex = dGa - chi * A
    left = smoothstep(xL, wellL, xTS, apex, n=n_half)
    right = smoothstep(xTS, apex, xR, wellR, n=n_half)
    # avoid duplicating the apex point
    pts = left + right[1:]
    return pts, xTS, apex, wellL, wellR


def fmt(pts):
    return " ".join(f"({x:.4f},{y:.4f})" for x, y in pts)


# ---- (a) equilibrium: A=0, chi=0.5 (symmetric well, TS centered) ----
dGa = 1.0
pts_a, xTS_a, apex_a, wL_a, wR_a = landscape(dGa, 0.0, 0.5)
print("== panel (a) equilibrium: A=0, chi=0.5 ==")
print(f"xTS={xTS_a:.3f}  apex(y)={apex_a:.3f}  wellL={wL_a:.3f}  wellR={wR_a:.3f}")
print(fmt(pts_a))

# ---- (b) driven: A=0.5*dGa, chi=0.35 (early, reactant-like TS) ----
A = 0.5
chi = 0.35
pts_b, xTS_b, apex_b, wL_b, wR_b = landscape(dGa, A, chi)
fwd_barrier = apex_b - wL_b           # = dGa - chi*A
rev_barrier = apex_b - wR_b           # = dGa + (1-chi)*A
print("\n== panel (b) driven: A=0.5, chi=0.35 ==")
print(f"xTS={xTS_b:.3f}  apex(y)={apex_b:.3f}  wellL={wL_b:.3f}  wellR={wR_b:.3f}")
print(f"forward barrier (from left well)  = {fwd_barrier:.4f}  (expect dGa-chi*A = {dGa-chi*A:.4f})")
print(f"reverse barrier (from right well) = {rev_barrier:.4f}  (expect dGa+(1-chi)*A = {dGa+(1-chi)*A:.4f})")
assert abs(fwd_barrier - (dGa - chi * A)) < 1e-9
assert abs(rev_barrier - (dGa + (1 - chi) * A)) < 1e-9
print("[ok] forward/reverse barrier heights match eq:bv exactly.")
print(fmt(pts_b))

# reference dotted copy of curve (a) overlaid in panel (b), for comparison
print("\n== panel (b) background dotted reference = curve (a), same coordinates ==")
print(fmt(pts_a))

print(f"\nchi-split tick positions on the reaction-coordinate axis of panel (b): "
      f"reactant well x={xL}, TS x={xTS_b:.3f} (fraction chi={chi} of the way to product), "
      f"product well x={xR}")
print(f"chi*A = {chi*A:.4f} (drop of forward barrier vs equilibrium apex 1.0), "
      f"(1-chi)*A = {(1-chi)*A:.4f} (rise of reverse barrier vs equilibrium apex 1.0)")
