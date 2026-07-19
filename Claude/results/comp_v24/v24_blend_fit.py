# -*- coding: utf-8 -*-
"""v1.0.24 V2(블렌드) — Si-흑연 반쪽셀 실측(Zenodo 20086298 pOCV, 상온) vs 문건 블렌드 모델.

검증 대상(문건 §3.5 blend 합성식): blend dQ/dV = 흑연 host + Si host (공통 V축 가산).
  → 실측 SiGr dQ/dV 가 (a)흑연 스테이징 sharp 피크 그대로 + (b)Si 넓은 기여 로 분해되나?
  → Si:흑연 용량 배분(fit)이 metadata wt% 유도 f_Si (AQ-1≈0.30·AQ-2≈0.75)와 부합하나?
파이프라인은 흑연(V2)과 동일: savgol dQ/dV, 출하 equilibrium() 합성 직접 호출 curve_fit.
  model = GraphiteAnode(gr_trs).equilibrium + GraphiteAnode(si_trs).equilibrium  (= BlendedAnodeDQDV.equilibrium)
"""
import numpy as np, pandas as pd, importlib.util, os, json
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from scipy.signal import savgol_filter
from scipy.optimize import curve_fit
_trapz = getattr(np, 'trapezoid', getattr(np, 'trapz', None))

SCRATCH = "/tmp/claude-0/-home-user-Project-Anode-Fit/e8d4cdbc-60e6-548e-b742-1446b8f7a8bd/scratchpad/zenodo_gr"
OUTDIR  = "/home/user/Project_Anode_Fit/Claude/results/comp_v24"
CELLS = {"SiGr_AQ1_lowSi": (f"{SCRATCH}/sigr_aq1_pocv.parquet", 510.0, 0.30),   # (path, theo mAh/g, f_Si기대)
         "SiGr_AQ2_highSi":(f"{SCRATCH}/sigr_aq2_pocv.parquet", 1150.0, 0.75)}
LO, HI = 0.05, 0.60      # 블렌드 창(Si 넓은 기여 포함)
RT_F = 8.314*298.15/96485.0
NG, NS = 4, 2            # 흑연 4전이 + Si 2전이

s = importlib.util.spec_from_file_location("af","/home/user/Project_Anode_Fit/Claude/docs/v1.0.23/Anode_Fit_v1.0.23.py")
af = importlib.util.module_from_spec(s); s.loader.exec_module(af)
GRfit = json.load(open(f"{OUTDIR}/gr_fit_result.json"))["cell_1d5628"]   # V2 흑연 초기값
Ug0 = GRfit["U_fit"]; wg0 = [x/1000 for x in GRfit["w_fit_mV"]]

def longest_segment(mask):
    idx = np.where(mask)[0]
    if len(idx)==0: return None
    return max(np.split(idx, np.where(np.diff(idx)>1)[0]+1), key=len)

def dqdv_savgol(seg, V, Qm, dV=0.0005, win_mV=6.0, poly=3):
    Vs=V[seg].astype(float); Qs=Qm[seg].astype(float); Qs=Qs-Qs[0]
    o=np.argsort(Vs); Vs,Qs=Vs[o],Qs[o]
    Vu,inv=np.unique(np.round(Vs,6),return_inverse=True)
    Qu=np.array([Qs[inv==k].mean() for k in range(len(Vu))])
    if len(Vu)<10: return None,None
    grid=np.arange(Vu.min(),Vu.max(),dV); Qg=np.interp(grid,Vu,Qu)
    win=int(round(win_mV/1000/dV)); win+=(win%2==0); win=max(win,poly+2)
    if win>=len(Qg): return grid, np.abs(np.gradient(Qg,dV))
    return grid, np.abs(savgol_filter(Qg,win,poly,deriv=1,delta=dV))

def model_blend(V, *p):
    """p=[Ug(4),wg(4),Qg(4), Us(2),ws(2),Qs(2), Cbg] → 흑연host.eq + Si host.eq (= 블렌드 합성식)."""
    i=0; Ug=p[i:i+NG]; i+=NG; wg=p[i:i+NG]; i+=NG; Qg=p[i:i+NG]; i+=NG
    Us=p[i:i+NS]; i+=NS; ws=p[i:i+NS]; i+=NS; Qs=p[i:i+NS]; i+=NS; Cbg=p[i]
    gr=[{'U':float(Ug[j]),'w':float(wg[j]),'Q':float(Qg[j])} for j in range(NG)]
    si=[{'U':float(Us[j]),'w':float(ws[j]),'Q':float(Qs[j])} for j in range(NS)]
    g_gr=af.GraphiteAnodeDischargeDQDV(gr, Cbg=float(Cbg))
    g_si=af.GraphiteAnodeDischargeDQDV(si, Cbg=0.0)
    Va=np.asarray(V,float)
    return np.asarray(g_gr.equilibrium(Va,T=298.15),float)+np.asarray(g_si.equilibrium(Va,T=298.15),float)

def fit_blend(name, path):
    df=pd.read_parquet(path)
    I=df['Current / A'].to_numpy(); V=df['Voltage / V'].to_numpy()
    Qc=df['Cumulative Capacity / Ah'].to_numpy()*1000.0
    seg=longest_segment((np.abs(I)>1e-9)&(I>0))   # delith
    gV,gd=dqdv_savgol(seg,V,Qc)
    m=(gV>=LO)&(gV<=HI); Vx,Dx=gV[m],gd[m]
    area=float(_trapz(Dx,Vx))
    # 초기값: 흑연=V2 fit, Si=SIC_LIT(넓은 0.30/0.42), Q 는 면적 분배
    p0 = list(Ug0)+list(wg0)+[0.2*area]*NG + [0.30,0.42]+[0.05,0.05]+[0.3*area,0.3*area] + [max(Dx.min(),1e-6)]
    lob = [0.05]*NG+[0.0008]*NG+[1e-6]*NG + [0.18,0.18]+[0.01,0.01]+[1e-6,1e-6] + [0.0]
    hib = [0.30]*NG+[0.060]*NG+[10*area]*NG + [0.58,0.58]+[0.25,0.25]+[10*area,10*area]+[max(Dx)]
    popt,_=curve_fit(model_blend,Vx,Dx,p0=p0,bounds=(lob,hib),maxfev=400000)
    pred=model_blend(Vx,*popt)
    r2=1.0-np.sum((Dx-pred)**2)/np.sum((Dx-Dx.mean())**2)
    i=0; Ug=popt[i:i+NG];i+=NG; wg=popt[i:i+NG];i+=NG; Qg=popt[i:i+NG];i+=NG
    Us=popt[i:i+NS];i+=NS; ws=popt[i:i+NS];i+=NS; Qs=popt[i:i+NS];i+=NS; Cbg=popt[i]
    Qgr=float(np.sum(Qg)); Qsi=float(np.sum(Qs)); fSi_fit=Qsi/(Qgr+Qsi)
    res={"name":name,"R2":round(float(r2),4),"area_mAh":round(area,3),
         "U_gr":[round(float(x),4) for x in Ug],"w_gr_mV":[round(float(x)*1000,2) for x in wg],
         "U_si":[round(float(x),4) for x in Us],"w_si_mV":[round(float(x)*1000,1) for x in ws],
         "Q_gr_sum":round(Qgr,4),"Q_si_sum":round(Qsi,4),"f_Si_fit":round(fSi_fit,3),"Cbg":round(float(Cbg),3)}
    return res,(Vx,Dx,pred,popt)

results={}; panels={}
for name,(path,theo,fexp) in CELLS.items():
    r,pk=fit_blend(name,path); r["f_Si_expected(theo%.0f)"%theo]=fexp
    results[name]=r; panels[name]=pk
    print(f"\n=== {name} (theo {theo} mAh/g, f_Si기대 {fexp}) ===")
    print(json.dumps(r,ensure_ascii=False,indent=2))

# 그림: 두 블렌드 real vs fit(흑연성분·Si성분 분해)
fig,axes=plt.subplots(len(CELLS),1,figsize=(11,5.0*len(CELLS)))
if len(CELLS)==1: axes=[axes]
for ax,(name,pk) in zip(axes,panels.items()):
    Vx,Dx,pred,popt=pk
    i=0; Ug=popt[:NG]; wg=popt[NG:2*NG]; Qg=popt[2*NG:3*NG]
    Us=popt[3*NG:3*NG+NS]; ws=popt[3*NG+NS:3*NG+2*NS]; Qs=popt[3*NG+2*NS:3*NG+3*NS]; Cbg=popt[-1]
    gr=[{'U':float(Ug[j]),'w':float(wg[j]),'Q':float(Qg[j])} for j in range(NG)]
    si=[{'U':float(Us[j]),'w':float(ws[j]),'Q':float(Qs[j])} for j in range(NS)]
    Vm=np.arange(LO,HI,0.00002)   # 고해상 0.02mV — 매끄러운 모델선
    d_gr=np.asarray(af.GraphiteAnodeDischargeDQDV(gr,Cbg=float(Cbg)).equilibrium(Vm,T=298.15),float)
    d_si=np.asarray(af.GraphiteAnodeDischargeDQDV(si,Cbg=0.0).equilibrium(Vm,T=298.15),float)
    ax.plot(Vx,Dx,color='tab:blue',lw=1.5,label='real delith (savgol)')
    ax.plot(Vm,model_blend(Vm,*popt),'--',color='k',lw=1.5,label=f'blend model FIT (R²={results[name]["R2"]:.3f}, fine grid)')
    ax.plot(Vm,d_gr,':',color='tab:green',lw=1.3,label='  ├ graphite host (staging)')
    ax.plot(Vm,d_si,':',color='tab:red',lw=1.3,label=f'  └ Si host (broad, f_Si={results[name]["f_Si_fit"]:.2f})')
    ax.set_xlabel('Voltage / V'); ax.set_ylabel('dQ/dV / (mAh/V)')
    ax.set_title(f'{name}: blend = graphite host + Si host (doc §3.5 composition)')
    ax.legend(fontsize=8); ax.grid(alpha=.3); ax.set_xlim(LO,HI)
fig.tight_layout()
OUT=f"{OUTDIR}/blend_fit.png"; fig.savefig(OUT,dpi=120); print("\nsaved",OUT)
json.dump(results,open(f"{OUTDIR}/blend_fit_result.json","w"),ensure_ascii=False,indent=2)
print("saved",f"{OUTDIR}/blend_fit_result.json")
