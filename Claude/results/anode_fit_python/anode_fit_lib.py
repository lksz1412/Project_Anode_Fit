# -*- coding: utf-8 -*-
# ============================================================================
#  anode_fit_lib.py
#  Anode_Fit Chapter 1 (graphite_ica_ch1_Opus_v4.tex) 닫힌 식의 Python 함수화
# ----------------------------------------------------------------------------
#  식 번호 표기 (1.x) = PDF 렌더 번호. 출처 = graphite_ica_ch1_Opus_v4.aux 의
#  \newlabel 매핑 (권위). 각 함수 docstring 의 4항:
#     (1) 출처식  : 문건 몇번식인지 / 몇번식 + 몇번식의 조합인지
#     (2) 조합·근사: 어떤 식을 어떻게 결합하고 어떤 극한/근사를 취했는지
#     (3) 가정     : 그 식이 성립하는 물리 가정 (문건 §1.16 '가정의 울타리' 참조)
#     (4) x축      : V(전위) 인지 Q(용량) 인지  ★ 사용자 핵심 질문
# ----------------------------------------------------------------------------
#  ★★★ 축(axis) 규약 — "x축을 V로 두는지 Q로 두는지" 에 대한 답 ★★★
#
#  본 모델에는 좌표축이 셋 있고, 함수마다 docstring 에 어느 축인지 명시한다.
#
#  [A] V 축  (전위, 단위 mV vs Li/Li+)
#        - 관측량 dQ/dV 의 자연 축. peak 가 전위 U_j 에 "선다".
#        - 평형 peak 모델 (종 모양) 과 꼬리가 모두 V 의 함수로 적힌다.
#        - 해당 함수: xi_eq, bell, tail, peak_dQdV, electrode_dQdV
#
#  [B] q 축  (정규화 용량, q = Q/Q_cell, 무차원 0~1)
#        - 동역학(꼬리)이 유도되는 축. 완화 ODE (1.53) dξ/dq, 기억 커널 (1.57),
#          꼬리 길이 L_q (1.54) 가 전부 q 에서 유도된다.
#        - 최종 모델에서는 국소 기울기 |dV_n/dq| 로 V 축 길이 L_V (1.63) 로
#          "환산"되어 흡수되므로, 사용자가 직접 q 축을 다룰 일은 거의 없다.
#        - 해당: ln_Lq, L_V_from_Lq (스칼라 — 전이당 상수로 동결)
#
#  [C] Q 축  (용량 — 정규화 q 또는 절대 Ah)
#        - 풀셀 분해의 축. 두 전극이 같은 전하를 흘리므로(직렬 연결)
#          공통 용량 Q 위에서  V_FC(Q) = V_CT(Q) - V_AN(Q).
#        - 매칭/피팅은 Q 축에서 한다 (BDD BatteryData_Matching 규약과 동일).
#        - 해당: electrode_QV, invert_QV, full_cell_from_electrodes, fc_residual
#
#  [A] <-> [C] 다리 = OCV 곡선  Q(V) = ∫ (dQ/dV) dV
#        ( (1.42) 전하보존식의 적분 = (1.47) 관측식 dQ/dV 의 부정적분 ).
#        electrode_QV 가 이 적분을, invert_QV 가 그 역함수 V(Q) 를 준다.
# ----------------------------------------------------------------------------
#  부호·단위 규약 (문건 §1.1):
#     - 모든 전위 = 흑연 음극 반쪽전지 전위 (vs Li/Li+). 본 코드 단위 = mV.
#     - s  = +1 (방전 본론 규약, 평형식 (1.27) 안에 고정).
#     - σ_d (sigma_d) = +1 방전 / -1 충전 — 분극 부호·분기 중심·꼬리 방향만 바꾼다.
#     - Q_j, C_bg 는 Q_cell 정규화 (무차원, 단위 /mV). |I|/Q_cell 은 rate [1/s].
# ============================================================================

import numpy as np

# ---- 물리 상수 (문건 (1.2) Eyring 식의 prefactor k_B T / h 에 쓰임) ----
R  = 8.314          # J/(mol K)  기체 상수
F  = 96485.0        # C/mol      Faraday 상수
KB = 1.380649e-23   # J/K        Boltzmann 상수
H  = 6.62607015e-34 # J s        Planck 상수


# ===========================================================================
#  Phase 1 — Primitive 함수층 (식 하나 = 함수 하나)
# ===========================================================================

def xi_eq(V, U, w, s=+1.0):
    """평형 점유율(등온선) ξ_eq — "상전이 j 의 종 모양"의 적분형.

    (1) 출처식 : (1.27) eq:logistic.
    (2) 조합   : 단독. 정·역 속도 (1.25) 의 정지점에서 회수된 logistic.
    (3) 가정   : 평형 등온선이 smooth (0→1 급점프 금지). 이상 극한 폭 w=RT/F,
                 상호작용 있으면 (1.32) eq:weff 의 w_eff 로 좁아진다.
    (4) x축    : V  (전위). 중심 U 에서 ξ=1/2.

    반환: ξ ∈ (0,1). z = s (V-U)/w 로 1/(1+e^{-z}).
    """
    z = s * (V - U) / w
    return 1.0 / (1.0 + np.exp(-z))


def bell(V, U, w, Q, s=+1.0):
    """평형 peak (종 모양) 의 dQ/dV 기여 = Q · dξ_eq/dV.

    (1) 출처식 : (1.50) eq:dxidV  =  Q × (1.49) eq:belliden 에 연쇄율 dz/dV=s/w.
                 즉  dξ_eq/dV = s·ξ(1-ξ)/w,  여기에 전이 용량 Q 를 곱한 것.
    (2) 근사   : 평형 추종 — 전류가 평형을 따라간다고 본 상승부 지배 항.
    (3) 가정   : 분리(겹치지 않는) 단봉. 정점 높이 = Q/(4w), 면적 = Q  ((1.51) eq:eqpeak).
    (4) x축    : V (전위). 봉우리가 U 에 선다.
    """
    xi = xi_eq(V, U, w, s)
    return Q * s * xi * (1.0 - xi) / w


def ln_Lq(T, I_abs, Q_cell, dHa_eff, b, chi_d, A_d):
    """꼬리 길이의 로그 ln L_q (전이당 상수로 동결).

    (1) 출처식 : (1.69) eq:lnLq.  이는 (1.54) eq:Lq [L_q=|I|/(Q_cell k)] 에
                 (1.64) eq:keff [유효장벽 ΔG_eff=ΔG_a-χA] 와
                 (1.68) eq:LqT [Eyring prefactor k_0=k_B T/h → T_*] 를 넣어 묶은 조합.
    (2) 근사   : forward 극한 (A_d ≳ 3RT 면 역방향 무시). A_d<3RT 면 보편형
                 괄호 인자 (1+e^{-A/RT}) 로 '나눈다'(속도에 곱하는 인자 → L_q 는 나눔).
    (3) 가정   : 활성화 지배(S0 통과). b = -ΔS_a/R + prefactor 보정 (결합 절편, S4 산출).
                 dHa_eff = ΔH_a - χ_d Ω (Ω≠0 전이의 유효값, (1.95) eq:dHeff).
    (4) x축    : 스칼라 (한 전이의 한 점에서 평가) — 출력은 무차원 ln L_q.

    A_d = σ_d F (V_a - U^d) ≥ 0  (방향형 구동력, (1.19) eq:affinity).
    """
    T_star = I_abs * H / (Q_cell * KB)                 # (1.68) 특성 온도 T_*
    val = np.log(T_star / T) + dHa_eff / (R * T) + b - chi_d * A_d / (R * T)
    if A_d < 3.0 * R * T:                              # 전이대 보정 (M3)
        val -= np.log(1.0 + np.exp(-A_d / (R * T)))
    return val


def L_V_from_Lq(Lq, dVn_dq_at_qa):
    """V 축 꼬리 길이 L_V  =  |dV_n/dq|_{q_a} · L_q.

    (1) 출처식 : (1.63) eq:tail 의 L_V 정의.
    (2) 조합   : q 축 길이 L_q (=exp(ln_Lq)) 를 꼬리 시작점 q_a 의 국소 기울기
                 |dV_n/dq| 로 곱해 V 축 길이로 환산. ★ [B]q축 → [A]V축 환산.
    (3) 가정   : post-peak 에서 V_n(q) 의 국소 기울기가 창 안에서 거의 일정.
    (4) x축    : 스칼라 [mV] — 이후 tail 의 V 축 감쇠 길이로 쓰인다.
    """
    return abs(dVn_dq_at_qa) * Lq


def tail(V, V_a, L_V, r_a, Q, s=+1.0):
    """동역학 꼬리의 dQ/dV 기여 (단방향 지수).

    (1) 출처식 : (1.78) eq:taildiff  ( = (1.61) eq:rsol 의 미분 = (1.63) eq:tail ).
                 -dr̄/dV = (r_a/L_V) e^{-(V-V_a)/L_V},  여기에 Q 를 곱한 것.
    (2) 근사   : ρ_G→δ (좁은 장벽 분포) 극한. 원천 소멸(peak 통과 후) 가정으로
                 기억 적분이 사라지고 초기 지연의 지수 감쇠만 남음.
    (3) 가정   : 단방향(indicator 1{s(V-V_a)≥0}) — 방전 진행 방향으로만 꼬리.
                 면적 = Q·r_a  (종의 (1-r_a) 와 합쳐 Q 보존, (1.80) eq:areacons).
    (4) x축    : V (전위). V_a 에서 진폭 r_a/L_V 로 점화.
    """
    arg = s * (V - V_a)                                 # 지지(support) 판정
    sup = arg >= 0.0
    # 비지지 쪽 지수를 -inf 로 막아 exp 가 정확히 0 (강건성, §1.17 np.where 장치)
    decay = np.where(sup, -arg / L_V, -np.inf)
    return Q * (r_a / L_V) * np.exp(decay)


def dU_hys(T, Omega):
    """충방전 분기 gap ΔU^hys (히스테리시스 상한).

    (1) 출처식 : (1.88) eq:hysdU.
    (2) 근사   : spinodal 상한 — 준안정 띠 폭의 상한.
    (3) 가정   : Ω ≤ 2RT 면 0 (분기 없음, sqrt 가 NaN 주는 영역 → 명시 분기, M1).
    (4) x축    : 스칼라 [mV].

    u = sqrt(1 - 2RT/Ω),  ΔU = (2/F)(Ω u - 2RT artanh u).  [단위: V → ×1000 mV]
    """
    if Omega <= 2.0 * R * T:
        return 0.0
    u = np.sqrt(1.0 - 2.0 * R * T / Omega)
    return 1000.0 * (2.0 / F) * (Omega * u - 2.0 * R * T * np.arctanh(u))  # mV


def U_branch(T, U, Omega, gamma, sigma_d, h_eta=1.0):
    """방향별 분기 중심 U^d.

    (1) 출처식 : (1.91) eq:hyscenter.  (1.88) dU_hys 를 사용.
    (2) 조합   : 중점 U 에 ± ½ (h_η γ) ΔU^hys 를 더해 방전/충전 중심을 가른다.
    (3) 가정   : γ = 분기 축소 인자(실측 분기/이론 상한). 부분 cycle 은 γ→h(η)γ.
    (4) x축    : 스칼라 [mV].
    """
    return U + sigma_d * 0.5 * (h_eta * gamma) * dU_hys(T, Omega)


# ===========================================================================
#  Phase 2 — 전이·전극 모델층
# ===========================================================================

def peak_dQdV(V, tr, s=+1.0):
    """한 상전이의 dQ/dV (평형 종 + 동역학 꼬리). ★ "상전이마다 dQdV 피크".

    (1) 출처식 : (1.79) eq:simplefit (단일 전이 닫힌 실무형).
                 = bell × (1-r_a)  +  tail × r_a  의 구조.
                 bell=(1.50), tail=(1.78), 면적보존=(1.80).
    (2) 근사   : ρ_G→δ 실무 기본형. (1-r_a) 인자가 꼬리로 넘어간 미완 몫의 회계
                 → 종 면적 Q(1-r_a) + 꼬리 면적 Q·r_a = Q.
    (3) 가정   : 전이 하나(분리). 저율 극한 r_a→0 이면 순수 종(평형 peak).
    (4) x축    : V (전위).

    tr dict 키: U, w, Q, r_a, L_V, V_a  (꼬리 없으면 r_a=0 로 두면 종만 남음).
    """
    U, w, Q = tr['U'], tr['w'], tr['Q']
    ra = tr.get('r_a', 0.0)
    out = bell(V, U, w, Q, s) * (1.0 - ra)
    if ra > 0.0:
        out = out + tail(V, tr['V_a'], tr['L_V'], ra, Q, s)
    return out


def electrode_dQdV(V, transitions, Cbg=0.0, s=+1.0):
    """한 전극의 dQ/dV(V) = 배경 + 모든 상전이 peak 의 합. ★ 전극 = peak 들의 합.

    (1) 출처식 : (1.82) eq:total.  dQ/dV = C_bg + Σ_j Q_j dξ_j/dV.
                 각 항 = peak_dQdV (=(1.79)).
    (2) 조합   : 전이별 (1.79) 를 선형 합산. 합산 자체는 전하보존 (1.42) 의 직접 미분.
    (3) 가정   : 각 전이가 이웃에 독립으로 진화(전이 간 상호작용·순차 staging 무시).
                 C_bg = 배경 미분용량 ((1.43) eq:cbg), 상수 또는 V 의 함수(spline).
    (4) x축    : V (전위).

    transitions : list of tr dict.  Cbg : float 또는 callable(V)->array.
    반환: g_e(V) = dQ/dV  (≥0, 단조 적분 가능).
    """
    g = Cbg(V) if callable(Cbg) else np.full_like(np.asarray(V, dtype=float), Cbg)
    for tr in transitions:
        g = g + peak_dQdV(V, tr, s)
    return g


def dQdV_app(V_app, T, I_abs, Q_cell, sigma_d, par):
    """양방향(충방전) 통합 dQ/dV — 측정축(V_app) 평가. (§1.17 코드 직역 + 추적 강화)

    (1) 출처식 : (1.96) eq:hysmaster (방향별 통합식, M1–M6).
    (2) 조합   : (1.45) V_n=V_app-σ_d|I|R_n 환산 → 분기중심 (1.91) → 평형종 (1.50)
                 + 유효장벽 (1.69)→L_q→(1.63) 꼬리.  방향이 값을 바꾸는 두 자리만
                 σ_d 로 갈림: 구동력 A_d=σ_d F(V_a-U^d), 계수 χ_d(방전 χ/충전 1-χ).
    (3) 가정   : §1.16 '가정의 울타리' ①~⑯ (활성화 지배·좁은 ρ_G·상수-L 동결 등).
    (4) x축    : V_app (측정 전위) — 내부에서 V_n 으로 환산해 평가.

    par dict: 'Rn','Cbg','chi','transitions'(각 tr: U,w,Q,Omega,gamma,V_a,
              dVdq_qa,dHa_eff,b,r_a). 방전 sigma_d=+1, 충전 -1.
    """
    Vn = V_app - sigma_d * I_abs * par['Rn']                          # (1.45)
    y = par['Cbg'](Vn) if callable(par['Cbg']) else \
        np.full_like(np.asarray(Vn, dtype=float), par['Cbg'])        # (1.43)
    for tr in par['transitions']:
        Ud = U_branch(T, tr['U'], tr['Omega'], tr['gamma'], sigma_d, tr.get('h_eta', 1.0))  # M1
        xe = xi_eq(Vn, Ud, tr['w'], s=+1.0)                          # M2  ((1.27), 평형 s=+1 고정)
        A_d = sigma_d * F * (tr['V_a'] - Ud) / 1000.0                # (1.19) 방향형 (mV→V)
        chi_d = par['chi'] if sigma_d > 0 else 1.0 - par['chi']      # (1.21) 합-1
        Lq = np.exp(ln_Lq(T, I_abs, Q_cell, tr['dHa_eff'], tr['b'], chi_d, A_d))   # M3 (동결)
        LV = L_V_from_Lq(Lq, tr['dVdq_qa'])                          # M4
        ra = tr['r_a']
        bell_term = (1.0 - ra) * xe * (1.0 - xe) / tr['w']           # (1.96) 종
        sup = (sigma_d * (Vn - tr['V_a']) >= 0.0)
        dv = -sigma_d * (Vn - tr['V_a']) / LV
        tail_term = (ra / LV) * np.exp(np.where(sup, dv, -np.inf))   # (1.96) 꼬리
        y = y + tr['Q'] * (bell_term + tail_term)
    return y                                                          # M6: V_app 축 크기


# ===========================================================================
#  Phase 3 — V <-> Q 변환 + 전극 OCV 곡선  ([A]V축 <-> [C]Q축 다리)
# ===========================================================================

def electrode_QV(V_grid, transitions, Cbg=0.0, s=+1.0, Q0=0.0):
    """전극 OCV 곡선 Q(V) = ∫ (dQ/dV) dV.  ★ V 축을 Q 축으로 잇는 다리.

    (1) 출처식 : ∫ (1.82) eq:total.  ( = (1.42) eq:charge 전하보존 / (1.47) 관측식의 적분).
                 해석적으로  ∫bell = (1.27) ξ,  ∫tail = r_a(1-e^{-(V-V_a)/L_V}) — closed-form.
                 구현은 일반 C_bg(spline) 도 받도록 누적 사다리꼴 적분 사용(같은 값).
    (2) 근사   : 없음(수치 적분). g_e≥0 이라 Q(V) 단조 증가.
    (3) 가정   : 적분상수 Q0 = (1.42) 전하보존 anchor 한 점 (V_grid[0] 에서 Q=Q0).
    (4) x축    : 입력 V (전위) → 출력 Q (용량, /Q_cell). ★ V→Q.

    반환: Q_of_V (V_grid 와 같은 길이). dQ/dV = electrode_dQdV(V_grid).
    """
    V_grid = np.asarray(V_grid, dtype=float)
    g = electrode_dQdV(V_grid, transitions, Cbg, s)        # dQ/dV (V축)
    dQ = 0.5 * (g[1:] + g[:-1]) * np.diff(V_grid)          # 사다리꼴 증분
    Q_of_V = np.concatenate([[Q0], Q0 + np.cumsum(dQ)])
    return Q_of_V


def invert_QV(Q_query, V_grid, Q_of_V):
    """OCV 곡선의 역함수 V(Q).  ★ Q 축을 V 축으로 되돌리는 다리.

    (1) 출처식 : electrode_QV 의 역함수 (수치). Q(V) 단조 → 유일.
    (2) 근사   : 단조 격자 위 선형 보간.
    (3) 가정   : Q_of_V 가 단조 증가 (g_e≥0). 범위 밖은 np.interp 끝값 clamp.
    (4) x축    : 입력 Q (용량) → 출력 V (전위). ★ Q→V.
    """
    return np.interp(Q_query, Q_of_V, V_grid)


# ===========================================================================
#  Phase 4 — 풀셀 분해 조립  [확장: 문건은 반쪽셀까지. 아래는 BDD 매칭 규약]
# ===========================================================================
#  [확장 근거] 문건 §1.1 부호규약: full-cell 이면 양극 기여 제거 환산이 선행.
#  본 절은 그 '환산'을 명시한다. 풀셀은 두 반쪽셀의 직렬:
#     V_FC(Q) = V_CT(Q) - V_AN(Q)            (전위는 빼기)
#     (dV/dQ)_FC = (dV/dQ)_CT - (dV/dQ)_AN   (전압 기울기는 빼기 — 직렬 미분)
#     (dQ/dV)_FC = 1 / (dV/dQ)_FC            (역수)
#  각 전극의 (1.82) 미분용량 g_e 와 그 적분 OCV (electrode_QV) 가 재료다.
#  BDD BatteryData_Matching 규약 그대로:  modi_Capa = Q*A + B  (A=loading, B=slippage).
# ===========================================================================

def build_electrode_curves(V_grid, transitions, Cbg, s, loading, offset, reverse=False):
    """합성 전극 참조곡선 (BDD modi_Capa/modi_Volt/modi_dVdQ 형식).

    (1) 출처식 : electrode_dQdV (1.82) + electrode_QV (∫1.82).
    (2) 조합   : g_e=dQ/dV(V) → Q_e(V)=∫g_e → 풀셀 용량축으로 affine 사상.
                 modi_Capa = loading·Q_e + offset,  modi_dVdQ = (1/g_e)/loading.
                 (용량을 loading 배 늘리면 dV/dQ 는 1/loading 배 — BDD 규약.)
    (3) 가정   : loading = 활물질량(용량 스케일), offset = Li 인벤토리 slippage.
                 ★ 식별성 주의: peak 면적 Q_j 가 이미 용량을 담으므로 loading 과 Q_j 는
                 공선형(load→0.5, Q_j→2 배가 풀셀 불변; 문건 §1.11 경고한 collinearity).
                 → peak-basis 피팅에서는 loading=1 로 고정하고 Q_j 가 용량을 담게 한다.
                 BDD 처럼 '측정 참조곡선'(자체 임의 용량 스케일)을 쓸 때만 loading 자유.
                 ★ reverse: 풀셀에서 음극은 충전(Q↑) 시 리튬화 → V_AN 감소이므로 용량축을
                 반전한다(modi_Capa=loading·(Q_max−Q_e)+offset, dV/dQ<0). 그러면 풀셀
                 dV/dQ_FC = dV/dQ_CT − dV/dQ_AN 이 두 양수의 합(직렬)이 되어 물리적이다.
                 BDD 가 측정 음극 곡선을 이 방향으로 저장하는 것과 일치. 양극은 reverse=False.
    (4) x축    : 내부 V(전위) 격자에서 생성하되, 출력 modi_Capa 가 Q 축 좌표.

    반환: (modi_Capa, Volt, modi_dVdQ) — modi_Capa 오름차순 정렬(interp 요건).
    """
    V_grid = np.asarray(V_grid, dtype=float)
    g = electrode_dQdV(V_grid, transitions, Cbg, s)
    g = np.maximum(g, 1e-12)                               # 0분모 방지
    Q_e = electrode_QV(V_grid, transitions, Cbg, s, Q0=0.0)
    if not reverse:
        modi_Capa = loading * Q_e + offset                # BDD modi_Capa = Capa*A + B
        modi_dVdQ = (1.0 / g) / loading                   # dV/dQ on FC capacity axis (양)
        return modi_Capa, V_grid, modi_dVdQ
    # 음극 반전: full-cell Q 증가 = 리튬화 = V 감소 → 용량축 반전, dV/dQ 음
    modi_Capa = loading * (Q_e[-1] - Q_e) + offset
    modi_dVdQ = -(1.0 / g) / loading
    order = np.argsort(modi_Capa)                          # Capa 오름차순 정렬
    return modi_Capa[order], V_grid[order], modi_dVdQ[order]


def full_cell_from_electrodes(Q_query, AN, CT):
    """풀셀 곡선 합성: V_FC, (dV/dQ)_FC, (dQ/dV)_FC  (Q 축).

    (1) 출처식 : [확장] (1.47) 관측식 + (1.82) 전극별, 직렬 풀셀 FC=CT-AN.
    (2) 조합   : 공통 Q 격자에 각 전극 V·dV/dQ 를 보간 → CT - AN.
    (3) 가정   : 직렬(두 전극 동일 전하), lumped(접촉저항 등은 R_n 으로 별도).
    (4) x축    : Q (용량). ★ 매칭/피팅의 축.

    AN, CT : build_electrode_curves 의 출력 (modi_Capa, Volt, modi_dVdQ).
    반환: dict(V_FC, dVdQ_FC, dQdV_FC, valid) — 길이 = len(Q_query) (고정).
          valid = 두 전극 용량 겹침 안에 든 Q_query 점 (범위 밖은 interp 끝값 clamp).
    ★ 잔차의 고정 길이를 위해 mask 로 잘라내지 않고 전 Q_query 를 평가(범위 밖 clamp).
    """
    cAN, vAN, dAN = AN
    cCT, vCT, dCT = CT
    iV_AN = np.interp(Q_query, cAN, vAN)   # np.interp = 범위 밖 끝값 clamp
    id_AN = np.interp(Q_query, cAN, dAN)
    iV_CT = np.interp(Q_query, cCT, vCT)
    id_CT = np.interp(Q_query, cCT, dCT)
    dVdQ_FC = id_CT - id_AN
    lo = max(np.nanmin(cAN), np.nanmin(cCT))
    hi = min(np.nanmax(cAN), np.nanmax(cCT))
    valid = (Q_query > lo) & (Q_query < hi)
    return dict(V_FC=iV_CT - iV_AN,
                dVdQ_FC=dVdQ_FC,
                dQdV_FC=1.0 / dVdQ_FC,
                valid=valid)


def fc_residual(Q_query, meas, AN, CT, w_V=1.0, w_dVdQ=1.0, w_dQdV=1.0):
    """풀셀 3채널 잔차 (BDD RMSE_3 구조 미러).

    (1) 출처식 : [확장] full_cell_from_electrodes 의 3채널.
    (2) 조합   : R_V=(V_CT-V_AN)-V_FC^meas, R_dVdQ=(dVdQ_CT-dVdQ_AN)-dVdQ^meas,
                 R_dQdV=(dQ/dV)_FC,model - (dQ/dV)_FC^meas.  ( BDD RMSE_1/2/3 동일).
    (3) 가정   : 가중 LSQ (§1.16 (5)). dQdV 채널은 작은 dQ/dV 영역 잡음 증폭 주의.
    (4) x축    : Q (용량).

    meas dict: 'V_FC','dVdQ_FC' (측정 풀셀, Q_query 와 같은 길이; 미측정점은 NaN).
    반환: 1D 잔차 벡터 (가중 결합). ★ 고정 길이 = 측정 유효점 수 (least_squares 요건).
    """
    fit_mask = np.isfinite(meas['V_FC']) & np.isfinite(meas['dVdQ_FC'])  # 측정으로 고정
    fc = full_cell_from_electrodes(Q_query[fit_mask], AN, CT)
    R_V    = w_V    * (fc['V_FC']    - meas['V_FC'][fit_mask])
    R_dVdQ = w_dVdQ * (fc['dVdQ_FC'] - meas['dVdQ_FC'][fit_mask])
    R_dQdV = w_dQdV * (fc['dQdV_FC'] - 1.0 / meas['dVdQ_FC'][fit_mask])
    return np.concatenate([R_V, R_dVdQ, R_dQdV])


# ===========================================================================
#  Phase 5 — 단계 피팅 메소드 (staged_fit)
# ===========================================================================
#  [출처 논리] 문건 §1.11 '식별의 원칙 — 비순환' + §1.16 식별 사슬 S0–S5:
#     "한 데이터에서 모든 파라미터를 동시 자유 피팅하면 공선형이 되어 분리 안 됨.
#      독립 측정으로 먼저 고정해 다음 단계 기지값으로 만드는 순차 사슬." (§1.11)
#  → 코드판: 자유도를 한 겹씩 개방하고 직전 단계 출력을 동결. BDD RMSE_1→2→3→4
#     (M→+A,B→+dQdV채널→+kink) 의 '점진 자유도 개방' 과 동형.
#  ★ '더 많은 단계를 추가해서라도 제대로 피팅' = 이 동결 사슬의 길이를 늘리는 것.
# ===========================================================================

def pack_params(an_trs, ct_trs, load_an, off_an, load_ct, off_ct):
    """전이 dict 리스트 + loading/offset → 평탄 파라미터 벡터 θ (역: unpack_params).

    레이아웃: [U,w,Q]*N_an + [U,w,Q]*N_ct + [load_an, off_an, load_ct, off_ct].
    축: 파라미터 자체는 무차원/혼합 — U,w[mV], Q[/Q_cell], load[배], off[/Q_cell].
    """
    theta = []
    for tr in an_trs:
        theta += [tr['U'], tr['w'], tr['Q']]
    for tr in ct_trs:
        theta += [tr['U'], tr['w'], tr['Q']]
    theta += [load_an, off_an, load_ct, off_ct]
    return np.array(theta, dtype=float)


def unpack_params(theta, n_an, n_ct):
    """평탄 θ → (an_trs, ct_trs, load_an, off_an, load_ct, off_ct). pack 의 역."""
    an_trs, ct_trs = [], []
    k = 0
    for _ in range(n_an):
        an_trs.append(dict(U=theta[k], w=theta[k + 1], Q=theta[k + 2])); k += 3
    for _ in range(n_ct):
        ct_trs.append(dict(U=theta[k], w=theta[k + 1], Q=theta[k + 2])); k += 3
    load_an, off_an, load_ct, off_ct = theta[k:k + 4]
    return an_trs, ct_trs, load_an, off_an, load_ct, off_ct


def staged_fit(V_an, V_ct, Q_grid, meas, theta0, n_an, n_ct, stages,
               Cbg_an=0.0, Cbg_ct=0.0, s_an=+1.0, s_ct=+1.0,
               weights=(1.0, 1.0, 1.0), bounds=None, reverse_an=True, verbose=True):
    """풀셀 → 양·음극 분해 단계 피팅. ★ 사용자 원안의 '최종 피팅'.

    (1) 출처식 : 잔차 = fc_residual ([확장] 3채널). 단계 사슬 = §1.11/§1.16.
    (2) 조합   : 각 stage 에서 free 인덱스만 least_squares 로 풀고 나머지 동결.
    (3) 가정   : 전이 수(n_an,n_ct) 와 대략 위치는 사전 검출(저율 OCV/반쪽셀)로 anchor.
                 — 문건 §1.12: '저율로 고정 → 고율로 예측' 한 방향만 허용(비유일 회피).
    (4) x축    : 평가는 Q 축(fc_residual). 전극 곡선 생성은 V 축(build_electrode_curves).
                 V_an = 음극 전위 격자(흑연 ~0.1V vs Li), V_ct = 양극 전위 격자(~3.7V vs Li).

    stages : list of (이름, free_index_list[, stage_weights]). 직전 stage 결과를 다음 init 으로.
             stage_weights 가 있으면 그 단계만 그 가중 사용(없으면 공통 weights).
             ★ coarse-to-fine: 평활한 V-채널로 거친 정렬(basin 진입) → 날카로운 dV/dQ 로
               미세 정렬. (V_FC=적분=평활, dV/dQ=미분=sharp peak 에 민감 → rugged landscape.)
             예) [('P1 coarse(V)', [...], (5/scV, 0.1/scd, 0)),
                  ('P2 +dVdQ',     [...], (1/scV, 1/scd, 0)),
                  ('P3 +widths/dQdV', [모든 idx], (1/scV, 1/scd, 0.3/scq))]
    반환: dict(theta, history, an_trs, ct_trs, loadings).
    """
    from scipy.optimize import least_squares

    theta = theta0.copy()
    ntot = len(theta)
    if bounds is None:
        lb = np.full(ntot, -np.inf); ub = np.full(ntot, np.inf)
    else:
        lb, ub = bounds

    def residual_full(th, W):
        an_trs, ct_trs, la, oa, lc, oc = unpack_params(th, n_an, n_ct)
        AN = build_electrode_curves(V_an, an_trs, Cbg_an, s_an, la, oa, reverse=reverse_an)
        CT = build_electrode_curves(V_ct, ct_trs, Cbg_ct, s_ct, lc, oc)
        return fc_residual(Q_grid, meas, AN, CT, *W)

    history = []
    for stage in stages:
        name, free = stage[0], stage[1]
        W = stage[2] if len(stage) > 2 else weights
        free = np.asarray(free, dtype=int)
        fixed = np.array([i for i in range(ntot) if i not in set(free.tolist())], dtype=int)
        x0 = theta[free]
        flb, fub = lb[free], ub[free]

        def residual_sub(x):
            th = theta.copy()
            th[free] = x
            return residual_full(th, W)

        res = least_squares(residual_sub, x0, bounds=(flb, fub), method='trf', max_nfev=4000)
        theta[free] = res.x
        cost = float(np.sqrt(2 * res.cost / max(len(res.fun), 1)))   # RMSE 규모
        history.append((name, cost))
        if verbose:
            print(f"  [{name}] RMSE={cost:.5g}  (free={len(free)}, 동결={len(fixed)})")

    an_trs, ct_trs, la, oa, lc, oc = unpack_params(theta, n_an, n_ct)
    return dict(theta=theta, history=history, an_trs=an_trs, ct_trs=ct_trs,
                loadings=(la, oa, lc, oc))
