# -*- coding: utf-8 -*-
"""풀셀 분해 round-trip 실증 (계획 Phase 6, Test T5).

대상 셀 = LCO 기반 핸드폰용 파우치 셀 (흑연 음극 / LCO 양극). 사용자 명시.
알려진 θ* (음극 3 peak + 양극 3 peak + offset) 로 합성 풀셀을 만들고,
staged_fit (P1→P2→P3) 이 양·음극 분해를 회복하는지 본다.

★ loading=1 고정 (peak 면적 Q_j 가 용량을 담으므로 별도 loading 은 Q_j 와 공선형 —
  문건 §1.11 '식별의 원칙' 이 경고한 collinearity). 자유 정렬 = off_ct (slippage) 하나.
합격: 회복된 양·음극 전이(U,Q) 가 참값 근방 + 정렬 회복.
"""
import sys
import numpy as np
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

from anode_fit_lib import (build_electrode_curves, full_cell_from_electrodes,
                           pack_params, unpack_params, staged_fit)

rng = np.random.default_rng(20260616)

# ---------- 참값 θ* (LCO / 흑연 핸드폰 파우치 셀) ----------
# 음극 = 흑연 3 전이 (vs Li, mV) — staging LiC6/LiC12/Stage
AN_TRS = [dict(U=210.0, w=18.0, Q=0.15), dict(U=120.0, w=10.0, Q=0.40),
          dict(U=85.0,  w=8.0,  Q=0.35)]
# 양극 = LCO 3 전이 (vs Li, mV):
#   3930 = 주 육방정 plateau(큰 면적·broad), 4070 = 질서-무질서(sharp·소),
#   4180 = 단사정→육방정(sharp·소).
CT_TRS = [dict(U=3930.0, w=55.0, Q=0.60), dict(U=4070.0, w=12.0, Q=0.12),
          dict(U=4180.0, w=12.0, Q=0.10)]
CBG_AN, CBG_CT = 0.0001, 0.0001
OFF_AN, OFF_CT = 0.0, 0.03           # loading 은 1 고정(자유화 X)

V_AN = np.arange(30.0, 335.0, 0.25)   # 활성 범위로 한정(85~210 peak + 여유)
V_CT = np.arange(3820.0, 4270.0, 0.25)  # 3930~4180 peak + 여유

# ---------- 합성 풀셀 측정 ----------
AN_true = build_electrode_curves(V_AN, AN_TRS, CBG_AN, +1.0, 1.0, OFF_AN, reverse=True)  # 음극 반전(물리)
CT_true = build_electrode_curves(V_CT, CT_TRS, CBG_CT, +1.0, 1.0, OFF_CT)
Q_grid = np.linspace(0.04, 0.88, 360)   # 내부 overlap 전체 — 모든 peak interior
fc_true = full_cell_from_electrodes(Q_grid, AN_true, CT_true)
m = fc_true['valid']

def add_noise(arr, valid, frac=0.01):
    scale = frac * (np.nanmax(arr[valid]) - np.nanmin(arr[valid]))
    return arr + rng.normal(0, scale, size=arr.shape)

# 측정 = 잡음 추가한 전체 길이 배열, 단 overlap(valid) 밖은 NaN (미측정)
mV = add_noise(fc_true['V_FC'], m)
md = add_noise(fc_true['dVdQ_FC'], m)
meas_full = dict(V_FC=np.where(m, mV, np.nan), dVdQ_FC=np.where(m, md, np.nan))
meas = dict(V_FC=mV[m], dVdQ_FC=md[m])   # 스케일 계산용 (valid 점만)
print(f"LCO/흑연 합성 풀셀: 겹침점 {m.sum()},  V_FC=[{fc_true['V_FC'].min():.0f},{fc_true['V_FC'].max():.0f}] mV")

# ---------- 초기값 (참값 교란 — 검출 모사) ----------
def perturb(trs, dU=8.0, fw=0.25, fQ=0.25):
    return [dict(U=t['U'] + rng.uniform(-dU, dU),
                 w=t['w'] * (1 + rng.uniform(-fw, fw)),
                 Q=t['Q'] * (1 + rng.uniform(-fQ, fQ))) for t in trs]

an0, ct0 = perturb(AN_TRS), perturb(CT_TRS)
theta0 = pack_params(an0, ct0, 1.0, 0.0, 1.0, 0.0)   # load=1,1 / off_an=0 gauge
# ★ 전압 gauge anchor: 모든 위치 공통 δ 이동은 V_FC 불변(절대 기준 비식별) → 양극 주 peak
#   (LCO 3930mV, idx 9)를 반쪽셀 참조 진값에 고정해 gauge 잠금. 나머지는 그에 상대 결정.
theta0[9] = 3930.0
n_an, n_ct = 3, 3

# 인덱스: an 0..8, ct 9..17, load_an=18,off_an=19,load_ct=20,off_ct=21
idx_U = [0, 3, 6, 12, 15]      # idx 9(양극 주 peak) = gauge anchor 라 free 제외
idx_w = [1, 4, 7, 10, 13, 16]
idx_Q = [2, 5, 8, 11, 14, 17]
OFF_CT_IDX = 21

# 경계 — ★ 위치 U 는 검출 초기값 ±20mV 로 anchor (실제 워크플로: FC peak 검출로 위치 고정,
#   문건 §1.12 '저율로 고정 → 예측' 비순환 원칙. 위치를 풀어 놓으면 off 와 soft-gauge 결합).
N = len(theta0)
lb = np.full(N, -np.inf); ub = np.full(N, np.inf)
for k in idx_U:       lb[k], ub[k] = theta0[k] - 20.0, theta0[k] + 20.0   # 위치 anchor
for k in idx_w:       lb[k], ub[k] = 0.6 * theta0[k], 1.6 * theta0[k]     # 폭도 참조 상대 구속
# ★ 면적은 참조 초기값 ±40% 로 구속 (반쪽셀 참조가 면적을 그 정도로 안다 — 인접 peak 면적
#   붕괴/병합 방지. 무제약이면 120/85mV 인접 peak 분배가 비유일, §1.12).
for k in idx_Q:       lb[k], ub[k] = 0.6 * theta0[k], 1.6 * theta0[k]
lb[OFF_CT_IDX], ub[OFF_CT_IDX] = -0.08, 0.08            # off_ct (소 slippage)

# 3채널 스케일 정규화 (§1.16 (5) σ_i 가중)
sc_V = np.nanstd(meas['V_FC']); sc_d = np.nanstd(meas['dVdQ_FC'])
sc_q = np.nanstd(1.0 / meas['dVdQ_FC'])
# ★ coarse-to-fine 단계별 가중: 평활한 V_FC(=적분) 로 basin 진입 → 날카로운 dV/dQ(=미분)로
#   미세 정렬 → dQ/dV polish. (sharp LCO peak 의 dV/dQ 채널은 rugged landscape 라 거친 정렬엔 부적합.)
W_coarse = (5.0 / sc_V, 0.05 / sc_d, 0.0)        # V 지배 (basin 진입)
W_fine   = (1.0 / sc_V, 1.0 / sc_d, 0.0)         # V+dVdQ (sharp peak 정렬)
print(f"채널 스케일: V={sc_V:.1f} mV, dVdQ={sc_d:.1f}, dQdV={sc_q:.2e}")

# 비순환 coarse-to-fine 사슬. load(18,20)·off_an(19) 동결.
# ★ P1(V-only) 은 위치·정렬만 — 면적은 참조 초기값 동결(인접 peak 면적이 평활 V 에서 섞임 방지).
#   면적은 P2(dV/dQ, sharp 특징이 인접 peak 구분)에서 개방. (§1.12 비유일성 회피.)
stages = [
    ('P1 coarse align (V)', [OFF_CT_IDX] + idx_U,                 W_coarse),
    ('P2 +areas (dVdQ)',    idx_Q + [OFF_CT_IDX] + idx_U,         W_fine),
    ('P3 +widths',          idx_Q + [OFF_CT_IDX] + idx_U + idx_w, W_fine),
]

print("\n=== staged_fit (P1 coarse → P2 fine → P3 polish) ===")
res = staged_fit(V_AN, V_CT, Q_grid, meas_full, theta0, n_an, n_ct, stages,
                 Cbg_an=CBG_AN, Cbg_ct=CBG_CT, bounds=(lb, ub), verbose=True)

an_fit, ct_fit, la, oa, lc, oc = unpack_params(res['theta'], n_an, n_ct)

print("\n--- 정렬(slippage) 회복 (loading=1 고정) ---")
print(f"  off_ct {oc:.4f} vs {OFF_CT}")

ok_all = True
print("\n--- 음극(흑연) 전이 회복 ---")
for j, (tf, tt) in enumerate(zip(sorted(an_fit, key=lambda t: -t['U']),
                                 sorted(AN_TRS, key=lambda t: -t['U']))):
    dU, dQ = tf['U'] - tt['U'], tf['Q'] - tt['Q']
    print(f"  AN j={j+1}: U {tf['U']:6.1f} vs {tt['U']:5.0f} (d={dU:+.1f}) | "
          f"w {tf['w']:5.1f} vs {tt['w']:4.0f} | Q {tf['Q']:.3f} vs {tt['Q']:.2f} (d={dQ:+.3f})")
    ok_all = ok_all and abs(dU) < 15.0 and abs(dQ) < 0.05   # ill-posed 분해 정직 허용오차

print("\n--- 양극(LCO) 전이 회복 ---")
for j, (tf, tt) in enumerate(zip(sorted(ct_fit, key=lambda t: -t['U']),
                                 sorted(CT_TRS, key=lambda t: -t['U']))):
    dU, dQ = tf['U'] - tt['U'], tf['Q'] - tt['Q']
    print(f"  CT j={j+1}: U {tf['U']:7.1f} vs {tt['U']:6.0f} (d={dU:+.1f}) | "
          f"w {tf['w']:5.1f} vs {tt['w']:4.0f} | Q {tf['Q']:.3f} vs {tt['Q']:.2f} (d={dQ:+.3f})")
    ok_all = ok_all and abs(dU) < 15.0 and abs(dQ) < 0.05

# off_ct(절대 slippage) 는 단일 풀셀곡선서 ~1% softness (§1.11/§1.12 비유일성) — 정직 허용 0.015
ok_off = abs(oc - OFF_CT) < 0.015
print(f"\n  정렬 회복: {'OK' if ok_off else 'MISS'}  (off_ct d={oc-OFF_CT:+.4f})")
ok_all = ok_all and ok_off

# 재구성 풀셀 RMSE (분해가 측정을 재현하는가 — 가장 본질적 지표)
AN_f = build_electrode_curves(V_AN, an_fit, CBG_AN, +1.0, 1.0, oa, reverse=True)
CT_f = build_electrode_curves(V_CT, ct_fit, CBG_CT, +1.0, 1.0, oc)
fc_f = full_cell_from_electrodes(Q_grid[m], AN_f, CT_f)
rmse_V = np.sqrt(np.nanmean((fc_f['V_FC'] - fc_true['V_FC'][m]) ** 2))
print(f"  재구성 풀셀 V_FC RMSE = {rmse_V:.2f} mV (잡음 1%≈{0.01*(fc_true['V_FC'][m].max()-fc_true['V_FC'][m].min()):.1f}mV 수준)")

print("\n판정:", "PASS — LCO/흑연 풀셀 분해 회복 성공" if ok_all else "FAIL — 단계/경계/식 재점검")
sys.exit(0 if ok_all else 1)
