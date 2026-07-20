# -*- coding: utf-8 -*-
"""v1.0.24 최종 코드 — SINTEF 공개 실측(Zenodo 20086298, CC-BY-4.0) 흑연·실리콘·흑연+Si 블렌드 피팅.
   반쪽셀 pOCV(C/50, RT). 모델=출하 equilibrium 자유폭 MSMR(흑연 host + Si host 가산). BDD 스무딩·curve_fit."""
import numpy as np, importlib.util, pandas as pd
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
plt.rcParams['font.family']='NanumGothic'; plt.rcParams['axes.unicode_minus']=False
from scipy.optimize import curve_fit
_trapz=getattr(np,'trapezoid',None) or getattr(np,'trapz',None)
ROOT="/home/user/Project_Anode_Fit/Claude"; DOC=f"{ROOT}/docs/v1.0.24"; CV=f"{ROOT}/results/comp_v24"
SC="/tmp/claude-0/-home-user-Project-Anode-Fit/e8d4cdbc-60e6-548e-b742-1446b8f7a8bd/scratchpad/sintef"
def load(n,p): s=importlib.util.spec_from_file_location(n,p); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
m=load("af",f"{DOC}/Anode_Fit_v1.0.24.py"); bdd=load("bdd",f"{CV}/bdd_smoothing.py")
GR=m.GraphiteAnodeDischargeDQDV

def load_delith(k):
    d=pd.read_parquet(f"{SC}/{k}.parquet")
    I=d['Current / A'].to_numpy(); V=d['Voltage / V'].to_numpy(); Q=d['Cumulative Capacity / Ah'].to_numpy()*1000.0
    idx=np.where(I>1e-9)[0]                                  # delith(양전류) 세그
    seg=max(np.split(idx,np.where(np.diff(idx)>1)[0]+1),key=len)
    return V[seg], Q[seg]-Q[seg][0]

def dqdv(V,Q,win,dvv):
    gx,gy=bdd.dqdv_grid_bdd(V,Q,dV=dvv); gy=np.abs(gy)
    mk=(gx>=win[0])&(gx<=win[1]); return gx[mk],gy[mk]

def model(NG,NS):
    def f(V,*p):
        gr=[];si=[];i=0
        for _ in range(NG): gr.append({'U':p[i],'w':p[i+1],'Q':p[i+2]});i+=3
        for _ in range(NS): si.append({'U':p[i],'w':p[i+1],'Q':p[i+2]});i+=3
        Cbg=p[i]; Va=np.asarray(V,float); out=np.asarray(GR(gr,Cbg=float(Cbg)).equilibrium(Va,298.15),float)
        if si: out=out+np.asarray(GR(si,Cbg=0.0).equilibrium(Va,298.15),float)
        return out
    return f

def fit(k,win,dvv,Ug,wg,Us,ws):
    V,Q=load_delith(k); Vx,Dx=dqdv(V,Q,win,dvv)
    NG,NS=len(Ug),len(Us); area=float(_trapz(Dx,Vx)); p0=[];lo=[];hi=[]
    for j in range(NG): p0+=[Ug[j],wg[j],0.2*area]; lo+=[0.05,0.0008,1e-6]; hi+=[0.30,0.060,10*area]
    for j in range(NS): p0+=[Us[j],ws[j],0.3*area]; lo+=[0.15,0.003,1e-6]; hi+=[0.60,0.30,10*area]
    p0+=[max(Dx.min(),1e-6)]; lo+=[0.0]; hi+=[max(Dx)+1e-9]
    popt,_=curve_fit(model(NG,NS),Vx,Dx,p0=p0,bounds=(lo,hi),maxfev=600000)
    pred=model(NG,NS)(Vx,*popt); r2=1.0-np.sum((Dx-pred)**2)/np.sum((Dx-Dx.mean())**2)
    # 성분 분해(블렌드 가시화)
    i=0;Qg=0;Qs=0;grc=None;sic=None
    gr=[];si=[]
    for _ in range(NG): gr.append({'U':popt[i],'w':popt[i+1],'Q':popt[i+2]});Qg+=popt[i+2];i+=3
    for _ in range(NS): si.append({'U':popt[i],'w':popt[i+1],'Q':popt[i+2]});Qs+=popt[i+2];i+=3
    Cbg=popt[i]
    if NG: grc=np.asarray(GR(gr,Cbg=float(Cbg)).equilibrium(Vx,298.15),float)
    if NS: sic=np.asarray(GR(si,Cbg=0.0).equilibrium(Vx,298.15),float)
    fSi=Qs/(Qg+Qs) if (Qg+Qs)>0 else None
    return dict(Vx=Vx,Dx=Dx,pred=pred,r2=float(r2),NG=NG,NS=NS,npts=len(Vx),grc=grc,sic=sic,fSi=fSi)

r_gr =fit('gr',  (0.05,0.30),0.0005, Ug=[0.088,0.120,0.142,0.210],wg=[0.004,0.006,0.016,0.006], Us=[],ws=[])
r_si =fit('si',  (0.06,0.55),0.001,  Ug=[],wg=[], Us=[0.28,0.40,0.47],ws=[0.05,0.05,0.03])
r_sg =fit('sigr',(0.05,0.52),0.0007, Ug=[0.10,0.12,0.14,0.21],wg=[0.003,0.005,0.02,0.005], Us=[0.30,0.43,0.47],ws=[0.06,0.006,0.05])

fig,ax=plt.subplots(1,3,figsize=(18,5.4))
def draw(a,title,r,showcomp=False):
    a.plot(r['Vx'],r['Dx'],'o',ms=2.2,color='0.35',alpha=.55,label=f"실측 dQ/dV (BDD, {r['npts']}점)")
    a.plot(r['Vx'],r['pred'],'-',color='tab:red',lw=2,label=f"모델 피팅 (R²={r['r2']:.4f})")
    if showcomp and r['grc'] is not None:
        a.plot(r['Vx'],r['grc'],'--',color='tab:blue',lw=1.1,label='흑연 성분')
        a.plot(r['Vx'],r['sic'],':',color='tab:green',lw=1.4,label=f"Si 성분 (f_Si={r['fSi']:.2f})")
    a.set_title(title); a.set_xlabel('V vs Li'); a.set_ylabel('dQ/dV'); a.legend(fontsize=8); a.grid(alpha=.3)
draw(ax[0],'(1) 흑연 반쪽셀\nSINTEF Zenodo(실측 pOCV C/50)',r_gr)
draw(ax[1],'(2) 실리콘 반쪽셀\nSINTEF(단일상 broad 고용체)',r_si)
draw(ax[2],'(3) 흑연+Si 블렌드 반쪽셀\nSINTEF(흑연 4전이 + Si 가산)',r_sg,showcomp=True)
fig.suptitle('v1.0.24 최종 코드 — SINTEF 공개 실측(Zenodo 20086298, CC-BY-4.0) 피팅: 흑연·실리콘·흑연+Si 블렌드',fontsize=13)
fig.tight_layout(); fig.savefig(f"{CV}/final_fit_sintef.png",dpi=120)
print("="*72)
for nm,r in [("흑연(SINTEF)",r_gr),("실리콘(SINTEF)",r_si),("흑연+Si 블렌드(SINTEF)",r_sg)]:
    print(f"{nm:22s} R²={r['r2']:.4f}  흑연전이={r['NG']} Si전이={r['NS']}  f_Si={r['fSi'] if r['fSi'] else '-'}  점={r['npts']}")
print("saved: final_fit_sintef.png")
