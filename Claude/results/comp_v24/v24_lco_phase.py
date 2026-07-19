# -*- coding: utf-8 -*-
"""v1.0.24 B(LCO) — LCO 상 성격 판정 + O3 소스 교차검증. 문건·코드 무수정.
데이터 현실(에이전트 확인): 실측 O3-LCO 공개 numeric 부재. 가용:
  - 실측(digitized) O2-LCO OCV: Carlier/Delmas 2002 JES 149 A1310 (DOI 10.1149/1.1503075) — 폴리타입 O2(주의).
  - 해석 O3: PyBaMM Ramadass2004 OCP + Marquis2019(현 프록시) — 독립 2소스 교차검증용.
판정: (1)실측 O2 dQ/dV 로 LCO feature 폭/(RT/F) → 두-상(sharp) vs order-disorder(broad).
      (2)해석 O3 2소스(Marquis·Ramadass) feature 위치 교차검증(소스간 일관?).
정직: O3 결론은 해석fit 기반(실측 O3 numeric 부재) — 그림 디지타이즈만이 실 O3 경로.
"""
import numpy as np, pandas as pd, sys, json, warnings; warnings.filterwarnings("ignore")
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
plt.rcParams['font.family']='NanumGothic'; plt.rcParams['axes.unicode_minus']=False
from scipy.optimize import curve_fit, brentq
from scipy.signal import find_peaks
SC="/tmp/claude-0/-home-user-Project-Anode-Fit/e8d4cdbc-60e6-548e-b742-1446b8f7a8bd/scratchpad"
LD="/home/user/Project_Anode_Fit/Claude/results/comp_v24/lco_data"; OUT="/home/user/Project_Anode_Fit/Claude/results/comp_v24"
R,F,T=8.314,96485.0,298.15; RTF=R*T/F; RTFmv=RTF*1000; _trapz=getattr(np,'trapezoid',getattr(np,'trapz',None))

def ocv_to_dqdv(x,V,vlo,vhi,npts=600):
    o=np.argsort(V); V=np.asarray(V)[o]; x=np.asarray(x)[o]
    Vu,iu=np.unique(V,return_index=True); xu=x[iu]
    Vg=np.linspace(max(vlo,Vu.min()),min(vhi,Vu.max()),npts); xi=np.interp(Vg,Vu,xu)
    d=np.abs(np.gradient(xi,Vg)); return Vg,d
def load_xy(path):
    a=np.loadtxt(path,delimiter=',',skiprows=1); return a[:,0],a[:,1]
def fwhm(V,d,i):  # 피크 i 반치폭(mV)
    h=d[i]/2; l=i
    while l>0 and d[l]>h: l-=1
    r=i
    while r<len(d)-1 and d[r]>h: r+=1
    return (V[r]-V[l])*1000

# ===== (1) 실측 O2-LCO (Carlier 2002) =====
xO2,VO2=load_xy(f"{LD}/diffthermo_LCO_O2_OCV_Carlier2002JES_Fig4a_digitized.csv")
Vg,d=ocv_to_dqdv(xO2,VO2,3.2,4.5)
d=d/np.nanmax(d)  # 형상(정규화)
pk,_=find_peaks(d,height=0.10,prominence=0.05)
feats=[(round(Vg[i],3),round(fwhm(Vg,d,i),1),round(fwhm(Vg,d,i)/RTFmv,2)) for i in pk]
print("=== (1) 실측 O2-LCO (Carlier/Delmas 2002, digitized) dQ/dV feature ===")
print(f"  피크(V, FWHM mV, 폭/(RT/F)): {feats}")
print(f"  판정: 폭/(RT/F)≪1 ⇒ 두-상 sharp / ≳1 ⇒ order-disorder·고용체 broad")
twophase=[f for f in feats if f[2]<0.6]; broad=[f for f in feats if f[2]>=0.6]
print(f"  → 두-상(sharp) feature: {twophase}")
print(f"  → 고용체/order-disorder(broad) feature: {broad}")

# ===== (2) O3 해석 2소스 교차검증 (Marquis vs Ramadass) =====
xM,VM=load_xy(f"{SC}/ocp/lco_Marquis2019.csv")            # O3 프록시(현재)
xR,VR=load_xy(f"{LD}/pybamm_LCO_O3_OCP_Ramadass2004_ANALYTIC.csv")  # O3 독립 해석
VgM,dM=ocv_to_dqdv(xM,VM,3.5,4.3); dM=dM/np.nanmax(dM)
VgR,dR=ocv_to_dqdv(xR,VR,3.5,4.3); dR=dR/np.nanmax(dR)
def toppk(V,d):
    pk,_=find_peaks(d,height=0.2,prominence=0.1); return sorted(round(V[i],3) for i in pk)
pkM=toppk(VgM,dM); pkR=toppk(VgR,dR)
print("=== (2) O3 해석 2소스 feature 위치 교차검증 ===")
print(f"  Marquis2019(현프록시) 피크V={pkM}")
print(f"  Ramadass2004(독립)   피크V={pkR}")
print(f"  → 독립 2 해석소스가 같은 위치 지목하면 O3 구조 신뢰↑(단 둘 다 해석fit — 실측 아님)")

print("=== [정직 데이터 현실] ===")
print("  실측 O3-LCO 공개 numeric 부재(LiionDB DNS死·Zenodo/CAMP LCO 결여·Reynier/Hudak 그림전용).")
print("  실측 가용=O2-LCO(Carlier, 폴리타입 상이). O3=해석fit(Marquis·Ramadass·Moura dU/dT)만.")
print("  → LCO 실 O3 검증은 그림 디지타이즈(Reynier2004 dU/dT·Hudak2014 OCV) 만이 경로. 조작 금지 준수.")

fig,ax=plt.subplots(1,2,figsize=(14,5.2))
ax[0].plot(Vg,d,'k',lw=1.5,label='실측 O2-LCO(Carlier2002)')
for i in pk: ax[0].axvline(Vg[i],color='tab:red',ls=':',lw=.8); ax[0].annotate(f'{fwhm(Vg,d,i)/RTFmv:.1f}·RT/F',(Vg[i],d[i]),fontsize=7,color='tab:red')
ax[0].set_xlabel('V vs Li'); ax[0].set_ylabel('dQ/dV(정규화)'); ax[0].set_title('(1) 실측 O2-LCO dQ/dV — feature 폭 판정\n(폭/(RT/F): ≪1 두-상 / ≳1 order-disorder)'); ax[0].legend(fontsize=8); ax[0].grid(alpha=.3)
ax[1].plot(VgM,dM,lw=1.4,color='tab:blue',label=f'O3 Marquis2019(현프록시) pk={pkM}')
ax[1].plot(VgR,dR,lw=1.4,color='tab:green',ls='--',label=f'O3 Ramadass2004(독립) pk={pkR}')
ax[1].set_xlabel('V vs Li'); ax[1].set_ylabel('dQ/dV(정규화)'); ax[1].set_title('(2) O3 해석 2소스 교차검증\n(실측 O3 numeric 부재 — 둘 다 해석fit)'); ax[1].legend(fontsize=8); ax[1].grid(alpha=.3)
fig.tight_layout(); fig.savefig(f"{OUT}/lco_phase.png",dpi=120); print("saved lco_phase.png")
json.dump({"O2_real_features_V_FWHMmV_ratio":feats,"O3_Marquis_peaks":pkM,"O3_Ramadass_peaks":pkR,
           "data_reality":"real O3-LCO numeric unavailable; O2 real (Carlier) + O3 analytic (Marquis/Ramadass) only"},
          open(f"{OUT}/lco_phase_result.json","w"),indent=1,default=float)
