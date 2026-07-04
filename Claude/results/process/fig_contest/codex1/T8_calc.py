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

def causal_tail(xs, L=1.50, scale=1.60):
    ys = []
    for x in xs:
        u = -10.0
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

xs = [-6,-5,-4,-3,-2,-1,-0.5,0,0.5,1,1.5,2,2.5,3,4,5,6,7,8,9,10]
print('intrinsic', fmt([(x, bell(x,1.0)) for x in xs]))
print('symmetric_1p6w', fmt([(x, bell(x,1.60)) for x in xs]))
print('tail_L_1p5w', fmt([(x, y) for x, y in zip(xs, causal_tail(xs))]))
print('sigma_ratio', sqrt(1+1.25**2))
