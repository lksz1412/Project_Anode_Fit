"""T6 fig:logistic -- coordinate generator.

The existing figure plots xi_eq and its derivative vs the DIMENSIONLESS
z = sigma_d(V-U)/w (eq:xieq/eq:belliden) -- but z already absorbs the
T-dependence of w, so three temperatures plotted vs z are IDENTICAL
curves (z-space can't show temperature broadening at all). To actually
show 268/298/328 K as three distinguishable curves, this candidate plots
against the real voltage offset (V-U) in mV, where w = n_j R T / F
(n_j = 1) differs numerically between the three temperatures.

Two panels: (left) xi_eq(V) logistic, (right) w*-unnormalized derivative
dxi/dV = xi(1-xi)/w [1/V] -- both eq:xieq / eq:belliden evaluated at the
three real w(T) values, plus the center-slope tangent 1/(4w) at 298.15 K
(the geometric meaning of w requested by the brief).
"""

import math

R = 8.314462618
F = 96485.33212

temps = [268.0, 298.15, 328.0]
w = {T: R * T / F for T in temps}
for T in temps:
    print(f"T={T:6.2f} K  ->  w = n R T / F (n=1) = {w[T]*1000:.3f} mV")

print(f"\ncenter slope 1/(4w) at 298.15 K = {1/(4*w[298.15]):.4f} 1/V "
      f"= {1/(4*w[298.15])/1000:.6f} 1/mV")


def logistic(x_mV, w_V):
    x_V = x_mV / 1000.0
    z = x_V / w_V
    return 1.0 / (1.0 + math.exp(-z))


def bell(x_mV, w_V):
    xi = logistic(x_mV, w_V)
    return xi * (1 - xi) / w_V  # units: 1/V


xs_mV = list(range(-90, 91, 6))

print("\n== left panel: xi_eq(V-U) [mV] for the three temperatures ==")
for T in temps:
    pts = [(x, logistic(x, w[T])) for x in xs_mV]
    print(f"T={T:.2f} K:")
    print(" ".join(f"({x:.0f},{y:.4f})" for x, y in pts))

print("\n== right panel: dxi/dV [1/V] for the three temperatures ==")
for T in temps:
    pts = [(x, bell(x, w[T])) for x in xs_mV]
    ymax = max(y for _, y in pts)
    print(f"T={T:.2f} K  (peak height 1/(4w) = {1/(4*w[T]):.3f} 1/V, sampled max {ymax:.3f}):")
    print(" ".join(f"({x:.0f},{y:.4f})" for x, y in pts))

# tangent line at the center (V=U) for 298.15 K: slope = 1/(4w), passes through (0, 0.5)
slope298 = 1 / (4 * w[298.15]) / 1000.0  # per mV, since x-axis is in mV
x_tan = 25
y0, y1 = 0.5 - slope298 * x_tan, 0.5 + slope298 * x_tan
print(f"\ntangent at center, 298.15K, left panel: slope={slope298:.5f} per mV; "
      f"segment (-{x_tan},{y0:.4f})--({x_tan},{y1:.4f})")
