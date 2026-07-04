# -*- coding: utf-8 -*-
# T5 fig:flux (opus3) — stationary point as forward/reverse flux crossing, family over affinity A.
# Forward flux  F(xi) = r+ (1-xi)   (decreasing line, intercept r+ at xi=0)
# Reverse flux  R(xi) = r-  xi       (increasing line, fixed r-=1)
# Stationary point (eq:logisticsolve): r+(1-xi_eq)=r- xi_eq  ->  xi_eq = r+/(r+ + r-).
# detailed balance (eq:db): r+/r- = exp(A/RT).  Fix r-=1; vary r+ in {0.5,1,2}.
import numpy as np

rminus = 1.0
cases = [("A<0", 0.5), ("A=0", 1.0), ("A>0", 2.0)]

for name, rplus in cases:
    xi_eq = rplus / (rplus + rminus)
    flux = rplus * (1.0 - xi_eq)
    A_over_RT = np.log(rplus / rminus)
    print(f"{name}:  r+={rplus:.3f}  r-={rminus:.3f}  A/RT=ln(r+/r-)={A_over_RT:+.4f}")
    print(f"      xi_eq = r+/(r++r-) = {xi_eq:.4f}   flux at crossing = {flux:.4f}")
    print(f"      forward line: (0,{rplus:.3f}) -> (1,0)")
    print(f"      crossing point: ({xi_eq:.4f},{flux:.4f})")
    print()

print("reverse line (fixed): (0,0) -> (1,1)")
print("cross-check logistic identity xi_eq = 1/(1+exp(-A/RT)):")
for name, rplus in cases:
    A_over_RT = np.log(rplus / rminus)
    print(f"  {name}: 1/(1+e^-A/RT) = {1/(1+np.exp(-A_over_RT)):.4f}  == r+/(r++r-) = {rplus/(rplus+rminus):.4f}")
