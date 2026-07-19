# -*- coding: utf-8 -*-
"""v1.0.24 개선방향#4 프로토타입 — 정칙용액(Frumkin) peak vs 로지스틱(MSMR).
잔차 지배원인=두-상 near-delta(로지스틱 구조 한계, R²~0.95 천장). 정칙용액 등온선은 Ω→2RT 서
무한 sharp(진짜 두-상)로 수렴 → near-delta 재현 가능(문헌 #4). 흑연서 로지스틱 대비 R² 개선?
정칙용액: F(U−V)=RT·ln(θ/(1−θ))+Ω(1−2θ) → dQ/dV=Q·F/|RT/(θ(1−θ))−2Ω| (θ 매개변수화).
Ω<2RT 단일상(가역 invertible); Ω→2RT 서 peak 발산. ※프로토타입(문건 코드 무수정 실험).
"""
import numpy as np, pandas as pd, importlib.util, sys, warnings; warnings.filterwarnings("ignore")
sys.path.insert(0,"/home/user/Project_Anode_Fit/Claude/results/comp_v24"); import bdd_smoothing as bdd
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
SC="/tmp/claude-0/-home-user-Project-Anode-Fit/e8d4cdbc-60e6-548e-b742-1446b8f7a8bd/scratchpad/zenodo_gr"; OUT="/home/user/Project_Anode_Fit/Claude/results/comp_v24"
af_s=importlib.util.spec_from_file_location("af","/home/user/Project_Anode_Fit/Claude/docs/v1.0.23/Anode_Fit_v1.0.23.py")
af=importlib.util.module_from_spec(af_s); af_s.loader.exec_module(af); GR=af.GraphiteAnodeDischargeDQDV
R=8.314; F=96485.0; T=298.15; RT=R*T; _trapz=getattr(np,'trapezoid',getattr(np,'trapz',None))

def get(cell):
    d=pd.read_parquet(f"{SC}/{cell}"); I=d['Current / A'].to_numpy(); V=d['Voltage / V'].to_numpy(); Q=d['Cumulative Capacity / Ah'].to_numpy()*1000
    idx=np.where((np.abs(I)>1e-9)&(I>0))[0]; seg=max(np.split(idx,np.where(np.diff(idx)>1)[0]+1),key=len)
    return bdd.dqdv_grid_bdd(V[seg],Q[seg]-Q[seg][0],dV=0.0005)

_th=np.linspace(2e-3,1-2e-3,700)   # 안정·경량
_OMAX=2*RT*0.97                    # Ω<2RT 여유(특이점 회피, near-delta 유지)
def regsol_peak(Vg,U,Om,Q):
    Om=min(Om,_OMAX)
    Vth=U-(RT*np.log(_th/(1-_th))+Om*(1-2*_th))/F
    dq=np.clip(Q*F/np.abs(RT/(_th*(1-_th))-2*Om),0,5000)   # 물리 cap
    o=np.argsort(Vth)
    return np.interp(Vg,Vth[o],dq[o],left=0,right=0)
def logi(V,U,w): z=(V-U)/w; s=np.where(z>=0,1/(1+np.exp(-z)),np.exp(z)/(1+np.exp(z))); return s*(1-s)

NT=4; U0=[0.104,0.1415,0.227,0.140]
def model_log(V,*p):
    out=np.full_like(np.asarray(V,float),p[-1])
    for j in range(NT): out=out+p[3*j+2]*logi(V,p[3*j],p[3*j+1])
    return out
def model_rs(V,*p):
    out=np.full_like(np.asarray(V,float),p[-1])
    for j in range(NT): out=out+regsol_peak(V,p[3*j],p[3*j+1],p[3*j+2])
    return out

fig,ax=plt.subplots(1,2,figsize=(15,5.4)); summ={}
for k,cell in enumerate(["gr_pocv_4ccc47.parquet","gr_pocv_1d5628.parquet"]):
    gx,gy=get(cell); m=(gx>=0.05)&(gx<=0.30); Vx,Dx=gx[m],gy[m]; area=float(_trapz(Dx,Vx))
    # 로지스틱
    p0=[]; lo=[]; hi=[]
    for j in range(NT): p0+=[U0[j],0.003,50]; lo+=[0.05,0.0008,1e-6]; hi+=[0.30,0.06,1e5]
    p0+=[0.1]; lo+=[0]; hi+=[max(Dx)]
    pl,_=curve_fit(model_log,Vx,Dx,p0=p0,bounds=(lo,hi),maxfev=600000); prl=model_log(Vx,*pl)
    r2l=1-np.sum((Dx-prl)**2)/np.sum((Dx-Dx.mean())**2)
    # 정칙용액 (Ω<2RT·0.97)
    p0=[]; lo=[]; hi=[]
    for j in range(NT): p0+=[U0[j],2*RT*0.8,0.2*area]; lo+=[0.05,0.0,1e-6]; hi+=[0.30,_OMAX,10*area]
    p0+=[0.1]; lo+=[0]; hi+=[max(Dx)]
    pr,_=curve_fit(model_rs,Vx,Dx,p0=p0,bounds=(lo,hi),maxfev=40000); prr=model_rs(Vx,*pr)
    r2r=1-np.sum((Dx-prr)**2)/np.sum((Dx-Dx.mean())**2)
    Om_over_2RT=[round(pr[3*j+1]/(2*RT),3) for j in range(NT)]
    summ[cell]={"R2_logistic":round(r2l,4),"R2_regsol":round(r2r,4),"Omega/2RT":Om_over_2RT}
    a=ax[k]; a.plot(Vx,Dx,color='tab:blue',lw=1.5,label='real (BDD)')
    Vm=np.arange(0.05,0.30,0.00002)
    a.plot(Vm,model_log(Vm,*pl),'--',color='tab:orange',lw=1.1,label=f'로지스틱(MSMR) R²={r2l:.3f}')
    a.plot(Vm,model_rs(Vm,*pr),'-',color='k',lw=1.2,label=f'정칙용액(Frumkin) R²={r2r:.3f}')
    a.set_xlabel('V'); a.set_ylabel('dQ/dV'); a.set_title(f'{cell.split("_")[-1][:6]}: 로지스틱 vs 정칙용액'); a.legend(fontsize=8); a.grid(alpha=.3)
fig.tight_layout(); fig.savefig(f"{OUT}/regsol_proto.png",dpi=120)
import json; print(json.dumps(summ,ensure_ascii=False,indent=1)); print("saved regsol_proto.png")
