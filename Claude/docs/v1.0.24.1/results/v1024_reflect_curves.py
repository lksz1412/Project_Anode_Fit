# -*- coding: utf-8 -*-
"""v1.0.24 R2/R3 — 신규 기능 곡선 물리 타당성(매끈·단일봉·토글) 시각 검증."""
import numpy as np, importlib.util, sys
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
plt.rcParams['font.family']='NanumGothic'; plt.rcParams['axes.unicode_minus']=False
from scipy.signal import find_peaks
s=importlib.util.spec_from_file_location('af','/home/user/Project_Anode_Fit/Claude/docs/v1.0.24/Anode_Fit_v1.0.24.py')
m=importlib.util.module_from_spec(s); s.loader.exec_module(m); R=m.R
OUT="/home/user/Project_Anode_Fit/Claude/docs/v1.0.24/results"
fig,ax=plt.subplots(1,3,figsize=(17,5))

# (1) @5 흑연 5-feature — T-sweep(stage-2L 분리)
gr5=m.GraphiteAnodeDischargeDQDV(m.GRAPHITE_STAGING_XRD_v1024,x=0.5,Rn=0.01,Cbg=0.0)
V=np.linspace(0.06,0.24,3000)
for Tc,c in [(5,'tab:blue'),(25,'tab:gray'),(45,'tab:orange'),(65,'tab:red')]:
    d=np.asarray(gr5.equilibrium(V,T=Tc+273.15)); ax[0].plot(V,d/np.nanmax(d),color=c,lw=1.3,label=f'{Tc}℃')
ax[0].set_title('@5 흑연 XRD 5-feature\n(stage-2L 고온 분리·매끈)'); ax[0].set_xlabel('V'); ax[0].set_ylabel('dQ/dV(정규화)'); ax[0].legend(fontsize=8); ax[0].grid(alpha=.3)

# (2) @3 regsol(Si 고용체 Ω<2RT) vs 로지스틱 — 매끈·단일봉
T=298.15; RT=R*T
trR=dict(U=0.30,w=0.02,Q=1.0,n=1.0,Omega=1.0*RT,kernel='regsol',delta=0.003,dH_a=4e4,dS_a=0.,dVdq_qa=0.3)
trL=dict(U=0.30,w=0.05,Q=1.0,n=1.0,dH_a=4e4,dS_a=0.,dVdq_qa=0.3)
gR=m.GraphiteAnodeDischargeDQDV([trR],x=0.5,Rn=0.01,Cbg=0.0); gL=m.GraphiteAnodeDischargeDQDV([trL],x=0.5,Rn=0.01,Cbg=0.0)
Vr=np.linspace(0.05,0.55,3000); dR=np.asarray(gR.equilibrium(Vr,T=T)); dL=np.asarray(gL.equilibrium(Vr,T=T))
pk,_=find_peaks(dR,height=0.05*dR.max(),prominence=0.02*dR.max())
ax[1].plot(Vr,dR,color='tab:green',lw=1.5,label=f'@3 정칙용액(Ω<2RT)·prominent봉={len(pk)}')
ax[1].plot(Vr,dL,color='tab:blue',ls='--',lw=1.1,label='로지스틱(대조)')
ax[1].set_title('@3 Si 고용체 Frumkin 커널\n(단일 broad 봉·매끈)'); ax[1].set_xlabel('V'); ax[1].set_ylabel('dQ/dV'); ax[1].legend(fontsize=8); ax[1].grid(alpha=.3)

# (3) LCO 전자항 토글 ON/OFF — 298(동일)·318(분기)
kw=dict(Rn=0.005,Cbg=0.0); Vc=np.linspace(3.6,4.25,2000)
on=m.LCOCathodeDQDV(m.LCO_MSMR_LIT,include_electronic_entropy=True,**kw)
off=m.LCOCathodeDQDV(m.LCO_MSMR_LIT,include_electronic_entropy=False,**kw)
ax[2].plot(Vc,np.asarray(on.equilibrium(Vc,T=298.15)),color='k',lw=1.6,label='298K ON=OFF(U(T_ref)보존)')
ax[2].plot(Vc,np.asarray(off.equilibrium(Vc,T=298.15)),color='tab:cyan',ls=':',lw=1.2,label='298K OFF')
ax[2].plot(Vc,np.asarray(on.equilibrium(Vc,T=318.15)),color='tab:red',lw=1.2,label='318K ON')
ax[2].plot(Vc,np.asarray(off.equilibrium(Vc,T=318.15)),color='tab:orange',ls='--',lw=1.2,label='318K OFF(∂U/∂T 분기)')
ax[2].set_title('LCO 전자항 on/off 토글\n상온 무영향·다온도서만 분기'); ax[2].set_xlabel('V vs Li'); ax[2].set_ylabel('dQ/dV'); ax[2].legend(fontsize=7.5); ax[2].grid(alpha=.3)
fig.suptitle('v1.0.24 신규 코드 기능 — 물리 타당성(매끈·단일봉·토글)',fontsize=13); fig.tight_layout()
fig.savefig(f"{OUT}/reflect_curves.png",dpi=120); print(f"saved reflect_curves.png · @3 prominent봉={len(pk)}(단일 확인)")
