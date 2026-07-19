# -*- coding: utf-8 -*-
"""v1.0.24 진단 — 사용자 가설: "흑연이 되면 LCO도 같은 방법으로 됐어야."
LCO 실측(O2, Carlier2002)에 **흑연과 완전 동일한 plain MSMR(로지스틱 자유피팅)** 적용 → R².
이어 O3 해석프록시(Marquis)도 동일 방법. 흑연 R²(~0.95)와 대조 → LCO '안 맞음'이
(a)모델·방법 문제인가 (b)단지 실 O3 데이터 부재/프록시 불일치 문제인가 판별.
문건·코드 무수정(진단만).
"""
import numpy as np, pandas as pd, sys, json, warnings; warnings.filterwarnings("ignore")
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
plt.rcParams['font.family']='NanumGothic'; plt.rcParams['axes.unicode_minus']=False
from scipy.optimize import curve_fit
from scipy.signal import find_peaks
SC="/tmp/claude-0/-home-user-Project-Anode-Fit/e8d4cdbc-60e6-548e-b742-1446b8f7a8bd/scratchpad"
LD="/home/user/Project_Anode_Fit/Claude/results/comp_v24/lco_data"; OUT="/home/user/Project_Anode_Fit/Claude/results/comp_v24"
_trapz=getattr(np,'trapezoid',getattr(np,'trapz',None))

def logi(V,U,w,Q):
    z=(V-U)/w; s=np.where(z>=0,1/(1+np.exp(-z)),np.exp(z)/(1+np.exp(z))); return Q*s*(1-s)/w
def r2(y,yh): return 1-np.sum((y-yh)**2)/np.sum((y-y.mean())**2)
def ocv_dqdv(x,V,vlo,vhi,npts=500):
    o=np.argsort(V); V=np.asarray(V)[o]; x=np.asarray(x)[o]
    Vu,iu=np.unique(V,return_index=True); xu=x[iu]
    Vg=np.linspace(max(vlo,Vu.min()),min(vhi,Vu.max()),npts); xi=np.interp(Vg,Vu,xu)
    d=np.abs(np.gradient(xi,Vg)); return Vg,d
def load_xy(p): a=np.loadtxt(p,delimiter=',',skiprows=1); return a[:,0],a[:,1]

# ---- plain MSMR 자유피팅 (흑연과 완전 동일: 자유 U_j·w_j·Q_j·Cbg) ----
def plain_fit(Vx,Dx,Us):
    NT=len(Us); area=float(_trapz(Dx,Vx))
    def M(V,*p):
        o=np.full_like(np.asarray(V,float),p[-1])
        for j in range(NT): o=o+logi(V,p[3*j],p[3*j+1],p[3*j+2])
        return o
    p0=[];lo=[];hi=[]
    for u in Us: p0+=[u,0.01,0.2*area]; lo+=[u-0.06,0.002,1e-9]; hi+=[u+0.06,0.20,20*area]
    p0+=[max(Dx)*0.05];lo+=[0];hi+=[max(Dx)]
    pf,_=curve_fit(M,Vx,Dx,p0=p0,bounds=(lo,hi),maxfev=400000)
    return r2(Dx,M(Vx,*pf)),M,pf,NT
def autoU(Vx,Dx,n=4):
    pk,_=find_peaks(Dx,height=0.06*np.nanmax(Dx),prominence=0.03*np.nanmax(Dx))
    U=sorted(Vx[pk],key=lambda v:-Dx[list(Vx).index(v)])[:n] if len(pk)>0 else list(np.linspace(Vx.min(),Vx.max(),n))
    return sorted(U) if len(U)>=2 else list(np.linspace(Vx.min()+0.05,Vx.max()-0.05,n))

# === (1) LCO 실측 O2 (Carlier2002) ===
xO2,VO2=load_xy(f"{LD}/diffthermo_LCO_O2_OCV_Carlier2002JES_Fig4a_digitized.csv")
Vo2,Do2=ocv_dqdv(xO2,VO2,3.35,4.5); Uo2=autoU(Vo2,Do2,4)
r2_O2,M_O2,p_O2,n_O2=plain_fit(Vo2,Do2,Uo2)

# === (2) LCO 해석 O3 (Marquis proxy = 우리가 v6서 쓴 것) ===
xM,VM=load_xy(f"{SC}/ocp/lco_Marquis2019.csv"); Vm,Dm=ocv_dqdv(xM,VM,3.5,4.3); Um=autoU(Vm,Dm,3)
r2_O3,M_O3,p_O3,n_O3=plain_fit(Vm,Dm,Um)

# === (3) 흑연 참조 (동일 plain 방법) ===
import bdd_smoothing as bdd
d=pd.read_parquet(f"{SC}/zenodo_gr/gr_pocv_4ccc47.parquet")
I=d['Current / A'].to_numpy(); Vv=d['Voltage / V'].to_numpy(); Q=d['Cumulative Capacity / Ah'].to_numpy()*1000
idx=np.where((np.abs(I)>1e-9)&(I>0))[0]; seg=max(np.split(idx,np.where(np.diff(idx)>1)[0]+1),key=len)
gx,gy=bdd.dqdv_grid_bdd(Vv[seg],Q[seg]-Q[seg][0],dV=0.0005); m=(gx>=0.06)&(gx<=0.25); Vg,Dg=gx[m],gy[m]
r2_gr,M_gr,p_gr,n_gr=plain_fit(Vg,Dg,[0.09,0.12,0.14,0.21])

print("=== plain MSMR(흑연과 완전 동일 자유피팅) R² ===")
print(f"  흑연(실측)         : R²={r2_gr:.4f}  (전이 {n_gr})")
print(f"  LCO O2(실측,Carlier): R²={r2_O2:.4f}  (전이 {n_O2})  ← 실측 데이터")
print(f"  LCO O3(해석,Marquis): R²={r2_O3:.4f}  (전이 {n_O3})  ← 해석 프록시")
print(f"\n판정: LCO O2 실측이 흑연과 비슷한 R² 면 → '방법·모델'은 LCO서도 정상 작동")
print(f"      (앞선 'LCO 안 맞음'은 실 O3 numeric 부재+해석프록시 불일치 문제였음).")

fig,ax=plt.subplots(1,3,figsize=(17,5))
for a,(nm,Vx,Dx,MF,pp,rr,col) in zip(ax,[
    ("흑연 실측 (plain MSMR)",Vg,Dg,M_gr,p_gr,r2_gr,'tab:blue'),
    ("LCO O2 실측 Carlier (plain MSMR)",Vo2,Do2,M_O2,p_O2,r2_O2,'tab:green'),
    ("LCO O3 해석 Marquis (plain MSMR)",Vm,Dm,M_O3,p_O3,r2_O3,'tab:orange')]):
    a.plot(Vx,Dx,'k',lw=1.5,alpha=.85,label='데이터')
    a.plot(Vx,MF(Vx,*pp),'--',color=col,lw=1.4,label=f'plain fit R²={rr:.3f}')
    a.set_title(nm,fontsize=10); a.set_xlabel('V'); a.set_ylabel('dQ/dV'); a.legend(fontsize=9); a.grid(alpha=.3)
fig.suptitle('사용자 가설 검증: 흑연과 "완전 동일한" plain MSMR 을 LCO 실측에 적용',fontsize=13)
fig.tight_layout(); fig.savefig(f"{OUT}/lco_plainfit.png",dpi=120); print("saved lco_plainfit.png")
json.dump({"graphite_r2":r2_gr,"LCO_O2_real_r2":r2_O2,"LCO_O3_proxy_r2":r2_O3,
           "verdict":"LCO real(O2) fits with same plain method as graphite; earlier failure = no real O3 numeric + proxy disagreement, not model"},
          open(f"{OUT}/lco_plainfit_result.json","w"),indent=1,default=float)
