# -*- coding: utf-8 -*-
"""v1.0.24 V3-정량 — 유한율속 정량 검증(M제거 유한율속 절반 완결).
출하 dqdv()(분극 V_n=V_app−|I|Rn + 지연 L_V) 가 단일 (Rn, k: L_V=k·|I|)로 율속 시리즈를 재현하나.
절차: ①1mA(near-eq)서 평형(U,w,Q,Cbg) 피팅 → ②2mA서 (Rn,k) 피팅 → ③5mA 예측(전이성 검증).
데이터: Zenodo 20323533 DLR 흑연-SiOx 음극 delith 율속. ⚠상용 harvested(비옴 농도분극 잔차 예상).
"""
import numpy as np, pandas as pd, importlib.util, sys, warnings; warnings.filterwarnings("ignore")
sys.path.insert(0,"/home/user/Project_Anode_Fit/Claude/results/comp_v24"); import bdd_smoothing as bdd
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from scipy.optimize import curve_fit, least_squares
DLR="/tmp/claude-0/-home-user-Project-Anode-Fit/e8d4cdbc-60e6-548e-b742-1446b8f7a8bd/scratchpad/dlr/rate_delith.csv"
OUT="/home/user/Project_Anode_Fit/Claude/results/comp_v24"
af_s=importlib.util.spec_from_file_location("af","/home/user/Project_Anode_Fit/Claude/docs/v1.0.23/Anode_Fit_v1.0.23.py")
af=importlib.util.module_from_spec(af_s); af_s.loader.exec_module(af); GR=af.GraphiteAnodeDischargeDQDV

d=pd.read_csv(DLR,encoding='latin-1'); d.columns=[c.strip() for c in d.columns]
I=d['Current / A'].to_numpy(); V=d['Voltage / V'].to_numpy(); Q=d['Capacity/ Ah'].to_numpy()*1000
idx=np.where((np.abs(I)>1e-9)&(I>0))[0]; segs=[s for s in np.split(idx,np.where(np.diff(idx)>1)[0]+1) if len(s)>500]
seen={}; rate={}
for s in segs:
    k=round(float(np.median(np.abs(I[s])))*1000,1)
    if k not in seen: seen[k]=1; rate[k]=s
Qcell=float(np.max(Q[rate[min(rate)]]))/1000.0*1.0   # 대략 delith 용량[Ah]
def dqdv_rate(k_mA):
    s=rate[k_mA]; gx,gy=bdd.dqdv_grid_bdd(V[s],Q[s]-Q[s][0],dV=0.0005,denoise_deriv=0.4)
    m=(gx>=0.06)&(gx<=0.26); return gx[m],gy[m]
Vlo,Dlo=dqdv_rate(1.0); V2,D2=dqdv_rate(2.0); V5,D5=dqdv_rate(5.1)
Iabs={1.0:1.018e-3,2.0:2.035e-3,5.1:5.088e-3}

# ① 평형 피팅(1mA near-eq) — 2 흑연피크 + Cbg
NT=2; U0=[0.111,0.152]
def eqmodel(V,*p):
    trs=[{'U':p[3*j],'w':p[3*j+1],'Q':p[3*j+2]} for j in range(NT)]
    return np.asarray(GR(trs,Cbg=float(p[-1])).equilibrium(np.asarray(V,float),298.15),float)
p0=[0.111,0.003,0.3,0.152,0.003,0.2,5]; lo=[0.08,0.001,1e-3,0.13,0.001,1e-3,0]; hi=[0.13,0.03,50,0.18,0.03,50,50]
pe,_=curve_fit(eqmodel,Vlo,Dlo,p0=p0,bounds=(lo,hi),maxfev=200000)
eq_trs=[{'U':pe[3*j],'w':pe[3*j+1],'Q':pe[3*j+2]} for j in range(NT)]; Cbg=pe[-1]
print("평형(1mA) U:",[round(pe[3*j],3) for j in range(NT)],"w(mV):",[round(pe[3*j+1]*1000,2) for j in range(NT)])

# 유한율속 모델: 평형 고정 + (Rn,k) → dqdv()
def rate_pred(Vx, I_A, Rn, kLV):
    trs=[dict(t, L_V=max(kLV*I_A,1e-6)) for t in eq_trs]
    g=GR(trs, Rn=Rn, Cbg=Cbg)
    return np.asarray(g.dqdv(np.asarray(Vx,float), T=298.15, I_abs=I_A, Q_cell=max(Qcell,1e-3), s=+1),float)
# ②③ (Rn,k) 를 율속별 독립 피팅 → k(L_V/|I|) 일관성 = L_V∝|I| 검증(분극 모델과 분리)
def fit_rate(Vx,Dx,I_A):
    def resid(par): return rate_pred(Vx,I_A,par[0],par[1])-Dx
    s=least_squares(resid,[20.0,5.0],bounds=([0,0],[300,800]),max_nfev=6000)
    pr=rate_pred(Vx,I_A,s.x[0],s.x[1]); r2=1-np.sum((Dx-pr)**2)/np.sum((Dx-Dx.mean())**2)
    return s.x[0],s.x[1],pr,r2
Rn2,k2,pred2,r2_2=fit_rate(V2,D2,Iabs[2.0])
Rn5,k5,pred5,r2_5=fit_rate(V5,D5,Iabs[5.1])
predlo=eqmodel(Vlo,*pe)   # 1mA 패널 = 순수 평형(Rn=0) — 실측 1mA와 일치 확인
print(f"2mA 독립피팅: Rn_eff={Rn2:.1f}Ω  k(L_V/I)={k2:.1f} V/A  R²={r2_2:.3f}")
print(f"5mA 독립피팅: Rn_eff={Rn5:.1f}Ω  k(L_V/I)={k5:.1f} V/A  R²={r2_5:.3f}")
print(f"→ Rn_eff 율속 증가(비옴 농도분극 신호): {Rn2:.0f}→{Rn5:.0f}Ω  |  k(L_V/I) 일관성: {k2:.1f} vs {k5:.1f}")

fig,ax=plt.subplots(1,3,figsize=(16,4.8))
panels=[(Vlo,Dlo,predlo,'1mA: 순수 평형 vs real(일치)',None),
        (V2,D2,pred2,f'2mA 독립FIT Rn={Rn2:.0f}Ω,k={k2:.0f}',r2_2),
        (V5,D5,pred5,f'5mA 독립FIT Rn={Rn5:.0f}Ω,k={k5:.0f}',r2_5)]
for a,(Vx,Dx,pr,lab,r2) in zip(ax,panels):
    a.plot(Vx,Dx,color='tab:blue',lw=1.5,label='real (BDD)')
    a.plot(Vx,pr,'--',color='k',lw=1.4,label='doc'+(f' R²={r2:.3f}' if r2 is not None else ' 평형'))
    a.set_xlabel('V'); a.set_ylabel('dQ/dV'); a.set_title(lab,fontsize=9); a.legend(fontsize=8); a.grid(alpha=.3)
fig.tight_layout(); fig.savefig(f"{OUT}/rate_quant.png",dpi=120); print("saved rate_quant.png")
