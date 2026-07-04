# T7 fig:reversal — causal-memory tail direction, real discrete low-pass (eq:lowpass) evaluation.
# Work entirely in reduced coordinate z=(V-U)/w so L_V enters only via the ratio L_V/w
# (grid step Dz cancels w: rho = exp(-Dgrid/L_V) = exp(-(Dz*w)/(Lratio*w)) = exp(-Dz/Lratio)).
#
#   xi_eq(z)          : discharge sigma_d=+1 -> 1/(1+exp(-z));  charge sigma_d=-1 -> 1/(1+exp(+z))  (eq:xieq)
#   low-pass recursion: xi_lag[i] = rho*xi_lag[i-1] + (1-rho)*xi_eq[i], xi_lag[0]=xi_eq[0]  (eq:lowpass)
#   charge reversal   : filter on the array reversed in z (progress = V decreasing), then reverse back (eq:reversal)
#   peak shape        : (xi_eq - xi_lag)/Lratio, dimensionless (= w * physical peak shape)  (eq:peakshape)
#   equilibrium ref.  : xi(1-xi), max 0.25 at z=0  (eq:eqpeak, direction-invariant)
import math

Lratio = 1.5      # L_V / w  (matches the L_V=1.5 w_j example already used for fig:widthbudget)
Dz = 0.10         # grid step in z-units
rho = math.exp(-Dz / Lratio)

z_lo, z_hi = -6.0, 6.0
n = int(round((z_hi - z_lo) / Dz)) + 1
zs = [round(z_lo + i * Dz, 4) for i in range(n)]

def xi_eq_dis(z):
    return 1.0 / (1.0 + math.exp(-z))

def xi_eq_chg(z):
    return 1.0 / (1.0 + math.exp(z))

def lowpass(arr, rho):
    out = [arr[0]]
    for i in range(1, len(arr)):
        out.append(rho * out[-1] + (1 - rho) * arr[i])
    return out

xi_eq_d = [xi_eq_dis(z) for z in zs]
xi_lag_d = lowpass(xi_eq_d, rho)                      # ascending z = time order (discharge)

xi_eq_c = [xi_eq_chg(z) for z in zs]
xi_eq_c_rev = list(reversed(xi_eq_c))                  # progress = z decreasing -> reverse first
xi_lag_c_rev = lowpass(xi_eq_c_rev, rho)
xi_lag_c = list(reversed(xi_lag_c_rev))                # reverse back to ascending-z axis

peak_dis = [(xi_eq_d[i] - xi_lag_d[i]) / Lratio for i in range(n)]
peak_chg = [(xi_eq_c[i] - xi_lag_c[i]) / Lratio for i in range(n)]
peak_eqline = [xi_eq_d[i] * (1 - xi_eq_d[i]) for i in range(n)]  # direction-invariant equilibrium bell

# subsample for tikz plotting (every 4th point -> Dz_eff=0.4, plus endpoints)
step = 4
idx = list(range(0, n, step))
if idx[-1] != n - 1:
    idx.append(n - 1)

pts_eqline = [(zs[i], round(peak_eqline[i], 4)) for i in idx]
pts_dis = [(zs[i], round(peak_dis[i], 4)) for i in idx]
pts_chg = [(zs[i], round(peak_chg[i], 4)) for i in idx]

if __name__ == "__main__":
    print("rho =", round(rho, 5), " (Dz=", Dz, ", Lratio=L_V/w=", Lratio, ")")
    print("peak(equilibrium bell) max =", round(max(peak_eqline), 4), "at z=0 (expect 0.25)")
    print("peak_dis max =", round(max(peak_dis), 4), "at z =", zs[peak_dis.index(max(peak_dis))])
    print("peak_chg max =", round(max(peak_chg), 4), "at z =", zs[peak_chg.index(max(peak_chg))])
    print()
    print("equilibrium bell points:", pts_eqline)
    print()
    print("discharge peak-shape points (tail -> higher z/V):", pts_dis)
    print()
    print("charge peak-shape points (tail -> lower z/V):", pts_chg)
