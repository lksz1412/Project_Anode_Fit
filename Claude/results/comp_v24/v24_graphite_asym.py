# -*- coding: utf-8 -*-
"""v1.0.24 개선방향②검증 — 대칭 MSMR peak vs 두-측(비대칭) width. 4v6 결과: 흑연 잔차 지배원인은
미포착 피크 아닌 '피크 비대칭'(실측=급상승/완만tail). 단일 로지스틱 ξ(1-ξ)는 구조적 대칭.
Zhu 2023(Adv.Mater.) 두-측 접근: V<U 는 w_L, V>U 는 w_R. R² 개선하면 개선방향②가 실측 잔차의 해법.
※ 실험(코드 무수정) — 대칭판은 문건식과 동형(wL=wR 확인)."""
import numpy as np, pandas as pd, importlib.util, os, sys, json
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
sys.path.insert(0,"/home/user/Project_Anode_Fit/Claude/results/comp_v24"); import bdd_smoothing as bdd
SC="/tmp/claude-0/-home-user-Project-Anode-Fit/e8d4cdbc-60e6-548e-b742-1446b8f7a8bd/scratchpad/zenodo_gr"
OUT="/home/user/Project_Anode_Fit/Claude/results/comp_v24"; _trapz=getattr(np,'trapezoid',getattr(np,'trapz',None))

def get(path):
    d=pd.read_parquet(os.path.join(SC,path)); I=d['Current / A'].to_numpy(); V=d['Voltage / V'].to_numpy(); Q=d['Cumulative Capacity / Ah'].to_numpy()*1000
    idx=np.where((np.abs(I)>1e-9)&(I>0))[0]; seg=max(np.split(idx,np.where(np.diff(idx)>1)[0]+1),key=len)
    return bdd.dqdv_grid_bdd(V[seg],Q[seg]-Q[seg][0],dV=0.0005)

def logi(V,U,w):
    z=(V-U)/w; return np.where(z>=0,1/(1+np.exp(-z)),np.exp(z)/(1+np.exp(z)))
def peak_sym(V,U,w,A):
    s=logi(V,U,w); return A*s*(1-s)
def peak_asym(V,U,wL,wR,A):
    w=np.where(V<=U,wL,wR); s=logi(V,U,w); return A*s*(1-s)

NT=4; U0=[0.104,0.1415,0.227,0.140]
def model_sym(V,*p):
    out=np.full_like(np.asarray(V,float),p[-1])
    for j in range(NT): out=out+peak_sym(V,p[3*j],p[3*j+1],p[3*j+2])
    return out
def model_asym(V,*p):
    out=np.full_like(np.asarray(V,float),p[-1])
    for j in range(NT): out=out+peak_asym(V,p[4*j],p[4*j+1],p[4*j+2],p[4*j+3])
    return out

fig,ax=plt.subplots(1,2,figsize=(15,5.4)); summ={}
for k,cell in enumerate(["gr_pocv_4ccc47.parquet","gr_pocv_1d5628.parquet"]):
    gx,gy=get(cell); m=(gx>=0.05)&(gx<=0.30); Vx,Dx=gx[m],gy[m]; area=float(_trapz(Dx,Vx))
    # 대칭
    p0=[]; lo=[]; hi=[]
    for j in range(NT): p0+=[U0[j],0.003,50]; lo+=[0.05,0.0008,1e-6]; hi+=[0.30,0.06,1e5]
    p0+=[0.1]; lo+=[0]; hi+=[max(Dx)]
    ps,_=curve_fit(model_sym,Vx,Dx,p0=p0,bounds=(lo,hi),maxfev=800000); prs=model_sym(Vx,*ps)
    r2s=1-np.sum((Dx-prs)**2)/np.sum((Dx-Dx.mean())**2)
    # 비대칭(두-측)
    p0=[]; lo=[]; hi=[]
    for j in range(NT): p0+=[U0[j],0.003,0.003,50]; lo+=[0.05,0.0008,0.0008,1e-6]; hi+=[0.30,0.06,0.06,1e5]
    p0+=[0.1]; lo+=[0]; hi+=[max(Dx)]
    pa,_=curve_fit(model_asym,Vx,Dx,p0=p0,bounds=(lo,hi),maxfev=1200000); pra=model_asym(Vx,*pa)
    r2a=1-np.sum((Dx-pra)**2)/np.sum((Dx-Dx.mean())**2)
    asym=[round(pa[4*j+2]/pa[4*j+1],2) for j in range(NT)]  # wR/wL 비대칭비
    summ[cell]={"R2_sym":round(r2s,4),"R2_asym":round(r2a,4),"wR_over_wL":asym}
    a=ax[k]; a.plot(Vx,Dx,color='tab:blue',lw=1.4,label='real (BDD)')
    Vm=np.arange(0.05,0.30,0.00002)
    a.plot(Vm,model_sym(Vm,*ps),'--',color='tab:orange',lw=1.2,label=f'대칭 R²={r2s:.3f}')
    a.plot(Vm,model_asym(Vm,*pa),'-',color='k',lw=1.3,label=f'비대칭(두-측) R²={r2a:.3f}')
    a.set_xlabel('V'); a.set_ylabel('dQ/dV'); a.set_title(f'{cell.split("_")[-1][:6]}: 대칭 vs 두-측 width'); a.legend(fontsize=8); a.grid(alpha=.3)
fig.tight_layout(); fig.savefig(f"{OUT}/gr_sym_vs_asym.png",dpi=120); print("saved gr_sym_vs_asym.png")
print(json.dumps(summ,ensure_ascii=False,indent=1))
