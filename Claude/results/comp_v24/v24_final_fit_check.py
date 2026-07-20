# -*- coding: utf-8 -*-
"""v1.0.24 최종 코드 — 공개 실측 데이터셋 피팅 재현 검증.
   흑연 Chen2020(LG M50 공표 OCP) + LCO Ramadass2004 O3(리포) + LCO Carlier2002 O2(리포·디지타이즈).
   모델 = 출하 equilibrium() 자유폭 MSMR({U,w,Q}). dQ/dV 추출 = BDD 스무딩. 피팅 = curve_fit. R²·오버레이."""
import numpy as np, importlib.util, os
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
plt.rcParams['font.family']='NanumGothic'; plt.rcParams['axes.unicode_minus']=False
from scipy.optimize import curve_fit
_trapz=getattr(np,'trapezoid',None) or getattr(np,'trapz',None)

ROOT="/home/user/Project_Anode_Fit/Claude"
DOC=f"{ROOT}/docs/v1.0.24"; CV=f"{ROOT}/results/comp_v24"
def load(name,path):
    s=importlib.util.spec_from_file_location(name,path); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
m=load("af",f"{DOC}/Anode_Fit_v1.0.24.py")            # ★최종 v1.0.24 (main)
bdd=load("bdd",f"{CV}/bdd_smoothing.py")
GR=m.GraphiteAnodeDischargeDQDV; LCO=m.LCOCathodeDQDV

# ---- Chen2020 LG M50 흑연 음극 OCP (공표식 — PyBaMM 표준·peer-reviewed 실측 fit) ----
def chen2020_gr_ocp(sto):
    return (1.9793*np.exp(-39.3631*sto)+0.2482
            -0.0909*np.tanh(29.8538*(sto-0.1234))
            -0.04478*np.tanh(14.9159*(sto-0.2769))
            -0.0205*np.tanh(30.4444*(sto-0.6103)))

def load_xy(path):
    a=np.genfromtxt(path,delimiter=',',names=None,skip_header=1)
    a=np.atleast_2d(a); x=a[:,0].astype(float); V=a[:,1].astype(float)
    o=np.argsort(V); return V[o], x[o]           # V 오름차순

def data_dqdv(V, x, win, dvv):
    Q=x*100.0                                     # Q ∝ x (스케일은 Q_j 피팅 흡수)
    gx,gy=bdd.dqdv_grid_bdd(V,Q,dV=dvv)
    gy=np.abs(gy)                                 # ICA 크기(부호 무관)
    mk=(gx>=win[0])&(gx<=win[1]); return gx[mk], gy[mk]

def make_model(N, role):
    cls=LCO if role=="cathode" else GR
    def f(V,*p):
        tr=[]; i=0
        for _ in range(N): tr.append({'U':p[i],'w':p[i+1],'Q':p[i+2]}); i+=3
        Cbg=p[i]; return np.asarray(cls(tr,Cbg=float(Cbg)).equilibrium(np.asarray(V,float),298.15),float)
    return f

def fit_one(V,x,win,role,U0,w0,dvv,Ubound):
    Vx,Dx=data_dqdv(V,x,win,dvv)
    if len(Vx)<15: return None
    area=float(_trapz(Dx,Vx)); N=len(U0); p0=[]; lo=[]; hi=[]
    for j in range(N):
        p0+=[U0[j],w0[j],0.25*area]; lo+=[Ubound[0],0.0008,1e-6]; hi+=[Ubound[1],0.30,10*area]
    p0+=[max(Dx.min(),1e-6)]; lo+=[0.0]; hi+=[max(Dx)+1e-9]
    popt,_=curve_fit(make_model(N,role),Vx,Dx,p0=p0,bounds=(lo,hi),maxfev=400000)
    pred=make_model(N,role)(Vx,*popt)
    r2=1.0-np.sum((Dx-pred)**2)/np.sum((Dx-Dx.mean())**2)
    return dict(Vx=Vx,Dx=Dx,pred=pred,r2=float(r2),popt=popt,N=N,npts=len(Vx),dens=round(len(Vx)/((win[1]-win[0])*1000),2))

# ---- 데이터셋 3종 ----
# 1) 흑연 Chen2020
sto=np.linspace(0.006,0.99,600); Vg=chen2020_gr_ocp(sto)
r_gr=fit_one(Vg,sto,(0.05,0.30),"anode",
             U0=[0.088,0.120,0.142,0.210], w0=[0.004,0.006,0.016,0.006], dvv=0.0005, Ubound=(0.05,0.30))
# 2) LCO Ramadass O3 (리포 실측 OCP)
Vr,xr=load_xy(f"{CV}/lco_data/pybamm_LCO_O3_OCP_Ramadass2004_ANALYTIC.csv")
r_o3=fit_one(Vr,xr,(3.62,4.20),"cathode",
             U0=[3.90,3.95,4.10], w0=[0.03,0.05,0.05], dvv=0.001, Ubound=(3.6,4.25))
# 3) LCO Carlier O2 (리포 실측 디지타이즈)
Vc,xc=load_xy(f"{CV}/lco_data/diffthermo_LCO_O2_OCV_Carlier2002JES_Fig4a_digitized.csv")
r_o2=fit_one(Vc,xc,(3.85,4.55),"cathode",
             U0=[4.05,4.20,4.45], w0=[0.05,0.05,0.05], dvv=0.001, Ubound=(3.8,4.60))

# ---- 오버레이 그림 ----
fig,ax=plt.subplots(1,3,figsize=(18,5.4))
panels=[("(1) 흑연 반쪽셀 — Chen2020 LG M50 OCP\n(PyBaMM 표준 공표 실측 fit)", r_gr, 'V vs Li'),
        ("(2) LCO O3 반쪽셀 — Ramadass2004 OCP\n(리포 실측)", r_o3, 'V vs Li'),
        ("(3) LCO O2 — Carlier2002 JES Fig4a\n(리포 디지타이즈 실측)", r_o2, 'V vs Li')]
for a,(title,r,xl) in zip(ax,panels):
    if r is None: a.set_title(title+"\n[피팅 실패]"); continue
    a.plot(r['Vx'],r['Dx'],'o',ms=2.4,color='0.35',alpha=.6,label=f"데이터 dQ/dV (BDD, {r['npts']}점)")
    a.plot(r['Vx'],r['pred'],'-',color='tab:red',lw=2,label=f"모델 피팅 (전이 {r['N']}·R²={r['r2']:.4f})")
    a.set_title(title); a.set_xlabel(xl); a.set_ylabel('dQ/dV'); a.legend(fontsize=8.5); a.grid(alpha=.3)
fig.suptitle('v1.0.24 최종 코드 — 공개 실측 dQ/dV 피팅 재현 (흑연·LCO O3·LCO O2)',fontsize=14)
fig.tight_layout(); fig.savefig(f"{CV}/final_fit_check.png",dpi=120)

print("="*72)
for nm,r in [("흑연 Chen2020(LG M50 OCP)",r_gr),("LCO O3 Ramadass2004",r_o3),("LCO O2 Carlier2002",r_o2)]:
    if r: print(f"{nm:28s} R²={r['r2']:.4f}  전이={r['N']}  창내점={r['npts']}  밀도={r['dens']}/mV")
    else: print(f"{nm:28s} [피팅 실패]")
print("saved: final_fit_check.png")
