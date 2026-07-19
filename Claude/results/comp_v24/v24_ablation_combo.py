# -*- coding: utf-8 -*-
"""v1.0.24 — 흑연+Si 블렌드 @1·@3·@5 조합 ablation.
사용자: @1(흑연 near-delta Ω>2RT)·@3(Si 고용체 Frumkin)·@5(stage-2L 전이추가) 의
둘/셋 조합 비교. 개별효과가 조합서 상승(synergy)/상쇄(redundancy)되는지 = 상호작용 검증.
개별: @1 −0.02·@3 +0.67·@5 −0.44 %p. 문건·코드 무수정.
"""
import numpy as np, pandas as pd, sys, json, warnings; warnings.filterwarnings("ignore")
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
plt.rcParams['font.family']='NanumGothic'; plt.rcParams['axes.unicode_minus']=False
from scipy.optimize import curve_fit, brentq
sys.path.insert(0,"/home/user/Project_Anode_Fit/Claude/results/comp_v24"); import bdd_smoothing as bdd
SC="/tmp/claude-0/-home-user-Project-Anode-Fit/e8d4cdbc-60e6-548e-b742-1446b8f7a8bd/scratchpad/zenodo_gr"
OUT="/home/user/Project_Anode_Fit/Claude/results/comp_v24"
R,F,T=8.314,96485.0,298.15; RTF=R*T/F; _trapz=getattr(np,'trapezoid',getattr(np,'trapz',None))

def logi(V,U,w,Q):
    z=(V-U)/w; s=np.where(z>=0,1/(1+np.exp(-z)),np.exp(z)/(1+np.exp(z))); return Q*s*(1-s)/w
XG=np.linspace(1e-3,1-1e-3,150)  # 커널격자(속도) — 플롯품질 충분
# binodal xa(Ω) 룩업테이블(brentq 를 hot-loop서 제거 — 속도 핵심). a=Ω/RT∈[2.0,8].
def _bsolve(a):
    try: return brentq(lambda x: np.log(x/(1-x))+a*(1-2*x),1e-9,0.5-1e-12)
    except Exception: return 0.5
_ag=np.linspace(2.0001,8.0,600); _xag=np.array([_bsolve(a) for a in _ag])
def binodal_xa(Om):
    a=Om/(R*T)
    if a<=2.0: return 0.5
    return float(np.interp(a,_ag,_xag))
def sech2(v,d):
    zz=np.clip(v/(2*d),-350,350); c=1/np.cosh(zz); return c*c/(4*d)
def reg(V,U0,Om,Q,d):
    xa=binodal_xa(Om); xg=XG
    Vi=np.where((xg>xa)&(xg<1-xa),U0,U0-RTF*np.log(xg/(1-xg))-(Om/F)*(1-2*xg))
    wi=Q*(xg[1]-xg[0]); return (wi*sech2(np.asarray(V)[:,None]-Vi[None,:],d)).sum(axis=1)
def r2(y,yh): return 1-np.sum((y-yh)**2)/np.sum((y-y.mean())**2)

def blend_dqdv(cell):
    d=pd.read_parquet(f"{SC}/{cell}"); I=d['Current / A'].to_numpy(); V=d['Voltage / V'].to_numpy(); Q=d['Cumulative Capacity / Ah'].to_numpy()*1000
    idx=np.where((np.abs(I)>1e-9)&(I>0))[0]; seg=max(np.split(idx,np.where(np.diff(idx)>1)[0]+1),key=len)
    gx,gy=bdd.dqdv_grid_bdd(V[seg],np.abs(Q[seg]-Q[seg][0]),dV=0.001); m=(gx>=0.07)&(gx<=0.55); return gx[m],gy[m]
cell="sigr_aq1_pocv.parquet"; Vx,Dx=blend_dqdv(cell); area=float(_trapz(Dx,Vx))
Ugr=[0.088,0.118,0.145,0.205]; Ugr5=[0.088,0.118,0.135,0.152,0.205]; Usi=[0.30,0.45]; NS=2

# ---- 플래그(regsol_gr @1, use2L @5, frumkin_si @3) 기반 유연 모델 ----
def make(regsol_gr,use2L,frumkin_si):
    Ug=Ugr5 if use2L else Ugr; NGx=len(Ug)
    def model(V,*p):
        o=np.full_like(np.asarray(V,float),p[-1]); k=0
        for j in range(NGx):
            if regsol_gr: o=o+reg(V,p[k],p[k+1],p[k+2],p[k+3]); k+=4
            else: o=o+logi(V,p[k],p[k+1],p[k+2]); k+=3
        for j in range(NS):
            if frumkin_si: o=o+reg(V,p[k],p[k+1],p[k+2],p[k+3]); k+=4
            else: o=o+logi(V,p[k],p[k+1],p[k+2]); k+=3
        return o
    p0=[];lo=[];hi=[]
    for u in Ug:
        if regsol_gr: p0+=[u,3*R*T,0.09*area,0.0015]; lo+=[u-0.02,2.02*R*T,1e-7,0.0004]; hi+=[u+0.02,7*R*T,10*area,0.006]
        else: p0+=[u,0.004,0.09*area]; lo+=[u-0.02,0.001,1e-7]; hi+=[u+0.02,0.03,10*area]
    for u in Usi:
        if frumkin_si: p0+=[u,1.0*R*T,0.15*area,0.003]; lo+=[u-0.06,0.2*R*T,1e-7,0.001]; hi+=[u+0.06,1.99*R*T,10*area,0.02]
        else: p0+=[u,0.04,0.15*area]; lo+=[u-0.06,0.01,1e-7]; hi+=[u+0.06,0.15,10*area]
    p0+=[0.02];lo+=[0];hi+=[max(Dx)]
    return model,p0,lo,hi
def fit(flags):
    m,p0,lo,hi=make(*flags)
    pf,_=curve_fit(m,Vx,Dx,p0=p0,bounds=(lo,hi),maxfev=300000); return r2(Dx,m(Vx,*pf)),m,pf

combos=[("문건기본",(False,False,False)),("@1",(True,False,False)),("@3",(False,False,True)),("@5",(False,True,False)),
        ("@1+@3",(True,False,True)),("@1+@5",(True,True,False)),("@3+@5",(False,True,True)),("@1+@3+@5",(True,True,True))]
res={}; models={}
for nm,fl in combos:
    rr,m,pf=fit(fl); res[nm]=rr; models[nm]=(m,pf)
r2B=res["문건기본"]
ind={"@1":res["@1"]-r2B,"@3":res["@3"]-r2B,"@5":res["@5"]-r2B}
print(f"문건기본 R²={r2B:.4f}\n--- 개별 ---")
for k in ["@1","@3","@5"]: print(f"  {k:10s} R²={res[k]:.4f}  ΔR²={ind[k]*100:+.2f}%p")
print("--- 조합 (실제 ΔR² vs 개별합 = 상호작용) ---")
def parts(nm): return nm.split("+")
for nm in ["@1+@3","@1+@5","@3+@5","@1+@3+@5"]:
    d=(res[nm]-r2B)*100; s=sum(ind[p] for p in parts(nm))*100; inter=d-s
    tag="synergy(상승)" if inter>0.05 else ("redundancy(상쇄)" if inter<-0.05 else "가산적")
    print(f"  {nm:12s} R²={res[nm]:.4f}  ΔR²={d:+.2f}%p  개별합={s:+.2f}  상호작용={inter:+.2f} → {tag}")

# ===== 그림 =====
fig=plt.figure(figsize=(16,6.5)); gs=fig.add_gridspec(1,3,width_ratios=[1.35,1,1])
axb=fig.add_subplot(gs[0,0])
order=["@1","@3","@5","@1+@3","@1+@5","@3+@5","@1+@3+@5"]
dr=[(res[n]-r2B)*100 for n in order]
cols=['tab:green' if x>0.3 else ('tab:orange' if x>0.05 else 'tab:gray') for x in dr]
yy=np.arange(len(order))
axb.barh(yy,dr,color=cols); axb.set_yticks(yy); axb.set_yticklabels(order,fontsize=10)
axb.axhline(2.5,color='k',lw=.5,ls=':'); axb.axhline(5.5,color='k',lw=.5,ls=':')
axb.text(axb.get_xlim()[1]*0.5,-0.4,'개별',fontsize=8,color='gray'); axb.text(axb.get_xlim()[1]*0.5,3.6,'둘 조합',fontsize=8,color='gray'); axb.text(axb.get_xlim()[1]*0.5,6.4,'셋',fontsize=8,color='gray')
axb.axvline(0,color='k',lw=.8); axb.invert_yaxis(); axb.set_xlabel('ΔR² vs 문건기본 (%p)'); axb.margins(x=0.2)
axb.set_title(f'조합별 개선효과 ΔR²\n문건기본 R²={r2B:.3f}',fontsize=11); axb.grid(axis='x',alpha=.3)
for i,x in enumerate(dr): axb.annotate(f'{x:+.2f}',(x,i),fontsize=9,fontweight='bold',va='center',ha='left' if x>=0 else 'right')
# 상호작용 막대(조합 실제 − 개별합)
axi=fig.add_subplot(gs[0,1])
comb=["@1+@3","@1+@5","@3+@5","@1+@3+@5"]
inter=[((res[n]-r2B)-sum(ind[p] for p in parts(n)))*100 for n in comb]
ci=['tab:blue' if x>0.05 else ('tab:red' if x<-0.05 else 'tab:gray') for x in inter]
axi.barh(np.arange(len(comb)),inter,color=ci); axi.set_yticks(np.arange(len(comb))); axi.set_yticklabels(comb,fontsize=9)
axi.axvline(0,color='k',lw=.8); axi.invert_yaxis(); axi.set_xlabel('상호작용 (%p) = 조합−개별합'); axi.margins(x=0.25)
axi.set_title('상호작용\n(+파랑=상승 / −빨강=상쇄)',fontsize=11); axi.grid(axis='x',alpha=.3)
for i,x in enumerate(inter): axi.annotate(f'{x:+.2f}',(x,i),fontsize=9,va='center',ha='left' if x>=0 else 'right')
# best combo 곡선
axc=fig.add_subplot(gs[0,2])
best=max(order,key=lambda n:res[n]); mB,pB=models["문건기본"]; mb,pb=models[best]
axc.plot(Vx,Dx,'k',lw=1.4,alpha=.85,label='실측'); axc.plot(Vx,mB(Vx,*pB),color='tab:gray',ls=':',lw=1,label=f'기본 {r2B:.3f}')
axc.plot(Vx,mb(Vx,*pb),color='tab:red',lw=1,label=f'{best} {res[best]:.3f}')
axc.set_xlim(0.07,0.55); axc.set_xlabel('V'); axc.set_ylabel('dQ/dV'); axc.set_title(f'최고 조합: {best}',fontsize=11); axc.legend(fontsize=8); axc.grid(alpha=.3)
fig.suptitle('흑연+Si 블렌드 — @1·@3·@5 조합 ablation',fontsize=13); fig.tight_layout()
fig.savefig(f"{OUT}/ablation_combo.png",dpi=120); print("saved ablation_combo.png")

# ===== 그림2: 조합별 dQ/dV 피팅 전체곡선 (실측 vs 문건기본 vs 조합) =====
allc=["문건기본"]+order  # 8개
mB,pB=models["문건기본"]; residB=Dx-mB(Vx,*pB)
fig2,ax2=plt.subplots(2,4,figsize=(21,9.5))
for idx,nm in enumerate(allc):
    a=ax2.flat[idx]; m,p=models[nm]
    a.plot(Vx,Dx,'k',lw=1.6,alpha=.9,label='실측(공개)')
    if nm!="문건기본": a.plot(Vx,mB(Vx,*pB),color='tab:gray',ls=':',lw=1.3,label=f'문건기본 {r2B:.3f}')
    a.plot(Vx,m(Vx,*p),color='tab:red',lw=1.4,label=f'{nm} {res[nm]:.4f}')
    dd=(res[nm]-r2B)*100
    a.set_title(f'{nm}   R²={res[nm]:.4f}   ΔR²={dd:+.2f}%p',fontsize=11,fontweight='bold' if nm!="문건기본" else 'normal')
    a.set_xlim(0.07,0.55); a.set_xlabel('V vs Li',fontsize=9); a.set_ylabel('dQ/dV',fontsize=9)
    a.legend(fontsize=8,loc='upper right'); a.grid(alpha=.3)
fig2.suptitle('흑연+Si 블렌드 — 조합별 dQ/dV 피팅 전체곡선 (검정=실측·회색=문건기본·빨강=조합)',fontsize=14)
fig2.tight_layout(); fig2.savefig(f"{OUT}/ablation_combo_curves.png",dpi=115); print("saved ablation_combo_curves.png")

# ===== 그림3: 잔차(실측−모델) — 0에 가까울수록 정확. 회색=문건기본 대비 =====
fig3,ax3=plt.subplots(2,4,figsize=(21,9.5))
ymax=np.nanmax(np.abs(residB))*1.15
for idx,nm in enumerate(allc):
    a=ax3.flat[idx]; m,p=models[nm]; resid=Dx-m(Vx,*p)
    a.axhline(0,color='k',lw=.7)
    if nm!="문건기본": a.plot(Vx,residB,color='tab:gray',lw=1.1,alpha=.7,label=f'문건기본 잔차(RMSE {np.sqrt(np.mean(residB**2)):.2f})')
    a.plot(Vx,resid,color='tab:red',lw=1.2,label=f'{nm} 잔차(RMSE {np.sqrt(np.mean(resid**2)):.2f})')
    a.fill_between(Vx,resid,color='tab:red',alpha=.12)
    a.set_title(f'{nm}   R²={res[nm]:.4f}',fontsize=11); a.set_xlim(0.07,0.55); a.set_ylim(-ymax,ymax)
    a.set_xlabel('V vs Li',fontsize=9); a.set_ylabel('실측−모델',fontsize=9); a.legend(fontsize=8); a.grid(alpha=.3)
fig3.suptitle('조합별 잔차 (실측−모델): 빨강이 0선·회색보다 붙을수록 개선. Si 봉우리(0.3~0.5V)가 관건',fontsize=14)
fig3.tight_layout(); fig3.savefig(f"{OUT}/ablation_combo_resid.png",dpi=115); print("saved ablation_combo_resid.png")

json.dump({"cell":cell,"baseline":r2B,"R2":res,"individual_dR2_pct":{k:ind[k]*100 for k in ind},
           "interaction_pct":{n:((res[n]-r2B)-sum(ind[p] for p in parts(n)))*100 for n in comb}},
          open(f"{OUT}/ablation_combo_result.json","w"),indent=1,default=float)
