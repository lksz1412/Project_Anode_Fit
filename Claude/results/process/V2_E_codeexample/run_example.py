# -*- coding: utf-8 -*-
"""run_example.py — graphite_ica_model.py 의 실행 검증 (E.1 게이트).
검증 3건: (i) (1.88) 수치 = 본문 55 mV(Omega=4RT), (ii) (1.96) 평가의
면적 보존(종+꼬리 = Q_j), (iii) S1 잔차 골격으로 3전이 회복 round-trip.
"""
import sys
import numpy as np
from graphite_ica_model import (R, F, dU_hys, dQdV_app, s1_residual,
                                xi_eq)
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

T0 = 298.15
rng = np.random.default_rng(20260611)

# (i) dU_hys 수치 — 본문 sec1.13: Omega=4RT -> ~2.13 RT/F ~ 55 mV
g = dU_hys(T0, 4 * R * T0) * 1000.0
print(f"(i) dU_hys(4RT,25C) = {g:.1f} mV  (본문 ~55 mV)")
assert abs(g - 54.8) < 0.5
assert dU_hys(T0, 1.9 * R * T0) == 0.0          # M1 분기

# (ii) (1.96) 평가 + 면적 보존 — 1전이, 방전, r_a=0.3 (꼬리-우세)
# b 는 임의값이 아니라 자기일관 — 목표 L_q=0.02 를 (1.69)으로
# 풀면 b = ln L_q - ln(T*/T) - dHa/RT + chi*A/RT (+전이대 보정) = 10.95
par = dict(
    Cbg=lambda Vn: np.full_like(Vn, 0.5),       # [/V] = 0.0005/mV
    Rn=0.008, chi=0.5,
    transitions=[dict(U=0.120, w=0.0255, Q=0.40,
                      dHa_eff=45e3, b=10.95, Omega=0.0, gamma=0.0,
                      Va=0.180, dVdq_qa=2.0, r_a=0.30)])
V = np.linspace(-0.20, 1.20, 14001)
y = dQdV_app(V, T0, 0.1, 1.0, +1, par)
area = np.trapezoid(y - 0.5, V)                 # 배경 차감 면적
print(f"(ii) 전이 면적(방전) = {area:.4f}  (참 Q=0.4000)")
assert abs(area - 0.40) < 0.004                 # 보존 (1-r_a)+r_a=1
# 충전 가지 — 방향별 꼬리 파라미터(여기선 대칭 가정의 예시값)로 평가:
# A_d = sigma_d*F*(Va-Ud) = -F*(0.060-0.120) > 0, chi_d = 1-chi.
yc = dQdV_app(V, T0, 0.1, 1.0, -1,
              {**par, 'transitions': [dict(par['transitions'][0],
                                           Va=0.060)]})
area_c = np.trapezoid(yc - 0.5, V)
print(f"(ii) 전이 면적(충전) = {area_c:.4f}  (참 Q=0.4000)")
assert np.all(np.isfinite(yc)) and abs(area_c - 0.40) < 0.004

# (iii) S1 미니 round-trip — 3전이 저율 종 합성 + 1% 잡음 -> 회복
TRUE = [(0.210, 0.018, 0.15), (0.120, 0.010, 0.40),
        (0.085, 0.008, 0.35)]
Cbg0 = 0.5
Vs = np.linspace(0.02, 0.32, 1201)
y0 = np.full_like(Vs, Cbg0)
for U, w, Q in TRUE:
    xe = xi_eq(Vs, U, w)
    y0 += Q * xe * (1 - xe) / w
y_meas = y0 + rng.normal(0, 0.01 * (y0.max() - Cbg0), Vs.shape)

th = np.array(sum(([U * 1.02, w * 1.2, Q * 0.9]                 # 초기값
                   for U, w, Q in TRUE), []) + [Cbg0 * 1.5])
for _ in range(30):                              # Gauss-Newton (수치 J)
    r = s1_residual(th, Vs, y_meas, 3)
    Jm = np.zeros((len(Vs), len(th)))
    for k in range(len(th)):
        d = np.zeros_like(th)
        d[k] = max(1e-7, 1e-4 * abs(th[k]))
        Jm[:, k] = (s1_residual(th + d, Vs, y_meas, 3) - r) / d[k]
    dth, *_ = np.linalg.lstsq(-Jm, r, rcond=None)
    th += dth
    if np.max(np.abs(dth)) < 1e-10:
        break
print("(iii) S1 회복 (참값 대비):")
ok = True
for j, (U, w, Q) in enumerate(TRUE):
    Ur, wr, Qr = th[3 * j:3 * j + 3]
    print(f"  j={j+1}: U {Ur*1e3:7.2f} vs {U*1e3:5.1f} mV"
          f" | w {wr*1e3:5.2f} vs {w*1e3:4.1f} mV"
          f" | Q {Qr:.4f} vs {Q:.2f}")
    ok &= (abs(Ur - U) < 5e-4 and abs(wr - w) < 5e-4
           and abs(Qr - Q) < 0.01)
assert ok
print("판정: PASS — 문건 식 직역 모델로 평가·보존·S1 회복 모두 성립")
