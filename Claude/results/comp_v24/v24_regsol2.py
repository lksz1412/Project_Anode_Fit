# -*- coding: utf-8 -*-
"""v1.0.24 §6 실검증 — near-delta 헤드라인(정칙용액 Ω>2RT + Maxwell ⊗ kinetic) vs 로지스틱 MSMR.
문헌(Yao-Viswanathan 2024·Levi-Aurbach 1999): 로지스틱 ξ_j=이상(g=0) Frumkin. Ω 복원+Ω>2RT 서
공통접선(Maxwell)=진짜 miscibility gap(delta)=near-delta. 실피크=평형(delta)⊗kinetic 폭.
이전 실패(regsol_proto R²=0.79)=단일상(Ω<2RT·Maxwell 없음). 여기선 Ω>2RT+Maxwell 정정판.
※문건·코드 무수정 — 흑연 실 dQ/dV 로 두 모델 피팅·R² 비교(방법 검증만).

핵심 물리:
  정칙용액 U(x)=U0 − (RT/F)ln(x/(1−x)) − (Ω/F)(1−2x). Ω>2RT ⇒ dU/dx>0 구간(vdW loop).
  대칭 Maxwell: plateau=U0, 공존 x_α<½<x_β=1−x_α, ln(x_α/(1−x_α))+(Ω/RT)(1−2x_α)=0.
  평형 dQ/dV = Q·|dx/dV|: gap 내 delta(무게 Q(x_β−x_α)), 밖 solid-solution 가지(유한).
  kinetic 합성 = sech² 커널(=로지스틱 broadening족) 폭 δ 로 KDE 컨볼브.
로지스틱 MSMR 피크 ξ(1−ξ)/w = ¼·sech²(z/2)/w = 정확히 δ=w 인 delta⊗sech²(순수코어, 꼬리無).
→ 차이는 solid-solution 가지(어깨). 실 near-delta 피크가 코어+어깨면 정칙용액 우세.
"""
import numpy as np, pandas as pd, importlib.util, sys, json, warnings; warnings.filterwarnings("ignore")
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
plt.rcParams['font.family']='NanumGothic'; plt.rcParams['axes.unicode_minus']=False
from scipy.optimize import curve_fit, brentq
sys.path.insert(0,"/home/user/Project_Anode_Fit/Claude/results/comp_v24"); import bdd_smoothing as bdd
SC="/tmp/claude-0/-home-user-Project-Anode-Fit/e8d4cdbc-60e6-548e-b742-1446b8f7a8bd/scratchpad/zenodo_gr"
OUT="/home/user/Project_Anode_Fit/Claude/results/comp_v24"
R,F,T=8.314,96485.0,298.15; RTF=R*T/F   # ≈0.0257 V
_trapz=getattr(np,'trapezoid',getattr(np,'trapz',None))

# ---- 실 흑연 dQ/dV 추출(BDD) ----
def dqdv(cell):
    d=pd.read_parquet(f"{SC}/{cell}"); I=d['Current / A'].to_numpy(); V=d['Voltage / V'].to_numpy(); Q=d['Cumulative Capacity / Ah'].to_numpy()*1000
    idx=np.where((np.abs(I)>1e-9)&(I>0))[0]; seg=max(np.split(idx,np.where(np.diff(idx)>1)[0]+1),key=len)
    gx,gy=bdd.dqdv_grid_bdd(V[seg],Q[seg]-Q[seg][0],dV=0.0005); m=(gx>=0.06)&(gx<=0.25); return gx[m],gy[m]
Vx,Dx=dqdv("gr_pocv_4ccc47.parquet")

# ---- 로지스틱 MSMR(기준) ----
def logi_peak(V,U,w,Q):
    z=(V-U)/w; s=np.where(z>=0,1/(1+np.exp(-z)),np.exp(z)/(1+np.exp(z))); return Q*s*(1-s)/w
NT=4; Useed=[0.211,0.140,0.120,0.085]
def logi4(V,*p):
    out=np.full_like(V,p[-1])
    for j in range(NT): out=out+logi_peak(V,p[3*j],p[3*j+1],p[3*j+2])
    return out

# ---- 정칙용액 Ω>2RT + Maxwell ⊗ sech²(δ) ----
XG=np.linspace(1e-3,1-1e-3,600)   # x 격자(고정)
def binodal_xa(Om):  # ln(x/(1−x))+(Ω/RT)(1−2x)=0, x∈(1e-4,0.5)
    a=Om/(R*T)
    f=lambda x: np.log(x/(1-x))+a*(1-2*x)
    if a<=2.0: return 0.5   # Ω≤2RT: gap 없음(경계)
    try: return brentq(f,1e-6,0.5-1e-9)
    except Exception: return 0.5
def sech2(v,d):  # ∫=1 커널, FWHM≈3.53δ
    z=v/(2*d); c=1/np.cosh(np.clip(z,-350,350)); return c*c/(4*d)
def reg_peak(V,U0,Om,Q,d):
    xa=binodal_xa(Om);
    # 각 x → 평형 V_i: gap 내(xa<x<1−xa) → U0, 밖 → 단일상 가지
    xg=XG; Vi=np.where((xg>xa)&(xg<1-xa), U0, U0-RTF*np.log(xg/(1-xg))-(Om/F)*(1-2*xg))
    wi=Q*(xg[1]-xg[0])                       # 각 x 표본 무게 = Q·Δx
    # KDE: dQ/dV(V)=Σ_i wi·sech²(V−Vi; δ)
    Vm=np.asarray(V)[:,None]; return (wi*sech2(Vm-Vi[None,:],d)).sum(axis=1)
def reg4(V,*p):
    out=np.full_like(np.asarray(V,float),p[-1])
    for j in range(NT): out=out+reg_peak(V,p[4*j],p[4*j+1],p[4*j+2],p[4*j+3])
    return out

def r2(y,yh): return 1-np.sum((y-yh)**2)/np.sum((y-y.mean())**2)
area=float(_trapz(Dx,Vx))

# ---- (A) 로지스틱 피팅 ----
p0=[]; lo=[]; hi=[]
for j in range(NT): p0+=[Useed[j],0.004,0.15*area]; lo+=[Useed[j]-0.03,0.0006,1e-7]; hi+=[Useed[j]+0.03,0.05,10*area]
p0+=[0.05]; lo+=[0]; hi+=[max(Dx)]
pL,_=curve_fit(logi4,Vx,Dx,p0=p0,bounds=(lo,hi),maxfev=200000); r2L=r2(Dx,logi4(Vx,*pL))
wL=[pL[3*j+1]*1000 for j in range(NT)]

# ---- (B) 정칙용액 Ω>2RT+Maxwell 피팅 ----
p0=[]; lo=[]; hi=[]
for j in range(NT): p0+=[Useed[j],2.5*R*T,0.15*area,0.0016]; lo+=[Useed[j]-0.03,2.02*R*T,1e-7,0.0004]; hi+=[Useed[j]+0.03,8*R*T,10*area,0.02]
p0+=[0.05]; lo+=[0]; hi+=[max(Dx)]
pR,_=curve_fit(reg4,Vx,Dx,p0=p0,bounds=(lo,hi),maxfev=60000); r2R=r2(Dx,reg4(Vx,*pR))
OmR=[pR[4*j+1]/(R*T) for j in range(NT)]; dR=[pR[4*j+3]*1000 for j in range(NT)]; xaR=[binodal_xa(pR[4*j+1]) for j in range(NT)]

print("=== 흑연 dQ/dV: 로지스틱 vs 정칙용액(Ω>2RT+Maxwell⊗kinetic) ===")
print(f"(A) 로지스틱 MSMR    R²={r2L:.4f}  w_j(mV)={[round(x,2) for x in wL]}")
print(f"(B) 정칙용액+Maxwell R²={r2R:.4f}  Ω_j/RT={[round(x,2) for x in OmR]}  δ_j(mV)={[round(x,2) for x in dR]}")
print(f"    공존 x_α(gap 폭 1−2x_α)={[round(x,3) for x in xaR]}  (>2RT ⇒ 두-상)")
print(f"    ΔR²={r2R-r2L:+.4f} → {'정칙용액 우세(near-delta 개선)' if r2R>r2L+0.002 else '동등(로지스틱=커널 코어로 충분)' if abs(r2R-r2L)<=0.002 else '로지스틱 우세'}")

fig,ax=plt.subplots(1,2,figsize=(14,5.2))
ax[0].plot(Vx,Dx,'k',lw=1.6,label='실측(BDD)',alpha=.8)
ax[0].plot(Vx,logi4(Vx,*pL),'--',color='tab:blue',lw=1.3,label=f'로지스틱 MSMR R²={r2L:.3f}')
ax[0].plot(Vx,reg4(Vx,*pR),'-',color='tab:red',lw=1.3,label=f'정칙용액+Maxwell R²={r2R:.3f}')
ax[0].set_xlabel('V'); ax[0].set_ylabel('dQ/dV'); ax[0].set_title('흑연 두-상 피크: near-delta 재현\n로지스틱 vs 정칙용액(Ω>2RT+Maxwell⊗kinetic)'); ax[0].legend(fontsize=8); ax[0].grid(alpha=.3)
# 잔차
ax[1].plot(Vx,Dx-logi4(Vx,*pL),'--',color='tab:blue',lw=1,label='로지스틱 잔차')
ax[1].plot(Vx,Dx-reg4(Vx,*pR),'-',color='tab:red',lw=1,label='정칙용액 잔차')
ax[1].axhline(0,color='k',lw=.5); ax[1].set_xlabel('V'); ax[1].set_ylabel('잔차'); ax[1].set_title('잔차 비교(near-delta 코어서 로지스틱 결손?)'); ax[1].legend(fontsize=8); ax[1].grid(alpha=.3)
fig.tight_layout(); fig.savefig(f"{OUT}/regsol2.png",dpi=120); print("saved regsol2.png")
json.dump({"r2_logistic":r2L,"w_logistic_mV":wL,"r2_regsol":r2R,"Omega_over_RT":OmR,"delta_mV":dR,"xa":xaR,"dR2":r2R-r2L},
          open(f"{OUT}/regsol2_result.json","w"),indent=1)
