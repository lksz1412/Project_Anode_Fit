# -*- coding: utf-8 -*-
# FO3 좌표 생성기 — 모델 식 그대로의 수치 평가(하드코딩용).
import math

R = 8.314462618
F = 96485.33212

# --- Chapter 1 tab:staging 초기값 (fig:staging 과 동일) ---
# stage:  U[V],  dH[J/mol], dS[J/molK], Q[Q_cell], w_fallback[V]
stages = [
    ("4to3",   0.210, -11700,  29.0, 0.10, 0.020),
    ("3to2L",  0.140, -13500,   0.0, 0.12, 0.016),
    ("2Lto2",  0.120, -13100,  -5.0, 0.25, 0.014),
    ("2to1",   0.085, -13000, -16.0, 0.50, 0.012),
]

def logistic(z):
    if z >= 0:
        return 1.0/(1.0+math.exp(-z))
    e = math.exp(z); return e/(1.0+e)

# =====================================================================
# CAND-FO3-1 : 합성 관측 dQ/dV = C_bg + sum_j Q_j xi(1-xi)/w  (방전 sigma_d=+1)
#   fig:staging 와 동일 값(U_fallback-w Q). 배경 C_bg 상수.
# =====================================================================
def dqdv_components(V):
    """returns (bg, [peak_j...], total)"""
    C_bg = 0.6  # Q_cell/V, 완만한 배경 pedestal (모식 배경; 캡션서 예시 명시)
    peaks=[]
    for name,U,dH,dS,Q,w in stages:
        z=(V-U)/w  # sigma_d=+1
        xi=logistic(z)
        peaks.append(Q*xi*(1.0-xi)/w)
    return C_bg, peaks, C_bg+sum(peaks)

print("=== CAND-1 composite dQ/dV (peak heights check Q/4w) ===")
for name,U,dH,dS,Q,w in stages:
    print(f"  {name}: U={U} w={w} Q={Q} height Q/4w={Q/(4*w):.3f}")
# grid over V in [0.03, 0.26], dense
V1=[]
for i in range(0,231):
    V=0.030+ (0.260-0.030)*i/230.0
    V1.append(V)
comp=[dqdv_components(V) for V in V1]
# print a downsampled coordinate list for the TOTAL (every 5th) + each peak
def fmt(v,y): return f"({v:.4f},{y:.4f})"
# We'll emit later. Peak of total:
tot=[c[2] for c in comp]
imax=max(range(len(V1)),key=lambda i:tot[i]); print(f"  total peak {tot[imax]:.3f} at V={V1[imax]:.4f}")

# =====================================================================
# CAND-FO3-2 : 가역 발열 부호 교대  q_rev/I(x_bar) = -T dU_oc/dT
#   음함수 sum_j Q_j xi_eq,j(U_oc,T) = Q_tot * x_bar  풀어 U_oc, 중앙차분.
#   n_j=1 -> w=RT/F.  Ch2 form s=+1.
# =====================================================================
Qtot=sum(s[4] for s in stages)  # 0.97
def Uj_of_T(dH,dS,T): return (-dH + T*dS)/F
def sum_xi(U_oc,T):
    s=0.0
    w=R*T/F
    for name,U0,dH,dS,Q,wf in stages:
        Uj=Uj_of_T(dH,dS,T)
        s+=Q*logistic((U_oc-Uj)/w)
    return s
def solve_Uoc(xbar,T):
    target=Qtot*xbar
    lo,hi=-0.2,0.6
    for _ in range(200):
        mid=0.5*(lo+hi)
        if sum_xi(mid,T)<target: lo=mid
        else: hi=mid
    return 0.5*(lo+hi)
def dUoc_dT(xbar,T,h=3.0):
    return (solve_Uoc(xbar,T+h)-solve_Uoc(xbar,T-h))/(2*h)

T0=298.15
print("\n=== CAND-2 reversible heat: verify vs tab:qrev ===")
print(" xbar   U_oc[mV]  dU/dT[mV/K]  dS[J/molK]  qrev/I[mV]")
check={0.10:(43.5,-0.307,-29.6,+91.5),0.25:(74.4,-0.204,-19.7,+60.8),
       0.50:(109.0,-0.089,-8.6,+26.6),0.75:(148.8,+0.044,+4.3,-13.2),
       0.90:(195.2,+0.218,+21.0,-64.9)}
for xb in [0.10,0.25,0.50,0.75,0.90]:
    U=solve_Uoc(xb,T0); d=dUoc_dT(xb,T0); dS=F*d; qrev=-T0*d
    ref=check[xb]
    print(f" {xb:.2f}  {U*1000:7.1f}   {d*1000:+7.3f}    {dS:+6.1f}   {qrev*1000:+7.1f}   (tab: {ref[0]},{ref[1]},{ref[2]},{ref[3]})")

# smooth curve for the figure
print("\n=== CAND-2 smooth q_rev/I(x_bar) coordinates ===")
xs=[]
for i in range(0,49):
    xb=0.05+(0.95-0.05)*i/48.0
    xs.append(xb)
curve=[]
for xb in xs:
    d=dUoc_dT(xb,T0); qrev=-T0*d*1000.0  # mV
    curve.append((xb,qrev))
# zero crossing
for i in range(len(curve)-1):
    if curve[i][1]>0 and curve[i+1][1]<0:
        x0,y0=curve[i]; x1,y1=curve[i+1]
        xc=x0+(x1-x0)*(0-y0)/(y1-y0)
        print(f"  zero-crossing (발열/흡열 경계) at x_bar={xc:.3f}")

# also dS(x_bar) for secondary axis if needed
# store outputs to file for the tex writer
import json
out={
 "cand1_V":V1,"cand1_bg":[c[0] for c in comp],
 "cand1_peaks":[[c[1][j] for c in comp] for j in range(4)],
 "cand1_total":tot,
 "cand2_xs":xs,"cand2_qrev":[c[1] for c in curve],
 "cand2_pts":[(k,)+v for k,v in check.items()],
}
with open("coords.json","w") as f: json.dump(out,f)
print("\nwrote coords.json")

# =====================================================================
# CAND-FO3-4 : U_j(T) 온도 의존 (기울기 dS/F)
# =====================================================================
print("\n=== CAND-4 U_j(T) lines (T=270..330) ===")
for name,U0,dH,dS,Q,wf in stages:
    slope=dS/F*1000.0  # mV/K
    U270=Uj_of_T(dH,dS,270)*1000; U330=Uj_of_T(dH,dS,330)*1000; U298=Uj_of_T(dH,dS,298.15)*1000
    print(f"  {name}: slope dS/F={slope:+.4f} mV/K  U(270)={U270:.2f} U(298)={U298:.2f} U(330)={U330:.2f} mV")
