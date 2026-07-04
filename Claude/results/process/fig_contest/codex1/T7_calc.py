from math import exp, log, sqrt

def logistic(z):
    return 1/(1+exp(-z))

def dlogistic(z):
    s = logistic(z)
    return s*(1-s)

def fmt(points):
    return ' '.join(f'({x:.4f},{y:.4f})' for x, y in points)

def bell(x, scale=1.0):
    return dlogistic(x/scale)/scale

def causal_tail(xs, L=1.10, scale=1.0):
    ys = []
    for x in xs:
        u = -8.0
        du = 0.035
        total = 0.0
        prev = None
        while u <= x + 1e-9:
            val = bell(u, scale)*exp(-(x-u)/L)/L
            if prev is not None:
                total += 0.5*(prev+val)*du
            prev = val
            u += du
        ys.append(total)
    return ys

xs = [-3.5,-3.0,-2.5,-2.0,-1.5,-1.0,-0.5,0,0.5,1.0,1.5,2.0,2.5,3.0,3.5]
eq_raw = [bell(x) for x in xs]
tail = causal_tail(xs)
scale = 2.25/max(eq_raw)
dis = [(x, y*scale) for x, y in zip(xs, tail)]
print('equilibrium', fmt([(x, y*scale) for x, y in zip(xs, eq_raw)]))
print('discharge', fmt(dis))
print('charge', fmt([(-x, y) for x, y in reversed(dis)]))
