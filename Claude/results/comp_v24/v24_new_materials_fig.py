# -*- coding: utf-8 -*-
"""신규 소재 시각화: (1) LCO 첫 실피팅(PyBaMM Marquis2019=Doyle/Garcia Dualfoil 반쪽셀).
(2) 흑연 7소재(SINTEF 2 + OCP 5) dQ/dV 중첩 — 소재간 스테이징 위치·폭 변이."""
import numpy as np, pandas as pd, importlib.util, os, sys, warnings; warnings.filterwarnings("ignore")
sys.path.insert(0,"/home/user/Project_Anode_Fit/Claude/results/comp_v24"); import bdd_smoothing as bdd
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
SC="/tmp/claude-0/-home-user-Project-Anode-Fit/e8d4cdbc-60e6-548e-b742-1446b8f7a8bd/scratchpad"
OUT="/home/user/Project_Anode_Fit/Claude/results/comp_v24"; _trapz=getattr(np,'trapezoid',getattr(np,'trapz',None))
af_s=importlib.util.spec_from_file_location("af","/home/user/Project_Anode_Fit/Claude/docs/v1.0.23/Anode_Fit_v1.0.23.py")
af=importlib.util.module_from_spec(af_s); af_s.loader.exec_module(af); GR=af.GraphiteAnodeDischargeDQDV; LCO=af.LCOCathodeDQDV

def load_ocp(path):
    rows=[]
    for ln in open(path):
        ln=ln.strip()
        if not ln or ln[0]=='#': continue
        p=ln.replace(',',' ').split()
        try: rows.append((float(p[0]),float(p[1])))
        except: pass
    a=np.array(rows); x,V=a[:,0],a[:,1]; o=np.argsort(V); return V[o],x[o]*100
def load_parq(f):
    d=pd.read_parquet(f"{SC}/zenodo_gr/{f}"); I=d['Current / A'].to_numpy(); V=d['Voltage / V'].to_numpy(); Q=d['Cumulative Capacity / Ah'].to_numpy()*1000
    idx=np.where((np.abs(I)>1e-9)&(I>0))[0]; seg=max(np.split(idx,np.where(np.diff(idx)>1)[0]+1),key=len)
    return V[seg],Q[seg]-Q[seg][0]

fig,ax=plt.subplots(1,2,figsize=(15,5.6))
# --- (1) LCO 첫 피팅 ---
V,Q=load_ocp(f"{SC}/ocp/lco_Marquis2019.csv"); gx,gy=bdd.dqdv_grid_bdd(V,Q,dV=0.001)
LO,HI=3.60,4.30; m=(gx>=LO)&(gx<=HI); Vx,Dx=gx[m],gy[m]; area=float(_trapz(Dx,Vx))
def modelC(V,*p):
    trs=[{'U':p[3*j],'w':p[3*j+1],'Q':p[3*j+2]} for j in range(4)]
    return np.asarray(LCO(trs,Cbg=float(p[12])).equilibrium(np.asarray(V,float),298.15),float)
p0=[];lo=[];hi=[]
for u in [3.68,3.90,3.98,4.15]: p0+=[u,0.03,0.25*area];lo+=[LO,0.005,1e-6];hi+=[HI,0.20,10*area]
p0+=[max(Dx.min(),1e-6)];lo+=[0];hi+=[max(Dx)]
pc,_=curve_fit(modelC,Vx,Dx,p0=p0,bounds=(lo,hi),maxfev=400000); pr=modelC(Vx,*pc)
r2=1-np.sum((Dx-pr)**2)/np.sum((Dx-Dx.mean())**2)
ax[0].plot(Vx,Dx,color='tab:purple',lw=1.6,label='LCO real (Dualfoil 반쪽셀)')
Vm=np.arange(LO,HI,0.0002); ax[0].plot(Vm,modelC(Vm,*pc),'--',color='k',lw=1.4,label=f'문건 양극 FIT (R²={r2:.3f})')
ax[0].set_xlabel('V vs Li'); ax[0].set_ylabel('dQ/dV(|dx/dV|·100)'); ax[0].set_title('★ LCO 첫 실피팅 (PyBaMM Marquis2019)'); ax[0].legend(fontsize=8); ax[0].grid(alpha=.3)

# --- (2) 흑연 7소재 중첩(각자 최대 정규화) ---
mats=[("SINTEF_4ccc47","parq","gr_pocv_4ccc47.parquet"),("SINTEF_1d5628","parq","gr_pocv_1d5628.parquet"),
      ("Ecker2015","ocp","gr_Ecker2015.csv"),("Enertech","ocp","gr_Enertech_Ai2020.csv"),
      ("Chen2020","ocp","gr_Chen2020_LGM50.csv"),("PyBEP_xcrp","ocp","gr_PyBEP_xcrp2020.txt"),("PyBEP_srep","ocp","gr_PyBEP_srep2016.txt")]
cmap=plt.cm.turbo(np.linspace(0.05,0.95,len(mats)))
for (nm,typ,f),c in zip(mats,cmap):
    V,Q=(load_parq(f) if typ=="parq" else load_ocp(f"{SC}/ocp/{f}"))
    gx,gy=bdd.dqdv_grid_bdd(V,Q,dV=0.0005); m=(gx>=0.05)&(gx<=0.25)
    yy=gy[m]/np.nanmax(gy[m]) if np.nanmax(gy[m])>0 else gy[m]
    ax[1].plot(gx[m],yy,color=c,lw=1.3,label=nm,alpha=.85)
ax[1].set_xlabel('V vs Li'); ax[1].set_ylabel('dQ/dV (각자 정규화)'); ax[1].set_title('흑연 7소재 스테이징 dQ/dV (소재간 위치·폭 변이)'); ax[1].legend(fontsize=7); ax[1].grid(alpha=.3)
fig.tight_layout(); fig.savefig(f"{OUT}/new_materials.png",dpi=120); print("saved new_materials.png  LCO R²=",round(r2,3))
print("LCO U_fit:",[round(pc[3*j],3) for j in range(4)],"w(mV):",[round(pc[3*j+1]*1000,1) for j in range(4)])
