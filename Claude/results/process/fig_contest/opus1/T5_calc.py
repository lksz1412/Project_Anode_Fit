# T5 fig:flux — stationary point of dxi/dt: forward flux r+ (1-xi) vs reverse flux r- xi.
# Intersection: r+(1-xi) = r- xi  =>  xi_eq = r+/(r+ + r-).   [eq:logisticsolve]
# Detailed balance: r+/r- = exp(A/RT).   [eq:db]   Overlay three affinities A.
import math

rminus = 1.0
cases = [
    ("A=0",        0.0),
    ("A=RT ln2",   math.log(2.0)),
    ("A=RT ln3",   math.log(3.0)),
]

print("Reverse flux r- xi : line (0,0)->(1,%.3f)" % rminus)
for name, ART in cases:
    rplus = rminus * math.exp(ART)     # detailed balance
    xieq = rplus / (rplus + rminus)
    yint = rminus * xieq               # reverse flux value at crossing
    print(f"{name:10s}  A/RT={ART:.4f}  r+={rplus:.4f}  "
          f"forward line (0,{rplus:.4f})->(1,0)   xi_eq={xieq:.4f}  y_cross={yint:.4f}")
