"""T7 fig:reversal -- coordinate generator.

Implements the ACTUAL discrete low-pass recursion (eq:lowpass, l.1829):
    xi_lag[i] = rho*xi_lag[i-1] + (1-rho)*xi_eq[i],  rho = exp(-dgrid/L_V)
and the causal-tail peak shape (eq:peakshape): (xi_eq - xi_lag)/L_V,
with the charge-direction grid reversal of eq:reversal (l.1901-1907):
    discharge: LowPass(xi_eq) applied left-to-right (V increasing)
    charge:    Reverse[LowPass(Reverse[xi_eq])]  (V decreasing is the
               true time order, so the filter runs right-to-left)

This replaces the v7-11 figure's freehand bell+tail curves with numbers
that are the direct output of the chapter's own recursion, run on a
padded fine grid (dgrid=1 mV) and then subsampled for plotting.
"""

import math

R, F = 8.314462618, 96485.33212
w = R * 298.15 / F           # 25.69 mV, matches the 298 K reference used elsewhere
L_V = 0.015                  # 15 mV -- well above the nu*dgrid=2*1mV branch threshold
dgrid = 0.001                # 1 mV fine grid for the filter itself
rho = math.exp(-dgrid / L_V)
print(f"w={w*1000:.3f} mV, L_V={L_V*1000:.1f} mV, dgrid={dgrid*1000:.1f} mV, rho={rho:.5f}")

Vlo, Vhi = -0.140, 0.140     # padded range so edge transients sit outside +/-100 mV window
n = round((Vhi - Vlo) / dgrid) + 1
Vgrid = [Vlo + i * dgrid for i in range(n)]


def xi_eq(V):
    z = V / w
    return 1.0 / (1.0 + math.exp(-z))


xi_dis = [xi_eq(V) for V in Vgrid]        # sigma_d=+1 equilibrium species, increasing in V
xi_chg = [1.0 - v for v in xi_dis]        # sigma_d=-1 equilibrium species = mirror, decreasing in V


def lowpass(target):
    lag = [target[0]]
    for i in range(1, len(target)):
        lag.append(rho * lag[-1] + (1 - rho) * target[i])
    return lag


# ---- discharge: time order = grid ascending order (V increasing = progress direction) ----
lag_dis = lowpass(xi_dis)
peak_dis = [(xi_dis[i] - lag_dis[i]) / L_V for i in range(n)]

# ---- charge: time order = grid DESCENDING (eq:reversal) ----
# xi_chg[::-1] is the charge equilibrium species read off in true time order (rises 0->1,
# same shape as discharge's rise, just walked over the reversed voltage grid)
target_chg_time_order = xi_chg[::-1]
lag_chg_time_order = lowpass(target_chg_time_order)
lag_chg = lag_chg_time_order[::-1]        # back to ascending-V grid order for output
peak_chg = [(xi_chg[i] - lag_chg[i]) / L_V for i in range(n)]

print(f"discharge peak: max={max(peak_dis):.3f} at V={Vgrid[peak_dis.index(max(peak_dis))]*1000:.1f} mV "
      f"(equilibrium centre is V=0)")
print(f"charge    peak: max={max(peak_chg):.3f} at V={Vgrid[peak_chg.index(max(peak_chg))]*1000:.1f} mV")
assert all(p >= -1e-9 for p in peak_dis), "discharge peak shape went negative"
assert all(p >= -1e-9 for p in peak_chg), "charge peak shape went negative"
print("[ok] both peak shapes stay non-negative (S3/S7 sign check).")

# mirror check: charge peak at +x should equal discharge peak at -x (within the interior,
# away from the padded edges) since the whole construction is antisymmetric about V=0
mirror_err = []
for i in range(n):
    V = Vgrid[i]
    if abs(V) > 0.100:
        continue
    j = n - 1 - i  # grid index of -V
    mirror_err.append(abs(peak_chg[i] - peak_dis[j]))
print(f"max |peak_chg(V) - peak_dis(-V)| over |V|<=100 mV = {max(mirror_err):.2e} (mirror symmetry check)")
assert max(mirror_err) < 1e-8, "charge/discharge should be exact mirror images"
print("[ok] charge is the exact mirror image of discharge (S7 sign check).")

# ---- subsample to +/-100 mV every 5 mV for the figure ----
def subsample(values):
    out = []
    for i, V in enumerate(Vgrid):
        if abs(V) > 0.1005:
            continue
        Vmv = round(V * 1000)
        if Vmv % 5 == 0:
            out.append((Vmv, values[i]))
    return out


print("\n== equilibrium bell xi(1-xi)/w [dotted reference, direction-invariant, units 1/V] ==")
bell = [(round(V * 1000), xi_eq(V) * (1 - xi_eq(V)) / w) for V in Vgrid]  # units 1/V, x-axis in mV
bell_sub = [(Vmv, y) for Vmv, y in bell if Vmv % 5 == 0 and abs(Vmv) <= 100]
print(" ".join(f"({v},{y:.4f})" for v, y in bell_sub))

print("\n== discharge peak shape (V increasing = progress) [units 1/V] ==")
dis_sub = subsample(peak_dis)
print(" ".join(f"({v},{y:.4f})" for v, y in dis_sub))

print("\n== charge peak shape (V decreasing = progress, grid-reversed filter) [units 1/V] ==")
chg_sub = subsample(peak_chg)
print(" ".join(f"({v},{y:.4f})" for v, y in chg_sub))
