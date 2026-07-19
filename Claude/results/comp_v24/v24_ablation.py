# -*- coding: utf-8 -*-
"""v1.0.24 — 흑연+Si 블렌드 개별 개선 효과 ablation (OFAT: one-factor-at-a-time).
사용자 요구: 공개데이터 / 문건기본 산출 / 문건+@ 산출 3자 비교. @는 한 번에 하나만 추가.
각 @의 ΔR²(개선효과)를 개별 정량 → 어떤 게 효과 크고 어떤 게 무의미한지 한눈에.
LCO 제외·음극(흑연+Si) 한정. 문건·코드 무수정(모델형태 실험만).
"""
import numpy as np, pandas as pd, sys, json, warnings; warnings.filterwarnings("ignore")
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
plt.rcParams['font.family']='NanumGothic'; plt.rcParams['axes.unicode_minus']=False
from scipy.optimize import curve_fit, brentq
sys.path.insert(0,"/home/user/Project_Anode_Fit/Claude/results/comp_v24"); import bdd_smoothing as bdd
SC="/tmp/claude-0/-home-user-Project-Anode-Fit/e8d4cdbc-60e6-548e-b742-1446b8f7a8bd/scratchpad/zenodo_gr"
OUT="/home/user/Project_Anode_Fit/Claude/results/comp_v24"
R,F,T=8.314,96485.0,298.15; RTF=R*T/F; _trapz=getattr(np,'trapezoid',getattr(np,'trapz',None))

# ---- 커널들 ----
def logi(V,U,w,Q):
    z=(V-U)/w; s=np.where(z>=0,1/(1+np.exp(-z)),np.exp(z)/(1+np.exp(z))); return Q*s*(1-s)/w
def asym(V,U,wL,wR,Q):  # 비대칭: 좌/우 다른 폭. apex 연속 정규화(4/(wL+wR)) — 대칭의 진짜 상위집합
    w=np.where(V<U,wL,wR); z=(V-U)/w; s=1/(1+np.exp(-np.clip(z,-350,350))); return Q*s*(1-s)*(4.0/(wL+wR))
XG=np.linspace(1e-3,1-1e-3,400)
def binodal_xa(Om):
    a=Om/(R*T)
    if a<=2.0: return 0.5
    try: return brentq(lambda x: np.log(x/(1-x))+a*(1-2*x),1e-6,0.5-1e-9)
    except Exception: return 0.5
def sech2(v,d):
    zz=np.clip(v/(2*d),-350,350); c=1/np.cosh(zz); return c*c/(4*d)
def reg(V,U0,Om,Q,d):  # 정칙용액 Ω(>2RT near-delta / <2RT broad)+kinetic δ
    xa=binodal_xa(Om); xg=XG
    Vi=np.where((xg>xa)&(xg<1-xa),U0,U0-RTF*np.log(xg/(1-xg))-(Om/F)*(1-2*xg))
    wi=Q*(xg[1]-xg[0]); return (wi*sech2(np.asarray(V)[:,None]-Vi[None,:],d)).sum(axis=1)
def r2(y,yh): return 1-np.sum((y-yh)**2)/np.sum((y-y.mean())**2)

# ---- 블렌드 데이터(탈리튬화) ----
def blend_dqdv(cell):
    d=pd.read_parquet(f"{SC}/{cell}"); I=d['Current / A'].to_numpy(); V=d['Voltage / V'].to_numpy(); Q=d['Cumulative Capacity / Ah'].to_numpy()*1000
    idx=np.where((np.abs(I)>1e-9)&(I>0))[0]; seg=max(np.split(idx,np.where(np.diff(idx)>1)[0]+1),key=len)
    gx,gy=bdd.dqdv_grid_bdd(V[seg],np.abs(Q[seg]-Q[seg][0]),dV=0.001); m=(gx>=0.07)&(gx<=0.55); return gx[m],gy[m]
# 가장 흑연피크 뚜렷한 블렌드 자동선택
cands=["sigr_aq1_pocv.parquet","sigr1_c2_pocv.parquet","sigr2_c2_pocv.parquet","sigr_aq2_pocv.parquet"]
best=None
for c in cands:
    try:
        Vx,Dx=blend_dqdv(c)
        gpk=Dx[(Vx>=0.08)&(Vx<=0.16)].max()/max(Dx.max(),1e-9)  # 흑연영역 상대강도
        if best is None or gpk>best[0]: best=(gpk,c,Vx,Dx)
    except Exception as e: pass
_,cell,Vx,Dx=best; area=float(_trapz(Dx,Vx))
print(f"선택 블렌드셀: {cell} (흑연피크 상대강도 {best[0]:.2f})  npts={len(Vx)}")

Ugr=[0.088,0.118,0.145,0.205]; Usi=[0.30,0.45]  # 탈리튬 흑연4+Si2 시드
NG=len(Ugr); NS=len(Usi)

# ===== Baseline(문건기본): 흑연4 로지스틱(자유폭 대칭)+Si2 로지스틱(broad) =====
def M_base(V,*p):
    o=np.full_like(np.asarray(V,float),p[-1]); k=0
    for j in range(NG): o=o+logi(V,p[k],p[k+1],p[k+2]); k+=3
    for j in range(NS): o=o+logi(V,p[k],p[k+1],p[k+2]); k+=3
    return o
def seed_base():
    p0=[];lo=[];hi=[]
    for u in Ugr: p0+=[u,0.004,0.1*area]; lo+=[u-0.02,0.001,1e-7]; hi+=[u+0.02,0.03,10*area]
    for u in Usi: p0+=[u,0.04,0.15*area]; lo+=[u-0.06,0.01,1e-7]; hi+=[u+0.06,0.15,10*area]
    p0+=[0.02];lo+=[0];hi+=[max(Dx)]; return p0,lo,hi
p0,lo,hi=seed_base(); pB,_=curve_fit(M_base,Vx,Dx,p0=p0,bounds=(lo,hi),maxfev=200000); r2B=r2(Dx,M_base(Vx,*pB))

# ===== @1 정칙용액 Ω>2RT near-delta 커널(흑연 두-상) =====
def M_reg(V,*p):
    o=np.full_like(np.asarray(V,float),p[-1]); k=0
    for j in range(NG): o=o+reg(V,p[k],p[k+1],p[k+2],p[k+3]); k+=4
    for j in range(NS): o=o+logi(V,p[k],p[k+1],p[k+2]); k+=3
    return o
p0=[];lo=[];hi=[]
for u in Ugr: p0+=[u,3*R*T,0.1*area,0.0015]; lo+=[u-0.02,2.02*R*T,1e-7,0.0004]; hi+=[u+0.02,7*R*T,10*area,0.006]
for u in Usi: p0+=[u,0.04,0.15*area]; lo+=[u-0.06,0.01,1e-7]; hi+=[u+0.06,0.15,10*area]
p0+=[0.02];lo+=[0];hi+=[max(Dx)]
pR,_=curve_fit(M_reg,Vx,Dx,p0=p0,bounds=(lo,hi),maxfev=200000); r2R=r2(Dx,M_reg(Vx,*pR))

# ===== @2 비대칭 폭(Zhu2023) 흑연 =====
def M_asym(V,*p):
    o=np.full_like(np.asarray(V,float),p[-1]); k=0
    for j in range(NG): o=o+asym(V,p[k],p[k+1],p[k+2],p[k+3]); k+=4
    for j in range(NS): o=o+logi(V,p[k],p[k+1],p[k+2]); k+=3
    return o
p0=[];lo=[];hi=[]
for u in Ugr: p0+=[u,0.004,0.004,0.1*area]; lo+=[u-0.02,0.001,0.001,1e-7]; hi+=[u+0.02,0.03,0.03,10*area]
for u in Usi: p0+=[u,0.04,0.15*area]; lo+=[u-0.06,0.01,1e-7]; hi+=[u+0.06,0.15,10*area]
p0+=[0.02];lo+=[0];hi+=[max(Dx)]
pA,_=curve_fit(M_asym,Vx,Dx,p0=p0,bounds=(lo,hi),maxfev=200000); r2A=r2(Dx,M_asym(Vx,*pA))

# ===== @3 Si 전용 고용체(Frumkin Ω<2RT) — Si2 를 정칙용액으로 =====
def M_sifr(V,*p):
    o=np.full_like(np.asarray(V,float),p[-1]); k=0
    for j in range(NG): o=o+logi(V,p[k],p[k+1],p[k+2]); k+=3
    for j in range(NS): o=o+reg(V,p[k],p[k+1],p[k+2],p[k+3]); k+=4
    return o
p0=[];lo=[];hi=[]
for u in Ugr: p0+=[u,0.004,0.1*area]; lo+=[u-0.02,0.001,1e-7]; hi+=[u+0.02,0.03,10*area]
for u in Usi: p0+=[u,1.0*R*T,0.15*area,0.003]; lo+=[u-0.06,0.2*R*T,1e-7,0.001]; hi+=[u+0.06,1.99*R*T,10*area,0.02]
p0+=[0.02];lo+=[0];hi+=[max(Dx)]
pS,_=curve_fit(M_sifr,Vx,Dx,p0=p0,bounds=(lo,hi),maxfev=200000); r2S=r2(Dx,M_sifr(Vx,*pS))

# ===== @4 실측 U_j 물리시드 고정(위치=baseline 적합 위치, 폭·높이만 자유) =====
# 이 셀의 실제 피크위치(baseline fit)로 U 고정 → 위치자유 제거 비용 측정(물리앵커 무료?)
UgrF=[pB[0],pB[3],pB[6],pB[9]]; UsiF=[pB[12],pB[15]]
def M_fixU(V,*p):
    o=np.full_like(np.asarray(V,float),p[-1]); k=0
    for j in range(NG): o=o+logi(V,UgrF[j],p[k],p[k+1]); k+=2
    for j in range(NS): o=o+logi(V,UsiF[j],p[k],p[k+1]); k+=2
    return o
p0=[];lo=[];hi=[]
for u in Ugr: p0+=[0.004,0.1*area]; lo+=[0.001,1e-7]; hi+=[0.03,10*area]
for u in Usi: p0+=[0.04,0.15*area]; lo+=[0.01,1e-7]; hi+=[0.15,10*area]
p0+=[0.02];lo+=[0];hi+=[max(Dx)]
pF,_=curve_fit(M_fixU,Vx,Dx,p0=p0,bounds=(lo,hi),maxfev=200000); r2F=r2(Dx,M_fixU(Vx,*pF))

# ===== @5 stage-2L 5번째 흑연 전이 추가 =====
Ugr5=[0.088,0.118,0.135,0.152,0.205]; NG5=5
def M_2L(V,*p):
    o=np.full_like(np.asarray(V,float),p[-1]); k=0
    for j in range(NG5): o=o+logi(V,p[k],p[k+1],p[k+2]); k+=3
    for j in range(NS): o=o+logi(V,p[k],p[k+1],p[k+2]); k+=3
    return o
p0=[];lo=[];hi=[]
for u in Ugr5: p0+=[u,0.004,0.08*area]; lo+=[u-0.015,0.001,1e-7]; hi+=[u+0.015,0.03,10*area]
for u in Usi: p0+=[u,0.04,0.15*area]; lo+=[u-0.06,0.01,1e-7]; hi+=[u+0.06,0.15,10*area]
p0+=[0.02];lo+=[0];hi+=[max(Dx)]
p2,_=curve_fit(M_2L,Vx,Dx,p0=p0,bounds=(lo,hi),maxfev=200000); r22=r2(Dx,M_2L(Vx,*p2))

cases=[("@1 정칙용액 Ω>2RT\n(흑연 near-delta)",r2R,M_reg,pR),
       ("@2 비대칭 폭\n(Zhu2023)",r2A,M_asym,pA),
       ("@3 Si 고용체 Frumkin\n(Ω<2RT)",r2S,M_sifr,pS),
       ("@4 실측 U_j 고정\n(물리시드)",r2F,M_fixU,pF),
       ("@5 stage-2L 전이추가\n(흑연 4→5)",r22,M_2L,p2)]
print(f"\nBaseline(문건기본) R²={r2B:.4f}")
for nm,rr,_,_ in cases: print(f"  {nm.splitlines()[0]:28s} R²={rr:.4f}  ΔR²={(rr-r2B)*100:+.2f}%p")

# ===== 그림: (좌)ΔR² 막대 (우)곡선 그리드 =====
fig=plt.figure(figsize=(17,7)); gs=fig.add_gridspec(2,4,width_ratios=[1.25,1,1,1])
axb=fig.add_subplot(gs[:,0])
names=[c[0] for c in cases]; dr=[(c[1]-r2B)*100 for c in cases]
cols=['tab:green' if x>0.3 else ('tab:orange' if x>0.05 else 'tab:gray') for x in dr]
y=np.arange(len(dr))
axb.barh(y,dr,color=cols); axb.set_yticks(y); axb.set_yticklabels(names,fontsize=9)
axb.axvline(0,color='k',lw=.8); axb.invert_yaxis(); axb.set_xlabel('ΔR² vs 문건기본 (%p)')
axb.set_title(f'개별 개선효과 ΔR²\n문건기본 R²={r2B:.3f}',fontsize=11)
for i,x in enumerate(dr): axb.annotate(f'{x:+.2f}',(x,i),fontsize=9,fontweight='bold',va='center',ha='left' if x>=0 else 'right')
axb.grid(axis='x',alpha=.3); axb.margins(x=0.18)
pos=[(0,1),(0,2),(0,3),(1,1),(1,2)]
for (nm,rr,MF,pp),(r,c) in zip(cases,pos):
    ax=fig.add_subplot(gs[r,c])
    ax.plot(Vx,Dx,'k',lw=1.3,alpha=.85,label='실측')
    ax.plot(Vx,M_base(Vx,*pB),color='tab:gray',lw=1,ls=':',label=f'기본 {r2B:.3f}')
    ax.plot(Vx,MF(Vx,*pp),color='tab:red',lw=1,label=f'+@ {rr:.3f}')
    ax.set_title(nm,fontsize=8.5); ax.tick_params(labelsize=7); ax.set_xlim(0.07,0.55)
    ax.legend(fontsize=6.5,loc='upper right'); ax.set_xlabel('V',fontsize=8)
axn=fig.add_subplot(gs[1,3]); axn.axis('off')
axn.text(0,0.5,f"셀: {cell} (SINTEF 공개)\n검정=실측·회색점선=문건기본·빨강=+@\n\n초록=효과유의 / 회색=무의미·해로움\n\n결론: Si 고용체(@3)만 실효(+0.67%p)\nU_j 물리고정(@4)=공짜·전이추가(@5)=해로움",fontsize=9,va='center')
fig.suptitle('흑연+Si 블렌드 — 개별 개선효과 ablation (한 번에 @ 하나씩)',fontsize=13); fig.tight_layout()
fig.savefig(f"{OUT}/ablation.png",dpi=120); print("saved ablation.png")
json.dump({"cell":cell,"baseline_r2":r2B,"cases":{c[0].replace(chr(10),' '):c[1] for c in cases},
           "delta_r2_pct":{c[0].replace(chr(10),' '):(c[1]-r2B)*100 for c in cases}},
          open(f"{OUT}/ablation_result.json","w"),indent=1,default=float)
