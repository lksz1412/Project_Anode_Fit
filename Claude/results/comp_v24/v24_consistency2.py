# -*- coding: utf-8 -*-
"""v1.0.24 C — 파라미터 일관성 = 산업 사용성 실증(강화판). 문건·코드 무수정.
사용자 핵심 우려: 공개데이터 피팅 비일관 → 회사 적용 곤란. 방법론 문헌(Hu-Schwartz 2022·
PyBOP 2025·Lu-Trimboli 2021)이 제시한 프로토콜을 우리 데이터로 실증:
  P1) 동일소재 다중셀: 계층 피팅(자유 L0 → U공유 L1 → U·w공유 L2=단일 물리셋). L2 R²≈L0 이면
      단일 물리셋이 전 셀 설명 = 일관 = 산업사용가능. 자유 w 산포 = 아티팩트 확인.
  P2) 부트스트랩 UQ: L2 파라미터 신뢰구간 → 어느 U_j·w_j 가 식별가능(tight) vs 축퇴(wide).
      "평탄 OCV → 약한 식별성" 실측 노출.
  P3) 이종소재 U_j 보편성: 5 흑연(SINTEF·Enertech·Chen·PyBEP) 피크위치 → staging 위치는
      화학불변(tight)·폭/높이는 소재의존. 단일 U_j 셋이 전 흑연 시드가능.
"""
import numpy as np, pandas as pd, importlib.util, sys, json, warnings; warnings.filterwarnings("ignore")
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
plt.rcParams['font.family']='NanumGothic'; plt.rcParams['axes.unicode_minus']=False
from scipy.optimize import curve_fit
from scipy.signal import find_peaks
sys.path.insert(0,"/home/user/Project_Anode_Fit/Claude/results/comp_v24"); import bdd_smoothing as bdd
SC="/tmp/claude-0/-home-user-Project-Anode-Fit/e8d4cdbc-60e6-548e-b742-1446b8f7a8bd/scratchpad"
GRD=f"{SC}/zenodo_gr"; OCP=f"{SC}/ocp"; OUT="/home/user/Project_Anode_Fit/Claude/results/comp_v24"
R,F,T=8.314,96485.0,298.15; _trapz=getattr(np,'trapezoid',getattr(np,'trapz',None))
rng=np.random.default_rng(7)
NT=4; Useed=[0.211,0.140,0.120,0.085]

def dqdv_parq(cell):
    d=pd.read_parquet(f"{GRD}/{cell}"); I=d['Current / A'].to_numpy(); V=d['Voltage / V'].to_numpy(); Q=d['Cumulative Capacity / Ah'].to_numpy()*1000
    idx=np.where((np.abs(I)>1e-9)&(I>0))[0]; seg=max(np.split(idx,np.where(np.diff(idx)>1)[0]+1),key=len)
    gx,gy=bdd.dqdv_grid_bdd(V[seg],Q[seg]-Q[seg][0],dV=0.0005); m=(gx>=0.06)&(gx<=0.25); return gx[m],gy[m]

def dqdv_ocp(path,sep=None):
    xy=[]
    for ln in open(path):
        ln=ln.strip()
        if not ln or ln[0] in '#*': continue
        p=ln.replace(',',' ').split()
        try: xy.append((float(p[0]),float(p[1])))
        except Exception: pass
    a=np.array(xy); x=a[:,0]; V=a[:,1]
    o=np.argsort(V); V=V[o]; x=x[o]; m=(V>=0.06)&(V<=0.25)
    Vg=np.linspace(0.06,0.25,400); xi=np.interp(Vg,V,x); d=-np.gradient(xi,Vg)  # dQ/dV ∝ dx/dV
    d=np.clip(d,0,None); d=d/ max(_trapz(d,Vg),1e-9)  # 면적정규화(형상비교)
    return Vg,d

# ===== 로지스틱 4-전이 (스택 모델) =====
def logi_peak(V,U,w,Q):
    z=(V-U)/w; s=np.where(z>=0,1/(1+np.exp(-z)),np.exp(z)/(1+np.exp(z))); return Q*s*(1-s)/w
def r2(y,yh): return 1-np.sum((y-yh)**2)/np.sum((y-y.mean())**2)

cells=["gr_pocv_4ccc47.parquet","gr_pocv_1d5628.parquet"]
data=[dqdv_parq(c) for c in cells]; NC=len(data)

# ---- L0 자유: 각 셀 독립 ----
def one(V,*p):
    out=np.full_like(V,p[-1])
    for j in range(NT): out=out+logi_peak(V,p[3*j],p[3*j+1],p[3*j+2])
    return out
L0w=[]; L0U=[]; L0r2=[]
for (V,D) in data:
    ar=float(_trapz(D,V)); p0=[]; lo=[]; hi=[]
    for j in range(NT): p0+=[Useed[j],0.004,0.15*ar]; lo+=[Useed[j]-0.03,0.0006,1e-7]; hi+=[Useed[j]+0.03,0.05,10*ar]
    p0+=[0.05]; lo+=[0]; hi+=[max(D)]
    pf,_=curve_fit(one,V,D,p0=p0,bounds=(lo,hi),maxfev=200000)
    L0U.append([pf[3*j] for j in range(NT)]); L0w.append([pf[3*j+1]*1000 for j in range(NT)]); L0r2.append(r2(D,one(V,*pf)))
L0U=np.array(L0U); L0w=np.array(L0w)

# ---- L2 단일 물리셋: U_j·w_j 공유, Q_j·Cbg 셀별 ----
def stack_L2(_d,*p):
    U=p[:NT]; w=p[NT:2*NT]; out=[]
    for ci,(V,D) in enumerate(data):
        Q=p[2*NT+ci*(NT+1):2*NT+ci*(NT+1)+NT]; Cbg=p[2*NT+ci*(NT+1)+NT]; y=np.full_like(V,Cbg)
        for j in range(NT): y=y+logi_peak(V,U[j],w[j],Q[j])
        out.append(y)
    return np.concatenate(out)
allD=np.concatenate([D for _,D in data])
p0=list(Useed)+[0.003]*NT; lo=[u-0.03 for u in Useed]+[0.0006]*NT; hi=[u+0.03 for u in Useed]+[0.05]*NT
for (V,D) in data:
    ar=float(_trapz(D,V)); p0+=[0.15*ar]*NT+[0.05]; lo+=[1e-7]*NT+[0]; hi+=[10*ar]*NT+[max(D)]
pL2,_=curve_fit(stack_L2,None,allD,p0=p0,bounds=(lo,hi),maxfev=400000)
predL2=stack_L2(None,*pL2); off=0; L2r2=[]
for (V,D) in data:
    pr=predL2[off:off+len(D)]; off+=len(D); L2r2.append(r2(D,pr))
UL2=np.array(pL2[:NT]); wL2=np.array(pL2[NT:2*NT])*1000

# ---- P2 부트스트랩 UQ on L2 (잔차 재표집) ----
resid=[]; off=0
for (V,D) in data: resid.append(D-predL2[off:off+len(D)]); off+=len(D)
NB=120; bootU=[]; bootw=[]
for b in range(NB):
    synth=[]
    for ci,(V,D) in enumerate(data):
        rr=rng.choice(resid[ci],size=len(D),replace=True); synth.append(predL2[sum(len(d) for _,d in data[:ci]):sum(len(d) for _,d in data[:ci+1])]+rr)
    yb=np.concatenate(synth)
    try:
        pb,_=curve_fit(stack_L2,None,yb,p0=pL2,bounds=(lo,hi),maxfev=60000)
        bootU.append(pb[:NT]); bootw.append(np.array(pb[NT:2*NT])*1000)
    except Exception: pass
bootU=np.array(bootU); bootw=np.array(bootw)
Ucv=[np.std(bootU[:,j])*1000 for j in range(NT)]  # U 표준편차(mV)
wcv=[np.std(bootw[:,j])/max(np.mean(bootw[:,j]),1e-9)*100 for j in range(NT)]  # w CV%

# ---- P3 이종소재 U_j 보편성 ----
mats=[("SINTEF-1",data[0]),("SINTEF-2",data[1]),
      ("Enertech",dqdv_ocp(f"{OCP}/gr_Enertech_Ai2020.csv")),
      ("Chen-LGM50",dqdv_ocp(f"{OCP}/gr_Chen2020_LGM50.csv")),
      ("PyBEP",dqdv_ocp(f"{OCP}/gr_PyBEP_xcrp2020.txt"))]
def peakU(V,D):  # 주 전이 피크 위치(2↔1·2L↔2·3↔2L 영역)
    d=np.asarray(D); pk,_=find_peaks(d,height=0.12*np.nanmax(d),prominence=0.05*np.nanmax(d))
    return sorted(V[pk])
matU={}
for nm,(V,D) in mats: matU[nm]=peakU(V,D)

print("=== P1 동일소재(SINTEF Gr-AQ-1) 2셀 계층 일관성 ===")
print(f"L0 자유    R²={[round(x,3) for x in L0r2]}  w_j(mV) 셀1={[round(x,2) for x in L0w[0]]} 셀2={[round(x,2) for x in L0w[1]]}")
print(f"  자유 w 셀간 상대편차={[f'{abs(L0w[0][j]-L0w[1][j])/max(np.mean(L0w[:,j]),1e-9)*100:.0f}%' for j in range(NT)]}  ← 아티팩트")
print(f"L2 단일셋  R²={[round(x,3) for x in L2r2]}  공유 U_j(V)={[round(x,4) for x in UL2]}  공유 w_j(mV)={[round(x,2) for x in wL2]}")
print(f"  → L2 R² ≈ L0 R² 이면 단일 물리셋이 전 셀 설명(일관·산업사용가능): ΔR²={[round(L2r2[i]-L0r2[i],3) for i in range(NC)]}")
print(f"=== P2 부트스트랩 UQ(N={len(bootU)}) — 식별성 ===")
print(f"  U_j 불확실(±mV)={[round(x,2) for x in Ucv]}  (작을수록 잘 식별)")
print(f"  w_j 불확실(CV%)={[round(x,0) for x in wcv]}  (큰 값=축퇴/평탄영역)")
print(f"=== P3 이종소재 U_j 보편성 ===")
for nm in matU: print(f"  {nm:12s}: {[round(x,3) for x in matU[nm]]}")

# 주 전이별 소재간 U 표준편차(2↔1≈0.10·2L↔2≈0.12·3↔2L≈0.14 근처 매칭)
targets=[0.105,0.120,0.143]  # 관측 흑연 3 주피크(delith)
spread={}
for tU in targets:
    vals=[min(us,key=lambda u:abs(u-tU)) for us in matU.values() if us]
    vals=[v for v in vals if abs(v-tU)<0.02]
    if len(vals)>=3: spread[f'{tU:.3f}V']=(np.mean(vals),np.std(vals)*1000)
print(f"  주피크 소재간 위치 평균±σ(mV): {{{', '.join(f'{k}:{v[0]:.3f}±{v[1]:.1f}' for k,v in spread.items())}}}  ← σ 작으면 staging 화학불변")

# ===== 그림 =====
fig,ax=plt.subplots(1,3,figsize=(18,5.2))
off=0
for ci,(V,D) in enumerate(data):
    ax[0].plot(V,D,lw=1.4,alpha=.75,label=f'실측 셀{ci+1}')
    pr=predL2[off:off+len(D)]; off+=len(D); ax[0].plot(V,pr,'--',lw=1.1,label=f'L2단일셋 셀{ci+1} R²={L2r2[ci]:.3f}')
ax[0].set_title('P1: 단일 물리셋(U·w 공유) 전역피팅\n동일소재 2셀'); ax[0].set_xlabel('V'); ax[0].set_ylabel('dQ/dV'); ax[0].legend(fontsize=8); ax[0].grid(alpha=.3)
x=np.arange(NT); ax[1].bar(x-0.25,L0w[0],0.2,label='자유 셀1'); ax[1].bar(x-0.05,L0w[1],0.2,label='자유 셀2'); ax[1].bar(x+0.18,wL2,0.2,color='k',label='L2 공유')
ax[1].errorbar(x+0.18,wL2,yerr=[np.std(bootw[:,j]) for j in range(NT)],fmt='none',ecolor='r',capsize=3,label='부트 ±σ')
ax[1].set_xticks(x); ax[1].set_xticklabels([f'전이{j+1}\n{UL2[j]:.3f}V' for j in range(NT)],fontsize=8); ax[1].set_ylabel('w_j / mV'); ax[1].set_title('P1·P2: w_j 자유(비일관) vs 단일셋(+UQ)'); ax[1].legend(fontsize=7); ax[1].grid(alpha=.3)
cmap=plt.cm.viridis(np.linspace(0,1,len(mats)))
for (nm,(V,D)),c in zip(mats,cmap):
    ax[2].plot(V,D/np.nanmax(D),color=c,lw=1.2,label=nm)
    for u in matU[nm]: ax[2].axvline(u,color=c,ls=':',lw=.6,alpha=.5)
ax[2].set_title('P3: 이종 5흑연 dQ/dV(정규화)\nU_j 위치 화학불변 검증'); ax[2].set_xlabel('V'); ax[2].set_ylabel('dQ/dV(정규화)'); ax[2].legend(fontsize=8); ax[2].grid(alpha=.3)
fig.tight_layout(); fig.savefig(f"{OUT}/consistency2.png",dpi=120); print("saved consistency2.png")
json.dump({"L0_r2":L0r2,"L0_w_mV":L0w.tolist(),"L2_r2":L2r2,"L2_U":UL2.tolist(),"L2_w_mV":wL2.tolist(),
           "boot_U_sd_mV":Ucv,"boot_w_cv_pct":wcv,"matU":matU,"peak_spread":spread},
          open(f"{OUT}/consistency2_result.json","w"),indent=1,default=float)
