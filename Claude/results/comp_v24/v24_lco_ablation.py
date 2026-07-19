# -*- coding: utf-8 -*-
"""v1.0.24 진단 — LCO 실측(O2)에 흑연·블렌드와 동일 방법 + @3·@5 적용.
사용자: "3,5번 적용하기로 한 식으로도 LCO 같이 검토." → LCO가 흑연과 같은 개선 패턴이면
LCO도 정상(방법 문제 아님) 확증.
  baseline = plain MSMR(로지스틱 4피크) / @3 = 정칙용액 커널(per-peak 자유 Ω = 두-상 sharp+
  order broad 자동) / @5 = 전이 추가(4→6, LCO H1/H2·x0.5·H1-3 미세구조) / @3+@5.
LCO 실측 = Carlier2002 O2(digitized). 문건·코드 무수정(진단).
"""
import numpy as np, pandas as pd, sys, json, warnings; warnings.filterwarnings("ignore")
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
plt.rcParams['font.family']='NanumGothic'; plt.rcParams['axes.unicode_minus']=False
from scipy.optimize import curve_fit, brentq
LD="/home/user/Project_Anode_Fit/Claude/results/comp_v24/lco_data"; OUT="/home/user/Project_Anode_Fit/Claude/results/comp_v24"
R,F,T=8.314,96485.0,298.15; RTF=R*T/F; _trapz=getattr(np,'trapezoid',getattr(np,'trapz',None))

def logi(V,U,w,Q):
    z=(V-U)/w; s=np.where(z>=0,1/(1+np.exp(-z)),np.exp(z)/(1+np.exp(z))); return Q*s*(1-s)/w
XG=np.linspace(1e-3,1-1e-3,150)
_ag=np.linspace(2.0001,8.0,500)
def _bs(a):
    try: return brentq(lambda x: np.log(x/(1-x))+a*(1-2*x),1e-9,0.5-1e-12)
    except Exception: return 0.5
_xag=np.array([_bs(a) for a in _ag])
def binodal_xa(Om):
    a=Om/(R*T); return 0.5 if a<=2.0 else float(np.interp(a,_ag,_xag))
def sech2(v,d):
    zz=np.clip(v/(2*d),-350,350); c=1/np.cosh(zz); return c*c/(4*d)
def reg(V,U0,Om,Q,d):
    xa=binodal_xa(Om); xg=XG
    Vi=np.where((xg>xa)&(xg<1-xa),U0,U0-RTF*np.log(xg/(1-xg))-(Om/F)*(1-2*xg))
    wi=Q*(xg[1]-xg[0]); return (wi*sech2(np.asarray(V)[:,None]-Vi[None,:],d)).sum(axis=1)
def r2(y,yh): return 1-np.sum((y-yh)**2)/np.sum((y-y.mean())**2)
def ocv_dqdv(x,V,vlo,vhi,npts=500):
    o=np.argsort(V); V=np.asarray(V)[o]; x=np.asarray(x)[o]; Vu,iu=np.unique(V,return_index=True); xu=x[iu]
    Vg=np.linspace(max(vlo,Vu.min()),min(vhi,Vu.max()),npts); return Vg,np.abs(np.gradient(np.interp(Vg,Vu,xu),Vg))
a=np.loadtxt(f"{LD}/diffthermo_LCO_O2_OCV_Carlier2002JES_Fig4a_digitized.csv",delimiter=',',skiprows=1)
Vx,Dx=ocv_dqdv(a[:,0],a[:,1],3.35,4.5); area=float(_trapz(Dx,Vx))
U4=[3.70,4.03,4.15,4.40]; U6=[3.62,3.70,4.03,4.15,4.30,4.40]

def fit_logi(Us):
    NT=len(Us)
    def M(V,*p):
        o=np.full_like(np.asarray(V,float),p[-1])
        for j in range(NT): o=o+logi(V,p[3*j],p[3*j+1],p[3*j+2])
        return o
    p0=[];lo=[];hi=[]
    for u in Us: p0+=[u,0.012,0.2*area]; lo+=[u-0.05,0.003,1e-9]; hi+=[u+0.05,0.10,20*area]
    p0+=[max(Dx)*0.05];lo+=[0];hi+=[max(Dx)]
    pf,_=curve_fit(M,Vx,Dx,p0=p0,bounds=(lo,hi),maxfev=300000); return r2(Dx,M(Vx,*pf)),M,pf
def fit_reg(Us):
    NT=len(Us)
    def M(V,*p):
        o=np.full_like(np.asarray(V,float),p[-1])
        for j in range(NT): o=o+reg(V,p[4*j],p[4*j+1],p[4*j+2],p[4*j+3])
        return o
    p0=[];lo=[];hi=[]
    for u in Us: p0+=[u,1.5*R*T,0.2*area,0.006]; lo+=[u-0.05,0.3*R*T,1e-9,0.001]; hi+=[u+0.05,7*R*T,20*area,0.03]
    p0+=[max(Dx)*0.05];lo+=[0];hi+=[max(Dx)]
    pf,_=curve_fit(M,Vx,Dx,p0=p0,bounds=(lo,hi),maxfev=300000); return r2(Dx,M(Vx,*pf)),M,pf

r2_base,Mb,pb=fit_logi(U4)
r2_3,M3,p3=fit_reg(U4)
r2_5,M5,p5=fit_logi(U6)
r2_35,M35,p35=fit_reg(U6)
cases=[("문건기본(plain MSMR·4피크)",r2_base,Mb,pb),("@3 정칙용액커널(per-peak Ω)",r2_3,M3,p3),
       ("@5 전이추가(4→6)",r2_5,M5,p5),("@3+@5",r2_35,M35,p35)]
print("=== LCO 실측(O2 Carlier) — 흑연/블렌드와 동일 @3·@5 적용 ===")
print(f"  참고: 흑연 plain R²=0.940 · LCO plain R²={r2_base:.4f}")
for nm,rr,_,_ in cases: print(f"  {nm:28s} R²={rr:.4f}  ΔR²={(rr-r2_base)*100:+.2f}%p")
print("→ LCO도 흑연·블렌드와 같은 개선 패턴(@3/@5)이면 = LCO는 방법·모델상 흑연과 동일하게 작동.")

fig,ax=plt.subplots(1,2,figsize=(15,5.5)); gs=None
for nm,rr,MF,pp in cases:
    ax[0].plot(Vx,MF(Vx,*pp),lw=1.2,label=f'{nm.split("(")[0]} R²={rr:.3f}')
ax[0].plot(Vx,Dx,'k',lw=1.6,alpha=.85,label='LCO 실측(O2)',zorder=5)
ax[0].set_xlim(3.35,4.5); ax[0].set_xlabel('V vs Li'); ax[0].set_ylabel('dQ/dV'); ax[0].set_title('LCO 실측 @3·@5 피팅 오버레이'); ax[0].legend(fontsize=8); ax[0].grid(alpha=.3)
names=[c[0].split("(")[0] for c in cases]; dr=[(c[1]-r2_base)*100 for c in cases]
cols=['tab:gray']+['tab:green' if x>0.3 else ('tab:orange' if x>0.05 else 'tab:gray') for x in dr[1:]]
ax[1].barh(range(len(dr)),dr,color=cols); ax[1].set_yticks(range(len(dr))); ax[1].set_yticklabels(names,fontsize=9)
ax[1].axvline(0,color='k',lw=.8); ax[1].invert_yaxis(); ax[1].set_xlabel('ΔR² vs plain (%p)'); ax[1].margins(x=0.2); ax[1].grid(axis='x',alpha=.3)
ax[1].set_title(f'LCO 개선효과 (plain R²={r2_base:.3f})')
for i,x in enumerate(dr): ax[1].annotate(f'{x:+.2f}',(x,i),fontsize=9,fontweight='bold',va='center',ha='left' if x>=0 else 'right')
fig.suptitle('LCO 실측(O2 Carlier) — 흑연·블렌드와 동일 방법 + @3·@5 적용 검토',fontsize=13)
fig.tight_layout(); fig.savefig(f"{OUT}/lco_ablation.png",dpi=120); print("saved lco_ablation.png")
json.dump({"LCO_O2_real":{"plain":r2_base,"@3":r2_3,"@5":r2_5,"@3+@5":r2_35},"graphite_plain_ref":0.940},
          open(f"{OUT}/lco_ablation_result.json","w"),indent=1,default=float)
