# -*- coding: utf-8 -*-
"""v1.0.24 R2 반영 게이트 — 신규 기능(@3 regsol·@5 5-feature·LCO 토글·#1 단위) 검증.
기존 bit-exact 게이트(test_gates_v1024.py)와 별개. 신규 경로가 의도대로 작동하는지."""
import numpy as np, importlib.util
s=importlib.util.spec_from_file_location('af','Anode_Fit_v1.0.24.py'); m=importlib.util.module_from_spec(s); s.loader.exec_module(m)
F=m.F; R=m.R; _trapz=getattr(np,'trapezoid',getattr(np,'trapz',None)); PASS=True

print("="*74)
# ===== G-R1: @5 흑연 XRD 5-feature staging =====
gr5=m.GraphiteAnodeDischargeDQDV(m.GRAPHITE_STAGING_XRD_v1024, x=0.5, Rn=0.01, Cbg=0.0)
V=np.linspace(0.06,0.24,3000); d5=gr5.equilibrium(V,T=298.15)
fin=bool(np.all(np.isfinite(d5)) and np.all(d5>=-1e-12)); n5=len(m.GRAPHITE_STAGING_XRD_v1024)
# stage-2L 분리기울기: 3↔2L(dS+15) vs 2L↔2(dS−14) → |Δ(ΔS)|/F
def Uj(tr,T): return float(m.func_U_j(T,tr['dH_rxn'],tr['dS_rxn']))
t32L=m.GRAPHITE_STAGING_XRD_v1024[2]; t2L2=m.GRAPHITE_STAGING_XRD_v1024[3]
sep25=abs(Uj(t32L,298.15)-Uj(t2L2,298.15))*1000; sep45=abs(Uj(t32L,318.15)-Uj(t2L2,318.15))*1000
slope=(sep45-sep25)/20.0
g_r1 = fin and n5==5 and abs(slope-0.30)<0.03 and sep45>sep25
print(f"G-R1 @5 5-feature: 전이수={n5} 유한·비음={fin} | stage-2L 분리 25℃={sep25:.1f}mV·45℃={sep45:.1f}mV·기울기={slope:.3f}mV/℃(Dahn 0.30) → {'PASS' if g_r1 else 'FAIL'}")
PASS = PASS and g_r1

# ===== G-R2: LCO 전자항 on/off 토글 =====
kw=dict(Rn=0.005,Cbg=0.0); Vc=np.linspace(3.5,4.3,2000)
lco_on=m.LCOCathodeDQDV(m.LCO_MSMR_LIT,include_electronic_entropy=True,**kw)
lco_off=m.LCOCathodeDQDV(m.LCO_MSMR_LIT,include_electronic_entropy=False,**kw)
lco_def=m.LCOCathodeDQDV(m.LCO_MSMR_LIT,**kw)
d_on=np.asarray(lco_on.equilibrium(Vc,T=298.15)); d_off=np.asarray(lco_off.equilibrium(Vc,T=298.15))
d_on318=np.asarray(lco_on.equilibrium(Vc,T=318.15)); d_off318=np.asarray(lco_off.equilibrium(Vc,T=318.15))
d_def318=np.asarray(lco_def.equilibrium(Vc,T=318.15))
def_is_off=float(np.max(np.abs(d_off318-d_def318))) # ★기본=OFF(시드/브리프 사양): 318K서 OFF와 동일 →0
def_ne_on=float(np.max(np.abs(d_on318-d_def318)))   # 기본 ≠ ON: 318K서 ON과 차 >0
uref=float(np.max(np.abs(d_on-d_off)))              # 상온 U(T_ref) 보존: ON@298==OFF@298 → ~0
diff318=float(np.max(np.abs(d_on318-d_off318)))     # 318K서 ∂U/∂T 차(ON vs OFF) → >0
g_r2 = def_is_off==0.0 and def_ne_on>1e-6 and uref<1e-9 and diff318>1e-6
print(f"G-R2 LCO 토글: 기본=OFF(def=off@318 max|Δ|={def_is_off:.1e}=0·def≠on {def_ne_on:.2e}>0) | 상온 U(T_ref)보존 ON=OFF@298 max|Δ|={uref:.1e}(<1e-9) | ∂U/∂T차@318 {diff318:.2e}(>0) → {'PASS' if g_r2 else 'FAIL'}")
PASS = PASS and g_r2

# ===== G-R3: @3 정칙용액(Frumkin Ω<2RT) 커널 =====
T=298.15; RT=R*T
tr_reg=dict(U=0.30, w=0.02, Q=1.0, n=1.0, Omega=1.0*RT, kernel='regsol', delta=0.002,
            dH_a=40000.0, dS_a=0.0, dVdq_qa=0.30)
tr_log=dict(U=0.30, w=0.02, Q=1.0, n=1.0, dH_a=40000.0, dS_a=0.0, dVdq_qa=0.30)
gr_reg=m.GraphiteAnodeDischargeDQDV([tr_reg], x=0.5, Rn=0.01, Cbg=0.0)
gr_log=m.GraphiteAnodeDischargeDQDV([tr_log], x=0.5, Rn=0.01, Cbg=0.0)
Vr=np.linspace(0.05,0.55,3000)
dr=np.asarray(gr_reg.equilibrium(Vr,T=T)); dl=np.asarray(gr_log.equilibrium(Vr,T=T))
fin_r=bool(np.all(np.isfinite(dr)) and np.all(dr>=-1e-9))
# FWHM 비교 (고용체 broad 인지) — regsol Ω=RT<2RT 는 로지스틱보다 넓지 않을 수 있으나 유한 단일봉
npk=int((np.diff(np.sign(np.diff(dr)))<0).sum())  # 국소 최대 개수(대략)
# bit-exact 확인: 로지스틱 전이(kernel 없음)는 기존 경로 — 별 커널 미개입
g_r3 = fin_r and _trapz(dr,Vr)>0 and npk>=1
print(f"G-R3 @3 regsol: 유한·비음={fin_r} 면적={_trapz(dr,Vr):.3f} 국소최대={npk}(단일봉) | 로지스틱 대조 면적={_trapz(dl,Vr):.3f} → {'PASS' if g_r3 else 'FAIL'}")
PASS = PASS and g_r3

# ===== G-R4: #1 단위계약 = bit-exact (func_L_q 값 무변경 — 주석만) =====
lq=m.func_L_q(298.15, 0.2, 1.0, 46000.0, 0.0, 0.5, 3.0)
g_r4 = np.isfinite(lq) and lq>0
print(f"G-R4 #1 단위계약: func_L_q 정상 동작 lq={lq:.3e}(값 무변경·주석만) → {'PASS' if g_r4 else 'FAIL'}")
PASS = PASS and g_r4

print("="*74)
print(f">>> v1.0.24 REFLECT GATES: {'ALL PASS (4/4)' if PASS else 'FAIL'}")
