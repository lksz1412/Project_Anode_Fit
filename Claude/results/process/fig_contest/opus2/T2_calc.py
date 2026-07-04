#!/usr/bin/env python3
# T2 fig:staging  --  graphite staging gallery fill (4->3->2L->2->1) tied by droplines to the
# transition potentials on a bottom axis, with a per-transition equilibrium dQ/dV bell glyph.
# Transition initial values are the literature anchors of Table tab:staging:
#   4->3 : U=0.210 V, w=0.020 V, Q=0.10   (Dahn)
#   3->2L: U=0.140 V, w=0.016 V, Q=0.12   (Ohzuku, batched)
#   2L->2: U=0.120 V, w=0.014 V, Q=0.25   (Ohzuku, LiC12)
#   2->1 : U=0.085 V, w=0.012 V, Q=0.50   (Dahn,  LiC6)
# Bell glyph = normalized logistic-derivative  g(z)=sigma(z)(1-sigma(z))/0.25, z=(V-U)/w,
# so the SHAPE is one curve; only the V-width (∝ w) differs between transitions.
# peak height 1/(4w) and area∝Q printed for reference (glyphs drawn equal-height for legibility).
import math

trans = [("4->3",0.210,0.020,0.10),
         ("3->2L",0.140,0.016,0.12),
         ("2L->2",0.120,0.014,0.25),
         ("2->1",0.085,0.012,0.50)]

def sig(z): return 1.0/(1.0+math.exp(-z))
print("# transition : U[V]  w[V]  Q   true-peak 1/(4w)[/V]  area~Q  FWHM=3.5255w[mV]")
for name,U,w,Q in trans:
    print(f"  {name:6s}: {U:.3f} {w:.3f} {Q:.2f}   {1/(4*w):7.2f}          {Q:.2f}    {3.5255*w*1e3:.1f}")

# ---- normalized bell shape (z-domain, peak 1) sampled once ----
zs=[-3.0,-2.5,-2.0,-1.5,-1.317,-1.0,-0.5,0.0,0.5,1.0,1.317,1.5,2.0,2.5,3.0]
print("\n% normalized bell g(z)=sigma(z)(1-sigma(z))/0.25  (peak 1; z where g=0.5 at z=+-1.317):")
print(" ".join(f"({z:.3f},{sig(z)*(1-sig(z))/0.25:.4f})" for z in zs))
# half-max z: solve sigma(z)(1-sigma(z))=0.125 -> z = ln[(3+2 sqrt2)] ... check
zhalf=math.log(3+2*math.sqrt(2))/1.0   # 1.7627? verify numerically
# numeric half-max
lo,hi=0.0,4.0
for _ in range(60):
    mid=0.5*(lo+hi)
    if sig(mid)*(1-sig(mid))/0.25>0.5: lo=mid
    else: hi=mid
print(f"# half-max at z=+-{0.5*(lo+hi):.4f}  (FWHM in z = {2*0.5*(lo+hi):.4f} = 3.5255)")
