"""T5 fig:flux -- coordinate generator.

Forward flux r+(1-xi) and reverse flux r-*xi (eq:db / stationary-point
argument, l.1230-1239). Three affinity cases are shown together (a real
curve FAMILY, not just the existing single A>0 vs A=0 pair), all under a
common total-rate normalization r+ + r- = 3 (a bookkeeping choice for a
comparable overlay, disclosed in the caption -- it does NOT claim k_j is
independent of A in the real model).

r+/r- = exp(A/RT) is the detailed-balance ratio (eq:db); the three cases
below are ratio = 1 (A=0), 2 (matches the existing figure exactly,
A = RT ln2), 4 (a new, stronger-affinity overlay, A = RT ln4).
"""

import math

BUDGET = 3.0
cases = [1.0, 2.0, 4.0]

print("ratio=r+/r-   r+     r-     xi_eq=r+/(r++r-)   height=r-*xi_eq   A/RT=ln(ratio)")
for ratio in cases:
    r_minus = BUDGET / (1 + ratio)
    r_plus = BUDGET - r_minus
    xi_eq = r_plus / (r_plus + r_minus)
    height = r_minus * xi_eq
    A_over_RT = math.log(ratio)
    print(f"{ratio:5.1f}        {r_plus:.4f} {r_minus:.4f}   {xi_eq:.4f}              {height:.4f}            {A_over_RT:.4f}")
    # cross-check against the closed form xi_eq = 1/(1+exp(-A/RT)) (eq:logisticsolve)
    xi_from_logistic = 1.0 / (1.0 + math.exp(-A_over_RT))
    assert abs(xi_eq - xi_from_logistic) < 1e-12, "does not match eq:logisticsolve closed form"
    print(f"             [ok] matches eq:logisticsolve xi_eq=1/(1+exp(-A/RT)) = {xi_from_logistic:.4f}")

print("\nline endpoints for TikZ (straight lines, 2 points each suffice):")
for ratio in cases:
    r_minus = BUDGET / (1 + ratio)
    r_plus = BUDGET - r_minus
    print(f"ratio={ratio:.0f}: forward (0,{r_plus:.4f})--(1,0)   reverse (0,0)--(1,{r_minus:.4f})")
