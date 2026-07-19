# -*- coding: utf-8 -*-
"""v1.0.24 개선방향①검증 — 흑연 전이 4개 vs 6개 (BDD 추출). 문헌(coal-graphite MSMR 6-gallery,
JES 2024 ad2061)이 6전이 사용·U0≈{0.333,0.210,0.128,0.126,0.089,0.089}. 4→6 이 실측 잔차(병합된
4↔3↔2L 클러스터·미포착 sub-피크)를 닫는가? 개선방향 §1(저위험·최고효율) 실증. 코드 무수정(실험).
"""
import numpy as np, pandas as pd, importlib.util, os, sys, json
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
sys.path.insert(0,"/home/user/Project_Anode_Fit/Claude/results/comp_v24"); import bdd_smoothing as bdd
SC="/tmp/claude-0/-home-user-Project-Anode-Fit/e8d4cdbc-60e6-548e-b742-1446b8f7a8bd/scratchpad/zenodo_gr"
OUT="/home/user/Project_Anode_Fit/Claude/results/comp_v24"
af_s=importlib.util.spec_from_file_location("af","/home/user/Project_Anode_Fit/Claude/docs/v1.0.23/Anode_Fit_v1.0.23.py")
af=importlib.util.module_from_spec(af_s); af_s.loader.exec_module(af); GR=af.GraphiteAnodeDischargeDQDV
_trapz=getattr(np,'trapezoid',getattr(np,'trapz',None))

def get(path):
    d=pd.read_parquet(os.path.join(SC,path)); I=d['Current / A'].to_numpy(); V=d['Voltage / V'].to_numpy(); Q=d['Cumulative Capacity / Ah'].to_numpy()*1000
    idx=np.where((np.abs(I)>1e-9)&(I>0))[0]; seg=max(np.split(idx,np.where(np.diff(idx)>1)[0]+1),key=len)
    return bdd.dqdv_grid_bdd(V[seg],Q[seg]-Q[seg][0],dV=0.0005)

def model(NT):
    def f(V,*p):
        trs=[{'U':p[3*j],'w':p[3*j+1],'Q':p[3*j+2]} for j in range(NT)]; Cbg=p[3*NT]
        return np.asarray(GR(trs,Cbg=float(Cbg)).equilibrium(np.asarray(V,float),298.15),float)
    return f

def fit(Vx,Dx,U0,w0):
    NT=len(U0); area=float(_trapz(Dx,Vx))
    p0=[]; lo=[]; hi=[]
    for j in range(NT): p0+=[U0[j],w0[j],0.15*area]; lo+=[0.05,0.0008,1e-9]; hi+=[0.30,0.060,10*area]
    p0+=[max(Dx.min(),1e-6)]; lo+=[0.0]; hi+=[max(Dx)]
    popt,_=curve_fit(model(NT),Vx,Dx,p0=p0,bounds=(lo,hi),maxfev=800000)
    pred=model(NT)(Vx,*popt); r2=1-np.sum((Dx-pred)**2)/np.sum((Dx-Dx.mean())**2)
    return popt,pred,float(r2)

U4=[0.104,0.1415,0.227,0.140]; w4=[0.0009,0.0011,0.0016,0.018]
# 6전이: canonical stage 전위(coal-graphite 6-gallery 근사)
U6=[0.089,0.089,0.120,0.128,0.170,0.210]; w6=[0.001,0.003,0.002,0.012,0.020,0.010]

fig,ax=plt.subplots(1,2,figsize=(15,5.4)); summ={}
for k,cell in enumerate(["gr_pocv_4ccc47.parquet","gr_pocv_1d5628.parquet"]):
    gx,gy=get(cell); m=(gx>=0.05)&(gx<=0.30); Vx,Dx=gx[m],gy[m]
    p4,pr4,r4=fit(Vx,Dx,U4,w4); p6,pr6,r6=fit(Vx,Dx,U6,w6)
    summ[cell]={"R2_4tr":round(r4,4),"R2_6tr":round(r6,4),
                "U6":sorted([round(p6[3*j],4) for j in range(6)]),
                "w6_mV":[round(p6[3*j+1]*1000,2) for j in np.argsort([p6[3*j] for j in range(6)])]}
    a=ax[k]; a.plot(Vx,Dx,color='tab:blue',lw=1.4,label='real (BDD)')
    Vm=np.arange(0.05,0.30,0.00002)
    a.plot(Vm,model(4)(Vm,*p4),'--',color='tab:orange',lw=1.2,label=f'4전이 R²={r4:.3f}')
    a.plot(Vm,model(6)(Vm,*p6),'-',color='k',lw=1.3,label=f'6전이 R²={r6:.3f}')
    a.set_xlabel('V'); a.set_ylabel('dQ/dV'); a.set_title(f'{cell.split("_")[-1][:6]}: 흑연 4 vs 6 전이'); a.legend(fontsize=8); a.grid(alpha=.3)
fig.tight_layout(); fig.savefig(f"{OUT}/gr_4vs6_transitions.png",dpi=120); print("saved gr_4vs6_transitions.png")
print(json.dumps(summ,ensure_ascii=False,indent=1))
