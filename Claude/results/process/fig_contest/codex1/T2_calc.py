from math import exp

def ux(U):
    return (0.220-U)/(0.220-0.075)*6.4

def fmt(points):
    return ' '.join(f'({x:.4f},{y:.4f})' for x, y in points)

for U, name in [(0.210,'4--3'), (0.140,'3--2L'), (0.120,'2L--2'), (0.085,'2--1')]:
    x0 = ux(U)
    pts = [(x0+dx, 0.52*exp(-((dx/0.13)**2))) for dx in [-0.24,-0.16,-0.08,0,0.08,0.16,0.24]]
    print(name, 'U=', f'{U:.3f}', 'x=', f'{x0:.4f}', fmt(pts))
