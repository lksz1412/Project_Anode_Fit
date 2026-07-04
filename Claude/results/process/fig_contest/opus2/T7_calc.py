#!/usr/bin/env python3
# T7 fig:reversal  --  causal memory tail direction (discharge vs charge mirror).
# GENUINE numeric evaluation of the first-order low-pass recurrence (eq:lowpass) and
# the peak shape (eq:peakshape), NOT a schematic.
#   xi_eq(V)  = 1/(1+exp[-sigma_d (V-U)/w])                (eq:xieq)
#   rho       = exp(-dgrid/L_V)                            (eq:lowpass)
#   xi_lag_i  = rho xi_lag_{i-1} + (1-rho) xi_eq_i ,  xi_lag_0 = xi_eq_0
#   charge (sigma_d<0): Reverse[ LowPass( Reverse[xi_eq] ) ]   (eq:reversal)
#   peak shape = (xi_eq - xi_lag)/L_V   (units 1/V; V,w,L_V in w-units here)
#   equilibrium species (dotted, direction-invariant) = xi_eq(1-xi_eq)/w
# Units: w = 1 (normalized), U = 0, dgrid = 0.05 w, L_V = 1.5 w.
import math

w, U, dgrid, LV = 1.0, 0.0, 0.05, 1.5
rho = math.exp(-dgrid/LV)
print(f"# w={w} U={U} dgrid={dgrid} L_V={LV}  rho=exp(-dgrid/L_V)={rho:.5f}")

def sig(z): return 1.0/(1.0+math.exp(-z))

def lowpass(seq):
    out=[seq[0]]
    for i in range(1,len(seq)):
        out.append(rho*out[-1] + (1.0-rho)*seq[i])
    return out

# fine grid for the recurrence, then subsample for plotting
V = [ -6.0 + i*dgrid for i in range(int((10.0+6.0)/dgrid)+1) ]   # -6 .. +10

def build(sigma_d):
    xieq = [ sig(sigma_d*(v-U)/w) for v in V ]
    if sigma_d >= 0:
        xilag = lowpass(xieq)
    else:
        xilag = lowpass(xieq[::-1])[::-1]        # reverse, low-pass, reverse
    peak = [ (xieq[i]-xilag[i])/LV for i in range(len(V)) ]
    eqsp = [ xieq[i]*(1.0-xieq[i])/w for i in range(len(V)) ]
    return xieq, xilag, peak, eqsp

def subsample(xy, step=6):
    return [xy[i] for i in range(0,len(xy),step)] + ([xy[-1]] if (len(xy)-1)%step else [])

def emit(sigma_d, tag):
    xieq,xilag,peak,eqsp = build(sigma_d)
    imax = max(range(len(V)), key=lambda i: peak[i])
    eqmax = max(range(len(V)), key=lambda i: eqsp[i])
    print(f"\n## {tag}  sigma_d={sigma_d:+.0f}")
    print(f"#  peak-shape max = {peak[imax]:.4f} at V={V[imax]:.2f} w  "
          f"(equilibrium-species max {eqsp[eqmax]:.4f} at V={V[eqmax]:.2f})")
    P = [(V[i],peak[i]) for i in range(0,len(V),6)]
    E = [(V[i],eqsp[i]) for i in range(0,len(V),6)]
    print(f"% {tag} peak shape (V in w-units, y in 1/w):")
    print(" ".join(f"({v:.2f},{y:.4f})" for v,y in P))
    print(f"% {tag} equilibrium species xi_eq(1-xi_eq)/w:")
    print(" ".join(f"({v:.2f},{y:.4f})" for v,y in E))
    return V[imax], peak[imax], V[eqmax], eqsp[eqmax]

emit(+1, "discharge")
emit(-1, "charge")
