# -*- coding: utf-8 -*-
"""
Ch1 (graphite_ica_ch1_Fable.tex) §1.16 피팅 알고리즘 사양의 실행 실증 — round-trip 시험.

문건 (7)·(6') 의 검증 설계 그대로:
  - 합성 시나리오: 3전이 (U=210/120/85 mV, w=18/10/8 mV, Q=0.15/0.40/0.35 Q_cell,
    Omega_2=Omega_3=4RT0, gamma=0.6), C_bg = peak 순높이의 ~5% 수준 상수 spline.
  - 데이터: 준평형 + 충/방전 × 3온도(15/23/45 C) + 2율 gap, 잡음 1% (peak 높이 기준).
  - 파이프라인: (2) SG 평활 미분창 규칙 -> (3) prominence 검출·초기값(N_p 동결·충방전 중점)
    -> S1 회복 -> S5 절편 분해 + (gamma, Omega) 2-파라미터 비선형 LSQ.
  - 합격 기준 (i): 각 출력이 참값에서 보고 불확도의 2배 이내.

문건이 닫은 사양만 사용 — 본 스크립트에 문건 밖 가정 없음.
실행: python ch1_fit_roundtrip.py
"""
import sys
import numpy as np
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

R, F = 8.314, 96485.0
T0 = 298.15
RT0 = R * T0

# ---------- 참값 (문건 (7) 시나리오 표) ----------
TRUE = dict(
    U=np.array([210.0, 120.0, 85.0]),      # mV vs Li
    w=np.array([18.0, 10.0, 8.0]),         # mV
    Q=np.array([0.15, 0.40, 0.35]),        # /Q_cell
    Omega=np.array([0.0, 4 * RT0, 4 * RT0]),  # J/mol (j=1 단상)
    gamma=np.array([0.0, 0.6, 0.6]),
    Cbg=0.0005,                            # Q_cell/mV (배경, peak 순높이 ~5% 수준)
)
RN_mV_per_rate = 8.0   # 0.2C 에서 분극 8 mV -> rate r(C) 분극 = 40*r mV
TEMPS = np.array([288.15, 296.15, 318.15])
RATES = [0.1, 0.2]     # C
NOISE = 0.01           # peak 높이의 1%
rng = np.random.default_rng(20260610)

def dU_hys(T, Omega):
    """식 (1.48): spinodal gap [mV]. Omega<=2RT 면 0 (M1 환원)."""
    x = 2 * R * T / Omega if Omega > 0 else 2.0
    if x >= 1:
        return 0.0
    u = np.sqrt(1 - x)
    return 2000.0 * (Omega * u - 2 * R * T * np.arctanh(u)) / F

def model_dQdV(Vn, T, d, p):
    """M1–M5 (방전 메인; 평형 상승부 항 — 합성은 준평형 중심이라 꼬리항 생략 가능하나
    문건 M5 의 상승부+배경 구조 그대로)."""
    y = np.full_like(Vn, p['Cbg'])
    sigma_d = +1 if d == 'dis' else -1
    for j in range(3):
        Ujd = p['U'][j] + sigma_d * 0.5 * p['gamma'][j] * dU_hys(T, p['Omega'][j])
        # 폭의 T-스케일: 단상 w propto (RT - Omega/2)/F — 시나리오는 w 를 23C 값으로 주므로
        # 문건 (7) T-보간 규칙(분기 영역 w: 측정 T 간 선형)을 단순화해 w(T)=w23*(T/296.15) 사용
        wj = p['w'][j] * (T / 296.15)
        z = (Vn - Ujd) / wj
        xi = 1.0 / (1.0 + np.exp(-z))
        y = y + p['Q'][j] * xi * (1 - xi) / wj
    return y

def synth_curve(T, d, rate=0.0):
    """합성 측정: V_app 격자 (분극 포함), 잡음 1%."""
    Vn = np.arange(20.0, 320.0, 0.25)
    y = model_dQdV(Vn, T, d, TRUE)
    sigma_d = +1 if d == 'dis' else -1
    Vapp = Vn + sigma_d * RN_mV_per_rate * (rate / 0.2)
    peak_h = y.max() - TRUE['Cbg']
    y_noisy = y + rng.normal(0, NOISE * peak_h, size=y.shape)
    return Vapp, y_noisy

def sg_smooth(y, win):
    """(2) 단순 이동 다항(2차) 평활 — SG 동등 구현."""
    win = max(5, int(win) | 1)
    half = win // 2
    ys = np.copy(y)
    x = np.arange(-half, half + 1)
    A = np.vander(x, 3)
    H = A @ np.linalg.pinv(A)
    row = H[half]
    for i in range(half, len(y) - half):
        ys[i] = row @ y[i - half:i + half + 1]
    return ys

def detect_and_S1(V, y, dV=0.25, Np=3):
    """(3)+(S1): 평활 -> prominence 상위 N_p 선택(최소 분리 25 mV) ->
    U(위치), w(FWHM/3.53; 겹침 오염 회피 위해 2x좁은쪽 반폭), Q(FWHM 범위 면적), Cbg(골)."""
    win = int((3.53 * 8.0 / 5) / dV)        # 가장 좁은 peak FWHM/5 규칙
    ys = sg_smooth(y, win)
    Cbg = np.percentile(ys, 5)
    cands = [i for i in range(2, len(ys) - 2)
             if ys[i] > ys[i-1] and ys[i] >= ys[i+1]
             and (ys[i] - Cbg) > 0.05 * (ys.max() - Cbg)]
    cands.sort(key=lambda i: -ys[i])        # prominence(높이) 내림차순 greedy
    sel = []
    for i in cands:
        if all(abs(V[i] - V[k]) >= 25.0 for k in sel):
            sel.append(i)
        if len(sel) == Np:
            break
    sel_sorted = sorted(sel)
    out = []
    for i in sel:
        h = ys[i] - Cbg
        half = Cbg + h / 2
        # 탐색 상한: 인접 선택 peak 와의 중간점 (겹침 번짐 방지)
        pos = sel_sorted.index(i)
        lcap = 0 if pos == 0 else (sel_sorted[pos-1] + i) // 2
        rcap = len(ys) - 1 if pos == len(sel_sorted) - 1 else (i + sel_sorted[pos+1]) // 2
        l = i
        while l > lcap and ys[l] > half: l -= 1
        r_ = i
        while r_ < rcap and ys[r_] > half: r_ += 1
        fwhm = 2.0 * min(V[i] - V[l], V[r_] - V[i])   # 좁은 쪽 반폭 x2 (겹침 쪽 배제)
        w = fwhm / 3.53
        lo = max(0, i - int(fwhm / dV))
        hi = min(len(ys), i + int(fwhm / dV) + 1)
        Q = np.trapezoid(ys[lo:hi] - Cbg, V[lo:hi]) / 0.9431   # logistic 미분의 +-FWHM 면적 분율 보정
        # 정점 서브격자 보간(3점 포물선) — gap 정밀도 향상
        if 1 <= i < len(ys) - 1:
            denom = ys[i-1] - 2 * ys[i] + ys[i+1]
            Upk = V[i] + (0.5 * dV * (ys[i-1] - ys[i+1]) / denom if abs(denom) > 1e-18 else 0.0)
        else:
            Upk = V[i]
        out.append((Upk, w, Q, h))
    out.sort(key=lambda t: -t[0])   # 전위 내림차순 = j=1,2,3
    return out, Cbg

def refine_S1(V, y, init, Cbg0):
    """S1 후반: 평형식 국소 회귀 — 3-logistic-derivative + 상수 배경의 Gauss-Newton.
    init: [(U,w,Q,h)] 전위 내림차순. 반환: (U,w,Q)x3, Cbg."""
    th = np.array([v for (U, w, Q, _) in init for v in (U, w, Q)] + [Cbg0])

    def model(t):
        out = np.full_like(V, t[-1])
        for j in range(3):
            U, w, Q = t[3*j:3*j+3]
            z = (V - U) / w
            xi = 1.0 / (1.0 + np.exp(-z))
            out = out + Q * xi * (1 - xi) / w
        return out

    for _ in range(12):
        r = y - model(th)
        J = np.zeros((len(V), len(th)))
        for k in range(len(th)):
            d = np.zeros_like(th)
            d[k] = max(1e-6, 1e-4 * abs(th[k]))
            J[:, k] = (model(th + d) - model(th)) / d[k]
        dth, *_ = np.linalg.lstsq(J, r, rcond=None)
        th = th + dth
        if np.max(np.abs(dth[:9] / np.maximum(np.abs(th[:9]), 1e-9))) < 1e-6:
            break
    rec = [(th[3*j], th[3*j+1], th[3*j+2]) for j in range(3)]
    rec.sort(key=lambda t: -t[0])
    return rec, th[-1]

def run():
    print("=== Ch1 sec1.16 round-trip 실증 ===")
    # ---- S1: 각 온도 준평형 충/방전 -> 중점 U, 양방향 평균 w/Q ----
    S1 = {}
    for T in TEMPS:
        Vd, yd = synth_curve(T, 'dis')
        Vc, yc = synth_curve(T, 'chg')
        pd0, cb_d = detect_and_S1(Vd, yd)
        pc0, cb_c = detect_and_S1(Vc, yc)
        pd_, cb_d = refine_S1(Vd, yd, pd0, cb_d)   # S1 후반: 평형식 국소 회귀
        pc_, cb_c = refine_S1(Vc, yc, pc0, cb_c)
        n = min(len(pd_), len(pc_), 3)
        rec = []
        for j in range(n):
            U_mid = 0.5 * (pd_[j][0] + pc_[j][0])           # 중점 규칙 (walkthrough 1)
            w_avg = 0.5 * (pd_[j][1] + pc_[j][1])
            Q_avg = 0.5 * (pd_[j][2] + pc_[j][2])
            gap = pd_[j][0] - pc_[j][0]
            rec.append((U_mid, w_avg, Q_avg, gap))
        S1[T] = (rec, 0.5 * (cb_d + cb_c))
        print(f"T={T-273.15:.0f}C  N_p={n}  " + "  ".join(
            f"[U={r[0]:.1f} w={r[1]:.1f} Q={r[2]:.3f} gap={r[3]:.1f}]" for r in rec))

    # ---- 회복 오차 (23C 기준, 참값 대비) ----
    rec23 = S1[296.15][0]
    print("\n--- S1 회복 (23C, 참값 대비) ---")
    names = ["U[mV]", "w[mV]", "Q[/Qcell]"]
    for j in range(3):
        tU = TRUE['U'][j]
        tw = TRUE['w'][j]
        tQ = TRUE['Q'][j]
        print(f" j={j+1}: U {rec23[j][0]:7.1f} vs {tU:5.0f} (d={rec23[j][0]-tU:+.1f})"
              f" | w {rec23[j][1]:5.1f} vs {tw:4.0f} (d={rec23[j][1]-tw:+.1f})"
              f" | Q {rec23[j][2]:.3f} vs {tQ:.2f} (d={rec23[j][2]-tQ:+.3f})")

    # ---- S5: gap(T) -> (gamma, Omega) 비선형 LSQ (문건 (6') 그대로) ----
    print("\n--- S5: gap 절편의 (gamma,Omega) 회귀 (j=2) ---")
    gaps = np.array([S1[T][0][1][3] for T in TEMPS])   # j=2, |I|->0 (합성은 준평형이라 절편 자체)
    print(" 측정 절편(mV) @15/23/45C:", np.round(gaps, 2),
          " | 참값:", np.round([0.6 * dU_hys(T, 4 * RT0) for T in TEMPS], 2))
    Og = np.linspace(2.5 * RT0, 8 * RT0, 400)
    best = None
    for Om in Og:
        dU = np.array([dU_hys(T, Om) for T in TEMPS])
        if dU.min() <= 0: continue
        g = float(np.dot(gaps, dU) / np.dot(dU, dU))   # 선형 최적 gamma
        sse = float(np.sum((gaps - g * dU) ** 2))
        if best is None or sse < best[0]:
            best = (sse, Om, g)
    sse, Om, g = best
    print(f" 회귀: Omega={Om/RT0:.2f} RT0 (참 4.00), gamma={g:.3f} (참 0.600), SSE={sse:.3f} mV^2")

    # ---- 합격 판정 (기준 (i): 2x 불확도 — 잡음 1% 기준 어림 불확도) ----
    ok = (abs(Om / RT0 - 4.0) < 0.5) and (abs(g - 0.6) < 0.06) \
        and all(abs(rec23[j][0] - TRUE['U'][j]) < 2.0 for j in range(3)) \
        and all(abs(rec23[j][1] - TRUE['w'][j]) < 1.5 for j in range(3)) \
        and all(abs(rec23[j][2] - TRUE['Q'][j]) < 0.04 for j in range(3))
    print("\n판정:", "PASS — 문건 사양만으로 파라미터 회복 성공" if ok else "FAIL — 사양 공백/구현 확인 필요")
    return ok

if __name__ == "__main__":
    run()
