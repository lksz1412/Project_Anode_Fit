# -*- coding: utf-8 -*-
import math
R=8.314462618; F=96485.33212
stages=[("4→3",0.210,-11700,29.0,0.10,0.020),("3→2L",0.140,-13500,0.0,0.12,0.016),
        ("2L→2",0.120,-13100,-5.0,0.25,0.014),("2→1",0.085,-13000,-16.0,0.50,0.012)]
def lg(z):
    if z>=0: return 1.0/(1.0+math.exp(-z))
    e=math.exp(z); return e/(1.0+e)

def coords(xs,ys,nd=4,ndy=4):
    return " ".join(f"({x:.{nd}f},{y:.{ndy}f})" for x,y in zip(xs,ys))

# ---------- CAND-1 composite ----------
Cbg=0.6
def peak_j(V,j):
    n,U,dH,dS,Q,w=stages[j]; xi=lg((V-U)/w); return Q*xi*(1-xi)/w
def total(V): return Cbg+sum(peak_j(V,j) for j in range(4))
Vg=[0.030+(0.260-0.030)*i/57.0 for i in range(58)]
print("### CAND-1 background (const 0.6): draw line (0.030,0.6)-(0.260,0.6)")
print("### CAND-1 TOTAL:")
print(coords(Vg,[total(V) for V in Vg]))
for j in range(4):
    n,U,dH,dS,Q,w=stages[j]
    lo=max(0.030,U-5*w); hi=min(0.260,U+5*w)
    Vj=[lo+(hi-lo)*i/29.0 for i in range(30)]
    print(f"### CAND-1 peak {n} (thin, +bg baseline):")
    print(coords(Vj,[Cbg+peak_j(V,j) for V in Vj]))

# ---------- CAND-2 reversible heat ----------
Qtot=sum(s[4] for s in stages); T0=298.15
def Uj(dH,dS,T): return (-dH+T*dS)/F
def sx(U,T):
    w=R*T/F; return sum(Q*lg((U-Uj(dH,dS,T))/w) for _,_,dH,dS,Q,_ in stages)
def solve(xb,T):
    t=Qtot*xb; lo,hi=-0.2,0.6
    for _ in range(200):
        m=0.5*(lo+hi)
        if sx(m,T)<t: lo=m
        else: hi=m
    return 0.5*(lo+hi)
def dUdT(xb,T,h=3.0): return (solve(xb,T+h)-solve(xb,T-h))/(2*h)
xs=[0.05+(0.95-0.05)*i/44.0 for i in range(45)]
qr=[-T0*dUdT(xb,T0)*1000.0 for xb in xs]
print("\n### CAND-2 q_rev/I(x_bar) [mV] smooth:")
print(coords(xs,qr,3,3))
print("### CAND-2 exact table markers (x_bar, qrev mV):")
print("  ",[(round(xb,2),round(-T0*dUdT(xb,T0)*1000,1)) for xb in [0.10,0.25,0.50,0.75,0.90]])
print("### CAND-2 zero crossing x_bar:")
for i in range(len(xs)-1):
    if qr[i]>0 and qr[i+1]<0:
        xc=xs[i]+(xs[i+1]-xs[i])*(0-qr[i])/(qr[i+1]-qr[i]); print(f"   {xc:.4f}")

# ---------- CAND-3 single peak anatomy (generic, x in units of w) ----------
# y = xi(1-xi), xi=logistic(x); peak 0.25 at x=0. FWHM at y=0.125 -> x=+-1.7627 (=1.7627w); FWHM=3.5255w
xg=[-5+10*i/79.0 for i in range(80)]
yg=[ (lambda xi: xi*(1-xi))(lg(x)) for x in xg]
print("\n### CAND-3 bell y=xi(1-xi), x in units of w  (peak 0.25):")
print(coords(xg,yg,3,4))
xh=2*math.log(1+math.sqrt(2))  # half-width where xi(1-xi)=1/8
print(f"### CAND-3 half-max half-width = {xh:.4f} w ; FWHM=3.5255 w ; height=1/4")

# ---------- CAND-4 U_j(T) ----------
print("\n### CAND-4 U_j(T) endpoints [T in K, U in mV], T=268..328:")
for n,U0,dH,dS,Q,wf in stages:
    print(f"  {n}: ({268},{Uj(dH,dS,268)*1000:.2f}) ({328},{Uj(dH,dS,328)*1000:.2f})  slope={dS/F*1000:+.4f} mV/K")
