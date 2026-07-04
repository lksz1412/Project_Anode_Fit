from math import exp, log, sqrt

def logistic(z):
    return 1/(1+exp(-z))

def dlogistic(z):
    s = logistic(z)
    return s*(1-s)

def fmt(points):
    return ' '.join(f'({x:.4f},{y:.4f})' for x, y in points)

R = 8.31446261815324
F = 96485.33212
V = [-90,-75,-60,-45,-30,-15,0,15,30,45,60,75,90]
for T in [268,298,328]:
    w = R*T/F*1000
    print('T', T, 'w_mV', f'{w:.4f}')
    print('logistic', fmt([(v, 2.8*logistic(v/w)) for v in V]))
    print('derivative', fmt([(v, 11.2*dlogistic(v/w)) for v in V]))
