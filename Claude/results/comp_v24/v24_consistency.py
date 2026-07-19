# -*- coding: utf-8 -*-
"""v1.0.24 선-검토(문건·코드 무수정) — 파라미터 일관성 = 산업 사용성 검증.
사용자 우려: 공개데이터 피팅이 일관성 떨어짐 → 회사 적용 곤란.
핵심 구분: (A)동일소재 다중셀 = 파라미터 '일관해야'(1회 피팅→전 조건 적용) / (B)이종소재 = 물리적으로 다름(당연).
테스트: (1)자유피팅 w_j 셀간 spread, (2)전역피팅(U_j·w_j 공유·Q_j·Cbg 만 셀별) R² — 단일 물리셋이 설명하나.
물리 근거: 문건 Ω>2RT ⇒ 두-상(sharp) → 폭은 소재 heterogeneity(≈일정), 자유변수 아님.
"""
import numpy as np, pandas as pd, importlib.util, sys, json, warnings; warnings.filterwarnings("ignore")
sys.path.insert(0,"/home/user/Project_Anode_Fit/Claude/results/comp_v24"); import bdd_smoothing as bdd
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
SC="/tmp/claude-0/-home-user-Project-Anode-Fit/e8d4cdbc-60e6-548e-b742-1446b8f7a8bd/scratchpad/zenodo_gr"; OUT="/home/user/Project_Anode_Fit/Claude/results/comp_v24"
af_s=importlib.util.spec_from_file_location("af","/home/user/Project_Anode_Fit/Claude/docs/v1.0.23/Anode_Fit_v1.0.23.py")
af=importlib.util.module_from_spec(af_s); af_s.loader.exec_module(af); GR=af.GraphiteAnodeDischargeDQDV
R,F,T=8.314,96485.0,298.15
_trapz=getattr(np,'trapezoid',getattr(np,'trapz',None))
# 물리 시드(문건 thermo U_j) + 4전이(문건 established count)
U_seed=[af.func_U_j(T,tr['dH_rxn'],tr['dS_rxn']) for tr in af.GRAPHITE_STAGING_LIT]
NT=4

def dqdv(cell):
    d=pd.read_parquet(f"{SC}/{cell}"); I=d['Current / A'].to_numpy(); V=d['Voltage / V'].to_numpy(); Q=d['Cumulative Capacity / Ah'].to_numpy()*1000
    idx=np.where((np.abs(I)>1e-9)&(I>0))[0]; seg=max(np.split(idx,np.where(np.diff(idx)>1)[0]+1),key=len)
    gx,gy=bdd.dqdv_grid_bdd(V[seg],Q[seg]-Q[seg][0],dV=0.0005); m=(gx>=0.05)&(gx<=0.30); return gx[m],gy[m]

cells=["gr_pocv_4ccc47.parquet","gr_pocv_1d5628.parquet"]  # 동일소재(Gr-AQ-1) 2셀
data=[dqdv(c) for c in cells]

def one_model(V,*p):  # 단일셀: U,w,Q per 전이 + Cbg
    out=np.full_like(np.asarray(V,float),p[-1])
    for j in range(NT):
        z=(V-p[3*j])/p[3*j+1]; s=np.where(z>=0,1/(1+np.exp(-z)),np.exp(z)/(1+np.exp(z))); out=out+p[3*j+2]*s*(1-s)
    return out
# (1) 자유피팅 각 셀
free_w=[]
for (Vx,Dx) in data:
    area=float(_trapz(Dx,Vx)); p0=[]; lo=[]; hi=[]
    for j in range(NT): p0+=[U_seed[j],0.003,50]; lo+=[0.05,0.0008,1e-6]; hi+=[0.30,0.06,1e5]
    p0+=[0.1]; lo+=[0]; hi+=[max(Dx)]
    pf,_=curve_fit(one_model,Vx,Dx,p0=p0,bounds=(lo,hi),maxfev=400000)
    free_w.append([pf[3*j+1]*1000 for j in range(NT)])
free_w=np.array(free_w)

# (2) 전역피팅: U_j·w_j 공유, Q_j·Cbg 셀별 → 단일 물리셋
def global_model(_dummy,*p):
    U=p[0:NT]; w=p[NT:2*NT]; out=[]
    for ci,(Vx,Dx) in enumerate(data):
        Qc=p[2*NT+ci*(NT+1): 2*NT+ci*(NT+1)+NT]; Cbg=p[2*NT+ci*(NT+1)+NT]
        y=np.full_like(Vx,Cbg)
        for j in range(NT):
            z=(Vx-U[j])/w[j]; s=np.where(z>=0,1/(1+np.exp(-z)),np.exp(z)/(1+np.exp(z))); y=y+Qc[j]*s*(1-s)
        out.append(y)
    return np.concatenate(out)
allD=np.concatenate([Dx for _,Dx in data])
p0=list(U_seed)+[0.0015]*NT
lo=[0.05]*NT+[0.0008]*NT; hi=[0.30]*NT+[0.06]*NT
for (Vx,Dx) in data:
    area=float(_trapz(Dx,Vx)); p0+=[0.2*area]*NT+[0.1]; lo+=[1e-6]*NT+[0]; hi+=[1e5]*NT+[max(Dx)]
pg,_=curve_fit(global_model,None,allD,p0=p0,bounds=(lo,hi),maxfev=600000)
Ug=pg[0:NT]; wg=pg[NT:2*NT]
pred=global_model(None,*pg); off=0; r2g=[]
for (Vx,Dx) in data:
    pr=pred[off:off+len(Dx)]; off+=len(Dx); r2g.append(1-np.sum((Dx-pr)**2)/np.sum((Dx-Dx.mean())**2))

print("=== 동일소재(SINTEF Gr-AQ-1) 2셀 일관성 ===")
print("자유피팅 w_j(mV) 셀1:",[round(x,2) for x in free_w[0]],"셀2:",[round(x,2) for x in free_w[1]])
print("  → 셀간 w 상대편차:",[f'{abs(free_w[0][j]-free_w[1][j])/max(np.mean(free_w[:,j]),1e-9)*100:.0f}%' for j in range(NT)])
print(f"전역피팅 단일셋 U_j(V):",[round(x,4) for x in Ug]," w_j(mV):",[round(x*1000,2) for x in wg])
print(f"  → 단일 물리셋 R²: 셀1={r2g[0]:.3f} 셀2={r2g[1]:.3f} (자유와 비슷하면 = 파라미터 일관/산업사용가능)")
json.dump({"free_w_mV":free_w.tolist(),"global_U":list(map(float,Ug)),"global_w_mV":[float(x*1000) for x in wg],"global_R2":r2g},
          open(f"{OUT}/consistency_result.json","w"),indent=1)

fig,ax=plt.subplots(1,2,figsize=(14,5.2))
off=0
for ci,(Vx,Dx) in enumerate(data):
    ax[0].plot(Vx,Dx,lw=1.5,alpha=.8,label=f'real 셀{ci+1}')
    pr=pred[off:off+len(Dx)]; off+=len(Dx)   # 데이터 격자 동일 예측(공정 비교)
    ax[0].plot(Vx,pr,'--',lw=1.2,label=f'전역FIT 셀{ci+1} R²={r2g[ci]:.3f}')
ax[0].set_title('동일소재 2셀: 단일 물리셋(U_j·w_j 공유) 전역피팅\n(동일 추출격자 비교)'); ax[0].set_xlabel('V'); ax[0].set_ylabel('dQ/dV'); ax[0].legend(fontsize=8); ax[0].grid(alpha=.3)
# w 일관성 막대
x=np.arange(NT); ax[1].bar(x-0.2,free_w[0],0.18,label='자유 셀1'); ax[1].bar(x,free_w[1],0.18,label='자유 셀2'); ax[1].bar(x+0.2,[w*1000 for w in wg],0.18,label='전역 공유',color='k')
ax[1].set_xticks(x); ax[1].set_xticklabels([f'전이{j+1}\n{U_seed[j]:.3f}V' for j in range(NT)],fontsize=8); ax[1].set_ylabel('w_j / mV'); ax[1].set_title('w_j: 자유(셀별) vs 전역(공유) 일관성'); ax[1].legend(fontsize=8); ax[1].grid(alpha=.3)
fig.tight_layout(); fig.savefig(f"{OUT}/consistency.png",dpi=120); print("saved consistency.png")
