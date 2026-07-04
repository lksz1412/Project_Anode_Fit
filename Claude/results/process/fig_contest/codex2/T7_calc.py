import math


def logistic(x: float) -> float:
    return 1.0 / (1.0 + math.exp(-x))


dx = 0.1
lag_len = 0.85
rho = math.exp(-dx / lag_len)
fine = [-4.0 + i * dx for i in range(81)]
lag = []
prev = logistic(fine[0])
for x in fine:
    eq = logistic(x)
    prev = rho * prev + (1.0 - rho) * eq
    lag.append(prev)

shape = [(x, (logistic(x) - ylag) / lag_len) for x, ylag in zip(fine, lag)]
scale = 2.25 / max(y for _, y in shape)
sample = [-4.0 + 0.4 * i for i in range(21)]
lookup = {round(x, 1): y * scale for x, y in shape}

eq_curve = [(x, 2.25 * logistic(x) * (1.0 - logistic(x)) / 0.25) for x in sample]
discharge = [(x, lookup[round(x, 1)]) for x in sample]
charge = [(x, lookup[round(-x, 1)]) for x in sample]

for name, pts in [("eq", eq_curve), ("discharge", discharge), ("charge", charge)]:
    print(name + ":", " ".join(f"({x:.4f},{y:.4f})" for x, y in pts))
