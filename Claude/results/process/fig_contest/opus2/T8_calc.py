#!/usr/bin/env python3
# T8 fig:widthbudget  --  two-phase broadening width budget (eq:widthbudget), 4 numeric stages:
#   (0) equilibrium delta at the Maxwell (plateau) potential.
#   (ii) intrinsic logistic-derivative bell g0(x) = xi(1-xi)/w = (1/4) sech^2(x/2),  scale w=1.
#        variance = pi^2 w^2 / 3 ; sigma_int = pi w / sqrt3 = 1.8138 w ; FWHM = 3.5255 w.
#   (ii)⊗(iii) convolve g0 with a Gaussian of sigma_eta = 1.25 sigma_int (ensemble eta spread);
#        variances add: sigma_sym = sqrt(1+1.25^2) sigma_int = 1.6008 sigma_int.  (GENUINE conv.)
#   (i) +tail: convolve the broadened bell with a one-sided (causal) exponential kernel,
#        length L_V = 1.5 w  ->  skew + mean shift.  (GENUINE conv.)
import math

w = 1.0
sig_int = math.pi*w/math.sqrt(3.0)          # 1.81380 w
sig_eta = 1.25*sig_int
sig_sym = math.sqrt(sig_int**2 + sig_eta**2)
kFW = 2.0*math.log(3.0+2.0*math.sqrt(2.0))
print(f"# sigma_int = pi w/sqrt3      = {sig_int:.4f} w")
print(f"# sigma_eta = 1.25 sigma_int  = {sig_eta:.4f} w")
print(f"# sigma_sym = sqrt(1+1.25^2) sigma_int = {sig_sym:.4f} w  (= {sig_sym/sig_int:.4f} sigma_int)")
print(f"# intrinsic FWHM = {kFW:.4f} w ;  L_V(tail) = 1.5 w")

# ---- numeric grid & convolutions ----
dx = 0.02
xs = [ -10.0 + i*dx for i in range(int(20.0/dx)+1) ]      # -10..+10
def g0(x):                                                # intrinsic bell, area 1
    return 0.25/ (math.cosh(x/2.0)**2)                    # = xi(1-xi), integral over x = 1

# (ii) intrinsic
bell = [g0(x) for x in xs]

# (iii) Gaussian kernel, sigma_eta
def gauss(x,s): return math.exp(-0.5*(x/s)**2)/(s*math.sqrt(2.0*math.pi))
klen = int(6*sig_eta/dx)
gk = [gauss(j*dx, sig_eta) for j in range(-klen,klen+1)]
gksum = sum(gk)*dx
def convsym(f,k,koff):
    n=len(f); out=[0.0]*n
    for i in range(n):
        acc=0.0
        for j in range(len(k)):
            m=i+(j-koff)
            if 0<=m<n: acc+=f[m]*k[j]
        out[i]=acc*dx
    return out
broad = convsym(bell, gk, klen)

# (i) one-sided causal exponential kernel, length L_V=1.5, tail toward +x (higher V, discharge)
LV=1.5
elen=int(9*LV/dx)
ek=[ (math.exp(-(j*dx)/LV)/LV if j>=0 else 0.0) for j in range(0,elen+1) ]  # j>=0 only
def convcausal(f,k):
    n=len(f); out=[0.0]*n
    for i in range(n):
        acc=0.0
        for j in range(len(k)):
            m=i-j
            if 0<=m<n: acc+=f[m]*k[j]
        out[i]=acc*dx
    return out
tailed = convcausal(broad, ek)

def peakinfo(name,f):
    im=max(range(len(xs)),key=lambda i:f[i])
    # FWHM
    half=f[im]/2.0
    l=next(xs[i] for i in range(im,-1,-1) if f[i]<=half)
    r=next(xs[i] for i in range(im,len(xs)) if f[i]<=half)
    print(f"# {name}: peak={f[im]:.4f} at x={xs[im]:.2f}  FWHM~{r-l:.3f} w")
peakinfo("(ii) intrinsic", bell)
peakinfo("(ii)x(iii) broadened", broad)
peakinfo("(i) tailed", tailed)

def emit(name,f,step=25):
    pts=[(xs[i],f[i]) for i in range(0,len(xs),step)]
    print(f"% {name}:")
    print(" ".join(f"({x:.2f},{y:.4f})" for x,y in pts))
print("\n# curves sampled every %.2f w:"%(dx*25))
emit("intrinsic bell", bell)
emit("broadened (ii x iii)", broad)
emit("tailed (+ i)", tailed)
print(f"# delta arrow height (match intrinsic peak): {max(bell):.4f}")
