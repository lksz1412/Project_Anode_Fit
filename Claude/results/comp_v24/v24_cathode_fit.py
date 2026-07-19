# -*- coding: utf-8 -*-
"""v1.0.24 V2확장(양극) — 층상산화물 반쪽셀 실측 vs 문건 양극 모델(LCOCathodeDQDV/MSMR).
⚠ NMC ≠ LCO: 공개 LCO 반쪽셀 원자료 부재(전수 확인) → 층상(R-3m) 구조 유사체 NMC111/NMC532
   (동일 Zenodo 20086298, 상온 pOCV)로 '양극측 곡선식(솔리드솔루션 로지스틱-미분 합)'을 검증.
   결과는 양극 모델링 접근의 실측 타당성만 지지 — LCO 고유 feature(3.93V 평탄·order-disorder)와는 다름.
모델 = 출하 LCOCathodeDQDV.equilibrium (흑연식 상속, MSMR 동형). 'w'만 부여=자유폭.
"""
import numpy as np, pandas as pd, importlib.util, os, json
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from scipy.signal import savgol_filter
from scipy.optimize import curve_fit
_trapz = getattr(np,'trapezoid',getattr(np,'trapz',None))
SC="/tmp/claude-0/-home-user-Project-Anode-Fit/e8d4cdbc-60e6-548e-b742-1446b8f7a8bd/scratchpad/zenodo_gr"
OUT="/home/user/Project_Anode_Fit/Claude/results/comp_v24"
s=importlib.util.spec_from_file_location("af","/home/user/Project_Anode_Fit/Claude/docs/v1.0.23/Anode_Fit_v1.0.23.py")
af=importlib.util.module_from_spec(s); s.loader.exec_module(af)
LCO=af.LCOCathodeDQDV
CELLS={"NMC111":"nmc111_c1_pocv.parquet","NMC532":"nmc532_c1_pocv.parquet"}
LO,HI=3.55,4.28; NT=4     # 양극 창(주 solid-solution 영역), 4 전이

def longest(mask):
    idx=np.where(mask)[0]
    if len(idx)==0: return None
    return max(np.split(idx,np.where(np.diff(idx)>1)[0]+1),key=len)
def dqdv(path,win_mV=15.0,dV=0.001):
    d=pd.read_parquet(os.path.join(SC,path))
    I=d['Current / A'].to_numpy(); V=d['Voltage / V'].to_numpy(); Q=d['Cumulative Capacity / Ah'].to_numpy()*1000.0
    seg=longest((np.abs(I)>1e-9)&(I>0)); Vs=V[seg]; Qs=Q[seg]-Q[seg][0]
    o=np.argsort(Vs); Vs,Qs=Vs[o],Qs[o]
    Vu,inv=np.unique(np.round(Vs,5),return_inverse=True)
    Qu=np.array([Qs[inv==k].mean() for k in range(len(Vu))])
    grid=np.arange(Vu.min(),Vu.max(),dV); Qg=np.interp(grid,Vu,Qu)
    win=int(round(win_mV/1000/dV)); win+=(win%2==0); win=max(win,5)
    return grid,np.abs(savgol_filter(Qg,win,3,deriv=1,delta=dV))
def model(V,*p):
    trs=[{'U':p[3*j],'w':p[3*j+1],'Q':p[3*j+2]} for j in range(NT)]; Cbg=p[3*NT]
    return np.asarray(LCO(trs,Cbg=float(Cbg)).equilibrium(np.asarray(V,float),298.15),float)
def fit(name,path):
    gV,gd=dqdv(path); m=(gV>=LO)&(gV<=HI); Vx,Dx=gV[m],gd[m]; area=float(_trapz(Dx,Vx))
    U0=[3.68,3.75,3.90,4.05]
    p0=[]; lob=[]; hib=[]
    for j in range(NT): p0+=[U0[j],0.03,0.25*area]; lob+=[LO,0.005,1e-6]; hib+=[HI,0.20,10*area]
    p0+=[max(Dx.min(),1e-6)]; lob+=[0.0]; hib+=[max(Dx)]
    popt,_=curve_fit(model,Vx,Dx,p0=p0,bounds=(lob,hib),maxfev=400000)
    pred=model(Vx,*popt); r2=1-np.sum((Dx-pred)**2)/np.sum((Dx-Dx.mean())**2)
    U=sorted([round(popt[3*j],4) for j in range(NT)]); w=[round(popt[3*j+1]*1000,1) for j in range(NT)]
    return {"name":name,"R2":round(float(r2),4),"U_fit":U,"w_mV":sorted(w)},(Vx,Dx,popt)
res={}; pan={}
for n,p in CELLS.items():
    r,pk=fit(n,p); res[n]=r; pan[n]=pk; print(json.dumps(r,ensure_ascii=False))
fig,ax=plt.subplots(1,len(CELLS),figsize=(13,4.8))
for a,(n,pk) in zip(ax,pan.items()):
    Vx,Dx,popt=pk; Vm=np.arange(LO,HI,0.0002)
    a.plot(Vx,Dx,color='tab:purple',lw=1.5,label='real delith (charge)')
    a.plot(Vm,model(Vm,*popt),'--',color='k',lw=1.4,label=f'doc cathode FIT (R²={res[n]["R2"]:.3f})')
    a.set_title(f'{n} half-cell (⚠ LCO 아님, 층상 유사체)',fontsize=10); a.set_xlabel('V vs Li'); a.set_ylabel('dQ/dV'); a.legend(fontsize=8); a.grid(alpha=.3)
fig.tight_layout(); fig.savefig(f"{OUT}/cathode_fit.png",dpi=120); print("saved",f"{OUT}/cathode_fit.png")
json.dump(res,open(f"{OUT}/cathode_fit_result.json","w"),ensure_ascii=False,indent=2)
