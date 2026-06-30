# -*- coding: utf-8 -*-
# graphite_ica_model.py — Ch.1 (v3) 식의 직역. 주석은 식 번호·단계 표지만 단다(해설은 §1.17 본문).
import numpy as np

R, F = 8.314, 96485.0
KB, H = 1.380649e-23, 6.62607015e-34


def dU_hys(T, Omega):
    """(1.88) spinodal 상한 gap [V] — Omega <= 2RT 면 0 (M1 명시 분기)."""
    if Omega <= 2.0 * R * T:
        return 0.0
    u = np.sqrt(1.0 - 2.0 * R * T / Omega)
    return (2.0 / F) * (Omega * u - 2.0 * R * T * np.arctanh(u))


def U_branch(T, U, Omega, gamma, sigma_d, h_eta=1.0):
    """(1.91) 분기 중심 U^d — 부분 cycle 은 gamma -> h(eta)*gamma (M1)."""
    return U + sigma_d * 0.5 * (h_eta * gamma) * dU_hys(T, Omega)


def xi_eq(Vn, Ud, w):
    """(1.27) 의 꼴 — M2 (중심 U^d, 폭 w 는 S1 동결값)."""
    return 1.0 / (1.0 + np.exp(-(Vn - Ud) / w))


def ln_Lq(T, I_abs, Q_cell, dHa_eff, b, chi_d, A_d):
    """(1.69) — M3. A_d >= 0 방향형; 전이대(A_d < 3RT)는 괄호 인자로 나눈다."""
    T_star = I_abs * H / (Q_cell * KB)
    val = np.log(T_star / T) + dHa_eff / (R * T) + b - chi_d * A_d / (R * T)
    if A_d < 3.0 * R * T:
        val -= np.log(1.0 + np.exp(-A_d / (R * T)))
    return val


def r_a_connect(Lq, dxi_dq_at_qa):
    """M4 접속 분기(L_V < w/3): r_a = L_q * (dxi_eq/dq)|_{q_a} — par['r_a'] 생성용."""
    return Lq * dxi_dq_at_qa


def dQdV_app(V_app, T, I_abs, Q_cell, sigma_d, par):
    """(1.96) 양방향 통합식의 평가, M1~M6 — 반환은 방향 정렬 ICA 크기 [Q_cell/V]."""
    Vn = V_app - sigma_d * I_abs * par['Rn']                                       # (1.45)
    y = np.asarray(par['Cbg'](Vn), dtype=float)                                    # (1.43)
    for tr in par['transitions']:
        Ud = U_branch(T, tr['U'], tr['Omega'], tr['gamma'], sigma_d, tr.get('h_eta', 1.0))  # M1
        xe = xi_eq(Vn, Ud, tr['w'])                                                # M2
        A_d = sigma_d * F * (tr['Va'] - Ud)                                        # (1.19) 방향형
        chi_d = par['chi'] if sigma_d > 0 else 1.0 - par['chi']                    # (1.21) 합-1
        Lq = np.exp(ln_Lq(T, I_abs, Q_cell, tr['dHa_eff'], tr['b'], chi_d, A_d))   # M3 (동결)
        LV = abs(tr['dVdq_qa']) * Lq                                               # M4
        ra = tr['r_a']
        bell = (1.0 - ra) * xe * (1.0 - xe) / tr['w']                              # (1.96) 종
        sup = (sigma_d * (Vn - tr['Va']) >= 0.0)
        dv = -sigma_d * (Vn - tr['Va']) / LV
        tail = (ra / LV) * np.exp(np.where(sup, dv, -np.inf))                      # (1.96) 꼬리
        y = y + tr['Q'] * (bell + tail)
    return y                                                                       # M6: V_app 축


# ---- 단계 회귀의 골격 — 해설·규약은 본문, 목적함수는 (5) 의 가중 LSQ
def s1_residual(theta, V, y_meas, Np):
    """S1 잔차 — theta = [U_1, w_1, Q_1, ..., U_Np, w_Np, Q_Np, Cbg0]; (1.79) 종 항만.
    Cbg0 은 상수 근사 — 실데이터는 (3) 의 anchor spline."""
    model = np.full_like(V, theta[-1])
    for j in range(Np):
        U, w, Q = theta[3 * j:3 * j + 3]
        xe = xi_eq(V, U, w)
        model = model + Q * xe * (1.0 - xe) / w
    return y_meas - model

# S3: (V_drive, ln L_q) 점들의 직선 기울기 = -chi*F/RT (방전, S0-pass)      ... (1.67)
# S4: y(T) 를 1/T 로 회귀 — 기울기 = -dHa_eff/R, b = -절편                  ... (1.70)·(1.71)
# S5: 절편(T) 3점 -> (gamma, Omega) 2-파라미터 비선형 LSQ                   ... (1.93)
