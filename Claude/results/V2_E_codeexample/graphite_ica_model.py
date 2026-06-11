# -*- coding: utf-8 -*-
# graphite_ica_model.py — Ch.1 (v2) 의 식만으로 구성한 dQ/dV 모델.
# 주석의 (1.x)/M*/S* 는 전부 본 문건의 식 번호와 알고리즘 단계다.
import numpy as np

R, F = 8.314, 96485.0                        # §1.1 표
KB, H = 1.380649e-23, 6.62607015e-34         # Boltzmann, Planck


def dU_hys(T, Omega):
    """(1.34) spinodal 상한 gap [V].
    M1 의 명시 분기: Omega <= 2RT 면 0 (제곱근이 NaN 인 영역)."""
    if Omega <= 2.0 * R * T:
        return 0.0
    u = np.sqrt(1.0 - 2.0 * R * T / Omega)
    return (2.0 / F) * (Omega * u - 2.0 * R * T * np.arctanh(u))


def U_branch(T, U, Omega, gamma, sigma_d, h_eta=1.0):
    """(1.35) 분기 중심 U^d. 부분 cycle 이면 gamma -> h(eta)*gamma (M1)."""
    return U + sigma_d * 0.5 * (h_eta * gamma) * dU_hys(T, Omega)


def xi_eq(Vn, Ud, w):
    """(1.11) 의 꼴 — M2. 중심은 분기 중심 U^d, 폭 w 는 S1 동결값
    (박스의 RT/F 는 이상 극한 — 하드코딩 금지)."""
    return 1.0 / (1.0 + np.exp(-(Vn - Ud) / w))


def ln_Lq(T, I_abs, Q_cell, dHa_eff, b, chi_d, A_d):
    """M3 — (1.27) 의 역:
      ln L_q = ln(T*/T) + dHa/RT + b - chi_d*A_d/RT,
      T* = |I|h/(Q_cell kB) — |I|/Q_cell 는 rate [1/s] 비로만 쓰인다.
    b = -dS_a/R 결합값 (S4 의 y-절편의 부호 반전).
    A_d = sigma_d*F*(Va - U^d) >= 0 — 자기 방향으로 양수인 구동력.
    chi_d: 방전이면 chi, 충전이면 1-chi — 같은 전이상태의 합-1 강제(1.8);
    충전 회귀와 S3 chi 의 합치가 그 가정의 검정이다(§1.15).
    전이대(A_d < 3RT)의 보편형 괄호 인자는 속도에 곱 => L 은 나눈다."""
    T_star = I_abs * H / (Q_cell * KB)
    val = (np.log(T_star / T) + dHa_eff / (R * T) + b
           - chi_d * A_d / (R * T))
    if A_d < 3.0 * R * T:
        val -= np.log(1.0 + np.exp(-A_d / (R * T)))
    return val


def r_a_connect(Lq, dxi_dq_at_qa):
    """M4 의 접속값 분기 (L_V < w/3): r_a = L_q * (dxi_eq/dq)|_{q_a}.
    dxi_dq_at_qa 는 자기 방향 진행의 크기(>0)로 넣는다.
    그 외(꼬리-우세)는 r_a 가 (0, xi_eq(q_a)] 범위의 자유 파라미터."""
    return Lq * dxi_dq_at_qa


def dQdV_app(V_app, T, I_abs, Q_cell, sigma_d, par):
    """(1.38) 양방향 통합식의 평가 — M1~M6. 반환 단위 [Q_cell/V].
    반환은 방향 정렬된 ICA 크기다 — signed dQ/dV 데이터와 맞출 때는
    sigma_d*dQ/dV >= 0 이 되도록 부호를 정렬한다((2) 의 규약).
    단위 규약: Q(전이)·Cbg 는 Q_cell 정규화(무차원, /V), I_abs/Q_cell
    는 rate [1/s] 가 되도록 넣는다(T* 가 그 비만 쓴다).
    방향 규약: 평형 3량과 (Omega,gamma,chi)는 방향 공통이지만, 꼬리
    파라미터 {Va, dVdq_qa, r_a, b}는 방향별 독립이다(1.38) — 충전
    평가에는 충전 데이터에서 닫은 값을 담은 par 를 쓴다. Cbg 는 해당
    T 의 closure((7) 의 T-회귀로 생성).
    par 의 구성 (괄호는 그 값을 닫는 단계):
      Cbg(Vn)      배경 미분용량 함수 [Q_cell/V] (S1 동결 spline)
      Rn           lumped 분극 [V per |I|] (S2 직독)
      chi          전달 계수 (S3; 충전 가지는 1-chi 로 자동 적용)
      transitions  전이 dict 리스트:
        U, w, Q        평형 3량 (1.20)/(1.13) (S1)
        dHa_eff, b     (1.27)+M3 (S4; Omega!=0 전이는 chi_d*Omega 흡수
                       유효값 — S5 후 dHa = dHa_eff + chi_d*Omega 복원)
        Omega, gamma   (1.34)/(1.35) (S5; 비분기 전이는 0)
        Va, dVdq_qa    꼬리 컷 전위(3'), |dV/dq|_{q_a} (M4 — 피팅 시
                       해당 율의 측정 V(q), 예측 시 OCV 해에서 읽음)
        r_a            잔류 지연 (M4 분기 결과), h_eta (기본 1)
    """
    Vn = V_app - sigma_d * I_abs * par['Rn']           # (1.17)
    y = np.asarray(par['Cbg'](Vn), dtype=float)        # (1.16)
    for tr in par['transitions']:
        Ud = U_branch(T, tr['U'], tr['Omega'], tr['gamma'],
                      sigma_d, tr.get('h_eta', 1.0))   # M1
        xe = xi_eq(Vn, Ud, tr['w'])                    # M2
        A_d = sigma_d * F * (tr['Va'] - Ud)            # (1.7) 방향형
        chi_d = par['chi'] if sigma_d > 0 \
            else 1.0 - par['chi']                      # (1.8) 합-1
        Lq = np.exp(ln_Lq(T, I_abs, Q_cell, tr['dHa_eff'],
                          tr['b'], chi_d, A_d))        # M3 (동결)
        LV = abs(tr['dVdq_qa']) * Lq                   # M4
        ra = tr['r_a']
        bell = (1.0 - ra) * xe * (1.0 - xe) / tr['w']  # (1.38) 종
        sup = (sigma_d * (Vn - tr['Va']) >= 0.0)       # indicator
        tail = (ra / LV) * np.exp(
            -sigma_d * (Vn - tr['Va']) / LV) * sup     # (1.38) 꼬리
        y = y + tr['Q'] * (bell + tail)
    return y                                           # M6: V_app 축


# ---- 단계 회귀의 골격 — 최소화 루틴은 독자 몫((5): 가중 LSQ 만 지키면 됨)
def s1_residual(theta, V, y_meas, Np):
    """S1 잔차: 저율 OCV 의 다-peak 동시 회귀.
    theta = [U_1, w_1, Q_1, ..., U_Np, w_Np, Q_Np, Cbg0].
    저율(r_a -> 0)이라 (1.31) 의 종 항만 남는다. 배경을 상수 하나로
    둔 것은 예시 단순화 — 실데이터는 (3) 의 anchor spline 을 쓴다."""
    model = np.full_like(V, theta[-1])
    for j in range(Np):
        U, w, Q = theta[3 * j:3 * j + 3]
        xe = xi_eq(V, U, w)
        model = model + Q * xe * (1.0 - xe) / w
    return y_meas - model

# S3: (V_drive, ln L_q) 점들의 직선 기울기 = -chi*F/RT        ... (1.26)
# S4: y(T) = ln(T*/(L_q T)) - chi*A/RT 를 1/T 로 회귀 —
#     기울기 = -dHa/R, b = -절편                              ... (1.27)
# S5: 절편(T) 3점 -> (gamma, Omega) 2-파라미터 비선형 LSQ      ... (1.36)
