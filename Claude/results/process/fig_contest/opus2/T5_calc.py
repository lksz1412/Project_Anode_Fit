#!/usr/bin/env python3
# T5 fig:flux  --  stationary point = intersection of forward/reverse per-site flux.
# Forward flux  F+(xi) = r+ (1-xi),  reverse flux  F-(xi) = r- xi   (eq:logisticsolve setup).
# Stationary point r+(1-xi)=r- xi  ->  xi_eq = r+/(r+ + r-) = 1/(1+e^{-A/RT})   (detailed balance eq:db).
# Overlay three affinities (fix r- = 1, so reverse line y = xi is COMMON to all cases):
#   A/RT = 0      -> r+/r- = 1  -> xi_eq = 1/2
#   A/RT = ln 2   -> r+/r- = 2  -> xi_eq = 2/3
#   A/RT = ln 4   -> r+/r- = 4  -> xi_eq = 4/5
import math

rminus = 1.0
cases = [("A=0",       0.0),
         ("A=RT ln2",  math.log(2.0)),
         ("A=2RT ln2", math.log(4.0))]

print("# reverse flux line (common): from (0,0) to (1,%.3f)" % rminus)
for name, AoRT in cases:
    rplus = rminus*math.exp(AoRT)          # r+ = r- e^{A/RT}
    xi_eq = rplus/(rplus + rminus)          # = 1/(1+e^{-A/RT})
    flux  = rminus*xi_eq                     # flux value at the crossing (on y=xi line)
    print(f"{name:10s}: A/RT={AoRT:.4f}  r+/r-={rplus/rminus:.3f}  "
          f"forward-line (0,{rplus:.3f})->(1,0)  xi_eq={xi_eq:.4f}  flux*={flux:.4f}")

# closed-form check: xi_eq = 1/(1+e^{-A/RT})
for name, AoRT in cases:
    chk = 1.0/(1.0+math.exp(-AoRT))
    print(f"# check {name}: 1/(1+e^-A/RT) = {chk:.6f}")
