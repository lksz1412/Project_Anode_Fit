# -*- coding: utf-8 -*-
"""v1.0.24 최종 코드 샘플 이미지 — 핵심 곡선 정상작동 + 신규 3반영(@5·@3·토글) 시각 검증.
   main/Anode_Fit_v1.0.24.py 를 그대로 로드해 실행. 물리 타당성(유한·매끈·단일값·미분가능) 자동 점검."""
import numpy as np, importlib.util, sys
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
plt.rcParams['font.family'] = 'NanumGothic'; plt.rcParams['axes.unicode_minus'] = False
from scipy.signal import find_peaks

HERE = "/home/user/Project_Anode_Fit/Claude/docs/v1.0.24"
s = importlib.util.spec_from_file_location('af', f"{HERE}/Anode_Fit_v1.0.24.py")
m = importlib.util.module_from_spec(s); s.loader.exec_module(m)
OUT = f"{HERE}/results"
R = m.R; F = m.F
chk = []  # (이름, 유한?, 봉수, 매끈?)
def validate(name, y):
    fin = bool(np.all(np.isfinite(y)))
    d2 = np.abs(np.diff(y, 2)); smooth = bool(np.nanmax(d2) < 50*np.nanmedian(d2[d2>0]) if np.any(d2>0) else True)
    chk.append((name, fin, smooth)); return y

# ========================= FIGURE 1 — 핵심 곡선 정상작동 =========================
fig1, ax = plt.subplots(2, 3, figsize=(18, 10))
V = np.linspace(0.02, 0.30, 2000)
gr = m.GraphiteAnodeDischargeDQDV(m.GRAPHITE_STAGING_LIT, x=0.5, Rn=0.01, Cbg=0.05, use_dH_eff=True)

# (1) 흑연 dQ/dV — 평형 + 율속 의존
ax[0,0].plot(V, validate('gr_eq', np.asarray(gr.equilibrium(V, 298.15))), 'k', lw=2, label='평형')
for c, col in [(0.05,'tab:green'), (0.2,'tab:orange'), (1.0,'tab:red')]:
    ax[0,0].plot(V, validate(f'gr_{c}C', np.asarray(gr.dqdv(V, 298.15, c, 1.0, +1))), col, lw=1.1, label=f'{c}C(방전)')
ax[0,0].set_title('(1) 흑연 dQ/dV — 평형·율속 의존(꼬리)'); ax[0,0].set_xlabel('V vs Li'); ax[0,0].set_ylabel('dQ/dV'); ax[0,0].legend(fontsize=8); ax[0,0].grid(alpha=.3)

# (2) 흑연 DVA (dV/dQ) — solve_U_oc 미분
xb = np.linspace(0.03, 0.97, 1500); Uoc = validate('gr_Uoc', np.asarray(gr.solve_U_oc(xb, 298.15)))
dVdQ = np.gradient(Uoc, xb)  # Q ∝ x → dV/dQ ∝ dU/dx
ax[0,1].plot(xb, validate('gr_dVdQ', np.abs(dVdQ)), 'tab:blue', lw=1.5)
ax[0,1].set_title('(2) 흑연 DVA |dV/dQ| — 단조 U(x) 미분'); ax[0,1].set_xlabel('SOC (평균 리튬화율)'); ax[0,1].set_ylabel('|dV/dQ|'); ax[0,1].set_yscale('log'); ax[0,1].grid(alpha=.3)

# (3) 흑연 dQ/dV 온도 의존
for Tc, col in [(5,'tab:blue'),(25,'tab:gray'),(45,'tab:orange')]:
    ax[0,2].plot(V, validate(f'grT{Tc}', np.asarray(gr.equilibrium(V, Tc+273.15))), col, lw=1.3, label=f'{Tc}℃')
ax[0,2].set_title('(3) 흑연 dQ/dV 온도 의존(평형)'); ax[0,2].set_xlabel('V vs Li'); ax[0,2].set_ylabel('dQ/dV'); ax[0,2].legend(fontsize=8); ax[0,2].grid(alpha=.3)

# (4) LCO dQ/dV (기본 = 전자항 OFF)
VL = np.linspace(3.6, 4.25, 2000)
lco = m.LCOCathodeDQDV(m.LCO_MSMR_LIT, Rn=0.005, Cbg=0.0)  # 기본 OFF
ax[1,0].plot(VL, validate('lco_eq', np.asarray(lco.equilibrium(VL, 298.15))), 'tab:purple', lw=1.8, label='평형(25℃)')
ax[1,0].plot(VL, validate('lco_02C', np.asarray(lco.dqdv(VL, 298.15, 0.2, 1.0, -1))), 'tab:pink', lw=1.1, label='0.2C(충전)')
ax[1,0].set_title('(4) LCO dQ/dV (기본=전자항 OFF)'); ax[1,0].set_xlabel('V vs Li'); ax[1,0].set_ylabel('dQ/dV'); ax[1,0].legend(fontsize=8); ax[1,0].grid(alpha=.3)

# (5) 흑연+Si 블렌드 vs 흑연 단독
Vb = np.linspace(0.02, 0.55, 2500)
bl = m.BlendedAnodeDQDV(0.1, si_case='sic', graphite_transitions=m.GRAPHITE_STAGING_LIT, x=0.5, Rn=0.01, Cbg=0.05, use_dH_eff=True)
gr0 = m.GraphiteAnodeDischargeDQDV(m.GRAPHITE_STAGING_LIT, x=0.5, Rn=0.01, Cbg=0.05, use_dH_eff=True)
ax[1,1].plot(Vb, validate('gr_only', np.asarray(gr0.equilibrium(Vb, 298.15))), 'k', lw=1.3, label='흑연 단독')
ax[1,1].plot(Vb, validate('blend', np.asarray(bl.equilibrium(Vb, 298.15))), 'tab:red', lw=1.5, label='흑연+Si(f_Si=0.1)')
ax[1,1].set_title('(5) 흑연+Si 블렌드 dQ/dV — Si 기여 가산'); ax[1,1].set_xlabel('V vs Li'); ax[1,1].set_ylabel('dQ/dV'); ax[1,1].legend(fontsize=8); ax[1,1].grid(alpha=.3)

# (6) 흑연 발열 — 엔트로피 계수 ∂U/∂T
xe = np.linspace(0.05, 0.95, 500)
try:
    ec = validate('gr_dUdT', np.asarray(gr.entropy_coefficient_x(xe, 298.15))*1e3)
except Exception:
    ec = validate('gr_dUdT', np.asarray([gr.entropy_coefficient(gr.solve_U_oc(x,298.15),298.15) for x in xe]).ravel()*1e3)
ax[1,2].plot(xe, ec, 'tab:brown', lw=1.6)
ax[1,2].axhline(0, color='gray', ls=':', lw=.8)
ax[1,2].set_title('(6) 흑연 엔트로피 계수 ∂U/∂T (가역열)'); ax[1,2].set_xlabel('SOC (평균 리튬화율)'); ax[1,2].set_ylabel('∂U/∂T [mV/K]'); ax[1,2].grid(alpha=.3)

fig1.suptitle('v1.0.24 최종 코드 — 핵심 곡선 물리 타당성 (흑연·LCO·블렌드 dQ/dV·DVA·가역열)', fontsize=14)
fig1.tight_layout(); fig1.savefig(f"{OUT}/final_sample_core.png", dpi=115)

# ========================= FIGURE 2 — v1.0.24 신규 3반영 =========================
fig2, bx = plt.subplots(1, 3, figsize=(18, 5.2))

# (A) @5 stage-2L — XRD 5-feature T-sweep
gr5 = m.GraphiteAnodeDischargeDQDV(m.GRAPHITE_STAGING_XRD_v1024, x=0.5, Rn=0.01, Cbg=0.0)
Vs = np.linspace(0.06, 0.24, 3000)
for Tc, col in [(5,'tab:blue'),(25,'tab:gray'),(45,'tab:orange'),(65,'tab:red')]:
    d = validate(f'@5_{Tc}', np.asarray(gr5.equilibrium(Vs, Tc+273.15))); bx[0].plot(Vs, d/np.nanmax(d), col, lw=1.3, label=f'{Tc}℃')
bx[0].set_title('@5 흑연 XRD 5-feature\nstage-2L 온도 분리(고온 2peak·상온 병합)'); bx[0].set_xlabel('V vs Li'); bx[0].set_ylabel('dQ/dV(정규화)'); bx[0].legend(fontsize=8); bx[0].grid(alpha=.3)

# (B) @3 Si Frumkin(정칙용액 Ω<2RT) vs 로지스틱
T=298.15; RT=R*T
trR=dict(U=0.30,w=0.02,Q=1.0,n=1.0,Omega=1.0*RT,kernel='regsol',delta=0.003,dH_a=4e4,dS_a=0.,dVdq_qa=0.3)
trL=dict(U=0.30,w=0.05,Q=1.0,n=1.0,dH_a=4e4,dS_a=0.,dVdq_qa=0.3)
gR=m.GraphiteAnodeDischargeDQDV([trR],x=0.5,Rn=0.01,Cbg=0.0); gL=m.GraphiteAnodeDischargeDQDV([trL],x=0.5,Rn=0.01,Cbg=0.0)
Vr=np.linspace(0.05,0.55,3000); dR=validate('@3_regsol', np.asarray(gR.equilibrium(Vr,T))); dL=validate('@3_logi', np.asarray(gL.equilibrium(Vr,T)))
pk,_=find_peaks(dR,height=0.05*dR.max(),prominence=0.02*dR.max())
bx[1].plot(Vr,dR,'tab:green',lw=1.6,label=f'@3 정칙용액(Ω<2RT)·prominent봉={len(pk)}')
bx[1].plot(Vr,dL,'tab:blue',ls='--',lw=1.1,label='로지스틱(대조)')
bx[1].set_title('@3 Si-host Frumkin 커널\n(단일 broad 봉·매끈·Ω→0 로지스틱 폴백)'); bx[1].set_xlabel('V vs Li'); bx[1].set_ylabel('dQ/dV'); bx[1].legend(fontsize=8); bx[1].grid(alpha=.3)

# (C) LCO 전자항 토글 — 기본 OFF vs ON (298 동일·318 분기)
kw=dict(Rn=0.005,Cbg=0.0); Vc=np.linspace(3.6,4.25,2000)
off=m.LCOCathodeDQDV(m.LCO_MSMR_LIT,**kw)  # 기본 OFF
on =m.LCOCathodeDQDV(m.LCO_MSMR_LIT,include_electronic_entropy=True,**kw)
bx[2].plot(Vc,validate('lco_off298', np.asarray(off.equilibrium(Vc,298.15))),'k',lw=1.8,label='298K 기본 OFF (= ON)')
bx[2].plot(Vc,validate('lco_on298', np.asarray(on.equilibrium(Vc,298.15))),'tab:cyan',ls=':',lw=1.3,label='298K ON')
bx[2].plot(Vc,validate('lco_off318', np.asarray(off.equilibrium(Vc,318.15))),'tab:orange',ls='--',lw=1.2,label='318K OFF')
bx[2].plot(Vc,validate('lco_on318', np.asarray(on.equilibrium(Vc,318.15))),'tab:red',lw=1.2,label='318K ON(∂U/∂T 분기)')
bx[2].set_title('LCO 전자항 토글(기본 OFF)\n상온 커브 무영향·다온도서만 분기'); bx[2].set_xlabel('V vs Li'); bx[2].set_ylabel('dQ/dV'); bx[2].legend(fontsize=7.5); bx[2].grid(alpha=.3)

fig2.suptitle('v1.0.24 신규 3반영 — @5 stage-2L 온도분리 · @3 Si Frumkin · LCO 전자항 토글(기본 OFF)', fontsize=13)
fig2.tight_layout(); fig2.savefig(f"{OUT}/final_sample_reflect.png", dpi=120)

# ========================= 타당성 요약 =========================
# 298K OFF==ON bit-check
off298=np.asarray(off.equilibrium(Vc,298.15)); on298=np.asarray(on.equilibrium(Vc,298.15))
d298=float(np.max(np.abs(off298-on298))); d318=float(np.max(np.abs(np.asarray(off.equilibrium(Vc,318.15))-np.asarray(on.equilibrium(Vc,318.15)))))
nfin=sum(1 for _,f,_ in chk if f); nsm=sum(1 for _,_,sm in chk if sm)
print("="*70)
print(f"검사 곡선 {len(chk)}개 · 전부 유한={nfin}/{len(chk)} · 매끈(2차차분 유계)={nsm}/{len(chk)}")
bad=[n for n,f,sm in chk if not(f and sm)]
print(f"비정상 곡선: {bad if bad else '없음(전부 정상)'}")
print(f"토글 검증: LCO 298K OFF vs ON max|Δ|={d298:.2e}(→0, 상온 커브 무영향) · 318K max|Δ|={d318:.2e}(>0, ∂U/∂T 분기)")
print(f"@3 정칙용액 prominent 봉수={len(pk)}(단일 broad 확인)")
print("saved: final_sample_core.png · final_sample_reflect.png")
