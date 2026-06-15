# -*- coding: utf-8 -*-
"""anode_fit_lib 함수들이 그리는 그래프 개형 샘플 (4 그림).
실행: python plot_samples.py  → fig1~fig4 PNG 저장."""
import sys
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

from anode_fit_lib import (R, F, xi_eq, bell, peak_dQdV, electrode_dQdV,
                           electrode_QV, invert_QV, ln_Lq, L_V_from_Lq,
                           build_electrode_curves, full_cell_from_electrodes)

T0 = 298.15
RT0 = R * T0

# ============================================================
# 그림 1 — 단일 상전이 peak 의 해부 (x축 = V 전위)
# ============================================================
fig, ax = plt.subplots(1, 3, figsize=(15, 4.2))
V = np.arange(40.0, 260.0, 0.1)
U, Q = 120.0, 0.4

# (a) 평형 peak (bell) — 폭 w 변화, 면적 Q 동일  [(1.50)/(1.51)]
for w in [8, 15, 25]:
    ax[0].plot(V, bell(V, U, w, Q), label=f"w={w} mV (정점 Q/4w={Q/(4*w):.3f})")
ax[0].axvline(U, color='gray', ls=':', lw=0.8)
ax[0].set_title("(a) 평형 peak = logistic 미분 (1.50)\n폭 w↓ → 좁고 높음 (면적 Q 보존)")
ax[0].set_xlabel("V  (전위, mV vs Li)"); ax[0].set_ylabel("dQ/dV"); ax[0].legend(fontsize=8)

# (b) bell + tail — 꼬리 잔류 r_a 변화, 면적 보존  [(1.79)/(1.80)]
for ra in [0.0, 0.2, 0.4, 0.6]:
    tr = dict(U=U, w=10.0, Q=Q, r_a=ra, V_a=150.0, L_V=30.0)
    ax[1].plot(V, peak_dQdV(V, tr), label=f"r_a={ra}")
ax[1].axvline(150.0, color='gray', ls=':', lw=0.8)
ax[1].annotate("꼬리 점화점 $V_a$", (150, 0.002), fontsize=8, color='gray')
ax[1].set_title("(b) 종 + 꼬리 = 닫힌식 (1.79)\nr_a↑ → 종 (1−r_a) 깎이고 꼬리 자람 (면적 Q 보존)")
ax[1].set_xlabel("V  (전위, mV vs Li)"); ax[1].set_ylabel("dQ/dV"); ax[1].legend(fontsize=8)

# (c) 꼬리 길이 L_V 변화, r_a 동일  [(1.63)]
for lv in [12, 25, 50]:
    tr = dict(U=U, w=10.0, Q=Q, r_a=0.4, V_a=150.0, L_V=lv)
    ax[2].plot(V, peak_dQdV(V, tr), label=f"L_V={lv} mV")
ax[2].set_title("(c) 꼬리 길이 $L_V$ (1.63)\n$L_V$↑ → 길고 낮은 꼬리 (진폭 $r_a/L_V$)")
ax[2].set_xlabel("V  (전위, mV vs Li)"); ax[2].set_ylabel("dQ/dV"); ax[2].legend(fontsize=8)
plt.tight_layout(); plt.savefig("fig1_single_peak.png", dpi=110); plt.close()
print("fig1 저장")

# ============================================================
# 그림 2 — 세 인자(온도·C-rate) 의존 (x축 = V). 물리 스케일 (ln_Lq).
# ============================================================
fig, ax = plt.subplots(1, 2, figsize=(11, 4.2))
U, w, Q = 120.0, 10.0, 0.40
Va = U + 22.0                     # 꼬리 컷점 (전형 배치)
dHa, chi = 42000.0, 0.5           # 활성화 엔탈피 [J/mol], 전달계수
dVdq = 120.0                      # 국소 |dV_n/dq| (mV per q-unit, 전형)
A_d = F * (Va - U) / 1000.0       # 구동력 [J/mol]
# 자기일관 b: 25℃·0.1C 에서 목표 L_q0=0.03 이 되도록 (문건 §1.17 경고 — 임의 b 금지)
Qcell, I_ref = 1.0, 0.1 / 3600.0  # 0.1C → rate [1/s]
b = np.log(0.03) - ln_Lq(T0, I_ref, Qcell, dHa, 0.0, chi, A_d)

def peak_at(T, rate_C):
    I_abs = rate_C / 3600.0
    Lq = np.exp(ln_Lq(T, I_abs, Qcell, dHa, b, chi, A_d))
    Lv = L_V_from_Lq(Lq, dVdq)
    ra = min(0.7, 6.0 * Lq)        # 잔류 지연도 L_q 와 함께 증가 (저온·고율서 큼)
    return peak_dQdV(V, dict(U=U, w=w, Q=Q, r_a=ra, V_a=Va, L_V=Lv)), Lv, ra

V = np.arange(60.0, 320.0, 0.1)
# (a) 온도 T↓ → 꼬리 길어짐 (서론의 '저온 긴 꼬리')
for T, c in zip([318.15, 298.15, 288.15], ['C0', 'C1', 'C2']):
    y, Lv, ra = peak_at(T, 0.2)
    ax[0].plot(V, y, color=c, label=f"{T-273.15:.0f}℃  (L_V={Lv:.0f}mV, r_a={ra:.2f})")
ax[0].set_title("(a) 온도 의존 (0.2C 고정)\n저온 → 꼬리 길고 낮음 = '저온 긴 꼬리'")
ax[0].set_xlabel("V  (전위, mV vs Li)"); ax[0].set_ylabel("dQ/dV"); ax[0].legend(fontsize=8)

# (b) C-rate |I|↑ → 꼬리 길어짐
for rc, c in zip([0.1, 0.3, 1.0], ['C0', 'C1', 'C2']):
    y, Lv, ra = peak_at(298.15, rc)
    ax[1].plot(V, y, color=c, label=f"{rc}C  (L_V={Lv:.0f}mV, r_a={ra:.2f})")
ax[1].set_title("(b) C-rate 의존 (25℃ 고정)\n고율 → 꼬리 길어짐 ($L_V\\propto|I|$)")
ax[1].set_xlabel("V  (전위, mV vs Li)"); ax[1].set_ylabel("dQ/dV"); ax[1].legend(fontsize=8)
plt.tight_layout(); plt.savefig("fig2_three_factors.png", dpi=110); plt.close()
print("fig2 저장")

# ============================================================
# 그림 3 — 전극 = peak 들의 합 (흑연 음극). dQ/dV 와 OCV 곡선.
# ============================================================
fig, ax = plt.subplots(1, 2, figsize=(11, 4.2))
AN_TRS = [dict(U=210.0, w=18.0, Q=0.15), dict(U=120.0, w=10.0, Q=0.40),
          dict(U=85.0, w=8.0, Q=0.35)]
Cbg = 0.0002
Vg = np.arange(30.0, 320.0, 0.1)
# (a) dQ/dV = C_bg + Σ peak  [(1.82)]
g = electrode_dQdV(Vg, AN_TRS, Cbg)
ax[0].plot(Vg, g, 'k', lw=1.6, label="전극 dQ/dV (합)")
for tr in AN_TRS:
    ax[0].plot(Vg, electrode_dQdV(Vg, [tr], 0.0), '--', lw=0.9,
               label=f"전이 U={tr['U']:.0f}, Q={tr['Q']}")
ax[0].axhline(Cbg, color='gray', ls=':', lw=0.8)
ax[0].set_title("(a) 흑연 음극 dQ/dV = 배경 + 상전이 peak 합 (1.82)\n(x축 = V)")
ax[0].set_xlabel("V  (전위, mV vs Li)"); ax[0].set_ylabel("dQ/dV"); ax[0].legend(fontsize=8)

# (b) OCV 곡선 V(Q) — electrode_QV 적분 후 표시 (x=Q, y=V)
Qv = electrode_QV(Vg, AN_TRS, Cbg, Q0=0.0)
ax[1].plot(Qv, Vg, 'k', lw=1.6)
for tr in AN_TRS:
    ax[1].axhline(tr['U'], color='gray', ls=':', lw=0.7)
ax[1].set_title("(b) 같은 전극의 OCV 곡선 V(Q) = ∫dQ/dV 의 역 (1.42/1.47)\n(x축 = Q) — peak = OCV 평탄부")
ax[1].set_xlabel("Q  (용량, /Q_cell)"); ax[1].set_ylabel("V  (전위, mV vs Li)")
plt.tight_layout(); plt.savefig("fig3_electrode.png", dpi=110); plt.close()
print("fig3 저장")

# ============================================================
# 그림 4 — 풀셀 분해 (LCO/흑연). x축 = Q. 핵심 그림.
# ============================================================
fig, ax = plt.subplots(1, 3, figsize=(16, 4.4))
CT_TRS = [dict(U=3930.0, w=55.0, Q=0.60), dict(U=4070.0, w=12.0, Q=0.12),
          dict(U=4180.0, w=12.0, Q=0.10)]
V_AN = np.arange(30.0, 335.0, 0.25); V_CT = np.arange(3820.0, 4270.0, 0.25)
AN = build_electrode_curves(V_AN, AN_TRS, 0.0001, +1.0, 1.0, 0.0, reverse=True)  # 음극 반전(물리)
CT = build_electrode_curves(V_CT, CT_TRS, 0.0001, +1.0, 1.0, 0.03)
Qg = np.linspace(0.05, 0.85, 400)
fc = full_cell_from_electrodes(Qg, AN, CT)
m = fc['valid']; Qm = Qg[m]
iV_AN = np.interp(Qm, AN[0], AN[1]); iV_CT = np.interp(Qm, CT[0], CT[1])
id_AN = np.interp(Qm, AN[0], AN[2]); id_CT = np.interp(Qm, CT[0], CT[2])

# (a) 전극 전위 + 풀셀 전위
ax[0].plot(Qm, iV_CT, 'C3', label="양극 LCO  $V_{CT}$")
ax[0].plot(Qm, iV_AN, 'C0', label="음극 흑연  $V_{AN}$")
ax[0].plot(Qm, fc['V_FC'][m], 'k', lw=1.8, label="풀셀  $V_{FC}=V_{CT}-V_{AN}$")
ax[0].set_title("(a) 풀셀 전위 = 양극 − 음극 (x축 = Q)")
ax[0].set_xlabel("Q  (용량)"); ax[0].set_ylabel("V  (mV vs Li / 풀셀)"); ax[0].legend(fontsize=8)

# (b) dV/dQ: 양극·음극·풀셀
ax[1].plot(Qm, id_CT, 'C3', lw=0.9, label="양극 dV/dQ")
ax[1].plot(Qm, id_AN, 'C0', lw=0.9, label="음극 dV/dQ")
ax[1].plot(Qm, fc['dVdQ_FC'][m], 'k', lw=1.4, label="풀셀 dV/dQ = CT − AN")
ax[1].set_title("(b) dV/dQ 분해 (x축 = Q)\n풀셀 = 양극 − 음극")
ax[1].set_xlabel("Q  (용량)"); ax[1].set_ylabel("dV/dQ"); ax[1].legend(fontsize=8)

# (c) dQ/dV 풀셀 (ICA) — 양·음극 peak 가 함께 보임
ax[2].plot(Qm, fc['dQdV_FC'][m], 'k', lw=1.4)
ax[2].set_title("(c) 풀셀 dQ/dV = 1/(dV/dQ) (x축 = Q)\n양·음극 상전이 peak 가 함께 출현")
ax[2].set_xlabel("Q  (용량)"); ax[2].set_ylabel("dQ/dV (풀셀)")
plt.tight_layout(); plt.savefig("fig4_fullcell.png", dpi=110); plt.close()
print("fig4 저장")
print("완료 — fig1~fig4 PNG")
