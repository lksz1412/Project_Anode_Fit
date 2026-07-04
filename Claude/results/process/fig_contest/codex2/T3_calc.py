import math


def veq_scaled(xi: float, omega_over_rt: float = 4.0) -> float:
    return math.log(xi / (1.0 - xi)) + omega_over_rt * (1.0 - 2.0 * xi)


root = math.sqrt(1.0 - 2.0 / 4.0)
spinodal_low = (1.0 - root) / 2.0
spinodal_high = (1.0 + root) / 2.0
xis = [0.02, 0.04, 0.06, 0.08, 0.10, spinodal_low, 0.20, 0.30, 0.40,
       0.50, 0.60, 0.70, 0.80, spinodal_high, 0.90, 0.92, 0.94, 0.96, 0.98]
pts = [(x, veq_scaled(x)) for x in xis]

print(f"xi_s_minus={spinodal_low:.8f}, y={veq_scaled(spinodal_low):.8f}")
print(f"xi_s_plus ={spinodal_high:.8f}, y={veq_scaled(spinodal_high):.8f}")
print(f"scaled gap={veq_scaled(spinodal_low)-veq_scaled(spinodal_high):.8f}")
print("curve:", " ".join(f"({x:.4f},{y:.4f})" for x, y in pts))
