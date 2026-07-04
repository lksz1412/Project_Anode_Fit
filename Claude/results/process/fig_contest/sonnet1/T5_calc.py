# T5 fig:flux — stopping-point construction, forward/reverse flux intersection.
# eq:bv/eq:db: r+/r- = exp(A/RT) (detailed balance, chi-independent).
# eq:logisticsolve: stopping point r+(1-xi_eq) = r-*xi_eq  =>  xi_eq = r+/(r+ + r-).
# Fix r- = 1 (arbitrary common scale) and vary r+ = exp(A/RT) for three affinities
# A/RT = 0, ln2, ln4  ->  r+ = 1, 2, 4  ->  xi_eq = 1/2, 2/3, 4/5.
import math

r_minus = 1.0
cases = [
    ("A=0",       0.0),
    ("A=RT ln2",  math.log(2.0)),
    ("A=RT ln4",  math.log(4.0)),
]

results = []
for label, A_over_RT in cases:
    r_plus = r_minus * math.exp(A_over_RT)
    xi_eq = r_plus / (r_plus + r_minus)
    # forward line: from (0, r_plus) to (1, 0)  [r+ (1-xi)]
    # reverse line: from (0, 0) to (1, r_minus) [r- xi] -- same for all cases (r_minus fixed)
    results.append((label, round(r_plus, 4), round(xi_eq, 4)))

if __name__ == "__main__":
    for label, r_plus, xi_eq in results:
        print(f"{label}: r+ = {r_plus}, r- = {r_minus}, xi_eq = r+/(r+ + r-) = {xi_eq}")
    print()
    print("forward line endpoints (0,r+)-(1,0) for r+ in", [r for _, r, _ in results])
    print("reverse line endpoints (0,0)-(1,1) [r-=1, fixed]")
    print("intersection markers (xi_eq, r_minus*xi_eq):",
          [(xi, round(r_minus * xi, 4)) for _, _, xi in results])
