from math import exp, log, sqrt

def logistic(z):
    return 1/(1+exp(-z))

def dlogistic(z):
    s = logistic(z)
    return s*(1-s)

def fmt(points):
    return ' '.join(f'({x:.4f},{y:.4f})' for x, y in points)

print('logistic', fmt([(z, 0.8*logistic(2*z)) for z in [-1.0,-0.5,0,0.5,1.0]]))
print('tail', fmt([(0.00,0.08),(0.35,0.22),(0.70,0.56),(1.05,0.62),(1.40,0.43),(1.75,0.26)]))
