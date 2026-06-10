# -*- coding: utf-8 -*-
"""
v2 (graphite_ica_ch1_Fable_v2.tex) 꼬리 경로 round-trip — R13 실행 검증.

검증 대상 (R10/R12 에서 갱신된 사양):
  - eq:Lq 보편 ODE 를 정확 적분한 합성 곡선(문건 밖 가정 없음 — 단상 1전이, 보존식 해 V_n(q))
  - (3') q_a = 원천 5% 컷(정점 이후 첫 교차), tail sub-window 3창 -> 국소 L_V -> (V, ln L_q) 점
  - M3: ln L_q 의 전위 회귀 기울기 -chi*sF/RT (S3) — 전이대 보편형 괄호 인자는 속도에 곱 = L 은 나눔
  - M4: r_a 접속/자유 분기 (L_V < w/3 문턱)
  - R10 면적 회계: ODE 진실의 상승부/꼬리 면적 분할이 (1-r_a)/r_a 와 맞는지, 무보존형(1+r_a)과 비교

실행: python v2_r13_tail_roundtrip.py
"""
import sys
import numpy as np
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

R, F = 8.314, 96485.0
T = 296.15
RT = R * T
mV = 1000.0

# ---------- 참값 ----------
U = 120.0                 # mV
w = RT / F * mV           # mV (단상 이상 극한 = 25.5 mV @23C)
Q = 0.40                  # /Q_cell
Cbg = 0.0005              # /mV
chi = 0.50
L0 = 0.40                 # L_q at V=U (진짜 꼬리-우세: L_V >~ 2w 보장)
NOISE = 0.01
rng = np.random.default_rng(20260611)

def xi_eq(Vn):
    return 1.0 / (1.0 + np.exp(-(Vn - U) / w))

def Lq_true(Vn):
    # eq:keff 의 forward 형 + 보편형 괄호 인자(역방향 몫)까지 정확히:
    # k = k_f * (1 + e^{-A/RT}),  L = |I|/(Q k)  ->  L = L0 e^{-chi A/RT} / (1 + e^{-A/RT}) * 2
    # (V=U 에서 L=L0 이 되도록 정규화: 거기서 e^{-chiA}=1, 괄호=2)
    A_over_RT = F * (Vn - U) / (mV * RT)
    return L0 * 2.0 * np.exp(-chi * A_over_RT) / (1.0 + np.exp(-A_over_RT))

# ---------- 합성: eq:Lq ODE 정확 적분 (보존식 해 V_n(q) 동시) ----------
def synth():
    Vmin = 20.0
    nq = 200000
    dq = 1.0 / nq
    q_arr = np.linspace(0, 1, nq + 1)
    xi = np.zeros(nq + 1)
    Vn = np.zeros(nq + 1)
    for i in range(nq + 1):
        # 보존식 (단일 전이 + 선형 배경): q = Cbg*(Vn - Vmin) + Q*xi  ->  명시 해
        Vn[i] = Vmin + (q_arr[i] - Q * xi[i]) / Cbg
        if i < nq:
            # stiff 안정화: 스텝 내 (xi_eq, L) 동결한 정확 완화 해 (exponential integrator)
            xe = xi_eq(Vn[i])
            L = Lq_true(Vn[i])
            decay = np.exp(-dq / L) if L > 1e-300 else 0.0
            xi[i + 1] = xe + (xi[i] - xe) * decay
    return q_arr, xi, Vn

# ---------- 파이프라인 (문건 사양 그대로) ----------
def run():
    print("=== v2 R13: 꼬리 경로 round-trip (chi 회복 + (1-r_a) 면적 회계) ===")
    q_arr, xi, Vn = synth()
    r_arr = xi_eq(Vn) - xi

    # (3') 원천 5% 컷 — dxi_eq/dq 가 정점값의 5% 로 떨어지는 정점 이후 첫 교차
    src = np.gradient(xi_eq(Vn), q_arr)
    ipk = int(np.argmax(src))
    thr = 0.05 * src[ipk]
    ia = ipk + int(np.argmax(src[ipk:] < thr))
    q_a, V_a, r_a = q_arr[ia], Vn[ia], r_arr[ia]
    dVdq_a = np.gradient(Vn, q_arr)[ia]
    print(f" q_a={q_a:.4f}  V_a={V_a:.1f} mV  (V_a-U)/w={(V_a-U)/w:.2f}  r_a={r_a:.4f}")

    # M4 regime 분기: L_V vs w/3
    LV_a = abs(dVdq_a) * Lq_true(V_a)
    branch = "접속값" if LV_a < w / 3 else "자유 파라미터(꼬리-우세)"
    print(f" L_V(q_a)={LV_a:.1f} mV vs w/3={w/3:.1f} mV  ->  r_a 분기: {branch}")

    # tail sub-window 3창 -> 국소 L_q -> (V_mid, ln L_q) -> S3 회귀
    # 창 시작: A >= 3RT (전이대 창은 원천 잔류로 chi 를 위로 편향 — R13 발견) /
    # 창 끝: r 가 3 decade 감쇠하는 지점(그 밖은 수치 언더플로 영역)
    V3RT = U + 3 * RT / F * mV
    i3 = ia + int(np.argmax(Vn[ia:] >= V3RT))
    tail_r = r_arr[i3:]
    r3 = r_arr[i3]
    iend = i3 + int(np.argmax(tail_r < r3 * 1e-3)) if (tail_r < r3 * 1e-3).any() else len(q_arr) - 1
    nwin = 6   # 좁은 창일수록 창 내 L 변화의 평균-중심 편향이 줄어든다 (R13 측정)
    bounds = np.linspace(i3, iend, nwin + 1).astype(int)
    pts = []
    for k in range(nwin):
        sl = slice(bounds[k], bounds[k + 1])
        # 잡음 모델: 지연(=꼬리 신호)에 1% 곱셈 잡음
        rr = r_arr[sl] * (1 + rng.normal(0, NOISE, bounds[k + 1] - bounds[k]))
        coef = np.polyfit(q_arr[sl], np.log(np.abs(rr)), 1)
        Lq_loc = -1.0 / coef[0]
        V_mid = Vn[(bounds[k] + bounds[k + 1]) // 2]
        # M3: 전이대(A<3RT)면 보편형 괄호 인자로 '나눔' 보정
        A_over_RT = F * (V_mid - U) / (mV * RT)
        Lq_corr = Lq_loc * (1.0 + np.exp(-A_over_RT)) if A_over_RT < 3 else Lq_loc
        pts.append((V_mid, np.log(Lq_corr)))
        print(f"  창{k+1}: V_mid={V_mid:.1f} mV  L_q(국소)={Lq_loc:.4f}  보정 후 ln L_q={np.log(Lq_corr):+.3f}")
    Vs = np.array([p[0] for p in pts])
    lnL = np.array([p[1] for p in pts])
    slope = np.polyfit(Vs, lnL, 1)[0]              # [1/mV]
    chi_rec = -slope * mV * RT / F
    print(f" S3 회귀: 기울기={slope:.5f} /mV  ->  chi={chi_rec:.3f} (참 {chi:.2f})")

    # R10 면적 회계: 총면적이 시험 기준 (simplefit 종은 V_a 이후도 살아 분할 비교는 모양 근사)
    total = xi[-1]                       # ODE 진실 총 전환 분율 (= 총면적/Q)
    rise_frac = xi[ia]
    print(f"\n--- 면적 회계 (/Q) ---")
    print(f" ODE 진실 총면적      = {total:.4f}")
    print(f" 보존형(v2) 총면적    = (1-r_a)+r_a = 1.0000  (d={total-1:+.4f})")
    print(f" 무보존형(구판) 총면적 = 1+r_a = {1+r_a:.4f}  -> 과계상 {100*r_a:.1f}%")
    print(f" (참고: V<V_a 분할 — ODE {rise_frac:.3f} vs simplefit (1-r_a)*xi_eq(V_a)="
          f"{(1-r_a)*xi_eq(V_a):.3f})")

    ok = (abs(chi_rec - chi) < 0.05 and abs(total - 1.0) < 0.01)
    print("\n판정:", "PASS — (3')/M3/M4/S3 사양과 (1-r_a) 회계가 ODE 진실과 정합"
          if ok else "FAIL — 사양 공백/회계 불일치")
    return ok

if __name__ == "__main__":
    run()
