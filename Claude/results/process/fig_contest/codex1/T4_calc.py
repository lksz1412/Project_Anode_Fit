def base(x):
    u = (x-3)/2
    return 0.10 + 0.90*((u*u - 1)**2)

def driven(x, A=0.70):
    return base(x) - A*(x-1)/4

def fmt(points):
    return ' '.join(f'({x:.4f},{y:.4f})' for x, y in points)

xs = [i*0.25 for i in range(25)]
print('base', fmt([(x, base(x)) for x in xs]))
print('driven', fmt([(x, driven(x)) for x in xs]))
print('barriers forward reverse', driven(3)-driven(1), driven(3)-driven(5))
