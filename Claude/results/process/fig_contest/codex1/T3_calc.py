from math import exp, log, sqrt

def logistic(z):
    return 1/(1+exp(-z))

def dlogistic(z):
    s = logistic(z)
    return s*(1-s)

def fmt(points):
    return ' '.join(f'({x:.4f},{y:.4f})' for x, y in points)

def y(xi):
    return log(xi/(1-xi)) + 4*(1-2*xi)

xs = [0.02,0.04,0.06,0.08,0.10,0.12,0.1464,0.18,0.22,0.30,0.40,0.50,0.60,0.70,0.78,0.82,0.8536,0.88,0.90,0.92,0.94,0.96,0.98]
print('curve', fmt([(x, y(x)) for x in xs]))
sm = (1-sqrt(0.5))/2
sp = (1+sqrt(0.5))/2
print('spinodal-', sm, y(sm))
print('spinodal+', sp, y(sp))
print('gap_y', y(sm)-y(sp))
