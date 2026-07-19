# -*- coding: utf-8 -*-
"""v1.0.24 V2확장 — 공개데이터 다중 셀·다중 조성 종합 검증(Zenodo 20086298, 상온 pOCV).
대상: 흑연(2셀)·순수Si(2셀)·SiGr-AQ1저Si(2셀)·SiGr-AQ2고Si(2셀)·B/SiGr-AQ3(2셀) = 10셀.
목적:
  (1) 모델선을 고해상 격자(0.02mV)로 그려 '각짐(그림 격자 아티팩트)' 제거.
  (2) 순수 Si host 단독 검증(문건 Si 케이스 셋의 중심·폭 실측 대조).
  (3) 흑연 스테이징 피크 위치·폭의 셀·조성 간 재현성.
  (4) 피팅 f_Si 가 metadata theo 용량 유도 f_Si 와 조성 전반에서 일치하나.
모델 = 출하 GraphiteAnodeDischargeDQDV.equilibrium 합성(흑연 host + Si host), 'w'만 부여=자유폭.
"""
import numpy as np, pandas as pd, importlib.util, os, json
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from scipy.signal import savgol_filter
from scipy.optimize import curve_fit
_trapz = getattr(np, 'trapezoid', getattr(np, 'trapz', None))

SC = "/tmp/claude-0/-home-user-Project-Anode-Fit/e8d4cdbc-60e6-548e-b742-1446b8f7a8bd/scratchpad/zenodo_gr"
OUT = "/home/user/Project_Anode_Fit/Claude/results/comp_v24"
QGR, QSI = 372.0, 3579.0
def fSi_exp(theo): return None if theo is None else round(((theo-QGR)/(QSI-QGR))*QSI/theo, 3)

# (label, file, theo, NG, NS, window)  NG=흑연전이수 NS=Si전이수
CELLS = [
 ("Gr_c1(4ccc47)","gr_pocv_4ccc47.parquet",372,4,0,(0.05,0.30)),
 ("Gr_c2(1d5628)","gr_pocv_1d5628.parquet",372,4,0,(0.05,0.30)),
 ("Si_c1","si_c1_pocv.parquet",3579,0,3,(0.05,0.60)),
 ("Si_c2","si_c2_pocv.parquet",3579,0,3,(0.05,0.60)),
 ("SiGr1_lowSi_c1","sigr_aq1_pocv.parquet",510,4,2,(0.05,0.60)),
 ("SiGr1_lowSi_c2","sigr1_c2_pocv.parquet",510,4,2,(0.05,0.60)),
 ("SiGr2_highSi_c1","sigr_aq2_pocv.parquet",1150,4,2,(0.05,0.60)),
 ("SiGr2_highSi_c2","sigr2_c2_pocv.parquet",1150,4,2,(0.05,0.60)),
 ("SiGr3_B_c1","sigr3B_c1_pocv.parquet",900,4,2,(0.05,0.60)),
 ("SiGr3_B_c2","sigr3B_c2_pocv.parquet",900,4,2,(0.05,0.60)),
]

s = importlib.util.spec_from_file_location("af","/home/user/Project_Anode_Fit/Claude/docs/v1.0.23/Anode_Fit_v1.0.23.py")
af = importlib.util.module_from_spec(s); s.loader.exec_module(af)
GR = af.GraphiteAnodeDischargeDQDV
Ug0=[0.104,0.1415,0.227,0.140]; wg0=[0.0008,0.0009,0.0016,0.018]  # V2 흑연 피팅 초기값

def longest(mask):
    idx=np.where(mask)[0]
    if len(idx)==0: return None
    return max(np.split(idx,np.where(np.diff(idx)>1)[0]+1),key=len)

def dqdv(path,win_mV=6.0,dV=0.0005):
    d=pd.read_parquet(os.path.join(SC,path))
    I=d['Current / A'].to_numpy(); V=d['Voltage / V'].to_numpy()
    Q=d['Cumulative Capacity / Ah'].to_numpy()*1000.0
    seg=longest((np.abs(I)>1e-9)&(I>0))          # 탈리튬화
    Vs=V[seg]; Qs=Q[seg]-Q[seg][0]
    o=np.argsort(Vs); Vs,Qs=Vs[o],Qs[o]
    Vu,inv=np.unique(np.round(Vs,6),return_inverse=True)
    Qu=np.array([Qs[inv==k].mean() for k in range(len(Vu))])
    grid=np.arange(Vu.min(),Vu.max(),dV); Qg=np.interp(grid,Vu,Qu)
    win=int(round(win_mV/1000/dV)); win+=(win%2==0); win=max(win,5)
    return grid, np.abs(savgol_filter(Qg,win,3,deriv=1,delta=dV))

def make_model(NG,NS):
    def f(V,*p):
        i=0; gr=[]; si=[]
        for _ in range(NG):
            gr.append({'U':p[i],'w':p[i+1],'Q':p[i+2]}); i+=3
        for _ in range(NS):
            si.append({'U':p[i],'w':p[i+1],'Q':p[i+2]}); i+=3
        Cbg=p[i]
        Va=np.asarray(V,float); out=np.zeros_like(Va)
        if gr: out=out+np.asarray(GR(gr,Cbg=float(Cbg)).equilibrium(Va,298.15),float)
        else:  out=out+float(Cbg)
        if si: out=out+np.asarray(GR(si,Cbg=0.0).equilibrium(Va,298.15),float)
        return out
    return f

def fit_one(label,path,theo,NG,NS,win):
    LO,HI=win
    gV,gd=dqdv(path); m=(gV>=LO)&(gV<=HI); Vx,Dx=gV[m],gd[m]
    area=float(_trapz(Dx,Vx))
    p0=[]; lob=[]; hib=[]
    for j in range(NG):
        p0+=[Ug0[j],wg0[j],0.2*area]; lob+=[0.05,0.0008,1e-6]; hib+=[0.30,0.060,10*area]
    si_init=[(0.30,0.05),(0.45,0.05),(0.20,0.05)]
    for j in range(NS):
        u,w=si_init[j]; p0+=[u,w,0.3*area]; lob+=[0.15,0.01,1e-6]; hib+=[0.58,0.30,10*area]
    p0+=[max(Dx.min(),1e-6)]; lob+=[0.0]; hib+=[max(Dx)]
    try:
        popt,_=curve_fit(make_model(NG,NS),Vx,Dx,p0=p0,bounds=(lob,hib),maxfev=600000)
    except Exception as e:
        return {"label":label,"error":str(e)[:80]}, (Vx,Dx,None,NG,NS,None)
    pred=make_model(NG,NS)(Vx,*popt)
    r2=1.0-np.sum((Dx-pred)**2)/np.sum((Dx-Dx.mean())**2)
    i=0; Ug=[];wg=[];Qg=[];Us=[];ws=[];Qs=[]
    for _ in range(NG): Ug.append(popt[i]);wg.append(popt[i+1]);Qg.append(popt[i+2]);i+=3
    for _ in range(NS): Us.append(popt[i]);ws.append(popt[i+1]);Qs.append(popt[i+2]);i+=3
    Qgr=float(np.sum(Qg)); Qsi=float(np.sum(Qs)); tot=Qgr+Qsi
    res={"label":label,"theo":theo,"R2":round(float(r2),4),
         "U_gr":sorted([round(float(x),4) for x in Ug]) if NG else [],
         "w_gr_mV":[round(float(x)*1000,2) for x in wg] if NG else [],
         "U_si":sorted([round(float(x),4) for x in Us]) if NS else [],
         "w_si_mV":[round(float(x)*1000,1) for x in ws] if NS else [],
         "f_Si_fit":round(Qsi/tot,3) if tot>0 else None,"f_Si_exp":fSi_exp(theo) if (NG and NS) else (1.0 if NG==0 else 0.0)}
    return res,(Vx,Dx,popt,NG,NS,win)

results=[]; panels=[]
for c in CELLS:
    r,pk=fit_one(*c); results.append(r); panels.append((r["label"],pk))
    print(json.dumps(r,ensure_ascii=False))

# ---- 종합 그림: 조성별 대표셀(각 c1) real + 고해상 모델 + 성분 ----
reps=[p for p in panels if p[0].endswith("c1") or p[0].startswith("Gr_c1") or "c1(" in p[0]]
reps=[panels[i] for i in [0,2,4,6,8]]  # Gr,Si,SiGr1,SiGr2,SiGr3 대표
fig,axes=plt.subplots(len(reps),1,figsize=(11,3.8*len(reps)))
for ax,(label,(Vx,Dx,popt,NG,NS,win)) in zip(axes,reps):
    ax.plot(Vx,Dx,color='tab:blue',lw=1.5,label='real delith')
    if popt is not None:
        LO,HI=win; Vm=np.arange(LO,HI,0.00002)   # 고해상 0.02mV → 매끄러움
        pred=make_model(NG,NS)(Vm,*popt)
        ax.plot(Vm,pred,'--',color='k',lw=1.4,label='doc model FIT (fine grid)')
        i=0; gr=[];si=[]
        for _ in range(NG): gr.append({'U':popt[i],'w':popt[i+1],'Q':popt[i+2]});i+=3
        for _ in range(NS): si.append({'U':popt[i],'w':popt[i+1],'Q':popt[i+2]});i+=3
        Cbg=popt[i]
        if gr: ax.plot(Vm,np.asarray(GR(gr,Cbg=float(Cbg)).equilibrium(Vm,298.15),float),':',color='tab:green',lw=1.1,label='├ graphite host')
        if si: ax.plot(Vm,np.asarray(GR(si,Cbg=0.0).equilibrium(Vm,298.15),float),':',color='tab:red',lw=1.1,label='└ Si host')
        r2=[r for r in results if r["label"]==label][0]["R2"]
        ax.set_title(f'{label}  (R²={r2})',fontsize=10)
    ax.set_xlabel('V'); ax.set_ylabel('dQ/dV'); ax.legend(fontsize=7); ax.grid(alpha=.3); ax.set_xlim(win[0],win[1])
fig.tight_layout()
fig.savefig(f"{OUT}/multi_fit.png",dpi=120); print("saved",f"{OUT}/multi_fit.png")
json.dump(results,open(f"{OUT}/multi_fit_result.json","w"),ensure_ascii=False,indent=2)
print("saved",f"{OUT}/multi_fit_result.json")
