# T4 fig:barrier — Eyring activation landscape, equilibrium vs driven.
# Closed-form model consistent with eq:bv/eq:db (detailed balance) and the transfer-coefficient
# split chi used throughout Sec. N7 (eq:chid, eq:dHeff):
#
#   G0(x)  = Gmin + (Gts-Gmin) * (1 - u(x)^2)^2 ,   u(x) = (x - x_ts) / half_width
#            -- closed-form symmetric quartic double well: minima at x=x_R,x_P (u=-+1,
#               G=Gmin), maximum at TS x=x_ts (u=0, G=Gts).  DeltaG_a = Gts-Gmin.
#
#   h(x)   = fractional reaction-coordinate position in [0,1], h(x_R)=0, h(x_ts)=chi,
#            h(x_P)=1 (piecewise-linear reaction coordinate map).
#
#   G(x)   = G0(x) - A*h(x)     -- driven landscape, affinity A tilts the whole coordinate.
#
# This reproduces eq:bv exactly at the two barrier heights:
#   forward barrier  = G(x_ts)-G(x_R) = DeltaG_a - chi*A
#   reverse barrier  = G(x_ts)-G(x_P) = DeltaG_a + (1-chi)*A
# i.e. the same chi/(1-chi) split that turns the rate ratio r+/r- into detailed balance
# exp(A/RT) (eq:db) independent of chi.
import math

Gmin = 0.10          # well depth (both wells, equilibrium case)
Gts = 1.00           # transition-state free energy (equilibrium case)
dGa = Gts - Gmin     # = 0.90  (activation barrier, A=0 reference)
x_R, x_ts, x_P = 1.0, 3.0, 5.0
half_width = 2.0     # x_ts - x_R = x_P - x_ts

chi = 0.35           # transfer coefficient (asymmetric example, brief calls for chi/(1-chi) split)
A = 0.60             # affinity A (same units as G), driven case

def G0(x):
    u = (x - x_ts) / half_width
    return Gmin + dGa * (1 - u * u) ** 2

def h(x):
    if x <= x_R:
        return 0.0
    if x < x_ts:
        return chi * (x - x_R) / half_width
    if x < x_P:
        return chi + (1 - chi) * (x - x_ts) / half_width
    return 1.0

def G_driven(x):
    return G0(x) - A * h(x)

xs = [round(0.7 + 0.1 * i, 2) for i in range(int((5.3 - 0.7) / 0.1) + 1)]
pts_eq = [(x, round(G0(x), 4)) for x in xs]
pts_dr = [(x, round(G_driven(x), 4)) for x in xs]

fwd_barrier = G_driven(x_ts) - G_driven(x_R)
rev_barrier = G_driven(x_ts) - G_driven(x_P)
fwd_expect = dGa - chi * A
rev_expect = dGa + (1 - chi) * A

if __name__ == "__main__":
    print("DeltaG_a =", dGa)
    print("driven forward barrier  =", round(fwd_barrier, 4), " expect DeltaG_a-chi*A =", round(fwd_expect, 4))
    print("driven reverse barrier  =", round(rev_barrier, 4), " expect DeltaG_a+(1-chi)*A =", round(rev_expect, 4))
    print("G_driven(x_R) =", round(G_driven(x_R), 4), " G_driven(x_P) =", round(G_driven(x_P), 4),
          " (drop = A =", round(G_driven(x_R) - G_driven(x_P), 4), ")")
    print()
    print("equilibrium curve points G0(x):")
    print(pts_eq)
    print()
    print("driven curve points G_driven(x):")
    print(pts_dr)
