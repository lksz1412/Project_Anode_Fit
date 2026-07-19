# -*- coding: utf-8 -*-
"""v1.0.24 V4-온도 — 문건 가역 엔트로피 계수 ∂U/∂T=ΔS_rxn/F 실측 검증.
데이터: O'Regan 2022(Zenodo 5171874) 흑연-SiOx 음극 entropic term(측정 dU/dT vs x, 다온도 유도).
검증: 출하 entropy_coefficient_x(x,T) 가 측정 dU/dT(x) 를 재현하나. (1)기본값(GRAPHITE_STAGING_LIT
  ΔS_rxn=+29/0/-5/-16 placeholder) 대조, (2)ΔS_rxn 피팅 시 machinery 가 측정곡선 재현하나.
"""
import numpy as np, pandas as pd, importlib.util, sys, glob, warnings; warnings.filterwarnings("ignore")
sys.path.insert(0,"/home/user/Project_Anode_Fit/Claude/results/comp_v24")
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from scipy.optimize import least_squares
OR="/tmp/claude-0/-home-user-Project-Anode-Fit/e8d4cdbc-60e6-548e-b742-1446b8f7a8bd/scratchpad/oregan"
OUT="/home/user/Project_Anode_Fit/Claude/results/comp_v24"
af_s=importlib.util.spec_from_file_location("af","/home/user/Project_Anode_Fit/Claude/docs/v1.0.23/Anode_Fit_v1.0.23.py")
af=importlib.util.module_from_spec(af_s); af_s.loader.exec_module(af)
GR=af.GraphiteAnodeDischargeDQDV; LIT=af.GRAPHITE_STAGING_LIT

# --- O'Regan 측정 dU/dT ---
def load_ent(cell):
    f=glob.glob(f"{OR}/**/Entropic_Term_Negative_Electrode_Cell_{cell}.csv",recursive=True)[0]
    d=pd.read_csv(f); d=d.iloc[:,:2]; d.columns=['x','dudt']
    return d['x'].to_numpy(float), d['dudt'].to_numpy(float)
x1,e1=load_ent("001"); x2,e2=load_ent("002")
print("O'Regan x:",np.round(x1,3)[:6],"... dU/dT(mV/K):",np.round(e1,3)[:6])

# --- 문건 모델 entropy_coefficient_x ---
def model_dudt(trs, xg, T=298.15):
    g=GR(trs)
    out=[]
    for x in xg:
        try: out.append(float(g.entropy_coefficient_x(float(x),T))*1000.0)  # V/K→mV/K
        except Exception: out.append(np.nan)
    return np.array(out)

# 기본값(placeholder ΔS_rxn) — x 규약: O'Regan x=리튬화분율, 문건 x_bar=탈리튬분율 → 1-x 시도
xg=np.linspace(0.05,0.95,120)
dudt_default=model_dudt(LIT,xg)

# ΔS_rxn 피팅: 측정 dU/dT(x) 재현 (U_j=기본 유지, dS_rxn 만 자유) — machinery 검증
base=[dict(t) for t in LIT]
def build(dS):
    trs=[]
    for t,ds in zip(base,dS):
        tt=dict(t); tt['dS_rxn']=float(ds); trs.append(tt)
    return trs
# 측정은 탈리튬분율 축으로 뒤집어 맞춤(x_model=1-x_oregan)
xm1=1.0-x1
def resid(dS):
    pred=model_dudt(build(dS), xm1)
    return np.nan_to_num(pred-e1, nan=0.0)
sol=least_squares(resid,[29.0,0.0,-5.0,-16.0],bounds=([-80]*4,[80]*4),max_nfev=300)
dS_fit=sol.x
pred_fit=model_dudt(build(dS_fit), xm1)
ss=1-np.nansum((e1-pred_fit)**2)/np.nansum((e1-np.nanmean(e1))**2)
print("기본 ΔS_rxn:",[t['dS_rxn'] for t in LIT])
print("피팅 ΔS_rxn:",[round(float(x),1) for x in dS_fit],f" R²(측정 dU/dT)={ss:.3f}")

fig,ax=plt.subplots(1,2,figsize=(14,5.4))
# 좌: 측정 vs 기본값(placeholder)
ax[0].scatter(x1,e1,c='tab:blue',s=40,label="O'Regan cell1 (측정)")
ax[0].scatter(x2,e2,c='tab:cyan',s=40,label="O'Regan cell2")
ax[0].plot(1-xg,dudt_default,'--',color='tab:red',lw=1.4,label='문건 기본 ΔS_rxn(placeholder)')
ax[0].set_xlabel('x (리튬화분율)'); ax[0].set_ylabel('dU/dT / mV·K⁻¹'); ax[0].set_title('측정 vs 문건 기본값(placeholder ΔS_rxn)'); ax[0].legend(fontsize=8); ax[0].grid(alpha=.3)
# 우: ΔS_rxn 피팅
ax[1].scatter(x1,e1,c='tab:blue',s=40,label="O'Regan 측정")
ax[1].plot(x1,pred_fit,'--',color='k',lw=1.5,label=f'문건 FIT(ΔS_rxn) R²={ss:.3f}')
ax[1].set_xlabel('x (리튬화분율)'); ax[1].set_ylabel('dU/dT / mV·K⁻¹'); ax[1].set_title('문건 entropy_coefficient machinery ΔS_rxn 피팅'); ax[1].legend(fontsize=8); ax[1].grid(alpha=.3)
fig.tight_layout(); fig.savefig(f"{OUT}/temperature_entropy.png",dpi=120); print("saved temperature_entropy.png")
